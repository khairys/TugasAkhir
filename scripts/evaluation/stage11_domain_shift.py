#!/usr/bin/env python3
"""Inference-only Stage 11 evaluation for isolated DS3 OOD and DS5 external sets."""
from __future__ import annotations
import argparse, hashlib, json, runpy, sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
CFG = ROOT / "configs/evaluation/stage10_robustness.json"
MANIFEST = ROOT / "data/processed/stage11/manifest_v1.json"
OUT = ROOT / "reports/stage11/domain_shift"
DATASETS = {
    "ds3_ood": ROOT / "data/processed/stage11/ds3_ood_v1.csv",
    "ds5_external": ROOT / "data/processed/stage11/ds5_external_v1.csv",
}
DISPLAY = {"linear_svm": "Linear SVM", "char_cnn": "Char-CNN", "indobert": "IndoBERT"}
ALL_DATASETS = ("ds3_ood", "ds5_external")
ALL_MODELS = ("linear_svm", "char_cnn", "indobert")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_dataset(key: str, path: Path, manifest: dict) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8")
    required = {"record_id", "text_raw", "canonical_label"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: required columns missing")
    if df["record_id"].duplicated().any() or df["record_id"].isna().any():
        raise ValueError(f"{path}: record IDs must be present and unique")
    df["canonical_label"] = pd.to_numeric(df["canonical_label"], errors="raise").astype(int)
    if not set(df["canonical_label"].unique()).issubset({0, 1}):
        raise ValueError(f"{path}: labels are not binary")
    if df["text_raw"].isna().any() or not df["text_raw"].map(lambda x: isinstance(x, str)).all():
        raise ValueError(f"{path}: text_raw must contain strings; inference must not silently normalize missing text")
    mkey = "ds3_ood_v1" if key == "ds3_ood" else "ds5_external_v1"
    expected = manifest.get("datasets", {}).get(mkey, {})
    if not expected:
        raise ValueError(f"Manifest entry {mkey} is missing")
    actual_hash = sha256(path)
    if expected.get("sha256") and actual_hash != expected["sha256"]:
        raise ValueError(f"{path}: SHA-256 mismatch; expected {expected['sha256']}, got {actual_hash}")
    if expected.get("rows") is not None and int(expected["rows"]) != len(df):
        raise ValueError(f"{path}: row count mismatch")
    for label, field in [(1, "promotion"), (0, "non_promotion")]:
        if expected.get(field) is not None and int(expected[field]) != int((df.canonical_label == label).sum()):
            raise ValueError(f"{path}: {field} count mismatch")
    return df


def load_models(cfg: dict, requested: list[str], device: str):
    helper = runpy.run_path(str(ROOT / "scripts/22_run_stage10_robustness.py"))
    actual_device = device
    if device == "auto":
        try:
            import torch
            actual_device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            actual_device = "cpu"
    loaded, errors = {}, []
    for name in requested:
        try:
            if name == "linear_svm":
                obj = helper["load_svm_pipeline"](str(ROOT / cfg["models"][name]["model_path"]))
                loaded[name] = lambda texts, obj=obj: helper["predict_svm"](obj, texts)
            elif name == "char_cnn":
                model_cfg = cfg["models"][name]
                obj = helper["CharCNNModule"](
                    str(ROOT / model_cfg["model_weights_path"]),
                    str(ROOT / model_cfg["vocab_path"]), device=actual_device
                )
                loaded[name] = lambda texts, obj=obj: obj.predict(texts)
            else:
                model_cfg = cfg["models"][name]
                obj = helper["IndoBERTModule"](
                    str(ROOT / model_cfg["model_dir"]), device=actual_device
                )
                loaded[name] = lambda texts, obj=obj: obj.predict(texts)
            print(f"[PASS] Loaded {DISPLAY[name]}")
        except Exception as exc:
            message = f"{name}: {type(exc).__name__}: {exc}"
            errors.append(message)
            print(f"[BLOCKED] {message}", file=sys.stderr)
    return loaded, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=["ds3_ood", "ds5_external", "both"], default="both")
    parser.add_argument("--models", nargs="+", choices=list(DISPLAY), default=list(DISPLAY))
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    args = parser.parse_args()
    if not CFG.exists() or not MANIFEST.exists():
        raise SystemExit("Stage 10 config or Stage 11 manifest missing")
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    dataset_names = list(ALL_DATASETS) if args.dataset == "both" else [args.dataset]
    datasets, errors = {}, []
    for key in dataset_names:
        try:
            path = DATASETS[key]
            if not path.exists():
                raise FileNotFoundError(path)
            datasets[key] = load_dataset(key, path, manifest)
            print(f"[PASS] {key}: {len(datasets[key]):,} rows")
        except Exception as exc:
            message = f"{key}: {type(exc).__name__}: {exc}"
            errors.append(message)
            print(f"[BLOCKED] {message}", file=sys.stderr)
    models, model_errors = load_models(cfg, args.models, args.device) if datasets else ({}, [])
    errors.extend(model_errors)
    OUT.mkdir(parents=True, exist_ok=True)
    new_metrics = []
    for dataset_name, df in datasets.items():
        y = df.canonical_label.to_numpy(dtype=int)
        texts = df.text_raw.tolist()  # preserve raw text byte-for-byte at the Python string level
        for model_name, predict in models.items():
            try:
                pred, score = predict(texts)
                pred = np.asarray(pred, dtype=int)
                score = np.asarray(score, dtype=float)
                if len(pred) != len(df) or len(score) != len(df) or not np.isin(pred, [0, 1]).all():
                    raise ValueError("Output length or predicted labels invalid")
                tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
                pred_path = OUT / f"{dataset_name}_{model_name}_predictions.csv"
                pd.DataFrame({
                    "record_id": df.record_id.astype(str),
                    "canonical_label": y,
                    "predicted_label": pred,
                    "model_score": score,
                    "is_correct": pred == y,
                }).to_csv(pred_path, index=False, encoding="utf-8", lineterminator="\n")
                new_metrics.append({
                    "dataset": dataset_name, "model": model_name,
                    "model_display_name": DISPLAY[model_name], "n": len(df),
                    "n_non_promotion": int((y == 0).sum()), "n_promotion": int((y == 1).sum()),
                    "f1_promotion": f1_score(y, pred, pos_label=1, zero_division=0),
                    "precision_promotion": precision_score(y, pred, pos_label=1, zero_division=0),
                    "recall_promotion": recall_score(y, pred, pos_label=1, zero_division=0),
                    "accuracy": accuracy_score(y, pred), "macro_f1": f1_score(y, pred, average="macro", zero_division=0),
                    "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
                    "candidate_sha256": sha256(DATASETS[dataset_name]),
                    "prediction_file": str(pred_path.relative_to(ROOT)).replace("\\", "/"),
                })
                print(f"[PASS] {dataset_name}/{model_name}: F1={new_metrics[-1]['f1_promotion']:.4f}")
            except Exception as exc:
                message = f"{dataset_name}/{model_name}: {type(exc).__name__}: {exc}"
                errors.append(message)
                print(f"[BLOCKED] {message}", file=sys.stderr)

    metrics_path = OUT / "domain_shift_metrics.csv"
    existing = pd.read_csv(metrics_path, encoding="utf-8") if metrics_path.exists() else pd.DataFrame()

    # Validate the current bytes of BOTH frozen candidates before claiming the overall
    # Stage 11 domain stage is complete, even when this invocation evaluates only one.
    dataset_hashes, dataset_hash_valid = {}, {}
    for key in ALL_DATASETS:
        path = DATASETS[key]
        mkey = "ds3_ood_v1" if key == "ds3_ood" else "ds5_external_v1"
        expected = manifest.get("datasets", {}).get(mkey, {}).get("sha256")
        if path.is_file():
            actual = sha256(path)
            dataset_hashes[key] = actual
            dataset_hash_valid[key] = bool(expected and actual == expected)
        else:
            dataset_hashes[key] = None
            dataset_hash_valid[key] = False

    if not existing.empty:
        # A prior model result stays eligible only while its candidate dataset still
        # matches the frozen manifest. Stale results are removed from the aggregate.
        for key in ALL_DATASETS:
            if not dataset_hash_valid[key]:
                existing = existing.loc[existing["dataset"] != key]
            else:
                existing = existing.loc[~((existing["dataset"] == key) &
                                          (existing["candidate_sha256"] != dataset_hashes[key]))]
    combined_parts = [frame for frame in [existing, pd.DataFrame(new_metrics)] if not frame.empty]
    if combined_parts:
        combined = pd.concat(combined_parts, ignore_index=True)
        combined = combined.drop_duplicates(subset=["dataset", "model"], keep="last")
        combined = combined.sort_values(["dataset", "model"]).reset_index(drop=True)
        combined.to_csv(metrics_path, index=False, encoding="utf-8", lineterminator="\n")
    else:
        combined = pd.DataFrame()

    completed_keys = set()
    if not combined.empty:
        completed_keys = set(zip(combined["dataset"].astype(str), combined["model"].astype(str)))
    full_expected = {(d, m) for d in ALL_DATASETS for m in ALL_MODELS}
    current_expected = {(d, m) for d in dataset_names for m in args.models}
    current_done = set((m["dataset"], m["model"]) for m in new_metrics)
    command_complete = current_expected.issubset(current_done) and not errors
    overall_complete = full_expected.issubset(completed_keys) and all(dataset_hash_valid.values())
    status = {
        "requested_datasets": dataset_names,
        "requested_models": args.models,
        "current_run_metric_rows": len(new_metrics),
        "current_run_expected_metric_rows": len(current_expected),
        "completed_metric_rows_total": len(completed_keys),
        "expected_metric_rows_total": len(full_expected),
        "command_status": "SUCCESS" if command_complete else "INCOMPLETE",
        "overall_stage11_domain_status": "COMPLETE" if overall_complete else "PARTIAL",
        "frozen_dataset_hash_validation": dataset_hash_valid,
        "errors_or_blockers": errors,
        "guardrail": "Secondary inference only; do not train or tune on DS3/DS5.",
    }
    (OUT / "run_status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0 if command_complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
