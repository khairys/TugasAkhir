# Repository Audit and Handoff Map

## Scope and cleanup

The cleaned working branch reorganizes the research artifacts around the three canonical models and the frozen robustness protocol. It removes superseded generation code and unused model experiments that are not required for future analysis, while retaining the frozen data lineage, audit evidence, model artifacts, and official results needed for research interpretation and reproducibility.

### Canonical model lineup

| Purpose | Location | Role |
|---|---|---|
| Model registry | `configs/model_registry.json` | Source of truth for the three display names and artifact paths |
| Evaluation config | `configs/evaluation/stage10_robustness.json` | Frozen inputs, model artifacts, metrics, and paired protocol |
| Linear SVM | `scripts/training/linear_svm.py`, `models/linear_svm/config.json`, `models/linear_svm/` | Stable training interface and selected pipeline |
| Char-CNN | `scripts/training/char_cnn.py`, `models/char_cnn/config.json`, `models/char_cnn/artifacts/final_model/` | Stable training interface, selected character-level model, and vocabulary |
| IndoBERT | `scripts/training/indobert.py`, `models/indobert/config.json`, `models/indobert/artifacts/final_model/` | Stable training interface and selected baseline model/tokenizer/config; weights need verified handoff |
| Official robustness evaluation | `scripts/evaluation/robustness.py`, `scripts/evaluation/validate_results.py`, `reports/stage10/` | Official three-model evaluation, predictions, metrics, manifests, and error audit |
| O4 diagnostic | `scripts/diagnostics/unicode_obfuscation.py`, `reports/diagnostics/unicode_obfuscation/` | Validation-only diagnostic; not part of official test evaluation |
| Obfuscation engine | `src/obfuscation/` | Controlled transformation implementation used by the frozen protocol |
| Frozen data protocol | `data/splits/v1/`, `data/processed/test_normal_v1.csv`, `data/processed/obfuscated_test_v1/` | Fixed split and paired test conditions |
| Dataset lineage and review | `data/raw/`, `data/source_variants/`, `data/interim/`, `data/audit/`, `data/review/`, `data/manifests/` | Source preservation, derived datasets, provenance, and quality-control evidence |
| Tests | `tests/obfuscation/`, `tests/stage8/`, `tests/stage9/`, `tests/stage10/` | Transformation and data/model/evaluation integrity checks |

## Current top-level layout

```text
configs/
  model_registry.json
  models/
  evaluation/
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
  training/
  evaluation/
  diagnostics/
  utils/
src/obfuscation/
tests/
reports/stage10/
reports/diagnostics/
docs/data/
docs/research/
docs/handoff/
```

## What was removed from the active branch

- The later IndoBERT training experiment directory, model bundle, candidate outputs, and separate robustness report/prediction artifacts.
- The unused alternate IndoBERT training script and old standalone four-model comparison script.
- Superseded dataset-generation and pilot preparation scripts from the early numbered pipeline; their resulting frozen data and audit evidence remain.
- Generated logs, smoke-only artifacts, duplicate result ZIPs, and bulky full-pool intermediates.

The removal of the later model implementation does not change the official three-model Stage 10 result files. Its selection metrics remain summarized in `docs/research/MODEL_SELECTION_DECISION.md` so the decision is transparent. The original/main branch was not modified by this cleanup.

## Known reproducibility caveats (separate from validating saved Stage 11 results)

### 1. Frozen train/validation checksum mismatch

The manifest `data/splits/v1/split_manifest_v1.json` specifies train SHA-256 `65a10e93713586e20ebb9a3a0c0694d860a6d9d5541e84000713f2918d595cf3` and validation SHA-256 `7753fb36275d36a2367e15d28de3f52f06e0f33a4f666d81d7dd95c5a9d87038`. The CSV files tracked in the cleaned GitHub tree were observed to hash to different values. Recover the original frozen split snapshot from the original research storage and compare its contents and hashes. Do not edit the expected manifest hashes merely to make validation pass.

### 2. Selected IndoBERT weights

The evaluation configuration expects `models/indobert/artifacts/final_model/model.safetensors` with SHA-256 `890dd84c8f25f2d0761959335c5bc00c76b396cf6065317d7589ee84d3ddafbd`, but this file is not tracked in Git. Supply the verified weights from approved storage. Do not bypass Git's large-file exclusions without agreeing on a distribution method.

### 3. Runtime verification

This audit reflects the repository state before the Stage 11 artifact-validation workflow was added. The focused validator checks saved Stage 11 results without training or inference. It does not claim full Stage 10 inference or a full repository test-suite rerun; use the actual workflow result for any pass/fail claim.

## Recommended thesis presentation order

1. Research question and frozen dataset/pairing protocol.
2. Normal baseline metrics for the three canonical models.
3. Paired F1 and robustness retention over O1–O4, MILD and STRONG.
4. Error analysis, especially IndoBERT false positives under Unicode homoglyphs.
5. Limitations and release/reproducibility constraints.


## Stage 11 artifact closure update — 2026-10-17

The branch contains saved primary robustness tables, 10,000-resample paired-bootstrap intervals, frozen DS3/DS5 candidates, and six domain-shift prediction/metric combinations. The 113-row error queue now contains AI-assisted text-only first-pass annotations. It does not claim independent human adjudication, and gold labels remain unchanged.

The focused validator at `scripts/validation/validate_stage11_artifacts.py` checks frozen candidate hashes/counts, primary table shapes, input hashes recorded in the analysis snapshot, six domain-shift prediction files and confusion-matrix metrics, and annotation completeness. GitHub Actions runs the validator and `tests/stage11`; the actual run status is the authority for pass/fail.

Known caveats are retained: train/validation CSV hashes differ from the official split manifest; the DS5 raw-source hash differs from its official source hash although the evaluated frozen candidate hash is recorded; and large IndoBERT weights are intentionally external to Git. These limit clean-clone retraining/fresh-inference claims, but do not by themselves prevent validating and reporting saved Stage 11 metrics and predictions. Do not change frozen data or expected hashes to make checks pass.
