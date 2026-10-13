# Reproducibility Guide — Supervisor Review

## 1. Frozen environment and integrity prerequisites

The standard main comparison contains only **Linear SVM, Char-CNN, and IndoBERT**. Their authoritative paths are listed in `configs/model_registry.json`, and the frozen evaluation contract is `configs/evaluation/stage10_robustness.json`.

Experiment anchors:

- Base Transformer: `indobenchmark/indobert-base-p2`, revision `94b4e0a82081fa57f227fcc2024d1ea89b57ac1f`.
- Frozen training rows: 32,920; validation rows: 4,116; test rows: 4,116.
- Label mapping: `0 = Non-Promotion`, `1 = Promotion`.
- Split manifest: `data/splits/v1/split_manifest_v1.json`.
- Frozen test/obfuscation manifest: `data/experiments/frozen_experiment_manifest_v1.json` and `configs/evaluation/stage10_robustness.json`.

**Release blocker:** train and validation CSV files currently tracked under `data/splits/v1/` do not match their official manifest hashes. Recover the original frozen split archive and validate it before making an end-to-end reproducibility claim. Do not adjust the expected hashes to match the current files.

## 2. Dataset preparation lineage

For data lineage and the frozen paired test protocol, inspect scripts in this order:

1. `scripts/01_raw_manifest_and_inventory.py`
2. `scripts/02_harmonize_interim.py`
3. `scripts/04_adjudicate_conflicts.py`
4. `scripts/08_validate_and_rebuild_overlap.py`
5. `scripts/09_rebuild_near_duplicates.py`
6. `scripts/10_build_leakage_safe_pools.py`
7. `scripts/11_rebuild_audit_reports.py`
8. `scripts/12_final_dataset_validation.py`
9. `scripts/15_create_experimental_split.py` and `scripts/16_validate_experimental_split.py`
10. `scripts/17_generate_official_obfuscated_test.py` and `scripts/18_validate_official_obfuscated_test.py`

Do not rerun dataset generation over frozen files during ordinary reproduction. If regeneration is necessary, write to a separate versioned destination and compare hashes before considering it equivalent.

## 3. Canonical models and artifacts

| Model | Training script/config | Final artifact |
|---|---|---|
| Linear SVM | `scripts/19_train_linear_svm.py`; `configs/models/linear_svm.json` | `models/linear_svm/model/model.joblib` |
| Char-CNN | `models/char_cnn/project/charcnn_train.py`; `models/char_cnn/project/charcnn_v1.json` | `models/char_cnn/artifacts/final_model/charcnn_model.pt`, plus `vocab.json` |
| IndoBERT | `models/indobert/project/indobert_train.py`; `models/indobert/project/indobert_v1.json` | `models/indobert/artifacts/final_model/` |

Model selection is based on the normal validation Promotion F1 and the tie-breakers recorded in each configuration/run manifest. Do not use the frozen test sets to tune learning rates, epochs, thresholds, or preprocessing.

## 4. Standard Stage 10 evaluation

Run all commands from the repository root, after the dataset and model artifact blockers have been resolved:

```bash
python scripts/22_run_stage10_robustness.py --mode preflight
python scripts/22_run_stage10_robustness.py --mode official
python scripts/23_validate_stage10_results.py
pytest tests/
```

The official output directory is `reports/stage10/`, including:

- `test_normal_metrics.csv`
- `obfuscation_metrics_full.csv`
- `paired_robustness_metrics.csv`
- `prediction_flip_summary.csv`
- `paired_error_analysis.csv`
- `source_stratified_metrics.csv`
- `robustness_summary.json`
- `manifest_v1.json`
- `predictions/` — one normal and eight obfuscated prediction files for each canonical model.

Use `--mode preflight` before a full inference run. Preserve existing frozen report files unless a deliberate, fully documented regeneration is being performed.

## 5. Supporting Unicode diagnostic

`scripts/24_unicode_obfuscation_diagnostic.py` is a validation-only diagnostic using the selected IndoBERT baseline. It writes to `reports/diagnostics/unicode_obfuscation/` and should not modify official Stage 10 outputs. It is supplemental evidence, not a replacement for the frozen test results.

## 6. Selected IndoBERT weight handoff

The expected `models/indobert/artifacts/final_model/model.safetensors` is not in Git because large model weights are excluded. Retrieve the approved artifact bundle and verify its SHA-256 against `configs/evaluation/stage10_robustness.json` before inference. Tokenizer/config files alone are not sufficient to reproduce the classifier.

## 7. Pre-submission checklist

- Recover and verify train/validation files against the frozen manifest.
- Verify all model artifacts, especially the IndoBERT weights, against the configured hashes.
- Run the official Stage 10 input/output validation and relevant tests on the exact branch being handed over.
- Record actual commands and outcomes; do not describe unexecuted checks as passing.
- Keep the test conditions frozen and do not tune on the final test results.
