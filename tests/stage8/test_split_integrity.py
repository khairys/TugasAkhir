"""Tests for Stage 8: Split Integrity.

Validates that:
- Total records across train, validation, and test equal 41,152
- All record_ids are globally unique and disjoint
- Promotion and Non-Promotion classes exist in all 3 partitions
- No unapproved source datasets enter the split
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


def test_total_split_row_counts(splits_data):
    train_df, val_df, test_df = splits_data
    total = len(train_df) + len(val_df) + len(test_df)
    assert total == 41152, f"Total split rows must be 41,152, got {total}"
    assert len(train_df) == 32920
    assert len(val_df) == 4116
    assert len(test_df) == 4116


def test_record_id_disjointness(splits_data):
    train_df, val_df, test_df = splits_data
    train_ids = set(train_df["record_id"])
    val_ids = set(val_df["record_id"])
    test_ids = set(test_df["record_id"])
    
    assert train_ids.isdisjoint(val_ids), "Train and Val record_ids must be disjoint"
    assert train_ids.isdisjoint(test_ids), "Train and Test record_ids must be disjoint"
    assert val_ids.isdisjoint(test_ids), "Val and Test record_ids must be disjoint"
    assert len(train_ids | val_ids | test_ids) == 41152


def test_label_representation_in_all_partitions(splits_data):
    train_df, val_df, test_df = splits_data
    for name, df in [("train", train_df), ("val", val_df), ("test", test_df)]:
        prom_count = (df["canonical_label"] == 1).sum()
        non_prom_count = (df["canonical_label"] == 0).sum()
        assert prom_count > 0, f"Promotion count in {name} must be > 0"
        assert non_prom_count > 0, f"Non-promotion count in {name} must be > 0"
        assert set(df["canonical_label"].unique()) == {0, 1}


def test_source_dataset_composition(splits_data):
    train_df, val_df, test_df = splits_data
    allowed_sources = {"DS1_fahruu", "DS2_kyyyy8_all", "DS4_kyyyy8_platform"}
    all_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    actual_sources = set(all_df["source_dataset"].unique())
    assert actual_sources == allowed_sources, f"Splits contain unexpected sources: {actual_sources}"
