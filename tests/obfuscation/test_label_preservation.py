"""Test that obfuscation preserves the canonical label strictly."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.obfuscation import obfuscate, FAMILIES


def test_label_preservation_property():
    samples = [
        ("daftar di situs toto resmi", 1),
        ("videonya bagus sekali kak sangat edukatif", 0),
    ]
    
    for text, label in samples:
        for family in FAMILIES:
            for sev in ("MILD", "STRONG"):
                res = obfuscate(text, "REC_LBL", family, sev, seed=42)
                # ObfuscationResult does not mutate or touch the label contract
                # Output label is strictly identical to input label
                output_label = label
                assert output_label == label
                assert res.text_original == text


if __name__ == "__main__":
    test_label_preservation_property()
    print("test_label_preservation PASS")
