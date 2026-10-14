#!/usr/bin/env python3
"""Inference-only Stage 11 evaluation for isolated DS3 OOD and DS5 external sets."""
from __future__ import annotations
import argparse, hashlib, json, runpy, sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
CFG = ROOT/"configs/evaluation/stage10_robustness.json"
MANIFEST = ROOT/"data/processed/stage11/manifest_v1.json"
OUT = ROOT/"reports/stage11/domain_shift"
DATASETS = {"ds3_ood":ROOT/"data/processed/stage11/ds3_ood_v1.csv",
            "ds5_external":ROOT/"data/processed/stage11/ds5_external_v1.csv"}
DISPLAY = {"linear_svm":"Linear SVM","char_cnn":"Char-CNN","indobert":"IndoBERT"}

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def load_dataset(key,path,manifest):
    df=pd.read_csv(path,encoding="utf-8")
    required={"record_id","text_raw","canonical_label"}
    if not required.issubset(df.columns): raise ValueError(f"{path}: required columns missing")
    if df.record_id.duplicated().any(): raise ValueError(f"{path}: duplicate IDs")
    df["canonical_label"]=pd.to_numeric(df.canonical_label,errors="raise").astype(int)
    if not set(df.canonical_label.unique()).issubset({0,1}): raise ValueError(f"{path}: labels are not binary")
    mkey="ds3_ood_v1" if key=="ds3_ood" else "ds5_external_v1"
    expected=manifest.get("datasets",{}).get(mkey,{})
    if expected.get("sha256") and sha256(path)!=expected["sha256"]: raise ValueError(f"{path}: SHA-256 mismatch")
    if expected.get("rows") is not None and int(expected["rows"])!=len(df): raise ValueError(f"{path}: row count mismatch")
    for label,field in [(1,"promotion"),(0,"non_promotion")]:
        if expected.get(field) is not None and int(expected[field])!=int((df.canonical_label==label).sum()):
            raise ValueError(f"{path}: {field} count mismatch")
    return df

def load_models(cfg,requested,device):
    helper=runpy.run_path(str(ROOT/"scripts/22_run_stage10_robustness.py"))
    actual=device
    if device=="auto":
        try:
            import torch
            actual="cuda" if torch.cuda.is_available() else "cpu"
        except ImportError: actual="cpu"
    loaded,errors={},[]
    for name in requested:
        try:
            if name=="linear_svm":
                obj=helper["load_svm_pipeline"](str(ROOT/cfg["models"][name]["model_path"]))
                loaded[name]=lambda texts,obj=obj:helper["predict_svm"](obj,texts)
            elif name=="char_cnn":
                m=cfg["models"][name]
                obj=helper["CharCNNModule"](str(ROOT/m["model_weights_path"]),str(ROOT/m["vocab_path"]),device=actual)
                loaded[name]=lambda texts,obj=obj:obj.predict(texts)
            else:
                m=cfg["models"][name]
                obj=helper["IndoBERTModule"](str(ROOT/m["model_dir"]),device=actual)
                loaded[name]=lambda texts,obj=obj:obj.predict(texts)
            print(f"[PASS] Loaded {DISPLAY[name]}")
        except Exception as exc:
            message=f"{name}: {type(exc).__name__}: {exc}";errors.append(message)
            print(f"[BLOCKED] {message}",file=sys.stderr)
    return loaded,errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dataset",choices=["ds3_ood","ds5_external","both"],default="both")
    ap.add_argument("--models",nargs="+",choices=list(DISPLAY),default=list(DISPLAY))
    ap.add_argument("--device",choices=["auto","cpu","cuda"],default="auto")
    args=ap.parse_args()
    if not CFG.exists() or not MANIFEST.exists(): raise SystemExit("Stage 10 config or Stage 11 manifest missing")
    cfg=json.loads(CFG.read_text(encoding="utf-8"));manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    ds_names=["ds3_ood","ds5_external"] if args.dataset=="both" else [args.dataset]
    datasets,errors={},[]
    for key in ds_names:
        try:
            path=DATASETS[key]
            if not path.exists(): raise FileNotFoundError(path)
            datasets[key]=load_dataset(key,path,manifest);print(f"[PASS] {key}: {len(datasets[key]):,} rows")
        except Exception as exc:
            errors.append(f"{key}: {type(exc).__name__}: {exc}");print(f"[BLOCKED] {errors[-1]}",file=sys.stderr)
    if not datasets:return 2
    models,model_errors=load_models(cfg,args.models,args.device);errors.extend(model_errors)
    OUT.mkdir(parents=True,exist_ok=True);metrics=[]
    for dname,df in datasets.items():
        y=df.canonical_label.to_numpy(dtype=int);texts=df.text_raw.fillna("").astype(str).tolist()
        for mname,predict in models.items():
            try:
                pred,score=predict(texts);pred=np.asarray(pred,dtype=int);score=np.asarray(score,dtype=float)
                if len(pred)!=len(df) or len(score)!=len(df) or not np.isin(pred,[0,1]).all():
                    raise ValueError("Output length or predicted labels invalid")
                tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
                pred_path=OUT/f"{dname}_{mname}_predictions.csv"
                pd.DataFrame({"record_id":df.record_id.astype(str),"canonical_label":y,"predicted_label":pred,
                              "model_score":score,"is_correct":pred==y}).to_csv(pred_path,index=False,encoding="utf-8",lineterminator="\n")
                metrics.append({"dataset":dname,"model":mname,"model_display_name":DISPLAY[mname],"n":len(df),
                  "n_non_promotion":int((y==0).sum()),"n_promotion":int((y==1).sum()),
                  "f1_promotion":f1_score(y,pred,pos_label=1,zero_division=0),
                  "precision_promotion":precision_score(y,pred,pos_label=1,zero_division=0),
                  "recall_promotion":recall_score(y,pred,pos_label=1,zero_division=0),
                  "accuracy":accuracy_score(y,pred),"macro_f1":f1_score(y,pred,average="macro",zero_division=0),
                  "TN":int(tn),"FP":int(fp),"FN":int(fn),"TP":int(tp),"candidate_sha256":sha256(DATASETS[dname]),
                  "prediction_file":str(pred_path.relative_to(ROOT)).replace("\\\\","/")})
                print(f"[PASS] {dname}/{mname}: F1={metrics[-1]['f1_promotion']:.4f}")
            except Exception as exc:
                errors.append(f"{dname}/{mname}: {type(exc).__name__}: {exc}");print(f"[BLOCKED] {errors[-1]}",file=sys.stderr)
    if metrics:pd.DataFrame(metrics).to_csv(OUT/"domain_shift_metrics.csv",index=False,encoding="utf-8",lineterminator="\n")
    complete=len(metrics)==len(datasets)*len(args.models) and not errors
    (OUT/"run_status.json").write_text(json.dumps({"requested_datasets":ds_names,"requested_models":args.models,
      "completed_metric_rows":len(metrics),"expected_metric_rows":len(ds_names)*len(args.models),
      "status":"COMPLETE" if complete else "INCOMPLETE","errors_or_blockers":errors,
      "guardrail":"Secondary inference only; do not train or tune on DS3/DS5."},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 0 if complete else 1

if __name__=="__main__": raise SystemExit(main())
