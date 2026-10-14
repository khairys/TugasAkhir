import numpy as np

from scripts.analysis.stage11_robustness_analysis import as_bool, paired_bootstrap_f1_drop


def test_as_bool_handles_csv_boolean_values():
    assert as_bool(True)
    assert as_bool("True")
    assert as_bool("1")
    assert not as_bool(False)
    assert not as_bool("False")


def test_paired_bootstrap_has_ordered_interval_and_zero_for_identical_predictions():
    y_true = np.array([0, 0, 1, 1, 1, 0])
    pred = np.array([0, 1, 1, 1, 0, 0])
    result = paired_bootstrap_f1_drop(y_true, pred, pred, n_resamples=200, seed=42)
    assert result["bootstrap_f1_drop_mean"] == 0.0
    assert result["ci_95_lower"] == 0.0
    assert result["ci_95_upper"] == 0.0


def test_paired_bootstrap_reports_nonzero_drop_when_obfuscated_predictions_change():
    y_true = np.array([0, 0, 1, 1, 1, 0, 1, 0])
    pred_normal = np.array([0, 0, 1, 1, 1, 0, 1, 0])
    pred_obfuscated = np.array([0, 1, 1, 0, 1, 0, 1, 0])
    result = paired_bootstrap_f1_drop(
        y_true, pred_normal, pred_obfuscated, n_resamples=500, seed=42
    )
    assert result["bootstrap_f1_drop_mean"] > 0
    assert result["ci_95_lower"] <= result["ci_95_upper"]
