#!/usr/bin/env python3
"""Resumable Stage 9 IndoBERT fine-tuning script with fixed EarlyStoppingCallback metric prefix.

Fixes:
1. EarlyStoppingCallback metric-prefix inconsistency:
   - Previously, post-training evaluation used `metric_key_prefix='validation'`, but EarlyStoppingCallback
     hardcoded a search for `eval_{metric_for_best_model}`. This caused the warning:
     "early stopping required metric_for_best_model, but did not find eval_f1_promotion so early stopping is disabled".
   - In this fixed version, `RobustEarlyStoppingCallback` is prefix-agnostic, supporting `eval_`, `validation_`,
     or unprefixed metric names.
   - All evaluation calls consistently use `metric_key_prefix='eval'`.
2. Adds configurable `--max-epochs` override to evaluate longer training limits without modifying frozen configs.
3. Strict scientific constraints:
   - Only uses training and validation data (never touches the frozen test set).
   - Preserves all model architectures, tokenizers, seeds, and class weights.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, shutil, sys, time, uuid, platform
from pathlib import Path
from datetime import datetime, timezone
import logging

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, Subset
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedShuffleSplit
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments,
                          TrainerCallback, EarlyStoppingCallback, set_seed)
from transformers.trainer_callback import TrainerControl, TrainerState

logger = logging.getLogger(__name__)


def sha256_file(path: Path, chunk_size=1024*1024) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk_size)
            if not b: break
            h.update(b)
    return h.hexdigest()


def atomic_json(path: Path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp-' + uuid.uuid4().hex)
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=_json_default)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def _json_default(obj):
    if isinstance(obj, (np.integer,)): return int(obj)
    if isinstance(obj, (np.floating,)): return float(obj)
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, Path): return str(obj)
    return str(obj)


def json_read(path: Path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def valid_checkpoint(path: Path) -> bool:
    if not path.is_dir(): return False
    has_model = (path / 'model.safetensors').exists() or (path / 'pytorch_model.bin').exists()
    required = ['optimizer.pt', 'scheduler.pt', 'trainer_state.json']
    return has_model and all((path / n).is_file() and (path / n).stat().st_size > 0 for n in required)


def checkpoint_step(p: Path) -> int:
    try: return int(p.name.split('-')[-1])
    except Exception: return -1


def find_persistent_checkpoints(cand_root: Path):
    ckpt_dir = cand_root / 'checkpoints'
    if not ckpt_dir.exists(): return []
    valid = [p for p in ckpt_dir.glob('checkpoint-*') if valid_checkpoint(p)]
    return sorted(valid, key=checkpoint_step)


def sync_checkpoint(local_cp: Path, cand_root: Path, state: TrainerState):
    ckpt_dir = cand_root / 'checkpoints'; ckpt_dir.mkdir(parents=True, exist_ok=True)
    dest = ckpt_dir / local_cp.name
    if dest.exists(): shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(local_cp, dest)
    if not valid_checkpoint(dest): raise RuntimeError(f'Checkpoint tidak valid setelah copy: {dest}')
    record = {
        'last_checkpoint': str(dest),
        'last_step': int(state.global_step),
        'best_checkpoint': str(state.best_model_checkpoint) if state.best_model_checkpoint else None,
        'best_metric': float(state.best_metric) if state.best_metric is not None else None,
        'updated_at_utc': datetime.now(timezone.utc).isoformat()
    }
    atomic_json(cand_root / 'checkpoint_state.json', record)


def sync_dir(src: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists(): shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(src, dest)
    return dest


def sync_persistent_checkpoints_to_local(cand_root: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for cp in find_persistent_checkpoints(cand_root):
        local = output_dir / cp.name
        if local.exists(): shutil.rmtree(local, ignore_errors=True)
        shutil.copytree(cp, local)
        if not valid_checkpoint(local): raise RuntimeError(f'Checkpoint gagal dipulihkan ke workspace: {local}')
    candidates = [p for p in output_dir.glob('checkpoint-*') if valid_checkpoint(p)]
    if not candidates: return None
    return sorted(candidates, key=checkpoint_step)[-1]


class PersistentCheckpointCallback(TrainerCallback):
    def __init__(self, cand_root: Path): self.cand_root = Path(cand_root)
    def on_save(self, args, state, control, **kwargs):
        local = Path(args.output_dir) / f'checkpoint-{state.global_step}'
        if local.exists():
            sync_checkpoint(local, self.cand_root, state)
        return control


class PauseAfterStepCallback(TrainerCallback):
    def __init__(self, pause_after_step: int): self.pause_after_step = pause_after_step
    def on_step_end(self, args, state, control, **kwargs):
        if self.pause_after_step > 0 and state.global_step >= self.pause_after_step:
            control.should_training_stop = True
        return control


class RobustEarlyStoppingCallback(EarlyStoppingCallback):
    """EarlyStoppingCallback with prefix-agnostic metric resolution.
    
    Resolves the warning by matching against 'eval_{metric}', 'validation_{metric}',
    or bare '{metric}' so that custom metric_key_prefix values never disable early stopping.
    """
    def on_evaluate(self, args, state, control, metrics, **kwargs):
        raw_metric = args.metric_for_best_model
        base_name = raw_metric.replace("eval_", "").replace("validation_", "")
        
        candidates = [
            raw_metric,
            f"eval_{base_name}",
            f"validation_{base_name}",
            base_name
        ]
        
        metric_value = None
        for cand in candidates:
            if cand in metrics:
                metric_value = metrics[cand]
                break
                
        if metric_value is None:
            logger.warning(
                f"[RobustEarlyStoppingCallback] metric_for_best_model ({raw_metric}) "
                f"tidak ditemukan di metrics keys: {list(metrics.keys())}. Early stopping dinonaktifkan."
            )
            return

        self.check_metric_value(args, state, control, metric_value)
        if self.early_stopping_patience_counter >= self.early_stopping_patience:
            control.should_training_stop = True


class ArrayDataset(Dataset):
    def __init__(self, cache_path: Path):
        z = np.load(cache_path, allow_pickle=False)
        self.input_ids = torch.from_numpy(z['input_ids'].astype(np.int64, copy=False))
        self.attention_mask = torch.from_numpy(z['attention_mask'].astype(np.int64, copy=False))
        self.token_type_ids = torch.from_numpy(z['token_type_ids'].astype(np.int64, copy=False)) if 'token_type_ids' in z.files else None
        self.labels = torch.from_numpy(z['labels'].astype(np.int64, copy=False))
    def __len__(self): return len(self.labels)
    def __getitem__(self, idx):
        row = {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_mask[idx], 'labels': self.labels[idx]}
        if self.token_type_ids is not None: row['token_type_ids'] = self.token_type_ids[idx]
        return row


class WeightedTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = torch.tensor(class_weights, dtype=torch.float32) if class_weights is not None else None
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop('labels')
        outputs = model(**inputs)
        weights = self.class_weights.to(outputs.logits.device) if self.class_weights is not None else None
        loss = nn.CrossEntropyLoss(weight=weights)(outputs.logits, labels)
        return (loss, outputs) if return_outputs else loss


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    cm = confusion_matrix(labels, preds, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return {
        'f1_promotion': float(f1_score(labels, preds, pos_label=1, zero_division=0)),
        'precision_promotion': float(precision_score(labels, preds, pos_label=1, zero_division=0)),
        'recall_promotion': float(recall_score(labels, preds, pos_label=1, zero_division=0)),
        'accuracy': float(accuracy_score(labels, preds)),
        'macro_f1': float(f1_score(labels, preds, average='macro', zero_division=0)),
        'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp)
    }


def set_all_seeds(seed=42):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)
    set_seed(seed)


def build_args(candidate, config, output_dir, mode, max_epochs_override=None):
    t = config['training']
    num_epochs = max_epochs_override if max_epochs_override is not None else int(t['max_epochs'])
    
    if mode == 'smoke':
        return TrainingArguments(
            output_dir=str(output_dir), overwrite_output_dir=False,
            learning_rate=float(candidate['learning_rate']), weight_decay=float(candidate['weight_decay']),
            per_device_train_batch_size=4, per_device_eval_batch_size=8, gradient_accumulation_steps=1,
            num_train_epochs=1, max_steps=4, fp16=True, gradient_checkpointing=False,
            logging_strategy='steps', logging_steps=1, eval_strategy='no', save_strategy='steps', save_steps=2,
            save_total_limit=2, save_safetensors=True, report_to='none', seed=int(config['seed']), data_seed=int(config['seed']),
            dataloader_num_workers=0, dataloader_pin_memory=True
        )
    return TrainingArguments(
        output_dir=str(output_dir), overwrite_output_dir=False,
        learning_rate=float(candidate['learning_rate']), weight_decay=float(candidate['weight_decay']),
        per_device_train_batch_size=int(t['per_device_train_batch_size']),
        per_device_eval_batch_size=int(t['per_device_eval_batch_size']),
        gradient_accumulation_steps=int(t['gradient_accumulation_steps']),
        num_train_epochs=num_epochs, fp16=True, bf16=False,
        gradient_checkpointing=True, max_grad_norm=float(t['max_grad_norm']),
        warmup_ratio=float(t['warmup_ratio']), lr_scheduler_type='linear', optim='adamw_torch',
        logging_strategy='steps', logging_steps=int(t['logging_steps']), eval_strategy='epoch', save_strategy='epoch',
        save_total_limit=2, save_safetensors=True, load_best_model_at_end=True,
        metric_for_best_model='f1_promotion', greater_is_better=True,
        report_to='none', seed=int(config['seed']), data_seed=int(config['seed']),
        dataloader_num_workers=int(t['dataloader_num_workers']), dataloader_pin_memory=True,
        logging_dir=str(output_dir / 'tensorboard'),
        label_names=['labels']
    )


def load_train_val(workspace):
    train_path = workspace / 'data_snapshot' / 'train_v1.csv'
    val_path = workspace / 'data_snapshot' / 'validation_v1.csv'
    if not train_path.exists() or not val_path.exists():
        raise FileNotFoundError('data_snapshot train/validation CSV tidak ditemukan di workspace.')
    tr = pd.read_csv(train_path, low_memory=False); va = pd.read_csv(val_path, low_memory=False)
    for name, df, n, p, nprom in [('train', tr, 32920, 3960, 28960), ('validation', va, 4116, 495, 3621)]:
        required = {'record_id', 'text_raw', 'canonical_label'}
        if required - set(df.columns): raise RuntimeError(f'{name}: kolom hilang {required - set(df.columns)}')
        if len(df) != n: raise RuntimeError(f'{name}: jumlah baris {len(df)} != {n}')
        if df['record_id'].duplicated().any(): raise RuntimeError(f'{name}: record_id duplikat')
        if df[['text_raw', 'canonical_label']].isna().any().any(): raise RuntimeError(f'{name}: nilai null')
        y = pd.to_numeric(df['canonical_label']).astype(int)
        if set(y.unique()) != {0, 1}: raise RuntimeError(f'{name}: label bukan 0/1')
        if int((y == 1).sum()) != p or int((y == 0).sum()) != nprom: raise RuntimeError(f'{name}: distribusi label tidak sesuai')
        df['canonical_label'] = y
    if set(tr.record_id.astype(str)) & set(va.record_id.astype(str)): raise RuntimeError('record_id overlap train/validation')
    return tr, va
