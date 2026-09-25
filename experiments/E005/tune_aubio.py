from __future__ import annotations

import csv
import json
import wave
from pathlib import Path

import aubio

ROOT = Path(__file__).resolve().parents[2]
DEV = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav")
HOLDOUT = ("low_01_low.wav",)
REFERENCE = ROOT / "experiments" / "E003" / "ground_truth.csv"
METHODS = ("default", "hfc", "energy", "specflux", "specdiff", "phase", "complex", "kl", "mkl")
THRESHOLDS = (0.1, 0.3, 0.5, 0.7)


def reference_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    with REFERENCE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            counts[row["excerpt_id"]] = counts.get(row["excerpt_id"], 0) + 1
    return counts


def detect(path: Path, method: str, threshold: float) -> int:
    with wave.open(str(path), "rb") as handle:
        sample_rate = handle.getframerate()
        total_frames = handle.getnframes()
    source = aubio.source(str(path), samplerate=0, hop_size=64)
    onset = aubio.onset(method, 256, 64, sample_rate)
    onset.set_threshold(threshold)
    processed = 0
    count = 0
    while processed < total_frames:
        frames, _ = source()
        if len(frames) == 0:
            break
        processed += len(frames)
        if onset(frames):
            count += 1
    return count


def score(method: str, threshold: float, excerpts: tuple[str, ...], reference: dict[str, int]) -> int:
    error = 0
    for excerpt in excerpts:
        error += abs(detect(ROOT / "experiments" / "E002" / "listener_slices" / excerpt, method, threshold) - reference[excerpt])
    return error


def main() -> None:
    reference = reference_counts()
    scores = []
    for method in METHODS:
        for threshold in THRESHOLDS:
            try:
                development_error = score(method, threshold, DEV, reference)
                scores.append({"method": method, "threshold": threshold, "development_count_error": development_error})
            except Exception as error:
                scores.append({"method": method, "threshold": threshold, "error": str(error)})
    valid = [item for item in scores if "development_count_error" in item]
    best = min(valid, key=lambda item: item["development_count_error"])
    holdout_error = score(best["method"], best["threshold"], HOLDOUT, reference)
    result = {"development": DEV, "holdout": HOLDOUT, "scores": scores, "best": best, "holdout_count_error": holdout_error}
    output = Path(__file__).with_name("aubio_tuning_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
