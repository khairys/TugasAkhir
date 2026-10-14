# Future Analysis Plan

This document defines the default research path after the Stage 10 model-selection decision. It does not introduce a new model or change the frozen test protocol.

## Canonical comparison

Use exactly three model systems in all primary analyses:

1. Linear SVM — word-level TF-IDF.
2. Char-CNN — character-level CNN.
3. IndoBERT — the selected original fine-tuned baseline.

Do not introduce IndoBERT training versions as separate primary models unless a new, explicitly scoped experiment is approved before test-set analysis.

## Analysis order

### 1. Verify the frozen inputs

Resolve the train/validation snapshot hash mismatch and verify the selected IndoBERT weight bundle. Do not modify manifest hashes to accommodate a different dataset snapshot.

### 2. Re-run the official integrity checks

Run the Stage 10 preflight, official evaluation validator, and repository tests on the exact handoff branch. Record the actual command outcomes.

### 3. Primary robustness analysis

Use the existing frozen normal test and eight paired obfuscation conditions. Report Promotion F1 as the primary metric, with precision, recall, accuracy, F1 retention, F1 drop, false-positive transitions, and evasion transitions as supporting measures.

### 4. Statistical uncertainty

Where needed for the thesis, use the already specified paired bootstrap procedure from `configs/evaluation/stage10_robustness.json`. Report confidence intervals rather than making significance claims that the current point estimates cannot support.

### 5. Error analysis

Focus on the failure mechanisms revealed by the frozen results, especially the large false-positive increase for IndoBERT under O4 Unicode homoglyph obfuscation. Compare representative false-positive and evasion examples across the three canonical models.

### 6. Source-stratified analysis

Use the existing source-stratified Stage 10 outputs to check whether the robustness pattern is consistent across source datasets. Treat this as secondary analysis rather than a new model-selection criterion.

### 7. Stage 11.1 — DS3 OOD evaluation

Evaluate the prepared, overlap-isolated DS3 candidate with the already selected models. This is a secondary domain-shift evaluation only. Use the candidate hash and row/label counts in `data/processed/stage11/manifest_v1.json`; do not mix the records into the Main Pool or tune thresholds against DS3. The inference-only runner is `scripts/evaluation/stage11_domain_shift.py`.

### 8. Stage 11.2 — DS5 external-source evaluation

Evaluate the prepared, overlap-isolated DS5 candidate as a supplementary external-source check. Do not use DS5 for training, fine-tuning, model selection, or threshold tuning. The tracked DS5 raw file currently differs from the official raw-source SHA-256 in the Stage 11 manifest, so the preparation script must refuse to rebuild that candidate until the audited raw snapshot is restored. A prepared candidate is usable for inference only if its recorded hash and label counts verify.

### 9. Stage 11 completion and reporting

The first Stage 11 result snapshot is derived from the saved Stage 10 aggregate tables. Run the primary analysis script in a clean checkout to regenerate per-condition metrics and paired bootstrap intervals from record-level predictions. Complete manual error review and report domain inference only for model/dataset combinations that actually ran successfully. Report the current missing IndoBERT weights and train/validation split hash mismatch as reproducibility limitations rather than silently changing the protocol.

### 10. Thesis reporting

The primary narrative should be organized around:

- robustness differences between the three representations;
- the effect of each obfuscation family and severity;
- Char-CNN's robustness advantage;
- IndoBERT's Unicode/homoglyph failure mode;
- limitations of the frozen split, single-seed evaluation, and controlled transformations.

## Explicitly out of scope for the main pipeline

- IndoBERT v2 or any later IndoBERT training version as a fourth model.
- Re-tuning models against the frozen test set.
- Re-generating the frozen test conditions in place.
- Changing the split manifest hashes to match altered files.
- Adding a new model solely because it improves one obfuscation family after observing the existing test results.

Any future model or preprocessing experiment should be declared as a separate experiment with its own protocol, configuration, and evaluation boundary before the final test set is inspected.
