# Stage 10 Closure Checklist

The main comparison is locked to exactly three models: **Linear SVM, Char-CNN, and IndoBERT** using the original baseline checkpoint. The cleaned branch has removed the unused later-IndoBERT implementation, standalone robustness outputs, and alternate training script; its selection rationale is retained in `docs/research/MODEL_SELECTION_DECISION.md`.

## Scientific analysis

- [x] Normal-test baseline and eight paired obfuscation conditions reported for the three canonical models.
- [x] Paired metrics restricted to successful transformations (`changed == True`).
- [x] Main pattern documented: Char-CNN is most robust across the tested conditions.
- [x] IndoBERT Unicode-homoglyph failure mode documented.
- [x] Model selection fixed and reflected in the machine-readable `configs/model_registry.json`.
- [x] Naming and directory structure reorganized around `models/{linear_svm,char_cnn,indobert}/`.

## Release and reproducibility — still open

- [ ] Recover the original frozen train/validation snapshot that matches the hashes in `data/splits/v1/split_manifest_v1.json`. Do not change manifest hashes to fit the currently tracked files.
- [ ] Supply the selected IndoBERT `model.safetensors` bundle and verify it against the SHA-256 in `configs/evaluation/stage10_robustness.json`.
- [ ] Run `python scripts/22_run_stage10_robustness.py --mode preflight` on the exact cleaned branch.
- [ ] Run `python scripts/23_validate_stage10_results.py` and `pytest tests/` after prerequisites are restored; record the real results.
- [ ] Audit configuration and manifests after the path reorganization to ensure every referenced input/artifact exists or is explicitly listed as a required external artifact.

## Closure recommendation

The scientific comparison is complete as a descriptive analysis of one frozen test split. The selected model lineup is stable and contains no separate IndoBERT training versions. The repository release should not be described as fully reproducible until split integrity, selected-model weight handoff, and runtime validation are complete.
