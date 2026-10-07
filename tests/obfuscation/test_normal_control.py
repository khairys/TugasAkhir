"""Test NORMAL control condition."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.obfuscation import obfuscate


def test_normal_control_condition():
    texts = [
        "daftar di situs gacor https://slot.com",
        "halo semuanya selamat pagi!!",
        "12345 67890",
    ]
    
    for t in texts:
        res = obfuscate(t, "REC_NORM", family="NORMAL", severity="NORMAL", seed=42)
        assert res.text_obfuscated == t
        assert not res.changed
        assert res.modified_char_count == 0
        assert res.modified_char_ratio == 0.0
        assert res.status == "SUCCESS"


if __name__ == "__main__":
    test_normal_control_condition()
    print("test_normal_control PASS")
