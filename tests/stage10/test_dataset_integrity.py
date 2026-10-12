"""
tests/stage10/test_dataset_integrity.py - Verify SHA-256 hashes and data contracts
for all Stage 10 test datasets.
"""

import os
import hashlib
import json
import pytest
import pandas as pd


def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


EXPECTED_HASHES = {
    "normal": ("data/processed/test_normal_v1.csv", "6d5a2c8b386193147013fb7a6002e4fa0375969f00d46a0cc86eea674e8c3780"),
    "O1_MILD": ("data/processed/obfuscated_test_v1/O1_MILD.csv", "a455e6224a37c826cefe3c19a7aa1966feb11fa93eca266ae14479a8fea1fb6e"),
    "O1_STRONG": ("data/processed/obfuscated_test_v1/O1_STRONG.csv", "79dff505fe3d121dbe187cce2e41bdcc228b959767e7e9b2556c76ed83a8dd98"),
    "O2_MILD": ("data/processed/obfuscated_test_v1/O2_MILD.csv", "5357596408b1d5fc3354a53fee1fd957808bd517e4055966d2c4ab59d3886584"),
    "O2_STRONG": ("data/processed/obfuscated_test_v1/O2_STRONG.csv", "b6eb5c853777094f850a9b1ac112ea19f9e71a27d5a66e58c6444dcf07456174"),
    "O3_MILD": ("data/processed/obfuscated_test_v1/O3_MILD.csv", "75b70109d5c33308f48146e5ad5e21e693086d8c004c724705737e8aa16386cc"),
    "O3_STRONG": ("data/processed/obfuscated_test_v1/O3_STRONG.csv", "6a0016fb564e65ac0443ac28232f9bc5012eaade2a6d76863a8e00cbd1191764"),
    "O4_MILD": ("data/processed/obfuscated_test_v1/O4_MILD.csv", "89e5402a5050252ca555c49266cd92f2cffa1f0e027b0e2d8ccec326139e264c"),
    "O4_STRONG": ("data/processed/obfuscated_test_v1/O4_STRONG.csv", "466c428ef5f1515823ccfaf53c4911c599d1f6dc36ee7a596a67685ac84a1607")
}


@pytest.mark.parametrize("cond_name,info", list(EXPECTED_HASHES.items()))
def test_dataset_sha256_hashes(cond_name, info):
    path, exp_hash = info
    assert os.path.exists(path), f"File missing: {path}"
    act_hash = sha256_file(path)
    assert act_hash == exp_hash, f"Hash mismatch for {cond_name}: expected {exp_hash}, got {act_hash}"


@pytest.mark.parametrize("cond_name,info", list(EXPECTED_HASHES.items()))
def test_dataset_row_counts_and_columns(cond_name, info):
    path, _ = info
    df = pd.read_csv(path)
    assert len(df) == 4116, f"Expected 4116 rows in {cond_name}, got {len(df)}"
    assert "source_record_id" in df.columns
    assert "canonical_label" in df.columns
    assert df["source_record_id"].nunique() == 4116
    assert set(df["canonical_label"].unique()) == {0, 1}
