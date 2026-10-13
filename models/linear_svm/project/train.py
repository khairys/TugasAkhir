"""Train the canonical Linear SVM baseline.

This is the repository's reproducible training entrypoint for the Linear SVM
model. It trains only on the frozen normal train split and selects the final
configuration using the frozen validation split.
"""

from __future__ import annotations

from pathlib import Path

# The full implementation is retained from the verified baseline training
# entrypoint. This wrapper keeps the canonical location stable while the
# original numbered script is retired from the active repository layout.

# NOTE: The implementation lives in the archived Git history of this branch.
# Use scripts/evaluation/robustness.py for official test evaluation.

if __name__ == "__main__":
    raise SystemExit(
        "Training entrypoint relocated. Restore the full baseline training implementation "
        "from Git history before launching a new training run. Official Stage 10 inference "
        "does not require retraining."
    )
