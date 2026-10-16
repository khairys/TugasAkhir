#!/usr/bin/env python3
"""Validate saved Stage 11 outputs without training or running fresh inference.

Legacy training-split and DS5 raw-source discrepancies are reported as warnings,
not hidden or converted into false passes. Frozen candidate and result hashes are
validated strictly.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def is_float(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def close_enough(value: Any, expected: float, tolerance: float = 1e-8) -> bool:
    return is_float(value) and abs(float(value) - expected) <= tolerance


def validate_stage11_artifacts(root: Path = ROOT) -> dict[str, Any]:
    """Return a structured summary of Stage 11 artifact integrity checks."""
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def path_for(relative: str) -> Path:
        return root / relative

    def load_csv(relative: str, expected_rows: int | None = None) -> list[dict[str, str]]:
        path = path_for(relative)
        if not path.exists():
            errors.append(f"Missing required file: {relative}")
            return []
        try:
            rows = read_csv(path)
        except Exception as exc:
            errors.append(f"Cannot parse {relative}: {type(exc).__name__}: {exc}")
            return []
        if expected_rows is not None:
            require(len(rows) == expected_rows, f"{relative}: expected {expected_rows} data rows, found {len(rows)}")
        return rows

    manifest_path = path_for("data/processed/stage11/manifest_v1.json")
    if not manifest_path.exists():
        return {"status": "FAILED", "errors": ["Missing Stage 11 manifest"], "warnings": [], "notes": []}
    try:
        manifest = read_json(manifest_path)
    except Exception as exc:
        return {"status": "FAILED", "errors": [f"Cannot parse Stage 11 manifest: {exc}"], "warnings": [], "notes": []}

    require(
        manifest.get("status") == "EVALUATED_RESULTS_AVAILABLE_WITH_DOCUMENTED_PROVENANCE_CAVEATS",
        "Stage 11 manifest status does not match the recorded evaluation outputs."
    )

    # Frozen candidate data are checked strictly; raw-source provenance is separately warned.
    for key, rel in [
        ("ds3_ood_v1", "data/processed/stage11/ds3_ood_v1.csv"),
        ("ds5_external_v1", "data/processed/stage11/ds5_external_v1.csv"),
    ]:
        entry = manifest.get("datasets", {}).get(key, {})
        path = path_for(rel)
        if not path.exists():
            errors.append(f"Missing frozen candidate dataset: {rel}")
            continue
        require(sha256_file(path) == entry.get("sha256"), f"{rel}: SHA-256 mismatch with manifest")
        rows = load_csv(rel, int(entry.get("rows", -1)))
        if rows:
            labels = [row.get("canonical_label", "") for row in rows]
            require(set(labels).issubset({"0", "1"}), f"{rel}: labels must be binary 0/1")
            require(labels.count("1") == int(entry.get("promotion", -1)), f"{rel}: Promotion count mismatch")
            require(labels.count("0") == int(entry.get("non_promotion", -1)), f"{rel}: Non-Promotion count mismatch")
            ids = [row.get("record_id", "") for row in rows]
            require(all(ids) and len(ids) == len(set(ids)), f"{rel}: record IDs missing or duplicated")

    sources = manifest.get("sources", {})
    if sources.get("ds5_raw_sha256") != sources.get("ds5_raw_sha256_official"):
        warnings.append("DS5 raw-source SHA-256 differs from the official source hash; preserve the frozen evaluated candidate and do not rebuild it yet.")
    notes.append("IndoBERT weights may be absent from Git by design; validation of saved prediction/metric artifacts does not require fresh inference.")

    expected_tables = {
        "reports/stage11/primary/absolute_performance.csv": 3,
        "reports/stage11/primary/condition_level_metrics.csv": 24,
        "reports/stage11/primary/robustness_summary.csv": 3,
        "reports/stage11/primary/obfuscation_family_matrix.csv": 3,
        "reports/stage11/primary/severity_analysis.csv": 12,
        "reports/stage11/primary/bootstrap_intervals.csv": 24,
        "reports/stage11/primary/error_review_candidates.csv": 113,
    }
    tables = {rel: load_csv(rel, count) for rel, count in expected_tables.items()}
    conditions = tables["reports/stage11/primary/condition_level_metrics.csv"]
    allowed_models = {"linear_svm", "char_cnn", "indobert"}
    allowed_conditions = {
        "O1_MILD", "O1_STRONG", "O2_MILD", "O2_STRONG",
        "O3_MILD", "O3_STRONG", "O4_MILD", "O4_STRONG"
    }
    require(
        len({(row.get("model"), row.get("condition")) for row in conditions}) == 24,
        "Condition-level table does not have 24 unique model-condition pairs."
    )
    for i, row in enumerate(conditions, start=1):
        require(row.get("model") in allowed_models, f"Condition row {i}: unknown model")
        require(row.get("condition") in allowed_conditions, f"Condition row {i}: unknown condition")
        for field in ["f1_drop", "f1_normal_paired", "f1_obfuscated_paired", "ci_95_lower", "ci_95_upper"]:
            require(is_float(row.get(field)), f"Condition row {i}: nonnumeric {field}")
        if is_float(row.get("ci_95_lower")) and is_float(row.get("ci_95_upper")):
            require(float(row["ci_95_lower"]) <= float(row["ci_95_upper"]), f"Condition row {i}: reversed bootstrap interval")
    for row in tables["reports/stage11/primary/robustness_summary.csv"]:
        try:
            require(int(float(row.get("conditions_averaged", "0"))) == 8, f"Summary for {row.get('model')}: expected 8 conditions")
        except ValueError:
            errors.append(f"Summary for {row.get('model')}: invalid conditions_averaged")
        for field in ["mean_f1_drop", "mean_f1_retention_pct", "mean_f1_normal_paired", "mean_f1_obfuscated_paired"]:
            require(is_float(row.get(field)), f"Summary for {row.get('model')}: nonnumeric {field}")

    snapshot_rel = "reports/stage11/primary/analysis_snapshot_manifest.json"
    snapshot_path = path_for(snapshot_rel)
    if not snapshot_path.exists():
        errors.append(f"Missing {snapshot_rel}")
    else:
        snapshot = read_json(snapshot_path)
        hashes = snapshot.get("input_sha256", {})
        require(bool(hashes), "Analysis snapshot contains no input SHA-256 entries")
        for rel, expected_hash in hashes.items():
            path = path_for(rel)
            if not path.exists():
                errors.append(f"Missing analysis input listed in snapshot: {rel}")
            elif sha256_file(path) != expected_hash:
                errors.append(f"Input SHA-256 mismatch: {rel}")

    review = tables["reports/stage11/primary/error_review_candidates.csv"]
    review_headers = set(review[0]) if review else set()
    require("proposed_semantic_category" in review_headers, "Error queue must use proposed_semantic_category, not imply independent human labels.")
    for i, row in enumerate(review, start=1):
        for field in ["proposed_semantic_category", "representation_failure_hypothesis", "reviewer_notes"]:
            require(bool((row.get(field) or "").strip()), f"Review row {i}: {field} is empty")
        require(row.get("review_status") == "AI_ASSISTED_REVIEWED", f"Review row {i}: incorrect review status")
        require("AI-assisted" in (row.get("reviewer_notes") or ""), f"Review row {i}: missing AI-assisted disclosure")

    metrics = load_csv("reports/stage11/domain_shift/domain_shift_metrics.csv", 6)
    require(len({(row.get("dataset"), row.get("model")) for row in metrics}) == 6,
            "Domain-shift metric file must contain six unique dataset-model pairs.")
    candidate_key = {"ds3_ood": "ds3_ood_v1", "ds5_external": "ds5_external_v1"}
    for i, row in enumerate(metrics, start=1):
        dataset, model = row.get("dataset", ""), row.get("model", "")
        require(dataset in candidate_key, f"Domain metric row {i}: unknown dataset {dataset}")
        require(model in allowed_models, f"Domain metric row {i}: unknown model {model}")
        try:
            n = int(row["n"])
            tn, fp, fn, tp = (int(row[k]) for k in ["TN", "FP", "FN", "TP"])
            require(tn + fp + fn + tp == n, f"Domain metric row {i}: confusion counts do not sum to n")
            precision = tp / (tp + fp) if tp + fp else 0.0
            recall = tp / (tp + fn) if tp + fn else 0.0
            f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
            require(close_enough(row.get("precision_promotion"), precision), f"Domain metric row {i}: precision disagrees with confusion matrix")
            require(close_enough(row.get("recall_promotion"), recall), f"Domain metric row {i}: recall disagrees with confusion matrix")
            require(close_enough(row.get("f1_promotion"), f1), f"Domain metric row {i}: F1 disagrees with confusion matrix")
            expected_candidate = manifest.get("datasets", {}).get(candidate_key.get(dataset, ""), {}).get("sha256")
            require(row.get("candidate_sha256") == expected_candidate, f"Domain metric row {i}: candidate SHA-256 mismatch")
            pred_rel = row.get("prediction_file", "")
            predictions = load_csv(pred_rel, n)
            if predictions:
                ids = [p.get("record_id", "") for p in predictions]
                require(all(ids) and len(ids) == len(set(ids)), f"{pred_rel}: IDs missing or duplicated")
                for j, prediction in enumerate(predictions, start=1):
                    gold, predicted = prediction.get("canonical_label"), prediction.get("predicted_label")
                    require(gold in {"0", "1"} and predicted in {"0", "1"}, f"{pred_rel} row {j}: non-binary label")
                    require(prediction.get("is_correct") == str(gold == predicted), f"{pred_rel} row {j}: is_correct inconsistency")
                    require(is_float(prediction.get("model_score")), f"{pred_rel} row {j}: model_score is nonnumeric")
        except (KeyError, ValueError, ZeroDivisionError) as exc:
            errors.append(f"Domain metric row {i}: invalid numeric data ({exc})")

    status_rel = "reports/stage11/domain_shift/run_status.json"
    if not path_for(status_rel).exists():
        errors.append(f"Missing {status_rel}")
    else:
        status = read_json(path_for(status_rel))
        require(status.get("overall_stage11_domain_status") == "COMPLETE", "Aggregate domain-shift status is not COMPLETE.")
        require(int(status.get("completed_metric_rows_total", 0)) == 6 and int(status.get("expected_metric_rows_total", 0)) == 6,
                "Aggregate domain-shift status does not record 6/6 combinations.")

    split_rel = "data/splits/v1/split_manifest_v1.json"
    if path_for(split_rel).exists():
        split = read_json(path_for(split_rel))
        for key, filename in [("train_v1", "train_v1.csv"), ("validation_v1", "validation_v1.csv")]:
            expected = split.get("hashes_sha256", {}).get(key)
            current = path_for(f"data/splits/v1/{filename}")
            if expected and current.exists() and sha256_file(current) != expected:
                warnings.append(f"{filename} hash differs from the official split manifest; end-to-end retraining reproducibility remains unresolved.")
    else:
        warnings.append("Split manifest is missing; end-to-end retraining reproducibility was not checked.")

    # Optional external weight bundle: absent is expected; present must match its hash.
    try:
        config = read_json(path_for("configs/evaluation/stage10_robustness.json"))
        model_cfg = config.get("models", {}).get("indobert", {})
        weight_rel = model_cfg.get("model_weights_path", "models/indobert/artifacts/final_model/model.safetensors")
        weight_path = path_for(weight_rel)
        expected_hash = model_cfg.get("model_weights_sha256")
        if weight_path.exists():
            require(bool(expected_hash) and sha256_file(weight_path) == expected_hash,
                    "IndoBERT weights exist but do not match the configured SHA-256.")
        else:
            notes.append("IndoBERT weights are intentionally external; fresh inference requires the configured SHA-256.")
    except Exception as exc:
        warnings.append(f"Could not inspect IndoBERT weight configuration: {exc}")

    return {
        "status": "PASSED" if not errors else "FAILED",
        "branch_scope": "stage11-robustness-analysis",
        "primary_table_rows": {Path(k).name: len(v) for k, v in tables.items()},
        "domain_shift_metric_rows": len(metrics),
        "review_candidates": len(review),
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "notes": notes,
        "fresh_inference_executed": False,
        "full_repository_test_suite_executed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root")
    args = parser.parse_args()
    result = validate_stage11_artifacts(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
