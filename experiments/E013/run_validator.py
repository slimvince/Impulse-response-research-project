from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "experiments" / "E012" / "validate_cubase_candidates.py"
OUTPUT = Path(__file__).resolve().parent / "results"


def main() -> None:
    subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--include-additional-sets",
            "--output-dir",
            str(OUTPUT),
        ],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
