# Graph Report - Code  (2026-10-14)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 372 nodes · 790 edges · 16 communities (13 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `707663e6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pandas
- indobert_train.py
- 19_train_linear_svm.py
- charcnn_train.py
- 22_run_stage10_robustness.py
- pytest
- obfuscate
- json
- src/obfuscation/__init__.py
- pathlib
- 24_unicode_obfuscation_diagnostic.py
- rules.py
- run_indobert_inference
- test_protected_tokens.py
- test_obfuscation_determinism.py

## God Nodes (most connected - your core abstractions)
1. `obfuscate()` - 34 edges
2. `main()` - 22 edges
3. `main()` - 18 edges
4. `main()` - 14 edges
5. `find_eligible_token_spans()` - 11 edges
6. `run_official_evaluation()` - 11 edges
7. `main()` - 10 edges
8. `make_rng()` - 10 edges
9. `validate_final()` - 10 edges
10. `run_preflight()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_email_protection()` --calls--> `obfuscate()`  [EXTRACTED]
  tests/obfuscation/test_protected_tokens.py → src/obfuscation/engine.py
- `test_mention_and_hashtag_protection()` --calls--> `obfuscate()`  [EXTRACTED]
  tests/obfuscation/test_protected_tokens.py → src/obfuscation/engine.py
- `test_build_pipeline_structure()` --calls--> `build_pipeline()`  [INFERRED]
  tests/stage9/test_pipeline_and_serialization.py → scripts/19_train_linear_svm.py
- `test_stratified_paired_bootstrap()` --calls--> `run_stratified_paired_bootstrap()`  [INFERRED]
  tests/stage10/test_metrics.py → scripts/22_run_stage10_robustness.py
- `generate_homoglyph_only()` --calls--> `make_rng()`  [EXTRACTED]
  scripts/24_unicode_obfuscation_diagnostic.py → src/obfuscation/rules.py

## Import Cycles
- None detected.

## Communities (16 total, 3 thin omitted)

### Community 0 - "pandas"
Cohesion: 0.06
Nodes (17): compute_alnum_hash(), compute_exact_hash(), compute_normalized_hash(), compute_whitespace_hash(), sha256_file(), test_dataset_row_counts_and_columns(), test_dataset_sha256_hashes(), normal_test() (+9 more)

### Community 1 - "indobert_train.py"
Cohesion: 0.10
Nodes (22): ArrayDataset, atomic_json(), build_args(), checkpoint_is_compatible(), checkpoint_step(), compute_metrics(), find_persistent_checkpoints(), _json_default() (+14 more)

### Community 2 - "19_train_linear_svm.py"
Cohesion: 0.08
Nodes (14): compute_sha256(), main(), build_pipeline(), compute_sha256(), evaluate_pipeline(), get_git_info(), is_candidate_better(), main() (+6 more)

### Community 3 - "charcnn_train.py"
Cohesion: 0.16
Nodes (25): atomic_json(), atomic_text(), autocast_context(), batch_predict(), candidate_complete(), capture_rng(), CharCNN, compute_metrics() (+17 more)

### Community 4 - "22_run_stage10_robustness.py"
Cohesion: 0.10
Nodes (9): CharCNNModule, IndoBERTModule, load_svm_pipeline(), main(), predict_svm(), run_official_evaluation(), run_preflight(), run_stratified_paired_bootstrap() (+1 more)

### Community 5 - "pytest"
Cohesion: 0.09
Nodes (10): calculate_classification_metrics(), test_calculate_classification_metrics_known_case(), test_calculate_classification_metrics_perfect(), test_evasion_flip_definition(), test_paired_f1_drop_and_retention(), test_stratified_paired_bootstrap(), normal_df(), test_pairing_alignment_and_labels() (+2 more)

### Community 6 - "obfuscate"
Cohesion: 0.12
Nodes (11): obfuscate(), test_different_seeds_or_ids_deterministic(), test_identical_runs_produce_identical_outputs(), test_no_eligible_targets_handling(), test_o1_char_substitution(), test_o2_char_insert_delete(), test_o3_whitespace(), test_o4_unicode_orthographic() (+3 more)

### Community 7 - "json"
Cohesion: 0.12
Nodes (8): sha256_file(), validate_all_outputs(), test_char_cnn_label_mapping(), test_indobert_label_mapping(), compute_sha256(), test_experiment_manifest_hashes(), test_split_manifest_hashes(), config()

### Community 8 - "src/obfuscation/__init__.py"
Cohesion: 0.19
Nodes (5): ObfuscationResult, count_character_changes(), count_modified_ratio(), is_protected_token(), levenshtein_distance()

### Community 10 - "24_unicode_obfuscation_diagnostic.py"
Cohesion: 0.17
Nodes (7): generate_homoglyph_only(), generate_markdown_report(), generate_standard_o4(), main(), normalize_homoglyphs(), sha256_file(), verify_repo_integrity()

### Community 11 - "rules.py"
Cohesion: 0.22
Nodes (6): char_insert_delete(), char_substitution(), make_rng(), unicode_orthographic(), whitespace_manipulation(), find_eligible_token_spans()

### Community 12 - "run_indobert_inference"
Cohesion: 0.20
Nodes (3): analyze_tokenization(), compute_metrics(), run_indobert_inference()

### Community 13 - "test_protected_tokens.py"
Cohesion: 0.25
Nodes (5): extract_protected_spans(), verify_protected_spans(), test_email_protection(), test_mention_and_hashtag_protection(), test_url_protection()

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `obfuscate()` connect `obfuscate` to `19_train_linear_svm.py`, `src/obfuscation/__init__.py`, `rules.py`, `test_protected_tokens.py`, `test_obfuscation_determinism.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Should `pandas` be split into smaller, more focused modules?**
  _Cohesion score 0.061683599419448475 - nodes in this community are weakly interconnected._
- **Why does `run_indobert_inference()` connect `run_indobert_inference` to `24_unicode_obfuscation_diagnostic.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `indobert_train.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09595959595959595 - nodes in this community are weakly interconnected._
- **Should `19_train_linear_svm.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08232118758434548 - nodes in this community are weakly interconnected._
- **Should `22_run_stage10_robustness.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1010752688172043 - nodes in this community are weakly interconnected._
- **Should `pytest` be split into smaller, more focused modules?**
  _Cohesion score 0.08866995073891626 - nodes in this community are weakly interconnected._