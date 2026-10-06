import os
import sys
import hashlib
import logging
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to sys.path
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
    filename="logs/08_validate_and_rebuild_overlap.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

DATASETS = [
    "DS1_fahruu",
    "DS2_kyyyy8_all",
    "DS3_yaemico",
    "DS4_kyyyy8_platform",
    "DS5_ferdiansakti"
]

def check_raw_integrity():
    logging.info("Memeriksa integritas SHA-256 raw dataset...")
    manifest_path = Path("data/manifests/raw_file_manifest.csv")
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest tidak ditemukan: {manifest_path}")
        
    manifest = pd.read_csv(manifest_path)
    rows = []
    for _, r in manifest.iterrows():
        p = Path(r["raw_storage_path"])
        exp = r["sha256_checksum"]
        act = hashlib.sha256(p.read_bytes()).hexdigest()
        status = "PASS" if exp == act else "FAIL"
        rows.append({
            "source_dataset": r["source_id"],
            "path": r["raw_storage_path"],
            "expected_sha256": exp,
            "actual_sha256": act,
            "status": status
        })
        
    res_df = pd.DataFrame(rows)
    res_df.to_csv("data/audit/raw_integrity_check_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/raw_integrity_check_v2.csv")
    
    assert (res_df["status"] == "PASS").all(), "Raw file integrity check FAILED!"
    logging.info("Raw integrity check: 100% PASS.")

