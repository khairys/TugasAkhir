"""Canonical entrypoint for the three-model robustness evaluation.

The implementation remains in the verified Stage 10 script for now; this
stable path is the interface future analysis should call.
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = ROOT / "scripts" / "22_run_stage10_robustness.py"

if __name__ == "__main__":
    runpy.run_path(str(IMPLEMENTATION), run_name="__main__")
