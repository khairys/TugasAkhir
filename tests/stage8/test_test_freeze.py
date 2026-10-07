"""Tests for Stage 8: Normal Test Freeze Integrity.

Validates that:
- data/processed/test_normal_v1.csv exists and has 4,116 rows.
- Schema contains required fields: source_record_id, text_original, canonical_label, source_dataset, leakage_group_id.
- Exact 1-to-1 match with data/splits/v1/test_v1.csv.
"""

from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_frozen_test_normal_matches_test_partition():
    test_normal_path = REPO_ROOT / "data" / "processed" / "test_normal_v1.csv"
    test_v1_path = REPO_ROOT / "data" / "splits" / "v1" / "test_v1.csv"
    
    assert test_normal_path.exists(), f"Frozen test missing: {test_normal_path}"
    assert test_v1_path.exists(), f"Test split missing: {test_v1_path}"
    
    normal_df = pd.read_csv(test_normal_path, low_memory=False)
    split_df = pd.read_csv(test_v1_path, low_memory=False)
    
    assert len(normal_df) == 4116
    assert len(split_df) == 4116
    
    req_cols = ["source_record_id", "text_original", "canonical_label", "source_dataset", "leakage_group_id"]
    for c in req_cols:
        assert c in normal_df.columns, f"Required column missing from frozen test: {c}"
        
    assert (normal_df["source_record_id"] == split_df["record_id"]).all()
    assert (normal_df["canonical_label"] == split_df["canonical_label"]).all()
    assert (normal_df["source_dataset"] == split_df["source_dataset"]).all()
    assert (normal_df["leakage_group_id"] == split_df["leakage_group_id"]).all()
    
    # Original text byte-for-byte match
    orig_norm = normal_df["text_original"].fillna("").astype(str)
    orig_split = split_df["text_raw"].fillna("").astype(str)
    assert (orig_norm == orig_split).all(), "text_original does not match text_raw exactly!"
