"""Configuration and constants for Stage 7 Text Obfuscation."""

from __future__ import annotations

import re

SEED = 42

FAMILIES = (
    "O1_CHAR_SUBSTITUTION",
    "O2_CHAR_INSERT_DELETE",
    "O3_WHITESPACE",
    "O4_UNICODE_ORTHOGRAPHIC",
)

SEVERITIES = (
    "NORMAL",
    "MILD",
    "STRONG",
)

# O1: Character Substitution Map (Visual / Leetspeak mapping)
CHAR_SUBSTITUTION_MAP: dict[str, str] = {
    "a": "4",
    "A": "4",
    "e": "3",
    "E": "3",
    "i": "1",
    "I": "1",
    "o": "0",
    "O": "0",
    "s": "5",
    "S": "5",
    "t": "7",
    "T": "7",
    "g": "9",
    "G": "9",
    "b": "8",
    "B": "8",
}

# O4: Unicode Confusable Homoglyph Map (Cyrillic lookalikes)
UNICODE_CONFUSABLE_MAP: dict[str, str] = {
    "a": "\u0430",  # Cyrillic small letter a
    "A": "\u0410",  # Cyrillic capital letter A
    "c": "\u0441",  # Cyrillic small letter es
    "C": "\u0421",  # Cyrillic capital letter Es
    "e": "\u0435",  # Cyrillic small letter ie
    "E": "\u0415",  # Cyrillic capital letter Ie
    "o": "\u043E",  # Cyrillic small letter o
    "O": "\u041E",  # Cyrillic capital letter O
    "p": "\u0440",  # Cyrillic small letter er
    "P": "\u0420",  # Cyrillic capital letter Er
    "x": "\u0445",  # Cyrillic small letter ha
    "X": "\u0425",  # Cyrillic capital letter Ha
}

# Regex patterns for tokenization & protection
TOKEN_PATTERN = re.compile(r"\S+")

URL_PATTERN = re.compile(
    r"(https?://\S+|www\.\S+)",
    re.IGNORECASE,
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

SPECIAL_TOKEN_PATTERN = re.compile(r"^[@#]\S+$")

# Validation diagnostic thresholds
MILD_MAX_MODIFIED_RATIO = 0.20
STRONG_MAX_MODIFIED_RATIO = 0.35
MIN_LENGTH_RATIO = 0.50
MAX_LENGTH_RATIO = 2.00
