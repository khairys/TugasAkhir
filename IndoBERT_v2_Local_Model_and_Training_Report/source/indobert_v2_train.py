#!/usr/bin/env python3
"""IndoBERT v2 epoch-budget experiment. Train/validation only; never loads test files."""
from __future__ import annotations
import argparse, gc, hashlib, json, os, random, re, shutil, subprocess, time, traceback
from pathlib import Path
from datetime import datetime, timezone
os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")
os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("USE_TORCH", "1")
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, Subset
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments,
    TrainerCallback, EarlyStoppingCallback, DataCollatorWithPadding, set_seed,
)
try:
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 2)))
except Exception:
    pass


def sha256_file(path: Path | str, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def json_read(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def atomic_json(path: Path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp-{os.getpid()}")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    os.replace(tmp, path)


def copytree_verified(src: Path, dst: Path):
    """Copy a tree to a temp directory then rename, so Drive never sees a partial checkpoint."""
    src, dst = Path(src), Path(dst)
    tmp = dst.with_name(dst.name + f".tmp-{os.getpid()}")
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    shutil.copytree(src, tmp)
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)
    os.replace(tmp, dst)


def set_all_seeds(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    set_seed(seed)


def load_model(snapshot_dir: Path, attention_backend: str):
    kwargs = {"local_files_only": True}
    if attention_backend in {"sdpa", "eager"}:
        kwargs["attn_implementation"] = attention_backend
    return AutoModelForSequenceClassification.from_pretrained(str(snapshot_dir), **kwargs)


class CommentDataset(Dataset):
    """Tokenized, variable-length examples. Padding occurs dynamically per batch."""
    def __init__(self, texts, labels, tokenizer, max_length: int):
        self.encodings = tokenizer(
            ["" if pd.isna(t) else str(t) for t in texts],
            add_special_tokens=True,
            truncation=True,
            max_length=int(max_length),
            padding=False,
            return_attention_mask=True,
        )
        self.labels = np.asarray(labels, dtype=np.int64)
        self.lengths = [len(ids) for ids in self.encodings["input_ids"]]

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: v[idx] for k, v in self.encodings.items()}
        item["labels"] = int(self.labels[idx])
        return item


class WeightedTrainer(Trainer):
    """Cross-entropy class weights derived only from the training labels."""
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = torch.tensor(class_weights, dtype=torch.float32) if class_weights is not None else None

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        weights = self.class_weights.to(outputs.logits.device) if self.class_weights is not None else None
        loss = nn.CrossEntropyLoss(weight=weights)(outputs.logits.float(), labels)
        return (loss, outputs) if return_outputs else loss


def compute_metrics(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=np.int64)
    y_pred = np.asarray(y_pred, dtype=np.int64)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return {
        "f1_promotion": float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "precision_promotion": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "recall_promotion": float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
    }


def trainer_compute_metrics(eval_pred):
    logits, labels = eval_pred
    return compute_metrics(labels, np.argmax(logits, axis=-1))


def gpu_status_line():
    try:
        p = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5,
        )
        return p.stdout.strip() if p.returncode == 0 else "nvidia-smi unavailable"
    except Exception as exc:
        return f"GPU telemetry unavailable: {exc}"


def attempt_training_step(snapshot_dir, tokenizer, train_ds, collator, profile, batch_size, use_gc, optimizer_kind):
    """Short throwaway CUDA forward/backward/optimizer step to select a batch that fits."""
    model = None
    optimizer = None
    scaler = None
    try:
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        set_all_seeds(42)
        model = load_model(snapshot_dir, profile.get("attention_backend", "sdpa")).cuda()
        if use_gc:
            model.gradient_checkpointing_enable()
            model.config.use_cache = False
        model.train()
        idxs = sorted(range(len(train_ds)), key=lambda i: train_ds.lengths[i], reverse=True)[:batch_size]
        batch = collator([train_ds[i] for i in idxs])
        batch = {k: v.cuda(non_blocking=True) for k, v in batch.items()}
        fused = optimizer_kind == "adamw_torch_fused"
        try:
            optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5, fused=fused)
        except (TypeError, RuntimeError):
            if fused:
                return {"ok": False, "fallback_optimizer": True, "oom": False}
            raise
        use_bf16 = profile["amp"] == "bf16"
        amp_dtype = torch.bfloat16 if use_bf16 else torch.float16
        try:
            scaler = torch.amp.GradScaler("cuda", enabled=not use_bf16)
        except Exception:
            scaler = torch.cuda.amp.GradScaler(enabled=not use_bf16)
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda", dtype=amp_dtype, enabled=True):
            outputs = model(**batch)
            loss = nn.CrossEntropyLoss()(outputs.logits.float(), batch["labels"])
        if use_bf16:
            loss.backward()
            optimizer.step()
        else:
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        torch.cuda.synchronize()
        peak_gib = torch.cuda.max_memory_allocated() / (1024**3)
        return {"ok": True, "oom": False, "peak_memory_gib": round(peak_gib, 3)}
    except (torch.cuda.OutOfMemoryError, RuntimeError) as exc:
        is_oom = isinstance(exc, torch.cuda.OutOfMemoryError) or "out of memory" in str(exc).lower()
        if is_oom:
            return {"ok": False, "oom": True, "error": str(exc)[:400]}
        raise
    except (TypeError, ValueError) as exc:
        message = str(exc).lower()
        if "attention" in message or "sdpa" in message or "attn_implementation" in message:
            return {"ok": False, "oom": False, "unsupported_attention": True, "error": str(exc)[:400]}
        raise
    finally:
        try:
            if optimizer is not None:
                optimizer.zero_grad(set_to_none=True)
        except Exception:
            pass
        del model, optimizer, scaler
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def choose_or_load_runtime_profile(profile_path, snapshot_dir, tokenizer, train_ds, collator, target_effective_batch):
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable. Set Colab Runtime > Change runtime type > GPU, then rerun from the top.")
    props = torch.cuda.get_device_properties(0)
    current_gpu = torch.cuda.get_device_name(0)
    supports_bf16 = bool(torch.cuda.is_bf16_supported())
    current_amp = "bf16" if supports_bf16 else "fp16"
    current_capability = f"{props.major}.{props.minor}"

    if profile_path.exists():
        profile = json_read(profile_path)
        if profile.get("target_effective_batch_size") != target_effective_batch:
            raise RuntimeError("Saved runtime profile conflicts with the v2 config. Start a new experiment directory rather than editing a run in progress.")
        if profile.get("amp") == "bf16" and not supports_bf16:
            raise RuntimeError("This runtime cannot resume a BF16 run. Reconnect to a BF16-capable GPU or start a new versioned run.")
        if profile.get("attention_backend") not in {"sdpa", "eager"}:
            raise RuntimeError("Invalid saved attention backend in runtime profile.")
        print(f"Using frozen runtime profile: {profile['micro_batch_size']} x {profile['gradient_accumulation_steps']} = effective {profile['effective_batch_size']}; AMP={profile['amp']}; optimizer={profile['optimizer']}")
        trial = attempt_training_step(
            snapshot_dir, tokenizer, train_ds, collator, profile,
            int(profile["micro_batch_size"]), bool(profile["gradient_checkpointing"]), str(profile["optimizer"]),
        )
        if not trial.get("ok"):
            raise RuntimeError(
                "The saved GPU/batch profile no longer fits this runtime. Do not silently change the batch size of a resumable run. "
                "Reconnect to a sufficiently large GPU or start a clean, separately versioned run. Trial: " + str(trial)
            )
        if current_gpu != profile.get("first_gpu_name"):
            print(f"WARNING: current GPU is {current_gpu}; original GPU was {profile.get('first_gpu_name')}. Settings remain frozen; monitor stability.")
        profile["last_verified_gpu_name"] = current_gpu
        profile["last_verified_at_utc"] = datetime.now(timezone.utc).isoformat()
        atomic_json(profile_path, profile)
        return profile

    total_gib = props.total_memory / (1024**3)
    preferred = 32 if total_gib >= 20 else 16
    # Keep effective batch size at 32 to make the candidate comparison coherent.
    batch_candidates = [b for b in [preferred, 16, 8, 4] if b <= preferred and target_effective_batch % b == 0]
    batch_candidates = list(dict.fromkeys(batch_candidates))
    attention_options = ["sdpa", "eager"]
    optimizer_options = ["adamw_torch_fused", "adamw_torch"]
    attempts = []
    chosen = None
    for attention in attention_options:
        for use_gc in [False, True]:
            for bs in batch_candidates:
                for optim in optimizer_options:
                    trial_profile = {
                        "amp": current_amp,
                        "attention_backend": attention,
                        "gradient_checkpointing": use_gc,
                    }
                    trial = attempt_training_step(snapshot_dir, tokenizer, train_ds, collator, trial_profile, bs, use_gc, optim)
                    attempts.append({"batch_size": bs, "gradient_checkpointing": use_gc, "attention_backend": attention, "optimizer": optim, **trial})
                    if trial.get("fallback_optimizer"):
                        continue
                    if trial.get("ok"):
                        chosen = {
                            "profile_version": 1,
                            "first_gpu_name": current_gpu,
                            "compute_capability": current_capability,
                            "gpu_total_memory_gib": round(total_gib, 3),
                            "amp": current_amp,
                            "attention_backend": attention,
                            "optimizer": optim,
                            "gradient_checkpointing": use_gc,
                            "micro_batch_size": bs,
                            "gradient_accumulation_steps": target_effective_batch // bs,
                            "effective_batch_size": target_effective_batch,
                            "target_effective_batch_size": target_effective_batch,
                            "calibration_peak_memory_gib": trial.get("peak_memory_gib"),
                            "calibration_attempts": attempts,
                            "created_at_utc": datetime.now(timezone.utc).isoformat(),
                        }
                        break
                if chosen:
                    break
            if chosen:
                break
        if chosen:
            break
    if chosen is None:
        raise RuntimeError("No CUDA batch configuration passed the memory preflight. Tried: " + json.dumps(attempts[-12:], default=str))
    atomic_json(profile_path, chosen)
    print("Selected CUDA profile:", json.dumps({k: chosen[k] for k in ["first_gpu_name", "gpu_total_memory_gib", "amp", "attention_backend", "optimizer", "gradient_checkpointing", "micro_batch_size", "gradient_accumulation_steps", "effective_batch_size", "calibration_peak_memory_gib"]}, indent=2))
    return chosen


