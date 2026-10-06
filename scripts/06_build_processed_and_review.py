import os
import sys
import re
import json
import logging
import unicodedata
from collections import Counter
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/06_build_processed.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

DATASET_PRIORITY = {
    "DS4_kyyyy8_platform": 1,
    "DS3_yaemico": 2,
    "DS1_fahruu": 3,
    "DS2_kyyyy8_all": 4,
    "DS5_ferdiansakti": 5
}

KNOWN_ENTITIES = [
    ("ambil4d", r"ambil\s*4\s*d"),
    ("gunungwin", r"gunung\s*win"),
    ("alexis17", r"alexis\s*[-_☯❤️]*\s*17"),
    ("wisdomtoto", r"wisdom\s*toto"),
    ("pas4d", r"pas\s*4\s*d"),
    ("bardi4d", r"bardi\s*4\s*d"),
    ("garudahoki", r"ga\s*ruda\s*[-_ ]*ho\s*ki|garuda\s*hoki"),
    ("kembar78", r"kembar\s*78"),
    ("pulauwin", r"pulau\s*win"),
    ("weton88", r"weton\s*`*88"),
    ("timo4d", r"timo\s*4\s*d"),
    ("wifi4d", r"wifi\s*4\s*d"),
    ("sendal4d", r"sendal\s*4\s*d"),
    ("takjub4d", r"takjub\s*4\s*d"),
    ("berkah99", r"berkah\s*99"),
    ("toke69", r"t\s*o\s*k\s*e\s*6\s*9|toke\s*69"),
    ("artis4d", r"artis\s*4\s*d"),
    ("zeus_olympus", r"zeus|kakek\s*zeus|olympus|pragmatic|scatter|maxwin|gacor|slot")
]

def detect_entities(text):
    if not isinstance(text, str):
        return []
    found = []
    # normalize for detection
    norm = unicodedata.normalize('NFKC', text).lower()
    for ent_name, pattern in KNOWN_ENTITIES:
        if re.search(pattern, norm):
            found.append(ent_name)
    return found

def classify_promotion_type(row, entities):
    c_lbl = str(row["canonical_label"]) if pd.notna(row["canonical_label"]) else None
    txt = str(row["text_raw"])
    txt_lower = unicodedata.normalize('NFKC', txt).lower()
    
    if row["label_status"] == "review":
        return "ambiguous"
        
    if c_lbl == "0":
        # Check non-gambling subcategories
        if re.search(r'jangan|stop|bahaya|merusak|hancur|bego|tolol|haram|dosa|penipu|rungkad|rungkat|korban', txt_lower) and any(e in entities for e in ["zeus_olympus", "judi", "judol"]):
            return "anti_gambling"
        elif re.search(r'lapor|polisi|pemerintah|kominfo|menteri|tangkap|berantas|koperasi|pasal|hukum|sadbor', txt_lower):
            return "criticism"
        elif re.search(r'spam|bot|nyampah|blokir|penonton', txt_lower):
            return "spam_complaint"
        elif any(e in entities for e in ["zeus_olympus"]) or re.search(r'judi|judol|slot|taruhan|depo', txt_lower):
            return "neutral_gambling_discussion"
        else:
            return "non_gambling"
    elif c_lbl == "1":
        # Check promotion subcategories
        is_obf = False
        for c in txt:
            cp = ord(c)
            if (0x1D400 <= cp <= 0x1D7FF) or (0x2460 <= cp <= 0x24FF) or (0xFF01 <= cp <= 0xFF5E):
                is_obf = True
                break
        if is_obf or re.search(r'[a-z]\s+[a-z]\s+[a-z]|[-_]{2,}', txt_lower):
            return "obfuscated_promotion"
        elif re.search(r'daftar|link|klik|gabung|join|hubungi|ketik di google|depo disini|wa\.me', txt_lower):
            return "call_to_action"
        elif re.search(r'bonus|freechip|gratis|event|garansi|cashback|diskon', txt_lower):
            return "explicit_ad"
        elif re.search(r'bukti|terima kasih|makasih|kebeli|cuan|hasil|narik|cair|wd|menang|jepe|jp', txt_lower):
            return "testimonial"
        elif re.search(r'gacor|maxwin|sensasional|mudah|gampang|terpercaya|terbaik|mantap|rekomendasi', txt_lower):
            return "promotional_claim"
        else:
            return "site_endorsement"
    else:
        return "ambiguous"

