"""Stage 7 Text Obfuscation Package."""

from .config import (
    SEED,
    FAMILIES,
    SEVERITIES,
    CHAR_SUBSTITUTION_MAP,
    UNICODE_CONFUSABLE_MAP,
)
from .engine import ObfuscationResult, obfuscate
from .validators import (
    is_protected_token,
    find_eligible_token_spans,
    levenshtein_distance,
    count_character_changes,
    count_modified_ratio,
    verify_protected_spans,
)

__all__ = [
    "SEED",
    "FAMILIES",
    "SEVERITIES",
    "CHAR_SUBSTITUTION_MAP",
    "UNICODE_CONFUSABLE_MAP",
    "ObfuscationResult",
    "obfuscate",
    "is_protected_token",
    "find_eligible_token_spans",
    "levenshtein_distance",
    "count_character_changes",
    "count_modified_ratio",
    "verify_protected_spans",
]
