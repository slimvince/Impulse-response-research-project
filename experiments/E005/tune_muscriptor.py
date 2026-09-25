from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYTHON = Path(r"C:/IR research/.venv-muscriptor/Scripts/python.exe")
INPUTS = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav", "low_01_low.wav")
REFERENCE = {"low_02_low.wav": 3, "bass_friendly_01_bass_friendly.wav": 3, "broad_03_broad.wav": 3, "low_01_low.wav": 5}
PARAMETERS = (
    {"id": "greedy_cfg1", "beam_size": 1, "cfg_coef": 1.0},
    {"id": "beam2_cfg1", "beam_size": 2, "cfg_coef": 1.0},
    {"id": "greedy_cfg1_5", "beam_size": 1, "cfg_coef": 1.5},
    {"id": "beam2_cfg1_5", "beam_size": 2, "cfg_coef": 1.5},
)


def run_variant(excerpt: str, params: dict[str, object], output: Path) -> int:
    source = ROOT / "experiments" / "E002" / "listener_slices" / excerpt
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    command = [str(PYTHON), "-m", "muscriptor", "transcribe", str(source), "--format", "json", "--output", str(output), "--model", "small", "--device", "cpu", "--dtype", "float32", "--batch-size", "1", "--beam-size", str(params["beam_size"]), "--cfg-coef", str(params["cfg_coef"])]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    events = json.loads(output.read_text(encoding="utf-8"))
    return sum(event.get("type") == "start" for event in events)


def main() -> None:
    out = Path(__file__).with_name("muscriptor_tuning_outputs")
    out.mkdir(exist_ok=True)
    results = []
    for params in PARAMETERS:
        counts = {}
        for excerpt in INPUTS:
            output = out / f"{Path(excerpt).stem}_{params['id']}.json"
            counts[excerpt] = run_variant(excerpt, params, output)
        development_error = sum(abs(counts[excerpt] - REFERENCE[excerpt]) for excerpt in INPUTS[:3])
        holdout_error = abs(counts[INPUTS[3]] - REFERENCE[INPUTS[3]])
        results.append({**params, "counts": counts, "development_count_error": development_error, "holdout_count_error": holdout_error})
    report = Path(__file__).with_name("muscriptor_tuning_results.json")
    report.write_text(json.dumps({"parameters": results}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"parameters": results}, indent=2))


if __name__ == "__main__":
    main()
