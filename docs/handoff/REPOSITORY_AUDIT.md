# Repository Audit and Handoff Map

## Scope and cleanup

The cleaned working branch reorganizes the research artifacts around the three canonical models and the frozen robustness protocol. It also removes generated or unused material that obscured the active pipeline.

### Canonical model lineup

| Purpose | Location | Role |
|---|---|---|
| Model registry | `configs/model_registry.json` | Source of truth for the three display names and artifact paths |
| Evaluation config | `configs/evaluation/stage10_robustness.json` | Frozen inputs, model artifacts, metrics, and paired protocol |
| Linear SVM | `scripts/19_train_linear_svm.py`, `configs/models/linear_svm.json`, `models/linear_svm/` | TF-IDF baseline and selected pipeline |
| Char-CNN | `models/char_cnn/project/`, `models/char_cnn/artifacts/final_model/` | Character-level model, vocabulary, and training configuration |
| IndoBERT | `models/indobert/project/`, `models/indobert/artifacts/final_model/` | Selected baseline model/tokenizer/config; weights need verified handoff |
| Official Stage 10 | `scripts/22_run_stage10_robustness.py`, `scripts/23_validate_stage10_results.py`, `reports/stage10/` | The official three-model evaluation, predictions, metrics, manifests, and error audit |
| O4 diagnostic | `scripts/24_unicode_obfuscation_diagnostic.py`, `reports/diagnostics/unicode_obfuscation/` | Validation-only diagnostic; not part of official test evaluation |
| Obfuscation engine | `src/obfuscation/`, `scripts/17_generate_official_obfuscated_test.py`, `scripts/18_validate_official_obfuscated_test.py` | Transformation implementation and frozen test validation |
| Frozen data protocol | `data/splits/v1/`, `data/processed/test_normal_v1.csv`, `data/processed/obfuscated_test_v1/` | Fixed split and paired test conditions |
| Dataset lineage and review | `data/raw/`, `data/source_variants/`, `data/interim/`, `data/audit/`, `data/review/`, `data/manifests/` | Source preservation, derived datasets, provenance, and quality-control evidence |
| Tests | `tests/obfuscation/`, `tests/stage8/`, `tests/stage9/`, `tests/stage10/` | Transformation and data/evaluation integrity checks |

## Current top-level layout

```text
configs/
  evaluation/
  models/
  model_registry.json
data/
  raw/
  source_variants/
  interim/
  audit/
  review/
  manifests/
  splits/v1/
  processed/
models/
  linear_svm/
  char_cnn/
  indobert/
scripts/
src/obfuscation/
tests/
reports/stage10/
reports/diagnostics/unicode_obfuscation/
docs/data/
docs/research/
docs/handoff/
```

## What was removed from the active branch

- The later IndoBERT training experiment directory, its model bundle, candidate outputs, and corresponding robustness reports/predictions.
- The unused alternate IndoBERT training script and the old standalone model-comparison script.
- Generated logs, smoke-only SVM artifacts/reports, duplicate result ZIPs, and several bulky full-pool pickle intermediates.
- Old duplicate source snapshot folders were consolidated under `data/source_variants/`; raw source data and the audit/review lineage remain available.

The removal of the later model's implementation does not change the official three-model Stage 10 result files. Its selection metrics remain summarized in `docs/research/MODEL_SELECTION_DECISION.md` so the decision is transparent. The original/main branch was not modified by this cleanup.

## Data and model release blockers

### 1. Frozen train/validation checksum mismatch

The manifest `data/splits/v1/split_manifest_v1.json` specifies train SHA-256 `65a10e93713586e20ebb9a3a0c0694d860a6d9d5541e84000713f2918d595cf3` and validation SHA-256 `7753fb36275d36a2367e15d28de3f52f06e0f33a4f666d81d7dd95c5a9d87038`. The CSV files tracked in the cleaned GitHub tree were observed to hash to different values. Recover the original frozen split snapshot from the original research storage and compare its contents and hashes. Do not edit the expected manifest hashes merely to make validation pass.

### 2. Selected IndoBERT weights

The evaluation configuration expects `models/indobert/artifacts/final_model/model.safetensors` with SHA-256 `890dd84c8f25f2d0761959335c5bc00c76b396cf6065317d7589ee84d3ddafbd`, but this file is not tracked in Git. Supply the verified weights from approved storage. Do not bypass Git's large-file exclusions without agreeing on a distribution method.

### 3. Runtime verification

This cleanup was checked statically against repository paths and configuration content. Full Stage 10 inference, the validator, and the complete test suite have not been run against the exact cleaned branch. The cleanup should not be described as runtime-tested until those checks are executed successfully.

## Recommended thesis presentation order

1. Research question and frozen dataset/pairing protocol.
2. Normal baseline metrics for the three canonical models.
3. Paired F1 and robustness retention over O1–O4, MILD and STRONG.
4. Error analysis, especially IndoBERT false positives under Unicode homoglyphs.
5. Limitations and release/reproducibility constraints.
