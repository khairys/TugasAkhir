"""Canonical Linear SVM training entrypoint."""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = ROOT / "scripts" / "19_train_linear_svm.py"
CONFIG = ROOT / "models" / "linear_svm" / "config.json"

if __name__ == "__main__":
    argv = list(sys.argv)
    if "--config" not in argv:
        argv.extend(["--config", str(CONFIG)])
    sys.argv = argv
    runpy.run_path(str(IMPLEMENTATION), run_name="__main__")
