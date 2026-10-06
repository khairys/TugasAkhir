import os
import sys
import re
import hashlib
import unicodedata
import logging
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/02_harmonize_interim.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

def has_unicode_math(text):
    if not isinstance(text, str): return False
    for char in text:
        cp = ord(char)
        if (0x1D400 <= cp <= 0x1D7FF) or (0x2460 <= cp <= 0x24FF) or (0x2100 <= cp <= 0x214F):
            return True
    return False

def check_quality_flags(text):
    flags = []
    if not isinstance(text, str) or pd.isna(text) or text.strip() == "":
        return "invalid", ["empty_or_whitespace_text"]

    t_strip = text.strip()
    char_len = len(t_strip)
    words = t_strip.split()
    word_count = len(words)

    # Length flags
    if char_len < 4 or word_count < 2:
        flags.append("very_short")
    if char_len > 1000:
        flags.append("very_long")

    # Character type purity
    # digits only
    if re.fullmatch(r'[\d\s]+', t_strip):
        flags.append("digits_only")
    # emoji or symbols only
    alnum_count = sum(1 for c in t_strip if c.isalnum())
    if alnum_count == 0:
        flags.append("no_alphanumeric_chars")

    # URL detection
    if re.search(r'https?://|www\.|\.com|\.id|\.net|\.xyz|\.link', t_strip, re.I):
        flags.append("has_url")

    # Unicode math obfuscation
    if has_unicode_math(t_strip):
        flags.append("has_unicode_math")

    # Whitespace anomaly
    if re.search(r'[\r\n\t]| {2,}|\u00a0|\u200b', text):
        flags.append("whitespace_anomaly")

    # Control chars
    for c in text:
        if unicodedata.category(c) == 'Cc' and c not in ('\n', '\r', '\t'):
            flags.append("control_characters")
            break

    status = "suspicious" if flags else "valid"
    return status, flags

def make_author_group(author_str, prefix):
    if not isinstance(author_str, str) or pd.isna(author_str) or author_str.strip() == "":
        return None
    cleaned = author_str.strip().lower()
    h = hashlib.md5(cleaned.encode('utf-8')).hexdigest()[:10]
    return f"{prefix}_{h}"

