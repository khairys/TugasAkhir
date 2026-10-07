"""Test rule-specific mechanics for O1, O2, O3, and O4 families."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.obfuscation import (
    obfuscate,
    CHAR_SUBSTITUTION_MAP,
    UNICODE_CONFUSABLE_MAP,
)


def test_o1_char_substitution():
    text = "situs gacor"
    res = obfuscate(text, "REC_O1", "O1_CHAR_SUBSTITUTION", "MILD", seed=42)
    assert res.changed
    # Check that any changed char is in substitution map values
    assert any(c in CHAR_SUBSTITUTION_MAP.values() for c in res.text_obfuscated)


def test_o2_char_insert_delete():
    text = "sekarang bonus gacor"
    res = obfuscate(text, "REC_O2", "O2_CHAR_INSERT_DELETE", "MILD", seed=42)
    assert res.changed
    # Length differs by +1 (insertion) or -1 (deletion)
    diff = abs(len(res.text_obfuscated) - len(text))
    assert diff == 1


def test_o3_whitespace():
    text = "situs gacor"
    res = obfuscate(text, "O3_REC", "O3_WHITESPACE", "MILD", seed=42)
    assert res.changed
    # Space count increased by 1
    assert res.text_obfuscated.count(" ") == text.count(" ") + 1


def test_o4_unicode_orthographic():
    text = "poker deposit"
    res = obfuscate(text, "O4_REC", "O4_UNICODE_ORTHOGRAPHIC", "MILD", seed=42)
    assert res.changed
    # Should contain either Cyrillic confusable or elongated vowel
    has_cyrillic = any(c in UNICODE_CONFUSABLE_MAP.values() for c in res.text_obfuscated)
    has_elongated = len(res.text_obfuscated) > len(text)
    assert has_cyrillic or has_elongated


if __name__ == "__main__":
    test_o1_char_substitution()
    test_o2_char_insert_delete()
    test_o3_whitespace()
    test_o4_unicode_orthographic()
    print("test_family_rules PASS")
