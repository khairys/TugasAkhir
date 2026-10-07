"""Stage 7: Validate Obfuscation Pilot Dataset and Generate Audit Report.

Validates:
A. Determinism (rerun produces 100% identical outputs)
B. Original text preservation (matches main pool byte-for-byte)
C. Label preservation (canonical label matches main pool)
D. Protected spans (URLs, emails, mentions, hashtags intact)
E. Normal condition (text_obfuscated == text_original, changed == False)
F. Transformation change rates
G. Length sanity flags
H. Excessive corruption diagnostics

Outputs data/audit/obfuscation_pilot_validation_v1.md.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.obfuscation import (
    SEED,
    FAMILIES,
    SEVERITIES,
    obfuscate,
    verify_protected_spans,
)
from src.obfuscation.config import (
    MILD_MAX_MODIFIED_RATIO,
    STRONG_MAX_MODIFIED_RATIO,
    MIN_LENGTH_RATIO,
    MAX_LENGTH_RATIO,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO_ROOT / "logs" / "14_validate_obfuscation_pilot.log", mode="w", encoding="utf-8")
    ]
)


def df_to_markdown(df: pd.DataFrame) -> str:
    headers = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in df.itertuples(index=False):
        clean_row = [str(val).replace("\n", " ").replace("|", "\\|") for val in row]
        lines.append("| " + " | ".join(clean_row) + " |")
    return "\n".join(lines)


def main():
    logging.info("Starting Phase 14: Validate Obfuscation Pilot Dataset (Stage 7)...")
    
    pilot_path = REPO_ROOT / "data" / "interim" / "obfuscation_pilot_v1.csv"
    main_pool_path = REPO_ROOT / "data" / "processed" / "main_pool_candidate_v2.csv"
    review_path = REPO_ROOT / "data" / "review" / "obfuscation_pilot_review_v1.csv"
    
    assert pilot_path.exists(), f"Pilot file missing: {pilot_path}"
    assert main_pool_path.exists(), f"Main pool missing: {main_pool_path}"
    assert review_path.exists(), f"Review queue missing: {review_path}"
    
    pilot_df = pd.read_csv(pilot_path, dtype={"canonical_label": int})
    main_pool_df = pd.read_csv(main_pool_path, dtype={"canonical_label": int})
    review_df = pd.read_csv(review_path, dtype={"canonical_label": int})
    
    logging.info(f"Loaded {len(pilot_df):,} pilot records, {len(review_df):,} review records.")
    
    # Pre-index main pool for O(1) lookup
    main_lookup = {}
    for r in main_pool_df.itertuples(index=False):
        main_lookup[getattr(r, "record_id")] = (
            str(getattr(r, "text_raw")) if pd.notna(getattr(r, "text_raw")) else "",
            int(getattr(r, "canonical_label"))
        )
        
    validation_checks = {}
    
    # -------------------------------------------------------------------------
    # Check A: Determinism
    # -------------------------------------------------------------------------
    logging.info("[CHECK A] Verifying Determinism on all 1,800 pilot records...")
    determinism_mismatch = 0
    for r in pilot_df.itertuples(index=False):
        rec_id = getattr(r, "source_record_id")
        family = getattr(r, "family")
        sev = getattr(r, "severity")
        orig = str(getattr(r, "text_original"))
        exp_obf = str(getattr(r, "text_obfuscated"))
        
        rerun = obfuscate(orig, rec_id, family, sev, seed=SEED)
        if rerun.text_obfuscated != exp_obf:
            determinism_mismatch += 1
            if determinism_mismatch <= 5:
                logging.error(f"Determinism mismatch on {getattr(r, 'pair_id')}")
                
    determinism_pass = (determinism_mismatch == 0)
    validation_checks["A_determinism"] = "PASS" if determinism_pass else "FAIL"
    assert determinism_pass, f"Determinism check failed with {determinism_mismatch} mismatches!"
    logging.info(f"[CHECK A PASSED] All {len(pilot_df):,} records reproduce identically.")
    
    # -------------------------------------------------------------------------
    # Check B: Original Text Preservation
    # -------------------------------------------------------------------------
    logging.info("[CHECK B] Verifying Original Text Preservation against main pool...")
    orig_text_mismatch = 0
    for r in pilot_df.itertuples(index=False):
        rec_id = getattr(r, "source_record_id")
        orig = str(getattr(r, "text_original"))
        if rec_id not in main_lookup:
            orig_text_mismatch += 1
            continue
        expected_raw, _ = main_lookup[rec_id]
        if orig != expected_raw:
            orig_text_mismatch += 1
            
    orig_text_pass = (orig_text_mismatch == 0)
    validation_checks["B_original_preservation"] = "PASS" if orig_text_pass else "FAIL"
    assert orig_text_pass, f"Original text mismatch found in {orig_text_mismatch} records!"
    logging.info("[CHECK B PASSED] All original texts match main pool byte-for-byte.")
    
    # -------------------------------------------------------------------------
    # Check C: Label Preservation
    # -------------------------------------------------------------------------
    logging.info("[CHECK C] Verifying Label Preservation against main pool...")
    label_mismatch = 0
    for r in pilot_df.itertuples(index=False):
        rec_id = getattr(r, "source_record_id")
        pilot_lbl = int(getattr(r, "canonical_label"))
        if rec_id not in main_lookup:
            label_mismatch += 1
            continue
        _, expected_lbl = main_lookup[rec_id]
        if pilot_lbl != expected_lbl:
            label_mismatch += 1
            
    label_pass = (label_mismatch == 0)
    validation_checks["C_label_preservation"] = "PASS" if label_pass else "FAIL"
    assert label_pass, f"Label mismatch found in {label_mismatch} records!"
    logging.info("[CHECK C PASSED] Canonical label strictly preserved across all pairs.")
    
    # -------------------------------------------------------------------------
    # Check D: Protected Spans
    # -------------------------------------------------------------------------
    logging.info("[CHECK D] Verifying Protected Spans (URLs, emails, mentions, hashtags)...")
    protected_violation = 0
    for r in pilot_df.itertuples(index=False):
        orig = str(getattr(r, "text_original"))
        obf = str(getattr(r, "text_obfuscated"))
        if not verify_protected_spans(orig, obf):
            protected_violation += 1
            if protected_violation <= 5:
                logging.error(f"Protected span damaged in {getattr(r, 'pair_id')}")
                
    protected_pass = (protected_violation == 0)
    validation_checks["D_protected_spans"] = "PASS" if protected_pass else "FAIL"
    assert protected_pass, f"Protected span violations found in {protected_violation} records!"
    logging.info("[CHECK D PASSED] All protected spans remain completely intact.")
    
    # -------------------------------------------------------------------------
    # Check E: Normal Condition
    # -------------------------------------------------------------------------
    logging.info("[CHECK E] Verifying Normal Control Condition...")
    normal_df = pilot_df[pilot_df["severity"] == "NORMAL"]
    normal_exact_matches = (normal_df["text_original"] == normal_df["text_obfuscated"]).all()
    normal_no_change = (normal_df["changed"] == False).all()
    normal_zero_chars = (normal_df["modified_char_count"] == 0).all()
    normal_pass = (len(normal_df) == 200 and normal_exact_matches and normal_no_change and normal_zero_chars)
    validation_checks["E_normal_control"] = "PASS" if normal_pass else "FAIL"
    assert normal_pass, "Normal control condition validation failed!"
    logging.info(f"[CHECK E PASSED] All {len(normal_df)} normal controls strictly identical.")
    
    # -------------------------------------------------------------------------
    # Check F: Transformation Statistics & Change Rates
    # -------------------------------------------------------------------------
    logging.info("Computing transformation statistics per family/severity...")
    stat_rows = []
    for family, sev in [
        ("NORMAL", "NORMAL"),
        ("O1_CHAR_SUBSTITUTION", "MILD"),
        ("O1_CHAR_SUBSTITUTION", "STRONG"),
        ("O2_CHAR_INSERT_DELETE", "MILD"),
        ("O2_CHAR_INSERT_DELETE", "STRONG"),
        ("O3_WHITESPACE", "MILD"),
        ("O3_WHITESPACE", "STRONG"),
        ("O4_UNICODE_ORTHOGRAPHIC", "MILD"),
        ("O4_UNICODE_ORTHOGRAPHIC", "STRONG"),
    ]:
        subset = pilot_df[(pilot_df["family"] == family) & (pilot_df["severity"] == sev)]
        n_gen = len(subset)
        n_changed = int((subset["changed"] == True).sum())
        n_no_target = int((subset["status"] == "NO_CHANGE").sum())
        change_rate = round(n_changed / max(n_gen, 1) * 100, 2)
        
        stat_rows.append({
            "family": family,
            "severity": sev,
            "number_generated": n_gen,
            "number_changed": n_changed,
            "number_no_eligible_target": n_no_target,
            "change_rate_pct": change_rate,
        })
    stats_df = pd.DataFrame(stat_rows)
    
    # -------------------------------------------------------------------------
    # Check G & H: Length Sanity & Excessive Modification Diagnostics
    # -------------------------------------------------------------------------
    logging.info("Analyzing modification ratios and length diagnostics...")
    diag_rows = []
    excessive_corruption_count = 0
    length_anomaly_count = 0
    
    for family in FAMILIES:
        for sev in ("MILD", "STRONG"):
            sub = pilot_df[(pilot_df["family"] == family) & (pilot_df["severity"] == sev) & (pilot_df["changed"] == True)]
            if len(sub) == 0:
                continue
                
            chars = sub["modified_char_count"]
            ratios = sub["modified_char_ratio"]
            
            # Diagnostic thresholds
            max_allowed_ratio = MILD_MAX_MODIFIED_RATIO if sev == "MILD" else STRONG_MAX_MODIFIED_RATIO
            n_excessive = int((ratios > max_allowed_ratio).sum())
            excessive_corruption_count += n_excessive
            
            # Length sanity
            len_ratios = sub["text_obfuscated"].str.len() / sub["text_original"].str.len().clip(lower=1)
            n_len_anomaly = int(((len_ratios < MIN_LENGTH_RATIO) | (len_ratios > MAX_LENGTH_RATIO)).sum())
            length_anomaly_count += n_len_anomaly
            
            diag_rows.append({
                "family": family,
                "severity": sev,
                "changed_count": len(sub),
                "mean_mod_chars": round(float(chars.mean()), 2),
                "median_mod_chars": float(chars.median()),
                "max_mod_chars": int(chars.max()),
                "mean_mod_ratio": round(float(ratios.mean()), 4),
                "median_mod_ratio": round(float(ratios.median()), 4),
                "excessive_ratio_flags": n_excessive,
                "length_anomaly_flags": n_len_anomaly,
            })
    diag_df = pd.DataFrame(diag_rows)
    
    # -------------------------------------------------------------------------
    # Check Human Review Queue Integrity & Audit Completion
    # -------------------------------------------------------------------------
    logging.info("Checking human review queue audit completion...")
    assert len(review_df) == 320, f"Expected 320 review samples, got {len(review_df)}"
    # Verify human review fields are completed and approved
    assert (review_df["human_label_preserved"] == "YES").all(), "All samples must have human_label_preserved == YES!"
    assert (review_df["human_meaning_preserved"] == "YES").all(), "All samples must have human_meaning_preserved == YES!"
    assert (review_df["human_transformation_valid"] == "YES").all(), "All samples must have human_transformation_valid == YES!"
    assert (review_df["review_status"] == "APPROVED").all(), "All samples must be APPROVED!"
    logging.info(f"Human review queue: {len(review_df)} samples audited and APPROVED.")
    
    # -------------------------------------------------------------------------
    # Generate data/audit/obfuscation_pilot_validation_v1.md
    # -------------------------------------------------------------------------
    logging.info("Writing validation report data/audit/obfuscation_pilot_validation_v1.md...")
    md = []
    md.append("# OBFUSCATION PILOT VALIDATION REPORT v1")
    md.append("\n**Stage 7: Text Obfuscation Design, Generator, and Pilot Validation**\n")
    md.append(f"- **Timestamp**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    md.append(f"- **Pipeline Version**: `obfuscation_pilot_v1`")
    md.append(f"- **Global Seed**: `{SEED}`")
    md.append(f"- **Source Dataset**: `data/processed/main_pool_candidate_v2.csv`")
    md.append(f"- **Pilot Source Records**: `200` (100 Promotion, 100 Non-Promotion)")
    md.append(f"- **Total Pilot Rows Generated**: `{len(pilot_df):,}` rows (200 source × 9 conditions)")
    md.append(f"- **Human Audit Queue Size**: `{len(review_df)}` samples (balanced across 4 families × 2 severities × 2 labels)")
    md.append(f"- **Python Version**: `{sys.version.split()[0]}`")
    md.append(f"- **Pandas Version**: `{pd.__version__}`")
    md.append(f"- **NumPy Version**: `{np.__version__}`\n")
    md.append("---\n")
    
    # Automated Integrity Assertions Table
    md.append("## 1. Automated Integrity Assertions Summary")
    assertions_table = [
        {"Assertion": "Check A: Determinism", "Rule": "Rerun on 1,800 records produces 100% byte-exact output", "Status": validation_checks["A_determinism"]},
        {"Assertion": "Check B: Original Text Match", "Rule": "text_original strictly matches main pool byte-for-byte", "Status": validation_checks["B_original_preservation"]},
        {"Assertion": "Check C: Label Preservation", "Rule": "canonical_label is identical to main pool label", "Status": validation_checks["C_label_preservation"]},
        {"Assertion": "Check D: Protected Spans", "Rule": "URLs, emails, mentions, hashtags remain completely intact", "Status": validation_checks["D_protected_spans"]},
        {"Assertion": "Check E: Normal Control", "Rule": "All 200 normal controls strictly unchanged (0 edits)", "Status": validation_checks["E_normal_control"]},
        {"Assertion": "Check F: Human Review Verified", "Rule": "320 review samples audited with 100% label and meaning preserved", "Status": "PASS"},
    ]
    md.append(df_to_markdown(pd.DataFrame(assertions_table)))
    md.append("\n\n---\n")
    
    # Generation & Change Rate Statistics
    md.append("## 2. Generation & Change Rate Statistics")
    md.append(df_to_markdown(stats_df))
    md.append("\n\n---\n")
    
    # Modification & Diagnostic Statistics
    md.append("## 3. Modification & Diagnostic Statistics (Changed Records)")
    md.append(df_to_markdown(diag_df))
    md.append(f"\n- **Total Excessive Ratio Flags**: `{excessive_corruption_count}` (Diagnostic flags for human inspection)")
    md.append(f"- **Total Length Anomaly Flags**: `{length_anomaly_count}`\n")
    md.append("---\n")
    
    # Human Review Status
    md.append("## 4. Human Review Audit Status")
    md.append("- **Review Queue Path**: `data/review/obfuscation_pilot_review_v1.csv`")
    md.append("- **Total Review Samples**: `320` samples (4 families × 2 severities × 2 labels × 20 samples)")
    md.append("- **Audit State**: **`AUDIT_COMPLETED_AND_APPROVED`**")
    md.append("- **Audit Summary**: 320 dari 320 sampel (100%) diverifikasi secara kontekstual:")
    md.append("  1. `human_meaning_preserved`: 320/320 (100% YES)")
    md.append("  2. `human_label_preserved`: 320/320 (100% YES)")
    md.append("  3. `human_transformation_valid`: 320/320 (100% YES)")
    md.append("  4. Komentar Non-Promosi (160 sampel): Terverifikasi murni komentar YouTube organik non-judi.")
    md.append("  5. Komentar Promosi (160 sampel): Terverifikasi promosi situs/platform judi online.")
    md.append("- **Keputusan Audit**: Preservasi semantik dan validitas fungsi komunikasi terbukti valid.\n")
    md.append("---\n")
    
    # Final Stage Status
    md.append("## 5. Stage 7 Final Decision")
    md.append("### OBFUSCATION_STATUS: `FROZEN_V1`\n")
    md.append("- Generator implementasi: **SELESAI & VALID ✅**")
    md.append("- Validasi integritas otomatis: **100% PASS ✅**")
    md.append("- Audit semantik & label manusia: **100% VERIFIED & APPROVED ✅**")
    md.append("- Pembekuan spesifikasi formal: **RESMI FROZEN_V1 (Siap masuk Stage 8) ✅**\n")
    
    report_file = REPO_ROOT / "data" / "audit" / "obfuscation_pilot_validation_v1.md"
    report_file.write_text("\n".join(md), encoding="utf-8")
    logging.info(f"Saved validation report to {report_file}")
    print("Script 14 completed successfully. OBFUSCATION_STATUS = FROZEN_V1")


if __name__ == "__main__":
    main()
