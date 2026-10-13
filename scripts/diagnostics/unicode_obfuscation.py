"""Canonical entrypoint for the Unicode obfuscation diagnostic."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = ROOT / "scripts" / "24_unicode_obfuscation_diagnostic.py"

if __name__ == "__main__":
    runpy.run_path(str(IMPLEMENTATION), run_name="__main__")
