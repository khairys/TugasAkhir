"""Canonical IndoBERT baseline training entrypoint."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = ROOT / "models" / "indobert" / "project" / "indobert_train.py"

if __name__ == "__main__":
    runpy.run_path(str(IMPLEMENTATION), run_name="__main__")