def main():
    logging.info("Memulai Phase: Validate & Rebuild Overlap and Conflicts (v2)")
    
    # 1. Raw Integrity Check
    check_raw_integrity()
    
    # 2. Load interim harmonized datasets
    logging.info("Loading 5 interim harmonized datasets...")
    files = [
        "data/interim/ds1_harmonized.csv",
        "data/interim/ds2_harmonized.csv",
        "data/interim/ds3_harmonized.csv",
        "data/interim/ds4_harmonized.csv",
        "data/interim/ds5_harmonized.csv"
    ]
    dfs = [pd.read_csv(f, dtype=str) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    logging.info(f"Loaded {len(df):,} total records.")
    
    # 3. Compute Hashes using single source of truth
    logging.info("Computing exact, whitespace, normalized, and alnum hashes...")
    df["exact_hash"] = df["text_raw"].apply(compute_exact_hash)
    df["ws_hash"] = df["text_raw"].apply(compute_whitespace_hash)
    df["norm_hash"] = df["text_raw"].apply(compute_normalized_hash)
    df["alnum_hash"] = df["text_raw"].apply(compute_alnum_hash)
    
    df["exact_duplicate_group"] = df["exact_hash"].apply(lambda h: f"EDG_{h[:12]}" if h != "NULL_HASH" else None)
    df["whitespace_duplicate_group"] = df["ws_hash"].apply(lambda h: f"WDG_{h[:12]}" if h != "NULL_HASH" else None)
    df["normalized_variant_group"] = df["norm_hash"].apply(lambda h: f"NVG_{h[:12]}" if h != "NULL_HASH" else None)
    
    # 4. Pairwise Overlap Recomputation
    logging.info("Computing pairwise overlap for all 10 dataset pairs...")
    overlap_rows = []
    
    for i in range(len(DATASETS)):
        ds_a = DATASETS[i]
        sub_a = df[df["source_dataset"] == ds_a].drop_duplicates("exact_hash")
        
        for j in range(i + 1, len(DATASETS)):
            ds_b = DATASETS[j]
            sub_b = df[df["source_dataset"] == ds_b].drop_duplicates("exact_hash")
            
            # Exact shared groups: exact hashes present in both A and B
            exact_a = set(sub_a["exact_hash"]) - {"NULL_HASH"}
            exact_b = set(sub_b["exact_hash"]) - {"NULL_HASH"}
            shared_exact_groups = len(exact_a.intersection(exact_b))
            
            # Whitespace shared groups: EDGs in (A U B) matching on ws_hash
            ws_a = set(sub_a["ws_hash"]) - {"NULL_HASH"}
            ws_b = set(sub_b["ws_hash"]) - {"NULL_HASH"}
            a_in_b_ws = set(sub_a[sub_a["ws_hash"].isin(ws_b)]["exact_hash"])
            b_in_a_ws = set(sub_b[sub_b["ws_hash"].isin(ws_a)]["exact_hash"])
            shared_ws_groups = len(a_in_b_ws.union(b_in_a_ws))
            
            # Normalized shared groups: EDGs in (A U B) matching on norm_hash
            norm_a = set(sub_a["norm_hash"]) - {"NULL_HASH"}
            norm_b = set(sub_b["norm_hash"]) - {"NULL_HASH"}
            a_in_b_norm = set(sub_a[sub_a["norm_hash"].isin(norm_b)]["exact_hash"])
            b_in_a_norm = set(sub_b[sub_b["norm_hash"].isin(norm_a)]["exact_hash"])
            shared_norm_groups = len(a_in_b_norm.union(b_in_a_norm))
            
            # Alnum shared groups: EDGs in (A U B) matching on alnum_hash
            alnum_a = set(sub_a["alnum_hash"]) - {"NULL_HASH", "EMPTY_ALNUM_HASH"}
            alnum_b = set(sub_b["alnum_hash"]) - {"NULL_HASH", "EMPTY_ALNUM_HASH"}
            a_in_b_alnum = set(sub_a[sub_a["alnum_hash"].isin(alnum_b)]["exact_hash"])
            b_in_a_alnum = set(sub_b[sub_b["alnum_hash"].isin(alnum_a)]["exact_hash"])
            shared_alnum_groups = len(a_in_b_alnum.union(b_in_a_alnum))
            
            # Direct hash intersections for complete diagnostic reporting
            raw_shared_ws_hashes = len(ws_a.intersection(ws_b))
            raw_shared_norm_hashes = len(norm_a.intersection(norm_b))
            raw_shared_alnum_hashes = len(alnum_a.intersection(alnum_b))
            
            # Strict mathematical assertion
            assert shared_exact_groups <= shared_ws_groups <= shared_norm_groups <= shared_alnum_groups, (
                f"Monotonicity violation between {ds_a} and {ds_b}: "
                f"exact={shared_exact_groups}, ws={shared_ws_groups}, norm={shared_norm_groups}, alnum={shared_alnum_groups}"
            )
            
            # Label conflicts between this pair
            pair_exact = exact_a.intersection(exact_b)
            pair_conflicts = 0
            if pair_exact:
                merged = pd.merge(
                    sub_a[sub_a["exact_hash"].isin(pair_exact)][["exact_hash", "source_label"]].drop_duplicates(),
                    sub_b[sub_b["exact_hash"].isin(pair_exact)][["exact_hash", "source_label"]].drop_duplicates(),
                    on="exact_hash", suffixes=("_a", "_b")
                )
                pair_conflicts = len(merged[merged["source_label_a"] != merged["source_label_b"]]["exact_hash"].unique())
                
            notes = []
            if ds_a in ("DS2_kyyyy8_all", "DS4_kyyyy8_platform") and ds_b in ("DS2_kyyyy8_all", "DS4_kyyyy8_platform"):
                notes.append(f"Kyyyy8 Lineage (overlap masif {shared_exact_groups:,} teks, {pair_conflicts} konflik label)")
            elif pair_conflicts > 0:
                notes.append(f"Terdapat {pair_conflicts} konflik label")
            elif shared_exact_groups > 0:
                notes.append(f"Shared {shared_exact_groups:,} teks persis")
            else:
                notes.append("Tidak ada irisan teks persis")
                
            overlap_rows.append({
                "dataset_a": ds_a,
                "dataset_b": ds_b,
                "shared_exact_groups": shared_exact_groups,
                "shared_whitespace_groups": shared_ws_groups,
                "shared_normalized_groups": shared_norm_groups,
                "shared_alnum_groups": shared_alnum_groups,
                "unique_ws_hashes_shared": raw_shared_ws_hashes,
                "unique_norm_hashes_shared": raw_shared_norm_hashes,
                "unique_alnum_hashes_shared": raw_shared_alnum_hashes,
                "pair_label_conflicts": pair_conflicts,
                "monotonicity_status": "PASS",
                "notes": "; ".join(notes)
            })
            
    overlap_df = pd.DataFrame(overlap_rows)
    overlap_df.to_csv("data/audit/cross_dataset_overlap_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/cross_dataset_overlap_v2.csv (All 10 pairs PASS monotonicity assertion).")
    
    # 5. Conflict Analysis (Within vs Cross Dataset)
    logging.info("Analyzing conflicts across full pool...")
    exact_groups = df.groupby("exact_hash")
    
    conflict_audit_rows = []
    
    # Load previously established adjudication decisions from data/audit/label_conflicts.csv
    prev_adj_df = pd.read_csv("data/audit/label_conflicts.csv")
    prev_adj = {}
    for _, r in prev_adj_df.drop_duplicates("exact_hash").iterrows():
        prev_adj[r["exact_hash"]] = {
            "canonical_label": r["canonical_label"],
            "label_status": r["label_status"],
            "decision": r["decision"],
            "reason": r["reason"],
            "note": r["adjudication_note"]
        }
    logging.info(f"Loaded {len(prev_adj)} previously adjudicated conflict decisions.")
    
    conflicting_text_groups = 0
    conflicting_record_rows = 0
    cross_conf_groups = 0
    within_conf_groups = 0
    
    for h, g in exact_groups:
        if h == "NULL_HASH":
            continue
            
        labels_all = g["source_label"].dropna().unique()
        if len(labels_all) > 1:
            conflicting_text_groups += 1
            conflicting_record_rows += len(g)
            
            # check within
            has_within = any(sub["source_label"].nunique() > 1 for _, sub in g.groupby("source_dataset"))
            
            # check cross
            ds_labels = {ds: set(sub["source_label"].dropna()) for ds, sub in g.groupby("source_dataset")}
            has_cross = False
            ds_keys = list(ds_labels.keys())
            for idx_a in range(len(ds_keys)):
                for idx_b in range(idx_a + 1, len(ds_keys)):
                    if ds_labels[ds_keys[idx_a]] != ds_labels[ds_keys[idx_b]]:
                        has_cross = True
                        break
                if has_cross: break
                
            if has_cross: cross_conf_groups += 1
            if has_within: within_conf_groups += 1
            
            adj = prev_adj.get(h)
            if not adj:
                raise ValueError(f"Unadjudicated conflict detected for hash {h}: {g['text_raw'].iloc[0]}")
                
            c_lbl = adj["canonical_label"]
            l_stat = adj["label_status"]
            dec = adj["decision"]
            
            datasets_present = ";".join(sorted(g["source_dataset"].unique()))
            labels_str = ";".join([f"{k}:{','.join(sorted(v))}" for k, v in ds_labels.items()])
            
            conflict_audit_rows.append({
                "exact_hash": h,
                "text_raw": g["text_raw"].iloc[0],
                "datasets_present": datasets_present,
                "source_record_count": len(g),
                "source_labels": labels_str,
                "cross_dataset_conflict": has_cross,
                "within_dataset_conflict": has_within,
                "global_conflict": True,
                "canonical_label": c_lbl,
                "label_status": l_stat,
                "adjudication_decision": dec,
                "adjudication_reason": adj["reason"],
                "adjudication_note": adj["note"]
            })
            
    conflict_df = pd.DataFrame(conflict_audit_rows)
    conflict_df.to_csv("data/audit/label_conflicts_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/audit/label_conflicts_v2.csv ({len(conflict_df)} groups).")
    
    # Conflict summary
    conflict_summary = pd.DataFrame([{
        "conflicting_text_groups": conflicting_text_groups,
        "conflicting_record_rows": conflicting_record_rows,
        "cross_dataset_conflicting_text_groups": cross_conf_groups,
        "within_dataset_conflicting_text_groups": within_conf_groups,
        "exclusively_cross_dataset_groups": cross_conf_groups - (cross_conf_groups + within_conf_groups - conflicting_text_groups),
        "exclusively_within_dataset_groups": within_conf_groups - (cross_conf_groups + within_conf_groups - conflicting_text_groups),
        "both_cross_and_within_groups": cross_conf_groups + within_conf_groups - conflicting_text_groups
    }])
    conflict_summary.to_csv("data/audit/conflict_summary_v2.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/conflict_summary_v2.csv")
    
    # Save checkpoint
    df.to_pickle("data/interim/full_pool_v2_hashed.pkl")
    logging.info("Saved data/interim/full_pool_v2_hashed.pkl")
    print("Script 08 completed successfully.")

if __name__ == "__main__":
    main()
