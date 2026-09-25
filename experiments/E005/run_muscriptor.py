from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYTHON = Path(r"C:/IR research/.venv-muscriptor/Scripts/python.exe")
INPUTS = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav", "low_01_low.wav")


def main() -> None:
    output_dir = Path(__file__).with_name("muscriptor_outputs")
    output_dir.mkdir(exist_ok=True)
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    summary: list[dict[str, object]] = []
    for excerpt in INPUTS:
        source = ROOT / "experiments" / "E002" / "listener_slices" / excerpt
        output = output_dir / f"{Path(excerpt).stem}.json"
        result = subprocess.run(
            [str(PYTHON), "-m", "muscriptor", "transcribe", str(source), "--format", "json", "--output", str(output), "--model", "small", "--device", "cpu", "--dtype", "float32", "--batch-size", "1"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(f"MuScriptor failed for {excerpt}: {result.stderr[-2000:]}")
        events = json.loads(output.read_text(encoding="utf-8"))
        starts = sum(event.get("type") == "start" for event in events) if isinstance(events, list) else None
        summary.append({"excerpt": excerpt, "output": str(output), "event_count": starts, "raw_record_count": len(events) if isinstance(events, list) else None})
    path = Path(__file__).with_name("muscriptor_results.json")
    path.write_text(json.dumps({"candidate": "muscriptor", "model": "small", "results": summary}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