def copy_remote_checkpoints_to_local(remote_ckpt_root: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for p in output_dir.glob("checkpoint-*"):
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
    if not remote_ckpt_root.exists():
        return None
    remote_ckpts = [p for p in remote_ckpt_root.glob("checkpoint-*") if p.is_dir() and re.fullmatch(r"checkpoint-\d+", p.name)]
    for cp in remote_ckpts:
        copytree_verified(cp, output_dir / cp.name)
    valid = [p for p in output_dir.glob("checkpoint-*") if p.is_dir() and re.fullmatch(r"checkpoint-\d+", p.name)]
    if not valid:
        return None
    return max(valid, key=lambda p: int(p.name.split("-")[-1]))


class PersistCheckpointCallback(TrainerCallback):
    """Persist full Trainer checkpoints to Drive every 2 epochs and whenever a new best is selected."""
    def __init__(self, remote_ckpt_root: Path, every_n_epochs: int = 2):
        self.remote_ckpt_root = Path(remote_ckpt_root)
        self.every_n_epochs = int(every_n_epochs)

    def on_save(self, args, state, control, **kwargs):
        current = Path(args.output_dir) / f"checkpoint-{state.global_step}"
        if not current.exists():
            return control
        epoch = int(round(float(state.epoch or 0)))
        best_path = Path(state.best_model_checkpoint) if state.best_model_checkpoint else None
        is_best = bool(best_path and best_path.name == current.name)
        should_sync = (epoch > 0 and epoch % self.every_n_epochs == 0) or is_best
        if not should_sync:
            print(f"[DRIVE CHECKPOINT] local checkpoint {current.name}; sync deferred until next even epoch unless it becomes best.", flush=True)
            return control

        self.remote_ckpt_root.mkdir(parents=True, exist_ok=True)
        copytree_verified(current, self.remote_ckpt_root / current.name)
        keep = {current.name}
        if best_path and best_path.exists():
            if not (self.remote_ckpt_root / best_path.name).exists():
                copytree_verified(best_path, self.remote_ckpt_root / best_path.name)
            keep.add(best_path.name)
        for other in self.remote_ckpt_root.glob("checkpoint-*"):
            if other.is_dir() and other.name not in keep:
                shutil.rmtree(other, ignore_errors=True)
        print(f"[DRIVE CHECKPOINT] persisted {current.name}; best={best_path.name if best_path else 'not-set'}; kept={sorted(keep)}", flush=True)
        return control


class EpochTelemetryCallback(TrainerCallback):
    def on_epoch_end(self, args, state, control, **kwargs):
        print(f"[GPU MONITOR] epoch={state.epoch:.2f}; GPU util,memory_used,total MiB={gpu_status_line()}; allocated={torch.cuda.memory_allocated()/1024**3:.2f} GiB; reserved={torch.cuda.memory_reserved()/1024**3:.2f} GiB; peak={torch.cuda.max_memory_allocated()/1024**3:.2f} GiB", flush=True)
        return control


def ensure_identity(candidate_root: Path, identity: dict):
    p = candidate_root / "experiment_identity.json"
    if p.exists():
        old = json_read(p)
        if old != identity:
            raise RuntimeError(
                f"Experiment identity mismatch for {candidate_root.name}. Configuration, data, code, initial weights, or batch/AMP profile changed. "
                "Do not resume with a changed identity; create a new versioned run."
            )
    else:
        if (candidate_root / "checkpoints").exists() and any((candidate_root / "checkpoints").glob("checkpoint-*")):
            raise RuntimeError(f"Checkpoints exist but identity is missing at {candidate_root}; refusing unsafe resume.")
        atomic_json(p, identity)


def build_training_args(config, profile, output_dir: Path, num_workers: int, candidate: dict):
    t = config["training"]
    return TrainingArguments(
        output_dir=str(output_dir),
        overwrite_output_dir=True,
        num_train_epochs=int(t["max_epochs"]),
        per_device_train_batch_size=int(profile["micro_batch_size"]),
        per_device_eval_batch_size=int(t["per_device_eval_batch_size"]),
        gradient_accumulation_steps=int(profile["gradient_accumulation_steps"]),
        learning_rate=float(candidate["learning_rate"]),
        weight_decay=float(candidate["weight_decay"]),
        warmup_ratio=float(t["warmup_ratio"]),
        lr_scheduler_type="linear",
        max_grad_norm=float(t["max_grad_norm"]),
        fp16=(profile["amp"] == "fp16"),
        bf16=(profile["amp"] == "bf16"),
        tf32=bool(profile.get("tf32", False)),
        gradient_checkpointing=bool(profile["gradient_checkpointing"]),
        gradient_checkpointing_kwargs={"use_reentrant": False} if profile["gradient_checkpointing"] else None,
        optim=str(profile["optimizer"]),
        logging_strategy="steps",
        logging_steps=int(t["logging_steps"]),
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        save_safetensors=True,
        load_best_model_at_end=True,
        metric_for_best_model="f1_promotion",
        greater_is_better=True,
        group_by_length=True,
        dataloader_num_workers=int(num_workers),
        dataloader_pin_memory=True,
        dataloader_persistent_workers=(int(num_workers) > 0),
        report_to="none",
        seed=int(config["seed"]),
        data_seed=int(config["seed"]),
        label_names=["labels"],
        disable_tqdm=False,
    )


def run_candidate(candidate, config, profile, tokenizer, train_ds, val_ds, val_df, class_weights,
                  snapshot_dir, workspace, persist, identity_base, num_workers):
    cid = candidate["candidate_id"]
    cand_root = persist / "candidates" / cid
    cand_root.mkdir(parents=True, exist_ok=True)
    result_path = cand_root / "result.json"
    final_model_drive = cand_root / "best_model"
    identity = {**identity_base, "candidate_id": cid, "candidate": candidate}
    ensure_identity(cand_root, identity)

    if result_path.exists() and (final_model_drive / "config.json").exists() and (final_model_drive / "model.safetensors").exists():
        result = json_read(result_path)
        if result.get("status") == "SUCCESS" and result.get("identity_sha256") == hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest():
            print(f"\n[SKIP] {cid} already completed with matching identity; F1={result['validation_metrics']['f1_promotion']:.4f}")
            shutil.rmtree(cand_root / "checkpoints", ignore_errors=True)
            return result
        raise RuntimeError(f"Result exists but identity does not match for {cid}. Do not overwrite; audit the run directory.")

    out_dir = workspace / "runs" / cid
    out_dir.mkdir(parents=True, exist_ok=True)
    remote_ckpt_root = cand_root / "checkpoints"
    resume_path = copy_remote_checkpoints_to_local(remote_ckpt_root, out_dir)
    if resume_path:
        print(f"[RESUME] {cid} from {resume_path.name}; saved checkpoint step {resume_path.name.split('-')[-1]}")
    else:
        print(f"\n[START] {cid} from the identical initial IndoBERT snapshot.")

    set_all_seeds(int(config["seed"]))
    model = load_model(snapshot_dir, profile["attention_backend"])
    model.config.id2label = {0: "Non-Promotion", 1: "Promotion"}
    model.config.label2id = {"Non-Promotion": 0, "Promotion": 1}
    model.config.use_cache = False
    args = build_training_args(config, profile, out_dir, num_workers, candidate)
    if args.device.type != "cuda":
        raise RuntimeError(f"Trainer selected {args.device}, not CUDA. Training aborted.")
    print(f"[DEVICE] {args.device}; GPU={torch.cuda.get_device_name(0)}; microbatch={args.per_device_train_batch_size}; accumulation={args.gradient_accumulation_steps}; effective batch={args.per_device_train_batch_size * args.gradient_accumulation_steps}; AMP={profile['amp']}; attention={profile['attention_backend']}; optimizer={profile['optimizer']}; gradient checkpointing={profile['gradient_checkpointing']}")

    callbacks = [
        EarlyStoppingCallback(early_stopping_patience=int(config["training"]["early_stopping_patience"])),
        PersistCheckpointCallback(remote_ckpt_root, every_n_epochs=int(config["training"]["drive_checkpoint_every_n_epochs"])),
        EpochTelemetryCallback(),
    ]
    trainer = WeightedTrainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer, pad_to_multiple_of=8),
        processing_class=tokenizer,
        compute_metrics=trainer_compute_metrics,
        class_weights=class_weights,
        callbacks=callbacks,
    )
    if trainer.args.device.type != "cuda":
        raise RuntimeError("Trainer/Accelerate did not select CUDA; refusing CPU training.")
    first_param_device = next(trainer.model.parameters()).device
    print(f"[MODEL DEVICE] {first_param_device}; Trainer device={trainer.args.device}")
    if first_param_device.type != "cuda":
        raise RuntimeError(f"Model parameters are on {first_param_device}, not CUDA; refusing to train on CPU.")

    t0 = time.time()
    train_out = trainer.train(resume_from_checkpoint=str(resume_path) if resume_path else None)
    train_seconds = time.time() - t0

    # load_best_model_at_end=True has restored the best checkpoint based on validation F1.
    local_best = out_dir / "best_model_export"
    if local_best.exists():
        shutil.rmtree(local_best, ignore_errors=True)
    trainer.save_model(str(local_best))
    tokenizer.save_pretrained(local_best)

    # Predict validation only; there is intentionally no code path for test data.
    pred_out = trainer.predict(val_ds, metric_key_prefix="validation")
    logits = pred_out.predictions[0] if isinstance(pred_out.predictions, tuple) else pred_out.predictions
    y_pred = np.argmax(logits, axis=-1).astype(np.int64)
    y_true = val_df["canonical_label"].to_numpy(dtype=np.int64)
    metrics = compute_metrics(y_true, y_pred)
    pred_probs = torch.softmax(torch.tensor(logits, dtype=torch.float32), dim=-1).numpy()[:, 1]
    pred_df = pd.DataFrame({
        "record_id": val_df["record_id"].astype(str).to_numpy(),
        "canonical_label": y_true,
        "pred_label": y_pred,
        "prob_promotion": pred_probs,
    })
    pred_df.to_csv(cand_root / "validation_predictions.csv", index=False)
    history = trainer.state.log_history
    atomic_json(cand_root / "training_history.json", history)
    copytree_verified(local_best, final_model_drive)

    eval_logs = [x for x in history if "eval_f1_promotion" in x]
    best_epoch = None
    if eval_logs:
        best_log = max(eval_logs, key=lambda x: (float(x.get("eval_f1_promotion", -1)), -int(x.get("epoch", 9999))))
        best_epoch = best_log.get("epoch")
    identity_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    result = {
        "status": "SUCCESS",
        "candidate_id": cid,
        "candidate": candidate,
        "validation_metrics": metrics,
        "trainer_best_metric": float(trainer.state.best_metric) if trainer.state.best_metric is not None else None,
        "trainer_best_checkpoint": str(trainer.state.best_model_checkpoint) if trainer.state.best_model_checkpoint else None,
        "best_epoch_from_history": best_epoch,
        "max_epochs": int(config["training"]["max_epochs"]),
        "train_runtime_seconds": round(train_seconds, 2),
        "train_runtime_minutes": round(train_seconds / 60, 2),
        "train_output_metrics": train_out.metrics,
        "runtime_profile": profile,
        "identity_sha256": identity_hash,
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    atomic_json(result_path, result)
    # Finished candidates need only best-model weights + report; remove large optimizer checkpoints.
    shutil.rmtree(remote_ckpt_root, ignore_errors=True)
    shutil.rmtree(out_dir, ignore_errors=True)
    del trainer, model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"[DONE] {cid}: F1={metrics['f1_promotion']:.4f}; Precision={metrics['precision_promotion']:.4f}; Recall={metrics['recall_promotion']:.4f}; best epoch={best_epoch}; runtime={train_seconds/60:.1f} min")
    return result


