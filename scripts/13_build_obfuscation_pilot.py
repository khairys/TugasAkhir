"""Stage 7: Build Obfuscation Pilot Dataset and Human Review Queue.

Selects 200 deterministic pilot development records (100 Promotion, 100 Non-Promotion)
from data/processed/main_pool_candidate_v2.csv and generates 9 conditions:
NORMAL, O1 MILD/STRONG, O2 MILD/STRONG, O3 MILD/STRONG, O4 MILD/STRONG.
Total = 1,800 rows saved to data/interim/obfuscation_pilot_v1.csv.
Also creates balanced human review queue of 320 transformed samples in data/review/obfuscation_pilot_review_v1.csv.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
import pandas as pd

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.obfuscation import (
    SEED,
    FAMILIES,
    obfuscate,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO_ROOT / "logs" / "13_build_obfuscation_pilot.log", mode="w", encoding="utf-8")
    ]
)

CONDITIONS = [
    ("NORMAL", "NORMAL"),
    ("O1_CHAR_SUBSTITUTION", "MILD"),
    ("O1_CHAR_SUBSTITUTION", "STRONG"),
    ("O2_CHAR_INSERT_DELETE", "MILD"),
    ("O2_CHAR_INSERT_DELETE", "STRONG"),
    ("O3_WHITESPACE", "MILD"),
    ("O3_WHITESPACE", "STRONG"),
    ("O4_UNICODE_ORTHOGRAPHIC", "MILD"),
    ("O4_UNICODE_ORTHOGRAPHIC", "STRONG"),
]


def main():
    logging.info("Starting Phase 13: Build Obfuscation Pilot Dataset (Stage 7)...")
    
    # Ensure directories exist
    (REPO_ROOT / "data" / "interim").mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "data" / "review").mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "logs").mkdir(parents=True, exist_ok=True)
    
    main_pool_path = REPO_ROOT / "data" / "processed" / "main_pool_candidate_v2.csv"
    if not main_pool_path.exists():
        raise FileNotFoundError(f"Missing main pool file: {main_pool_path}")
        
    logging.info(f"Loading main pool from {main_pool_path}...")
    main_pool_df = pd.read_csv(main_pool_path, dtype={"canonical_label": int})
    logging.info(f"Loaded {len(main_pool_df):,} records from main pool.")
    
    # 1. Deterministic Sampling of 200 source records (100 Promotion, 100 Non-Promotion)
    prom_df = main_pool_df[main_pool_df["canonical_label"] == 1].sample(n=100, random_state=SEED)
    non_prom_df = main_pool_df[main_pool_df["canonical_label"] == 0].sample(n=100, random_state=SEED)
    
    pilot_source = pd.concat([prom_df, non_prom_df], ignore_index=True)
    pilot_source = pilot_source.sort_values("record_id").reset_index(drop=True)
    logging.info(f"Sampled {len(pilot_source)} source pilot records (100 Prom, 100 Non-Prom).")
    
    # 2. Generate 9 conditions for each source record (200 * 9 = 1,800 rows)
    pilot_rows = []
    
    for row in pilot_source.itertuples(index=False):
        rec_id = getattr(row, "record_id")
        src_ds = getattr(row, "source_dataset")
        canon_lbl = int(getattr(row, "canonical_label"))
        raw_text = str(getattr(row, "text_raw"))
        if pd.isna(raw_text):
            raw_text = ""
            
        for family, severity in CONDITIONS:
            pair_id = f"{rec_id}_{family}_{severity}"
            res = obfuscate(
                text=raw_text,
                source_record_id=rec_id,
                family=family,
                severity=severity,
                seed=SEED,
            )
            
            pilot_rows.append({
                "pair_id": pair_id,
                "source_record_id": rec_id,
                "source_dataset": src_ds,
                "canonical_label": canon_lbl,
                "family": family,
                "severity": severity,
                "seed": SEED,
                "text_original": raw_text,
                "text_obfuscated": res.text_obfuscated,
                "changed": res.changed,
                "status": res.status,
                "failure_reason": res.failure_reason if res.failure_reason else "",
                "modified_char_count": res.modified_char_count,
                "modified_char_ratio": res.modified_char_ratio,
                "modified_token_count": res.modified_token_count,
            })
            
    pilot_df = pd.DataFrame(pilot_rows)
    pilot_csv_path = REPO_ROOT / "data" / "interim" / "obfuscation_pilot_v1.csv"
    pilot_df.to_csv(pilot_csv_path, index=False, encoding="utf-8")
    logging.info(f"Saved {len(pilot_df):,} pilot rows to {pilot_csv_path}")
    
    # 3. Build Balanced Human Review Queue (Target = 320 samples)
    # Balanced across: 4 families * 2 severities * 2 labels * 20 samples = 320
    logging.info("Constructing balanced human review queue (320 samples)...")
    transformed_df = pilot_df[pilot_df["severity"] != "NORMAL"].copy()
    
    review_samples = []
    for family in FAMILIES:
        for severity in ("MILD", "STRONG"):
            for label in (0, 1):
                stratum = transformed_df[
                    (transformed_df["family"] == family) &
                    (transformed_df["severity"] == severity) &
                    (transformed_df["canonical_label"] == label)
                ]
                sample_n = min(20, len(stratum))
                sampled_stratum = stratum.sample(n=sample_n, random_state=SEED)
                review_samples.append(sampled_stratum)
                
    review_df = pd.concat(review_samples, ignore_index=True)
    # Sort deterministically
    review_df = review_df.sort_values(["family", "severity", "canonical_label", "source_record_id"]).reset_index(drop=True)
    
    # Format review queue columns
    review_df["review_id"] = [f"REV_{i+1:04d}" for i in range(len(review_df))]
    review_df["human_label_preserved"] = ""
    review_df["human_meaning_preserved"] = ""
    review_df["human_transformation_valid"] = ""
    review_df["review_notes"] = ""
    review_df["reviewer"] = ""
    review_df["review_status"] = "PENDING"
    
    review_cols = [
        "review_id",
        "source_record_id",
        "family",
        "severity",
        "canonical_label",
        "text_original",
        "text_obfuscated",
        "human_label_preserved",
        "human_meaning_preserved",
        "human_transformation_valid",
        "review_notes",
        "reviewer",
        "review_status",
    ]
    
    review_csv_path = REPO_ROOT / "data" / "review" / "obfuscation_pilot_review_v1.csv"
    review_df[review_cols].to_csv(review_csv_path, index=False, encoding="utf-8")
    logging.info(f"Saved {len(review_df):,} review samples to {review_csv_path}")
    print("Script 13 completed successfully.")


if __name__ == "__main__":
    main()
