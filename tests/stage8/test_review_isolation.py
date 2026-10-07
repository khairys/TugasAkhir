"""Tests for Stage 8: Review Records Isolation.

Validates that:
- Zero records from data/review/label_review_queue_v2.csv enter train, validation, or test.
- No exact duplicate family belonging to review queue appears in any split.
"""

from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_review_records_not_in_splits():
    review_path = REPO_ROOT / "data" / "review" / "label_review_queue_v2.csv"
    assert review_path.exists(), f"Review queue missing: {review_path}"
    review_df = pd.read_csv(review_path)
    
    splits_dir = REPO_ROOT / "data" / "splits" / "v1"
    train_df = pd.read_csv(splits_dir / "train_v1.csv", low_memory=False)
    val_df = pd.read_csv(splits_dir / "validation_v1.csv", low_memory=False)
    test_df = pd.read_csv(splits_dir / "test_v1.csv", low_memory=False)
    
    review_edg = set(review_df["exact_duplicate_group"].dropna())
    review_records = set(review_df["record_id"].dropna())
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        overlap_edg = set(df["exact_duplicate_group"]).intersection(review_edg)
        overlap_rec = set(df["record_id"]).intersection(review_records)
        assert len(overlap_edg) == 0, f"Review exact_duplicate_group leaked into {name}: {overlap_edg}"
        assert len(overlap_rec) == 0, f"Review record_id leaked into {name}: {overlap_rec}"
