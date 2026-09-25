from __future__ import annotations

import csv
import json
from pathlib import Path

import soundfile as sf
from basic_pitch.inference import predict

ROOT = Path(__file__).resolve().parents[2]
TEMP_DIR = Path(__file__).with_name("tmp_basic_pitch_tuning")
DEV = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav")
HOLDOUT = ("low_01_low.wav",)
REFERENCE = ROOT / "experiments" / "E003" / "ground_truth.csv"
PARAMETERS = (
    {"id": "permissive_short", "onset_threshold": 0.3, "frame_threshold": 0.1, "minimum_note_length": 50.0},
    {"id": "permissive", "onset_threshold": 0.4, "frame_threshold": 0.2, "minimum_note_length": 80.0},
    {"id": "default", "onset_threshold": 0.5, "frame_threshold": 0.3, "minimum_note_length": 127.7},
    {"id": "strict", "onset_threshold": 0.7, "frame_threshold": 0.5, "minimum_note_length": 200.0},
)


def references() -> dict[str, int]:
    counts: dict[str, int] = {}
    with REFERENCE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            counts[row["excerpt_id"]] = counts.get(row["excerpt_id"], 0) + 1
    return counts


def count(path: Path, params: dict[str, object]) -> int:
    TEMP_DIR.mkdir(exist_ok=True)
    samples, sample_rate = sf.read(str(path), dtype="float32", always_2d=True)
    temp = TEMP_DIR / path.name
    sf.write(str(temp), samples, sample_rate)
    _, _, events = predict(
        str(temp),
        onset_threshold=params["onset_threshold"],
        frame_threshold=params["frame_threshold"],
        minimum_note_length=params["minimum_note_length"],
        minimum_frequency=40.0,
        maximum_frequency=400.0,
        multiple_pitch_bends=False,
        melodia_trick=True,
    )
    temp.unlink(missing_ok=True)
    return len(events)


def score(params: dict[str, object], excerpts: tuple[str, ...], reference: dict[str, int]) -> int:
    return sum(
        abs(count(ROOT / "experiments" / "E002" / "listener_slices" / excerpt, params) - reference[excerpt])
        for excerpt in excerpts
    )


def main() -> None:
    reference = references()
    scores = [{**params, "development_count_error": score(params, DEV, reference)} for params in PARAMETERS]
    best = min(scores, key=lambda item: item["development_count_error"])
    holdout_error = score(best, HOLDOUT, reference)
    output = {"development": DEV, "holdout": HOLDOUT, "scores": scores, "best": best, "holdout_count_error": holdout_error}
    path = Path(__file__).with_name("basic_pitch_tuning_results.json")
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
