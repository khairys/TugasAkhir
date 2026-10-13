"""Verify label mapping for the three canonical models."""

import os
import json
import joblib


def test_svm_label_mapping():
    """Verify Linear SVM pipeline classes are binary [0, 1]."""
    svm_path = "models/linear_svm/model/model.joblib"
    assert os.path.exists(svm_path), f"SVM model not found: {svm_path}"
    pipe = joblib.load(svm_path)
    clf = pipe.named_steps.get("classifier", pipe.named_steps.get("svm", pipe.steps[-1][1]))
    assert hasattr(clf, "classes_")
    assert list(clf.classes_) == [0, 1]


def test_char_cnn_label_mapping():
    """Verify Char-CNN config maps 0 to Non-Promotion and 1 to Promotion."""
    config_path = "models/char_cnn/project/config.json"
    assert os.path.exists(config_path), f"Char-CNN config not found: {config_path}"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    assert cfg["selection"]["primary_metric"] == "f1_promotion"

    contract_path = "models/char_cnn/artifacts/final_model/data_contract.json"
    if os.path.exists(contract_path):
        with open(contract_path, "r", encoding="utf-8") as f:
            contract = json.load(f)
        assert contract["label_mapping"]["0"] == "Non-Promotion"
        assert contract["label_mapping"]["1"] == "Promotion"


def test_indobert_label_mapping():
    """Verify IndoBERT Hugging Face config id2label and label2id."""
    config_path = "models/indobert/artifacts/final_model/config.json"
    assert os.path.exists(config_path), f"IndoBERT config not found: {config_path}"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    id2label = cfg.get("id2label", {})
    label2id = cfg.get("label2id", {})
    assert str(id2label.get("0", id2label.get(0, ""))).lower().startswith("non")
    assert str(id2label.get("1", id2label.get(1, ""))).lower().startswith("prom")
    assert label2id.get("Non-Promotion") == 0
    assert label2id.get("Promotion") == 1
