"""Stage 8: Phase 15 - Create Deterministic Experimental Split.

Implements:
- StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)
- Groups: leakage_group_id
- Stratification: canonical_label
- Partition assignments:
  - Fold 0 -> TEST (~10%)
  - Fold 1 -> VALIDATION (~10%)
  - Folds 2-9 -> TRAIN (~80%)

Outputs:
- data/splits/v1/train_v1.csv
- data/splits/v1/validation_v1.csv
- data/splits/v1/test_v1.csv
- data/splits/v1/split_manifest_v1.json
- data/splits/v1/split_statistics_v1.csv
"""

from __future__ import annotations

import hashlib
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import sklearn
from sklearn.model_selection import StratifiedGroupKFold

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

Path(REPO_ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO_ROOT / "logs" / "15_create_experimental_split.log", mode="w", encoding="utf-8")
    ]
)


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def get_git_commit_sha() -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        logging.warning(f"Could not retrieve git commit SHA: {e}")
        return "UNKNOWN"


def main():
    logging.info("Starting Phase 15: Create Experimental Split (Stage 8)...")
    
    main_pool_path = REPO_ROOT / "data" / "processed" / "main_pool_candidate_v2.csv"
    assert main_pool_path.exists(), f"Main pool missing: {main_pool_path}"
    
    main_pool_sha = compute_sha256(main_pool_path)
    logging.info(f"Source Main Pool SHA-256: {main_pool_sha}")
    
    df = pd.read_csv(main_pool_path)
    logging.info(f"Loaded Main Pool: {len(df):,} records")
    assert len(df) == 41152, f"Expected 41,152 records, got {len(df):,}"
    
    # Required columns check
    req_cols = [
        "record_id", "source_dataset", "source_row_id", "text_raw",
        "canonical_label", "leakage_group_id", "exact_duplicate_group",
        "normalized_variant_group", "near_duplicate_group", "author", "timestamp"
    ]
    for c in req_cols:
        assert c in df.columns, f"Required column missing: {c}"
        
    assert df["canonical_label"].isin([0, 1]).all(), "Invalid canonical labels found!"
    assert df["record_id"].nunique() == len(df), "record_id is not globally unique!"
    assert df["leakage_group_id"].notna().all(), "Null leakage_group_id found!"
    
    # StratifiedGroupKFold
    seed = 42
    n_splits = 10
    logging.info(f"Running StratifiedGroupKFold (n_splits={n_splits}, shuffle=True, random_state={seed})...")
    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    
    fold_assignments = {}
    for fold_idx, (train_idx, val_test_idx) in enumerate(
        sgkf.split(X=df["text_raw"], y=df["canonical_label"], groups=df["leakage_group_id"])
    ):
        fold_assignments[fold_idx] = val_test_idx
        
    test_indices = fold_assignments[0]
    val_indices = fold_assignments[1]
    train_indices = []
    for f in range(2, 10):
        train_indices.extend(fold_assignments[f])
        
    train_df = df.iloc[train_indices].copy().reset_index(drop=True)
    val_df = df.iloc[val_indices].copy().reset_index(drop=True)
    test_df = df.iloc[test_indices].copy().reset_index(drop=True)
    
    # Hard asserts on row counts and partitions
    assert len(train_df) + len(val_df) + len(test_df) == 41152
    
    train_ids = set(train_df["record_id"])
    val_ids = set(val_df["record_id"])
    test_ids = set(test_df["record_id"])
    assert train_ids.isdisjoint(val_ids)
    assert train_ids.isdisjoint(test_ids)
    assert val_ids.isdisjoint(test_ids)
    
    train_lg = set(train_df["leakage_group_id"])
    val_lg = set(val_df["leakage_group_id"])
    test_lg = set(test_df["leakage_group_id"])
    assert train_lg.isdisjoint(val_lg), "Leakage group overlap between TRAIN and VAL!"
    assert train_lg.isdisjoint(test_lg), "Leakage group overlap between TRAIN and TEST!"
    assert val_lg.isdisjoint(test_lg), "Leakage group overlap between VAL and TEST!"
    
    logging.info(f"TRAIN: {len(train_df):,} rows (Groups: {len(train_lg):,})")
    logging.info(f"VALIDATION: {len(val_df):,} rows (Groups: {len(val_lg):,})")
    logging.info(f"TEST: {len(test_df):,} rows (Groups: {len(test_lg):,})")
    
    # Save splits to data/splits/v1/
    out_dir = REPO_ROOT / "data" / "splits" / "v1"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    train_path = out_dir / "train_v1.csv"
    val_path = out_dir / "validation_v1.csv"
    test_path = out_dir / "test_v1.csv"
    
    train_df.to_csv(train_path, index=False, encoding="utf-8")
    val_df.to_csv(val_path, index=False, encoding="utf-8")
    test_df.to_csv(test_path, index=False, encoding="utf-8")
    logging.info(f"Saved split files to {out_dir}")
    
    # Compute SHA256 of outputs
    train_sha = compute_sha256(train_path)
    val_sha = compute_sha256(val_path)
    test_sha = compute_sha256(test_path)
    
    # Build statistics table
    stats = []
    for split_name, s_df in [("train", train_df), ("validation", val_df), ("test", test_df)]:
        n_total = len(s_df)
        n_prom = int((s_df["canonical_label"] == 1).sum())
        n_non_prom = int((s_df["canonical_label"] == 0).sum())
        prom_pct = round(n_prom / n_total * 100, 4)
        n_groups = s_df["leakage_group_id"].nunique()
        split_pct = round(n_total / 41152 * 100, 4)
        stats.append({
            "split": split_name,
            "total_records": n_total,
            "percentage_of_pool": split_pct,
            "promotion_count": n_prom,
            "non_promotion_count": n_non_prom,
            "promotion_percentage": prom_pct,
            "unique_leakage_groups": n_groups
        })
    stats_df = pd.DataFrame(stats)
    stats_path = out_dir / "split_statistics_v1.csv"
    stats_df.to_csv(stats_path, index=False, encoding="utf-8")
    logging.info(f"Saved split statistics to {stats_path}")
    
    # Build split manifest
    manifest = {
        "split_version": "v1",
        "dataset_version": "canonical_dataset_v2",
        "main_pool_version": "main_pool_candidate_v2",
        "seed": seed,
        "method": "StratifiedGroupKFold",
        "n_splits": n_splits,
        "fold_assignment": {
            "train": [2, 3, 4, 5, 6, 7, 8, 9],
            "validation": [1],
            "test": [0]
        },
        "group_column": "leakage_group_id",
        "stratification_column": "canonical_label",
        "git_commit_sha": get_git_commit_sha(),
        "generation_timestamp": datetime.now().isoformat(),
        "environment": {
            "python_version": sys.version.split()[0],
            "scikit_learn_version": sklearn.__version__,
            "pandas_version": pd.__version__
        },
        "hashes_sha256": {
            "source_main_pool": main_pool_sha,
            "train_v1": train_sha,
            "validation_v1": val_sha,
            "test_v1": test_sha
        },
        "partitions": {
            "train": {
                "rows": len(train_df),
                "promotion_count": int((train_df["canonical_label"] == 1).sum()),
                "non_promotion_count": int((train_df["canonical_label"] == 0).sum()),
                "unique_groups": len(train_lg)
            },
            "validation": {
                "rows": len(val_df),
                "promotion_count": int((val_df["canonical_label"] == 1).sum()),
                "non_promotion_count": int((val_df["canonical_label"] == 0).sum()),
                "unique_groups": len(val_lg)
            },
            "test": {
                "rows": len(test_df),
                "promotion_count": int((test_df["canonical_label"] == 1).sum()),
                "non_promotion_count": int((test_df["canonical_label"] == 0).sum()),
                "unique_groups": len(test_lg)
            }
        }
    }
    
    manifest_path = out_dir / "split_manifest_v1.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    logging.info(f"Saved split manifest to {manifest_path}")
    print("Phase 15 completed successfully. Split v1 generated.")


if __name__ == "__main__":
    main()
