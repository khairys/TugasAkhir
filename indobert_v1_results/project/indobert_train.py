#!/usr/bin/env python3
"""Resumable Stage 9 IndoBERT fine-tuning for Colab T4.

Uses only normal train/validation data. It never reads the frozen test set.
Checkpoints are mirrored to persistent storage at epoch boundaries.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, shutil, sys, time, uuid, platform
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, Subset
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedShuffleSplit
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments,
                          TrainerCallback, EarlyStoppingCallback, set_seed)


def sha256_file(path: Path, chunk_size=1024*1024) -> str:
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            b=f.read(chunk_size)
            if not b: break
            h.update(b)
    return h.hexdigest()


def atomic_json(path: Path, obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp-'+uuid.uuid4().hex)
    with open(tmp,'w',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2,default=_json_default)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)


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
    has_model=(path/'model.safetensors').exists() or (path/'pytorch_model.bin').exists()
    required=['optimizer.pt','scheduler.pt','trainer_state.json']
    return has_model and all((path/n).is_file() and (path/n).stat().st_size>0 for n in required)


def checkpoint_step(path: Path) -> int:
    try: return int(path.name.split('-')[-1])
    except Exception: return -1


def sync_checkpoint(src: Path, cand_root: Path, state):
    """Copy a completed local Trainer checkpoint to Drive and verify key files."""
    if not valid_checkpoint(src):
        raise RuntimeError(f'Checkpoint local belum lengkap; tidak disinkronkan: {src}')
    ckpt_root=cand_root/'checkpoints'; ckpt_root.mkdir(parents=True,exist_ok=True)
    dest=ckpt_root/src.name
    if dest.exists() and (dest/'CHECKPOINT_COMPLETE.json').exists():
        return dest
    tmp=ckpt_root/(src.name+'.pending-'+uuid.uuid4().hex)
    shutil.copytree(src,tmp)
    if not valid_checkpoint(tmp):
        shutil.rmtree(tmp,ignore_errors=True)
        raise RuntimeError(f'Checkpoint setelah copy tidak lengkap: {tmp}')
    files_to_check=['trainer_state.json','optimizer.pt','scheduler.pt']
    model_name='model.safetensors' if (src/'model.safetensors').exists() else 'pytorch_model.bin'
    files_to_check.append(model_name)
    sizes={n:(src/n).stat().st_size for n in files_to_check}
    for n,size in sizes.items():
        if (tmp/n).stat().st_size != size:
            shutil.rmtree(tmp,ignore_errors=True)
            raise RuntimeError(f'Ukuran file checkpoint berbeda setelah copy: {n}')
    marker={
      'status':'COMPLETE','global_step':checkpoint_step(src),'saved_at_utc':datetime.now(timezone.utc).isoformat(),
      'files':sizes,'trainer_state_sha256':sha256_file(tmp/'trainer_state.json')
    }
    atomic_json(tmp/'CHECKPOINT_COMPLETE.json',marker)
    if dest.exists(): shutil.rmtree(dest,ignore_errors=True)
    tmp.rename(dest)
    if not (dest/'CHECKPOINT_COMPLETE.json').exists() or not valid_checkpoint(dest):
        raise RuntimeError(f'Checkpoint Drive belum tervalidasi: {dest}')
    best_path=getattr(state,'best_model_checkpoint',None)
    best_step=checkpoint_step(Path(best_path)) if best_path else -1
    complete=[p for p in ckpt_root.glob('checkpoint-*') if (p/'CHECKPOINT_COMPLETE.json').exists() and valid_checkpoint(p)]
    complete=sorted(complete,key=checkpoint_step,reverse=True)
    keep={p.name for p in complete[:2]}
    if best_step >= 0: keep.add(f'checkpoint-{best_step}')
    for p in complete:
        if p.name not in keep: shutil.rmtree(p,ignore_errors=True)
    atomic_json(cand_root/'latest_checkpoint.json',{
      'latest_checkpoint':complete[0].name if complete else dest.name,
      'global_step':checkpoint_step(dest),'best_model_checkpoint_step':best_step,
      'updated_at_utc':datetime.now(timezone.utc).isoformat()
    })
    return dest


def sync_dir(src: Path, dest: Path):
    """Copy a directory via staging, verify files and then replace destination."""
    src=Path(src); dest=Path(dest); dest.parent.mkdir(parents=True,exist_ok=True)
    tmp=dest.parent/(f'.{dest.name}.pending-'+uuid.uuid4().hex)
    shutil.copytree(src,tmp)
    # At least one model weights file and config are required for HF model folders.
    has_weights=(tmp/'model.safetensors').exists() or (tmp/'pytorch_model.bin').exists()
    if not has_weights or not (tmp/'config.json').exists():
        shutil.rmtree(tmp,ignore_errors=True)
        raise RuntimeError(f'Directory model tidak memiliki config/bobot yang diperlukan: {src}')
    for p in src.rglob('*'):
        if p.is_file():
            rel=p.relative_to(src); copied=tmp/rel
            if not copied.exists() or copied.stat().st_size != p.stat().st_size:
                shutil.rmtree(tmp,ignore_errors=True)
                raise RuntimeError(f'Verifikasi ukuran copy gagal: {rel}')
    backup=None
    if dest.exists():
        backup=dest.parent/(f'.{dest.name}.old-'+uuid.uuid4().hex)
        dest.rename(backup)
    try:
        tmp.rename(dest)
    except Exception:
        if backup and backup.exists() and not dest.exists(): backup.rename(dest)
        raise
    if backup: shutil.rmtree(backup,ignore_errors=True)
    return dest


def find_persistent_checkpoints(cand_root: Path):
    root=cand_root/'checkpoints'
    if not root.exists(): return []
    out=[]
    for p in root.glob('checkpoint-*'):
        if (p/'CHECKPOINT_COMPLETE.json').exists() and valid_checkpoint(p): out.append(p)
    return sorted(out,key=checkpoint_step)


def sync_persistent_checkpoints_to_local(cand_root: Path, output_dir: Path):
    output_dir.mkdir(parents=True,exist_ok=True)
    for cp in find_persistent_checkpoints(cand_root):
        local=output_dir/cp.name
        if local.exists(): shutil.rmtree(local,ignore_errors=True)
        shutil.copytree(cp,local)
        if not valid_checkpoint(local): raise RuntimeError(f'Checkpoint gagal dipulihkan ke workspace: {local}')
    candidates=[p for p in output_dir.glob('checkpoint-*') if valid_checkpoint(p)]
    if not candidates: return None
    return sorted(candidates,key=checkpoint_step)[-1]


class PersistentCheckpointCallback(TrainerCallback):
    def __init__(self, cand_root: Path): self.cand_root=Path(cand_root)
    def on_save(self,args,state,control,**kwargs):
        local=Path(args.output_dir)/f'checkpoint-{state.global_step}'
        if local.exists():
            sync_checkpoint(local,self.cand_root,state)
        return control


class PauseAfterStepCallback(TrainerCallback):
    def __init__(self, pause_after_step: int): self.pause_after_step=pause_after_step
    def on_step_end(self,args,state,control,**kwargs):
        if self.pause_after_step > 0 and state.global_step >= self.pause_after_step:
            control.should_training_stop=True
        return control


class ArrayDataset(Dataset):
    def __init__(self, cache_path: Path):
        z=np.load(cache_path,allow_pickle=False)
        self.input_ids=torch.from_numpy(z['input_ids'].astype(np.int64,copy=False))
        self.attention_mask=torch.from_numpy(z['attention_mask'].astype(np.int64,copy=False))
        self.token_type_ids=torch.from_numpy(z['token_type_ids'].astype(np.int64,copy=False)) if 'token_type_ids' in z.files else None
        self.labels=torch.from_numpy(z['labels'].astype(np.int64,copy=False))
    def __len__(self): return len(self.labels)
    def __getitem__(self,idx):
        row={'input_ids':self.input_ids[idx], 'attention_mask':self.attention_mask[idx], 'labels':self.labels[idx]}
        if self.token_type_ids is not None: row['token_type_ids']=self.token_type_ids[idx]
        return row


class WeightedTrainer(Trainer):
    def __init__(self,*args,class_weights=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.class_weights=torch.tensor(class_weights,dtype=torch.float32) if class_weights is not None else None
    def compute_loss(self,model,inputs,return_outputs=False,num_items_in_batch=None):
        labels=inputs.pop('labels')
        outputs=model(**inputs)
        weights=self.class_weights.to(outputs.logits.device) if self.class_weights is not None else None
        loss=nn.CrossEntropyLoss(weight=weights)(outputs.logits,labels)
        return (loss,outputs) if return_outputs else loss


def compute_metrics(eval_pred):
    logits, labels=eval_pred
    preds=np.argmax(logits,axis=-1)
    cm=confusion_matrix(labels,preds,labels=[0,1])
    tn,fp,fn,tp=cm.ravel()
    return {
      'f1_promotion':float(f1_score(labels,preds,pos_label=1,zero_division=0)),
      'precision_promotion':float(precision_score(labels,preds,pos_label=1,zero_division=0)),
      'recall_promotion':float(recall_score(labels,preds,pos_label=1,zero_division=0)),
      'accuracy':float(accuracy_score(labels,preds)),
      'macro_f1':float(f1_score(labels,preds,average='macro',zero_division=0)),
      'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp)
    }


def set_all_seeds(seed=42):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)
    set_seed(seed)


def checkpoint_is_compatible(root: Path, config_sha: str, train_sha: str, val_sha: str, script_sha: str):
    state_path=root/'experiment_identity.json'
    current={'config_sha256':config_sha,'train_sha256':train_sha,'validation_sha256':val_sha,'script_sha256':script_sha}
    if state_path.exists():
        prior=json_read(state_path)
        if prior != current:
            raise RuntimeError('Identitas eksperimen berbeda dengan run tersimpan. Jangan resume memakai konfigurasi/data/kode berbeda. Gunakan run version baru atau audit terlebih dahulu.')
    else:
        # If checkpoints exist but identity is missing, fail closed rather than guessing.
        if find_persistent_checkpoints(root):
            raise RuntimeError(f'Ada checkpoint tetapi experiment_identity.json tidak ada: {root}')
        atomic_json(state_path,current)


def load_result(path: Path):
    if not path.exists(): return None
    try:
        obj=json_read(path)
        model_dir=path.parent/'best_model'
        if obj.get('status')=='SUCCESS' and model_dir.exists() and ((model_dir/'model.safetensors').exists() or (model_dir/'pytorch_model.bin').exists()):
            return obj
    except Exception: pass
    return None


def build_args(candidate, config, output_dir, mode):
    t=config['training']
    if mode=='smoke':
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
      num_train_epochs=int(t['max_epochs']), fp16=True, bf16=False,
      gradient_checkpointing=True, max_grad_norm=float(t['max_grad_norm']),
      warmup_ratio=float(t['warmup_ratio']), lr_scheduler_type='linear', optim='adamw_torch',
      logging_strategy='steps', logging_steps=int(t['logging_steps']), eval_strategy='epoch', save_strategy='epoch',
      save_total_limit=2, save_safetensors=True, load_best_model_at_end=True,
      metric_for_best_model='f1_promotion', greater_is_better=True,
      report_to='none', seed=int(config['seed']), data_seed=int(config['seed']),
      dataloader_num_workers=int(t['dataloader_num_workers']), dataloader_pin_memory=True,
      logging_dir=str(output_dir/'tensorboard'),
      label_names=['labels']
    )


def load_train_val(workspace):
    train_path=workspace/'data_snapshot'/'train_v1.csv'; val_path=workspace/'data_snapshot'/'validation_v1.csv'
    if not train_path.exists() or not val_path.exists(): raise FileNotFoundError('data_snapshot train/validation CSV tidak ditemukan di workspace.')
    tr=pd.read_csv(train_path,low_memory=False); va=pd.read_csv(val_path,low_memory=False)
    for name,df,n,p,nprom in [('train',tr,32920,3960,28960),('validation',va,4116,495,3621)]:
        required={'record_id','text_raw','canonical_label'}
        if required-set(df.columns): raise RuntimeError(f'{name}: kolom hilang {required-set(df.columns)}')
        if len(df)!=n: raise RuntimeError(f'{name}: jumlah baris {len(df)} != {n}')
        if df['record_id'].duplicated().any(): raise RuntimeError(f'{name}: record_id duplikat')
        if df[['text_raw','canonical_label']].isna().any().any(): raise RuntimeError(f'{name}: nilai null')
        y=pd.to_numeric(df['canonical_label']).astype(int)
        if set(y.unique())!={0,1}: raise RuntimeError(f'{name}: label bukan 0/1')
        if int((y==1).sum())!=p or int((y==0).sum())!=nprom: raise RuntimeError(f'{name}: distribusi label tidak sesuai kontrak')
        df['canonical_label']=y
    if set(tr.record_id.astype(str)) & set(va.record_id.astype(str)): raise RuntimeError('record_id overlap train/validation')
    if 'leakage_group_id' in tr.columns and 'leakage_group_id' in va.columns:
        if set(tr.leakage_group_id.astype(str)) & set(va.leakage_group_id.astype(str)):
            raise RuntimeError('leakage_group_id overlap train/validation')
    return tr,va


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=['smoke','official','validate'],required=True)
    ap.add_argument('--workspace',required=True)
    ap.add_argument('--persistent-root',required=True)
    ap.add_argument('--resume',choices=['auto','never'],default='auto')
    ap.add_argument('--pause-after-step',type=int,default=0)
    args=ap.parse_args()
    workspace=Path(args.workspace); persist=Path(args.persistent_root)
    project=persist/'project'; config_path=project/'indobert_v1.json'; script_path=project/'indobert_train.py'
    train_df,val_df=load_train_val(workspace)
    train_path=workspace/'data_snapshot'/'train_v1.csv'; val_path=workspace/'data_snapshot'/'validation_v1.csv'
    train_sha=sha256_file(train_path); val_sha=sha256_file(val_path)
    config=json_read(config_path)
    if config['data']['train_sha256']!=train_sha or config['data']['validation_sha256']!=val_sha:
        raise RuntimeError('Hash data berbeda dengan konfigurasi beku.')
    config_sha=sha256_file(config_path); script_sha=sha256_file(script_path)
    if not torch.cuda.is_available(): raise RuntimeError('CUDA tidak tersedia; training IndoBERT dihentikan.')
    gpu=torch.cuda.get_device_name(0)
    if 'T4' not in gpu.upper(): raise RuntimeError(f'GPU aktif bukan T4: {gpu}')
    token_cache=workspace/'data_cache'
    train_cache=token_cache/'train_tokens.npz'; val_cache=token_cache/'validation_tokens.npz'
    if not train_cache.exists() or not val_cache.exists(): raise FileNotFoundError('Tokenized cache belum ada. Jalankan cell persiapan/tokenisasi notebook terlebih dahulu.')
    y_train=train_df['canonical_label'].to_numpy(dtype=np.int64)
    class_weights=[len(y_train)/(2*int((y_train==i).sum())) for i in [0,1]]
    train_ds=ArrayDataset(train_cache); val_ds=ArrayDataset(val_cache)
    model_snapshot=workspace/'pretrained_snapshot'
    if not (model_snapshot/'config.json').exists(): raise FileNotFoundError('Snapshot model pralatih tidak tersedia di workspace.')
    if args.mode=='validate':
        validate_final(persist,workspace,config,train_sha,val_sha)
        return

    if args.mode=='smoke':
        run_root=persist/'runs'/'indobert_v1_smoke'; reports=persist/'reports'/'indobert_v1_smoke'
        candidates=[config['candidates'][0]]
        splitter=StratifiedShuffleSplit(n_splits=1,train_size=1200,random_state=int(config['seed']))
        tr_idx,_=next(splitter.split(np.zeros(len(y_train)),y_train)); train_use=Subset(train_ds,tr_idx.tolist())
        val_y=val_df['canonical_label'].to_numpy(dtype=np.int64)
        vs=StratifiedShuffleSplit(n_splits=1,train_size=300,random_state=int(config['seed']))
        va_idx,_=next(vs.split(np.zeros(len(val_y)),val_y)); val_use=Subset(val_ds,va_idx.tolist())
        pause=args.pause_after_step
    else:
        run_root=persist/'runs'/'indobert_v1'; reports=persist/'reports'/'indobert_v1'
        candidates=config['candidates']; train_use=train_ds; val_use=val_ds; pause=0
    run_root.mkdir(parents=True,exist_ok=True); reports.mkdir(parents=True,exist_ok=True)
    identity={'config_sha256':config_sha,'train_sha256':train_sha,'validation_sha256':val_sha,'script_sha256':script_sha}
    id_path=run_root/'experiment_identity.json'
    if id_path.exists() and json_read(id_path)!=identity:
        raise RuntimeError('Experiment identity mismatch; tidak aman untuk resume. Jangan menimpa run lama.')
    if not id_path.exists(): atomic_json(id_path,identity)
    results=[]

    for cand in candidates:
        cid=cand['candidate_id']; cand_root=run_root/'candidates'/cid; cand_root.mkdir(parents=True,exist_ok=True)
        result_path=cand_root/'candidate_result.json'
        old=load_result(result_path) if args.resume=='auto' else None
        if old:
            print(f'[SKIP] {cid} sudah selesai dan artefak terbaik tersedia. F1={old["metrics"].get("f1_promotion")}',flush=True)
            results.append(old); continue
        out_dir=workspace/'local_runs'/run_root.name/cid
        # Restore every valid remote checkpoint, including the recorded best checkpoint.
        remote_cps=find_persistent_checkpoints(cand_root)
        if args.resume=='never' and remote_cps: raise RuntimeError(f'Checkpoint sudah ada untuk {cid}; gunakan --resume auto atau run version baru.')
        out_dir.mkdir(parents=True,exist_ok=True)
        if args.resume=='auto' and remote_cps:
            local_resume=sync_persistent_checkpoints_to_local(cand_root,out_dir)
            print(f'[RESUME] {cid} dari {local_resume.name} (global_step={checkpoint_step(local_resume)})',flush=True)
        else:
            # Do not wipe unrelated logs; remove only checkpoint folders if deliberately starting fresh.
            for old_cp in out_dir.glob('checkpoint-*'):
                if old_cp.is_dir(): shutil.rmtree(old_cp,ignore_errors=True)
            local_resume=None
        set_all_seeds(int(config['seed']))
        model=AutoModelForSequenceClassification.from_pretrained(str(model_snapshot),local_files_only=True)
        model.config.id2label={0:'Non-Promotion',1:'Promotion'}
        model.config.label2id={'Non-Promotion':0,'Promotion':1}
        targs=build_args(cand,config,out_dir,args.mode)
        callbacks=[PersistentCheckpointCallback(cand_root)]
        if args.mode=='official': callbacks.append(EarlyStoppingCallback(early_stopping_patience=int(config['training']['early_stopping_patience'])))
        if args.mode=='smoke' and pause>0: callbacks.append(PauseAfterStepCallback(pause))
        trainer=WeightedTrainer(model=model,args=targs,train_dataset=train_use,eval_dataset=val_use if args.mode=='official' else None,
                                compute_metrics=compute_metrics,callbacks=callbacks,class_weights=class_weights,
                                processing_class=AutoTokenizer.from_pretrained(str(model_snapshot),local_files_only=True))
        started=time.time()
        train_out=trainer.train(resume_from_checkpoint=str(local_resume) if local_resume else None)
        elapsed=round(time.time()-started,3)
        final_step=int(trainer.state.global_step)
        if args.mode=='smoke' and pause>0 and final_step < int(targs.max_steps):
            atomic_json(cand_root/'smoke_pause_state.json',{'status':'PAUSED_INTENTIONALLY','global_step':final_step,'updated_at_utc':datetime.now(timezone.utc).isoformat()})
            print(f'[SMOKE PAUSED] {cid} paused at step {final_step}. Checkpoint persisted. Run smoke resume cell next.',flush=True)
            return
        if args.mode=='smoke':
            pred=trainer.predict(val_use,metric_key_prefix='validation')
            metrics={k.replace('validation_',''):float(v) if isinstance(v,(int,float,np.number)) else v for k,v in pred.metrics.items() if k.startswith('validation_')}
            atomic_json(reports/'smoke_validation_metrics.json',{'candidate_id':cid,'metrics':metrics,'steps':final_step,'seconds':elapsed})
            atomic_json(cand_root/'smoke_complete.json',{'status':'SUCCESS','global_step':final_step,'resume_tested':local_resume is not None,'updated_at_utc':datetime.now(timezone.utc).isoformat()})
            # No large optimizer checkpoint needs to be retained after smoke validation.
            shutil.rmtree(cand_root/'checkpoints',ignore_errors=True)
            print(f'[SMOKE COMPLETE] steps={final_step}; resumed={local_resume is not None}; metrics={metrics}',flush=True)
            return

        # load_best_model_at_end=True; Trainer has restored its best validation checkpoint weights.
        eval_metrics=trainer.evaluate(val_ds,metric_key_prefix='validation')
        normalized={k.replace('validation_',''):float(v) if isinstance(v,(int,float,np.number)) else v for k,v in eval_metrics.items() if k.startswith('validation_')}
        pred=trainer.predict(val_ds,metric_key_prefix='validation')
        logits=pred.predictions[0] if isinstance(pred.predictions,tuple) else pred.predictions
        pred_labels=np.argmax(logits,axis=-1)
        final_local=workspace/'candidate_best_models'/cid
        if final_local.exists(): shutil.rmtree(final_local,ignore_errors=True)
        trainer.save_model(str(final_local))
        tok=AutoTokenizer.from_pretrained(str(model_snapshot),local_files_only=True); tok.save_pretrained(final_local)
        best_dir=sync_dir(final_local,cand_root/'best_model')
        p_df=pd.DataFrame({'record_id':val_df['record_id'].astype(str),'actual_label':val_df['canonical_label'].astype(int),
                           'predicted_label':pred_labels.astype(int),'is_correct':(pred_labels==val_df['canonical_label'].to_numpy(dtype=np.int64))})
        pred_path=reports/f'{cid}_validation_predictions.csv'; p_df.to_csv(pred_path,index=False,encoding='utf-8')
        hist_path=reports/f'{cid}_training_history.json'; atomic_json(hist_path,trainer.state.log_history)
        best_checkpoint_path=Path(trainer.state.best_model_checkpoint) if trainer.state.best_model_checkpoint else None
        best_epoch=None
        if best_checkpoint_path and (best_checkpoint_path/'trainer_state.json').exists():
            try: best_epoch=json_read(best_checkpoint_path/'trainer_state.json').get('epoch')
            except Exception: best_epoch=None
        summary={
          'candidate_id':cid,'status':'SUCCESS','hyperparameters':cand,'metrics':normalized,
          'train_runtime_seconds':elapsed,'global_step':final_step,'final_epoch':getattr(trainer.state,'epoch',None),
          'best_epoch':best_epoch,'best_checkpoint_step':checkpoint_step(best_checkpoint_path) if best_checkpoint_path else None,
          'best_metric':float(trainer.state.best_metric) if trainer.state.best_metric is not None else None,
          'best_checkpoint':str(trainer.state.best_model_checkpoint) if trainer.state.best_model_checkpoint else None,
          'training_samples':len(train_df),'validation_samples':len(val_df),
          'class_weights':{'Non-Promotion':class_weights[0],'Promotion':class_weights[1]},
          'best_model_path':str(best_dir),'best_model_config_sha256':sha256_file(best_dir/'config.json'),
          'validation_predictions_path':str(pred_path),'training_history_path':str(hist_path),
          'completed_at_utc':datetime.now(timezone.utc).isoformat()
        }
        atomic_json(result_path,summary)
        results.append(summary)
        # Keep only the best inference-ready model and history for completed candidates, not huge optimizer checkpoints.
        shutil.rmtree(cand_root/'checkpoints',ignore_errors=True)
        print(f'[OFFICIAL COMPLETE] {cid}: F1 Promotion={normalized.get("f1_promotion")}, P={normalized.get("precision_promotion")}, R={normalized.get("recall_promotion")}',flush=True)

    if args.mode=='official':
        # Re-read all four successful candidates, including any skipped because already completed.
        all_results=[]
        for cand in config['candidates']:
            r=load_result(run_root/'candidates'/cand['candidate_id']/'candidate_result.json')
            if not r: raise RuntimeError(f'Kandidat belum selesai/artefak tidak valid: {cand["candidate_id"]}')
            all_results.append(r)
        order={c['candidate_id']:i for i,c in enumerate(config['candidates'])}
        best=sorted(all_results,key=lambda r:(-r['metrics'].get('f1_promotion',0),-r['metrics'].get('precision_promotion',0),-r['metrics'].get('recall_promotion',0),-r['metrics'].get('macro_f1',0),order[r['candidate_id']]))[0]
        rows=[]
        for r in all_results:
            m=r['metrics']; hp=r['hyperparameters']
            rows.append({'candidate_id':r['candidate_id'],'learning_rate':hp['learning_rate'],'weight_decay':hp['weight_decay'],
              'f1_promotion':m.get('f1_promotion'),'precision_promotion':m.get('precision_promotion'),'recall_promotion':m.get('recall_promotion'),
              'accuracy':m.get('accuracy'),'macro_f1':m.get('macro_f1'),'TN':m.get('TN'),'FP':m.get('FP'),'FN':m.get('FN'),'TP':m.get('TP'),
              'best_epoch':r.get('best_epoch'),'global_step':r.get('global_step'),'train_runtime_seconds':r.get('train_runtime_seconds'),
              'is_selected':r['candidate_id']==best['candidate_id']})
        pd.DataFrame(rows).to_csv(reports/'tuning_results.csv',index=False,encoding='utf-8')
        atomic_json(reports/'validation_metrics.json',best)
        selected_source=run_root/'candidates'/best['candidate_id']/'best_model'
        final_dir=persist/'artifacts'/'final_model'
        # Preserve current final artifact until the new selected model has copied and validated.
        sync_dir(selected_source,final_dir)
        contract={
          'experiment':'Stage 9 IndoBERT binary classifier','base_model':config['model']['id'],
          'base_model_revision':config['model'].get('resolved_revision'),'selected_candidate':best['candidate_id'],
          'max_length':config['encoding']['max_length'],'label2id':{'Non-Promotion':0,'Promotion':1},
          'id2label':{'0':'Non-Promotion','1':'Promotion'},'text_column':'text_raw','label_column':'canonical_label',
          'training_data_sha256':train_sha,'validation_data_sha256':val_sha,'test_set_used':False
        }
        atomic_json(final_dir/'inference_contract.json',contract)
        env={
          'python':platform.python_version(),'torch':torch.__version__,'cuda':torch.version.cuda,
          'transformers':__import__('transformers').__version__,'pandas':pd.__version__,'numpy':np.__version__,
          'gpu_name':gpu,'gpu_memory_gib':round(torch.cuda.get_device_properties(0).total_memory/(1024**3),3)
        }
        manifest={
          'experiment_name':'indobert_baseline_v1','stage':'stage9','status':'SUCCESS','updated_at_utc':datetime.now(timezone.utc).isoformat(),
          'git_source_commit':config.get('git_source_commit'),'environment':env,'model':config['model'],'encoding':config['encoding'],
          'training':config['training'],'candidate_grid':config['candidates'],'class_weights':{'Non-Promotion':class_weights[0],'Promotion':class_weights[1]},
          'data':{'train_rows':len(train_df),'validation_rows':len(val_df),'train_sha256':train_sha,'validation_sha256':val_sha},
          'selected_candidate':best['candidate_id'],'selected_metrics':best['metrics'],
          'selected_model_config_sha256':sha256_file(final_dir/'config.json'),'selected_model_weights_sha256':sha256_file(final_dir/'model.safetensors') if (final_dir/'model.safetensors').exists() else sha256_file(final_dir/'pytorch_model.bin'),
          'config_sha256':config_sha,'training_script_sha256':script_sha,'test_set_used':False,
          'candidates':[{'candidate_id':r['candidate_id'],'status':r['status'],'metrics':r['metrics']} for r in all_results]
        }
        atomic_json(reports/'run_manifest.json',manifest)
        atomic_json(run_root/'run_manifest.json',manifest)
        print('\n=== INDoBERT OFFICIAL RESULT ===',flush=True)
        print(pd.DataFrame(rows).to_string(index=False),flush=True)
        print('Selected candidate:',best['candidate_id'],flush=True)
        print('Validation F1 Promotion:',best['metrics'].get('f1_promotion'),flush=True)
        print('Final model:',final_dir,flush=True)


def validate_final(persist: Path,workspace: Path,config,train_sha,val_sha):
    final_dir=persist/'artifacts'/'final_model'; report_dir=persist/'reports'/'indobert_v1'
    if not final_dir.exists() or not (final_dir/'inference_contract.json').exists(): raise FileNotFoundError('Final model/contract belum tersedia; jalankan official training dahulu.')
    df=pd.read_csv(workspace/'data_snapshot'/'validation_v1.csv',low_memory=False)
    contract=json_read(final_dir/'inference_contract.json')
    if contract.get('validation_data_sha256')!=val_sha or contract.get('training_data_sha256')!=train_sha: raise RuntimeError('Hash data pada inference contract tidak cocok.')
    tok=AutoTokenizer.from_pretrained(str(final_dir),local_files_only=True)
    model=AutoModelForSequenceClassification.from_pretrained(str(final_dir),local_files_only=True)
    device=torch.device('cuda'); model.to(device); model.eval()
    cache=np.load(workspace/'data_cache'/'validation_tokens.npz',allow_pickle=False)
    preds=[]
    bs=16
    with torch.inference_mode():
        for start in range(0,len(df),bs):
            end=min(start+bs,len(df))
            batch={'input_ids':torch.as_tensor(cache['input_ids'][start:end],dtype=torch.long,device=device),
                   'attention_mask':torch.as_tensor(cache['attention_mask'][start:end],dtype=torch.long,device=device)}
            if 'token_type_ids' in cache.files: batch['token_type_ids']=torch.as_tensor(cache['token_type_ids'][start:end],dtype=torch.long,device=device)
            with torch.autocast('cuda',dtype=torch.float16): logits=model(**batch).logits
            preds.extend(logits.argmax(-1).detach().cpu().numpy().tolist())
    metrics=compute_metrics((np.eye(2)[np.asarray(preds)],df['canonical_label'].to_numpy(dtype=np.int64)))
    predfile=report_dir/'validation_predictions.csv'
    selected=json_read(report_dir/'validation_metrics.json')
    # Generate final reload predictions as an independent persisted record; compare class decisions if selected prediction exists.
    reload_df=pd.DataFrame({'record_id':df['record_id'].astype(str),'actual_label':df['canonical_label'].astype(int),'predicted_label':preds,
                            'is_correct':(np.asarray(preds)==df['canonical_label'].to_numpy(dtype=np.int64))})
    reload_path=report_dir/'final_reload_validation_predictions.csv'; reload_df.to_csv(reload_path,index=False,encoding='utf-8')
    selection_pred=report_dir/f"{selected['candidate_id']}_validation_predictions.csv"
    comparison='NOT_AVAILABLE'
    if selection_pred.exists():
        saved=pd.read_csv(selection_pred)
        if saved['record_id'].astype(str).tolist()!=df['record_id'].astype(str).tolist(): raise RuntimeError('Urutan record_id prediksi tersimpan berbeda.')
        exact=float((saved['predicted_label'].to_numpy()==np.asarray(preds)).mean())
        comparison={'prediction_agreement_pct':round(exact*100,6),'rows':len(df)}
        if exact<0.999: raise RuntimeError(f'Prediksi model hasil reload tidak konsisten dengan prediksi resmi: {exact:.4%}')
    model_hash=sha256_file(final_dir/'model.safetensors') if (final_dir/'model.safetensors').exists() else sha256_file(final_dir/'pytorch_model.bin')
    report={'status':'PASS','validated_at_utc':datetime.now(timezone.utc).isoformat(),'gpu_name':torch.cuda.get_device_name(0),
            'train_sha256':train_sha,'validation_sha256':val_sha,'model_weights_sha256':model_hash,'metrics_from_reloaded_final_model':metrics,
            'comparison_to_saved_candidate_predictions':comparison,'test_set_used':False}
    atomic_json(report_dir/'artifact_validation_report.json',report)
    # Create results archive excluding optimizer checkpoints and all test data.
    zip_path=persist/'indobert_v1_results.zip'
    if zip_path.exists(): zip_path.unlink()
    import zipfile
    include=[persist/'project'/'indobert_train.py',persist/'project'/'indobert_v1.json',persist/'project'/'environment_snapshot.json',
             persist/'data_snapshot'/'split_manifest_v1.json',final_dir,report_dir]
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as zf:
        for item in include:
            if not item.exists(): continue
            if item.is_file(): zf.write(item,item.relative_to(persist))
            else:
                for f in item.rglob('*'):
                    if f.is_file(): zf.write(f,f.relative_to(persist))
    with zipfile.ZipFile(zip_path,'r') as zf:
        bad=zf.testzip()
        if bad: raise RuntimeError(f'ZIP hasil rusak di file {bad}')
    report['zip_path']=str(zip_path); report['zip_size_bytes']=zip_path.stat().st_size; report['zip_integrity']='PASS'
    atomic_json(report_dir/'artifact_validation_report.json',report)
    print('ARTIFACT VALIDATION PASS')
    print(json.dumps(report,ensure_ascii=False,indent=2,default=_json_default))
    print('Results ZIP:',zip_path)

if __name__=='__main__': main()
