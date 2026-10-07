"""Test protection of special tokens: URLs, emails, mentions, hashtags."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.obfuscation import obfuscate, FAMILIES, verify_protected_spans


def test_url_protection():
    text = "kunjungi https://example.com/daftar sekarang juga"
    for family in FAMILIES:
        for sev in ("MILD", "STRONG"):
            res = obfuscate(text, "REC_URL", family, sev, seed=42)
            assert "https://example.com/daftar" in res.text_obfuscated, f"URL damaged in {family} {sev}"
            assert verify_protected_spans(text, res.text_obfuscated)


def test_email_protection():
    text = "hubungi admin@judi99.com sekarang"
    for family in FAMILIES:
        for sev in ("MILD", "STRONG"):
            res = obfuscate(text, "REC_EMAIL", family, sev, seed=42)
            assert "admin@judi99.com" in res.text_obfuscated, f"Email damaged in {family} {sev}"


def test_mention_and_hashtag_protection():
    text = "follow @slotgacor dan gunakan #maxwin sekarang"
    for family in FAMILIES:
        for sev in ("MILD", "STRONG"):
            res = obfuscate(text, "REC_TAG", family, sev, seed=42)
            assert "@slotgacor" in res.text_obfuscated, f"Mention damaged in {family} {sev}"
            assert "#maxwin" in res.text_obfuscated, f"Hashtag damaged in {family} {sev}"


if __name__ == "__main__":
    test_url_protection()
    test_email_protection()
    test_mention_and_hashtag_protection()
    print("test_protected_tokens PASS")
