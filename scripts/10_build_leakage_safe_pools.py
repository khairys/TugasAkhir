import os
import sys
import re
import json
import logging
import hashlib
import unicodedata
from collections import Counter
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.utils.text_hashing import (
    compute_exact_hash,
    compute_whitespace_hash,
    compute_normalized_hash,
    compute_alnum_hash
)

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/10_build_leakage_safe_pools.log",
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

SOURCE_LINEAGE = {
    "DS1_fahruu": "FAHRUU",
    "DS2_kyyyy8_all": "KYYYY8",
    "DS4_kyyyy8_platform": "KYYYY8",
    "DS3_yaemico": "YAEMICO",
    "DS5_ferdiansakti": "FERDIANSAKTI"
}

# Known brand entities strictly separated from generic gambling lexical terms
KNOWN_BRANDS = [
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
    ("dewa787", r"dewa\s*787"),
    ("mona4d", r"mona\s*4\s*d"),
    ("mamajitu", r"mamajitu"),
    ("poipet308", r"poipet\s*308"),
    ("dora77", r"dora\s*77")
]

GAMBLING_LEXICAL_TERMS = [
    ("slot", r"\bslot\b"),
    ("gacor", r"\bgacor\b"),
    ("maxwin", r"\bmaxwin\b"),
    ("scatter", r"\bscatter\b"),
    ("pragmatic", r"\bpragmatic\b"),
    ("zeus_olympus", r"\bzeus\b|kakek\s*zeus|\bolympus\b"),
    ("depo_deposit", r"\bdepo\b|\bdeposit\b"),
    ("wd_withdraw", r"\bwd\b|\bwithdraw\b"),
    ("jp_jackpot", r"\bjp\b|\bjepe\b|\bjackpot\b"),
    ("freebet_freechip", r"\bfreebet\b|\bfreechip\b"),
    ("judi_judol", r"\bjudi\b|\bjudol\b|\btaruhan\b")
]

def detect_brands_and_signals(text):
    if not isinstance(text, str) or pd.isna(text):
        return [], []
    norm = unicodedata.normalize("NFKC", text).lower()
    
    brands = [b_name for b_name, pat in KNOWN_BRANDS if re.search(pat, norm)]
    signals = [s_name for s_name, pat in GAMBLING_LEXICAL_TERMS if re.search(pat, norm)]
    return brands, signals

def classify_promotion_type_heuristic(row, brands, signals):
    """Heuristic subtype classification.

    Explicitly flagged as HEURISTIC (not gold annotation).
    """
    if row["label_status"] == "review" or pd.isna(row["canonical_label_num"]):
        return "ambiguous"
        
    c_lbl = int(row["canonical_label_num"])
    txt = str(row["text_raw"])
    txt_lower = unicodedata.normalize("NFKC", txt).lower()
    
    if c_lbl == 0:
        if re.search(r'jangan|stop|bahaya|merusak|hancur|bego|tolol|haram|dosa|penipu|rungkad|rungkat|korban', txt_lower) and signals:
            return "anti_gambling"
        elif re.search(r'lapor|polisi|pemerintah|kominfo|menteri|tangkap|berantas|koperasi|pasal|hukum|sadbor', txt_lower):
            return "criticism"
        elif re.search(r'spam|bot|nyampah|blokir|penonton', txt_lower):
            return "spam_complaint"
        elif signals:
            return "neutral_gambling_discussion"
        else:
            return "non_gambling"
    elif c_lbl == 1:
        # Check obfuscated promotion
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
    return "ambiguous"

def is_obfuscation_candidate(text):
    if not isinstance(text, str) or pd.isna(text):
        return False
    for c in text:
        cp = ord(c)
        if (0x1D400 <= cp <= 0x1D7FF) or (0x2460 <= cp <= 0x24FF) or (0xFF01 <= cp <= 0xFF5E) or (0x2100 <= cp <= 0x214F):
            return True
    if re.search(r'\b[A-Za-z0-9]\s+[A-Za-z0-9]\s+[A-Za-z0-9]\b', text):
        return True
    if re.search(r'\[dot\]|\(dot\)|\*+[A-Za-z0-9]+\*+|█|☯|✅|⭐', text):
        return True
    return False

