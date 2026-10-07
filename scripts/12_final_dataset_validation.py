import os
import sys
import hashlib
import logging
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/12_final_dataset_validation.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

RAW_FILES = [
    ("DS1_fahruu", "data/raw/ds1_fahruu/judi_online.csv", 8440, "comment"),
    ("DS2_kyyyy8_all", "data/raw/ds2_kyyyy8_all/dataset.csv", 45592, "text"),
    ("DS3_yaemico", "data/raw/ds3_yaemico/youtube_chat_jogja_clean.csv", 6350, "message"),
    ("DS4_kyyyy8_platform", "data/raw/ds4_kyyyy8_platform/dataset_komentarJudol_preprocessed_nonAnom.csv", 18902, "text"),
    ("DS5_ferdiansakti", "data/raw/ds5_ferdiansakti/rawdata.csv", 4720, "Comments")
]

def df_to_markdown(df):
    headers = list(df.columns)
    lines = []
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        clean_row = [str(val).replace("\n", " ").replace("|", "\\|") for val in row]
        lines.append("| " + " | ".join(clean_row) + " |")
    return "\n".join(lines)

def main():
    logging.info("Memulai Phase 12: Final Comprehensive Dataset Validation & Acceptance (v2)")
    checks = {}
    
    # 1. Raw integrity check
    logging.info("[ASSERT 1] Verifying Raw Files Integrity...")
    manifest = pd.read_csv("data/manifests/raw_file_manifest.csv")
    raw_pass = True
    for _, r in manifest.iterrows():
        p = Path(r["raw_storage_path"])
        act = hashlib.sha256(p.read_bytes()).hexdigest()
        if act != r["sha256_checksum"]:
            raw_pass = False
            logging.error(f"Mismatch on {p}!")
    checks["raw_integrity"] = "PASS" if raw_pass else "FAIL"
    assert raw_pass, "Raw file SHA256 mismatch detected!"
    
    # 2. Source row counts
    logging.info("[ASSERT 2] Verifying Source Row Counts...")
    total_raw_rows = 0
    counts_pass = True
    raw_dfs = {}
    for ds_id, p_str, exp_rows, text_col in RAW_FILES:
        rdf = pd.read_csv(p_str)
        raw_dfs[ds_id] = (rdf, text_col)
        act_rows = len(rdf)
        total_raw_rows += act_rows
        if act_rows != exp_rows:
            counts_pass = False
            logging.error(f"Count mismatch on {ds_id}: expected {exp_rows}, got {act_rows}")
    checks["source_counts"] = "PASS" if (counts_pass and total_raw_rows == 84004) else "FAIL"
    assert counts_pass and total_raw_rows == 84004, "Source row count assertion failed!"
    
    # Load processed datasets
    canonical_df = pd.read_csv("data/processed/canonical_dataset_v2.csv")
    clean_pool_df = pd.read_csv("data/processed/clean_pool_v2.csv")
    main_pool_df = pd.read_csv("data/processed/main_pool_candidate_v2.csv")
    ood_df = pd.read_csv("data/processed/ood_ds3_candidate_v2.csv")
    ds5_all_df = pd.read_csv("data/processed/ds5_all_candidate_v2.csv")
    external_ds5_df = pd.read_csv("data/processed/external_ds5_candidate_v2.csv")
    label_review_df = pd.read_csv("data/review/label_review_queue_v2.csv")
    dq_review_df = pd.read_csv("data/review/data_quality_review_queue_v2.csv")
    master_df = pd.read_pickle("data/processed/full_pool_master_v2.pkl")
    
    # 3. Canonical Uniqueness
    logging.info("[ASSERT 3] Checking Canonical Uniqueness...")
    has_dup_exact = canonical_df.duplicated(subset=["exact_duplicate_group"]).any()
    checks["canonical_uniqueness"] = "PASS" if not has_dup_exact else "FAIL"
    assert not has_dup_exact, "Duplicate exact group found in canonical_dataset_v2!"
    
    # 4. Canonical Raw Text matches Source Raw Text (100% FULL CHECK: All 48,051 records)
    logging.info("[ASSERT 4] Verifying 100% Full Canonical Raw Text Byte-for-Byte against Source (all 48,051 records)...")
    raw_text_cache = {}
    for ds_id, (rdf, tcol) in raw_dfs.items():
        raw_text_cache[ds_id] = [
            val if isinstance(val, str) else ("" if pd.isna(val) else str(val))
            for val in rdf[tcol]
        ]
        
    canonical_rows_checked = len(canonical_df)
    raw_text_mismatch = 0
    missing_source_row = 0
    source_dataset_mismatch = 0
    
    for r in canonical_df.itertuples(index=False):
        ds_id = getattr(r, "source_dataset")
        row_id = int(getattr(r, "source_row_id"))
        c_txt = getattr(r, "text_raw")
        if not isinstance(c_txt, str):
            c_txt = "" if pd.isna(c_txt) else str(c_txt)
            
        if ds_id not in raw_text_cache:
            source_dataset_mismatch += 1
            continue
            
        cache = raw_text_cache[ds_id]
        if row_id < 0 or row_id >= len(cache):
            missing_source_row += 1
            continue
            
        s_txt = cache[row_id]
        if c_txt != s_txt:
            raw_text_mismatch += 1
            if raw_text_mismatch <= 5:
                logging.error(f"Mismatch at {getattr(r, 'record_id')}: canonical='{c_txt}' vs source='{s_txt}'")
                
    text_match_pass = (canonical_rows_checked == 48051 and raw_text_mismatch == 0 and missing_source_row == 0 and source_dataset_mismatch == 0)
    checks["raw_text_match"] = "PASS" if text_match_pass else "FAIL"
    assert text_match_pass, f"Raw text verification failed! checked={canonical_rows_checked}, mismatch={raw_text_mismatch}, missing={missing_source_row}, ds_mismatch={source_dataset_mismatch}"
    logging.info(f"[ASSERT 4 PASSED] Checked {canonical_rows_checked:,} records, 0 mismatches, 0 missing rows.")
    
    # 5. Label Integrity
    logging.info("[ASSERT 5] Checking Canonical Label Integrity (only 0 or 1 allowed)...")
    c_labels = set(canonical_df["canonical_label"].astype(str))
    label_int_pass = c_labels.issubset({"0", "1"})
    checks["label_integrity"] = "PASS" if label_int_pass else "FAIL"
    assert label_int_pass, f"Unexpected labels in canonical dataset: {c_labels}"
    
    # 6. Review Isolation
    logging.info("[ASSERT 6] Checking Review Records Isolation...")
    rev_exacts = set(label_review_df["exact_duplicate_group"].dropna())
    canon_exacts = set(canonical_df["exact_duplicate_group"].dropna())
    rev_in_canon = rev_exacts.intersection(canon_exacts)
    checks["review_isolation"] = "PASS" if len(rev_in_canon) == 0 else "FAIL"
    assert len(rev_in_canon) == 0, f"Review records leaked into canonical dataset: {rev_in_canon}"
    
    # 7. Overlap Monotonicity
    logging.info("[ASSERT 7] Verifying Pairwise Overlap Monotonicity across all 10 pairs...")
    overlap_df = pd.read_csv("data/audit/cross_dataset_overlap_v2.csv")
    mono_pass = True
    for _, r in overlap_df.iterrows():
        e = r["shared_exact_groups"]
        w = r["shared_whitespace_groups"]
        n = r["shared_normalized_groups"]
        a = r["shared_alnum_groups"]
        if not (e <= w <= n <= a):
            mono_pass = False
            logging.error(f"Monotonicity failed for {r['dataset_a']} vs {r['dataset_b']}: e={e}, w={w}, n={n}, a={a}")
    checks["overlap_monotonicity"] = "PASS" if mono_pass else "FAIL"
    assert mono_pass, "Overlap monotonicity failed!"
    
    # 8. OOD DS3 Isolation against Main Pool
    logging.info("[ASSERT 8] Checking Strict Isolation of OOD DS3 Candidate...")
    main_exact = set(main_pool_df["exact_duplicate_group"].dropna())
    main_ws = set(main_pool_df["whitespace_duplicate_group"].dropna())
    main_norm = set(main_pool_df["normalized_variant_group"].dropna())
    main_ndg = set(main_pool_df["near_duplicate_group"].dropna())
    
    ood_exact = set(ood_df["exact_duplicate_group"].dropna())
    ood_ws = set(ood_df["whitespace_duplicate_group"].dropna())
    ood_norm = set(ood_df["normalized_variant_group"].dropna())
    ood_ndg = set(ood_df["near_duplicate_group"].dropna())
    
    ood_leak_exact = len(ood_exact.intersection(main_exact))
    ood_leak_ws = len(ood_ws.intersection(main_ws))
    ood_leak_norm = len(ood_norm.intersection(main_norm))
    ood_leak_ndg = len(ood_ndg.intersection(main_ndg))
    
    ood_pass = (ood_leak_exact == 0 and ood_leak_ws == 0 and ood_leak_norm == 0 and ood_leak_ndg == 0)
    checks["ood_isolation"] = "PASS" if ood_pass else "FAIL"
    assert ood_pass, f"OOD DS3 leakage detected! exact={ood_leak_exact}, ws={ood_leak_ws}, norm={ood_leak_norm}, ndg={ood_leak_ndg}"
    
    # 9. DS5 External Candidate Strict Isolation against Main Pool
    logging.info("[ASSERT 9] Verifying DS5 External Candidate Strict Isolation against Main Pool...")
    ds5_overlap_file = Path("data/audit/ds5_overlap_with_main_pool_v2.csv")
    ds5_ex_file = Path("data/processed/external_ds5_candidate_v2.csv")
    ds5_all_file = Path("data/processed/ds5_all_candidate_v2.csv")
    
    assert ds5_overlap_file.exists(), "DS5 overlap audit file missing!"
    assert ds5_ex_file.exists(), "external_ds5_candidate_v2.csv missing!"
    assert ds5_all_file.exists(), "ds5_all_candidate_v2.csv missing!"
    
    ds5_ex_exact = set(external_ds5_df["exact_duplicate_group"].dropna())
    ds5_ex_ws = set(external_ds5_df["whitespace_duplicate_group"].dropna())
    ds5_ex_norm = set(external_ds5_df["normalized_variant_group"].dropna())
    ds5_ex_ndg = set(external_ds5_df["near_duplicate_group"].dropna())
    
    ds5_leak_exact = len(ds5_ex_exact.intersection(main_exact))
    ds5_leak_ws = len(ds5_ex_ws.intersection(main_ws))
    ds5_leak_norm = len(ds5_ex_norm.intersection(main_norm))
    ds5_leak_ndg = len(ds5_ex_ndg.intersection(main_ndg))
    
    ds5_counts_pass = (len(ds5_all_df) == 4202 and len(external_ds5_df) == 3999)
    ds5_leak_pass = (ds5_leak_exact == 0 and ds5_leak_ws == 0 and ds5_leak_norm == 0 and ds5_leak_ndg == 0)
    ds5_pass = ds5_counts_pass and ds5_leak_pass
    checks["ds5_isolation"] = "PASS" if ds5_pass else "FAIL"
    assert ds5_pass, f"DS5 strict isolation failed! counts: all={len(ds5_all_df)}/4202, isolated={len(external_ds5_df)}/3999; leakage: exact={ds5_leak_exact}, ws={ds5_leak_ws}, norm={ds5_leak_norm}, ndg={ds5_leak_ndg}"
    logging.info(f"[ASSERT 9 PASSED] DS5 all={len(ds5_all_df):,}, isolated={len(external_ds5_df):,}, zero leakage across all 4 levels.")
    
    # 10. Reconciliation Count Consistency
    logging.info("[ASSERT 10] Checking Complete Reconciliation Consistency...")
    unique_exact_groups = master_df["exact_duplicate_group"].nunique()
    accepted_groups = len(canonical_df)
    review_groups = len(label_review_df.drop_duplicates("exact_duplicate_group"))
    invalid_records = len(dq_review_df) if len(dq_review_df) else 0
    recon_pass = (accepted_groups + review_groups == unique_exact_groups)
    checks["reconciliation_consistency"] = "PASS" if recon_pass else "FAIL"
    assert recon_pass, f"Reconciliation mismatch: accepted({accepted_groups}) + review({review_groups}) != unique({unique_exact_groups})"
    
    logging.info("ALL 10 HARD ASSERTIONS PASSED WITH FLYING COLORS!")
    
    # Generate data/audit/final_dataset_validation_v3.md
    logging.info("Writing final_dataset_validation_v3.md...")
    md = []
    md.append("# FINAL DATASET VALIDATION REPORT v3 (Pipeline Hardening)")
    md.append("\n**Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Text Obfuscation pada Komentar YouTube Bahasa Indonesia**\n")
    md.append(f"- **Pipeline Version**: `dataset_finalization_v3`")
    md.append(f"- **Random Seed**: 42")
    md.append(f"- **Python Version**: `{sys.version.split()[0]}`")
    md.append(f"- **Pandas Version**: `{pd.__version__}`")
    md.append(f"- **NumPy Version**: `{np.__version__}`\n")
    md.append("---\n")
    
    # Summary of 10 Automated Hard Assertions
    md.append("## Automated Hard Assertions Summary (10/10 PASS)")
    assert_summary = [
        {"Assertion #": "ASSERT 1", "Check Description": "Raw Files Integrity (SHA-256 Checksum on 5 source files)", "Status": checks["raw_integrity"]},
        {"Assertion #": "ASSERT 2", "Check Description": "Source Row Counts Exactness (84,004 raw records)", "Status": checks["source_counts"]},
        {"Assertion #": "ASSERT 3", "Check Description": "Canonical Exact Group Uniqueness (48,051 unique accepted)", "Status": checks["canonical_uniqueness"]},
        {"Assertion #": "ASSERT 4", "Check Description": "100% Full Canonical Raw Text Byte-for-Byte Check (48,051 records)", "Status": checks["raw_text_match"]},
        {"Assertion #": "ASSERT 5", "Check Description": "Canonical Label Integrity (Strictly binary 0 or 1)", "Status": checks["label_integrity"]},
        {"Assertion #": "ASSERT 6", "Check Description": "Review Records Isolation (Quarantined from accepted pool)", "Status": checks["review_isolation"]},
        {"Assertion #": "ASSERT 7", "Check Description": "Pairwise Overlap Monotonicity (E <= W <= N <= A across 10 pairs)", "Status": checks["overlap_monotonicity"]},
        {"Assertion #": "ASSERT 8", "Check Description": "Strict Isolation of OOD DS3 Candidate (0 leakage into main pool)", "Status": checks["ood_isolation"]},
        {"Assertion #": "ASSERT 9", "Check Description": "Strict Isolation of External DS5 Candidate (0 leakage into main pool)", "Status": checks["ds5_isolation"]},
        {"Assertion #": "ASSERT 10", "Check Description": "Complete Pool Reconciliation Consistency (48,051 + 3 = 48,054)", "Status": checks["reconciliation_consistency"]}
    ]
    md.append(df_to_markdown(pd.DataFrame(assert_summary)))
    md.append("\n\n---\n")
    
    # A. Raw Integrity
    md.append("## A. Raw Integrity")
    md.append("Status: **PASS (100% Immutable)**\n")
    raw_int_df = pd.read_csv("data/audit/raw_integrity_check_v2.csv")
    md.append(df_to_markdown(raw_int_df))
    
    # B. Reconciliation
    md.append("\n\n## B. Reconciliation")
    recon_df = pd.read_csv("data/audit/dataset_reconciliation_v2.csv")
    md.append(df_to_markdown(recon_df))
    
    # C. Pairwise Overlap
    md.append("\n\n## C. Pairwise Overlap (All 10 Pairs)")
    md.append(df_to_markdown(overlap_df))
    
    # D. Conflict Accounting
    md.append("\n\n## D. Conflict Accounting")
    conf_df = pd.read_csv("data/audit/conflict_summary_v2.csv")
    md.append(df_to_markdown(conf_df))
    
    # E. Near Duplicate
    md.append("\n\n## E. Near Duplicate Clustering Summary")
    nd_summary = [
        {"metric": "Unique Normalized Variant Groups (NVG)", "value": master_df["normalized_variant_group"].nunique()},
        {"metric": "Near-Duplicate Groups / Template Families (NDG)", "value": master_df["near_duplicate_group"].nunique()},
        {"metric": "Consolidated Leakage Groups (LG)", "value": master_df["leakage_group_id"].nunique()},
        {"metric": "Inspection Sample Pairs Verified", "value": 300},
        {"metric": "Large Bucket Handling", "value": "Secondary deterministic sub-blocking (one-level deterministic partition)"}
    ]
    md.append(df_to_markdown(pd.DataFrame(nd_summary)))
    
    # F. Canonical Dataset
    md.append("\n\n## F. Canonical Dataset (Layer 1)")
    lbl_canon = canonical_df["canonical_label"].value_counts().to_dict()
    c0 = int(lbl_canon.get(0, lbl_canon.get("0", 0)))
    c1 = int(lbl_canon.get(1, lbl_canon.get("1", 0)))
    md.append(f"- **Total Canonical Records**: {len(canonical_df):,} rekaman.")
    md.append(f"- **Promotion (1)**: {c1:,} ({round(c1/len(canonical_df)*100, 2)}%)")
    md.append(f"- **Non-Promotion (0)**: {c0:,} ({round(c0/len(canonical_df)*100, 2)}%)\n")
    
    canon_src = canonical_df["source_dataset"].value_counts().to_dict()
    md.append("### Source Representative Attribution:")
    for ds, cnt in canon_src.items():
        md.append(f"- `{ds}`: {cnt:,} ({round(cnt/len(canonical_df)*100, 2)}%)")
        
    # G. Main Pool Candidate
    md.append("\n\n## G. Main Pool Candidate (Layer 2: DS1 + Unified Kyyyy8)")
    mp_lbl = main_pool_df["canonical_label"].value_counts().to_dict()
    mp0 = int(mp_lbl.get(0, mp_lbl.get("0", 0)))
    mp1 = int(mp_lbl.get(1, mp_lbl.get("1", 0)))
    md.append(f"- **Total Main Pool Records**: {len(main_pool_df):,} rekaman.")
    md.append(f"- **Promotion (1)**: {mp1:,} ({round(mp1/len(main_pool_df)*100, 2)}%)")
    md.append(f"- **Non-Promotion (0)**: {mp0:,} ({round(mp0/len(main_pool_df)*100, 2)}%)\n")
    
    # H. DS3 OOD Candidate
    md.append("\n## H. DS3 OOD Candidate (Layer 3: Live Chat CCTV Jogja Isolated)")
    ood_rep = pd.read_csv("data/audit/ood_ds3_filter_report_v2.csv")
    md.append(df_to_markdown(ood_rep))
    
    # I. DS5 External Candidate
    md.append("\n\n## I. DS5 External Candidate (Layer 3: Ambil4d Focused)")
    ds5_rep = pd.read_csv("data/audit/ds5_overlap_with_main_pool_v2.csv")
    md.append(df_to_markdown(ds5_rep))
    md.append(f"\n- **All Valid DS5 Records (`ds5_all_candidate_v2.csv`)**: {len(ds5_all_df):,} records (Audit & auxiliary provenance).")
    md.append(f"- **Strictly Isolated External DS5 (`external_ds5_candidate_v2.csv`)**: {len(external_ds5_df):,} records (0 leakage with main training pool across exact, whitespace, normalized, and near-duplicate).")
    md.append(f"- **Quarantined Overlap Records (`ds5_overlap_examples_v2.csv`)**: 203 records (21 exact, 0 ws, 3 normalized, 179 near-duplicate).")
    
    # J. 100% Full Raw-Text Byte-for-Byte Verification
    md.append("\n\n## J. 100% Full Raw-Text Byte-for-Byte Verification")
    md.append(f"- **Canonical Records Checked**: {canonical_rows_checked:,} / {len(canonical_df):,} (100% full coverage)")
    md.append(f"- **Raw Text Mismatch Count**: {raw_text_mismatch}")
    md.append(f"- **Missing Source Rows**: {missing_source_row}")
    md.append(f"- **Source Dataset Mismatch**: {source_dataset_mismatch}")
    md.append("- **Verification Status**: **PASS (Byte-for-byte exact against raw source CSVs)**")
    
    # K. Heuristic Metadata Clarification
    md.append("\n\n## K. Heuristic Metadata Clarification")
    md.append("- `promotion_type_heuristic`: Metadata turunan berbasis aturan (rule-based) untuk audit dan analisis, **BUKAN** anotasi gold manusia (`promotion_type_is_gold = False`).")
    md.append("- `known_brand_entity`: Entitas nama situs/platform perjudian resmi yang teridentifikasi.")
    md.append("- `gambling_signal_terms`: Istilah leksikal perjudian generik (misal `slot`, `gacor`, `maxwin`, `zeus`) yang sengaja dipisahkan agar tidak membingungkan pelaporan entitas kampanye.")
    md.append("- `obfuscation_candidate`: Flag keberadaan karakter font matematika unicode, pemisahan spasi, atau karakter pemblokir filter.")
    
    # L. Final Decision
    all_pass = all(v == "PASS" for v in checks.values())
    final_status = "READY_FOR_SPLIT" if all_pass else "NOT_READY_FOR_SPLIT"
    md.append(f"\n\n## L. Final Decision")
    md.append(f"### FINAL STATUS: `{final_status}`\n")
    md.append("Seluruh 10 automated hard assertions telah tuntas terverifikasi dan memenuhi seluruh batasan metodologis.")
    
    # Save v3 report and update v2 report
    Path("data/audit/final_dataset_validation_v3.md").write_text("\n".join(md), encoding="utf-8")
    Path("data/audit/final_dataset_validation_v2.md").write_text("\n".join(md), encoding="utf-8")
    logging.info("Saved data/audit/final_dataset_validation_v3.md & final_dataset_validation_v2.md")
    print(f"Validation completed. FINAL STATUS: {final_status}")

if __name__ == "__main__":
    main()
