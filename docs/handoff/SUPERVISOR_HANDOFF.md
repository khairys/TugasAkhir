# Research Handoff — Stage 10

**Research:** *Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube*

The main comparison is locked to three models: **Linear SVM, Char-CNN, and IndoBERT** (the original fine-tuned baseline). The cleaned branch removes the unused later-IndoBERT implementation and its model-specific outputs while preserving the scientific rationale for selecting the original checkpoint.

## Start here

1. [Canonical model-selection decision](../research/MODEL_SELECTION_DECISION.md) — the selected model lineup and rationale.
2. [Final research results](../research/FINAL_RESULTS.md) — main results, research questions, and limitations.
3. [Future analysis plan](../research/FUTURE_ANALYSIS_PLAN.md) — the default next analysis sequence and explicit out-of-scope items.
4. [Repository audit](REPOSITORY_AUDIT.md) — project structure, what was retained/removed, and remaining issues.
5. [Reproducibility guide](REPRODUCIBILITY_GUIDE.md) — input hashes, canonical artifacts, standard evaluation path, and checks.
6. [Stage 10 closure checklist](STAGE10_CLOSURE_CHECKLIST.md) — remaining release blockers.
7. [Formal obfuscation specification](../research/OBFUSCATION_SPECIFICATION_V1.md) — frozen O1–O4 transformation protocol.
8. [Dataset audit report](../data/DATASET_AUDIT_REPORT.md) and [labeling guideline](../data/LABELING_GUIDELINE.md) — source and label provenance.
9. [Stage 11 robustness analysis](../research/STAGE11_ROBUSTNESS_ANALYSIS.md) — absolute performance, paired robustness, obfuscation family matrix, severity, uncertainty, and domain-shift status.
10. [Stage 11 execution checklist](STAGE11_EXECUTION_CHECKLIST.md) — exact commands and open release gates.

## Stage 11 execution status

The Stage 11 branch now contains a primary-analysis script, an initial result snapshot based on the saved Stage 10 aggregate tables, and an inference-only DS3/DS5 runner. The snapshot is explicitly marked preliminary; running `scripts/analysis/stage11_robustness_analysis.py` from a clean local checkout regenerates the condition-level metrics and paired bootstrap intervals from individual prediction files.

The DS3 OOD and DS5 external candidate CSVs are prepared but have not been evaluated. The DS5 raw source hash currently differs from the official hash recorded in the manifest, so the preparation script blocks rebuilding those files until the audited source snapshot is restored. IndoBERT domain evaluation also remains blocked until the selected `model.safetensors` bundle is restored and its SHA-256 verified. Do not describe Stage 11 or the repository as fully reproducible until these checks and runtime tests pass.

## Main findings

On the reported frozen test protocol, Char-CNN has the highest normal-test Promotion F1 (0.9786) and wins all eight paired obfuscation conditions. The canonical models' unweighted mean paired F1 values are 0.9763 for Char-CNN, 0.8876 for Linear SVM, and 0.8771 for IndoBERT. The largest IndoBERT failure occurs under Unicode homoglyph obfuscation (O4), with a paired F1 of 0.6323 under O4 strong.

The choice to retain the original IndoBERT baseline rather than a later training experiment is documented in the model-selection decision. The later experiment improved O4 modestly but did not improve robustness on average and is no longer part of the active repository.

## Remaining release caveats

- The frozen train/validation CSVs do not currently match the SHA-256 values recorded in the split manifest. Recover and verify the original frozen split snapshot.
- The selected IndoBERT model weights are not tracked in Git and must be supplied as a verified artifact bundle.
- Full Stage 10 inference and the complete test suite have not been rerun after the repository cleanup. Do not claim runtime verification until those checks pass.

The main scientific comparison and the reproducible artifact handoff are separate: the results can be reported with their stated limitations, while the release checklist remains open until the blockers are resolved.
