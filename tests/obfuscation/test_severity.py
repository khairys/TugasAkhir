"""Test severity levels: NORMAL, MILD, and STRONG properties."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.obfuscation import obfuscate, FAMILIES


def test_severity_levels_token_limits():
    text = "daftar di situs slot gacor sekarang dapat bonus melimpah"
    
    for family in FAMILIES:
        res_mild = obfuscate(text, "REC_SEV", family, "MILD", seed=42)
        res_strong = obfuscate(text, "REC_SEV", family, "STRONG", seed=42)
        
        if res_mild.changed:
            assert res_mild.modified_token_count <= 1
            assert res_mild.modified_char_ratio <= 0.20
            
        if res_strong.changed:
            assert res_strong.modified_token_count <= 2
            assert res_strong.modified_char_ratio <= 0.35


if __name__ == "__main__":
    test_severity_levels_token_limits()
    print("test_severity PASS")
