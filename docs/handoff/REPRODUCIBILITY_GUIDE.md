# Reproducibility Guide — Supervisor Review

## 1. Frozen environment and integrity prerequisites

The standard main comparison contains only **Linear SVM, Char-CNN, and IndoBERT**. Their authoritative paths are listed in `configs/model_registry.json`, and the frozen evaluation contract is `configs/evaluation/stage10_robustness.json`.

Experiment anchors:

- Base Transformer: `indobenchmark/indobert-base-p2`, revision `94b4e0a82081fa57f227fcc2024d1ea89b57ac1f`.
- Frozen training rows: 32,920; validation rows: 4,116; test rows: 4,116.
- Label mapping: `0 = Non-Promotion`, `1 = Promotion`.
- Split manifest: `data/splits/v1/split_manifest_v1.json`.
- Frozen test/obfuscation manifest: `data/experiments/frozen_experiment_manifest_v1.json` and `configs/evaluation/stage10_robustness.json`.

**Training reproducibility caveat:** train and validation CSV files currently tracked under `data/splits/v1/` do not match their official manifest hashes. Recover the original frozen split archive before claiming end-to-end training reproducibility. This mismatch is not, by itself, a reason to discard or change persisted Stage 11 prediction/metric artifacts. Do not adjust expected hashes to fit current files.

## 2. Dataset preparation lineage

The active repository keeps the resulting frozen data, manifests, audits, and provenance needed to understand the dataset. Superseded candidate/intermediate datasets and pilot queues are intentionally excluded from the active working tree. Do not regenerate frozen files during ordinary reproduction.

If regeneration is necessary for a future methodological experiment, write to a separate versioned destination and compare hashes before considering the result equivalent to the frozen protocol. The controlled transformation implementation used by the official protocol is under `src/obfuscation/`.

## 3. Canonical models and artifacts

| Model | Stable training entrypoint | Configuration | Final artifact |
|---|---|---|---|
| Linear SVM | `scripts/training/linear_svm.py` | `models/linear_svm/config.json` | `models/linear_svm/model/model.joblib` |
| Char-CNN | `scripts/training/char_cnn.py` | `models/char_cnn/config.json` | `models/char_cnn/artifacts/final_model/charcnn_model.pt`, plus `vocab.json` |
| IndoBERT | `scripts/training/indobert.py` | `models/indobert/config.json` | `models/indobert/artifacts/final_model/` |

The model names above are the canonical comparison labels. Dataset and frozen-artifact suffixes such as `v1` are provenance identifiers for frozen data; they are not separate model choices. In the thesis and primary result tables, use only **Linear SVM**, **Char-CNN**, and **IndoBERT**.

Model selection is based on the normal validation Promotion F1 and the tie-breakers recorded in each configuration/run manifest. Do not use the frozen test sets to tune learning rates, epochs, thresholds, or preprocessing.

## 4. Standard robustness evaluation

Run all commands from the repository root, after the dataset and model artifact blockers have been resolved:

```bash
python scripts/evaluation/robustness.py --mode preflight
python scripts/evaluation/robustness.py --mode official
python scripts/evaluation/validate_results.py
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

`scripts/diagnostics/unicode_obfuscation.py` is a validation-only diagnostic using the selected IndoBERT baseline. It writes to `reports/diagnostics/unicode_obfuscation/` and should not modify official robustness outputs. It is supplemental evidence, not a replacement for the frozen test results.

## 6. Selected IndoBERT weight handoff

The expected `models/indobert/artifacts/final_model/model.safetensors` is intentionally not in Git because the model weights are very large. This is not a blocker for inspecting and validating saved Stage 11 predictions and metrics. Before fresh inference, retrieve the approved external artifact and verify its SHA-256 against `configs/evaluation/stage10_robustness.json`; tokenizer/config files alone are insufficient.

## 7. Pre-submission checklist

- For a future end-to-end retraining reproduction, recover and verify train/validation files against the frozen manifest.
- For fresh IndoBERT inference only, supply the external weights and verify their configured hash.
- Run the Stage 11 artifact validator and focused tests on the exact branch; record the actual workflow result.
- Keep test conditions frozen and do not tune on final test results.
- Preserve the DS5 candidate and resolve raw-source provenance before attempting a rebuild.


## 8. Stage 11 saved-artifact validation

Run `python scripts/validation/validate_stage11_artifacts.py` and `python -m pytest -q tests/stage11`. These checks validate the saved result package; they do not rerun training or inference. Warnings about the train/validation split and DS5 raw-source hashes are surfaced separately from Stage 11 artifact integrity failures. The absence of the large IndoBERT weight file is accepted for artifact-only validation, but fresh IndoBERT inference must verify the configured SHA-256.
