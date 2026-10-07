"""Test handling of texts with no eligible transformation targets."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.obfuscation import obfuscate, FAMILIES


def test_no_eligible_targets_handling():
    # Only digits, emojis, and very short tokens (<4 alnum)
    unusable_texts = [
        "123 456",
        "👍 🔥 ❤️",
        "di ke ya",
        "https://slot.com",
    ]
    
    for t in unusable_texts:
        for family in FAMILIES:
            res = obfuscate(t, "REC_NO_TARGET", family, "MILD", seed=42)
            assert res.text_obfuscated == t
            assert not res.changed
            assert res.status == "NO_CHANGE"
            assert res.failure_reason is not None


if __name__ == "__main__":
    test_no_eligible_targets_handling()
    print("test_failure_handling PASS")
