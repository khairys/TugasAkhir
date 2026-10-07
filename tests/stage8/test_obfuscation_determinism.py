"""Tests for Stage 8: Obfuscation Determinism.

Validates that:
- Running the obfuscation engine on test records produces 100% byte-identical output to the generated condition files.
"""

from pathlib import Path
import pandas as pd
import pytest

import sys
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.obfuscation import SEED, obfuscate

CONDITIONS = [
    ("O1_CHAR_SUBSTITUTION", "MILD", "O1_MILD"),
    ("O1_CHAR_SUBSTITUTION", "STRONG", "O1_STRONG"),
    ("O2_CHAR_INSERT_DELETE", "MILD", "O2_MILD"),
    ("O2_CHAR_INSERT_DELETE", "STRONG", "O2_STRONG"),
    ("O3_WHITESPACE", "MILD", "O3_MILD"),
    ("O3_WHITESPACE", "STRONG", "O3_STRONG"),
    ("O4_UNICODE_ORTHOGRAPHIC", "MILD", "O4_MILD"),
    ("O4_UNICODE_ORTHOGRAPHIC", "STRONG", "O4_STRONG"),
]


@pytest.mark.parametrize("family,severity,filename", CONDITIONS)
def test_condition_determinism_sample(family, severity, filename):
    cond_path = REPO_ROOT / "data" / "processed" / "obfuscated_test_v1" / f"{filename}.csv"
    assert cond_path.exists(), f"Condition file missing: {cond_path}"
    
    cond_df = pd.read_csv(cond_path, low_memory=False)
    # Test deterministic reproduction on 50 deterministic samples per condition
    samples = cond_df.sample(n=min(50, len(cond_df)), random_state=SEED)
    
    for _, row in samples.iterrows():
        rec_id = str(row["source_record_id"])
        orig_text = str(row["text_original"]) if pd.notna(row["text_original"]) else ""
        
        res = obfuscate(
            text=orig_text,
            source_record_id=rec_id,
            family=family,
            severity=severity,
            seed=SEED
        )
        
        assert res.text_obfuscated == str(row["text_obfuscated"]) if pd.notna(row["text_obfuscated"]) else ""
        assert res.changed == bool(row["changed"])
        assert res.status == str(row["status"])
