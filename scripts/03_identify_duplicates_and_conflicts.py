import os
import sys
import re
import hashlib
import unicodedata
import logging
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/03_duplicates_and_conflicts.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

def compute_hashes(text):
    if not isinstance(text, str) or pd.isna(text):
        return "NULL_HASH", "NULL_HASH", "NULL_HASH"
    
    # 1. Exact raw hash
    h_exact = hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    # 2. Whitespace collapsed hash
    t_ws = re.sub(r'\s+', ' ', text).strip()
    h_ws = hashlib.sha256(t_ws.encode('utf-8')).hexdigest()
    
    # 3. Unicode NFKC lowercase normalized hash (for audit grouping)
    t_norm = unicodedata.normalize('NFKC', text).lower().strip()
    t_norm = re.sub(r'\s+', ' ', t_norm)
    h_norm = hashlib.sha256(t_norm.encode('utf-8')).hexdigest()
    
    return h_exact, h_ws, h_norm

def main():
    logging.info("Memulai Phase 3: Exact, Whitespace, & Unicode Hashing & Conflict Detection")
    
    files = [
        "data/interim/ds1_harmonized.csv",
        "data/interim/ds2_harmonized.csv",
        "data/interim/ds3_harmonized.csv",
        "data/interim/ds4_harmonized.csv",
        "data/interim/ds5_harmonized.csv"
    ]
    
    dfs = [pd.read_csv(f, dtype=str) for f in files]
    full_df = pd.concat(dfs, ignore_index=True)
    logging.info(f"Loaded {len(full_df):,} total interim records.")
    
    # Compute hashes
    exact_hashes = []
    ws_hashes = []
    norm_hashes = []
    
    for text in full_df["text_raw"]:
        h_e, h_w, h_n = compute_hashes(text)
        exact_hashes.append(h_e)
        ws_hashes.append(h_w)
        norm_hashes.append(h_n)
        
    full_df["exact_hash"] = exact_hashes
    full_df["ws_hash"] = ws_hashes
    full_df["norm_hash"] = norm_hashes
    
    full_df["exact_duplicate_group"] = full_df["exact_hash"].apply(lambda h: f"EDG_{h[:12]}" if h != "NULL_HASH" else None)
    full_df["whitespace_duplicate_group"] = full_df["ws_hash"].apply(lambda h: f"WDG_{h[:12]}" if h != "NULL_HASH" else None)
    full_df["normalized_variant_group"] = full_df["norm_hash"].apply(lambda h: f"NVG_{h[:12]}" if h != "NULL_HASH" else None)
    
    # Duplicate frequency calculations
    exact_counts = full_df["exact_hash"].value_counts()
    full_df["exact_freq"] = full_df["exact_hash"].map(exact_counts)
    full_df["is_exact_duplicate"] = full_df["exact_freq"] > 1
    
    # Cross dataset duplicate check
    hash_sources = full_df.groupby("exact_hash")["source_dataset"].unique()
    hash_sources_count = hash_sources.apply(len)
    full_df["sources_count"] = full_df["exact_hash"].map(hash_sources_count)
    full_df["is_cross_dataset_duplicate"] = full_df["sources_count"] > 1
    
    # Cross dataset sources string
    hash_sources_str = hash_sources.apply(lambda arr: ";".join(sorted(arr)))
    full_df["cross_dataset_sources"] = full_df["exact_hash"].map(hash_sources_str)
    
    # Label conflict detection per exact hash
    hash_labels = full_df.groupby("exact_hash")["source_label"].unique()
    hash_labels_count = hash_labels.apply(len)
    full_df["label_conflict_count"] = full_df["exact_hash"].map(hash_labels_count)
    full_df["is_label_conflict"] = full_df["label_conflict_count"] > 1
    
    n_exact_groups = full_df["exact_duplicate_group"].nunique()
    n_exact_dups = full_df["is_exact_duplicate"].sum()
    n_cross_dups = full_df["is_cross_dataset_duplicate"].sum()
    n_conflicts = full_df["is_label_conflict"].sum()
    n_conflict_unique_texts = full_df[full_df["is_label_conflict"]]["exact_hash"].nunique()
    
    logging.info(f"Unique Exact Duplicate Groups (Unique Texts): {n_exact_groups:,}")
    logging.info(f"Total Exact Duplicate Records: {n_exact_dups:,}")
    logging.info(f"Total Cross-Dataset Duplicate Records: {n_cross_dups:,}")
    logging.info(f"Records with Label Conflict: {n_conflicts:,} (across {n_conflict_unique_texts} unique texts)")
    
    # Save checkpoint
    full_df.to_csv("data/interim/full_pool_hashed.csv", index=False, encoding="utf-8")
    full_df.to_pickle("data/interim/full_pool_hashed.pkl")
    logging.info("Saved data/interim/full_pool_hashed.csv and .pkl")

if __name__ == "__main__":
    main()
