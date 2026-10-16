# Stage 11 Validation Report

Updated: 17 October 2026  
Scope: saved-artifact validation on branch stage11-robustness-analysis.

## Automated checks

The entry point is scripts/validation/validate_stage11_artifacts.py. It checks the frozen Stage 11 candidate CSVs against manifest hashes, row counts and label distributions; primary table shapes and required values; all input hashes listed in the primary analysis snapshot; all six domain-shift prediction files against dataset/model metrics and confusion matrices; and completeness of the 113-row AI-assisted review queue.

GitHub Actions runs this validator and tests/stage11. This report does not pre-claim a pass status; use the actual workflow run attached to the relevant commit.

## Result package available

Primary analysis includes 3 absolute-performance rows, 24 model-condition rows, 3 robustness summary rows, 3 family-matrix rows, 12 model-family severity rows and 24 paired-bootstrap intervals. Domain-shift results include six unique combinations of three models and two datasets.

The error queue now has proposed semantic categories, representation-failure hypotheses and notes for each candidate. AI_ASSISTED_REVIEWED means AI-assisted first-pass classification from the text in the candidate row, not independent human adjudication.

## Warnings intentionally retained

- Train/validation hashes differ from the official split manifest. This is an unresolved end-to-end retraining reproducibility issue; the validator surfaces it as a warning.
- DS5 raw source hash differs from the official source hash. The frozen DS5 candidate hash remains the one used by the existing predictions; do not overwrite it while resolving provenance.
- IndoBERT weights are intentionally stored outside Git due to file size. Artifact validation accepts their absence; fresh inference needs the approved external bundle matching its configured SHA-256.
- The validator does not run inference, train models, tune thresholds, or modify frozen datasets.

## Interpretation rule

A successful focused run means the persisted Stage 11 package passes implemented structural, hash, row-count and metric-consistency checks. It does not establish clean-clone training reproducibility, fresh IndoBERT inference reproducibility, human inter-annotator agreement, or causal explanation of individual model errors.
