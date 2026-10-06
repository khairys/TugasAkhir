# FINAL AUDIT SUMMARY v2
## Dataset Harmonization, Cleaning, and Quality Control Summary v2

### 1. Dataset Overview
```text
Raw records: 84,004
Canonical unique records: 48,051
Accepted: 83,996
Review: 6
Invalid: 2
Excluded: 2
```

### 2. Label Distribution (Canonical Unique Dataset v2)
```text
Promotion (1): 7,999 (16.65%)
Non-Promotion (0): 40,052 (83.35%)
```

### 3. Layered Candidate Pools Architecture
```text
Layer 1: Canonical Master (canonical_dataset_v2): 48,051 records
Layer 2: Main Model Candidate (main_pool_candidate_v2): 41,152 records (DS1 + Unified Kyyyy8)
Layer 3: Isolated OOD Candidate (ood_ds3_candidate_v2): 2,689 records (Zero overlap with main pool)
Layer 3: External Candidate (external_ds5_candidate_v2): 4,202 records (Audited against main pool)
```

### 4. Leakage Risk Groups
```text
Exact duplicate families (EDG): 48,054
Whitespace duplicate families (WDG): 48,041
Normalized variant families (NVG): 47,645
Near-duplicate template families (NDG): 46,469
Consolidated Leakage Groups (LG): 46,469
Scoped Author Groups: 18,968
Cross-source duplicate records: 0
Adjudicated label conflicts: 0 records across 51 unique text groups
```

### 5. Major Methodological Corrections in v2
1. **Resolved Monotonicity Inconsistency (Issue A)**: Recomputed overlap metrics strictly ensuring `exact_shared <= whitespace_shared <= normalized_shared <= alnum_shared` for all 10 pairs.
2. **Disentangled Conflict Types (Issue B)**: Clearly separated cross-dataset conflicts (48 groups) from within-dataset conflicts (6 groups) totaling 51 unique text groups (181 rows).
3. **Non-Skipping Near-Duplicate Clustering (Issue C)**: Removed silent bucket skips using recursive sub-blocking and generated 300 validation samples.
4. **Promotion Type Demoted to Heuristic (Issue D)**: Explicitly renamed to `promotion_type_heuristic_version = 'v2'` and `promotion_type_is_gold = False`, fixing float casting.
5. **Strict Brand vs Lexical Term Separation (Issue E)**: Disentangled site entities (`ambil4d`, `gunungwin`) from lexical gambling terms (`slot`, `maxwin`, `zeus`).
6. **Strictly Isolated OOD DS3 (Issue F)**: Purged all exact, whitespace, normalized, and near-duplicate overlapping records from DS3 relative to the main training pool.