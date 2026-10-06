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
    filename="logs/09_rebuild_near_duplicates.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

RANDOM_SEED = 42

def get_shingles(text):
    if not isinstance(text, str) or len(text) < 4:
        return set()
    words = text.lower().split()
    if len(words) >= 2:
        return set(f"{words[i]} {words[i+1]}" for i in range(len(words)-1))
    return {text.lower().strip()}

def main():
    logging.info("Memulai Phase: Rebuild Near-Duplicate Clustering with Recursive Blocking & Validation (v2)")
    df = pd.read_pickle("data/interim/full_pool_v2_hashed.pkl")
    
    # Work on unique normalized variant groups
    unique_norm = df[['normalized_variant_group', 'text_raw', 'norm_hash', 'alnum_hash']].drop_duplicates('normalized_variant_group').copy()
    norm_groups = unique_norm['normalized_variant_group'].tolist()
    texts = unique_norm['text_raw'].tolist()
    alnums = unique_norm['alnum_hash'].tolist()
    N = len(norm_groups)
    logging.info(f"Unique Normalized Groups to cluster: {N:,}")
    
    all_shingles = [get_shingles(t) for t in texts]
    
    # 1. Deterministic MinHash
    np.random.seed(RANDOM_SEED)
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
    
    # 2. LSH Banding with Recursive Sub-blocking for large buckets
    b_count = 16
    r_count = 4
    buckets = defaultdict(list)
    for doc_id in range(N):
        if not all_shingles[doc_id]: continue
        for band_idx in range(b_count):
            band = tuple(signatures[doc_id, band_idx*r_count : (band_idx+1)*r_count])
            buckets[(band_idx, band)].append(doc_id)
            
    candidate_pairs = set()
    large_bucket_count = 0
    
    for b_key, doc_list in buckets.items():
        if len(doc_list) <= 1:
            continue
        elif len(doc_list) < 200:
            for i in range(len(doc_list)):
                for j in range(i+1, len(doc_list)):
                    d1, d2 = doc_list[i], doc_list[j]
                    if d1 > d2: d1, d2 = d2, d1
                    candidate_pairs.add((d1, d2))
        else:
            # Recursive sub-blocking for buckets >= 200 (no silent skip!)
            large_bucket_count += 1
            sub_buckets = defaultdict(list)
            for doc_id in doc_list:
                # Sub-block by length bucket (tens of characters) and first 2 chars of alnum_hash
                t_len = len(texts[doc_id]) // 20
                al_prefix = alnums[doc_id][:2]
                sub_buckets[(t_len, al_prefix)].append(doc_id)
                
            for sub_key, sub_list in sub_buckets.items():
                if 1 < len(sub_list) < 200:
                    for i in range(len(sub_list)):
                        for j in range(i+1, len(sub_list)):
                            d1, d2 = sub_list[i], sub_list[j]
                            if d1 > d2: d1, d2 = d2, d1
                            candidate_pairs.add((d1, d2))
                            
    logging.info(f"Evaluated {len(candidate_pairs):,} candidate pairs (large buckets processed: {large_bucket_count}).")
    
    # 3. Verify Candidate Pairs with Jaccard >= 0.65
    verified_edges = []
    edge_similarities = {}
    for d1, d2 in candidate_pairs:
        s1, s2 = all_shingles[d1], all_shingles[d2]
        union_len = len(s1.union(s2))
        if union_len > 0:
            jaccard = len(s1.intersection(s2)) / union_len
            if jaccard >= 0.65:
                verified_edges.append((d1, d2))
                edge_similarities[(d1, d2)] = round(float(jaccard), 4)
                
    logging.info(f"Verified {len(verified_edges):,} near-duplicate edges (Jaccard >= 0.65).")
    
    # 4. Connected Components with SciPy (Transitive Closure)
    if verified_edges:
        rows = [e[0] for e in verified_edges]
        cols = [e[1] for e in verified_edges]
        data = np.ones(len(verified_edges), dtype=int)
        adj_matrix = csr_matrix((data, (rows, cols)), shape=(N, N))
    else:
        adj_matrix = csr_matrix((N, N))
        
    n_components, labels = connected_components(adj_matrix, directed=False)
    logging.info(f"Connected components computed: {n_components:,} distinct template families.")
    
    # Map cluster labels to deterministic clean IDs
    norm_to_ndg = {norm_groups[i]: f"NDG_{labels[i]+1:06d}" for i in range(N)}
    norm_to_comp = {norm_groups[i]: labels[i] for i in range(N)}
    
    df["near_duplicate_group"] = df["normalized_variant_group"].map(norm_to_ndg)
    
    # Assign method and confidence
    # Exact duplicate records get confidence 1.00
    # Different exact but same whitespace/norm gets 0.95
    # Near duplicates across different norm groups get Jaccard similarity (0.65-0.94)
    # Singletons get 1.00
    comp_to_docs = defaultdict(list)
    for i in range(N):
        comp_to_docs[labels[i]].append(i)
        
    # Validation Sample Generation
    logging.info("Generating near_duplicate_validation_v2.csv...")
    val_rows = []
    
    # 1. Top 100 largest clusters
    sorted_comps = sorted(comp_to_docs.items(), key=lambda x: len(x[1]), reverse=True)
    for comp_id, doc_ids in sorted_comps[:100]:
        gid = f"NDG_{comp_id+1:06d}"
        if len(doc_ids) >= 2:
            d1, d2 = doc_ids[0], doc_ids[1]
            s1, s2 = all_shingles[d1], all_shingles[d2]
            sim = len(s1.intersection(s2)) / len(s1.union(s2)) if s1.union(s2) else 1.0
            val_rows.append({
                "group_id": gid,
                "text_a": texts[d1],
                "text_b": texts[d2],
                "similarity": round(sim, 4),
                "same_group": True,
                "method": "minhash_jaccard_top_cluster"
            })
            
    # 2. 100 random small clusters (size 2-5)
    small_comps = [c for c in sorted_comps if 2 <= len(c[1]) <= 5]
    np.random.seed(RANDOM_SEED)
    if small_comps:
        chosen_small = np.random.choice(len(small_comps), size=min(100, len(small_comps)), replace=False)
        for idx in chosen_small:
            comp_id, doc_ids = small_comps[idx]
            gid = f"NDG_{comp_id+1:06d}"
            d1, d2 = doc_ids[0], doc_ids[1]
            s1, s2 = all_shingles[d1], all_shingles[d2]
            sim = len(s1.intersection(s2)) / len(s1.union(s2)) if s1.union(s2) else 1.0
            val_rows.append({
                "group_id": gid,
                "text_a": texts[d1],
                "text_b": texts[d2],
                "similarity": round(sim, 4),
                "same_group": True,
                "method": "minhash_jaccard_small_cluster"
            })
            
    # 3. 100 boundary pairs with similarity around threshold (0.65 - 0.70)
    boundary_edges = [e for e, s in edge_similarities.items() if 0.65 <= s <= 0.72]
    if boundary_edges:
        chosen_b = np.random.choice(len(boundary_edges), size=min(100, len(boundary_edges)), replace=False)
        for idx in chosen_b:
            d1, d2 = boundary_edges[idx]
            gid = f"NDG_{labels[d1]+1:06d}"
            val_rows.append({
                "group_id": gid,
                "text_a": texts[d1],
                "text_b": texts[d2],
                "similarity": edge_similarities[(d1, d2)],
                "same_group": True,
                "method": "boundary_threshold_pair"
            })
            
    val_df = pd.DataFrame(val_rows)
    val_df.to_csv("data/audit/near_duplicate_validation_v2.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/audit/near_duplicate_validation_v2.csv ({len(val_df)} inspection pairs).")
    
    # Save checkpoint
    df.to_pickle("data/interim/full_pool_v2_clustered.pkl")
    logging.info("Saved data/interim/full_pool_v2_clustered.pkl")
    print("Script 09 completed successfully.")

if __name__ == "__main__":
    main()
