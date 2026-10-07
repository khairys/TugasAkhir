"""Tests for Stage 8: Canonical Label Preservation.

Validates that:
- For every condition, canonical_label is 100% strictly identical to frozen normal test.
- No perturbation changes or inverts the classification label.
"""

from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CONDITIONS = [
    "O1_MILD", "O1_STRONG",
    "O2_MILD", "O2_STRONG",
    "O3_MILD", "O3_STRONG",
    "O4_MILD", "O4_STRONG"
]


@pytest.fixture(scope="module")
def normal_test():
    path = REPO_ROOT / "data" / "processed" / "test_normal_v1.csv"
    assert path.exists()
    return pd.read_csv(path, low_memory=False)


@pytest.mark.parametrize("condition", CONDITIONS)
def test_canonical_label_strictly_preserved(normal_test, condition):
    cond_path = REPO_ROOT / "data" / "processed" / "obfuscated_test_v1" / f"{condition}.csv"
    assert cond_path.exists(), f"Condition file missing: {cond_path}"
    
    cond_df = pd.read_csv(cond_path, low_memory=False)
    assert (cond_df["canonical_label"] == normal_test["canonical_label"]).all(), (
        f"Label mismatch detected in {condition}!"
    )
    assert set(cond_df["canonical_label"].unique()) == {0, 1}
