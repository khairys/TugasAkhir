# Research Handoff — Stage 11 Robustness Analysis

**Research title:** Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube  
**Active branch:** stage11-robustness-analysis  
**Prior head before validation work:** b68e1a04996337f3447cb2e9bf6e8331aae1f6c0

## Research scope

The primary comparison is fixed to Linear SVM with word-level TF-IDF, Char-CNN, and the fine-tuned IndoBERT baseline. The task is binary classification of Indonesian YouTube comments (0 = Non-Promotion, 1 = Promotion). The primary metric is Promotion F1.

Stage 11 analyzes saved Stage 10 predictions across eight O1–O4 obfuscation conditions and reports secondary OOD/external evaluation on DS3 and DS5. It does not train a new model or use DS3/DS5 for tuning.

## Results package

- Primary result tables and 95% paired-bootstrap intervals: reports/stage11/primary/
- Domain-shift predictions and metrics for all six model-dataset combinations: reports/stage11/domain_shift/
- Frozen candidate datasets and their manifest: data/processed/stage11/
- AI-assisted text-only first-pass annotations for 113 error candidates: reports/stage11/primary/error_review_candidates.csv
- Numerical analysis script: scripts/analysis/stage11_robustness_analysis.py
- Artifact validator: scripts/validation/validate_stage11_artifacts.py
- Focused tests: tests/stage11/
- GitHub Actions workflow: .github/workflows/stage11-validation.yml

## Findings in the saved artifacts

- Char-CNN has the highest clean-test Promotion F1 (0.9786) and the smallest mean paired F1 drop across eight obfuscation conditions (0.0037; retention 99.62%).
- Linear SVM has mean paired F1 drop 0.0569 (retention 93.98%); whitespace O3 is its largest-degradation family on average.
- IndoBERT has mean paired F1 drop 0.0839 (retention 91.27%); Unicode/orthographic O4 is its clearest weakness.
- Domain-shift ranking differs: saved IndoBERT results have the highest Promotion F1 on DS3 OOD (0.4643) and DS5 external (0.9547). This does not conflict with Char-CNN being strongest under controlled obfuscation; these are different evaluation dimensions.

These findings are read from existing prediction/metric artifacts. The focused validation workflow checks artifact integrity and metric consistency; it does not independently retrain models or regenerate inference.

## Closure approach

Stage 11 saved-artifact analysis is treated as complete when the artifact validator and focused tests pass on this branch. The 113 rows have AI-assisted text-only first-pass annotations; they are not represented as independent human adjudication. The gold labels remain unchanged, and individual causal claims still require careful research interpretation.

The successful GitHub Actions run [#38949243961](https://github.com/khairys/TugasAkhir/actions/runs/38949243961) completed on 17 October 2026: the artifact validator returned PASSED with 0 errors, and `tests/stage11` returned 4 passed. This applies to saved-artifact validation and the focused Stage 11 tests, not to fresh inference or the full repository test suite.

## Known caveats

1. Tracked train/validation CSVs do not match the official split-manifest hashes. Restore the original snapshot before claiming end-to-end training reproducibility; do not edit the manifest to fit different data.
2. The raw DS5 hash differs from the official-source hash. The evaluated frozen DS5 candidate hash is recorded; do not rebuild or overwrite the candidate until provenance is reconciled.
3. IndoBERT weights are intentionally excluded from Git because of file size. They are not needed to validate saved predictions/metrics, but fresh inference requires the external weight file to match SHA-256 890dd84c8f25f2d0761959335c5bc00c76b396cf6065317d7589ee84d3ddafbd.
4. AI-assisted semantic review is text-only and does not establish independent human adjudication or causal mechanisms.

## Reviewer entry points

- Analysis: docs/research/STAGE11_ROBUSTNESS_ANALYSIS.md
- Checklist: docs/handoff/STAGE11_EXECUTION_CHECKLIST.md
- Reproducibility guide: docs/handoff/REPRODUCIBILITY_GUIDE.md
- Repository audit: docs/handoff/REPOSITORY_AUDIT.md
- Validation report: docs/handoff/STAGE11_VALIDATION_REPORT.md
