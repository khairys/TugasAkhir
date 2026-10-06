import os
import sys
import re
import json
import logging
import hashlib
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/05_near_duplicates.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

def get_shingles(text):
    if not isinstance(text, str) or len(text) < 4:
        return set()
    words = text.lower().split()
    if len(words) >= 2:
        return set(f"{words[i]} {words[i+1]}" for i in range(len(words)-1))
    return {text.lower().strip()}

def main():
    logging.info("Memulai Phase 5: Near-Duplicate Clustering with MinHash, LSH & SciPy Graph")
    df = pd.read_pickle("data/interim/full_pool_adjudicated.pkl")
    
    # Work on unique normalized variant groups
    unique_norm = df[['normalized_variant_group', 'text_raw']].drop_duplicates('normalized_variant_group').copy()
    norm_groups = unique_norm['normalized_variant_group'].tolist()
    texts = unique_norm['text_raw'].tolist()
    N = len(norm_groups)
    logging.info(f"Unique Normalized Groups to cluster: {N:,}")
    
    all_shingles = [get_shingles(t) for t in texts]
    
    # Deterministic MinHash
    np.random.seed(42)
    num_perm = 64
    p = 4294967311 # prime > 2^32
    a = np.random.randint(1, p, size=num_perm, dtype=np.int64)
    b = np.random.randint(0, p, size=num_perm, dtype=np.int64)
    
    shingle_hash_cache = {}
    def hash_shingle(s):
        if s not in shingle_hash_cache:
            shingle_hash_cache[s] = int(hashlib.md5(s.encode('utf-8')).hexdigest()[:8], 16)
        return shingle_hash_cache[s]
        
    signatures = np.full((N, num_perm), fill_value=p, dtype=np.int64)
    for idx, sset in enumerate(all_shingles):
        if not sset:
            continue
        hvals = np.array([hash_shingle(s) for s in sset], dtype=np.int64)
        sig = ((a[:, None] * hvals[None, :] + b[:, None]) % p).min(axis=1)
        signatures[idx] = sig
        
    logging.info("Calculated MinHash signatures.")
    
    # LSH Banding
    b_count = 16
    r_count = 4
    buckets = defaultdict(list)
    for doc_id in range(N):
        if not all_shingles[doc_id]: continue
        for band_idx in range(b_count):
            band = tuple(signatures[doc_id, band_idx*r_count : (band_idx+1)*r_count])
            buckets[(band_idx, band)].append(doc_id)
            
    candidate_pairs = set()
    for b_key, doc_list in buckets.items():
        if 1 < len(doc_list) < 200:
            for i in range(len(doc_list)):
                for j in range(i+1, len(doc_list)):
                    d1, d2 = doc_list[i], doc_list[j]
                    if d1 > d2: d1, d2 = d2, d1
                    candidate_pairs.add((d1, d2))
                    
    logging.info(f"Evaluated {len(candidate_pairs):,} candidate pairs from LSH.")
    
    # Verify candidate pairs with Jaccard >= 0.65
    verified_edges = []
    for d1, d2 in candidate_pairs:
        s1, s2 = all_shingles[d1], all_shingles[d2]
        union_len = len(s1.union(s2))
        if union_len > 0:
            jaccard = len(s1.intersection(s2)) / union_len
            if jaccard >= 0.65:
                verified_edges.append((d1, d2))
                
    logging.info(f"Verified {len(verified_edges):,} near-duplicate edges.")
    
    # Build graph using SciPy
    if verified_edges:
        rows = [e[0] for e in verified_edges]
        cols = [e[1] for e in verified_edges]
        data = np.ones(len(verified_edges), dtype=int)
        adj_matrix = csr_matrix((data, (rows, cols)), shape=(N, N))
    else:
        adj_matrix = csr_matrix((N, N))
        
    n_components, labels = connected_components(adj_matrix, directed=False)
    logging.info(f"Connected components computed: {n_components:,} distinct template families.")
    
    # Map cluster labels to clean IDs
    norm_to_ndg = {norm_groups[i]: f"NDG_{labels[i]+1:06d}" for i in range(N)}
    
    # Assign near_duplicate_group to full dataframe
    df["near_duplicate_group"] = df["normalized_variant_group"].map(norm_to_ndg)
    
    total_ndg = df["near_duplicate_group"].nunique()
    logging.info(f"Total Near-Duplicate Groups generated: {total_ndg:,}")
    
    # Save checkpoint
    df.to_pickle("data/interim/full_pool_clustered.pkl")
    logging.info("Saved data/interim/full_pool_clustered.pkl")
    print("Near-duplicate clustering completed successfully.")

if __name__ == "__main__":
    main()
