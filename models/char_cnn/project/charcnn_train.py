#!/usr/bin/env python3
"""Resumable Stage 9 Character-level CNN experiment for Google Colab T4."""
from __future__ import annotations
import argparse, copy, csv, hashlib, json, os, random, shutil, sys, time, uuid, platform
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedShuffleSplit


def sha256_file(path, chunk_size=1024*1024):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            b=f.read(chunk_size)
            if not b: break
            h.update(b)
    return h.hexdigest()

def sha256_json(obj):
    b=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(b).hexdigest()

def atomic_json(path, obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp-'+uuid.uuid4().hex)
    with open(tmp,'w',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

def persist_file(local_src, drive_dst):
    local_src=Path(local_src); drive_dst=Path(drive_dst)
    drive_dst.parent.mkdir(parents=True,exist_ok=True)
    expected=sha256_file(local_src)
    tmp=drive_dst.with_name(drive_dst.name+'.uploading-'+uuid.uuid4().hex)
    shutil.copy2(local_src,tmp)
    actual=sha256_file(tmp)
    if actual != expected:
        try: tmp.unlink()
        except OSError: pass
        raise RuntimeError(f'Copy verification failed: {drive_dst}')
    os.replace(tmp,drive_dst)
    if sha256_file(drive_dst) != expected:
        raise RuntimeError(f'Persistent file verification failed: {drive_dst}')
    return expected

def atomic_text(path, text):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp-'+uuid.uuid4().hex)
    with open(tmp,'w',encoding='utf-8') as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

def seed_everything(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark=False
    torch.backends.cudnn.deterministic=True

def capture_rng():
    return {'python':random.getstate(), 'numpy':np.random.get_state(), 'torch_cpu':torch.get_rng_state(),
            'torch_cuda':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []}

def restore_rng(state):
    random.setstate(state['python']); np.random.set_state(state['numpy']); torch.set_rng_state(state['torch_cpu'])
    if torch.cuda.is_available() and state.get('torch_cuda'):
        torch.cuda.set_rng_state_all(state['torch_cuda'])

def cpu_state_dict(state):
    return {k:v.detach().cpu().clone() for k,v in state.items()}

class CharCNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim=32, kernel_sizes=(3,5,7), conv_channels=64,
                 hidden_dim=128, dropout=0.3, pad_id=0):
        super().__init__()
        self.embedding=nn.Embedding(vocab_size,embedding_dim,padding_idx=pad_id)
        self.convs=nn.ModuleList([nn.Conv1d(embedding_dim,conv_channels,kernel_size=k,padding=k//2) for k in kernel_sizes])
        self.fc1=nn.Linear(conv_channels*len(kernel_sizes),hidden_dim)
        self.dropout=nn.Dropout(dropout)
        self.fc2=nn.Linear(hidden_dim,2)
    def forward(self, input_ids, lengths):
        # input_ids [B,L]; mask makes right-padding positions ineligible for global pooling.
        z=self.embedding(input_ids).transpose(1,2)
        positions=torch.arange(input_ids.shape[1],device=input_ids.device).unsqueeze(0)
        valid=(positions < lengths.unsqueeze(1)).unsqueeze(1)
        pooled=[]
        for conv in self.convs:
            h=F.relu(conv(z))
            h=h.masked_fill(~valid, torch.finfo(h.dtype).min)
            pooled.append(h.amax(dim=-1))
        x=torch.cat(pooled,dim=1)
        x=F.relu(self.fc1(x)); x=self.dropout(x)
        return self.fc2(x)

def encode_texts(texts, stoi, max_length, unk_id=1):
    x=np.zeros((len(texts),max_length),dtype=np.int32)
    lengths=np.empty(len(texts),dtype=np.int32)
    for i,text in enumerate(texts):
        s=str(text)[:max_length]
        ids=[stoi.get(ch,unk_id) for ch in s]
        if not ids:
            ids=[unk_id]
        n=min(len(ids),max_length); x[i,:n]=ids[:n]; lengths[i]=n
        if (i+1)%5000==0: print(f'Encoded {i+1:,}/{len(texts):,} texts',flush=True)
    return x,lengths

def get_scaler(enabled=True):
    try: return torch.amp.GradScaler('cuda',enabled=enabled)
    except (AttributeError,TypeError): return torch.cuda.amp.GradScaler(enabled=enabled)

def autocast_context(enabled=True):
    return torch.autocast(device_type='cuda',dtype=torch.float16,enabled=enabled)

def compute_metrics(y_true, y_pred):
    cm=confusion_matrix(y_true,y_pred,labels=[0,1]); tn,fp,fn,tp=cm.ravel()
    return {'f1_promotion':float(f1_score(y_true,y_pred,pos_label=1,zero_division=0)),
            'precision_promotion':float(precision_score(y_true,y_pred,pos_label=1,zero_division=0)),
            'recall_promotion':float(recall_score(y_true,y_pred,pos_label=1,zero_division=0)),
            'accuracy':float(accuracy_score(y_true,y_pred)),
            'macro_f1':float(f1_score(y_true,y_pred,average='macro',zero_division=0)),
            'confusion_matrix':{'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp)}}

def metric_rank(m):
    return (m['f1_promotion'],m['precision_promotion'],m['recall_promotion'],m['macro_f1'])

def validate_df(df,name,expected,expected_prom):
    required={'record_id','text_raw','canonical_label'}
    if not required.issubset(df.columns): raise RuntimeError(f'{name}: missing columns {required-set(df.columns)}')
    if len(df)!=expected: raise RuntimeError(f'{name}: expected {expected}, found {len(df)}')
    if df['record_id'].duplicated().any(): raise RuntimeError(f'{name}: duplicate record_id')
    if df['text_raw'].isna().any() or df['canonical_label'].isna().any(): raise RuntimeError(f'{name}: null found')
    if set(pd.to_numeric(df['canonical_label']).unique())!={0,1}: raise RuntimeError(f'{name}: labels must be 0/1')
    if int((df['canonical_label']==1).sum())!=expected_prom: raise RuntimeError(f'{name}: Promotion count mismatch')
    if (df['text_raw'].astype(str).str.len()==0).any(): raise RuntimeError(f'{name}: empty text found')
    print(f'{name} data contract PASS: {len(df):,} rows')

def write_checkpoint(state, cand_dir, local_tmp_root, keep=3):
    ckpt_dir=Path(cand_dir)/'checkpoints'; ckpt_dir.mkdir(parents=True,exist_ok=True)
    local_tmp_root=Path(local_tmp_root); local_tmp_root.mkdir(parents=True,exist_ok=True)
    local_path=local_tmp_root/f'{state["candidate_id"]}_{state["global_step"]}_{uuid.uuid4().hex}.pt'
    torch.save(state,local_path)
    name=f'checkpoint_step_{state["global_step"]:08d}_{uuid.uuid4().hex[:8]}.pt'
    dest=ckpt_dir/name
    digest=persist_file(local_path,dest)
    atomic_text(dest.with_suffix(dest.suffix+'.sha256'),digest+'\n')
    atomic_json(ckpt_dir/'latest_checkpoint.json',{'file':name,'sha256':digest,'saved_at':datetime.now(timezone.utc).isoformat(),
                                                   'next_epoch':state['next_epoch'],'next_batch_idx':state['next_batch_idx'],
                                                   'global_step':state['global_step']})
    # Rotasi baru dilakukan setelah checkpoint terbaru terverifikasi dan pointer tersimpan.
    all_ckpts=sorted(ckpt_dir.glob('checkpoint_step_*.pt'),key=lambda p:p.stat().st_mtime,reverse=True)
    for old in all_ckpts[keep:]:
        if old.name==name: continue
        try:
            old.unlink()
            side=old.with_suffix(old.suffix+'.sha256')
            if side.exists(): side.unlink()
        except OSError:
            pass
    try: local_path.unlink()
    except OSError: pass
    return {'file':name,'sha256':digest}

def load_latest_checkpoint(cand_dir, expected_identity):
    ckpt_dir=Path(cand_dir)/'checkpoints'
    if not ckpt_dir.exists(): return None
    candidates=[]
    pointer=ckpt_dir/'latest_checkpoint.json'
    if pointer.exists():
        try:
            p=json.loads(pointer.read_text(encoding='utf-8'))
            f=ckpt_dir/p['file']
            if f.exists() and sha256_file(f)==p['sha256']:
                candidates.append(f)
        except Exception as e: print('Latest pointer invalid; scanning verified backups:',e)
    for f in sorted(ckpt_dir.glob('checkpoint_step_*.pt'),key=lambda p:p.stat().st_mtime,reverse=True):
        if f in candidates: continue
        side=f.with_suffix(f.suffix+'.sha256')
        if not side.exists(): continue
        try:
            if sha256_file(f)==side.read_text(encoding='utf-8').strip(): candidates.append(f)
        except Exception: pass
    for f in candidates:
        try:
            try: state=torch.load(f,map_location='cpu',weights_only=False)
            except TypeError: state=torch.load(f,map_location='cpu')
            if state.get('identity') != expected_identity:
                raise RuntimeError('Checkpoint identity/config/data/code hash mismatch; refusing unsafe resume.')
            print(f'Resuming from {f.name}; epoch={state["next_epoch"]+1}, next_batch={state["next_batch_idx"]}, step={state["global_step"]}')
            return state
        except RuntimeError:
            raise
        except Exception as e:
            print(f'Cannot load checkpoint {f.name}; trying older verified checkpoint: {e}')
    return None

def make_model(config, vocab_size, dropout):
    a=config['architecture']
    return CharCNN(vocab_size=vocab_size,embedding_dim=a['embedding_dim'],kernel_sizes=tuple(a['kernel_sizes']),
                   conv_channels=a['conv_channels'],hidden_dim=a['hidden_dim'],dropout=dropout,pad_id=config['encoding']['pad_id'])

def batch_predict(model, X, lengths, device, batch_size, amp_enabled=True, y_true=None, criterion=None):
    model.eval(); preds=[]; scores=[]; loss_sum=0.0; loss_count=0
    with torch.no_grad():
        for start in range(0,len(X),batch_size):
            xb=X[start:start+batch_size].to(device,dtype=torch.long,non_blocking=True)
            lb=lengths[start:start+batch_size].to(device,dtype=torch.long,non_blocking=True)
            with autocast_context(amp_enabled):
                logits=model(xb,lb)
                loss=None
                if y_true is not None and criterion is not None:
                    yb=torch.as_tensor(y_true[start:start+batch_size],dtype=torch.long,device=device)
                    loss=criterion(logits,yb)
            logits32=logits.float()
            pred=logits32.argmax(dim=1)
            prob=torch.softmax(logits32,dim=1)[:,1]
            preds.extend(pred.cpu().numpy().tolist()); scores.extend(prob.cpu().numpy().tolist())
            if loss is not None:
                loss_sum += float(loss.detach().float().item()) * len(xb)
                loss_count += len(xb)
    mean_loss=(loss_sum/max(1,loss_count)) if loss_count else None
    return np.asarray(preds,dtype=np.int64),np.asarray(scores,dtype=np.float32),mean_loss

def save_candidate_model(model_state, config, candidate, vocab_size, vocab_sha, config_sha, dest, work_root, best_metrics, best_epoch):
    model_args={'vocab_size':vocab_size,'embedding_dim':config['architecture']['embedding_dim'],
        'kernel_sizes':config['architecture']['kernel_sizes'],'conv_channels':config['architecture']['conv_channels'],
        'hidden_dim':config['architecture']['hidden_dim'],'dropout':candidate['dropout'],'pad_id':config['encoding']['pad_id']}
    payload={'format_version':1,'model_state_dict':cpu_state_dict(model_state),'model_args':model_args,
             'candidate':candidate,'best_metrics':best_metrics,'best_epoch':int(best_epoch),
             'max_length':int(config['encoding']['max_length']),'vocabulary_sha256':vocab_sha,'config_sha256':config_sha,
             'label_mapping':{'0':'Non-Promotion','1':'Promotion'}}
    tmp=Path(work_root)/'tmp_artifacts'/f'best_model_{uuid.uuid4().hex}.pt'; tmp.parent.mkdir(parents=True,exist_ok=True)
    torch.save(payload,tmp)
    digest=persist_file(tmp,dest)
    try: tmp.unlink()
    except OSError: pass
    return digest

def candidate_complete(cand_dir, identity):
    rp=Path(cand_dir)/'candidate_result.json'
    mp=Path(cand_dir)/'best_model.pt'
    if not rp.exists() or not mp.exists(): return None
    try:
        r=json.loads(rp.read_text(encoding='utf-8'))
        if r.get('status')!='COMPLETED' or r.get('identity')!=identity: return None
        if sha256_file(mp)!=r.get('model_sha256'): return None
        return r
    except Exception: return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=['smoke','official','validate'],required=True)
    ap.add_argument('--workspace',required=True)
    ap.add_argument('--persistent-root',required=True)
    ap.add_argument('--resume',choices=['auto','never'],default='auto')
    ap.add_argument('--stop-after-steps',type=int,default=0,help='Controlled interruption for resume smoke test; 0 disables.')
    args=ap.parse_args()
    work=Path(args.workspace); persist=Path(args.persistent_root)
    data_dir=work/'data_snapshot'; project=persist/'training'
    train_path=data_dir/'train_v1.csv'; val_path=data_dir/'validation_v1.csv'
    config_path=project/'model_config.json'; vocab_path=project/'vocab.json'
    for p in [train_path,val_path,config_path,vocab_path]:
        if not p.exists(): raise FileNotFoundError(p)
    config=json.loads(config_path.read_text(encoding='utf-8'))
    vocab_obj=json.loads(vocab_path.read_text(encoding='utf-8'))
    vocab=vocab_obj['stoi']; vocab_size=len(vocab_obj['itos']); vocab_sha=config['vocabulary_sha256']
    train_sha=sha256_file(train_path); val_sha=sha256_file(val_path)
    if train_sha!=config['data']['train_sha256'] or val_sha!=config['data']['validation_sha256']:
        raise RuntimeError('Data hash mismatch with frozen configuration; refusing to train/resume.')
    config_sha=sha256_file(config_path); script_sha=sha256_file(Path(__file__).resolve())
    identity={'train_sha256':train_sha,'validation_sha256':val_sha,'config_sha256':config_sha,
              'script_sha256':script_sha,'vocabulary_sha256':vocab_sha,'seed':config['seed'],'mode':args.mode}
    train_df=pd.read_csv(train_path,low_memory=False); val_df=pd.read_csv(val_path,low_memory=False)
    validate_df(train_df,'TRAIN',32920,3960); validate_df(val_df,'VALIDATION',4116,495)
    if 'leakage_group_id' in train_df.columns and 'leakage_group_id' in val_df.columns:
        if set(train_df.leakage_group_id.astype(str)) & set(val_df.leakage_group_id.astype(str)):
            raise RuntimeError('leakage_group_id overlap detected')
    if not torch.cuda.is_available() or 'T4' not in torch.cuda.get_device_name(0).upper():
        raise RuntimeError('Expected an active NVIDIA T4 CUDA GPU. Stop and select T4 runtime.')
    device=torch.device('cuda')
    torch.backends.cudnn.benchmark=False
    torch.backends.cudnn.deterministic=True
    print(f'GPU={torch.cuda.get_device_name(0)} | torch={torch.__version__} | CUDA={torch.version.cuda}')

    # Smoke is an engineering check, not a research result; train vocabulary/config remain those of the full train split.
    if args.mode=='smoke':
        seed=int(config['seed'])
        train_idx,_=next(StratifiedShuffleSplit(n_splits=1,train_size=int(config['smoke']['train_rows']),random_state=seed).split(train_df,train_df.canonical_label))
        val_idx,_=next(StratifiedShuffleSplit(n_splits=1,train_size=int(config['smoke']['validation_rows']),random_state=seed).split(val_df,val_df.canonical_label))
        train_df=train_df.iloc[train_idx].reset_index(drop=True); val_df=val_df.iloc[val_idx].reset_index(drop=True)
        batch_size=int(config['smoke']['batch_size']); max_epochs=int(config['smoke']['max_epochs'])
        candidates=config['candidates'][:int(config['smoke']['candidate_limit'])]
        run_dir=persist/'runs'/'smoke'
    elif args.mode=='official':
        batch_size=int(config['training']['batch_size']); max_epochs=int(config['training']['max_epochs'])
        candidates=config['candidates']
        run_dir=persist/'runs'/'official'
    else:
        run_dir=persist/'runs'/'official'
        return validate_final(work,persist,config,vocab_obj,identity)

    X_train_np,len_train_np=encode_texts(train_df.text_raw.astype(str).tolist(),vocab,int(config['encoding']['max_length']),int(config['encoding']['unk_id']))
    X_val_np,len_val_np=encode_texts(val_df.text_raw.astype(str).tolist(),vocab,int(config['encoding']['max_length']),int(config['encoding']['unk_id']))
    X_train=torch.from_numpy(X_train_np).pin_memory(); L_train=torch.from_numpy(len_train_np).pin_memory()
    Y_train=torch.tensor(train_df.canonical_label.astype(int).to_numpy(),dtype=torch.long).pin_memory()
    X_val=torch.from_numpy(X_val_np).pin_memory(); L_val=torch.from_numpy(len_val_np).pin_memory()
    y_val=val_df.canonical_label.astype(int).to_numpy()
    trunc_train=int(sum(len(str(t))>config['encoding']['max_length'] for t in train_df.text_raw))
    trunc_val=int(sum(len(str(t))>config['encoding']['max_length'] for t in val_df.text_raw))
    print(f'Encoding ready: vocab={vocab_size:,}, max_length={config["encoding"]["max_length"]}, batch={batch_size}, truncation train={trunc_train}/{len(train_df)}, validation={trunc_val}/{len(val_df)}')

    if args.mode=='validate': return validate_final(work,persist,config,vocab_obj,identity)
    run_dir.mkdir(parents=True,exist_ok=True)
    all_results=[]
    for cand_i,cand in enumerate(candidates):
        cid=cand['candidate_id']; cand_dir=run_dir/'candidates'/cid; cand_dir.mkdir(parents=True,exist_ok=True)
        done=candidate_complete(cand_dir,identity) if args.resume=='auto' else None
        if done is not None:
            print(f'SKIP completed candidate {cid}; verified model hash={done["model_sha256"]}')
            all_results.append(done); continue
        candidate_identity=dict(identity); candidate_identity['candidate_id']=cid
        seed=int(config['seed'])+cand_i*1000
        torch.cuda.empty_cache(); seed_everything(seed)
        model=make_model(config,vocab_size,float(cand['dropout'])).to(device)
        optimizer=torch.optim.AdamW(model.parameters(),lr=float(cand['learning_rate']),weight_decay=float(config['training']['weight_decay']))
        scaler=get_scaler(enabled=True)
        counts=np.bincount(train_df.canonical_label.astype(int).to_numpy(),minlength=2).astype(np.float64)
        class_weights=(len(y_val)*0+len(train_df)/ (2.0*counts)) # label weights are derived from the current training partition only
        if args.mode=='smoke':
            counts=np.bincount(train_df.canonical_label.astype(int).to_numpy(),minlength=2).astype(np.float64)
            class_weights=len(train_df)/(2.0*counts)
        weight_t=torch.tensor(class_weights,dtype=torch.float32,device=device)
        criterion=nn.CrossEntropyLoss(weight=weight_t)
        next_epoch=0; next_batch_idx=0; global_step=0; best_rank=(-1.,-1.,-1.,-1.); best_metrics=None
        best_epoch=0; best_model_state=None; patience_count=0; history=[]; epoch_loss_sum=0.0; epoch_loss_count=0
        state=load_latest_checkpoint(cand_dir,candidate_identity) if args.resume=='auto' else None
        if state is not None:
            model.load_state_dict(state['model_state_dict']); optimizer.load_state_dict(state['optimizer_state_dict'])
            scaler.load_state_dict(state['scaler_state_dict'])
            next_epoch=int(state['next_epoch']); next_batch_idx=int(state['next_batch_idx']); global_step=int(state['global_step'])
            best_rank=tuple(state['best_rank']); best_metrics=state['best_metrics']; best_epoch=int(state['best_epoch'])
            best_model_state=state['best_model_state_dict']; patience_count=int(state['patience_count'])
            history=state['history']; epoch_loss_sum=float(state.get('epoch_loss_sum',0.0)); epoch_loss_count=int(state.get('epoch_loss_count',0))
            restore_rng(state['rng_state'])
        else:
            # If a checkpoint exists but cannot be safely resumed, do not silently overwrite it.
            ckpt_files=list((cand_dir/'checkpoints').glob('checkpoint_step_*.pt')) if (cand_dir/'checkpoints').exists() else []
            if ckpt_files and args.resume=='auto':
                raise RuntimeError(f'{cid}: checkpoints exist but no valid compatible checkpoint was found. Do not restart/overwrite automatically.')
            best_model_state=cpu_state_dict(model.state_dict())
        print(f'\n=== {args.mode.upper()} {cid}: lr={cand["learning_rate"]}, dropout={cand["dropout"]} ===')
        num_batches=int(np.ceil(len(train_df)/batch_size))
        steps_this_session=0; stopped_intentionally=False
        for epoch in range(next_epoch,max_epochs):
            epoch_started=time.time()
            model.train()
            generator=torch.Generator(device='cpu'); generator.manual_seed(seed+epoch*1000003)
            permutation=torch.randperm(len(train_df),generator=generator)
            b_start=next_batch_idx if epoch==next_epoch else 0
            for batch_idx in range(b_start,num_batches):
                lo=batch_idx*batch_size; hi=min(lo+batch_size,len(train_df))
                ix=permutation[lo:hi]
                xb=X_train[ix].to(device=device,dtype=torch.long,non_blocking=True)
                lb=L_train[ix].to(device=device,dtype=torch.long,non_blocking=True)
                yb=Y_train[ix].to(device=device,non_blocking=True)
                optimizer.zero_grad(set_to_none=True)
                with autocast_context(True): logits=model(xb,lb); loss=criterion(logits,yb)
                if not torch.isfinite(loss): raise RuntimeError(f'Non-finite loss at {cid}, epoch={epoch+1}, step={global_step}')
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(),float(config['training']['grad_clip_norm']))
                scaler.step(optimizer); scaler.update()
                global_step+=1; steps_this_session+=1
                epoch_loss_sum+=float(loss.detach().float().item())*len(ix); epoch_loss_count+=len(ix)
                next_e=epoch; next_b=batch_idx+1
                should_save=(global_step % int(config['training']['checkpoint_every_steps'])==0)
                should_pause=(args.stop_after_steps>0 and steps_this_session>=args.stop_after_steps)
                if should_save or should_pause:
                    ckpt={'identity':candidate_identity,'candidate_id':cid,'model_state_dict':cpu_state_dict(model.state_dict()),
                          'optimizer_state_dict':optimizer.state_dict(),'scaler_state_dict':scaler.state_dict(),
                          'next_epoch':next_e,'next_batch_idx':next_b,'global_step':global_step,
                          'best_rank':best_rank,'best_metrics':best_metrics,'best_epoch':best_epoch,
                          'best_model_state_dict':best_model_state,'patience_count':patience_count,'history':history,
                          'epoch_loss_sum':epoch_loss_sum,'epoch_loss_count':epoch_loss_count,'rng_state':capture_rng(),
                          'saved_at':datetime.now(timezone.utc).isoformat()}
                    ref=write_checkpoint(ckpt,cand_dir,work/'tmp_checkpoints')
                    print(f'Checkpoint persisted: {ref["file"]} step={global_step}')
                if should_pause:
                    stopped_intentionally=True
                    print(f'PAUSED intentionally after {steps_this_session} steps. Checkpoint is saved. Rerun the same command without --stop-after-steps to resume.')
                    return 0
            # Full epoch complete: evaluate validation and select checkpoint by deterministic metrics rank.
            preds, probs, val_loss=batch_predict(model,X_val,L_val,device,batch_size,True,y_true=y_val,criterion=criterion)
            metrics=compute_metrics(y_val,preds)
            metrics['validation_loss']=float(val_loss)
            rank=metric_rank(metrics)
            improved=rank>best_rank
            if improved:
                best_rank=rank; best_metrics=dict(metrics); best_epoch=epoch+1
                best_model_state=cpu_state_dict(model.state_dict()); patience_count=0
            else:
                patience_count+=1
            mean_train_loss=epoch_loss_sum/max(1,epoch_loss_count)
            row={'candidate_id':cid,'epoch':epoch+1,'global_step':global_step,'train_loss':mean_train_loss,
                 'learning_rate':float(cand['learning_rate']),'dropout':float(cand['dropout']),
                 'validation_loss':float(val_loss),'f1_promotion':metrics['f1_promotion'],
                 'precision_promotion':metrics['precision_promotion'],'recall_promotion':metrics['recall_promotion'],
                 'accuracy':metrics['accuracy'],'macro_f1':metrics['macro_f1'],
                 'TN':metrics['confusion_matrix']['TN'],'FP':metrics['confusion_matrix']['FP'],
                 'FN':metrics['confusion_matrix']['FN'],'TP':metrics['confusion_matrix']['TP'],
                 'best_f1_so_far':best_rank[0],'is_best_epoch':bool(improved),
                 'epoch_duration_sec':round(time.time()-epoch_started,3)}
            history.append(row)
            # The epoch boundary checkpoint carries updated best weights and early-stopping state.
            next_epoch=epoch+1; next_batch_idx=0; epoch_loss_sum=0.0; epoch_loss_count=0
            ckpt={'identity':candidate_identity,'candidate_id':cid,'model_state_dict':cpu_state_dict(model.state_dict()),
                  'optimizer_state_dict':optimizer.state_dict(),'scaler_state_dict':scaler.state_dict(),
                  'next_epoch':next_epoch,'next_batch_idx':0,'global_step':global_step,
                  'best_rank':best_rank,'best_metrics':best_metrics,'best_epoch':best_epoch,
                  'best_model_state_dict':best_model_state,
                  'patience_count':patience_count,'history':history,'epoch_loss_sum':0.0,'epoch_loss_count':0,
                  'rng_state':capture_rng(),'saved_at':datetime.now(timezone.utc).isoformat()}
            ref=write_checkpoint(ckpt,cand_dir,work/'tmp_checkpoints')
            # Persist human-readable history only after the epoch checkpoint is safely on Drive.
            hist_path=work/'tmp_artifacts'/f'history_{cid}.csv'; hist_path.parent.mkdir(parents=True,exist_ok=True)
            pd.DataFrame(history).to_csv(hist_path,index=False)
            persist_file(hist_path,cand_dir/'training_history.csv')
            print(f'Epoch {epoch+1}/{max_epochs} | loss={mean_train_loss:.4f} | F1P={metrics["f1_promotion"]:.4f} | P={metrics["precision_promotion"]:.4f} | R={metrics["recall_promotion"]:.4f} | best_epoch={best_epoch} | patience={patience_count}/{config["training"]["early_stopping_patience"]}')
            # Persist separate inference model after the resumable checkpoint records the new best state.
            if improved:
                best_sha=save_candidate_model(best_model_state,config,cand,vocab_size,vocab_sha,config_sha,cand_dir/'best_model.pt',work,best_metrics,best_epoch)
                atomic_json(cand_dir/'best_model_manifest.json',{'sha256':best_sha,'candidate_id':cid,'best_epoch':best_epoch,'metrics':best_metrics,'identity':candidate_identity})
            if patience_count>=int(config['training']['early_stopping_patience']):
                print(f'Early stopping {cid} after {epoch+1} epochs.')
                break
        # Export best model even if resumed from a checkpoint whose best artifact was not yet uploaded.
        if best_metrics is None or best_model_state is None: raise RuntimeError(f'{cid}: no valid best validation checkpoint')
        best_sha=save_candidate_model(best_model_state,config,cand,vocab_size,vocab_sha,config_sha,cand_dir/'best_model.pt',work,best_metrics,best_epoch)
        hist_path=work/'tmp_artifacts'/f'history_{cid}.csv'; hist_path.parent.mkdir(parents=True,exist_ok=True)
        pd.DataFrame(history).to_csv(hist_path,index=False); persist_file(hist_path,cand_dir/'training_history.csv')
        result={'status':'COMPLETED','candidate_id':cid,'candidate':cand,'best_epoch':best_epoch,'best_metrics':best_metrics,
                'history':history,'identity':identity,'candidate_identity':candidate_identity,'model_sha256':best_sha,
                'config_sha256':config_sha,'data_hashes':{'train':train_sha,'validation':val_sha},
                'steps':global_step,'completed_at':datetime.now(timezone.utc).isoformat(),
                'train_rows_used':len(train_df),'validation_rows_used':len(val_df),'is_smoke':args.mode=='smoke'}
        atomic_json(cand_dir/'candidate_result.json',result)
        all_results.append(result)
        print(f'Candidate completed: {cid} | best epoch={best_epoch} | F1P={best_metrics["f1_promotion"]:.4f}')
    # For smoke, leave smoke artifacts isolated; do not label smoke as research result.
    if args.mode=='smoke':
        atomic_json(run_dir/'smoke_run_manifest.json',{'status':'SMOKE_COMPLETED','identity':identity,'completed_at':datetime.now(timezone.utc).isoformat(),
                    'warning':'Technical smoke test only. Not a scientific result; do not compare with official metrics.'})
        print('SMOKE TEST COMPLETED. This is only a technical check; no test set was read.')
        return 0
    finalize_official(work,persist,config,vocab_obj,identity,run_dir,train_df,val_df,X_val,L_val,y_val,device,batch_size)
    return 0

def finalize_official(work,persist,config,vocab_obj,identity,run_dir,train_df,val_df,X_val,L_val,y_val,device,batch_size):
    cand_dirs=sorted((run_dir/'candidates').glob('*'))
    results=[]
    for cdir in cand_dirs:
        rp=cdir/'candidate_result.json'; mp=cdir/'best_model.pt'
        if not rp.exists() or not mp.exists(): raise RuntimeError(f'Candidate incomplete: {cdir.name}. Resume official training.')
        r=json.loads(rp.read_text(encoding='utf-8'))
        if r.get('status')!='COMPLETED' or r.get('identity')!=identity or sha256_file(mp)!=r.get('model_sha256'):
            raise RuntimeError(f'Candidate result/model verification failed: {cdir.name}')
        results.append(r)
    expected=len(config['candidates'])
    if len(results)!=expected: raise RuntimeError(f'Expected {expected} completed candidates, found {len(results)}')
    results.sort(key=lambda r:next(i for i,c in enumerate(config['candidates']) if c['candidate_id']==r['candidate_id']))
    # Deterministic selection: F1 Promotion, precision, recall, macro-F1; fixed order wins exact ties.
    best=max(results,key=lambda r:metric_rank(r['best_metrics']))
    selected_dir=run_dir/'candidates'/best['candidate_id']; selected_file=selected_dir/'best_model.pt'
    final_dir=persist/'model'; final_dir.mkdir(parents=True,exist_ok=True)
    final_model=final_dir/'weights.pt'; model_sha=persist_file(selected_file,final_model)
    persist_file(persist/'training'/'vocab.json',final_dir/'vocab.json')
    persist_file(persist/'training'/'charcnn_v1.json',final_dir/'model_config.json')
    persist_file(persist/'training'/'data_contract.json',final_dir/'data_contract.json')
    payload=torch.load(final_model,map_location='cpu',weights_only=False)
    args=payload['model_args']; model=CharCNN(**args).to(device); model.load_state_dict(payload['model_state_dict']); model.eval()
    # Validation inference only; test set is never opened.
    counts=np.bincount(train_df.canonical_label.astype(int).to_numpy(),minlength=2).astype(np.float64)
    class_weights=torch.tensor(len(train_df)/(2.0*counts),dtype=torch.float32,device=device)
    val_criterion=nn.CrossEntropyLoss(weight=class_weights)
    pred,prob,val_loss=batch_predict(model,X_val,L_val,device,batch_size,True,y_true=y_val,criterion=val_criterion)
    val_metrics=compute_metrics(y_val,pred)
    val_metrics['validation_loss']=float(val_loss)
    reports=persist/'reports'/'training'; reports.mkdir(parents=True,exist_ok=True)
    rows=[]
    for r in results:
        m=r['best_metrics']; rows.append({'candidate_id':r['candidate_id'],'learning_rate':r['candidate']['learning_rate'],
           'dropout':r['candidate']['dropout'],'best_epoch':r['best_epoch'],'steps':r['steps'],
           'f1_promotion':m['f1_promotion'],'precision_promotion':m['precision_promotion'],'recall_promotion':m['recall_promotion'],
           'accuracy':m['accuracy'],'macro_f1':m['macro_f1'],'TN':m['confusion_matrix']['TN'],'FP':m['confusion_matrix']['FP'],
           'FN':m['confusion_matrix']['FN'],'TP':m['confusion_matrix']['TP'],'is_selected':r['candidate_id']==best['candidate_id']})
    pd.DataFrame(rows).to_csv(work/'tmp_artifacts'/'tuning_results.csv',index=False)
    persist_file(work/'tmp_artifacts'/'tuning_results.csv',reports/'tuning_results.csv')
    all_hist=[]
    for r in results:
        hp=run_dir/'candidates'/r['candidate_id']/'training_history.csv'
        if hp.exists():
            h=pd.read_csv(hp); all_hist.append(h)
    if all_hist:
        pd.concat(all_hist,ignore_index=True).to_csv(work/'tmp_artifacts'/'training_history.csv',index=False)
        persist_file(work/'tmp_artifacts'/'training_history.csv',reports/'training_history.csv')
    metric_doc={'selected_candidate':best['candidate_id'],'candidate':best['candidate'],'best_epoch':best['best_epoch'],
                **val_metrics,'selection_source':'validation only','test_set_used':False}
    atomic_json(reports/'validation_metrics.json',metric_doc)
    preds_df=pd.DataFrame({'record_id':val_df['record_id'].astype(str),'actual_label':y_val,'predicted_label':pred,
                           'promotion_probability':np.round(prob,6),'is_correct':(np.asarray(y_val)==pred)})
    preds_df.to_csv(work/'tmp_artifacts'/'validation_predictions.csv',index=False)
    persist_file(work/'tmp_artifacts'/'validation_predictions.csv',reports/'validation_predictions.csv')
    run_manifest={'experiment_name':config['experiment_name'],'status':'SUCCESS','run_timestamp_utc':datetime.now(timezone.utc).isoformat(),
       'identity':identity,'environment':{'python':platform.python_version(),'torch':torch.__version__,'cuda':torch.version.cuda,
          'numpy':np.__version__,'pandas':pd.__version__,'gpu':torch.cuda.get_device_name(0),'gpu_vram_gib':round(torch.cuda.get_device_properties(0).total_memory/1024**3,3)},
       'config_sha256':sha256_file(persist/'training'/'charcnn_v1.json'),'vocabulary_sha256':config['vocabulary_sha256'],
       'data_hashes':{'train':sha256_file(work/'data_snapshot'/'train_v1.csv'),'validation':sha256_file(work/'data_snapshot'/'validation_v1.csv')},
       'selected_candidate':best['candidate_id'],'selected_metrics':metric_doc,'candidate_results':rows,'final_model_sha256':model_sha,
       'train_rows':len(train_df),'validation_rows':len(val_df),'test_set_used':False,
       'method':'All candidates trained on normal train; selected using normal validation F1 Promotion; no test data read.'}
    atomic_json(reports/'run_manifest.json',run_manifest)
    atomic_json(reports/'artifact_validation_report.json',{'status':'PENDING_VALIDATION_CELL','model_sha256':model_sha,'vocabulary_sha256':config['vocabulary_sha256']})
    print('\nOFFICIAL TRAINING COMPLETE')
    print('Selected candidate:',best['candidate_id'])
    print('Validation F1 Promotion:',round(val_metrics['f1_promotion'],6))
    print('Final model:',final_model)
    print('Reports:',reports)

def validate_final(work,persist,config,vocab_obj,identity):
    run_dir=persist/'runs'/'official'; reports=persist/'reports'/'training'; final_dir=persist/'model'
    manifest_path=reports/'run_manifest.json'; model_path=final_dir/'weights.pt'
    if not manifest_path.exists() or not model_path.exists(): raise RuntimeError('Official final artifacts not found. Complete official training first.')
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('status')!='SUCCESS': raise RuntimeError('Official run manifest status is not SUCCESS')
    for n,h in [('train_v1.csv',config['data']['train_sha256']),('validation_v1.csv',config['data']['validation_sha256'])]:
        p=work/'data_snapshot'/n
        if sha256_file(p)!=h: raise RuntimeError(f'Data hash changed: {n}')
    payload=torch.load(model_path,map_location='cpu',weights_only=False)
    vocab_path=final_dir/'vocab.json'
    vocab_f=json.loads(vocab_path.read_text(encoding='utf-8'))
    if sha256_file(model_path)!=manifest['final_model_sha256']: raise RuntimeError('Final model SHA256 mismatch')
    if sha256_json(vocab_f)!=config['vocabulary_sha256']: raise RuntimeError('Vocabulary hash mismatch')
    args=payload['model_args']; device=torch.device('cuda')
    model=CharCNN(**args).to(device); model.load_state_dict(payload['model_state_dict']); model.eval()
    val=pd.read_csv(work/'data_snapshot'/'validation_v1.csv',low_memory=False)
    enc, lens=encode_texts(val.text_raw.astype(str).tolist(),vocab_f['stoi'],int(config['encoding']['max_length']),int(config['encoding']['unk_id']))
    x=torch.from_numpy(enc).pin_memory(); l=torch.from_numpy(lens).pin_memory()
    # Use the same GPU/AMP inference path used by official validation, then compare all saved predictions.
    pred_all, _, _ = batch_predict(model,x,l,device,64,True)
    saved=pd.read_csv(reports/'validation_predictions.csv')
    if len(saved)!=len(pred_all) or not np.array_equal(saved['predicted_label'].to_numpy(dtype=np.int64),pred_all):
        raise RuntimeError('Reloaded model predictions mismatch validation_predictions.csv')
    y=val.canonical_label.to_numpy(dtype=np.int64); metrics=compute_metrics(y,pred_all)
    if any(not np.isfinite(v) for v in [metrics['f1_promotion'],metrics['precision_promotion'],metrics['recall_promotion'],metrics['accuracy'],metrics['macro_f1']]):
        raise RuntimeError('Non-finite metrics')
    zip_path=persist/'model_bundle.zip'
    import zipfile
    local_zip=Path(work)/'model_bundle.zip'
    pre_zip_report={'status':'PASS','final_model_sha256':sha256_file(model_path),'vocabulary_sha256':config['vocabulary_sha256'],
            'train_sha256':sha256_file(work/'data_snapshot'/'train_v1.csv'),'validation_sha256':sha256_file(work/'data_snapshot'/'validation_v1.csv'),
            'rows_validation':len(val),'predictions_match_saved_validation':True,
            'zip_integrity':'TO_BE_CHECKED','test_set_used':False,'validated_at_utc':datetime.now(timezone.utc).isoformat(),
            'note':'Archive hash is recorded in the on-Drive copy to avoid a circular self-hash.'}
    atomic_json(reports/'artifact_validation_report.json',pre_zip_report)
    include=[persist/'training'/'charcnn_train.py',persist/'training'/'charcnn_v1.json',persist/'training'/'vocab.json',
             persist/'training'/'data_contract.json',persist/'training'/'train_text_length_profile.json',
             reports/'tuning_results.csv',reports/'validation_metrics.json',reports/'validation_predictions.csv',
             reports/'training_history.csv',reports/'run_manifest.json',reports/'artifact_validation_report.json',
             model_path,final_dir/'vocab.json',final_dir/'model_config.json',final_dir/'data_contract.json']
    with zipfile.ZipFile(local_zip,'w',compression=zipfile.ZIP_DEFLATED) as zf:
        for p in include:
            if p.exists(): zf.write(p,arcname=str(p.relative_to(persist)))
    with zipfile.ZipFile(local_zip,'r') as zf:
        bad=zf.testzip()
        if bad: raise RuntimeError(f'Final ZIP corrupt at {bad}')
        bad_names=[n for n in zf.namelist() if 'test_normal_v1' in n.lower() or 'obfuscated_test_v1' in n.lower()]
        if bad_names: raise RuntimeError(f'Test file accidentally included in final ZIP: {bad_names}')
    zip_sha=persist_file(local_zip,zip_path)
    report={'status':'PASS','final_model_sha256':sha256_file(model_path),'vocabulary_sha256':config['vocabulary_sha256'],
            'train_sha256':sha256_file(work/'data_snapshot'/'train_v1.csv'),'validation_sha256':sha256_file(work/'data_snapshot'/'validation_v1.csv'),
            'rows_validation':len(val),'predictions_match_saved_validation':True,'zip_sha256':zip_sha,
            'zip_integrity':'PASS','test_set_used':False,'validated_at_utc':datetime.now(timezone.utc).isoformat()}
    atomic_json(reports/'artifact_validation_report.json',report)
    print('FINAL ARTIFACT VALIDATION PASS')
    print('Model reload predictions: IDENTICAL to saved validation predictions')
    print('ZIP:',zip_path)
    print('ZIP SHA256:',zip_sha)
    print('Metrics:',metrics)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
