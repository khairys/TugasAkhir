"""Tests for Stage 8: Manifest and Hash Integrity.

Validates that:
- data/splits/v1/split_manifest_v1.json exists and all recorded SHA-256 hashes match files.
- data/experiments/frozen_experiment_manifest_v1.json exists and all hashes match.
"""

import hashlib
import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def test_split_manifest_hashes():
    manifest_path = REPO_ROOT / "data" / "splits" / "v1" / "split_manifest_v1.json"
    assert manifest_path.exists(), f"Split manifest missing: {manifest_path}"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    hashes = manifest["hashes_sha256"]
    
    main_pool_path = REPO_ROOT / "data" / "processed" / "main_pool_candidate_v2.csv"
    train_path = REPO_ROOT / "data" / "splits" / "v1" / "train_v1.csv"
    val_path = REPO_ROOT / "data" / "splits" / "v1" / "validation_v1.csv"
    test_path = REPO_ROOT / "data" / "splits" / "v1" / "test_v1.csv"
    
    assert compute_sha256(main_pool_path) == hashes["source_main_pool"]
    assert compute_sha256(train_path) == hashes["train_v1"]
    assert compute_sha256(val_path) == hashes["validation_v1"]
    assert compute_sha256(test_path) == hashes["test_v1"]


def test_experiment_manifest_hashes():
    manifest_path = REPO_ROOT / "data" / "experiments" / "frozen_experiment_manifest_v1.json"
    assert manifest_path.exists(), f"Experiment manifest missing: {manifest_path}"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    hashes = manifest["hashes_sha256"]
    
    main_pool_path = REPO_ROOT / "data" / "processed" / "main_pool_candidate_v2.csv"
    test_normal_path = REPO_ROOT / "data" / "processed" / "test_normal_v1.csv"
    
    assert compute_sha256(main_pool_path) == hashes["main_pool"]
    assert compute_sha256(test_normal_path) == hashes["test_normal"]
    
    for cond_name, recorded_hash in hashes["obfuscated_conditions"].items():
        cond_path = REPO_ROOT / "data" / "processed" / "obfuscated_test_v1" / f"{cond_name}.csv"
        assert cond_path.exists()
        assert compute_sha256(cond_path) == recorded_hash
