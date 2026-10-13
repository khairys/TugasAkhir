# Online Gambling Promotion Detection — Robustness Study

This repository contains the research assets for evaluating robustness of Indonesian YouTube-comment classifiers against controlled text obfuscation.

## Canonical model lineup

The main analysis uses exactly three model systems:

| Display name | Representation | Model artifact |
|---|---|---|
| Linear SVM | Word-level TF-IDF | `models/linear_svm/model/model.joblib` |
| Char-CNN | Character-level CNN | `models/char_cnn/artifacts/final_model/charcnn_model.pt` |
| IndoBERT | Fine-tuned `indobenchmark/indobert-base-p2` | `models/indobert/artifacts/final_model/` |

Use these display names in future result tables and figures. Do not list different IndoBERT training versions as separate main models. The model-selection rationale is retained in [the decision memo](docs/research/MODEL_SELECTION_DECISION.md).

## Start here

1. [Model-selection decision](docs/research/MODEL_SELECTION_DECISION.md)
2. [Stage 10 final conclusions](docs/research/STAGE10_FINAL_CONCLUSIONS.md)
3. [Supervisor handoff](docs/handoff/SUPERVISOR_HANDOFF.md)
4. [Reproducibility guide](docs/handoff/REPRODUCIBILITY_GUIDE.md)
5. [Stage 10 closure checklist](docs/handoff/STAGE10_CLOSURE_CHECKLIST.md)
6. [Obfuscation specification](docs/research/OBFUSCATION_SPECIFICATION_V1.md)
7. [Dataset audit and labeling guideline](docs/data/DATASET_AUDIT_REPORT.md)

## Repository layout

```text
configs/
  models/                 Linear SVM config used by its training entry point
  evaluation/             Frozen Stage 10 evaluation configuration
  model_registry.json     Authoritative three-model registry
data/
  raw/                    Original source datasets (immutable)
  source_variants/        Additional source snapshots retained for provenance
  interim/                Harmonized datasets and auditable intermediates
  audit/                  Dataset quality, overlap, and integrity evidence
  review/                 Human-review queues
  manifests/              Record and source manifests
  splits/v1/              Frozen train/validation/test split and manifest
  processed/              Frozen normal test and paired obfuscation conditions
models/
  linear_svm/             Selected SVM artifact and training report
  char_cnn/               Selected Char-CNN artifact, source config and reports
  indobert/               Selected IndoBERT baseline artifact, source config and reports
scripts/                  Ordered dataset preparation and official evaluation
src/obfuscation/          Controlled text-transformation implementation
tests/                    Dataset, obfuscation, and Stage 10 integrity checks
reports/stage10/          Official three-model robustness results
reports/diagnostics/      Supporting diagnostic analysis
docs/data/                Dataset audit and labeling methods
docs/research/            Research protocol and scientific conclusions
docs/handoff/             Supervisor and reproducibility materials
```

## Main results

Normal-test Promotion F1:

- Linear SVM: 0.9428
- Char-CNN: **0.9786**
- IndoBERT: 0.9605

Unweighted mean paired F1 across the eight obfuscation conditions:

- Char-CNN: **0.9763** (99.62% mean F1 retention)
- Linear SVM: 0.8876 (93.98%)
- IndoBERT: 0.8771 (91.27%)

These are descriptive results from one frozen test split. No multi-seed evaluation or formal significance test was run.

## Standard commands

Run commands from the repository root:

```bash
python scripts/22_run_stage10_robustness.py --mode preflight
python scripts/22_run_stage10_robustness.py --mode official
python scripts/23_validate_stage10_results.py
pytest tests/
```

The Unicode/tokenizer diagnostic is separate from the official test evaluation:

```bash
python scripts/24_unicode_obfuscation_diagnostic.py
```

## Known reproducibility blockers

- The train and validation CSVs currently in `data/splits/v1/` do not match the hashes in the official split manifest. Recover and verify the original split archive; do not alter the manifest hashes just to force a pass.
- The selected IndoBERT `model.safetensors` file is not present in Git although its expected hash is recorded in the evaluation configuration. Obtain the verified model bundle before running full inference.
- A full Stage 10 runtime and test run has not been executed as part of this cleanup.

Original raw data, final frozen test conditions, and dataset-audit evidence are retained. Generated logs, smoke-only artifacts, the duplicate Char-CNN ZIP, bulky full-pool pickle intermediates, and the unused later IndoBERT experiment bundle have been removed from this working branch.