def run_integration_smoke(config, profile, tokenizer, train_ds, class_weights, snapshot_dir, workspace, persist, config_sha, script_sha):
    """Run four throwaway optimizer steps before the long experiment; never used as a result."""
    marker = persist / "project" / "cuda_smoke_preflight.json"
    profile_identity = {k: profile.get(k) for k in ["amp", "attention_backend", "optimizer", "gradient_checkpointing", "micro_batch_size", "gradient_accumulation_steps", "effective_batch_size", "tf32"]}
    identity = {
        "config_sha256": config_sha,
        "script_sha256": script_sha,
        "profile": profile_identity,
    }
    identity_sha = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    if marker.exists():
        prior = json_read(marker)
        if prior.get("status") == "SUCCESS" and prior.get("identity_sha256") == identity_sha:
            print("[SMOKE] Existing CUDA integration smoke is valid; skipping.")
            return
        raise RuntimeError("CUDA smoke marker exists with a different identity. Do not overwrite; start a clean versioned run.")

    smoke_dir = workspace / "cuda_smoke"
    if smoke_dir.exists():
        shutil.rmtree(smoke_dir, ignore_errors=True)
    # Use a small subset of normal training rows only. Four optimizer steps check integration, not model quality.
    subset_size = min(512, len(train_ds))
    smoke_ds = Subset(train_ds, list(range(subset_size)))
    candidate = config["candidates"][0]
    set_all_seeds(int(config["seed"]))
    model = load_model(snapshot_dir, profile["attention_backend"])
    args = TrainingArguments(
        output_dir=str(smoke_dir), overwrite_output_dir=True,
        num_train_epochs=1, max_steps=4,
        per_device_train_batch_size=int(profile["micro_batch_size"]),
        per_device_eval_batch_size=16,
        gradient_accumulation_steps=int(profile["gradient_accumulation_steps"]),
        learning_rate=float(candidate["learning_rate"]), weight_decay=float(candidate["weight_decay"]),
        warmup_ratio=0.0, lr_scheduler_type="linear", max_grad_norm=float(config["training"]["max_grad_norm"]),
        fp16=(profile["amp"] == "fp16"), bf16=(profile["amp"] == "bf16"), tf32=bool(profile.get("tf32", False)),
        gradient_checkpointing=bool(profile["gradient_checkpointing"]),
        gradient_checkpointing_kwargs={"use_reentrant": False} if profile["gradient_checkpointing"] else None,
        optim=str(profile["optimizer"]), logging_strategy="steps", logging_steps=1,
        eval_strategy="no", save_strategy="no", group_by_length=True,
        dataloader_num_workers=0, dataloader_pin_memory=True, report_to="none", disable_tqdm=True,
        seed=int(config["seed"]), data_seed=int(config["seed"]), label_names=["labels"],
    )
    if args.device.type != "cuda":
        raise RuntimeError("Smoke TrainingArguments did not select CUDA.")
    trainer = WeightedTrainer(
        model=model, args=args, train_dataset=smoke_ds,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer, pad_to_multiple_of=8),
        processing_class=tokenizer, class_weights=class_weights,
    )
    if next(trainer.model.parameters()).device.type != "cuda":
        raise RuntimeError("Smoke model is not on CUDA; refusing to start official candidates.")
    t0 = time.time()
    out = trainer.train()
    elapsed = time.time() - t0
    if int(trainer.state.global_step) != 4:
        raise RuntimeError(f"CUDA smoke expected 4 optimizer steps, got {trainer.state.global_step}.")
    atomic_json(marker, {
        "status": "SUCCESS", "identity_sha256": identity_sha,
        "optimizer_steps": int(trainer.state.global_step), "runtime_seconds": round(elapsed, 2),
        "profile": profile_identity, "test_set_used": False,
        "note": "Throwaway integration smoke only; not a candidate result.",
    })
    del trainer, model
    gc.collect()
    torch.cuda.empty_cache()
    shutil.rmtree(smoke_dir, ignore_errors=True)
    print(f"[SMOKE PASS] 4 CUDA optimizer steps in {elapsed:.1f}s using {profile['micro_batch_size']} x {profile['gradient_accumulation_steps']} microbatch/accumulation.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--persistent-root", required=True)
    args = ap.parse_args()
    workspace = Path(args.workspace).resolve()
    persist = Path(args.persistent_root).resolve()
    project = persist / "project"
    config_path = project / "indobert_v2.json"
    script_path = project / "indobert_v2_train.py"
    snapshot_dir = workspace / "pretrained_snapshot"
    train_path = workspace / "data_snapshot" / "train_v1.csv"
    val_path = workspace / "data_snapshot" / "validation_v1.csv"
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available. This notebook intentionally refuses to run on CPU.")
    if not config_path.is_file() or not snapshot_dir.joinpath("config.json").is_file():
        raise FileNotFoundError("Config or pretrained initialization snapshot missing; rerun setup cells first.")
    config = json_read(config_path)
    train_sha, val_sha = sha256_file(train_path), sha256_file(val_path)
    if train_sha != config["data"]["train_sha256"] or val_sha != config["data"]["validation_sha256"]:
        raise RuntimeError("Data SHA-256 does not match frozen v2 config.")
    train_df = pd.read_csv(train_path, low_memory=False)
    val_df = pd.read_csv(val_path, low_memory=False)
    if len(train_df) != 32920 or len(val_df) != 4116:
        raise RuntimeError(f"Unexpected split sizes: train={len(train_df)}, validation={len(val_df)}")
    for name, frame, expected_prom in [("train", train_df, 3960), ("validation", val_df, 495)]:
        if not {"record_id", "text_raw", "canonical_label"}.issubset(frame.columns):
            raise RuntimeError(f"Missing required columns in {name}.")
        if frame["record_id"].duplicated().any() or frame[["text_raw", "canonical_label"]].isna().any().any():
            raise RuntimeError(f"Duplicate IDs/null values in {name}.")
        labels = pd.to_numeric(frame["canonical_label"]).astype(int)
        if not set(labels.unique()) == {0, 1} or int((labels == 1).sum()) != expected_prom:
            raise RuntimeError(f"Unexpected labels in {name}.")
        frame["canonical_label"] = labels
    if set(train_df.record_id.astype(str)) & set(val_df.record_id.astype(str)):
        raise RuntimeError("Train/validation record_id overlap.")
    if "leakage_group_id" in train_df.columns and "leakage_group_id" in val_df.columns:
        if set(train_df.leakage_group_id.astype(str)) & set(val_df.leakage_group_id.astype(str)):
            raise RuntimeError("Train/validation leakage-group overlap.")

    init_manifest_path = project / "pretrained_model_manifest.json"
    init_manifest = json_read(init_manifest_path)
    weight_name = init_manifest["weights_file"]
    weights_path = snapshot_dir / weight_name
    if not weights_path.exists() or sha256_file(weights_path) != init_manifest["weights_sha256"]:
        raise RuntimeError("Initial IndoBERT snapshot hash mismatch.")
    tokenizer = AutoTokenizer.from_pretrained(str(snapshot_dir), local_files_only=True, use_fast=True)
    max_length = int(config["encoding"]["max_length"])
    print("Tokenizing train/validation once with dynamic padding (no test files opened)...", flush=True)
    t0 = time.time()
    train_ds = CommentDataset(train_df["text_raw"].tolist(), train_df["canonical_label"].to_numpy(), tokenizer, max_length)
    val_ds = CommentDataset(val_df["text_raw"].tolist(), val_df["canonical_label"].to_numpy(), tokenizer, max_length)
    print(f"Tokenization complete in {time.time()-t0:.1f}s; train avg tokens={np.mean(train_ds.lengths):.1f}; validation avg tokens={np.mean(val_ds.lengths):.1f}; max={max(train_ds.lengths)}", flush=True)
    collator = DataCollatorWithPadding(tokenizer=tokenizer, pad_to_multiple_of=8)

    target_batch = int(config["training"]["effective_batch_size"])
    profile_path = project / "runtime_profile.json"
    profile = choose_or_load_runtime_profile(profile_path, snapshot_dir, tokenizer, train_ds, collator, target_batch)
    capability_major = int(profile["compute_capability"].split(".")[0])
    profile["tf32"] = capability_major >= 8
    atomic_json(profile_path, profile)
    num_workers = 2 if (os.cpu_count() or 2) >= 4 else 0
    print(f"CPU workers={num_workers}; GPU={torch.cuda.get_device_name(0)}; nvidia-smi={gpu_status_line()}", flush=True)

    class_counts = np.bincount(train_df["canonical_label"].to_numpy(dtype=np.int64), minlength=2).astype(np.float64)
    class_weights = [len(train_df) / (2.0 * float(class_counts[i])) for i in [0, 1]]
    config_sha = sha256_file(config_path)
    script_sha = sha256_file(script_path)
    identity_base = {
        "config_sha256": config_sha,
        "script_sha256": script_sha,
        "train_sha256": train_sha,
        "validation_sha256": val_sha,
        "initial_snapshot_sha256": init_manifest["weights_sha256"],
        "pretrained_revision": init_manifest["resolved_revision"],
        "runtime_profile": {k: profile.get(k) for k in ["amp", "attention_backend", "optimizer", "gradient_checkpointing", "micro_batch_size", "gradient_accumulation_steps", "effective_batch_size"]},
    }
    atomic_json(project / "execution_manifest_start.json", {
        "experiment": config["experiment_name"],
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_data_commit": config["data"]["source_commit"],
        "train_sha256": train_sha,
        "validation_sha256": val_sha,
        "initial_snapshot_sha256": init_manifest["weights_sha256"],
        "runtime_profile": profile,
        "train_rows": len(train_df), "validation_rows": len(val_df),
        "test_set_used": False,
    })
    run_integration_smoke(config, profile, tokenizer, train_ds, class_weights, snapshot_dir, workspace, persist, config_sha, script_sha)
    results = []
    for candidate in config["candidates"]:
        result = run_candidate(candidate, config, profile, tokenizer, train_ds, val_ds, val_df, class_weights,
                               snapshot_dir, workspace, persist, identity_base, num_workers)
        results.append(result)

    # Pull completed candidate results too, in case some were skipped on this rerun.
    candidates_all = []
    for cand in config["candidates"]:
        rp = persist / "candidates" / cand["candidate_id"] / "result.json"
        if not rp.exists():
            raise RuntimeError(f"Candidate incomplete: {cand['candidate_id']}; see logs/checkpoints and rerun this cell to resume.")
        candidates_all.append(json_read(rp))
    candidate_order = {c["candidate_id"]: i for i, c in enumerate(config["candidates"])}
    candidates_all.sort(key=lambda r: (
        float(r["validation_metrics"]["f1_promotion"]),
        float(r["validation_metrics"]["precision_promotion"]),
        float(r["validation_metrics"]["recall_promotion"]),
        float(r["validation_metrics"]["macro_f1"]),
        -candidate_order[r["candidate_id"]],  # Fixed candidate order is the final tie-breaker.
    ), reverse=True)
    selected = candidates_all[0]
    selected_id = selected["candidate_id"]
    selected_source = persist / "candidates" / selected_id / "best_model"
    final_model = persist / "artifacts" / "final_model"
    if final_model.exists():
        shutil.rmtree(final_model, ignore_errors=True)
    copytree_verified(selected_source, final_model)
    manifest = {
        "experiment_name": config["experiment_name"],
        "status": "SUCCESS",
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "selected_candidate": selected_id,
        "selected_validation_metrics": selected["validation_metrics"],
        "candidate_results": [{"candidate_id": r["candidate_id"], **r["validation_metrics"], "best_epoch": r.get("best_epoch_from_history"), "runtime_minutes": r.get("train_runtime_minutes")} for r in candidates_all],
        "model": config["model"],
        "encoding": config["encoding"],
        "training_config": config["training"],
        "runtime_profile": profile,
        "class_weights_from_train_only": {"Non-Promotion": class_weights[0], "Promotion": class_weights[1]},
        "data": {"train_sha256": train_sha, "validation_sha256": val_sha, "train_rows": len(train_df), "validation_rows": len(val_df)},
        "config_sha256": config_sha,
        "script_sha256": script_sha,
        "test_set_used": False,
        "selection_source": "normal validation F1 Promotion with documented tie-breakers; no test/obfuscated test used",
    }
    atomic_json(persist / "reports" / "indobert_v2_epoch_budget_manifest.json", manifest)
    pd.DataFrame([{
        "candidate_id": r["candidate_id"], "learning_rate": r["candidate"]["learning_rate"], "weight_decay": r["candidate"]["weight_decay"],
        **r["validation_metrics"], "best_epoch": r.get("best_epoch_from_history"), "runtime_minutes": r.get("train_runtime_minutes"),
    } for r in candidates_all]).to_csv(persist / "reports" / "indobert_v2_candidate_summary.csv", index=False)
    print("\n=== INDOBERT V2 COMPLETE ===")
    print(f"Selected candidate: {selected_id}")
    print(f"Validation F1={selected['validation_metrics']['f1_promotion']:.4f}; Precision={selected['validation_metrics']['precision_promotion']:.4f}; Recall={selected['validation_metrics']['recall_promotion']:.4f}")
    print(f"Final model: {final_model}")
    print(f"Run manifest: {persist / 'reports' / 'indobert_v2_epoch_budget_manifest.json'}")
    print(f"Candidate summary: {persist / 'reports' / 'indobert_v2_candidate_summary.csv'}")
    print("Official Stage 9/10 artifacts were not written by this script. No test files were loaded.")


if __name__ == "__main__":
    main()
