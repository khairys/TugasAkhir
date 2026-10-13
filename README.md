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
2. [Final research results](docs/research/FINAL_RESULTS.md)
3. [Future analysis plan](docs/research/FUTURE_ANALYSIS_PLAN.md)
4. [Supervisor handoff](docs/handoff/SUPERVISOR_HANDOFF.md)
5. [Reproducibility guide](docs/handoff/REPRODUCIBILITY_GUIDE.md)
6. [Stage 10 closure checklist](docs/handoff/STAGE10_CLOSURE_CHECKLIST.md)
7. [Obfuscation specification](docs/research/OBFUSCATION_SPECIFICATION_V1.md)
8. [Dataset audit and labeling guideline](docs/data/DATASET_AUDIT_REPORT.md)

## Repository layout

```text
configs/
  model_registry.json     Authoritative three-model registry
  models/                 Model-specific configuration files
  evaluation/             Frozen robustness evaluation configuration
data/
  raw/                    Original source datasets retained for provenance
  audit/                  Dataset quality, overlap, and integrity evidence
  manifests/              Record and source manifests
  splits/v1/              Frozen train/validation/test split and manifest
data/processed/
  test_normal_v1.csv      Frozen normal test condition
  obfuscated_test_v1/     Eight frozen paired obfuscation conditions
models/
  linear_svm/             Selected Linear SVM artifact and training report
  char_cnn/               Selected Char-CNN artifact, configuration and reports
  indobert/               Selected IndoBERT baseline artifact, configuration and reports
scripts/
  19_train_linear_svm.py  Linear SVM training entry point
  22_run_stage10_robustness.py
  23_validate_stage10_results.py
  24_unicode_obfuscation_diagnostic.py
src/obfuscation/          Controlled text-transformation implementation
tests/                    Obfuscation and Stage 10 integrity checks
reports/stage10/          Official three-model robustness results
reports/diagnostics/      Supporting diagnostic analysis
docs/data/                Dataset audit and labeling methods
docs/research/            Research protocol, final results, and future analysis plan
docs/handoff/             Supervisor and reproducibility materials
```

The active research repository intentionally excludes superseded candidate pools, duplicate source snapshots, pilot review queues, smoke-only outputs, and the unused later IndoBERT experiment. Those artifacts remain recoverable through Git history when provenance is required.

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

## Standard evaluation commands

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

The active branch retains the frozen raw sources, final split/test assets, model artifacts, audit evidence, research protocol, and official three-model results. Superseded candidate/intermediate data and the unused IndoBERT experiment are deliberately excluded from the active research layout.
