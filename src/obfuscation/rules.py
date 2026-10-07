"""Transformation rules and random number generator for Stage 7 Text Obfuscation."""

from __future__ import annotations

import hashlib
import random
from .config import (
    SEED,
    CHAR_SUBSTITUTION_MAP,
    UNICODE_CONFUSABLE_MAP,
)
from .validators import find_eligible_token_spans


def make_rng(
    source_record_id: str,
    family: str,
    severity: str,
    seed: int = SEED,
) -> random.Random:
    """Create a deterministic Random instance based on SHA-256 seed payload."""
    payload = f"{seed}|{source_record_id}|{family}|{severity}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    integer_seed = int(digest[:16], 16)
    return random.Random(integer_seed)


def char_substitution(
    text: str,
    source_record_id: str,
    severity: str,
    seed: int = SEED,
) -> tuple[str, int, int]:
    """O1: Substitute selected characters using visual/leetspeak mapping."""
    rng = make_rng(source_record_id, "O1_CHAR_SUBSTITUTION", severity, seed)
    spans = find_eligible_token_spans(text)
    if not spans:
        return text, 0, 0

    # Filter spans that contain at least one substitutable character
    substitutable_spans = [
        (s, e) for s, e in spans if any(text[i] in CHAR_SUBSTITUTION_MAP for i in range(s, e))
    ]
    if not substitutable_spans:
        return text, 0, 0

    max_tokens = 1 if severity == "MILD" else 2
    selected = rng.sample(substitutable_spans, k=min(max_tokens, len(substitutable_spans)))

    chars = list(text)
    modified_chars = 0
    modified_tokens = 0

    for start, end in sorted(selected, reverse=True):
        eligible_positions = [
            i for i in range(start, end) if chars[i] in CHAR_SUBSTITUTION_MAP
        ]
        if not eligible_positions:
            continue

        num_substitutions = 1
        if severity == "STRONG":
            num_substitutions = min(2, len(eligible_positions))

        positions = rng.sample(eligible_positions, k=num_substitutions)
        token_changed = False
        for pos in positions:
            orig = chars[pos]
            chars[pos] = CHAR_SUBSTITUTION_MAP[orig]
            if chars[pos] != orig:
                modified_chars += 1
                token_changed = True
        if token_changed:
            modified_tokens += 1

    return "".join(chars), modified_chars, modified_tokens


def char_insert_delete(
    text: str,
    source_record_id: str,
    severity: str,
    seed: int = SEED,
) -> tuple[str, int, int]:
    """O2: Insert duplicate character or delete internal character in eligible token."""
    rng = make_rng(source_record_id, "O2_CHAR_INSERT_DELETE", severity, seed)
    spans = find_eligible_token_spans(text)
    if not spans:
        return text, 0, 0

    max_tokens = 1 if severity == "MILD" else 2
    selected = rng.sample(spans, k=min(max_tokens, len(spans)))

    chars = list(text)
    offset = 0
    modified_chars = 0
    modified_tokens = 0

    for orig_start, orig_end in sorted(selected):
        start = orig_start + offset
        end = orig_end + offset
        token = "".join(chars[start:end])

        # Find internal alphanumeric positions (excluding first and last character)
        internal_alnum_pos = [
            i for i in range(1, len(token) - 1)
            if token[i].isalnum() and token[i - 1].isalnum()
        ]
        if not internal_alnum_pos:
            continue

        pos = rng.choice(internal_alnum_pos)
        alnum_len = len([c for c in token if c.isalnum()])
        can_delete = alnum_len >= 5  # minimum alphanumeric length after deletion >= 4

        # 50% chance insertion vs deletion (if deletion allowed)
        if rng.random() < 0.5 and can_delete:
            # Deletion of one internal character
            token = token[:pos] + token[pos + 1:]
            offset -= 1
            modified_chars += 1
            modified_tokens += 1
        else:
            # Insertion by duplication of one internal character
            token = token[:pos] + token[pos] + token[pos:]
            offset += 1
            modified_chars += 1
            modified_tokens += 1

        chars[start:end] = list(token)

    return "".join(chars), modified_chars, modified_tokens


def whitespace_manipulation(
    text: str,
    source_record_id: str,
    severity: str,
    seed: int = SEED,
) -> tuple[str, int, int]:
    """O3: Split an eligible token by inserting a single space."""
    rng = make_rng(source_record_id, "O3_WHITESPACE", severity, seed)
    spans = find_eligible_token_spans(text)
    if not spans:
        return text, 0, 0

    max_tokens = 1 if severity == "MILD" else 2
    selected = rng.sample(spans, k=min(max_tokens, len(spans)))

    chars = list(text)
    offset = 0
    modified_chars = 0
    modified_tokens = 0

    for orig_start, orig_end in sorted(selected):
        start = orig_start + offset
        end = orig_end + offset
        token = "".join(chars[start:end])

        # Eligible split positions: strictly between two alphanumeric characters
        split_positions = [
            i for i in range(1, len(token))
            if token[i - 1].isalnum() and token[i].isalnum()
        ]
        if not split_positions:
            continue

        split_pos = rng.choice(split_positions)
        token = token[:split_pos] + " " + token[split_pos:]
        chars[start:end] = list(token)

        offset += 1
        modified_chars += 1
        modified_tokens += 1

    return "".join(chars), modified_chars, modified_tokens


def unicode_orthographic(
    text: str,
    source_record_id: str,
    severity: str,
    seed: int = SEED,
) -> tuple[str, int, int]:
    """O4: Unicode confusable substitution or orthographic elongation."""
    rng = make_rng(source_record_id, "O4_UNICODE_ORTHOGRAPHIC", severity, seed)
    spans = find_eligible_token_spans(text)
    if not spans:
        return text, 0, 0

    max_tokens = 1 if severity == "MILD" else 2
    selected = rng.sample(spans, k=min(max_tokens, len(spans)))

    chars = list(text)
    offset = 0
    modified_chars = 0
    modified_tokens = 0

    for orig_start, orig_end in sorted(selected):
        start = orig_start + offset
        end = orig_end + offset
        token = "".join(chars[start:end])

        # Check for confusable characters first
        confusable_positions = [
            i for i, ch in enumerate(token) if ch in UNICODE_CONFUSABLE_MAP
        ]

        if confusable_positions:
            pos = rng.choice(confusable_positions)
            old_ch = token[pos]
            token = token[:pos] + UNICODE_CONFUSABLE_MAP[old_ch] + token[pos + 1:]
            modified_chars += 1
            modified_tokens += 1
        else:
            # Elongation: duplicate a vowel
            vowel_positions = [
                i for i, ch in enumerate(token) if ch.lower() in "aeiou"
            ]
            if vowel_positions:
                pos = rng.choice(vowel_positions)
                token = token[:pos] + token[pos] + token[pos:]
                offset += 1
                modified_chars += 1
                modified_tokens += 1
            else:
                # Fallback: duplicate an internal alphanumeric character
                internal_alnum = [
                    i for i in range(1, len(token) - 1) if token[i].isalnum()
                ]
                if not internal_alnum:
                    continue
                pos = rng.choice(internal_alnum)
                token = token[:pos] + token[pos] + token[pos:]
                offset += 1
                modified_chars += 1
                modified_tokens += 1

        chars[start:end] = list(token)

    return "".join(chars), modified_chars, modified_tokens
