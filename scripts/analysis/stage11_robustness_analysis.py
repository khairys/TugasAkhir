#!/usr/bin/env python3
"""Stage 11 analysis from the frozen Stage 10 per-record prediction outputs.

This script does not retrain models and does not run inference. It pairs records by
source_record_id, restricts robustness estimates to changed == True, computes a
stratified paired bootstrap CI for each F1 drop, summarizes effects by obfuscation
family/severity, and creates an unreviewed error-analysis queue.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parents[2]
PRED_ROOT = ROOT / "reports" / "stage10" / "predictions"
ERRORS_PATH = ROOT / "reports" / "stage10" / "paired_error_analysis.csv"
OUT = ROOT / "reports" / "stage11" / "primary"

MODEL_DIRS = {
    "linear_svm": "svm",
    "char_cnn": "char_cnn",
    "indobert": "indobert",
}
MODEL_NAMES = {
    "linear_svm": "Linear SVM",
    "char_cnn": "Char-CNN",
    "indobert": "IndoBERT",
}
CONDITIONS = {
    "O1_MILD": ("O1", "MILD"),
    "O1_STRONG": ("O1", "STRONG"),
    "O2_MILD": ("O2", "MILD"),
    "O2_STRONG": ("O2", "STRONG"),
    "O3_MILD": ("O3", "MILD"),
    "O3_STRONG": ("O3", "STRONG"),
    "O4_MILD": ("O4", "MILD"),
    "O4_STRONG": ("O4", "STRONG"),
}
FAMILY_NAMES = {
    "O1": "Character substitution",
    "O2": "Insertion/deletion (spelling)",
    "O3": "Whitespace manipulation",
    "O4": "Unicode/orthographic manipulation",
}
POSITIVE_LABEL = 1


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def as_bool(value: Any) -> bool:
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def bool_series(series: pd.Series) -> pd.Series:
    return series.map(as_bool)


def load_predictions(path: Path, require_changed: bool = False) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required saved predictions are missing: {path}")
    df = pd.read_csv(path, encoding="utf-8")
    required = {"source_record_id", "canonical_label", "predicted_label"}
    if require_changed:
        required.add("changed")
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing required columns: {missing}")
    if df["source_record_id"].isna().any() or df["source_record_id"].duplicated().any():
        raise ValueError(f"{path}: record IDs must be present and unique")
    df["canonical_label"] = pd.to_numeric(df["canonical_label"], errors="raise").astype(int)
    df["predicted_label"] = pd.to_numeric(df["predicted_label"], errors="raise").astype(int)
    if not set(df["canonical_label"].unique()).issubset({0, 1}):
        raise ValueError(f"{path}: canonical labels must be binary 0/1")
    if not set(df["predicted_label"].unique()).issubset({0, 1}):
        raise ValueError(f"{path}: predictions must be binary 0/1")
    df["source_record_id"] = df["source_record_id"].astype(str)
    if require_changed:
        df["changed_bool"] = bool_series(df["changed"])
    return df


def classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, Any]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "f1_promotion": float(f1_score(y_true, y_pred, pos_label=POSITIVE_LABEL, zero_division=0)),
        "precision_promotion": float(precision_score(y_true, y_pred, pos_label=POSITIVE_LABEL, zero_division=0)),
        "recall_promotion": float(recall_score(y_true, y_pred, pos_label=POSITIVE_LABEL, zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
    }


def paired_bootstrap_f1_drop(
    y_true: np.ndarray,
    pred_normal: np.ndarray,
    pred_obfuscated: np.ndarray,
    n_resamples: int = 10_000,
    seed: int = 42,
    chunk_size: int = 128,
) -> dict[str, float]:
    """Percentile CI of F1(normal paired IDs) - F1(obfuscated paired IDs).

    The resampling unit is a record pair. Sampling is stratified by the observed
    gold label so each bootstrap replicate retains the paired subset's class counts.
    Predictions for normal/obfuscated text are always resampled at the same indices.
    """
    y_true = np.asarray(y_true, dtype=np.int8)
    pred_normal = np.asarray(pred_normal, dtype=np.int8)
    pred_obfuscated = np.asarray(pred_obfuscated, dtype=np.int8)
    if not (len(y_true) == len(pred_normal) == len(pred_obfuscated)):
        raise ValueError("Paired bootstrap arrays must have equal lengths")
    if n_resamples < 1:
        raise ValueError("n_resamples must be >= 1")
    idx_negative = np.flatnonzero(y_true == 0)
    idx_positive = np.flatnonzero(y_true == 1)
    if not len(idx_negative) or not len(idx_positive):
        raise ValueError("Stratified paired bootstrap requires both labels in the paired subset")

    rng = np.random.default_rng(seed)
    drops = np.empty(n_resamples, dtype=float)

    def f1_from_counts(tp: np.ndarray, fp: np.ndarray, fn: np.ndarray) -> np.ndarray:
        denominator = 2 * tp + fp + fn
        return np.divide(2 * tp, denominator, out=np.zeros_like(tp, dtype=float), where=denominator > 0)

    for start in range(0, n_resamples, chunk_size):
        stop = min(start + chunk_size, n_resamples)
        reps = stop - start
        sample_negative = rng.choice(idx_negative, size=(reps, len(idx_negative)), replace=True)
        sample_positive = rng.choice(idx_positive, size=(reps, len(idx_positive)), replace=True)

        # Actual label is known by stratum: predictions on negatives count as FP;
        # predictions on positives count as TP or FN. Resample paired predictions.
        normal_fp = np.count_nonzero(pred_normal[sample_negative] == 1, axis=1)
        normal_tp = np.count_nonzero(pred_normal[sample_positive] == 1, axis=1)
        normal_fn = len(idx_positive) - normal_tp
        obf_fp = np.count_nonzero(pred_obfuscated[sample_negative] == 1, axis=1)
        obf_tp = np.count_nonzero(pred_obfuscated[sample_positive] == 1, axis=1)
        obf_fn = len(idx_positive) - obf_tp

        f1_normal = f1_from_counts(normal_tp, normal_fp, normal_fn)
        f1_obfuscated = f1_from_counts(obf_tp, obf_fp, obf_fn)
        drops[start:stop] = f1_normal - f1_obfuscated

    return {
        "bootstrap_f1_drop_mean": float(np.mean(drops)),
        "bootstrap_f1_drop_std": float(np.std(drops, ddof=0)),
        "ci_95_lower": float(np.percentile(drops, 2.5)),
        "ci_95_upper": float(np.percentile(drops, 97.5)),
    }


def build_error_review_queue(max_per_stratum: int, seed: int) -> pd.DataFrame:
    if not ERRORS_PATH.exists():
        raise FileNotFoundError(f"Error-analysis input is missing: {ERRORS_PATH}")
    errors = pd.read_csv(ERRORS_PATH, encoding="utf-8")
    required = {
        "source_record_id", "model", "condition", "family", "severity",
        "canonical_label", "pred_normal", "pred_obfuscated",
        "is_evasion", "is_new_fp", "text_original", "text_obfuscated",
    }
    missing = sorted(required - set(errors.columns))
    if missing:
        raise ValueError(f"{ERRORS_PATH}: missing required columns: {missing}")
    errors["is_evasion_bool"] = bool_series(errors["is_evasion"])
    errors["is_new_fp_bool"] = bool_series(errors["is_new_fp"])
    family_hints = {
        "O1": "Character substitution",
        "O2": "Spelling / insertion-deletion",
        "O3": "Whitespace manipulation",
        "O4": "Unicode / orthographic manipulation",
    }
    selected: list[dict[str, Any]] = []
    grouping = ["model", "family", "severity"]
    for keys, group in errors.groupby(grouping, sort=True, dropna=False):
        model, family, severity = keys
        for error_type, flag in (
            ("EVASION_FALSE_NEGATIVE", "is_evasion_bool"),
            ("NEW_FALSE_POSITIVE", "is_new_fp_bool"),
        ):
            candidates = group[group[flag]].copy()
            if candidates.empty:
                continue
            stratum_seed = seed + sum(ord(char) for char in f"{model}|{family}|{severity}|{error_type}")
            chosen = candidates.sort_values("source_record_id").sample(
                n=min(max_per_stratum, len(candidates)), random_state=stratum_seed
            )
            for row in chosen.to_dict(orient="records"):
                selected.append({
                    "source_record_id": row["source_record_id"],
                    "model": model,
                    "condition": row["condition"],
                    "family": family,
                    "severity": severity,
                    "error_transition": error_type,
                    "canonical_label": row["canonical_label"],
                    "pred_normal": row["pred_normal"],
                    "pred_obfuscated": row["pred_obfuscated"],
                    "obfuscation_family_hint": family_hints.get(str(family), "Needs review"),
                    "text_original": row["text_original"],
                    "text_obfuscated": row["text_obfuscated"],
                    "human_semantic_category": "",
                    "representation_failure_hypothesis": "",
                    "reviewer_notes": "",
                    "review_status": "UNREVIEWED",
                })
    columns = [
        "source_record_id", "model", "condition", "family", "severity",
        "error_transition", "canonical_label", "pred_normal", "pred_obfuscated",
        "obfuscation_family_hint", "text_original", "text_obfuscated",
        "human_semantic_category", "representation_failure_hypothesis",
        "reviewer_notes", "review_status",
    ]
    return pd.DataFrame(selected, columns=columns)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8", lineterminator="\n")


def run(n_resamples: int, seed: int, max_error_samples: int) -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    absolute_rows: list[dict[str, Any]] = []
    condition_rows: list[dict[str, Any]] = []
    input_hashes: dict[str, str] = {}
    model_normal: dict[str, pd.DataFrame] = {}

    for model, folder in MODEL_DIRS.items():
        normal_path = PRED_ROOT / folder / "test_normal_predictions.csv"
        normal = load_predictions(normal_path)
        model_normal[model] = normal
        input_hashes[str(normal_path.relative_to(ROOT)).replace("\\", "/")] = sha256_file(normal_path)
        y = normal["canonical_label"].to_numpy(dtype=int)
        p = normal["predicted_label"].to_numpy(dtype=int)
        absolute_rows.append({
            "model": model,
            "model_display_name": MODEL_NAMES[model],
            "n_test": int(len(normal)),
            "n_non_promotion": int((y == 0).sum()),
            "n_promotion": int((y == 1).sum()),
            **classification_metrics(y, p),
        })

    for model, folder in MODEL_DIRS.items():
        normal = model_normal[model][["source_record_id", "canonical_label", "predicted_label"]].rename(
            columns={"canonical_label": "label_normal", "predicted_label": "pred_normal"}
        )
        for condition, (family, severity) in CONDITIONS.items():
            obf_path = PRED_ROOT / folder / f"{condition}_predictions.csv"
            obf = load_predictions(obf_path, require_changed=True)
            input_hashes[str(obf_path.relative_to(ROOT)).replace("\\", "/")] = sha256_file(obf_path)
            if obf["source_record_id"].duplicated().any():
                raise ValueError(f"{obf_path}: duplicate IDs prevent pair alignment")
            changed = obf.loc[obf["changed_bool"]].copy()
            if changed.empty:
                raise ValueError(f"{condition}/{model}: no successfully changed pairs")
            changed = changed.merge(
                normal, on="source_record_id", how="left", validate="one_to_one", indicator=True
            )
            if (changed["_merge"] != "both").any():
                raise ValueError(f"{condition}/{model}: changed IDs do not all exist in normal predictions")
            if (changed["canonical_label"] != changed["label_normal"]).any():
                raise ValueError(f"{condition}/{model}: labels changed across a paired record")
            y_pair = changed["canonical_label"].to_numpy(dtype=int)
            p_normal = changed["pred_normal"].to_numpy(dtype=int)
            p_obf = changed["predicted_label"].to_numpy(dtype=int)
            normal_metrics = classification_metrics(y_pair, p_normal)
            obf_metrics = classification_metrics(y_pair, p_obf)
            f1_drop = normal_metrics["f1_promotion"] - obf_metrics["f1_promotion"]
            bootstrap = paired_bootstrap_f1_drop(
                y_pair, p_normal, p_obf, n_resamples=n_resamples, seed=seed
            )
            base_f1 = normal_metrics["f1_promotion"]
            condition_rows.append({
                "model": model,
                "model_display_name": MODEL_NAMES[model],
                "condition": condition,
                "family": family,
                "family_name": FAMILY_NAMES[family],
                "severity": severity,
                "n_test_records": int(len(obf)),
                "n_changed_pairs": int(len(changed)),
                "transformation_rate_pct": float(100 * len(changed) / len(obf)),
                "f1_normal_paired": base_f1,
                "f1_obfuscated_paired": obf_metrics["f1_promotion"],
                "f1_drop": float(f1_drop),
                "relative_drop_pct": float(100 * f1_drop / base_f1) if base_f1 else float("nan"),
                "f1_retention_pct": float(100 * obf_metrics["f1_promotion"] / base_f1) if base_f1 else float("nan"),
                "precision_normal_paired": normal_metrics["precision_promotion"],
                "precision_obfuscated_paired": obf_metrics["precision_promotion"],
                "recall_normal_paired": normal_metrics["recall_promotion"],
                "recall_obfuscated_paired": obf_metrics["recall_promotion"],
                "accuracy_normal_paired": normal_metrics["accuracy"],
                "accuracy_obfuscated_paired": obf_metrics["accuracy"],
                "FP_normal": normal_metrics["FP"],
                "FN_normal": normal_metrics["FN"],
                "FP_obfuscated": obf_metrics["FP"],
                "FN_obfuscated": obf_metrics["FN"],
                **bootstrap,
                "ci_excludes_zero": bool(bootstrap["ci_95_lower"] > 0 or bootstrap["ci_95_upper"] < 0),
            })

    absolute = pd.DataFrame(absolute_rows)
    conditions = pd.DataFrame(condition_rows)
    model_order = list(MODEL_DIRS)
    conditions["model_order"] = conditions["model"].map({name: i for i, name in enumerate(model_order)})
    conditions["condition_order"] = conditions["condition"].map({name: i for i, name in enumerate(CONDITIONS)})
    conditions = conditions.sort_values(["model_order", "condition_order"]).drop(
        columns=["model_order", "condition_order"]
    )

    summary_rows = []
    for model in model_order:
        subset = conditions[conditions["model"] == model]
        worst = subset.loc[subset["f1_drop"].idxmax()]
        summary_rows.append({
            "model": model,
            "model_display_name": MODEL_NAMES[model],
            "conditions_averaged": int(len(subset)),
            "mean_f1_normal_paired": float(subset["f1_normal_paired"].mean()),
            "mean_f1_obfuscated_paired": float(subset["f1_obfuscated_paired"].mean()),
            "mean_absolute_f1_drop": float(subset["f1_drop"].mean()),
            "mean_relative_drop_pct": float(subset["relative_drop_pct"].mean()),
            "mean_f1_retention_pct": float(subset["f1_retention_pct"].mean()),
            "worst_condition_by_f1_drop": str(worst["condition"]),
            "worst_condition_f1_drop": float(worst["f1_drop"]),
        })
    robustness_summary = pd.DataFrame(summary_rows)

    matrix_rows = []
    for model in model_order:
        row: dict[str, Any] = {"model": model, "model_display_name": MODEL_NAMES[model]}
        subset = conditions[conditions["model"] == model]
        for family in ["O1", "O2", "O3", "O4"]:
            family_data = subset[subset["family"] == family]
            row[FAMILY_NAMES[family]] = float(family_data["f1_drop"].mean())
        matrix_rows.append(row)
    family_matrix = pd.DataFrame(matrix_rows)

    severity_rows = []
    for model in model_order:
        for family in ["O1", "O2", "O3", "O4"]:
            sub = conditions[(conditions["model"] == model) & (conditions["family"] == family)]
            mild = float(sub.loc[sub["severity"] == "MILD", "f1_drop"].iloc[0])
            strong = float(sub.loc[sub["severity"] == "STRONG", "f1_drop"].iloc[0])
            delta = strong - mild
            if delta > 1e-12:
                pattern = "Higher F1 drop under STRONG"
            elif delta < -1e-12:
                pattern = "Lower F1 drop under STRONG; non-monotonic"
            else:
                pattern = "Nearly unchanged"
            severity_rows.append({
                "model": model, "model_display_name": MODEL_NAMES[model],
                "family": family, "family_name": FAMILY_NAMES[family],
                "mild_f1_drop": mild, "strong_f1_drop": strong,
                "strong_minus_mild_drop": float(delta), "severity_pattern": pattern,
            })
    severity = pd.DataFrame(severity_rows)

    error_queue = build_error_review_queue(max_error_samples, seed)
    write_csv(absolute, OUT / "absolute_performance.csv")
    write_csv(conditions, OUT / "condition_level_metrics.csv")
    write_csv(robustness_summary, OUT / "robustness_summary.csv")
    write_csv(family_matrix, OUT / "obfuscation_family_matrix.csv")
    write_csv(severity, OUT / "severity_analysis.csv")
    write_csv(conditions[[
        "model", "condition", "family", "severity", "n_changed_pairs",
        "f1_drop", "bootstrap_f1_drop_mean", "bootstrap_f1_drop_std",
        "ci_95_lower", "ci_95_upper", "ci_excludes_zero",
    ]], OUT / "bootstrap_intervals.csv")
    write_csv(error_queue, OUT / "error_review_candidates.csv")
    input_hashes[str(ERRORS_PATH.relative_to(ROOT)).replace("\\", "/")] = sha256_file(ERRORS_PATH)
    manifest = {
        "stage": "stage11_primary_robustness_analysis",
        "status": "GENERATED_FROM_SAVED_STAGE10_PREDICTIONS",
        "models": model_order,
        "conditions": list(CONDITIONS),
        "primary_metric": "Promotion F1",
        "absolute_performance_definition": "Promotion F1 over all saved normal-test predictions",
        "robustness_definition": "F1(normal paired subset) - F1(obfuscated paired subset), using only changed == True rows aligned by source_record_id",
        "bootstrap": {
            "method": "stratified paired bootstrap percentile interval",
            "resamples": n_resamples,
            "confidence_level": 0.95,
            "seed": seed,
            "resampling_unit": "paired record IDs",
            "stratification": "gold label within changed == True paired subset",
        },
        "error_review": {
            "max_examples_per_model_family_severity_transition": max_error_samples,
            "semantic_categories_require_manual_review": True,
            "initial_status": "UNREVIEWED",
        },
        "input_sha256": input_hashes,
        "outputs": [
            "absolute_performance.csv", "condition_level_metrics.csv",
            "robustness_summary.csv", "obfuscation_family_matrix.csv",
            "severity_analysis.csv", "bootstrap_intervals.csv",
            "error_review_candidates.csv",
        ],
        "scope_note": "This script analyzes saved Stage 10 predictions only. It does not include DS3 OOD or DS5 external-source inference.",
    }
    (OUT / "analysis_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "out_dir": str(OUT.relative_to(ROOT)),
        "absolute_rows": len(absolute),
        "condition_rows": len(conditions),
        "error_review_candidates": len(error_queue),
        "bootstrap_resamples_per_model_condition": n_resamples,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap-resamples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-error-samples", type=int, default=3,
                        help="Samples per model × family × severity × transition stratum")
    args = parser.parse_args()
    if args.max_error_samples < 1:
        parser.error("--max-error-samples must be >= 1")
    result = run(args.bootstrap_resamples, args.seed, args.max_error_samples)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
