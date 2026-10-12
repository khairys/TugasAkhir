"""
tests/stage10/test_pairing.py - Verify 1-to-1 pairing invariants between normal test
and all 8 obfuscation conditions.
"""

import os
import pytest
import pandas as pd

NORMAL_PATH = "data/processed/test_normal_v1.csv"
OBF_DIR = "data/processed/obfuscated_test_v1"
CONDITIONS = [
    "O1_MILD", "O1_STRONG",
    "O2_MILD", "O2_STRONG",
    "O3_MILD", "O3_STRONG",
    "O4_MILD", "O4_STRONG"
]


@pytest.fixture(scope="module")
def normal_df():
    return pd.read_csv(NORMAL_PATH)


@pytest.mark.parametrize("cond", CONDITIONS)
def test_pairing_alignment_and_labels(cond, normal_df):
    cpath = os.path.join(OBF_DIR, f"{cond}.csv")
    df_c = pd.read_csv(cpath)

    # 1. Row counts & unique IDs
    assert len(df_c) == len(normal_df) == 4116
    assert df_c["source_record_id"].nunique() == 4116

    # 2. Perfect set equality of IDs
    assert set(df_c["source_record_id"]) == set(normal_df["source_record_id"])

    # 3. Align by source_record_id
    df_norm_idx = normal_df.set_index("source_record_id")
    df_c_idx = df_c.set_index("source_record_id")

    # 4. Check labels identical
    assert (df_c_idx["canonical_label"] == df_norm_idx["canonical_label"]).all()

    # 5. Check text_original identical
    assert (df_c_idx["text_original"] == df_norm_idx["text_original"]).all()

    # 6. Check changed flag invariant
    is_changed = (df_c_idx["text_obfuscated"] != df_c_idx["text_original"])
    assert (df_c_idx["changed"] == is_changed).all()
