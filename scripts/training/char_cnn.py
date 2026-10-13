"""Canonical Char-CNN training entrypoint."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = ROOT / "models" / "char_cnn" / "project" / "charcnn_train.py"

if __name__ == "__main__":
    runpy.run_path(str(IMPLEMENTATION), run_name="__main__")
