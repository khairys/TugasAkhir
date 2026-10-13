# IndoBERT v2 local bundle

This bundle contains the selected model from experiment `indobert_v2_epoch_budget`.

- Selected candidate: `D_lr3e-5_wd0.01`
- Model directory: `model/`
- Local inference: `python inference.py --input comments.csv --text-column text_raw --output predictions.csv`
- Training summary: `TRAINING_SUMMARY.md`
- Full run manifest: `reports/indobert_v2_epoch_budget_manifest.json`

Install dependencies with `python -m pip install -r requirements.txt`. The inference script loads only the local `model/` directory. CUDA is optional; CPU inference is supported.

Use the model as a binary classifier for the task represented in the training data. Review `TRAINING_SUMMARY.md` for validation metrics and limitations before reporting results.
