# IndoBERT v2 Training Summary

Generated: 2026-10-13T11:43:30.466697+00:00

## Outcome

- Experiment: `indobert_v2_epoch_budget`
- Status: **SUCCESS**
- Selected candidate: **D_lr3e-5_wd0.01**
- Model base: `indobenchmark/indobert-base-p2`
- Pretrained revision: `94b4e0a82081fa57f227fcc2024d1ea89b57ac1f`
- Test data used during model selection: **False**

## Selected model — validation results

| Metric | Value |
|---|---:|
| F1 — Promotion | 0.1178 (11.78%) |
| Precision — Promotion | 0.1184 (11.84%) |
| Recall — Promotion | 0.1172 (11.72%) |
| Accuracy | 0.7889 (78.89%) |
| Macro F1 | 0.4989 (49.89%) |
| True negatives | 3189 |
| False positives | 432 |
| False negatives | 437 |
| True positives | 58 |

## Candidate comparison

| Candidate | LR | Weight decay | Best epoch | Runtime (min) | F1 | Precision | Recall | Macro F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| D_lr3e-5_wd0.01 | 3.0e-05 | 0.010 | 6.00 | 26.32 | 0.1178 | 0.1184 | 0.1172 | 0.4989 |
| C_lr3e-5_wd0 | 3.0e-05 | 0.000 | 2.00 | 17.54 | 0.1152 | 0.1152 | 0.1152 | 0.4971 |
| A_lr2e-5_wd0 | 2.0e-05 | 0.000 | 3.00 | 22.44 | 0.1150 | 0.1149 | 0.1152 | 0.4970 |
| B_lr2e-5_wd0.01 | 2.0e-05 | 0.010 | 2.00 | 17.49 | 0.1144 | 0.1157 | 0.1131 | 0.4974 |

## Data and protocol

- Training rows: 32,920
- Validation rows: 4,116
- Training SHA-256: `65a10e93713586e20ebb9a3a0c0694d860a6d9d5541e84000713f2918d595cf3`
- Validation SHA-256: `7753fb36275d36a2367e15d28de3f52f06e0f33a4f666d81d7dd95c5a9d87038`
- Maximum sequence length: 128
- Padding: dynamic per batch, pad_to_multiple_of_8
- Maximum epochs: 6
- Early stopping patience: 2
- Effective training batch size: 32
- CUDA profile: `Tesla T4`
- Mixed precision: `bf16`
- Optimizer: `adamw_torch_fused`
- Attention backend: `sdpa`
- Class weights: `{"Non-Promotion": 0.5683701657458563, "Promotion": 4.156565656565657}`
- Primary selection metric: validation F1 for Promotion; test and obfuscated-test data are not used in this training-selection workflow.

## Local inference

1. Extract this ZIP.
2. Install a compatible Python and dependencies: `python -m pip install -r requirements.txt`.
3. Prepare a CSV with a text column (default: `text_raw`).
4. Run: `python inference.py --input comments.csv --text-column text_raw --output predictions.csv`.

Inference chooses CUDA automatically when PyTorch can access a GPU; otherwise it uses CPU. It loads model files from the bundled `model/` directory and does not download model weights.

## Interpretation and limitations

- Metrics in this report are from the normal validation set, not the held-out test set.
- Selection metrics estimate validation performance and should not be described as final test performance.
- The model predicts the two labels defined in the bundled model config: Non-Promotion and Promotion.
- The ZIP intentionally excludes training/validation source CSVs and all test/obfuscated-test datasets. Validation predictions are included for auditability.

## Included files

- `model/`: selected Hugging Face model and tokenizer files.
- `inference.py`, `requirements.txt`: local inference runner and dependencies.
- `reports/`: run manifest, candidate summary, per-candidate results, training histories, and validation predictions.
- `SHA256SUMS.txt`: SHA-256 checksums for bundled files (excluding the checksum list itself).
