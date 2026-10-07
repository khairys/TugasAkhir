"""Validation and measurement utilities for Stage 7 Text Obfuscation."""

from __future__ import annotations

import re
from .config import (
    URL_PATTERN,
    EMAIL_PATTERN,
    SPECIAL_TOKEN_PATTERN,
    TOKEN_PATTERN,
)


def is_protected_token(token: str) -> bool:
    """Check if a token must be strictly protected from transformation."""
    if not token:
        return True

    # URLs
    if URL_PATTERN.search(token):
        return True

    # Emails
    if EMAIL_PATTERN.search(token):
        return True

    # User mentions (@name) or hashtags (#tag)
    if SPECIAL_TOKEN_PATTERN.fullmatch(token):
        return True

    # Standalone numbers
    clean_alnum = [ch for ch in token if ch.isalnum()]
    if clean_alnum and all(ch.isdigit() for ch in clean_alnum):
        return True

    # Pure emoji / punctuation / non-alphanumeric tokens
    if not clean_alnum:
        return True

    # Short tokens: fewer than 4 alphanumeric characters
    if len(clean_alnum) < 4:
        return True

    return False


def find_eligible_token_spans(text: str) -> list[tuple[int, int]]:
    """Find character spans (start, end) of tokens eligible for perturbation."""
    spans: list[tuple[int, int]] = []

    for match in TOKEN_PATTERN.finditer(text):
        token = match.group(0).strip()
        if is_protected_token(token):
            continue
        spans.append((match.start(), match.end()))

    return spans


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute standard Levenshtein edit distance between two strings."""
    if s1 == s2:
        return 0
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def count_character_changes(original: str, transformed: str) -> int:
    """Count the total number of character edits between original and transformed."""
    return levenshtein_distance(original, transformed)


def count_modified_ratio(original: str, transformed: str) -> float:
    """Compute the ratio of modified characters relative to the original length."""
    edits = count_character_changes(original, transformed)
    return edits / max(len(original), 1)


def extract_protected_spans(text: str) -> list[str]:
    """Extract all protected substrings (URLs, emails, mentions, hashtags) from text."""
    protected: list[str] = []
    
    # URLs
    for match in URL_PATTERN.finditer(text):
        protected.append(match.group(0))
        
    # Emails
    for match in EMAIL_PATTERN.finditer(text):
        protected.append(match.group(0))
        
    # Mentions & hashtags
    for match in TOKEN_PATTERN.finditer(text):
        tok = match.group(0)
        if SPECIAL_TOKEN_PATTERN.fullmatch(tok):
            protected.append(tok)
            
    return protected


def verify_protected_spans(original: str, transformed: str) -> bool:
    """Verify that every protected span in original text remains intact in transformed text."""
    spans = extract_protected_spans(original)
    for span in spans:
        if span not in transformed:
            return False
    return True
