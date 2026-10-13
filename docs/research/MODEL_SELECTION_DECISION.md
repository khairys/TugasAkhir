# Canonical Model Selection Decision — Stage 10

**Decision date:** 2026-10-13  
**Status:** Locked for the main comparison and future analyses unless a new, predeclared experiment justifies a change.

## Decision

The main thesis comparison contains exactly three model systems:

1. **Linear SVM** — word-level TF-IDF.
2. **Char-CNN** — character-level convolutional neural network.
3. **IndoBERT** — the original fine-tuned `indobenchmark/indobert-base-p2` baseline used in the official three-model evaluation.

Use only those display names in future primary-result tables, figures, and standard reports. Artifact directory names and split versions remain provenance metadata, not separate model labels.

## Why the original IndoBERT baseline was selected

The research objective prioritizes robustness across four obfuscation families, rather than a marginal gain in clean-text F1 alone.

| Selection evidence | Original IndoBERT baseline | Later training experiment |
|---|---:|---:|
| Normal-test Promotion F1 | 0.9605 | 0.9613 |
| Mean paired F1 across eight obfuscation conditions | 0.8771 | 0.8721 |
| Mean F1 retention | 91.27% | 90.66% |

The later experiment increased normal-test F1 by only about **0.08 percentage points**. It improved paired F1 for Unicode homoglyphs (O4 mild: 0.8183 vs 0.7878; O4 strong: 0.6648 vs 0.6323), but was worse on all six O1–O3 conditions. Mean paired F1 and mean retention were also lower. These are descriptive point estimates from a single frozen split; no formal significance test or multi-seed evaluation was performed.

This did not justify replacing the original checkpoint as the third, stable comparator. The later experiment's source code, model bundle, predictions, and standalone report have been removed from the cleaned working branch. The summary above remains to document the selection decision, not to define a fourth active model.

## Canonical configuration and artifact map

| Stable ID | Display label | Training/configuration | Selected artifact |
|---|---|---|---|
| `linear_svm` | Linear SVM | `scripts/training/linear_svm.py`; `models/linear_svm/config.json` | `models/linear_svm/model/model.joblib` |
| `char_cnn` | Char-CNN | `scripts/training/char_cnn.py`; `models/char_cnn/config.json` | `models/char_cnn/artifacts/final_model/charcnn_model.pt` |
| `indobert` | IndoBERT | `scripts/training/indobert.py`; `models/indobert/config.json` | `models/indobert/artifacts/final_model/` |

The single source of truth for this lineup is `configs/model_registry.json`. The Stage 10 evaluation configuration is `configs/evaluation/stage10_robustness.json`.

## Reproducibility safeguards

The model choice is fixed, but the complete handoff is not yet fully reproducible:

- The train and validation CSVs tracked in `data/splits/v1/` were observed not to match the SHA-256 values in `data/splits/v1/split_manifest_v1.json`. Recover the original frozen split snapshot and verify its hashes. Do not silently change the manifest.
- The selected IndoBERT weight file, `models/indobert/artifacts/final_model/model.safetensors`, is not present in Git. Obtain the approved, verified artifact bundle and check it against the expected SHA-256 before running inference.
- Run the data-integrity checks, robustness validator, and applicable tests from the cleaned branch before describing the new tree as runtime-verified.

Any future model substitution must be declared as a separate experiment before the frozen test set is examined. Do not silently switch a selected checkpoint after viewing test results.
