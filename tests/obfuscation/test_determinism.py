"""Test deterministic reproducibility of obfuscation transformations."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.obfuscation import obfuscate, FAMILIES


def test_identical_runs_produce_identical_outputs():
    text = "daftar di situs gacor sekarang dapat bonus melimpah"
    record_id = "REC_0001"
    
    for family in FAMILIES:
        for severity in ("MILD", "STRONG"):
            res1 = obfuscate(text, record_id, family, severity, seed=42)
            res2 = obfuscate(text, record_id, family, severity, seed=42)
            assert res1.text_obfuscated == res2.text_obfuscated, f"Mismatch in {family} {severity}"
            assert res1.modified_char_count == res2.modified_char_count
            assert res1.status == res2.status


def test_different_seeds_or_ids_deterministic():
    text = "daftar di situs gacor sekarang dapat bonus melimpah"
    res_a = obfuscate(text, "REC_0001", "O1_CHAR_SUBSTITUTION", "MILD", seed=42)
    res_b = obfuscate(text, "REC_0001", "O1_CHAR_SUBSTITUTION", "MILD", seed=999)
    # Both should be deterministic on rerun
    res_a_rerun = obfuscate(text, "REC_0001", "O1_CHAR_SUBSTITUTION", "MILD", seed=42)
    assert res_a.text_obfuscated == res_a_rerun.text_obfuscated


if __name__ == "__main__":
    test_identical_runs_produce_identical_outputs()
    test_different_seeds_or_ids_deterministic()
    print("test_determinism PASS")
