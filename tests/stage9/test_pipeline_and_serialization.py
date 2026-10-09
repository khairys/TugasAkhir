"""Unit tests for Stage 9: Pipeline construction, fitting, serialization, and reloading."""

import sys
from pathlib import Path
import joblib
import numpy as np
import pytest

import importlib
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

train_svm_mod = importlib.import_module("scripts.19_train_svm")
build_pipeline = train_svm_mod.build_pipeline


def test_build_pipeline_structure():
    pipe = build_pipeline(ngram_range=(1, 1), C=1.0, seed=42)
    assert "tfidf" in pipe.named_steps
    assert "svm" in pipe.named_steps
    assert pipe.named_steps["tfidf"].ngram_range == (1, 1)
    assert pipe.named_steps["svm"].C == 1.0
    assert pipe.named_steps["svm"].class_weight == "balanced"
    assert pipe.named_steps["svm"].random_state == 42


def test_pipeline_fit_predict_and_reload(tmp_path):
    train_texts = [
        "gabung sekarang di situs slot gacor dapat bonus",
        "video ini sangat bagus sekali bang",
        "daftar agen judi online terpercaya jp maxwin",
        "tutorial bermain hero miya di mobile legends",
        "promo member baru deposit tanpa potongan",
        "resep masakan rendang khas padang enak"
    ]
    train_labels = [1, 0, 1, 0, 1, 0]

    test_texts = [
        "situs slot online deposit gacor",
        "video resep masakan yang sangat bermanfaat"
    ]

    pipe = build_pipeline(ngram_range=(1, 2), C=1.0, seed=42)
    pipe.fit(train_texts, train_labels)

    preds_original = pipe.predict(test_texts)
    scores_original = pipe.decision_function(test_texts)

    assert len(preds_original) == len(test_texts)
    assert set(preds_original).issubset({0, 1})
    assert len(scores_original) == len(test_texts)

    # Test serialization and reloading
    model_file = tmp_path / "test_pipeline.joblib"
    joblib.dump(pipe, model_file)

    reloaded_pipe = joblib.load(model_file)
    preds_reloaded = reloaded_pipe.predict(test_texts)
    scores_reloaded = reloaded_pipe.decision_function(test_texts)

    assert np.array_equal(preds_original, preds_reloaded), "Predictions from reloaded model mismatch"
    assert np.allclose(scores_original, scores_reloaded), "Decision scores from reloaded model mismatch"
