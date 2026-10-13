#!/usr/bin/env python3
"""
scripts/22_run_stage10_robustness.py - Stage 10 Official Robustness Evaluation
Linear SVM vs Character-level CNN vs IndoBERT

Evaluates 3 models across:
- 1 Normal test condition (test_normal_v1.csv, 4,116 rows)
- 8 Obfuscation conditions (O1_MILD, O1_STRONG, O2_MILD, O2_STRONG, O3_MILD, O3_STRONG, O4_MILD, O4_STRONG, 4,116 rows each)
Total: 27 model-condition combinations (111,132 predictions).

Computes:
- Full-set metrics for each model-condition
- Paired robustness metrics on changed == True subset (F1 Drop, Relative Drop, Retention)
- Evasion flip and false-negative analysis
- 95% Bootstrap Confidence Intervals (10,000 stratified paired resamples, seed 42)
- Source dataset stratified metrics
"""

import os
import sys
import argparse
import importlib.util
import hashlib
import json
import time
import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix

# Global configuration defaults
CONFIG_PATH = "configs/evaluation/stage10_robustness.json"


def sha256_file(filepath):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# -----------------------------------------------------------------------------
# Model Loaders and Predictors
# -----------------------------------------------------------------------------

def load_svm_pipeline(model_path):
    """Load trained Linear SVM pipeline from joblib artifact."""
    import joblib
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"SVM model not found: {model_path}")
    pipeline = joblib.load(model_path)
    return pipeline


def predict_svm(pipeline, texts):
    """Predict using Linear SVM pipeline. Returns preds (0/1) and decision scores."""
    preds = pipeline.predict(texts).astype(int)
    # Decision score from LinearSVC decision_function
    if hasattr(pipeline, "decision_function"):
        scores = pipeline.decision_function(texts).astype(float)
    else:
        scores = np.zeros(len(preds), dtype=float)
    return preds, scores


class CharCNNModule:
    """Wrapper for Character-level CNN inference."""

    def __init__(self, model_path, vocab_path, device="cpu"):
        import torch
        import torch.nn as nn
        import torch.nn.functional as F

        self.torch = torch
        self.device = torch.device(device)

        # 1. Load vocabulary
        with open(vocab_path, "r", encoding="utf-8") as f:
            self.vocab = json.load(f)
        self.stoi = self.vocab["stoi"]
        self.pad_id = self.vocab.get("pad_id", 0)
        self.unk_id = self.vocab.get("unk_id", 1)
        self.max_length = 576

        # 2. Define Model Class
        class _CharCNN(nn.Module):
            def __init__(self, vocab_size, embedding_dim=32, kernel_sizes=(3, 5, 7),
                         conv_channels=64, hidden_dim=128, dropout=0.5, pad_id=0):
                super().__init__()
                self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_id)
                self.convs = nn.ModuleList([
                    nn.Conv1d(embedding_dim, conv_channels, kernel_size=k, padding=k // 2)
                    for k in kernel_sizes
                ])
                self.fc1 = nn.Linear(conv_channels * len(kernel_sizes), hidden_dim)
                self.dropout = nn.Dropout(dropout)
                self.fc2 = nn.Linear(hidden_dim, 2)

            def forward(self, input_ids, lengths):
                z = self.embedding(input_ids).transpose(1, 2)
                positions = torch.arange(input_ids.shape[1], device=input_ids.device).unsqueeze(0)
                valid = (positions < lengths.unsqueeze(1)).unsqueeze(1)
                pooled = []
                for conv in self.convs:
                    h = F.relu(conv(z))
                    h = h.masked_fill(~valid, torch.finfo(h.dtype).min)
                    pooled.append(h.amax(dim=-1))
                x = torch.cat(pooled, dim=1)
                x = F.relu(self.fc1(x))
                x = self.dropout(x)
                return self.fc2(x)

        # 3. Load Model State Dict
        payload = torch.load(model_path, map_location=self.device, weights_only=False)
        args = payload.get("model_args", {
            "vocab_size": len(self.vocab["itos"]),
            "embedding_dim": 32,
            "kernel_sizes": [3, 5, 7],
            "conv_channels": 64,
            "hidden_dim": 128,
            "dropout": 0.5,
            "pad_id": self.pad_id
        })
        self.model = _CharCNN(**args).to(self.device)
        self.model.load_state_dict(payload["model_state_dict"])
        self.model.eval()

    def encode_texts(self, texts):
        """Encode a list of text strings into input_ids and lengths tensors."""
        batch_size = len(texts)
        input_ids = np.full((batch_size, self.max_length), self.pad_id, dtype=np.int64)
        lengths = np.zeros(batch_size, dtype=np.int64)

        for i, text in enumerate(texts):
            text_str = "" if pd.isna(text) else str(text)
            chars = list(text_str)[:self.max_length]
            length = len(chars)
            lengths[i] = max(1, length)
            for j, ch in enumerate(chars):
                input_ids[i, j] = self.stoi.get(ch, self.unk_id)

        return (
            self.torch.tensor(input_ids, dtype=self.torch.long, device=self.device),
            self.torch.tensor(lengths, dtype=self.torch.long, device=self.device)
        )

    def predict(self, texts, batch_size=128):
        """Batch inference returning predicted class (0/1) and promotion probability."""
        all_preds = []
        all_probs = []

        with self.torch.inference_mode():
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_ids, batch_lengths = self.encode_texts(batch_texts)
                logits = self.model(batch_ids, batch_lengths)
                probs = self.torch.softmax(logits, dim=1)[:, 1]
                preds = self.torch.argmax(logits, dim=1)

                all_preds.extend(preds.cpu().numpy().tolist())
                all_probs.extend(probs.cpu().numpy().tolist())

        return np.array(all_preds, dtype=int), np.array(all_probs, dtype=float)


class IndoBERTModule:
    """Wrapper for IndoBERT sequence classification inference."""

    def __init__(self, model_dir, device="cpu"):
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        self.torch = torch
        self.device = torch.device(device)
        self.max_length = 128

        if self.device.type == "cpu":
            self.torch.set_num_threads(os.cpu_count() or 4)

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir, local_files_only=True).to(self.device)
        self.model.eval()

        # Verify label mapping
        id2label = getattr(self.model.config, "id2label", {0: "Non-Promotion", 1: "Promotion"})
        assert str(id2label.get(1, id2label.get("1", ""))).lower().startswith("prom"), "Label 1 must be Promotion"

    def predict(self, texts, batch_size=64):
        """Batch inference with length-sorted bucketed batching for maximal CPU throughput."""
        clean_texts = ["" if pd.isna(t) else str(t) for t in texts]
        total = len(clean_texts)
        if total == 0:
            return np.array([], dtype=int), np.array([], dtype=float)

        # Sort indices by text length so batches have minimal padding waste
        lengths = [len(t) for t in clean_texts]
        sort_indices = np.argsort(lengths)
        sorted_texts = [clean_texts[idx] for idx in sort_indices]

        all_preds = []
        all_probs = []

        with self.torch.inference_mode():
            for i in range(0, total, batch_size):
                batch = sorted_texts[i:i + batch_size]
                inputs = self.tokenizer(
                    batch,
                    max_length=self.max_length,
                    padding=True,
                    truncation=True,
                    return_tensors="pt"
                ).to(self.device)

                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = self.torch.softmax(logits, dim=-1)[:, 1]
                preds = self.torch.argmax(logits, dim=-1)

                all_preds.extend(preds.cpu().numpy().tolist())
                all_probs.extend(probs.cpu().numpy().tolist())

                done = min(i + batch_size, total)
                if done % 1000 < batch_size or done == total:
                    print(f"   [IndoBERT] Processed {done}/{total} samples...", flush=True)

        sorted_preds = np.array(all_preds, dtype=int)
        sorted_probs = np.array(all_probs, dtype=float)

        # Restore original order
        reverse_indices = np.empty_like(sort_indices)
        reverse_indices[sort_indices] = np.arange(total)

        return sorted_preds[reverse_indices], sorted_probs[reverse_indices]


