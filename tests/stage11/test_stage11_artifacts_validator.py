from pathlib import Path

from scripts.validation.validate_stage11_artifacts import validate_stage11_artifacts


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_saved_stage11_artifact_package_is_consistent():
    result = validate_stage11_artifacts(REPO_ROOT)
    assert result["status"] == "PASSED", "\n".join(result["errors"])
    assert result["domain_shift_metric_rows"] == 6
    assert result["review_candidates"] == 113
    assert result["fresh_inference_executed"] is False
    # Known provenance/training caveats remain warnings, not silent green claims.
    assert any("DS5 raw-source" in warning for warning in result["warnings"])
