"""Unit tests for Stage 9: Evaluation metrics and candidate selection tie-breaking."""

import sys
from pathlib import Path
import numpy as np
import pytest

import importlib
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

train_svm_mod = importlib.import_module("scripts.19_train_svm")
evaluate_pipeline = train_svm_mod.evaluate_pipeline
build_pipeline = train_svm_mod.build_pipeline
is_candidate_better = train_svm_mod.is_candidate_better


def test_evaluate_pipeline_metrics():
    train_texts = [
        "daftar judi online slot gacor",
        "video ini menghibur sekali bang",
        "promo bonus deposit agen terpercaya",
        "gameplay miya mobile legends",
    ]
    train_labels = [1, 0, 1, 0]

    val_texts = [
        "daftar situs judi gacor",
        "video sangat bagus dan mendidik"
    ]
    val_labels = [1, 0]

    pipe = build_pipeline(ngram_range=(1, 1), C=1.0, seed=42)
    pipe.fit(train_texts, train_labels)

    metrics = evaluate_pipeline(pipe, val_texts, val_labels)

    required_keys = [
        "f1_promotion", "precision_promotion", "recall_promotion",
        "accuracy", "macro_f1", "confusion_matrix", "eval_duration_sec"
    ]
    for k in required_keys:
        assert k in metrics, f"Missing metric key: {k}"

    cm = metrics["confusion_matrix"]
    assert set(cm.keys()) == {"TN", "FP", "FN", "TP"}
    assert cm["TN"] + cm["FP"] + cm["FN"] + cm["TP"] == len(val_labels)


def test_tie_breaking_logic():
    # 1. Higher F1 is better
    c1 = {"f1_promotion": 0.85, "precision_promotion": 0.80, "recall_promotion": 0.90, "macro_f1": 0.88, "ngram_range": [1, 1], "C": 1.0}
    c2 = {"f1_promotion": 0.82, "precision_promotion": 0.85, "recall_promotion": 0.80, "macro_f1": 0.85, "ngram_range": [1, 1], "C": 1.0}
    assert is_candidate_better(c1, c2) is True
    assert is_candidate_better(c2, c1) is False

    # 2. Equal F1, higher Precision wins
    c3 = {"f1_promotion": 0.85, "precision_promotion": 0.88, "recall_promotion": 0.82, "macro_f1": 0.88, "ngram_range": [1, 1], "C": 1.0}
    assert is_candidate_better(c3, c1) is True

    # 3. Equal F1 and Precision, higher Recall wins
    c4 = {"f1_promotion": 0.85, "precision_promotion": 0.88, "recall_promotion": 0.85, "macro_f1": 0.88, "ngram_range": [1, 1], "C": 1.0}
    assert is_candidate_better(c4, c3) is True

    # 4. Equal metrics, unigram preferred over bigram
    c5_uni = {"f1_promotion": 0.85, "precision_promotion": 0.85, "recall_promotion": 0.85, "macro_f1": 0.85, "ngram_range": [1, 1], "C": 1.0}
    c5_bi = {"f1_promotion": 0.85, "precision_promotion": 0.85, "recall_promotion": 0.85, "macro_f1": 0.85, "ngram_range": [1, 2], "C": 1.0}
    assert is_candidate_better(c5_uni, c5_bi) is True

    # 5. Equal metrics and ngrams, lower C preferred
    c6_c01 = {"f1_promotion": 0.85, "precision_promotion": 0.85, "recall_promotion": 0.85, "macro_f1": 0.85, "ngram_range": [1, 1], "C": 0.1}
    assert is_candidate_better(c6_c01, c5_uni) is True