def is_obfuscation_candidate(text):
    if not isinstance(text, str):
        return False
    # Unicode math
    for c in text:
        cp = ord(c)
        if (0x1D400 <= cp <= 0x1D7FF) or (0x2460 <= cp <= 0x24FF) or (0xFF01 <= cp <= 0xFF5E) or (0x2100 <= cp <= 0x214F):
            return True
    # Deliberate letter separation like T O K E 6 9 or G a r u d a
    if re.search(r'\b[A-Za-z0-9]\s+[A-Za-z0-9]\s+[A-Za-z0-9]\b', text):
        return True
    # Obfuscated URL / special symbols
    if re.search(r'\[dot\]|\(dot\)|\*+[A-Za-z0-9]+\*+|█|☯|✅|⭐', text):
        return True
    return False

def main():
    logging.info("Memulai Phase 6: Build Processed Canonical Dataset, Clean Pool, and Review Queues")
    df = pd.read_pickle("data/interim/full_pool_clustered.pkl")
    N_total = len(df)
    logging.info(f"Loaded {N_total:,} records.")
    
    # 1. Obfuscation & Entity & Promotion Type Detection
    logging.info("Detecting entities, obfuscation flags, and promotion types...")
    obf_candidates = []
    entity_lists = []
    
    for text in df["text_raw"]:
        obf = is_obfuscation_candidate(text)
        ents = detect_entities(text)
        obf_candidates.append(obf)
        entity_lists.append(ents)
        
    df["obfuscation_candidate"] = obf_candidates
    df["detected_entities"] = [";".join(e) if e else None for e in entity_lists]
    
    # Campaign frequency count
    all_ents = [ent for sub in entity_lists for ent in sub]
    ent_counts = Counter(all_ents)
    ent_df = pd.DataFrame([{"entity": k, "frequency": v, "pct_of_total_raw": round(v/N_total*100, 2)} for k, v in ent_counts.most_common()])
    ent_df.to_csv("data/audit/campaign_entity_report.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/campaign_entity_report.csv")
    
    # Promotion type
    prom_types = []
    for idx, row in df.iterrows():
        pt = classify_promotion_type(row, entity_lists[idx])
        prom_types.append(pt)
    df["promotion_type"] = prom_types
    
    # 2. Duplicate counts & cross-dataset tracking
    logging.info("Calculating exact duplicate counts and canonical priority...")
    df["priority_rank"] = df["source_dataset"].map(DATASET_PRIORITY)
    
    # Sort dataframe so that for each exact_duplicate_group, the top row is the canonical record
    # Order: priority_rank ASC (DS4=1, DS3=2, DS1=3, DS2=4, DS5=5), then source_row_id ASC
    df = df.sort_values(by=["exact_duplicate_group", "priority_rank", "source_row_id"]).reset_index(drop=True)
    
    # Mark is_canonical_representative: first occurrence in each exact_duplicate_group
    # (handling NULL_HASH separately: invalid records are not canonical representatives)
    is_canonical = ~df.duplicated(subset=["exact_duplicate_group"], keep="first")
    # if data_quality_status == invalid, don't make it canonical
    is_canonical = is_canonical & (df["data_quality_status"] != "invalid")
    df["is_canonical_representative"] = is_canonical
    
    # Count frequency per exact duplicate group
    group_freq = df.groupby("exact_duplicate_group")["record_id"].count()
    df["duplicate_count"] = df["exact_duplicate_group"].map(group_freq)
    
    # Combine source datasets for each exact duplicate group
    group_sources = df.groupby("exact_duplicate_group")["source_dataset"].unique()
    group_sources_str = group_sources.apply(lambda arr: ";".join(sorted(arr)))
    df["source_datasets_combined"] = df["exact_duplicate_group"].map(group_sources_str)
    
    # Candidate role tagging (Section 27, 44)
    def assign_candidate_role(ds):
        if ds == "DS1_fahruu": return "Core_candidate"
        elif ds in ("DS2_kyyyy8_all", "DS4_kyyyy8_platform"): return "Unified_Kyyyy8_candidate"
        elif ds == "DS3_yaemico": return "OOD_candidate"
        elif ds == "DS5_ferdiansakti": return "Auxiliary_candidate"
        return "Unknown"
    df["candidate_role"] = df["source_dataset"].apply(assign_candidate_role)
    
    # 3. Save Manifests
    logging.info("Saving manifests...")
    manifest_cols = [
        "record_id", "source_dataset", "source_row_id", "exact_duplicate_group",
        "near_duplicate_group", "is_canonical_representative", "source_label",
        "canonical_label", "label_status", "data_quality_status", "exclusion_reason",
        "duplicate_count", "source_datasets_combined"
    ]
    df[manifest_cols].to_csv("data/manifests/canonical_record_manifest.csv", index=False, encoding="utf-8")
    logging.info("Saved data/manifests/canonical_record_manifest.csv")
    
    # 4. Review Queues
    logging.info("Building review queues...")
    # Label review queue (all records where label_status == 'review')
    label_review_df = df[df["label_status"] == "review"][[
        "record_id", "source_dataset", "source_row_id", "text_raw", "source_label",
        "canonical_label", "label_status", "label_reason", "adjudication_note",
        "exact_duplicate_group", "near_duplicate_group"
    ]]
    label_review_df.to_csv("data/review/label_review_queue.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/review/label_review_queue.csv ({len(label_review_df)} records).")
    
    # Data quality review queue (all invalid records)
    dq_review_df = df[df["data_quality_status"] == "invalid"][[
        "record_id", "source_dataset", "source_row_id", "text_raw", "source_label",
        "data_quality_status", "data_quality_flags", "exclusion_reason"
    ]]
    dq_review_df.to_csv("data/review/data_quality_review_queue.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/review/data_quality_review_queue.csv ({len(dq_review_df)} records).")
    
    # 5. Processed Datasets
    # Canonical Dataset: only unique canonical representatives with label_status == 'accepted'
    canonical_df = df[(df["is_canonical_representative"] == True) & (df["label_status"] == "accepted")].copy()
    
    canonical_output_cols = [
        "record_id", "source_dataset", "source_row_id", "text_raw", "source_label",
        "canonical_label", "label_status", "label_reason", "adjudication_note",
        "author", "timestamp", "timestamp_standardized", "author_group_id",
        "candidate_role", "promotion_type", "obfuscation_candidate", "detected_entities",
        "exact_duplicate_group", "whitespace_duplicate_group", "normalized_variant_group", "near_duplicate_group",
        "duplicate_count", "source_datasets_combined", "is_cross_dataset_duplicate",
        "data_quality_status", "data_quality_flags", "provenance_notes"
    ]
    
    canonical_df[canonical_output_cols].to_csv("data/processed/canonical_dataset.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/processed/canonical_dataset.csv ({len(canonical_df):,} unique accepted records).")
    
    # Clean pool: complete unique canonical pool (including review records flagged cleanly, for methodology inspection)
    clean_pool_df = df[df["is_canonical_representative"] == True][canonical_output_cols].copy()
    clean_pool_df.to_csv("data/processed/clean_pool.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/processed/clean_pool.csv ({len(clean_pool_df):,} records).")
    
    # Save checkpoint full dataframe
    df.to_pickle("data/processed/full_pool_master.pkl")
    logging.info("Saved data/processed/full_pool_master.pkl")

if __name__ == "__main__":
    main()
