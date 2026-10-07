"""Tests for Stage 8: Leakage Group Isolation.

Validates that:
- leakage_group_id never crosses train, validation, or test partitions.
- Every duplicate / near-duplicate family is completely isolated within exactly one partition.
"""

from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def splits_data():
    splits_dir = REPO_ROOT / "data" / "splits" / "v1"
    train_df = pd.read_csv(splits_dir / "train_v1.csv", low_memory=False)
    val_df = pd.read_csv(splits_dir / "validation_v1.csv", low_memory=False)
    test_df = pd.read_csv(splits_dir / "test_v1.csv", low_memory=False)
    return train_df, val_df, test_df


def test_leakage_group_id_disjointness(splits_data):
    train_df, val_df, test_df = splits_data
    train_lg = set(train_df["leakage_group_id"])
    val_lg = set(val_df["leakage_group_id"])
    test_lg = set(test_df["leakage_group_id"])
    
    assert train_lg.isdisjoint(val_lg), "Leakage groups between Train and Val must be disjoint"
    assert train_lg.isdisjoint(test_lg), "Leakage groups between Train and Test must be disjoint"
    assert val_lg.isdisjoint(test_lg), "Leakage groups between Val and Test must be disjoint"
    
    total_unique_groups = len(train_lg) + len(val_lg) + len(test_lg)
    assert total_unique_groups == 40091, f"Expected 40,091 total unique leakage groups, got {total_unique_groups}"


def test_exact_duplicate_group_disjointness(splits_data):
    train_df, val_df, test_df = splits_data
    train_edg = set(train_df["exact_duplicate_group"].dropna())
    val_edg = set(val_df["exact_duplicate_group"].dropna())
    test_edg = set(test_df["exact_duplicate_group"].dropna())
    
    assert train_edg.isdisjoint(val_edg), "Exact duplicate groups between Train and Val must be disjoint"
    assert train_edg.isdisjoint(test_edg), "Exact duplicate groups between Train and Test must be disjoint"
    assert val_edg.isdisjoint(test_edg), "Exact duplicate groups between Val and Test must be disjoint"
