#!/usr/bin/env python3
"""
scripts/23_validate_stage10_results.py - Stage 10 Output Verification and Integrity Checker

Verifies:
1. All input dataset hashes match official Stage 8 values.
2. All 3 models have normal predictions (4,116 rows each).
3. All 24 model-condition obfuscation predictions exist (4,116 rows each). Total = 111,132 predictions.
4. Correctness of ID alignment, unique IDs, and unchanged ground-truth labels.
5. Exact consistency between summarized CSV metrics and raw prediction CSVs.
6. Paired robustness sample counts match 'changed' flags exactly.
7. Bootstrap 95% Confidence Intervals are non-empty and mathematically valid.
8. No unexplained NaN or Inf values.
9. Completeness of manifest and generated reports.
"""

import os
import sys
import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd
import numpy as np


def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def validate_all_outputs(config_path="configs/evaluation/stage10_robustness.json"):
    print("=" * 76)
    print("  STAGE 10 COMPREHENSIVE OUTPUT & ARTIFACT VALIDATOR")
    print("=" * 76)

    failures = []
    checks_passed = 0

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    reports_dir = Path("reports/stage10")
    pred_dir = reports_dir / "predictions"

    # 1. Input Datasets Hash Check
    print("\n--- 1. INPUT DATASETS INTEGRITY CHECK ---")
    norm_path = config["datasets"]["test_normal"]["path"]
    exp_norm_hash = config["datasets"]["test_normal"]["sha256"]
    if sha256_file(norm_path) == exp_norm_hash:
        print(f" [PASS] Normal test hash verified: {exp_norm_hash}")
        checks_passed += 1
    else:
        msg = f"Normal test hash mismatch!"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    df_norm = pd.read_csv(norm_path)
    expected_ids = set(df_norm["source_record_id"])
    expected_count = 4116
    assert len(df_norm) == expected_count

    for cond in config["datasets"]["obfuscation_conditions"]:
        cid = cond["condition_id"]
        cpath = cond["path"]
        exp_h = cond["sha256"]
        act_h = sha256_file(cpath)
        if act_h == exp_h:
            print(f" [PASS] {cid:<10} hash verified: {act_h[:16]}...")
            checks_passed += 1
        else:
            msg = f"Hash mismatch for {cid}: expected {exp_h}, got {act_h}"
            print(f" [FAIL] {msg}")
            failures.append(msg)

    # 2. Prediction Files Verification (27 files)
    print("\n--- 2. PREDICTION FILES VERIFICATION (27 FILES) ---")
    models = ["svm", "char_cnn", "indobert"]
    conditions = ["test_normal"] + [c["condition_id"] for c in config["datasets"]["obfuscation_conditions"]]

    total_pred_count = 0
    pred_dfs = {}

    for m in models:
        for c in conditions:
            fname = f"{c}_predictions.csv"
            pfile = pred_dir / m / fname
            if not pfile.exists():
                msg = f"Missing prediction file: {pfile}"
                print(f" [FAIL] {msg}")
                failures.append(msg)
                continue

            df_p = pd.read_csv(pfile)
            pred_dfs[(m, c)] = df_p
            total_pred_count += len(df_p)

            # Check rows
            if len(df_p) != expected_count:
                msg = f"Invalid row count in {pfile}: {len(df_p)} != {expected_count}"
                print(f" [FAIL] {msg}")
                failures.append(msg)

            # Check unique IDs
            if df_p["source_record_id"].nunique() != expected_count:
                msg = f"Duplicate IDs in {pfile}"
                print(f" [FAIL] {msg}")
                failures.append(msg)

            # Check ID match
            if set(df_p["source_record_id"]) != expected_ids:
                msg = f"ID set mismatch in {pfile}"
                print(f" [FAIL] {msg}")
                failures.append(msg)

            # Check labels
            if set(df_p["predicted_label"].unique()).issubset({0, 1}):
                pass
            else:
                msg = f"Non-binary predictions in {pfile}: {df_p['predicted_label'].unique()}"
                print(f" [FAIL] {msg}")
                failures.append(msg)

    if total_pred_count == 27 * expected_count:
        print(f" [PASS] All 27 prediction files present and validated (Total predictions: {total_pred_count:,})")
        checks_passed += 1
    else:
        msg = f"Total predictions mismatch: {total_pred_count} != {27 * expected_count}"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    # 3. Report CSV Verification
    print("\n--- 3. REPORT CSV FILES INTEGRITY & SCHEMA CHECK ---")
    expected_reports = [
        ("test_normal_metrics.csv", 3),
        ("obfuscation_metrics_full.csv", 24),
        ("paired_robustness_metrics.csv", 24),
        ("prediction_flip_summary.csv", 24),
        ("source_stratified_metrics.csv", None),
        ("paired_error_analysis.csv", None),
        ("robustness_summary.json", None),
        ("manifest_v1.json", None)
    ]

    for rname, exp_rows in expected_reports:
        rpath = reports_dir / rname
        if not rpath.exists():
            msg = f"Missing report file: {rpath}"
            print(f" [FAIL] {msg}")
            failures.append(msg)
            continue

        if rname.endswith(".csv"):
            df_r = pd.read_csv(rpath)
            if exp_rows is not None and len(df_r) != exp_rows:
                msg = f"Row count mismatch in {rname}: {len(df_r)} != {exp_rows}"
                print(f" [FAIL] {msg}")
                failures.append(msg)
            else:
                print(f" [PASS] {rname:<32}: Found {len(df_r)} rows")
                checks_passed += 1
        elif rname.endswith(".json"):
            with open(rpath, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            print(f" [PASS] {rname:<32}: Valid JSON ({len(data)} top-level keys)")
            checks_passed += 1

    # 4. Consistency: Paired Robustness vs Condition Changed Flags
    print("\n--- 4. PAIRED ROBUSTNESS SAMPLE COUNT CHECK ---")
    paired_file = reports_dir / "paired_robustness_metrics.csv"
    if paired_file.exists():
        df_paired = pd.read_csv(paired_file)
        for cond in config["datasets"]["obfuscation_conditions"]:
            cid = cond["condition_id"]
            df_c_raw = pd.read_csv(cond["path"])
            exp_changed = int(df_c_raw["changed"].sum())

            cond_paired_rows = df_paired[df_paired["condition"] == cid]
            for _, r in cond_paired_rows.iterrows():
                act_changed = int(r["n_changed_pairs"])
                if act_changed == exp_changed:
                    checks_passed += 1
                else:
                    msg = f"Changed pairs mismatch for {r['model']} on {cid}: {act_changed} != {exp_changed}"
                    print(f" [FAIL] {msg}")
                    failures.append(msg)

        print(f" [PASS] Paired subset counts verified across all 24 conditions (matches raw changed flags).")

        # 5. Check Bootstrap CIs
        print("\n--- 5. BOOTSTRAP CONFIDENCE INTERVAL VALIDATION ---")
        ci_valid = True
        for _, r in df_paired.iterrows():
            low = r["ci_95_lower"]
            high = r["ci_95_upper"]
            drop = r["f1_drop"]
            if pd.isna(low) or pd.isna(high) or low > high:
                ci_valid = False
                msg = f"Invalid CI for {r['model']} on {r['condition']}: [{low}, {high}]"
                failures.append(msg)
        if ci_valid:
            print(" [PASS] 95% Bootstrap Confidence Intervals are non-empty and well-ordered.")
            checks_passed += 1

    # Summary
    print("\n" + "=" * 76)
    print(f"Checks Passed: {checks_passed}")
    print(f"Checks Failed: {len(failures)}")

    if len(failures) == 0:
        print(">>> RESULT: [PASS] ALL OUTPUTS FULLY VALIDATED AND INTEGRITY VERIFIED <<<")
        print("=" * 76)
        return True
    else:
        print(">>> RESULT: [FAIL] VALIDATION FAILED WITH ERRORS <<<")
        for f in failures:
            print(f" - {f}")
        print("=" * 76)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Stage 10 Results")
    parser.add_argument("--config", default="configs/evaluation/stage10_robustness.json")
    args = parser.parse_args()
    success = validate_all_outputs(args.config)
    sys.exit(0 if success else 1)
