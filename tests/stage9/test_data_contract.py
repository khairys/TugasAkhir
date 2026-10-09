"""Unit tests for Stage 9: Data contract verification for Train and Validation splits."""

from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def train_df():
    path = REPO_ROOT / "data" / "splits" / "v1" / "train_v1.csv"
    assert path.exists(), f"Train dataset missing: {path}"
    return pd.read_csv(path, low_memory=False)


@pytest.fixture(scope="module")
def val_df():
    path = REPO_ROOT / "data" / "splits" / "v1" / "validation_v1.csv"
    assert path.exists(), f"Validation dataset missing: {path}"
    return pd.read_csv(path, low_memory=False)


def test_train_data_contract(train_df):
    assert len(train_df) == 32920, f"Expected 32,920 train rows, got {len(train_df)}"
    assert train_df["record_id"].nunique() == len(train_df)
    assert train_df["text_raw"].isna().sum() == 0
    assert train_df["canonical_label"].isna().sum() == 0
    assert set(train_df["canonical_label"].unique()) == {0, 1}

    p_count = (train_df["canonical_label"] == 1).sum()
    np_count = (train_df["canonical_label"] == 0).sum()
    assert p_count == 3960, f"Expected 3,960 train promotions, got {p_count}"
    assert np_count == 28960, f"Expected 28,960 train non-promotions, got {np_count}"


def test_val_data_contract(val_df):
    assert len(val_df) == 4116, f"Expected 4,116 val rows, got {len(val_df)}"
    assert val_df["record_id"].nunique() == len(val_df)
    assert val_df["text_raw"].isna().sum() == 0
    assert val_df["canonical_label"].isna().sum() == 0
    assert set(val_df["canonical_label"].unique()) == {0, 1}

    p_count = (val_df["canonical_label"] == 1).sum()
    np_count = (val_df["canonical_label"] == 0).sum()
    assert p_count == 495, f"Expected 495 val promotions, got {p_count}"
    assert np_count == 3621, f"Expected 3,621 val non-promotions, got {np_count}"
