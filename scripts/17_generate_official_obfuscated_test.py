"""Stage 8: Phase 17 - Generate Official Paired Obfuscated Test Sets.

Applies the Frozen Stage 7 Obfuscation Engine (src.obfuscation.obfuscate)
to the Frozen Normal Test Anchor (data/processed/test_normal_v1.csv, 4,116 records).

Generates 8 conditions (4 families x 2 severities):
- O1_MILD.csv, O1_STRONG.csv
- O2_MILD.csv, O2_STRONG.csv
- O3_MILD.csv, O3_STRONG.csv
- O4_MILD.csv, O4_STRONG.csv

Also generates:
- condition_manifest.csv (Paired evaluation map)
- obfuscation_statistics_v1.csv (Transformation & success rate statistics)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.obfuscation import SEED, obfuscate

Path(REPO_ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO_ROOT / "logs" / "17_generate_official_obfuscated_test.log", mode="w", encoding="utf-8")
    ]
)

CONDITIONS = [
    ("O1_CHAR_SUBSTITUTION", "MILD", "O1_MILD"),
    ("O1_CHAR_SUBSTITUTION", "STRONG", "O1_STRONG"),
    ("O2_CHAR_INSERT_DELETE", "MILD", "O2_MILD"),
    ("O2_CHAR_INSERT_DELETE", "STRONG", "O2_STRONG"),
    ("O3_WHITESPACE", "MILD", "O3_MILD"),
    ("O3_WHITESPACE", "STRONG", "O3_STRONG"),
    ("O4_UNICODE_ORTHOGRAPHIC", "MILD", "O4_MILD"),
    ("O4_UNICODE_ORTHOGRAPHIC", "STRONG", "O4_STRONG"),
]


def main():
    logging.info("Starting Phase 17: Generate Official Obfuscated Test Sets (Stage 8)...")
    
    test_normal_path = REPO_ROOT / "data" / "processed" / "test_normal_v1.csv"
    assert test_normal_path.exists(), f"Frozen normal test missing: {test_normal_path}"
    
    test_normal_df = pd.read_csv(test_normal_path, low_memory=False)
    logging.info(f"Loaded Frozen Normal Test: {len(test_normal_df):,} records")
    assert len(test_normal_df) == 4116, f"Expected 4,116 test records, got {len(test_normal_df)}"
    
    out_dir = REPO_ROOT / "data" / "processed" / "obfuscated_test_v1"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    stats_list = []
    manifest_rows = []
    
    for family, severity, cond_filename in CONDITIONS:
        logging.info(f"Generating condition: {cond_filename} ({family} - {severity})...")
        cond_rows = []
        n_successful = 0
        n_no_target = 0
        
        for idx, row in test_normal_df.iterrows():
            rec_id = str(row["source_record_id"])
            orig_text = str(row["text_original"]) if pd.notna(row["text_original"]) else ""
            canon_label = int(row["canonical_label"])
            src_dataset = str(row["source_dataset"])
            
            # Apply frozen generator
            res = obfuscate(
                text=orig_text,
                source_record_id=rec_id,
                family=family,
                severity=severity,
                seed=SEED
            )
            
            pair_id = f"PAIR_{cond_filename}_{rec_id}"
            
            if res.changed:
                n_successful += 1
            else:
                n_no_target += 1
                
            cond_rows.append({
                "pair_id": pair_id,
                "source_record_id": rec_id,
                "canonical_label": canon_label,
                "source_dataset": src_dataset,
                "text_original": orig_text,
                "text_obfuscated": res.text_obfuscated,
                "family": family,
                "severity": severity,
                "seed": SEED,
                "changed": res.changed,
                "status": res.status,
                "modified_char_count": res.modified_char_count,
                "modified_char_ratio": round(res.modified_char_ratio, 6),
                "modified_token_count": res.modified_token_count,
            })
            
            manifest_rows.append({
                "condition_id": cond_filename,
                "pair_id": pair_id,
                "source_record_id": rec_id,
                "canonical_label": canon_label,
                "source_dataset": src_dataset,
                "changed": res.changed,
                "status": res.status,
                "is_evaluable_pair": res.changed
            })
            
        cond_df = pd.DataFrame(cond_rows)
        cond_file_path = out_dir / f"{cond_filename}.csv"
        cond_df.to_csv(cond_file_path, index=False, encoding="utf-8")
        
        success_rate = round(n_successful / len(test_normal_df) * 100, 2)
        condition_status = "READY" if success_rate >= 90.0 else "REVIEW_REQUIRED"
        
        logging.info(
            f"Saved {cond_file_path.name}: {len(cond_df):,} rows | "
            f"Changed: {n_successful:,} ({success_rate}%) | "
            f"No Target: {n_no_target:,} | Status: {condition_status}"
        )
        
        stats_list.append({
            "condition_id": cond_filename,
            "family": family,
            "severity": severity,
            "total_test_records": len(test_normal_df),
            "successful_transformations": n_successful,
            "no_eligible_target": n_no_target,
            "success_rate_pct": success_rate,
            "threshold_met_ge_90pct": (success_rate >= 90.0),
            "condition_status": condition_status
        })
        
    # Save Condition Manifest
    manifest_df = pd.DataFrame(manifest_rows)
    manifest_path = out_dir / "condition_manifest.csv"
    manifest_df.to_csv(manifest_path, index=False, encoding="utf-8")
    logging.info(f"Saved condition manifest to {manifest_path} ({len(manifest_df):,} rows)")
    
    # Save Obfuscation Statistics
    stats_df = pd.DataFrame(stats_list)
    stats_path = out_dir / "obfuscation_statistics_v1.csv"
    stats_df.to_csv(stats_path, index=False, encoding="utf-8")
    logging.info(f"Saved obfuscation statistics to {stats_path}")
    
    all_ready = (stats_df["condition_status"] == "READY").all()
    overall_status = "READY" if all_ready else "REVIEW_REQUIRED"
    logging.info(f"Phase 17 complete. OBFUSCATED_TEST_STATUS = {overall_status}")
    print(f"Phase 17 completed successfully. Overall Obfuscated Test Status: {overall_status}")


if __name__ == "__main__":
    main()
