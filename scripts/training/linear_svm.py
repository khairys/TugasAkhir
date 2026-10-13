"""Canonical Linear SVM training entrypoint.

The verified baseline implementation remains in the numbered historical
script. This stable interface is the path to use for any future retraining.
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = ROOT / "scripts" / "19_train_linear_svm.py"

if __name__ == "__main__":
    runpy.run_path(str(IMPLEMENTATION), run_name="__main__")
