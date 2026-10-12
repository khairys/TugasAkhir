"""
tests/stage10/test_results_integrity.py - Unit tests for result validators and edge cases.
"""

import os
import json
import pytest
import pandas as pd
import numpy as np


def test_validator_script_exists():
    """Verify validator script is present and executable."""
    val_script = "scripts/23_validate_stage10_results.py"
    assert os.path.exists(val_script), f"Validator script missing: {val_script}"


def test_bootstrap_edge_case_zero_drops():
    """Verify bootstrap handles case when f1_drop is zero identically."""
    import importlib.util
    from pathlib import Path

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "22_run_stage10_robustness.py"
    spec = importlib.util.spec_from_file_location("runner_mod", str(script_path))
    runner_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner_mod)

    y_true = np.array([0, 0, 0, 1, 1, 1])
    y_norm = np.array([0, 0, 0, 1, 1, 1])
    y_obf  = np.array([0, 0, 0, 1, 1, 1])

    res = runner_mod.run_stratified_paired_bootstrap(y_true, y_norm, y_obf, n_resamples=100, seed=42)
    assert res["bootstrap_f1_drop_mean"] == 0.0
    assert res["ci_95_lower"] == 0.0
    assert res["ci_95_upper"] == 0.0
