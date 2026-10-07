"""Core obfuscation engine interface for Stage 7 Text Obfuscation."""

from __future__ import annotations

from dataclasses import dataclass
from .config import SEED, FAMILIES, SEVERITIES
from .rules import (
    char_substitution,
    char_insert_delete,
    whitespace_manipulation,
    unicode_orthographic,
)
from .validators import count_character_changes, count_modified_ratio


@dataclass
class ObfuscationResult:
    source_record_id: str
    family: str
    severity: str
    seed: int
    text_original: str
    text_obfuscated: str
    changed: bool
    modified_char_count: int
    modified_char_ratio: float
    modified_token_count: int
    status: str
    failure_reason: str | None = None


def obfuscate(
    text: str,
    source_record_id: str,
    family: str,
    severity: str,
    seed: int = SEED,
) -> ObfuscationResult:
    """Apply deterministic obfuscation to input text.

    Args:
        text: The original text.
        source_record_id: The unique record identifier for deterministic seeding.
        family: Obfuscation family ('NORMAL', 'O1_CHAR_SUBSTITUTION', etc.).
        severity: Severity level ('NORMAL', 'MILD', 'STRONG').
        seed: Global integer seed (default 42).

    Returns:
        ObfuscationResult containing transformed text and diagnostic metrics.
    """
    if severity not in SEVERITIES:
        raise ValueError(f"Unsupported severity '{severity}'. Must be one of {SEVERITIES}")

    # Normal control condition
    if severity == "NORMAL" or family == "NORMAL":
        return ObfuscationResult(
            source_record_id=source_record_id,
            family="NORMAL",
            severity="NORMAL",
            seed=seed,
            text_original=text,
            text_obfuscated=text,
            changed=False,
            modified_char_count=0,
            modified_char_ratio=0.0,
            modified_token_count=0,
            status="SUCCESS",
            failure_reason=None,
        )

    if family not in FAMILIES:
        raise ValueError(f"Unsupported family '{family}'. Must be one of {FAMILIES}")

    # Dispatch to family transformation rule
    if family == "O1_CHAR_SUBSTITUTION":
        transformed, _, token_count = char_substitution(
            text, source_record_id, severity, seed
        )
    elif family == "O2_CHAR_INSERT_DELETE":
        transformed, _, token_count = char_insert_delete(
            text, source_record_id, severity, seed
        )
    elif family == "O3_WHITESPACE":
        transformed, _, token_count = whitespace_manipulation(
            text, source_record_id, severity, seed
        )
    elif family == "O4_UNICODE_ORTHOGRAPHIC":
        transformed, _, token_count = unicode_orthographic(
            text, source_record_id, severity, seed
        )
    else:
        raise ValueError(f"Unhandled family: {family}")

    # Check if transformation actually produced a change
    if transformed == text:
        return ObfuscationResult(
            source_record_id=source_record_id,
            family=family,
            severity=severity,
            seed=seed,
            text_original=text,
            text_obfuscated=text,
            changed=False,
            modified_char_count=0,
            modified_char_ratio=0.0,
            modified_token_count=0,
            status="NO_CHANGE",
            failure_reason="No eligible target or token found for transformation.",
        )

    # Compute exact character-level edits via Levenshtein distance
    edits = count_character_changes(text, transformed)
    ratio = count_modified_ratio(text, transformed)

    return ObfuscationResult(
        source_record_id=source_record_id,
        family=family,
        severity=severity,
        seed=seed,
        text_original=text,
        text_obfuscated=transformed,
        changed=True,
        modified_char_count=edits,
        modified_char_ratio=round(ratio, 4),
        modified_token_count=token_count,
        status="SUCCESS",
        failure_reason=None,
    )
