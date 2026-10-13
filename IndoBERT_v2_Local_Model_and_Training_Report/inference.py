#!/usr/bin/env python3
"""Run local inference with the bundled IndoBERT v2 model (no model download required)."""
from pathlib import Path
import argparse
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "model"
MAX_LENGTH = 128  # Must match the training manifest.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--text-column", default="text_raw", help="Column containing comments")
    parser.add_argument("--output", default="predictions.csv", help="Output CSV path")
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    if args.batch_size < 1:
        parser.error("--batch-size must be >= 1")
    if not (MODEL_DIR / "config.json").is_file() or not (MODEL_DIR / "model.safetensors").is_file():
        raise FileNotFoundError(f"Model files not found in {MODEL_DIR}")

    data = pd.read_csv(args.input)
    if args.text_column not in data.columns:
        raise ValueError(f"Text column {args.text_column!r} not found. Columns: {list(data.columns)}")
    if data[args.text_column].isna().any():
        raise ValueError(f"Input column {args.text_column!r} contains missing values.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR), local_files_only=True)
    model.to(device)
    model.eval()

    id2label = {int(k): v for k, v in model.config.id2label.items()}
    if not id2label:
        id2label = {0: "Non-Promotion", 1: "Promotion"}

    texts = data[args.text_column].astype(str).tolist()
    predicted_ids, promotion_probabilities = [], []
    with torch.inference_mode():
        for start in range(0, len(texts), args.batch_size):
            batch = texts[start:start + args.batch_size]
            encoded = tokenizer(
                batch, padding=True, truncation=True, max_length=MAX_LENGTH,
                return_tensors="pt"
            )
            encoded = {k: v.to(device) for k, v in encoded.items()}
            logits = model(**encoded).logits.float()
            probs = torch.softmax(logits, dim=-1)
            preds = probs.argmax(dim=-1)
            predicted_ids.extend(preds.cpu().tolist())
            promotion_probabilities.extend(probs[:, 1].cpu().tolist())

    output = data.copy()
    output["pred_label_id"] = predicted_ids
    output["pred_label"] = [id2label.get(i, str(i)) for i in predicted_ids]
    output["prob_promotion"] = promotion_probabilities
    output.to_csv(args.output, index=False)
    print(f"Device: {device}")
    print(f"Rows predicted: {len(output):,}")
    print(f"Saved: {Path(args.output).resolve()}")

if __name__ == "__main__":
    main()
