"""Stage 8: Phase 16 - Validate Experimental Split.

Validates all 8 Hard Assertions:
ASSERT 1: train + val + test == 41,152
ASSERT 2: record_id overlap exists == 0 (strictly disjoint)
ASSERT 3: leakage_group_id overlap exists == 0 (strictly disjoint)
ASSERT 4: duplicate leakage group exists across partitions == 0
ASSERT 5: invalid label exists == 0 (all canonical labels in {0, 1})
ASSERT 6: review record enters any partition == 0
ASSERT 7: source main pool hash changed == False
ASSERT 8: same source_row_id maps to multiple inconsistent records == 0

Diagnostics:
- Source dataset composition per partition
- Author overlap diagnostic (data/audit/author_overlap_diagnostic_v1.md)

Outputs:
- data/processed/test_normal_v1.csv (Snapshot of frozen normal test anchor)
- data/splits/v1/split_validation_report_v1.md
"""

from __future__ import annotations

import hashlib
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

Path(REPO_ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO_ROOT / "logs" / "16_validate_experimental_split.log", mode="w", encoding="utf-8")
    ]
)


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    logging.info("Starting Phase 16: Validate Experimental Split (Stage 8)...")
    
    splits_dir = REPO_ROOT / "data" / "splits" / "v1"
    train_path = splits_dir / "train_v1.csv"
    val_path = splits_dir / "validation_v1.csv"
    test_path = splits_dir / "test_v1.csv"
    manifest_path = splits_dir / "split_manifest_v1.json"
    main_pool_path = REPO_ROOT / "data" / "processed" / "main_pool_candidate_v2.csv"
    review_queue_path = REPO_ROOT / "data" / "review" / "label_review_queue_v2.csv"
    
    assert train_path.exists(), f"Train file missing: {train_path}"
    assert val_path.exists(), f"Val file missing: {val_path}"
    assert test_path.exists(), f"Test file missing: {test_path}"
    assert manifest_path.exists(), f"Manifest file missing: {manifest_path}"
    assert main_pool_path.exists(), f"Main pool missing: {main_pool_path}"
    assert review_queue_path.exists(), f"Review queue missing: {review_queue_path}"
    
    # Load manifest
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    # ASSERT 7: source main pool hash changed
    curr_main_hash = compute_sha256(main_pool_path)
    assert curr_main_hash == manifest["hashes_sha256"]["source_main_pool"], (
        f"ASSERT 7 FAILED: Main pool hash changed! Current: {curr_main_hash}, Expected: {manifest['hashes_sha256']['source_main_pool']}"
    )
    logging.info("[ASSERT 7 PASSED] Source main pool hash matches manifest.")
    
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)
    review_df = pd.read_csv(review_queue_path)
    
    # ASSERT 1: train + val + test == 41,152
    total_split_rows = len(train_df) + len(val_df) + len(test_df)
    assert total_split_rows == 41152, f"ASSERT 1 FAILED: Expected 41,152 rows, got {total_split_rows}"
    logging.info(f"[ASSERT 1 PASSED] Row counts: Train={len(train_df):,}, Val={len(val_df):,}, Test={len(test_df):,} (Total = 41,152).")
    
    # ASSERT 2: record_id disjointness
    train_ids = set(train_df["record_id"])
    val_ids = set(val_df["record_id"])
    test_ids = set(test_df["record_id"])
    assert train_ids.isdisjoint(val_ids), "ASSERT 2 FAILED: record_id overlap between train and val!"
    assert train_ids.isdisjoint(test_ids), "ASSERT 2 FAILED: record_id overlap between train and test!"
    assert val_ids.isdisjoint(test_ids), "ASSERT 2 FAILED: record_id overlap between val and test!"
    assert len(train_ids | val_ids | test_ids) == 41152, "ASSERT 2 FAILED: record_ids union != 41,152!"
    logging.info("[ASSERT 2 PASSED] record_id is 100% strictly disjoint across partitions.")
    
    # ASSERT 3 & ASSERT 4: leakage_group_id disjointness
    train_lg = set(train_df["leakage_group_id"])
    val_lg = set(val_df["leakage_group_id"])
    test_lg = set(test_df["leakage_group_id"])
    assert train_lg.isdisjoint(val_lg), "ASSERT 3/4 FAILED: leakage_group_id overlap between train and val!"
    assert train_lg.isdisjoint(test_lg), "ASSERT 3/4 FAILED: leakage_group_id overlap between train and test!"
    assert val_lg.isdisjoint(test_lg), "ASSERT 3/4 FAILED: leakage_group_id overlap between val and test!"
    logging.info("[ASSERT 3 & 4 PASSED] leakage_group_id is 100% strictly disjoint across all partitions.")
    
    # ASSERT 5: labels valid and promotion exists in all partitions
    for name, d in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        assert set(d["canonical_label"].unique()).issubset({0, 1}), f"ASSERT 5 FAILED: Invalid labels in {name}!"
        prom_count = (d["canonical_label"] == 1).sum()
        non_prom_count = (d["canonical_label"] == 0).sum()
        assert prom_count > 0, f"ASSERT 5 FAILED: Zero promotion in {name}!"
        assert non_prom_count > 0, f"ASSERT 5 FAILED: Zero non-promotion in {name}!"
        logging.info(f"[ASSERT 5 PASSED] {name} label distribution: Promotion={prom_count:,}, Non-Promotion={non_prom_count:,}")
        
    # ASSERT 6: review records never enter any partition
    review_edg = set(review_df["exact_duplicate_group"].dropna())
    review_records = set(review_df["record_id"].dropna())
    for name, d in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        overlap_edg = set(d["exact_duplicate_group"]).intersection(review_edg)
        overlap_rec = set(d["record_id"]).intersection(review_records)
        assert len(overlap_edg) == 0, f"ASSERT 6 FAILED: Review exact_duplicate_group leaked into {name}: {overlap_edg}"
        assert len(overlap_rec) == 0, f"ASSERT 6 FAILED: Review record_id leaked into {name}: {overlap_rec}"
    logging.info("[ASSERT 6 PASSED] Zero review records leaked into any partition.")
    
    # ASSERT 8: same source_row_id consistency
    all_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    src_dups = all_df.duplicated(subset=["source_dataset", "source_row_id"], keep=False)
    assert src_dups.sum() == 0, f"ASSERT 8 FAILED: Duplicate (source_dataset, source_row_id) found in splits: {src_dups.sum()}"
    logging.info("[ASSERT 8 PASSED] Every (source_dataset, source_row_id) is unique and consistent.")
    
    # Check DS3 and DS5 isolation
    allowed_sources = {"DS1_fahruu", "DS2_kyyyy8_all", "DS4_kyyyy8_platform"}
    actual_sources = set(all_df["source_dataset"].unique())
    assert actual_sources.issubset(allowed_sources), f"Unallowed source datasets found: {actual_sources - allowed_sources}"
    logging.info(f"[SOURCE ISOLATION PASSED] Allowed sources verified: {actual_sources}")
    
    # Source distribution per partition
    source_stats = []
    for split_name, s_df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        for src, count in s_df["source_dataset"].value_counts().items():
            prom = int(((s_df["source_dataset"] == src) & (s_df["canonical_label"] == 1)).sum())
            non_prom = int(((s_df["source_dataset"] == src) & (s_df["canonical_label"] == 0)).sum())
            source_stats.append({
                "partition": split_name,
                "source_dataset": src,
                "count": count,
                "pct_of_partition": round(count / len(s_df) * 100, 2),
                "promotion_count": prom,
                "non_promotion_count": non_prom,
                "promotion_rate_pct": round(prom / count * 100, 2)
            })
    source_stats_df = pd.DataFrame(source_stats)
    logging.info(f"Source distribution:\n{source_stats_df.to_string(index=False)}")
    
    # Author Overlap Diagnostic (Section 13)
    train_authors = set(train_df["author"].dropna().astype(str).str.strip()) - {"", "nan", "None"}
    val_authors = set(val_df["author"].dropna().astype(str).str.strip()) - {"", "nan", "None"}
    test_authors = set(test_df["author"].dropna().astype(str).str.strip()) - {"", "nan", "None"}
    
    train_val_author_overlap = train_authors.intersection(val_authors)
    train_test_author_overlap = train_authors.intersection(test_authors)
    val_test_author_overlap = val_authors.intersection(test_authors)
    
    diag_path = REPO_ROOT / "data" / "audit" / "author_overlap_diagnostic_v1.md"
    diag_content = f"""# AUTHOR OVERLAP DIAGNOSTIC REPORT v1

**Stage 8: Group-Aware Split Diagnostic Analysis**
- **Date**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
- **Methodology Rule**: Diagnostic only (Author is NOT a hard grouping constraint due to non-equivalent metadata across source datasets).

---

## 1. Author Metadata Inventory
- **Train Distinct Authors**: `{len(train_authors):,}`
- **Validation Distinct Authors**: `{len(val_authors):,}`
- **Test Distinct Authors**: `{len(test_authors):,}`

---

## 2. Cross-Partition Author Overlap Diagnostics
| Partition Pair | Overlapping Authors Count | Overlap % (relative to smaller partition) |
| --- | --- | --- |
| Train ∩ Validation | `{len(train_val_author_overlap):,}` | `{round(len(train_val_author_overlap) / max(1, len(val_authors)) * 100, 2)}%` |
| Train ∩ Test | `{len(train_test_author_overlap):,}` | `{round(len(train_test_author_overlap) / max(1, len(test_authors)) * 100, 2)}%` |
| Validation ∩ Test | `{len(val_test_author_overlap):,}` | `{round(len(val_test_author_overlap) / max(1, min(len(val_authors), len(test_authors))) * 100, 2)}%` |

---

## 3. Analysis & Methodological Note
- The primary hard constraint is `leakage_group_id` (which clusters exact duplicates, whitespace variants, normalized text, and near-duplicate templates with 100% strict disjointness).
- Author metadata varies widely across raw YouTube crawls (e.g. anonymous/random channel handles vs bot networks). Because bots deliberately use multiple distinct burner accounts to post identical templates, `leakage_group_id` provides superior protection against data leakage compared to author identifiers.
- The author overlap is documented here as an empirical diagnostic and does not violate the primary grouping rule.
"""
    diag_path.write_text(diag_content, encoding="utf-8")
    logging.info(f"Saved author overlap diagnostic to {diag_path}")
    
    # Freeze Test Set Snapshot (Section 20)
    # File: data/processed/test_normal_v1.csv
    test_normal_path = REPO_ROOT / "data" / "processed" / "test_normal_v1.csv"
    test_normal_df = test_df.copy()
    test_normal_df = test_normal_df.rename(columns={
        "record_id": "source_record_id",
        "text_raw": "text_original"
    })
    # Keep key columns first
    leading_cols = ["source_record_id", "text_original", "canonical_label", "source_dataset", "leakage_group_id"]
    other_cols = [c for c in test_normal_df.columns if c not in leading_cols]
    test_normal_df = test_normal_df[leading_cols + other_cols]
    
    test_normal_df.to_csv(test_normal_path, index=False, encoding="utf-8")
    test_normal_sha = compute_sha256(test_normal_path)
    logging.info(f"Created Frozen Normal Test Snapshot: {test_normal_path} ({len(test_normal_df):,} rows)")
    logging.info(f"Frozen Normal Test SHA-256: {test_normal_sha}")
    
    # Save Split Validation Report
    report_path = splits_dir / "split_validation_report_v1.md"
    report_content = f"""# SPLIT VALIDATION REPORT v1

**Stage 8: Final Experimental Lock - Group-Aware Split Validation**
- **Date**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
- **Split Directory**: `data/splits/v1/`
- **Main Pool**: `data/processed/main_pool_candidate_v2.csv` (SHA-256: `{curr_main_hash}`)
- **Normal Test Freeze**: `data/processed/test_normal_v1.csv` (SHA-256: `{test_normal_sha}`)

---

## 1. Hard Assertions Status
| Assertion | Description | Status |
| --- | --- | --- |
| ASSERT 1 | Total rows across partitions == 41,152 | PASS |
| ASSERT 2 | Exact record_id disjointness across Train, Val, Test | PASS |
| ASSERT 3 | Strict leakage_group_id disjointness (Train ∩ Val = 0) | PASS |
| ASSERT 4 | Strict leakage_group_id disjointness (Train ∩ Test = 0, Val ∩ Test = 0) | PASS |
| ASSERT 5 | Valid canonical labels (both classes > 0 in all partitions) | PASS |
| ASSERT 6 | Complete isolation of label review queue records (0 leakage) | PASS |
| ASSERT 7 | Source main pool SHA-256 hash verified unchanged | PASS |
| ASSERT 8 | Unique and consistent (source_dataset, source_row_id) mappings | PASS |

---

## 2. Partition Summary
- **Train Set (v1)**: `{len(train_df):,}` rows (Promotion: `{(train_df["canonical_label"] == 1).sum():,}`, Non-Promotion: `{(train_df["canonical_label"] == 0).sum():,}`)
- **Validation Set (v1)**: `{len(val_df):,}` rows (Promotion: `{(val_df["canonical_label"] == 1).sum():,}`, Non-Promotion: `{(val_df["canonical_label"] == 0).sum():,}`)
- **Test Set (v1)**: `{len(test_df):,}` rows (Promotion: `{(test_df["canonical_label"] == 1).sum():,}`, Non-Promotion: `{(test_df["canonical_label"] == 0).sum():,}`)

---

## 3. Decision
**SPLIT_STATUS: VALIDATED_AND_FROZEN ✅**
"""
    report_path.write_text(report_content, encoding="utf-8")
    logging.info(f"Saved split validation report to {report_path}")
    print("Phase 16 completed successfully. Experimental Split Validated and Normal Test Frozen.")


if __name__ == "__main__":
    main()
