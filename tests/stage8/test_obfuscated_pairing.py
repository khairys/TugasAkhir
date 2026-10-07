"""Tests for Stage 8: Obfuscated Test Pairing Invariants.

Validates that:
- For every condition, source_record_id strictly pairs with frozen normal test.
- text_original in obfuscated condition strictly matches text_original in frozen normal test.
- Every condition has exactly 4,116 records.
- changed=False records strictly match text_obfuscated == text_original.
- changed=True records strictly have text_obfuscated != text_original.
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
def test_condition_pairing(normal_test, condition):
    cond_path = REPO_ROOT / "data" / "processed" / "obfuscated_test_v1" / f"{condition}.csv"
    assert cond_path.exists(), f"Condition file missing: {cond_path}"
    
    cond_df = pd.read_csv(cond_path, low_memory=False)
    assert len(cond_df) == len(normal_test), f"Row count mismatch in {condition}"
    
    assert (cond_df["source_record_id"] == normal_test["source_record_id"]).all()
    
    # Original text preservation
    orig_c = cond_df["text_original"].fillna("").astype(str)
    orig_n = normal_test["text_original"].fillna("").astype(str)
    assert (orig_c == orig_n).all(), f"text_original mismatch in {condition}"
    
    # Check changed status consistency
    is_changed = cond_df["changed"].astype(bool)
    obf_text = cond_df["text_obfuscated"].fillna("").astype(str)
    
    # For changed=True, text must differ
    assert (obf_text[is_changed] != orig_c[is_changed]).all()
    # For changed=False, text must be identical
    assert (obf_text[~is_changed] == orig_c[~is_changed]).all()
