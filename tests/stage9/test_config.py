"""Unit tests for Stage 9: Configuration and Candidate Grid."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def config():
    cfg_path = REPO_ROOT / "configs" / "stage9" / "svm_v1.json"
    assert cfg_path.exists(), f"Configuration file missing: {cfg_path}"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_config_required_keys(config):
    required = ["experiment_name", "stage", "seed", "data", "base_model", "candidate_grid", "selection_criteria"]
    for k in required:
        assert k in config, f"Missing key in config: {k}"


def test_config_data_paths(config):
    data_cfg = config["data"]
    assert data_cfg["text_column"] == "text_raw"
    assert data_cfg["label_column"] == "canonical_label"
    assert data_cfg["id_column"] == "record_id"
    assert (REPO_ROOT / data_cfg["train_path"]).exists()
    assert (REPO_ROOT / data_cfg["validation_path"]).exists()


def test_candidate_grid_specifications(config):
    grid = config["candidate_grid"]
    assert len(grid) == 6, f"Expected 6 candidate configurations, got {len(grid)}"

    expected_combinations = [
        ([1, 1], 0.1),
        ([1, 1], 1.0),
        ([1, 1], 10.0),
        ([1, 2], 0.1),
        ([1, 2], 1.0),
        ([1, 2], 10.0),
    ]

    actual_combinations = [(c["ngram_range"], c["C"]) for c in grid]
    assert actual_combinations == expected_combinations, "Candidate grid parameters mismatch"


def test_base_model_specifications(config):
    base = config["base_model"]
    assert base["vectorizer"]["analyzer"] == "word"
    assert base["vectorizer"]["lowercase"] is True
    assert base["vectorizer"]["min_df"] == 1
    assert base["classifier"]["class_weight"] == "balanced"
    assert base["classifier"]["random_state"] == 42
    assert base["classifier"]["max_iter"] == 5000
