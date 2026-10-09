"""Stage 9: Train and Evaluate Linear SVM Baseline (v1).

Trains Linear SVM + TF-IDF pipeline on train_v1.csv (normal text).
Evaluates candidate configurations on validation_v1.csv.
Selects best configuration based on validation F1 Promotion.
Saves model pipeline, tuning results, validation metrics, predictions, and manifest.

Supports:
  --mode smoke     : Quick smoke test on small stratified subset (<= 2000 train, <= 500 val)
  --mode official  : Full training on all 32,920 train records, evaluation on all 4,116 val records
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

Path(REPO_ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO_ROOT / "logs" / "19_train_svm.log", mode="a", encoding="utf-8")
    ]
)


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def get_git_info() -> Tuple[str, bool]:
    try:
        sha_res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True
        )
        commit_sha = sha_res.stdout.strip()
    except Exception:
        commit_sha = "UNKNOWN"

    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True
        )
        is_clean = len(status_res.stdout.strip()) == 0
    except Exception:
        is_clean = False

    return commit_sha, is_clean


def validate_split_dataframe(df: pd.DataFrame, name: str, expected_len: int | None = None) -> None:
    req_cols = ["record_id", "text_raw", "canonical_label"]
    for col in req_cols:
        assert col in df.columns, f"Missing required column '{col}' in {name} dataset!"

    if expected_len is not None:
        assert len(df) == expected_len, f"Expected {expected_len:,} rows in {name}, found {len(df):,}"

    assert df["record_id"].nunique() == len(df), f"Duplicate record_id found in {name}!"
    assert df["text_raw"].isna().sum() == 0, f"Null text_raw values found in {name}!"
    assert df["canonical_label"].isna().sum() == 0, f"Null canonical_label values found in {name}!"
    assert set(df["canonical_label"].unique()).issubset({0, 1}), f"Invalid canonical labels in {name}!"

    p_count = (df["canonical_label"] == 1).sum()
    np_count = (df["canonical_label"] == 0).sum()
    assert p_count > 0, f"Zero Promotion records in {name}!"
    assert np_count > 0, f"Zero Non-Promotion records in {name}!"

    logging.info(f"[{name} Validated] Rows: {len(df):,} | Promotion: {p_count:,} | Non-Promotion: {np_count:,}")


def build_pipeline(ngram_range: Tuple[int, int], C: float, seed: int = 42) -> Pipeline:
    vectorizer = TfidfVectorizer(
        analyzer="word",
        lowercase=True,
        ngram_range=ngram_range,
        min_df=1
    )
    classifier = LinearSVC(
        C=C,
        class_weight="balanced",
        random_state=seed,
        max_iter=5000
    )
    return Pipeline([
        ("tfidf", vectorizer),
        ("svm", classifier)
    ])


def evaluate_pipeline(
    pipeline: Pipeline,
    X_val: List[str],
    y_val: List[int]
) -> Dict[str, Any]:
    t0 = time.time()
    y_pred = pipeline.predict(X_val)
    decision_scores = pipeline.decision_function(X_val)
    eval_time = time.time() - t0

    cm = confusion_matrix(y_val, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    metrics = {
        "f1_promotion": float(round(f1_score(y_val, y_pred, pos_label=1), 6)),
        "precision_promotion": float(round(precision_score(y_val, y_pred, pos_label=1), 6)),
        "recall_promotion": float(round(recall_score(y_val, y_pred, pos_label=1), 6)),
        "accuracy": float(round(accuracy_score(y_val, y_pred), 6)),
        "macro_f1": float(round(f1_score(y_val, y_pred, average="macro"), 6)),
        "confusion_matrix": {
            "TN": int(tn),
            "FP": int(fp),
            "FN": int(fn),
            "TP": int(tp)
        },
        "eval_duration_sec": float(round(eval_time, 4)),
        "y_pred": y_pred,
        "decision_scores": decision_scores
    }
    return metrics


def is_candidate_better(candidate: Dict[str, Any], current_best: Dict[str, Any]) -> bool:
    # 1. Primary: F1 Promotion
    diff_f1 = candidate["f1_promotion"] - current_best["f1_promotion"]
    if abs(diff_f1) > 1e-5:
        return diff_f1 > 0

    # 2. Tie-breaker 1: Precision Promotion (higher precision avoids false alarms on innocent users)
    diff_prec = candidate["precision_promotion"] - current_best["precision_promotion"]
    if abs(diff_prec) > 1e-5:
        return diff_prec > 0

    # 3. Tie-breaker 2: Recall Promotion
    diff_rec = candidate["recall_promotion"] - current_best["recall_promotion"]
    if abs(diff_rec) > 1e-5:
        return diff_rec > 0

    # 4. Tie-breaker 3: Macro-F1
    diff_macro = candidate["macro_f1"] - current_best["macro_f1"]
    if abs(diff_macro) > 1e-5:
        return diff_macro > 0

    # 5. Tie-breaker 4: Simpler model (unigram over bigram)
    cand_is_unigram = (list(candidate["ngram_range"]) == [1, 1])
    best_is_unigram = (list(current_best["ngram_range"]) == [1, 1])
    if cand_is_unigram != best_is_unigram:
        return cand_is_unigram  # prefer unigram

    # 6. Tie-breaker 5: Smaller regularization parameter C
    return candidate["C"] < current_best["C"]


def main():
    parser = argparse.ArgumentParser(description="Train and evaluate Linear SVM baseline for Stage 9.")
    parser.add_argument(
        "--mode",
        choices=["smoke", "official"],
        required=True,
        help="Execution mode: 'smoke' for quick verification, 'official' for complete experiment run."
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/stage9/svm_v1.json",
        help="Path to configuration JSON."
    )
    args = parser.parse_args()

    mode = args.mode
    logging.info(f"=== Starting Stage 9 Linear SVM v1 in [{mode.upper()}] mode ===")

    config_path = REPO_ROOT / args.config
    assert config_path.exists(), f"Configuration file not found: {config_path}"

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    seed = int(config.get("seed", 42))
    train_path = REPO_ROOT / config["data"]["train_path"]
    val_path = REPO_ROOT / config["data"]["validation_path"]

    assert train_path.exists(), f"Train dataset missing: {train_path}"
    assert val_path.exists(), f"Validation dataset missing: {val_path}"

    train_sha_pre = compute_sha256(train_path)
    val_sha_pre = compute_sha256(val_path)
    logging.info(f"Pre-run Train SHA-256: {train_sha_pre}")
    logging.info(f"Pre-run Validation SHA-256: {val_sha_pre}")

    train_df_full = pd.read_csv(train_path, low_memory=False)
    val_df_full = pd.read_csv(val_path, low_memory=False)

    validate_split_dataframe(train_df_full, "Train Full", expected_len=32920)
    validate_split_dataframe(val_df_full, "Validation Full", expected_len=4116)

    # Output directory setup
    if mode == "smoke":
        out_artifacts_dir = REPO_ROOT / "artifacts" / "stage9" / "svm_v1_smoke"
        out_reports_dir = REPO_ROOT / "reports" / "stage9" / "svm_v1_smoke"
        train_sample_size = 2000
        val_sample_size = 500

        logging.info(f"Sampling smoke subsets (Train={train_sample_size}, Val={val_sample_size}) with seed={seed}...")
        # Stratified sampling for train
        sss_train = StratifiedShuffleSplit(n_splits=1, train_size=train_sample_size, random_state=seed)
        train_idx, _ = next(sss_train.split(train_df_full, train_df_full["canonical_label"]))
        train_df = train_df_full.iloc[train_idx].copy().reset_index(drop=True)

        # Stratified sampling for val
        sss_val = StratifiedShuffleSplit(n_splits=1, train_size=val_sample_size, random_state=seed)
        val_idx, _ = next(sss_val.split(val_df_full, val_df_full["canonical_label"]))
        val_df = val_df_full.iloc[val_idx].copy().reset_index(drop=True)

        validate_split_dataframe(train_df, "Train Smoke", expected_len=train_sample_size)
        validate_split_dataframe(val_df, "Validation Smoke", expected_len=val_sample_size)
    else:
        out_artifacts_dir = REPO_ROOT / "artifacts" / "stage9" / "svm_v1"
        out_reports_dir = REPO_ROOT / "reports" / "stage9" / "svm_v1"
        train_df = train_df_full
        val_df = val_df_full

    out_artifacts_dir.mkdir(parents=True, exist_ok=True)
    out_reports_dir.mkdir(parents=True, exist_ok=True)

    X_train = train_df["text_raw"].astype(str).tolist()
    y_train = train_df["canonical_label"].astype(int).tolist()
    X_val = val_df["text_raw"].astype(str).tolist()
    y_val = val_df["canonical_label"].astype(int).tolist()

    candidate_grid = config["candidate_grid"]
    tuning_results: List[Dict[str, Any]] = []
    fitted_pipelines: Dict[str, Pipeline] = {}
    eval_predictions_cache: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}

    logging.info(f"Evaluating {len(candidate_grid)} candidate configurations...")

    for cand in candidate_grid:
        cfg_id = cand["config_id"]
        ngram_range = tuple(cand["ngram_range"])
        C = float(cand["C"])

        logging.info(f"--- Training {cfg_id}: ngram_range={ngram_range}, C={C} ---")
        pipeline = build_pipeline(ngram_range=ngram_range, C=C, seed=seed)

        t_train_start = time.time()
        pipeline.fit(X_train, y_train)
        train_dur = time.time() - t_train_start

        vocab_size = len(pipeline.named_steps["tfidf"].vocabulary_)
        logging.info(f"[{cfg_id}] Trained in {train_dur:.2f}s | Vocabulary size: {vocab_size:,}")

        eval_res = evaluate_pipeline(pipeline, X_val, y_val)
        y_pred = eval_res.pop("y_pred")
        dec_scores = eval_res.pop("decision_scores")

        eval_predictions_cache[cfg_id] = (y_pred, dec_scores)
        fitted_pipelines[cfg_id] = pipeline

        res_record = {
            "config_id": cfg_id,
            "ngram_range": list(ngram_range),
            "C": C,
            "vocab_size": vocab_size,
            "train_duration_sec": round(train_dur, 4),
            "eval_duration_sec": eval_res["eval_duration_sec"],
            "total_duration_sec": round(train_dur + eval_res["eval_duration_sec"], 4),
            "f1_promotion": eval_res["f1_promotion"],
            "precision_promotion": eval_res["precision_promotion"],
            "recall_promotion": eval_res["recall_promotion"],
            "accuracy": eval_res["accuracy"],
            "macro_f1": eval_res["macro_f1"],
            "confusion_matrix": eval_res["confusion_matrix"]
        }
        tuning_results.append(res_record)

        logging.info(
            f"[{cfg_id}] Val F1 (Prom): {eval_res['f1_promotion']:.4f} | "
            f"Prec: {eval_res['precision_promotion']:.4f} | "
            f"Rec: {eval_res['recall_promotion']:.4f} | "
            f"Acc: {eval_res['accuracy']:.4f} | "
            f"Macro-F1: {eval_res['macro_f1']:.4f}"
        )

    # Select best candidate
    best_candidate = tuning_results[0]
    for cand in tuning_results[1:]:
        if is_candidate_better(cand, best_candidate):
            best_candidate = cand

    best_cfg_id = best_candidate["config_id"]
    best_pipeline = fitted_pipelines[best_cfg_id]
    best_preds, best_scores = eval_predictions_cache[best_cfg_id]

    logging.info(f"=== Selected Best Configuration: {best_cfg_id} ===")
    logging.info(
        f"Validation F1 Promotion: {best_candidate['f1_promotion']:.4f} | "
        f"Precision: {best_candidate['precision_promotion']:.4f} | "
        f"Recall: {best_candidate['recall_promotion']:.4f}"
    )

    # 1. Save pipeline
    model_save_path = out_artifacts_dir / "linear_svm_pipeline.joblib"
    joblib.dump(best_pipeline, model_save_path)
    logging.info(f"Saved trained pipeline to: {model_save_path}")

    # 2. Verification of serialization & reloading
    reloaded_pipeline = joblib.load(model_save_path)
    reloaded_preds = reloaded_pipeline.predict(X_val)
    assert np.array_equal(best_preds, reloaded_preds), "Reloaded model predictions mismatch!"
    logging.info("[Reload Integrity Confirmed] Reloaded model predictions 100% match original.")

    # 3. Save tuning results CSV
    tuning_df = pd.DataFrame([
        {
            "config_id": r["config_id"],
            "ngram_range": str(tuple(r["ngram_range"])),
            "C": r["C"],
            "vocab_size": r["vocab_size"],
            "f1_promotion": r["f1_promotion"],
            "precision_promotion": r["precision_promotion"],
            "recall_promotion": r["recall_promotion"],
            "accuracy": r["accuracy"],
            "macro_f1": r["macro_f1"],
            "TN": r["confusion_matrix"]["TN"],
            "FP": r["confusion_matrix"]["FP"],
            "FN": r["confusion_matrix"]["FN"],
            "TP": r["confusion_matrix"]["TP"],
            "train_duration_sec": r["train_duration_sec"],
            "eval_duration_sec": r["eval_duration_sec"],
            "is_selected": (r["config_id"] == best_cfg_id)
        }
        for r in tuning_results
    ])
    tuning_csv_path = out_reports_dir / "tuning_results.csv"
    tuning_df.to_csv(tuning_csv_path, index=False, encoding="utf-8")
    logging.info(f"Saved tuning results to: {tuning_csv_path}")

    # 4. Save validation predictions CSV
    predictions_df = pd.DataFrame({
        "record_id": val_df["record_id"],
        "actual_label": y_val,
        "predicted_label": best_preds,
        "decision_function": np.round(best_scores, 6),
        "is_correct": (np.array(y_val) == best_preds)
    })
    preds_csv_path = out_reports_dir / "validation_predictions.csv"
    predictions_df.to_csv(preds_csv_path, index=False, encoding="utf-8")
    logging.info(f"Saved validation predictions to: {preds_csv_path}")

    # 5. Save validation metrics JSON
    metrics_json_path = out_reports_dir / "validation_metrics.json"
    with open(metrics_json_path, "w", encoding="utf-8") as f:
        json.dump(best_candidate, f, indent=2)
    logging.info(f"Saved validation metrics to: {metrics_json_path}")

    # 6. Verify train & val hash integrity
    train_sha_post = compute_sha256(train_path)
    val_sha_post = compute_sha256(val_path)
    assert train_sha_pre == train_sha_post, "FATAL: train_v1.csv modified during run!"
    assert val_sha_pre == val_sha_post, "FATAL: validation_v1.csv modified during run!"
    logging.info("[Data Immutability Confirmed] Train and Validation SHA-256 strictly unchanged.")

    # 7. Save Run Manifest
    commit_sha, is_clean = get_git_info()
    script_sha = compute_sha256(Path(__file__).resolve())
    config_sha = compute_sha256(config_path)
    model_sha = compute_sha256(model_save_path)

    run_manifest = {
        "experiment_name": config["experiment_name"],
        "stage": config["stage"],
        "mode": mode,
        "run_timestamp": datetime.now().isoformat(),
        "git": {
            "commit_sha": commit_sha,
            "working_tree_clean": is_clean
        },
        "environment": {
            "python_version": sys.version.split()[0],
            "scikit_learn_version": sklearn.__version__,
            "joblib_version": joblib.__version__,
            "pandas_version": pd.__version__,
            "numpy_version": np.__version__
        },
        "hashes_sha256": {
            "train_data": train_sha_post,
            "validation_data": val_sha_post,
            "config_file": config_sha,
            "training_script": script_sha,
            "saved_model": model_sha
        },
        "data_split_counts": {
            "train_records": len(train_df),
            "validation_records": len(val_df),
            "train_promotion_count": int((train_df["canonical_label"] == 1).sum()),
            "val_promotion_count": int((val_df["canonical_label"] == 1).sum())
        },
        "seed": seed,
        "selected_configuration": best_candidate,
        "all_candidate_results": tuning_results,
        "status": "SUCCESS"
    }

    manifest_json_path = out_reports_dir / "run_manifest.json"
    with open(manifest_json_path, "w", encoding="utf-8") as f:
        json.dump(run_manifest, f, indent=2)
    logging.info(f"Saved run manifest to: {manifest_json_path}")

    print(f"\nStage 9 Linear SVM [{mode.upper()}] run completed successfully!")
    print(f"Selected configuration: {best_cfg_id} (ngram={best_candidate['ngram_range']}, C={best_candidate['C']})")
    print(f"Validation F1 Promotion: {best_candidate['f1_promotion']:.4f}")
    print(f"Model saved to: {model_save_path}")


if __name__ == "__main__":
    main()