# -----------------------------------------------------------------------------
# Metric Calculations
# -----------------------------------------------------------------------------

def calculate_classification_metrics(y_true, y_pred):
    """Calculate binary Promotion classification metrics."""
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)

    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, labels=[0, 1], zero_division=0
    )
    acc = accuracy_score(y_true, y_pred)
    _, _, macro_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    return {
        "precision_promotion": float(precision[1]),
        "recall_promotion": float(recall[1]),
        "f1_promotion": float(f1[1]),
        "accuracy": float(acc),
        "macro_f1": float(macro_f1),
        "precision_non_promotion": float(precision[0]),
        "recall_non_promotion": float(recall[0]),
        "f1_non_promotion": float(f1[0]),
        "support_non_promotion": int(support[0]),
        "support_promotion": int(support[1]),
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
        "TP": int(tp),
        "total_samples": int(len(y_true))
    }


def run_stratified_paired_bootstrap(y_true, y_norm, y_obf, n_resamples=10000, seed=42):
    """
    Run stratified paired bootstrap to compute 95% Confidence Interval for F1 Drop.
    Resamples indices within class 0 and class 1 independently.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_norm = np.asarray(y_norm, dtype=int)
    y_obf = np.asarray(y_obf, dtype=int)

    idx_0 = np.where(y_true == 0)[0]
    idx_1 = np.where(y_true == 1)[0]
    n0, n1 = len(idx_0), len(idx_1)

    rng = np.random.default_rng(seed)
    f1_drops = []

    for _ in range(n_resamples):
        boot_idx_0 = rng.choice(idx_0, size=n0, replace=True)
        boot_idx_1 = rng.choice(idx_1, size=n1, replace=True)
        boot_idx = np.concatenate([boot_idx_0, boot_idx_1])

        yt_b = y_true[boot_idx]
        yn_b = y_norm[boot_idx]
        yo_b = y_obf[boot_idx]

        # F1 normal
        _, _, fn, _ = precision_recall_fscore_support(yt_b, yn_b, labels=[1], average="binary", zero_division=0)
        # F1 obfuscated
        _, _, fo, _ = precision_recall_fscore_support(yt_b, yo_b, labels=[1], average="binary", zero_division=0)

        f1_drops.append(float(fn - fo))

    ci_lower = float(np.percentile(f1_drops, 2.5))
    ci_upper = float(np.percentile(f1_drops, 97.5))
    ci_mean = float(np.mean(f1_drops))
    ci_std = float(np.std(f1_drops))

    return {
        "bootstrap_f1_drop_mean": ci_mean,
        "bootstrap_f1_drop_std": ci_std,
        "ci_95_lower": ci_lower,
        "ci_95_upper": ci_upper
    }


# -----------------------------------------------------------------------------
# Preflight Checker
# -----------------------------------------------------------------------------

def run_preflight(config):
    """Verify all prerequisites, data files, hashes, and run a smoke prediction."""
    print("=" * 76)
    print("  STAGE 10 PREFLIGHT VALIDATION CHECK")
    print("=" * 76)

    failures = []
    checks_passed = 0

    # 1. Check datasets and hashes
    print("\n--- 1. DATASET FILE INTEGRITY & HASH CHECK ---")
    all_files = [("NORMAL", config["datasets"]["test_normal"]["path"], config["datasets"]["test_normal"]["sha256"])]
    for cond in config["datasets"]["obfuscation_conditions"]:
        all_files.append((cond["condition_id"], cond["path"], cond["sha256"]))

    for cond_name, p, exp_hash in all_files:
        if not os.path.exists(p):
            msg = f"Dataset file missing: {p}"
            print(f" [FAIL] {msg}")
            failures.append(msg)
            continue
        act_hash = sha256_file(p)
        if act_hash == exp_hash:
            print(f" [PASS] {cond_name:<10}: Hash matched ({act_hash[:16]}...)")
            checks_passed += 1
        else:
            msg = f"Hash mismatch for {cond_name}: expected {exp_hash}, got {act_hash}"
            print(f" [FAIL] {msg}")
            failures.append(msg)

    # 2. Check model artifacts
    print("\n--- 2. MODEL ARTIFACTS CHECK ---")
    models_cfg = config["models"]

    # SVM
    svm_p = models_cfg["linear_svm"]["model_path"]
    svm_hash = models_cfg["linear_svm"]["sha256"]
    if os.path.exists(svm_p) and sha256_file(svm_p) == svm_hash:
        print(f" [PASS] Linear SVM pipeline artifact verified ({svm_p})")
        checks_passed += 1
    else:
        msg = f"Linear SVM artifact invalid or missing: {svm_p}"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    # Char-CNN
    cnn_p = models_cfg["char_cnn"]["model_weights_path"]
    cnn_h = models_cfg["char_cnn"]["model_weights_sha256"]
    vocab_p = models_cfg["char_cnn"]["vocab_path"]
    vocab_h = models_cfg["char_cnn"]["vocab_sha256"]
    if os.path.exists(cnn_p) and sha256_file(cnn_p) == cnn_h and os.path.exists(vocab_p) and sha256_file(vocab_p) == vocab_h:
        print(f" [PASS] Char-CNN model and vocab artifacts verified ({cnn_p})")
        checks_passed += 1
    else:
        msg = f"Char-CNN artifacts invalid or missing"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    # IndoBERT
    ib_dir = models_cfg["indobert"]["model_dir"]
    ib_weights = models_cfg["indobert"]["model_weights_path"]
    ib_h = models_cfg["indobert"]["model_weights_sha256"]
    if os.path.exists(ib_weights) and sha256_file(ib_weights) == ib_h:
        print(f" [PASS] IndoBERT model weights verified ({ib_weights})")
        checks_passed += 1
    else:
        msg = f"IndoBERT weights invalid or missing: {ib_weights}"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    # 3. Check environment libraries and GPU
    print("\n--- 3. RUNTIME & DEVICE CHECK ---")
    device = "cuda" if os.environ.get("USE_GPU") == "1" else "cpu"
    try:
        import torch
        if torch.cuda.is_available():
            print(f" [INFO] CUDA available! Found: {torch.cuda.get_device_name(0)}")
            device = "cuda"
        else:
            print(" [INFO] CUDA not available, using CPU device.")
            device = "cpu"
    except ImportError:
        print(" [WARN] Torch not installed yet.")

    print(f" [INFO] Inference device selected: {device}")

    # 4. Smoke Test Model Inference
    print("\n--- 4. SMOKE INFERENCE TEST (2 SAMPLES) ---")
    sample_texts = [
        "Terima kasih infonya bang sangat bermanfaat",
        "Daftar sekarang di link bio bonus new member 100%!"
    ]

    try:
        # SVM smoke
        svm_pipe = load_svm_pipeline(svm_p)
        svm_preds, svm_scores = predict_svm(svm_pipe, sample_texts)
        assert len(svm_preds) == 2
        print(" [PASS] Linear SVM smoke inference passed.")
        checks_passed += 1
    except Exception as e:
        msg = f"Linear SVM smoke inference failed: {e}"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    try:
        # Char-CNN smoke
        cnn_mod = CharCNNModule(cnn_p, vocab_p, device=device)
        cnn_preds, cnn_probs = cnn_mod.predict(sample_texts)
        assert len(cnn_preds) == 2
        print(" [PASS] Char-CNN smoke inference passed.")
        checks_passed += 1
    except Exception as e:
        msg = f"Char-CNN smoke inference failed: {e}"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    try:
        # IndoBERT smoke
        ib_mod = IndoBERTModule(ib_dir, device=device)
        ib_preds, ib_probs = ib_mod.predict(sample_texts)
        assert len(ib_preds) == 2
        print(" [PASS] IndoBERT smoke inference passed.")
        checks_passed += 1
    except Exception as e:
        msg = f"IndoBERT smoke inference failed: {e}"
        print(f" [FAIL] {msg}")
        failures.append(msg)

    print("\n" + "=" * 76)
    print(f"Preflight Checks Passed: {checks_passed}")
    print(f"Preflight Checks Failed: {len(failures)}")
    if len(failures) == 0:
        print(">>> RESULT: [PASS] PREFLIGHT SUCCEEDED. READY FOR OFFICIAL EVALUATION <<<")
        print("=" * 76)
        return True, device
    else:
        print(">>> RESULT: [FAIL] PREFLIGHT FAILED WITH ERRORS <<<")
        for f in failures:
            print(f" - {f}")
        print("=" * 76)
        return False, device


# -----------------------------------------------------------------------------
# Official Evaluation Execution Engine
# -----------------------------------------------------------------------------

def run_official_evaluation(config, device="cpu", resume=True):
    """Execute complete Stage 10 robustness evaluation."""
    start_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"\nSTARTING OFFICIAL STAGE 10 ROBUSTNESS EVALUATION: {start_time.isoformat()}")

    # Setup directories
    reports_dir = Path("reports/stage10")
    pred_dir = reports_dir / "predictions"
    svm_pred_dir = pred_dir / "svm"
    cnn_pred_dir = pred_dir / "char_cnn"
    ib_pred_dir = pred_dir / "indobert"

    for d in [svm_pred_dir, cnn_pred_dir, ib_pred_dir]:
        d.mkdir(parents=True, exist_ok=True)

    models_cfg = config["models"]

    # 1. Load Datasets
    print("\nLoading test datasets into memory...")
    normal_df = pd.read_csv(config["datasets"]["test_normal"]["path"])
    print(f"Loaded normal test: {len(normal_df)} rows")

    obf_dfs = {}
    for cond in config["datasets"]["obfuscation_conditions"]:
        cid = cond["condition_id"]
        df_c = pd.read_csv(cond["path"])
        obf_dfs[cid] = df_c
        print(f"Loaded {cid}: {len(df_c)} rows (changed={df_c['changed'].sum()})")

    # 2. Model 1: Linear SVM
    print("\n" + "=" * 60)
    print("1. RUNNING LINEAR SVM INFERENCE")
    print("=" * 60)
    svm_pipe = load_svm_pipeline(models_cfg["linear_svm"]["model_path"])

    # Normal
    svm_norm_file = svm_pred_dir / "test_normal_predictions.csv"
    if resume and svm_norm_file.exists():
        print(f" [RESUME] Found existing {svm_norm_file}")
        svm_norm_df = pd.read_csv(svm_norm_file)
    else:
        print(" Predicting test_normal with Linear SVM...")
        texts = normal_df["text_original"].fillna("").astype(str).tolist()
        preds, scores = predict_svm(svm_pipe, texts)
        svm_norm_df = pd.DataFrame({
            "source_record_id": normal_df["source_record_id"],
            "canonical_label": normal_df["canonical_label"],
            "predicted_label": preds,
            "decision_score": scores,
            "is_correct": (preds == normal_df["canonical_label"]),
            "model": "linear_svm",
            "condition": "NORMAL"
        })
        svm_norm_df.to_csv(svm_norm_file, index=False)
        print(f" Saved: {svm_norm_file}")

    # Obfuscations
    svm_obf_dfs = {}
    for cid, df_c in obf_dfs.items():
        svm_cond_file = svm_pred_dir / f"{cid}_predictions.csv"
        if resume and svm_cond_file.exists():
            print(f" [RESUME] Found existing {svm_cond_file}")
            svm_obf_dfs[cid] = pd.read_csv(svm_cond_file)
        else:
            print(f" Predicting {cid} with Linear SVM...")
            texts = df_c["text_obfuscated"].fillna("").astype(str).tolist()
            preds, scores = predict_svm(svm_pipe, texts)
            df_out = pd.DataFrame({
                "source_record_id": df_c["source_record_id"],
                "canonical_label": df_c["canonical_label"],
                "predicted_label": preds,
                "decision_score": scores,
                "is_correct": (preds == df_c["canonical_label"]),
                "changed": df_c["changed"],
                "model": "linear_svm",
                "condition": cid
            })
            df_out.to_csv(svm_cond_file, index=False)
            svm_obf_dfs[cid] = df_out
            print(f" Saved: {svm_cond_file}")

    del svm_pipe

    # 3. Model 2: Character-level CNN
    print("\n" + "=" * 60)
    print("2. RUNNING CHARACTER-LEVEL CNN INFERENCE")
    print("=" * 60)
    cnn_mod = CharCNNModule(
        models_cfg["char_cnn"]["model_weights_path"],
        models_cfg["char_cnn"]["vocab_path"],
        device=device
    )

    # Normal
    cnn_norm_file = cnn_pred_dir / "test_normal_predictions.csv"
    if resume and cnn_norm_file.exists():
        print(f" [RESUME] Found existing {cnn_norm_file}")
        cnn_norm_df = pd.read_csv(cnn_norm_file)
    else:
        print(" Predicting test_normal with Char-CNN...")
        texts = normal_df["text_original"].fillna("").astype(str).tolist()
        preds, probs = cnn_mod.predict(texts)
        cnn_norm_df = pd.DataFrame({
            "source_record_id": normal_df["source_record_id"],
            "canonical_label": normal_df["canonical_label"],
            "predicted_label": preds,
            "promotion_probability": probs,
            "is_correct": (preds == normal_df["canonical_label"]),
            "model": "char_cnn",
            "condition": "NORMAL"
        })
        cnn_norm_df.to_csv(cnn_norm_file, index=False)
        print(f" Saved: {cnn_norm_file}")

    # Obfuscations
    cnn_obf_dfs = {}
    for cid, df_c in obf_dfs.items():
        cnn_cond_file = cnn_pred_dir / f"{cid}_predictions.csv"
        if resume and cnn_cond_file.exists():
            print(f" [RESUME] Found existing {cnn_cond_file}")
            cnn_obf_dfs[cid] = pd.read_csv(cnn_cond_file)
        else:
            print(f" Predicting {cid} with Char-CNN...")
            texts = df_c["text_obfuscated"].fillna("").astype(str).tolist()
            preds, probs = cnn_mod.predict(texts)
            df_out = pd.DataFrame({
                "source_record_id": df_c["source_record_id"],
                "canonical_label": df_c["canonical_label"],
                "predicted_label": preds,
                "promotion_probability": probs,
                "is_correct": (preds == df_c["canonical_label"]),
                "changed": df_c["changed"],
                "model": "char_cnn",
                "condition": cid
            })
            df_out.to_csv(cnn_cond_file, index=False)
            cnn_obf_dfs[cid] = df_out
            print(f" Saved: {cnn_cond_file}")

    del cnn_mod

    # 4. Model 3: IndoBERT
    print("\n" + "=" * 60)
    print("3. RUNNING INDOBERT INFERENCE")
    print("=" * 60)
    ib_mod = IndoBERTModule(models_cfg["indobert"]["model_dir"], device=device)

    # Normal
    ib_norm_file = ib_pred_dir / "test_normal_predictions.csv"
    if resume and ib_norm_file.exists():
        print(f" [RESUME] Found existing {ib_norm_file}")
        ib_norm_df = pd.read_csv(ib_norm_file)
    else:
        print(" Predicting test_normal with IndoBERT...")
        texts = normal_df["text_original"].fillna("").astype(str).tolist()
        preds, probs = ib_mod.predict(texts)
        ib_norm_df = pd.DataFrame({
            "source_record_id": normal_df["source_record_id"],
            "canonical_label": normal_df["canonical_label"],
            "predicted_label": preds,
            "promotion_probability": probs,
            "is_correct": (preds == normal_df["canonical_label"]),
            "model": "indobert",
            "condition": "NORMAL"
        })
        ib_norm_df.to_csv(ib_norm_file, index=False)
        print(f" Saved: {ib_norm_file}")

    # Obfuscations
    ib_obf_dfs = {}
    for cid, df_c in obf_dfs.items():
        ib_cond_file = ib_pred_dir / f"{cid}_predictions.csv"
        if resume and ib_cond_file.exists():
            print(f" [RESUME] Found existing {ib_cond_file}")
            ib_obf_dfs[cid] = pd.read_csv(ib_cond_file)
        else:
            print(f" Predicting {cid} with IndoBERT...")
            texts = df_c["text_obfuscated"].fillna("").astype(str).tolist()
            preds, probs = ib_mod.predict(texts)
            df_out = pd.DataFrame({
                "source_record_id": df_c["source_record_id"],
                "canonical_label": df_c["canonical_label"],
                "predicted_label": preds,
                "promotion_probability": probs,
                "is_correct": (preds == df_c["canonical_label"]),
                "changed": df_c["changed"],
                "model": "indobert",
                "condition": cid
            })
            df_out.to_csv(ib_cond_file, index=False)
            ib_obf_dfs[cid] = df_out
            print(f" Saved: {ib_cond_file}")

    del ib_mod

    # -------------------------------------------------------------------------
    # 5. METRIC AGGREGATION & ROBUSTNESS ANALYSIS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("4. COMPUTING FULL-SET, PAIRED ROBUSTNESS & EVASION METRICS")
    print("=" * 60)

    all_models_norm = {
        "linear_svm": svm_norm_df,
        "char_cnn": cnn_norm_df,
        "indobert": ib_norm_df
    }

    all_models_obf = {
        "linear_svm": svm_obf_dfs,
        "char_cnn": cnn_obf_dfs,
        "indobert": ib_obf_dfs
    }

    # A. Normal Metrics
    norm_metrics_rows = []
    for model_name, df_n in all_models_norm.items():
        m = calculate_classification_metrics(df_n["canonical_label"], df_n["predicted_label"])
        m["model"] = model_name
        m["condition"] = "NORMAL"
        norm_metrics_rows.append(m)

    df_norm_metrics = pd.DataFrame(norm_metrics_rows)
    # Reorder columns
    cols_order = ["model", "condition", "f1_promotion", "precision_promotion", "recall_promotion",
                  "accuracy", "macro_f1", "TN", "FP", "FN", "TP", "total_samples"]
    df_norm_metrics = df_norm_metrics[cols_order]
    df_norm_metrics.to_csv(reports_dir / "test_normal_metrics.csv", index=False)
    print(f" Saved: {reports_dir / 'test_normal_metrics.csv'}")

    # B. Full-set Obfuscation Metrics (24 rows)
    obf_metrics_full_rows = []
    for cond in config["datasets"]["obfuscation_conditions"]:
        cid = cond["condition_id"]
        family = cond["family"]
        severity = cond["severity"]

        for model_name, obf_dict in all_models_obf.items():
            df_o = obf_dict[cid]
            m = calculate_classification_metrics(df_o["canonical_label"], df_o["predicted_label"])
            m["model"] = model_name
            m["condition"] = cid
            m["family"] = family
            m["severity"] = severity
            obf_metrics_full_rows.append(m)

    df_obf_full = pd.DataFrame(obf_metrics_full_rows)
    cols_full = ["model", "condition", "family", "severity", "f1_promotion", "precision_promotion",
                 "recall_promotion", "accuracy", "macro_f1", "TN", "FP", "FN", "TP", "total_samples"]
    df_obf_full = df_obf_full[cols_full]
    df_obf_full.to_csv(reports_dir / "obfuscation_metrics_full.csv", index=False)
    print(f" Saved: {reports_dir / 'obfuscation_metrics_full.csv'}")

    # C. Paired Robustness Metrics & Bootstrap CI (24 rows)
    paired_rows = []
    flip_rows = []
    all_paired_errors = []

    print("\n Computing Paired Robustness & 10,000 Bootstrap Resamples...")
    for cond in config["datasets"]["obfuscation_conditions"]:
        cid = cond["condition_id"]
        family = cond["family"]
        severity = cond["severity"]

        # Base condition dataframe for matching text
        df_cond_base = obf_dfs[cid].set_index("source_record_id")

        for model_name, obf_dict in all_models_obf.items():
            df_n = all_models_norm[model_name].set_index("source_record_id")
            df_o = obf_dict[cid].set_index("source_record_id")

            # Align on source_record_id
            common_ids = df_n.index.intersection(df_o.index)
            df_n_aligned = df_n.loc[common_ids]
            df_o_aligned = df_o.loc[common_ids]
            df_b_aligned = df_cond_base.loc[common_ids]

            # Filter changed == True
            changed_mask = df_b_aligned["changed"].astype(bool)
            n_total = len(common_ids)
            n_changed = int(changed_mask.sum())
            transform_rate = (n_changed / n_total) * 100

            # Paired subsets
            y_true_paired = df_n_aligned.loc[changed_mask, "canonical_label"].values
            y_norm_paired = df_n_aligned.loc[changed_mask, "predicted_label"].values
            y_obf_paired = df_o_aligned.loc[changed_mask, "predicted_label"].values

            # Normal paired metrics
            m_norm_p = calculate_classification_metrics(y_true_paired, y_norm_paired)
            # Obfuscated paired metrics
            m_obf_p = calculate_classification_metrics(y_true_paired, y_obf_paired)

            f1_norm_p = m_norm_p["f1_promotion"]
            f1_obf_p = m_obf_p["f1_promotion"]

            f1_drop = f1_norm_p - f1_obf_p
            rel_drop = (f1_drop / f1_norm_p * 100) if f1_norm_p > 0 else np.nan
            retention = (f1_obf_p / f1_norm_p * 100) if f1_norm_p > 0 else np.nan

            # Bootstrap 95% CI on f1_drop
            boot_res = run_stratified_paired_bootstrap(y_true_paired, y_norm_paired, y_obf_paired, n_resamples=10000, seed=42)

            paired_rows.append({
                "model": model_name,
                "condition": cid,
                "family": family,
                "severity": severity,
                "n_test_records": n_total,
                "n_changed_pairs": n_changed,
                "transformation_rate_pct": round(transform_rate, 2),
                "f1_normal_paired": f1_norm_p,
                "f1_obfuscated_paired": f1_obf_p,
                "f1_drop": f1_drop,
                "relative_drop_pct": rel_drop,
                "f1_retention_pct": retention,
                "ci_95_lower": boot_res["ci_95_lower"],
                "ci_95_upper": boot_res["ci_95_upper"],
                "precision_normal_paired": m_norm_p["precision_promotion"],
                "precision_obfuscated_paired": m_obf_p["precision_promotion"],
                "recall_normal_paired": m_norm_p["recall_promotion"],
                "recall_obfuscated_paired": m_obf_p["recall_promotion"],
                "accuracy_normal_paired": m_norm_p["accuracy"],
                "accuracy_obfuscated_paired": m_obf_p["accuracy"],
                "macro_f1_normal_paired": m_norm_p["macro_f1"],
                "macro_f1_obfuscated_paired": m_obf_p["macro_f1"],
                "TN_normal": m_norm_p["TN"], "FP_normal": m_norm_p["FP"],
                "FN_normal": m_norm_p["FN"], "TP_normal": m_norm_p["TP"],
                "TN_obfuscated": m_obf_p["TN"], "FP_obfuscated": m_obf_p["FP"],
                "FN_obfuscated": m_obf_p["FN"], "TP_obfuscated": m_obf_p["TP"]
            })

            # D. Evasion & Flip Analysis
            is_prom = (y_true_paired == 1)
            n_prom = int(is_prom.sum())
            n_tp_norm = int(((y_true_paired == 1) & (y_norm_paired == 1)).sum())

            # Evasion flip: actual=1, normal pred=1, obf pred=0
            evasion_flips = ((y_true_paired == 1) & (y_norm_paired == 1) & (y_obf_paired == 0))
            n_evasion = int(evasion_flips.sum())
            evasion_rate = (n_evasion / n_tp_norm * 100) if n_tp_norm > 0 else np.nan

            # Recovery flip: actual=1, normal pred=0, obf pred=1
            recovery_flips = ((y_true_paired == 1) & (y_norm_paired == 0) & (y_obf_paired == 1))
            n_recovery = int(recovery_flips.sum())

            # False Positive introduction: actual=0, normal pred=0, obf pred=1
            new_fp = ((y_true_paired == 0) & (y_norm_paired == 0) & (y_obf_paired == 1))
            n_new_fp = int(new_fp.sum())

            # Total flips (any label change between normal and obfuscated)
            total_flips = int((y_norm_paired != y_obf_paired).sum())

            flip_rows.append({
                "model": model_name,
                "condition": cid,
                "family": family,
                "severity": severity,
                "n_changed_pairs": n_changed,
                "n_prom_in_paired": n_prom,
                "n_tp_normal": n_tp_norm,
                "n_evasion_flips": n_evasion,
                "evasion_flip_rate_pct": evasion_rate,
                "n_recovery_flips": n_recovery,
                "n_new_fp_flips": n_new_fp,
                "total_prediction_flips": total_flips
            })

            # Extract detailed error rows for paired_error_analysis.csv
            error_mask = (y_true_paired != y_obf_paired) | (y_norm_paired != y_obf_paired)
            err_ids = common_ids[changed_mask][error_mask]
            for eid in err_ids:
                row_b = df_b_aligned.loc[eid]
                all_paired_errors.append({
                    "source_record_id": eid,
                    "model": model_name,
                    "condition": cid,
                    "family": family,
                    "severity": severity,
                    "canonical_label": int(row_b["canonical_label"]),
                    "pred_normal": int(df_n_aligned.loc[eid, "predicted_label"]),
                    "pred_obfuscated": int(df_o_aligned.loc[eid, "predicted_label"]),
                    "is_evasion": bool(row_b["canonical_label"] == 1 and df_n_aligned.loc[eid, "predicted_label"] == 1 and df_o_aligned.loc[eid, "predicted_label"] == 0),
                    "is_new_fp": bool(row_b["canonical_label"] == 0 and df_n_aligned.loc[eid, "predicted_label"] == 0 and df_o_aligned.loc[eid, "predicted_label"] == 1),
                    "text_original": str(row_b["text_original"]),
                    "text_obfuscated": str(row_b["text_obfuscated"])
                })

    df_paired = pd.DataFrame(paired_rows)
    df_paired.to_csv(reports_dir / "paired_robustness_metrics.csv", index=False)
    print(f" Saved: {reports_dir / 'paired_robustness_metrics.csv'}")

    df_flips = pd.DataFrame(flip_rows)
    df_flips.to_csv(reports_dir / "prediction_flip_summary.csv", index=False)
    print(f" Saved: {reports_dir / 'prediction_flip_summary.csv'}")

    df_err = pd.DataFrame(all_paired_errors)
    df_err.to_csv(reports_dir / "paired_error_analysis.csv", index=False)
    print(f" Saved: {reports_dir / 'paired_error_analysis.csv'} ({len(df_err)} error rows)")

    # E. Source Stratified Metrics
    print("\n Computing Source Dataset Stratified Metrics...")
    source_rows = []
    sources = sorted(normal_df["source_dataset"].unique())

    for src in sources:
        src_mask_norm = (normal_df["source_dataset"] == src)
        n_src_norm = int(src_mask_norm.sum())
        n_prom_src = int((normal_df.loc[src_mask_norm, "canonical_label"] == 1).sum())

        for model_name, df_n in all_models_norm.items():
            m_s_norm = calculate_classification_metrics(
                normal_df.loc[src_mask_norm, "canonical_label"],
                df_n.loc[src_mask_norm, "predicted_label"]
            )
            source_rows.append({
                "source_dataset": src,
                "model": model_name,
                "condition": "NORMAL",
                "subset_type": "full",
                "n_records": n_src_norm,
                "n_promotion": n_prom_src,
                "f1_promotion": m_s_norm["f1_promotion"],
                "precision_promotion": m_s_norm["precision_promotion"],
                "recall_promotion": m_s_norm["recall_promotion"],
                "accuracy": m_s_norm["accuracy"],
                "macro_f1": m_s_norm["macro_f1"]
            })

            # For each obfuscation condition on paired subset
            for cond in config["datasets"]["obfuscation_conditions"]:
                cid = cond["condition_id"]
                df_c_b = obf_dfs[cid]
                src_mask_obf = (df_c_b["source_dataset"] == src) & (df_c_b["changed"])
                n_src_paired = int(src_mask_obf.sum())
                if n_src_paired == 0:
                    continue

                y_t = df_c_b.loc[src_mask_obf, "canonical_label"]
                y_n = df_n.loc[src_mask_obf, "predicted_label"]
                y_o = all_models_obf[model_name][cid].loc[src_mask_obf, "predicted_label"]

                m_np = calculate_classification_metrics(y_t, y_n)
                m_op = calculate_classification_metrics(y_t, y_o)
                f1_d = m_np["f1_promotion"] - m_op["f1_promotion"]

                source_rows.append({
                    "source_dataset": src,
                    "model": model_name,
                    "condition": cid,
                    "subset_type": "paired_changed",
                    "n_records": n_src_paired,
                    "n_promotion": int((y_t == 1).sum()),
                    "f1_promotion": m_op["f1_promotion"],
                    "precision_promotion": m_op["precision_promotion"],
                    "recall_promotion": m_op["recall_promotion"],
                    "accuracy": m_op["accuracy"],
                    "macro_f1": m_op["macro_f1"],
                    "f1_drop": f1_d
                })

    df_source = pd.DataFrame(source_rows)
    df_source.to_csv(reports_dir / "source_stratified_metrics.csv", index=False)
    print(f" Saved: {reports_dir / 'source_stratified_metrics.csv'}")

    # F. Robustness Summary JSON
    summary_doc = {
        "summary_version": "1.0.0",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "normal_test_metrics": df_norm_metrics.to_dict(orient="records"),
        "model_rankings": {
            "normal_f1_rank": df_norm_metrics.sort_values(by="f1_promotion", ascending=False)[["model", "f1_promotion"]].to_dict(orient="records"),
            "mean_f1_drop_rank": df_paired.groupby("model")["f1_drop"].mean().sort_values().to_dict(),
            "mean_retention_rank": df_paired.groupby("model")["f1_retention_pct"].mean().sort_values(ascending=False).to_dict()
        },
        "family_average_f1_drop": df_paired.groupby(["model", "family"])["f1_drop"].mean().unstack().to_dict(),
        "severity_average_f1_drop": df_paired.groupby(["model", "severity"])["f1_drop"].mean().unstack().to_dict(),
        "total_evasion_flips_by_model": df_flips.groupby("model")["n_evasion_flips"].sum().to_dict(),
        "mean_evasion_flip_rate_by_model": df_flips.groupby("model")["evasion_flip_rate_pct"].mean().to_dict()
    }

    with open(reports_dir / "robustness_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_doc, f, indent=2)
    print(f" Saved: {reports_dir / 'robustness_summary.json'}")

    end_time = datetime.datetime.now(datetime.timezone.utc)
    duration_sec = (end_time - start_time).total_seconds()

    # G. Manifest v1 JSON
    manifest = {
        "manifest_version": "1.0.0",
        "stage": "stage10",
        "status": "SUCCESS",
        "run_identity": {
            "start_time_utc": start_time.isoformat(),
            "end_time_utc": end_time.isoformat(),
            "elapsed_seconds": round(duration_sec, 2),
            "seed": 42
        },
        "git": {
            "commit_sha": os.popen("git rev-parse HEAD").read().strip(),
            "working_tree_clean": (os.popen("git status --short").read().strip() == "")
        },
        "environment": {
            "python": sys.version.split()[0],
            "device": device
        },
        "model_artifacts": {
            "linear_svm": {
                "path": models_cfg["linear_svm"]["model_path"],
                "sha256": models_cfg["linear_svm"]["sha256"]
            },
            "char_cnn": {
                "path": models_cfg["char_cnn"]["model_weights_path"],
                "sha256": models_cfg["char_cnn"]["model_weights_sha256"],
                "vocab_sha256": models_cfg["char_cnn"]["vocab_sha256"]
            },
            "indobert": {
                "path": models_cfg["indobert"]["model_weights_path"],
                "sha256": models_cfg["indobert"]["model_weights_sha256"]
            }
        },
        "input_datasets": {
            "normal": {
                "path": config["datasets"]["test_normal"]["path"],
                "sha256": config["datasets"]["test_normal"]["sha256"],
                "rows": len(normal_df)
            },
            "obfuscation_conditions": [
                {
                    "condition_id": c["condition_id"],
                    "path": c["path"],
                    "sha256": c["sha256"],
                    "rows": len(obf_dfs[c["condition_id"]]),
                    "changed_pairs": int(obf_dfs[c["condition_id"]]["changed"].sum())
                }
                for c in config["datasets"]["obfuscation_conditions"]
            ]
        },
        "prediction_counts": {
            "total_model_condition_pairs": 27,
            "predictions_per_condition": 4116,
            "total_predictions": 27 * 4116
        },
        "output_reports": [
            "reports/stage10/test_normal_metrics.csv",
            "reports/stage10/obfuscation_metrics_full.csv",
            "reports/stage10/paired_robustness_metrics.csv",
            "reports/stage10/prediction_flip_summary.csv",
            "reports/stage10/paired_error_analysis.csv",
            "reports/stage10/source_stratified_metrics.csv",
            "reports/stage10/robustness_summary.json"
        ]
    }

    with open(reports_dir / "manifest_v1.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f" Saved: {reports_dir / 'manifest_v1.json'}")

    print("\n" + "=" * 76)
    print("STAGE 10 OFFICIAL ROBUSTNESS EVALUATION COMPLETED SUCCESSFULLY!")
    print(f"Elapsed Time: {duration_sec:.2f} seconds")
    print("=" * 76)


# -----------------------------------------------------------------------------
# Main CLI Entrypoint
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Stage 10 Official Robustness Evaluation Runner")
    parser.add_argument("--mode", choices=["preflight", "official", "validate"], default="preflight",
                        help="Execution mode (default: preflight)")
    parser.add_argument("--config", default=CONFIG_PATH, help="Path to Stage 10 configuration JSON")
    parser.add_argument("--device", default=None, help="Inference device (cpu/cuda, default: auto-detect)")
    parser.add_argument("--no-resume", action="store_true", help="Overwrite existing prediction files")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    if args.mode == "preflight":
        success, device = run_preflight(config)
        sys.exit(0 if success else 1)

    elif args.mode == "official":
        # Always run preflight before official execution
        success, auto_device = run_preflight(config)
        if not success:
            print("\nPreflight checks failed! Cannot proceed to official evaluation.")
            sys.exit(1)

        device = args.device or auto_device
        run_official_evaluation(config, device=device, resume=not args.no_resume)

    elif args.mode == "validate":
        print("Running Stage 10 output validation...")
        # Will call validator script
        validator_path = Path(__file__).resolve().with_name("23_validate_stage10_results.py")
        validator_spec = importlib.util.spec_from_file_location("stage10_validator", validator_path)
        if validator_spec is None or validator_spec.loader is None:
            raise RuntimeError(f"Unable to load Stage 10 validator: {validator_path}")
        validator = importlib.util.module_from_spec(validator_spec)
        validator_spec.loader.exec_module(validator)
        res = validator.validate_all_outputs(args.config)
        sys.exit(0 if res else 1)


if __name__ == "__main__":
    main()
