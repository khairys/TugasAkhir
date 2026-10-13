#!/usr/bin/env python3
"""
scripts/25_evaluate_indobert_v2_robustness.py
Official Robustness Evaluation for IndoBERT v2 Model & Comprehensive Multi-Model Comparison.

Evaluates IndoBERT v2 across:
- 1 Normal test condition (data/processed/test_normal_v1.csv, 4,116 rows)
- 8 Obfuscation conditions (O1_MILD, O1_STRONG, O2_MILD, O2_STRONG, O3_MILD, O3_STRONG, O4_MILD, O4_STRONG, 4,116 rows each)

Outputs stored separately in reports/indobert_v2_robustness/ without modifying official Stage 10 files.
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

CONFIG_PATH = REPO_ROOT / "configs" / "stage10" / "robustness_evaluation_v1.json"
MODEL_DIR = REPO_ROOT / "IndoBERT_v2_Local_Model_and_Training_Report" / "model"
REPORTS_DIR = REPO_ROOT / "reports" / "indobert_v2_robustness"
PRED_DIR = REPORTS_DIR / "predictions"
STAGE10_REPORTS_DIR = REPO_ROOT / "reports" / "stage10"


def calculate_metrics(y_true, y_pred):
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
        "total_samples": int(len(y_true)),
    }


def predict_indobert(texts, model, tokenizer, device, batch_size=64):
    """Length-sorted bucketed batch inference on CPU."""
    clean_texts = ["" if pd.isna(t) else str(t) for t in texts]
    total = len(clean_texts)
    if total == 0:
        return np.array([], dtype=int), np.array([], dtype=float)

    lengths = [len(t) for t in clean_texts]
    sort_indices = np.argsort(lengths)
    sorted_texts = [clean_texts[idx] for idx in sort_indices]

    all_preds = []
    all_probs = []

    with torch.inference_mode():
        for i in range(0, total, batch_size):
            batch = sorted_texts[i:i + batch_size]
            inputs = tokenizer(
                batch,
                max_length=128,
                padding=True,
                truncation=True,
                return_tensors="pt"
            ).to(device)

            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=-1)[:, 1]
            preds = torch.argmax(logits, dim=-1)

            all_preds.extend(preds.cpu().numpy().tolist())
            all_probs.extend(probs.cpu().numpy().tolist())

    sorted_preds = np.array(all_preds, dtype=int)
    sorted_probs = np.array(all_probs, dtype=float)

    reverse_indices = np.empty_like(sort_indices)
    reverse_indices[sort_indices] = np.arange(total)

    return sorted_preds[reverse_indices], sorted_probs[reverse_indices]


def main():
    print("=" * 80)
    print("STAGE 10 EVALUATION: INDOBERT V2 ROBUSTNESS & MULTI-MODEL COMPARISON")
    print("=" * 80)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    PRED_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Setup PyTorch & Model
    torch.set_num_threads(os.cpu_count() or 8)
    device = torch.device("cpu")
    print(f"Device: {device} with {torch.get_num_threads()} CPU threads.")

    print(f"Loading IndoBERT v2 from {MODEL_DIR}...")
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR), local_files_only=True).to(device)
    model.eval()
    print("IndoBERT v2 model loaded successfully.")

    # 1. Normal Test Inference
    print("\n--- 1. Evaluating Normal Test Set (test_normal_v1.csv) ---")
    norm_path = REPO_ROOT / config["datasets"]["test_normal"]["path"]
    df_normal = pd.read_csv(norm_path)
    norm_texts = df_normal["text_original"].fillna("").astype(str).tolist()
    y_true_normal = df_normal["canonical_label"].to_numpy(dtype=int)

    norm_preds_file = PRED_DIR / "test_normal_predictions_v2.csv"
    if norm_preds_file.exists():
        print(f"  [CACHE] Loading existing {norm_preds_file.name}")
        df_norm_pred = pd.read_csv(norm_preds_file)
        preds_norm = df_norm_pred["predicted_label"].to_numpy(dtype=int)
        probs_norm = df_norm_pred["probability_promotion"].to_numpy(dtype=float)
    else:
        t0 = time.time()
        preds_norm, probs_norm = predict_indobert(norm_texts, model, tokenizer, device)
        print(f"  Normal inference completed in {time.time() - t0:.2f}s")
        df_norm_pred = pd.DataFrame({
            "source_record_id": df_normal["source_record_id"],
            "canonical_label": y_true_normal,
            "predicted_label": preds_norm,
            "probability_promotion": probs_norm,
            "is_correct": (preds_norm == y_true_normal),
            "model": "indobert_v2",
            "condition": "NORMAL",
        })
        df_norm_pred.to_csv(norm_preds_file, index=False)
        print(f"  Saved: {norm_preds_file.name}")

    norm_metrics = calculate_metrics(y_true_normal, preds_norm)
    norm_metrics["model"] = "indobert_v2"
    norm_metrics["condition"] = "NORMAL"

    df_norm_metrics = pd.DataFrame([norm_metrics])
    df_norm_metrics.to_csv(REPORTS_DIR / "test_normal_metrics_v2.csv", index=False)
    print(f"Normal Test Metrics: F1={norm_metrics['f1_promotion']:.4f}, Prec={norm_metrics['precision_promotion']:.4f}, Rec={norm_metrics['recall_promotion']:.4f}, Acc={norm_metrics['accuracy']:.4f}")

    # 2. Obfuscation Conditions Inference
    print("\n--- 2. Evaluating 8 Obfuscation Conditions ---")
    obf_full_rows = []
    paired_rows = []
    obf_pred_dfs = {}

    for cond in config["datasets"]["obfuscation_conditions"]:
        cid = cond["condition_id"]
        family = cond["family"]
        severity = cond["severity"]
        cond_path = REPO_ROOT / cond["path"]

        df_cond = pd.read_csv(cond_path)
        y_true_cond = df_cond["canonical_label"].to_numpy(dtype=int)
        changed_mask = df_cond["changed"].to_numpy(dtype=bool)

        pred_cond_file = PRED_DIR / f"{cid}_predictions_v2.csv"
        if pred_cond_file.exists():
            print(f"  [CACHE] Loading existing {pred_cond_file.name}")
            df_pred_cond = pd.read_csv(pred_cond_file)
            preds_cond = df_pred_cond["predicted_label"].to_numpy(dtype=int)
            probs_cond = df_pred_cond["probability_promotion"].to_numpy(dtype=float)
        else:
            t0 = time.time()
            texts_cond = df_cond["text_obfuscated"].fillna("").astype(str).tolist()
            preds_cond, probs_cond = predict_indobert(texts_cond, model, tokenizer, device)
            print(f"  [{cid}] Inference completed in {time.time() - t0:.2f}s")

            df_pred_cond = pd.DataFrame({
                "source_record_id": df_cond["source_record_id"],
                "canonical_label": y_true_cond,
                "predicted_label": preds_cond,
                "probability_promotion": probs_cond,
                "is_correct": (preds_cond == y_true_cond),
                "changed": df_cond["changed"],
                "model": "indobert_v2",
                "condition": cid,
            })
            df_pred_cond.to_csv(pred_cond_file, index=False)

        obf_pred_dfs[cid] = df_pred_cond

        # Full-set metrics
        m_full = calculate_metrics(y_true_cond, preds_cond)
        m_full["model"] = "indobert_v2"
        m_full["condition"] = cid
        m_full["family"] = family
        m_full["severity"] = severity
        obf_full_rows.append(m_full)

        # Paired metrics on changed == True
        yt_paired = y_true_cond[changed_mask]
        yn_paired = preds_norm[changed_mask]
        yo_paired = preds_cond[changed_mask]
        n_changed = int(changed_mask.sum())

        m_norm_paired = calculate_metrics(yt_paired, yn_paired)
        m_obf_paired = calculate_metrics(yt_paired, yo_paired)

        f1_norm = m_norm_paired["f1_promotion"]
        f1_obf = m_obf_paired["f1_promotion"]
        f1_drop = f1_norm - f1_obf
        rel_drop = (f1_drop / max(1e-6, f1_norm)) * 100.0
        retention = 100.0 - rel_drop

        # Flips
        evasion_flips = int(np.sum((yt_paired == 1) & (yn_paired == 1) & (yo_paired == 0)))
        fp_flips = int(np.sum((yt_paired == 0) & (yn_paired == 0) & (yo_paired == 1)))

        paired_rows.append({
            "model": "indobert_v2",
            "condition": cid,
            "family": family,
            "severity": severity,
            "n_test_records": len(y_true_cond),
            "n_changed_pairs": n_changed,
            "transformation_rate_pct": round((n_changed / len(y_true_cond)) * 100, 2),
            "f1_normal_paired": f1_norm,
            "f1_obfuscated_paired": f1_obf,
            "f1_drop": round(f1_drop, 4),
            "relative_drop_pct": round(rel_drop, 2),
            "f1_retention_pct": round(retention, 2),
            "precision_normal_paired": m_norm_paired["precision_promotion"],
            "precision_obfuscated_paired": m_obf_paired["precision_promotion"],
            "recall_normal_paired": m_norm_paired["recall_promotion"],
            "recall_obfuscated_paired": m_obf_paired["recall_promotion"],
            "accuracy_normal_paired": m_norm_paired["accuracy"],
            "accuracy_obfuscated_paired": m_obf_paired["accuracy"],
            "TN_normal": m_norm_paired["TN"],
            "FP_normal": m_norm_paired["FP"],
            "FN_normal": m_norm_paired["FN"],
            "TP_normal": m_norm_paired["TP"],
            "TN_obfuscated": m_obf_paired["TN"],
            "FP_obfuscated": m_obf_paired["FP"],
            "FN_obfuscated": m_obf_paired["FN"],
            "TP_obfuscated": m_obf_paired["TP"],
            "evasion_flips": evasion_flips,
            "false_positive_flips": fp_flips,
        })
        print(f"  [{cid:<10}] Paired F1: {f1_norm:.4f} -> {f1_obf:.4f} (Drop: {f1_drop:+.4f}, Ret: {retention:.1f}%) | FP Flips: {fp_flips}, Eva Flips: {evasion_flips}")

    df_obf_full_v2 = pd.DataFrame(obf_full_rows)
    df_paired_v2 = pd.DataFrame(paired_rows)

    df_obf_full_v2.to_csv(REPORTS_DIR / "obfuscation_metrics_full_v2.csv", index=False)
    df_paired_v2.to_csv(REPORTS_DIR / "paired_robustness_metrics_v2.csv", index=False)

    # 3. Comprehensive Comparison Across All 4 Models
    print("\n--- 3. Building Comprehensive 4-Model Comparison Table ---")
    build_and_save_comparison(norm_metrics, df_paired_v2)


def build_and_save_comparison(norm_metrics_v2, df_paired_v2):
    """Build multi-model side-by-side comparison with Linear SVM, Char-CNN, IndoBERT v1, IndoBERT v2."""
    official_norm = pd.read_csv(STAGE10_REPORTS_DIR / "test_normal_metrics.csv")
    official_paired = pd.read_csv(STAGE10_REPORTS_DIR / "paired_robustness_metrics.csv")

    comparison_records = []

    # A. Normal baseline comparison
    for _, r in official_norm.iterrows():
        comparison_records.append({
            "model": r["model"],
            "condition": "NORMAL",
            "family": "NORMAL",
            "severity": "NORMAL",
            "f1_score": r["f1_promotion"],
            "f1_drop": 0.0,
            "relative_drop_pct": 0.0,
            "f1_retention_pct": 100.0,
            "precision": r["precision_promotion"],
            "recall": r["recall_promotion"],
            "accuracy": r["accuracy"],
            "fp": r["FP"],
            "fn": r["FN"],
            "fp_flips": 0,
            "evasion_flips": 0,
        })

    comparison_records.append({
        "model": "indobert_v2",
        "condition": "NORMAL",
        "family": "NORMAL",
        "severity": "NORMAL",
        "f1_score": norm_metrics_v2["f1_promotion"],
        "f1_drop": 0.0,
        "relative_drop_pct": 0.0,
        "f1_retention_pct": 100.0,
        "precision": norm_metrics_v2["precision_promotion"],
        "recall": norm_metrics_v2["recall_promotion"],
        "accuracy": norm_metrics_v2["accuracy"],
        "fp": norm_metrics_v2["FP"],
        "fn": norm_metrics_v2["FN"],
        "fp_flips": 0,
        "evasion_flips": 0,
    })

    # B. Paired Obfuscation comparison across all 8 conditions
    conditions = ["O1_MILD", "O1_STRONG", "O2_MILD", "O2_STRONG", "O3_MILD", "O3_STRONG", "O4_MILD", "O4_STRONG"]
    for cid in conditions:
        # 1. Existing models
        sub_off = official_paired[official_paired["condition"] == cid]
        for _, r in sub_off.iterrows():
            # Check for evasion_flips column in official paired if present, otherwise compute
            eva = r.get("evasion_flips", int((r["TP_normal"] - r["TP_obfuscated"])))
            comparison_records.append({
                "model": r["model"],
                "condition": cid,
                "family": r["family"],
                "severity": r["severity"],
                "f1_score": r["f1_obfuscated_paired"],
                "f1_drop": r["f1_drop"],
                "relative_drop_pct": r["relative_drop_pct"],
                "f1_retention_pct": r["f1_retention_pct"],
                "precision": r["precision_obfuscated_paired"],
                "recall": r["recall_obfuscated_paired"],
                "accuracy": r["accuracy_obfuscated_paired"],
                "fp": r["FP_obfuscated"],
                "fn": r["FN_obfuscated"],
                "fp_flips": int(r["FP_obfuscated"] - r["FP_normal"]),
                "evasion_flips": int(max(0, r["TP_normal"] - r["TP_obfuscated"])),
            })

        # 2. IndoBERT v2
        sub_v2 = df_paired_v2[df_paired_v2["condition"] == cid].iloc[0]
        comparison_records.append({
            "model": "indobert_v2",
            "condition": cid,
            "family": sub_v2["family"],
            "severity": sub_v2["severity"],
            "f1_score": sub_v2["f1_obfuscated_paired"],
            "f1_drop": sub_v2["f1_drop"],
            "relative_drop_pct": sub_v2["relative_drop_pct"],
            "f1_retention_pct": sub_v2["f1_retention_pct"],
            "precision": sub_v2["precision_obfuscated_paired"],
            "recall": sub_v2["recall_obfuscated_paired"],
            "accuracy": sub_v2["accuracy_obfuscated_paired"],
            "fp": sub_v2["FP_obfuscated"],
            "fn": sub_v2["FN_obfuscated"],
            "fp_flips": int(sub_v2["false_positive_flips"]),
            "evasion_flips": int(sub_v2["evasion_flips"]),
        })

    df_comp = pd.DataFrame(comparison_records)
    df_comp.to_csv(REPORTS_DIR / "comprehensive_model_comparison.csv", index=False)
    print(f"Saved: {REPORTS_DIR / 'comprehensive_model_comparison.csv'}")

    # Generate Markdown Report
    report_md = REPORTS_DIR / "indobert_v2_robustness_report.md"
    generate_markdown_report(report_md, df_comp)
    print(f"Saved: {report_md}")


def generate_markdown_report(report_path, df_comp):
    """Write rich academic comparison report."""
    md = []
    md.append("# LAPORAN EVALUASI KETAHANAN INDOBERT V2 & KOMPARASI MULTI-MODEL")
    md.append("## Linear SVM vs Character-level CNN vs IndoBERT v1 vs IndoBERT v2")
    md.append("")
    md.append(f"**Tanggal Pengujian**: {time.strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append("**Metodologi**: Protokol Resmi Stage 10 (Paired Robustness pada `changed == True`, 4.116 baris per kondisi)  ")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Perbandingan Performa Baseline (Normal Test Set Tanpa Penyamaran)")
    md.append("")
    md.append("| Model | F1 Promosi | Precision | Recall | Accuracy | False Positives (FP) | False Negatives (FN) |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

    df_norm = df_comp[df_comp["condition"] == "NORMAL"]
    for _, r in df_norm.iterrows():
        md.append(f"| **{r['model']}** | **{r['f1_score']:.4f}** | {r['precision']:.4f} | {r['recall']:.4f} | {r['accuracy']:.4f} | {r['fp']} | {r['fn']} |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. Perbandingan Ketahanan Berpasangan Lintas 8 Kondisi Penyamaran (Paired F1 & Retensi)")
    md.append("")
    md.append("| Kondisi | Linear SVM (F1 / Retensi) | Char-CNN (F1 / Retensi) | IndoBERT v1 (F1 / Retensi) | IndoBERT v2 (F1 / Retensi) | Pemenang Kondisi |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: |")

    conditions = ["O1_MILD", "O1_STRONG", "O2_MILD", "O2_STRONG", "O3_MILD", "O3_STRONG", "O4_MILD", "O4_STRONG"]
    for cid in conditions:
        sub = df_comp[df_comp["condition"] == cid].set_index("model")
        svm_f1 = sub.loc["linear_svm", "f1_score"]
        svm_ret = sub.loc["linear_svm", "f1_retention_pct"]
        cnn_f1 = sub.loc["char_cnn", "f1_score"]
        cnn_ret = sub.loc["char_cnn", "f1_retention_pct"]
        ib1_f1 = sub.loc["indobert", "f1_score"]
        ib1_ret = sub.loc["indobert", "f1_retention_pct"]
        ib2_f1 = sub.loc["indobert_v2", "f1_score"]
        ib2_ret = sub.loc["indobert_v2", "f1_retention_pct"]

        scores = {"Char-CNN": cnn_f1, "IndoBERT v2": ib2_f1, "IndoBERT v1": ib1_f1, "Linear SVM": svm_f1}
        winner = max(scores, key=scores.get)

        md.append(
            f"| **{cid}** | {svm_f1:.4f} ({svm_ret:.1f}%) | **{cnn_f1:.4f} ({cnn_ret:.1f}%)** | "
            f"{ib1_f1:.4f} ({ib1_ret:.1f}%) | {ib2_f1:.4f} ({ib2_ret:.1f}%) | **{winner}** |"
        )

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 3. Analisis Mendalam: IndoBERT v2 vs IndoBERT v1")
    md.append("")
    md.append("| Kondisi | F1 IndoBERT v1 | F1 IndoBERT v2 | Perubahan F1 (ΔF1 v2 vs v1) | FP Flips v1 | FP Flips v2 | Evasion Flips v1 | Evasion Flips v2 |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

    for cid in conditions:
        sub = df_comp[df_comp["condition"] == cid].set_index("model")
        ib1 = sub.loc["indobert"]
        ib2 = sub.loc["indobert_v2"]
        diff = ib2["f1_score"] - ib1["f1_score"]

        md.append(
            f"| **{cid}** | {ib1['f1_score']:.4f} | {ib2['f1_score']:.4f} | "
            f"**{diff:+.4f}** | {ib1['fp_flips']} | {ib2['fp_flips']} | "
            f"{ib1['evasion_flips']} | {ib2['evasion_flips']} |"
        )

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))


if __name__ == "__main__":
    main()
