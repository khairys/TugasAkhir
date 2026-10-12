"""
tests/stage10/test_metrics.py - Unit tests for metric calculations, paired drops,
evasion flips, and bootstrap confidence intervals using small synthetic fixtures.
"""

import pytest
import numpy as np
import pandas as pd
import importlib.util
from pathlib import Path

script_path = Path(__file__).resolve().parents[2] / "scripts" / "22_run_stage10_robustness.py"
spec = importlib.util.spec_from_file_location("runner_mod", str(script_path))
runner_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner_mod)

calculate_classification_metrics = runner_mod.calculate_classification_metrics
run_stratified_paired_bootstrap = runner_mod.run_stratified_paired_bootstrap


def test_calculate_classification_metrics_perfect():
    """Test metrics with 100% correct predictions."""
    y_true = [0, 0, 0, 1, 1]
    y_pred = [0, 0, 0, 1, 1]
    m = calculate_classification_metrics(y_true, y_pred)
    assert m["accuracy"] == 1.0
    assert m["f1_promotion"] == 1.0
    assert m["precision_promotion"] == 1.0
    assert m["recall_promotion"] == 1.0
    assert m["macro_f1"] == 1.0
    assert m["TP"] == 2
    assert m["TN"] == 3
    assert m["FP"] == 0
    assert m["FN"] == 0


def test_calculate_classification_metrics_known_case():
    """Test metrics with a known synthetic confusion matrix."""
    # TN=3, FP=1, FN=1, TP=3 -> total=8
    y_true = [0, 0, 0, 0, 1, 1, 1, 1]
    y_pred = [0, 0, 0, 1, 0, 1, 1, 1]
    m = calculate_classification_metrics(y_true, y_pred)
    assert m["TN"] == 3
    assert m["FP"] == 1
    assert m["FN"] == 1
    assert m["TP"] == 3
    assert m["accuracy"] == 6 / 8
    # Precision = 3 / (3 + 1) = 0.75
    assert m["precision_promotion"] == 0.75
    # Recall = 3 / (3 + 1) = 0.75
    assert m["recall_promotion"] == 0.75
    # F1 = 0.75
    assert m["f1_promotion"] == 0.75


def test_paired_f1_drop_and_retention():
    """Test paired F1 Drop and Retention formula."""
    f1_normal = 0.90
    f1_obfuscated = 0.72
    f1_drop = f1_normal - f1_obfuscated
    rel_drop_pct = (f1_drop / f1_normal) * 100
    retention_pct = (f1_obfuscated / f1_normal) * 100

    assert pytest.approx(f1_drop, 1e-6) == 0.18
    assert pytest.approx(rel_drop_pct, 1e-4) == 20.0
    assert pytest.approx(retention_pct, 1e-4) == 80.0


def test_evasion_flip_definition():
    """Test evasion flip rate logic."""
    # Record 1: actual=1, norm=1, obf=0 -> EVASION FLIP
    # Record 2: actual=1, norm=1, obf=1 -> Stable TP
    # Record 3: actual=1, norm=0, obf=0 -> Stable FN
    # Record 4: actual=0, norm=0, obf=0 -> Stable TN
    y_true = np.array([1, 1, 1, 0])
    y_norm = np.array([1, 1, 0, 0])
    y_obf  = np.array([0, 1, 0, 0])

    is_prom = (y_true == 1)
    norm_tp = (is_prom & (y_norm == 1))
    evasions = (norm_tp & (y_obf == 0))

    n_norm_tp = int(norm_tp.sum())  # 2
    n_evasion = int(evasions.sum()) # 1

    evasion_rate = (n_evasion / n_norm_tp) * 100
    assert n_norm_tp == 2
    assert n_evasion == 1
    assert pytest.approx(evasion_rate, 1e-4) == 50.0


def test_stratified_paired_bootstrap():
    """Test stratified paired bootstrap runs and produces valid interval."""
    # Synthetic dataset with 20 non-prom, 10 prom
    rng = np.random.default_rng(42)
    y_true = np.array([0] * 20 + [1] * 10)
    y_norm = y_true.copy()
    # Introduce some drops in obfuscated
    y_obf = y_norm.copy()
    y_obf[20:23] = 0  # 3 promotions flipped to 0

    res = run_stratified_paired_bootstrap(y_true, y_norm, y_obf, n_resamples=500, seed=42)
    assert "ci_95_lower" in res
    assert "ci_95_upper" in res
    assert res["ci_95_lower"] <= res["ci_95_upper"]
    assert res["bootstrap_f1_drop_mean"] >= 0.0
