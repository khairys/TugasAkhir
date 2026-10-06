import hashlib
import re
import unicodedata
import pandas as pd

def compute_exact_hash(text):
    """Exact raw text hash (SHA-256).

    Preserves 100% of original text without any transformation.
    """
    if not isinstance(text, str) or pd.isna(text):
        return "NULL_HASH"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def compute_whitespace_hash(text):
    """Whitespace-normalized hash (SHA-256).

    Strips leading/trailing whitespace and collapses repeated whitespace.
    Does NOT lowercase. Does NOT apply NFKC. Does NOT remove punctuation or emoji.
    """
    if not isinstance(text, str) or pd.isna(text):
        return "NULL_HASH"
    t_ws = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(t_ws.encode("utf-8")).hexdigest()

def compute_normalized_hash(text):
    """Normalized variant hash (SHA-256).

    Applies NFKC normalization, lowercases, collapses whitespace, and strips.
    Used for detecting unicode mathematical font / case variations.
    Audit/grouping only - NEVER modifies raw text.
    """
    if not isinstance(text, str) or pd.isna(text):
        return "NULL_HASH"
    t_norm = unicodedata.normalize("NFKC", text).lower().strip()
    t_norm = re.sub(r"\s+", " ", t_norm)
    return hashlib.sha256(t_norm.encode("utf-8")).hexdigest()

def compute_alnum_hash(text):
    """Alphanumeric audit hash (SHA-256).

    Applies NFKC normalization, lowercases, and removes all non-alphanumeric characters.
    Used specifically to detect deliberate spacing obfuscation like 'T O K E 6 9' vs 'TOKE69'.
    Audit only - NOT a canonical deduplication key.
    """
    if not isinstance(text, str) or pd.isna(text):
        return "NULL_HASH"
    t_norm = unicodedata.normalize("NFKC", text).lower()
    t_alnum = re.sub(r"[^a-z0-9]", "", t_norm)
    if not t_alnum:
        return "EMPTY_ALNUM_HASH"
    return hashlib.sha256(t_alnum.encode("utf-8")).hexdigest()