def main():
    logging.info("Memulai Phase 10: Build Leakage-Safe Pools, Isolated OOD, and Heuristic Metadata (v2)")
    df = pd.read_pickle("data/interim/full_pool_v2_clustered.pkl")
    N_total = len(df)
    logging.info(f"Loaded {N_total:,} total interim records.")
    
    # 1. Normalize Canonical Label Numerically
    df["canonical_label_num"] = pd.to_numeric(df["canonical_label"], errors="coerce")
    
    # Adjudication reconciliation for 51 conflict groups
    adj_v2 = pd.read_csv("data/audit/label_conflicts_v2.csv")
    adj_map = {}
    for _, r in adj_v2.iterrows():
        c_raw = r["canonical_label"]
        if pd.isna(c_raw) or str(c_raw).lower() in ("nan", "null", "none"):
            c_str = None
        else:
            try:
                c_str = str(int(float(c_raw)))
            except Exception:
                c_str = str(c_raw)
                
        adj_map[r["exact_hash"]] = {
            "canonical_label": c_str,
            "label_status": r["label_status"],
            "adjudication_decision": r["adjudication_decision"],
            "adjudication_reason": r["adjudication_reason"],
            "adjudication_note": r["adjudication_note"]
        }
        
    df["canonical_label"] = df["canonical_label"].astype(object)
    for idx, row in df.iterrows():
        h = row["exact_hash"]
        if h in adj_map:
            item = adj_map[h]
            df.at[idx, "canonical_label"] = item["canonical_label"]
            df.at[idx, "label_status"] = item["label_status"]
            df.at[idx, "label_reason"] = f"conflict_adjudication: {item['adjudication_decision']}"
            df.at[idx, "adjudication_note"] = f"{item['adjudication_reason']} | {item['adjudication_note']}"
            
    df["canonical_label_num"] = pd.to_numeric(df["canonical_label"], errors="coerce")
    df["canonical_label"] = df["canonical_label_num"].apply(lambda v: str(int(v)) if pd.notna(v) else None)
    
    # 2. Entity Detection & Campaign Entity Report v2
    logging.info("Detecting brand entities vs lexical gambling signals...")
    brands_col = []
    signals_col = []
    obf_col = []
    
    for text in df["text_raw"]:
        b, s = detect_brands_and_signals(text)
        brands_col.append(";".join(b) if b else None)
        signals_col.append(";".join(s) if s else None)
        obf_col.append(is_obfuscation_candidate(text))
        
    df["known_brand_entity"] = brands_col
    df["gambling_signal_terms"] = signals_col
    df["obfuscation_candidate"] = obf_col
    
    # Save campaign_entity_report_v2.csv
    brand_counts = Counter([b for sub in brands_col if sub for b in sub.split(";")])
    signal_counts = Counter([s for sub in signals_col if sub for s in sub.split(";")])
    
    ent_rows = []
    for b_name, cnt in brand_counts.most_common():
        ent_rows.append({
            "entity_name": b_name,
            "entity_type": "brand",
            "frequency_raw": cnt,
            "pct_of_total_raw": round(cnt / N_total * 100, 2)
        })
    for s_name, cnt in signal_counts.most_common():
        ent_rows.append({
            "entity_name": s_name,
            "entity_type": "lexical_signal",
            "frequency_raw": cnt,
            "pct_of_total_raw": round(cnt / N_total * 100, 2)
        })
    pd.DataFrame(ent_rows).to_csv("data/audit/campaign_entity_report_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/campaign_entity_report_v2.csv")
    
    # 3. Promotion Type Heuristic v2
    logging.info("Classifying promotion_type_heuristic...")
    prom_types = []
    for idx, row in df.iterrows():
        b = row["known_brand_entity"].split(";") if pd.notna(row["known_brand_entity"]) and str(row["known_brand_entity"]).strip() else []
        s = row["gambling_signal_terms"].split(";") if pd.notna(row["gambling_signal_terms"]) and str(row["gambling_signal_terms"]).strip() else []
        pt = classify_promotion_type_heuristic(row, b, s)
        prom_types.append(pt)
        
    df["promotion_type_heuristic"] = prom_types
    df["promotion_type_heuristic_version"] = "v2"
    df["promotion_type_is_gold"] = False
    
    # 4. Leakage Group & Lineage
    df["leakage_group_id"] = df["near_duplicate_group"].apply(lambda ndg: f"LG_{ndg[4:]}" if ndg else None)
    df["source_lineage"] = df["source_dataset"].map(SOURCE_LINEAGE)
    
    # Scoped author grouping
    def format_author_scope(row):
        auth = row["author"]
        ds = row["source_dataset"]
        if pd.isna(auth) or not auth or str(auth).strip() == "":
            return None
        h = hashlib.md5(str(auth).strip().lower().encode("utf-8")).hexdigest()[:10]
        prefix = "DS4" if ds == "DS4_kyyyy8_platform" else ("DS3" if ds == "DS3_yaemico" else ds[:3])
        return f"{prefix}_AUTH_{h}"
    df["author_group_id"] = df.apply(format_author_scope, axis=1)
    
    # 5. Canonical Representative Selection with Explicit Metadata
    logging.info("Selecting canonical representatives per exact group...")
    df["source_priority_rank"] = df["source_dataset"].map(DATASET_PRIORITY)
    df["source_row_id_int"] = pd.to_numeric(df["source_row_id"], errors="coerce")
    
    # Sort deterministically
    df = df.sort_values(by=["exact_duplicate_group", "source_priority_rank", "source_row_id_int"]).reset_index(drop=True)
    
    # Mark canonical representative
    is_canon = ~df.duplicated(subset=["exact_duplicate_group"], keep="first")
    is_canon = is_canon & (df["data_quality_status"] != "invalid")
    df["is_canonical_representative"] = is_canon
    
    # Group stats
    group_freq = df.groupby("exact_duplicate_group")["record_id"].count()
    df["source_record_count"] = df["exact_duplicate_group"].map(group_freq)
    
    group_sources = df.groupby("exact_duplicate_group")["source_dataset"].unique()
    df["source_datasets_combined"] = df["exact_duplicate_group"].map(lambda g: ";".join(sorted(group_sources.get(g, []))))
    
    df["canonical_selection_reason"] = df.apply(
        lambda r: f"highest_metadata_priority:{r['source_dataset']}" if r["is_canonical_representative"] else "duplicate_record",
        axis=1
    )
    df["canonical_source_priority"] = df["source_priority_rank"]
    
    # 6. Save Canonical Master (Layer 1)
    output_cols = [
        "record_id", "source_dataset", "source_lineage", "source_row_id", "text_raw",
        "source_label", "canonical_label", "label_status", "label_reason", "adjudication_note",
        "author", "timestamp", "timestamp_standardized", "author_group_id",
        "promotion_type_heuristic", "promotion_type_heuristic_version", "promotion_type_is_gold",
        "obfuscation_candidate", "known_brand_entity", "gambling_signal_terms",
        "exact_duplicate_group", "whitespace_duplicate_group", "normalized_variant_group", "near_duplicate_group",
        "leakage_group_id", "source_record_count", "source_datasets_combined", "is_cross_dataset_duplicate",
        "canonical_selection_reason", "canonical_source_priority",
        "data_quality_status", "data_quality_flags", "provenance_notes"
    ]
    
    # Canonical Dataset: accepted unique canonical representatives
    canonical_df = df[(df["is_canonical_representative"] == True) & (df["label_status"] == "accepted")].copy()
    canonical_df[output_cols].to_csv("data/processed/canonical_dataset_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/processed/canonical_dataset_v2.csv ({len(canonical_df):,} records).")
    
    # Clean pool: complete unique canonical pool (including review records cleanly flagged)
    clean_pool_df = df[df["is_canonical_representative"] == True][output_cols].copy()
    clean_pool_df.to_csv("data/processed/clean_pool_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/processed/clean_pool_v2.csv ({len(clean_pool_df):,} records).")
    
    # Review queues v2
    label_review_df = df[df["label_status"] == "review"][[
        "record_id", "source_dataset", "source_row_id", "text_raw", "source_label",
        "canonical_label", "label_status", "label_reason", "adjudication_note",
        "exact_duplicate_group", "near_duplicate_group", "leakage_group_id"
    ]]
    label_review_df.to_csv("data/review/label_review_queue_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/review/label_review_queue_v2.csv ({len(label_review_df)} records).")
    
    dq_review_df = df[df["data_quality_status"] == "invalid"][[
        "record_id", "source_dataset", "source_row_id", "text_raw", "source_label",
        "data_quality_status", "data_quality_flags", "exclusion_reason"
    ]]
    dq_review_df.to_csv("data/review/data_quality_review_queue_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/review/data_quality_review_queue_v2.csv ({len(dq_review_df)} records).")
    
    # 7. Layer 2: Main Model Candidate Pool (DS1, DS2, DS4)
    logging.info("Building Layer 2: main_pool_candidate_v2.csv...")
    main_pool_df = canonical_df[canonical_df["source_dataset"].isin(["DS1_fahruu", "DS2_kyyyy8_all", "DS4_kyyyy8_platform"])].copy()
    main_pool_df[output_cols].to_csv("data/processed/main_pool_candidate_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/processed/main_pool_candidate_v2.csv ({len(main_pool_df):,} records).")
    
    # Main pool source coverage report (Section 30)
    logging.info("Generating main_pool_source_coverage_v2.csv...")
    cov_rows = []
    for _, r in main_pool_df.iterrows():
        sources_present = r["source_datasets_combined"].split(";") if pd.notna(r["source_datasets_combined"]) else [r["source_dataset"]]
        cov_rows.append({
            "exact_duplicate_group": r["exact_duplicate_group"],
            "text_raw": r["text_raw"],
            "canonical_representative_source": r["source_dataset"],
            "source_lineage": r["source_lineage"],
            "appears_in_DS1": "DS1_fahruu" in sources_present,
            "appears_in_DS2": "DS2_kyyyy8_all" in sources_present,
            "appears_in_DS4": "DS4_kyyyy8_platform" in sources_present,
            "source_count": len([s for s in sources_present if s in ("DS1_fahruu", "DS2_kyyyy8_all", "DS4_kyyyy8_platform")])
        })
    pd.DataFrame(cov_rows).to_csv("data/audit/main_pool_source_coverage_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/main_pool_source_coverage_v2.csv")
    
    # 8. Layer 3: OOD DS3 Construction with Multi-Stage Isolation against Main Pool (Section 24, 25)
    logging.info("Constructing isolated OOD DS3 candidate...")
    main_exact = set(main_pool_df["exact_duplicate_group"].dropna())
    main_ws = set(main_pool_df["whitespace_duplicate_group"].dropna())
    main_norm = set(main_pool_df["normalized_variant_group"].dropna())
    main_ndg = set(main_pool_df["near_duplicate_group"].dropna())
    
    ds3_all_valid = df[(df["source_dataset"] == "DS3_yaemico") & (df["data_quality_status"] != "invalid")].drop_duplicates("exact_duplicate_group").copy()
    initial_ds3_count = len(ds3_all_valid)
    
    ood_overlap_examples = []
    
    # Filter 1: Exact overlap
    is_exact_ov = ds3_all_valid["exact_duplicate_group"].isin(main_exact)
    for _, ov_r in ds3_all_valid[is_exact_ov].iterrows():
        ood_overlap_examples.append({
            "record_id": ov_r["record_id"],
            "text_raw": ov_r["text_raw"],
            "exclusion_stage": "exact_overlap",
            "matched_group": ov_r["exact_duplicate_group"]
        })
    rem1 = ds3_all_valid[~is_exact_ov].copy()
    exact_removed = int(is_exact_ov.sum())
    
    # Filter 2: Whitespace overlap
    is_ws_ov = rem1["whitespace_duplicate_group"].isin(main_ws)
    for _, ov_r in rem1[is_ws_ov].iterrows():
        ood_overlap_examples.append({
            "record_id": ov_r["record_id"],
            "text_raw": ov_r["text_raw"],
            "exclusion_stage": "whitespace_overlap",
            "matched_group": ov_r["whitespace_duplicate_group"]
        })
    rem2 = rem1[~is_ws_ov].copy()
    ws_removed = int(is_ws_ov.sum())
    
    # Filter 3: Normalized variant overlap
    is_norm_ov = rem2["normalized_variant_group"].isin(main_norm)
    for _, ov_r in rem2[is_norm_ov].iterrows():
        ood_overlap_examples.append({
            "record_id": ov_r["record_id"],
            "text_raw": ov_r["text_raw"],
            "exclusion_stage": "normalized_variant_overlap",
            "matched_group": ov_r["normalized_variant_group"]
        })
    rem3 = rem2[~is_norm_ov].copy()
    norm_removed = int(is_norm_ov.sum())
    
    # Filter 4: Verified Near-duplicate overlap
    is_ndg_ov = rem3["near_duplicate_group"].isin(main_ndg)
    for _, ov_r in rem3[is_ndg_ov].iterrows():
        ood_overlap_examples.append({
            "record_id": ov_r["record_id"],
            "text_raw": ov_r["text_raw"],
            "exclusion_stage": "near_duplicate_overlap",
            "matched_group": ov_r["near_duplicate_group"]
        })
    final_ood_df = rem3[~is_ndg_ov].copy()
    ndg_removed = int(is_ndg_ov.sum())
    
    # Save OOD candidate and reports
    final_ood_df[output_cols].to_csv("data/processed/ood_ds3_candidate_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/processed/ood_ds3_candidate_v2.csv ({len(final_ood_df):,} strictly isolated records).")
    
    pd.DataFrame(ood_overlap_examples).to_csv("data/audit/ood_ds3_overlap_examples_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/ood_ds3_overlap_examples_v2.csv")
    
    ood_filter_report = pd.DataFrame([{
        "initial_ds3_unique_records": initial_ds3_count,
        "invalid_records_quarantined": len(df[(df["source_dataset"] == "DS3_yaemico") & (df["data_quality_status"] == "invalid")]),
        "exact_overlap_removed": exact_removed,
        "whitespace_overlap_removed": ws_removed,
        "normalized_overlap_removed": norm_removed,
        "near_duplicate_overlap_removed": ndg_removed,
        "total_overlap_removed": exact_removed + ws_removed + norm_removed + ndg_removed,
        "remaining_isolated_ood_records": len(final_ood_df),
        "promotion_count": int((final_ood_df["canonical_label_num"] == 1).sum()),
        "non_promotion_count": int((final_ood_df["canonical_label_num"] == 0).sum())
    }])
    ood_filter_report.to_csv("data/audit/ood_ds3_filter_report_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/ood_ds3_filter_report_v2.csv")
    
    # 9. Layer 3: External DS5 Candidate & Overlap Audit (Section 27)
    logging.info("Constructing external DS5 candidate and auditing overlap...")
    ds5_all_valid = df[(df["source_dataset"] == "DS5_ferdiansakti") & (df["data_quality_status"] != "invalid")].drop_duplicates("exact_duplicate_group").copy()
    
    ds5_exact_ov = ds5_all_valid[ds5_all_valid["exact_duplicate_group"].isin(main_exact)]
    ds5_rem1 = ds5_all_valid[~ds5_all_valid["exact_duplicate_group"].isin(main_exact)]
    ds5_ws_ov = ds5_rem1[ds5_rem1["whitespace_duplicate_group"].isin(main_ws)]
    ds5_rem2 = ds5_rem1[~ds5_rem1["whitespace_duplicate_group"].isin(main_ws)]
    ds5_norm_ov = ds5_rem2[ds5_rem2["normalized_variant_group"].isin(main_norm)]
    ds5_rem3 = ds5_rem2[~ds5_rem2["normalized_variant_group"].isin(main_norm)]
    ds5_ndg_ov = ds5_rem3[ds5_rem3["near_duplicate_group"].isin(main_ndg)]
    
    ds5_overlap_report = pd.DataFrame([{
        "initial_ds5_unique_records": len(ds5_all_valid),
        "exact_overlap_with_main_pool": len(ds5_exact_ov),
        "whitespace_overlap_with_main_pool": len(ds5_ws_ov),
        "normalized_overlap_with_main_pool": len(ds5_norm_ov),
        "near_duplicate_overlap_with_main_pool": len(ds5_ndg_ov),
        "total_overlapping_records": len(ds5_exact_ov) + len(ds5_ws_ov) + len(ds5_norm_ov) + len(ds5_ndg_ov),
        "strictly_non_overlapping_records": len(ds5_rem3[~ds5_rem3["near_duplicate_group"].isin(main_ndg)]),
        "campaign_focus": "ambil4d"
    }])
    ds5_overlap_report.to_csv("data/audit/ds5_overlap_with_main_pool_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/ds5_overlap_with_main_pool_v2.csv")
    
    ds5_all_valid[output_cols].to_csv("data/processed/external_ds5_candidate_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/processed/external_ds5_candidate_v2.csv ({len(ds5_all_valid):,} records).")
    
    # Save master checkpoint
    df.to_pickle("data/processed/full_pool_master_v2.pkl")
    logging.info("Saved data/processed/full_pool_master_v2.pkl")
    print("Script 10 completed successfully.")

if __name__ == "__main__":
    main()
