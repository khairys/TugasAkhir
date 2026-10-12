"""
tests/stage10/test_label_mapping.py - Verify label mapping across all three models:
Linear SVM, Character-level CNN, and IndoBERT.
"""

import os
import json
import pytest
import joblib


def test_svm_label_mapping():
    """Verify Linear SVM pipeline classes are binary [0, 1]."""
    svm_path = "artifacts/stage9/svm_v1/linear_svm_pipeline.joblib"
    assert os.path.exists(svm_path), f"SVM model not found: {svm_path}"
    pipe = joblib.load(svm_path)
    # The classifier step should have classes_ == [0, 1]
    clf = pipe.named_steps.get("classifier", pipe.steps[-1][1])
    assert hasattr(clf, "classes_")
    classes = list(clf.classes_)
    assert classes == [0, 1], f"Expected classes [0, 1], got {classes}"


def test_char_cnn_label_mapping():
    """Verify Char-CNN config maps 0 to Non-Promotion and 1 to Promotion."""
    config_path = "charcnn_v1_results/artifacts/final_model/charcnn_v1.json"
    assert os.path.exists(config_path), f"Char-CNN config not found: {config_path}"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    assert cfg["selection"]["primary_metric"] == "f1_promotion"

    contract_path = "charcnn_v1_results/artifacts/final_model/data_contract.json"
    if os.path.exists(contract_path):
        with open(contract_path, "r", encoding="utf-8") as f:
            contract = json.load(f)
        assert contract["label_mapping"]["0"] == "Non-Promotion"
        assert contract["label_mapping"]["1"] == "Promotion"


def test_indobert_label_mapping():
    """Verify IndoBERT Hugging Face config id2label and label2id."""
    config_path = "indobert_v1_results/artifacts/final_model/config.json"
    assert os.path.exists(config_path), f"IndoBERT config not found: {config_path}"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    id2label = cfg.get("id2label", {})
    label2id = cfg.get("label2id", {})

    # Check id2label: "0": "Non-Promotion", "1": "Promotion"
    assert str(id2label.get("0", id2label.get(0, ""))).lower().startswith("non")
    assert str(id2label.get("1", id2label.get(1, ""))).lower().startswith("prom")

    # Check label2id
    assert label2id.get("Non-Promotion") == 0
    assert label2id.get("Promotion") == 1