def format_timestamp_unix(ts_val):
    if pd.isna(ts_val): return None
    try:
        ts_float = float(ts_val)
        dt = datetime.fromtimestamp(ts_float, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None

def format_timestamp_str(ts_str):
    if not isinstance(ts_str, str) or pd.isna(ts_str) or ts_str.strip() == "":
        return None
    try:
        dt = pd.to_datetime(ts_str.strip(), errors='coerce')
        if pd.isna(dt): return None
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None

def main():
    logging.info("Memulai Phase 2: Harmonization to Canonical Schema (Interim)")

    # 1. DS1 - fahruu
    logging.info("Harmonizing DS1_fahruu...")
    df1 = pd.read_csv("data/raw/ds1_fahruu/judi_online.csv")
    records1 = []
    for idx, row in df1.iterrows():
        raw_val = row["comment"]
        # keep exact raw
        text_raw = raw_val if isinstance(raw_val, str) else ("" if pd.isna(raw_val) else str(raw_val))
        q_status, q_flags = check_quality_flags(text_raw)

        rec_id = f"DS1_{idx+1:06d}"
        s_lbl = row["label"]
        c_lbl = s_lbl if q_status != "invalid" else None
        lbl_status = "accepted" if q_status != "invalid" else "excluded"
        excl_reason = "empty_or_whitespace_text" if q_status == "invalid" else None

        records1.append({
            "record_id": rec_id,
            "source_dataset": "DS1_fahruu",
            "source_row_id": idx,
            "text_raw": text_raw,
            "source_label": s_lbl,
            "canonical_label": c_lbl,
            "label_status": lbl_status,
            "label_reason": "original_source_label",
            "adjudication_note": None,
            "author": None,
            "timestamp": None,
            "timestamp_standardized": None,
            "author_group_id": None,
            "exact_duplicate_group": None,
            "whitespace_duplicate_group": None,
            "normalized_variant_group": None,
            "near_duplicate_group": None,
            "is_exact_duplicate": False,
            "is_cross_dataset_duplicate": False,
            "is_label_conflict": False,
            "data_quality_status": q_status,
            "data_quality_flags": ";".join(q_flags),
            "exclusion_reason": excl_reason,
            "provenance_notes": "source=fahruu/komentar-judi-online; raw_col=comment; preprocessed_col=final_comment"
        })
    df1_harm = pd.DataFrame(records1)
    df1_harm.to_csv("data/interim/ds1_harmonized.csv", index=False, encoding="utf-8")
    logging.info(f"DS1 Harmonized: {len(df1_harm):,} records.")

    # 2. DS2 - kyyyy8_all
    logging.info("Harmonizing DS2_kyyyy8_all...")
    df2 = pd.read_csv("data/raw/ds2_kyyyy8_all/dataset.csv")
    records2 = []
    for idx, row in df2.iterrows():
        raw_val = row["text"]
        text_raw = raw_val if isinstance(raw_val, str) else ("" if pd.isna(raw_val) else str(raw_val))
        q_status, q_flags = check_quality_flags(text_raw)

        rec_id = f"DS2_{idx+1:06d}"
        s_lbl = row["label"]
        c_lbl = s_lbl if q_status != "invalid" else None
        lbl_status = "accepted" if q_status != "invalid" else "excluded"
        excl_reason = "empty_or_whitespace_text" if q_status == "invalid" else None

        records2.append({
            "record_id": rec_id,
            "source_dataset": "DS2_kyyyy8_all",
            "source_row_id": idx,
            "text_raw": text_raw,
            "source_label": s_lbl,
            "canonical_label": c_lbl,
            "label_status": lbl_status,
            "label_reason": "original_source_label",
            "adjudication_note": None,
            "author": None,
            "timestamp": None,
            "timestamp_standardized": None,
            "author_group_id": None,
            "exact_duplicate_group": None,
            "whitespace_duplicate_group": None,
            "normalized_variant_group": None,
            "near_duplicate_group": None,
            "is_exact_duplicate": False,
            "is_cross_dataset_duplicate": False,
            "is_label_conflict": False,
            "data_quality_status": q_status,
            "data_quality_flags": ";".join(q_flags),
            "exclusion_reason": excl_reason,
            "provenance_notes": "source=kyyyy8/dataset-komentar-judi-online-di-youtube; raw_col=text; preprocessed_col=text_preprocessed"
        })
    df2_harm = pd.DataFrame(records2)
    df2_harm.to_csv("data/interim/ds2_harmonized.csv", index=False, encoding="utf-8")
    logging.info(f"DS2 Harmonized: {len(df2_harm):,} records.")

    # 3. DS3 - yaemico
    logging.info("Harmonizing DS3_yaemico...")
    df3 = pd.read_csv("data/raw/ds3_yaemico/youtube_chat_jogja_clean.csv")
    records3 = []
    for idx, row in df3.iterrows():
        raw_val = row["message"]
        text_raw = raw_val if isinstance(raw_val, str) else ("" if pd.isna(raw_val) else str(raw_val))
        q_status, q_flags = check_quality_flags(text_raw)

        rec_id = f"DS3_{idx+1:06d}"
        s_lbl = row["label"]
        c_lbl = s_lbl if q_status != "invalid" else None
        lbl_status = "accepted" if q_status != "invalid" else "excluded"
        excl_reason = "empty_or_whitespace_text" if q_status == "invalid" else None

        auth = str(row["author_name"]) if not pd.isna(row["author_name"]) else None
        auth_group = make_author_group(auth, "DS3_AUTH")
        ts_raw = str(row["datetime"]) if not pd.isna(row["datetime"]) else None
        ts_std = format_timestamp_str(ts_raw)

        records3.append({
            "record_id": rec_id,
            "source_dataset": "DS3_yaemico",
            "source_row_id": idx,
            "text_raw": text_raw,
            "source_label": s_lbl,
            "canonical_label": c_lbl,
            "label_status": lbl_status,
            "label_reason": "original_source_label",
            "adjudication_note": None,
            "author": auth,
            "timestamp": ts_raw,
            "timestamp_standardized": ts_std,
            "author_group_id": auth_group,
            "exact_duplicate_group": None,
            "whitespace_duplicate_group": None,
            "normalized_variant_group": None,
            "near_duplicate_group": None,
            "is_exact_duplicate": False,
            "is_cross_dataset_duplicate": False,
            "is_label_conflict": False,
            "data_quality_status": q_status,
            "data_quality_flags": ";".join(q_flags),
            "exclusion_reason": excl_reason,
            "provenance_notes": "source=yaemico/deteksi-judi-online; raw_col=message; domain=youtube_live_chat_cctv_jogja; candidate_role=OOD_candidate; preprocessed_col=cleaned_message"
        })
    df3_harm = pd.DataFrame(records3)
    df3_harm.to_csv("data/interim/ds3_harmonized.csv", index=False, encoding="utf-8")
    logging.info(f"DS3 Harmonized: {len(df3_harm):,} records.")

    # 4. DS4 - kyyyy8_platform
    logging.info("Harmonizing DS4_kyyyy8_platform...")
    df4 = pd.read_csv("data/raw/ds4_kyyyy8_platform/dataset_komentarJudol_preprocessed_nonAnom.csv")
    records4 = []
    for idx, row in df4.iterrows():
        raw_val = row["text"]
        text_raw = raw_val if isinstance(raw_val, str) else ("" if pd.isna(raw_val) else str(raw_val))
        q_status, q_flags = check_quality_flags(text_raw)

        rec_id = f"DS4_{idx+1:06d}"
        s_lbl = row["label"]
        c_lbl = s_lbl if q_status != "invalid" else None
        lbl_status = "accepted" if q_status != "invalid" else "excluded"
        excl_reason = "empty_or_whitespace_text" if q_status == "invalid" else None

        auth = str(row["author"]) if not pd.isna(row["author"]) else None
        auth_group = make_author_group(auth, "DS4_AUTH")
        ts_raw = str(row["time_parsed"]) if not pd.isna(row["time_parsed"]) else None
        ts_std = format_timestamp_unix(row["time_parsed"])
        cid = str(row["comment_id"]) if not pd.isna(row["comment_id"]) else ""

        records4.append({
            "record_id": rec_id,
            "source_dataset": "DS4_kyyyy8_platform",
            "source_row_id": idx,
            "text_raw": text_raw,
            "source_label": s_lbl,
            "canonical_label": c_lbl,
            "label_status": lbl_status,
            "label_reason": "original_source_label",
            "adjudication_note": None,
            "author": auth,
            "timestamp": ts_raw,
            "timestamp_standardized": ts_std,
            "author_group_id": auth_group,
            "exact_duplicate_group": None,
            "whitespace_duplicate_group": None,
            "normalized_variant_group": None,
            "near_duplicate_group": None,
            "is_exact_duplicate": False,
            "is_cross_dataset_duplicate": False,
            "is_label_conflict": False,
            "data_quality_status": q_status,
            "data_quality_flags": ";".join(q_flags),
            "exclusion_reason": excl_reason,
            "provenance_notes": f"source=kyyyy8/dataset-komentar-judi-online-platform-youtube; comment_id={cid}; raw_col=text; preprocessed_col=text_preprocessed"
        })
    df4_harm = pd.DataFrame(records4)
    df4_harm.to_csv("data/interim/ds4_harmonized.csv", index=False, encoding="utf-8")
    logging.info(f"DS4 Harmonized: {len(df4_harm):,} records.")

    # 5. DS5 - ferdiansakti
    logging.info("Harmonizing DS5_ferdiansakti...")
    df5 = pd.read_csv("data/raw/ds5_ferdiansakti/rawdata.csv")
    records5 = []
    for idx, row in df5.iterrows():
        raw_val = row["Comments"]
        text_raw = raw_val if isinstance(raw_val, str) else ("" if pd.isna(raw_val) else str(raw_val))
        q_status, q_flags = check_quality_flags(text_raw)

        rec_id = f"DS5_{idx+1:06d}"
        s_lbl = row["Label"]
        c_lbl = s_lbl if q_status != "invalid" else None
        lbl_status = "accepted" if q_status != "invalid" else "excluded"
        excl_reason = "empty_or_whitespace_text" if q_status == "invalid" else None

        records5.append({
            "record_id": rec_id,
            "source_dataset": "DS5_ferdiansakti",
            "source_row_id": idx,
            "text_raw": text_raw,
            "source_label": s_lbl,
            "canonical_label": c_lbl,
            "label_status": lbl_status,
            "label_reason": "original_source_label",
            "adjudication_note": None,
            "author": None,
            "timestamp": None,
            "timestamp_standardized": None,
            "author_group_id": None,
            "exact_duplicate_group": None,
            "whitespace_duplicate_group": None,
            "normalized_variant_group": None,
            "near_duplicate_group": None,
            "is_exact_duplicate": False,
            "is_cross_dataset_duplicate": False,
            "is_label_conflict": False,
            "data_quality_status": q_status,
            "data_quality_flags": ";".join(q_flags),
            "exclusion_reason": excl_reason,
            "provenance_notes": "source=ferdiansakti/gambling-comments-from-youtube-platform; raw_col=Comments; campaign_focus=ambil4d"
        })
    df5_harm = pd.DataFrame(records5)
    df5_harm.to_csv("data/interim/ds5_harmonized.csv", index=False, encoding="utf-8")
    logging.info(f"DS5 Harmonized: {len(df5_harm):,} records.")

    total_harm = len(df1_harm) + len(df2_harm) + len(df3_harm) + len(df4_harm) + len(df5_harm)
    logging.info(f"Total interim harmonized records: {total_harm:,} (harus persis 84,004).")

if __name__ == "__main__":
    main()
