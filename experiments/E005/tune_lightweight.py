from __future__ import annotations

import csv
import json
from pathlib import Path

import librosa

from ir_research.audio import read_wav
from ir_research.events import detect_events

ROOT = Path(__file__).resolve().parents[2]
DEV = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav")
HOLDOUT = ("low_01_low.wav",)
REFERENCE = ROOT / "experiments" / "E003" / "ground_truth.csv"


def labels() -> dict[str, int]:
    counts: dict[str, int] = {}
    with REFERENCE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            counts[row["excerpt_id"]] = counts.get(row["excerpt_id"], 0) + 1
    return counts


def recursive_error(setting: tuple[int, int, float], excerpt_names: tuple[str, ...], reference: dict[str, int]) -> int:
    error = 0
    for excerpt in excerpt_names:
        audio = read_wav(ROOT / "experiments" / "E002" / "listener_slices" / excerpt)
        detected = detect_events(audio.samples, audio.sample_rate, frame_size=setting[0], hop_size=setting[1], threshold_db=setting[2])
        error += abs(len(detected) - reference[excerpt])
    return error


def librosa_error(delta: float, wait: int, excerpt_names: tuple[str, ...], reference: dict[str, int]) -> int:
    error = 0
    for excerpt in excerpt_names:
        audio = read_wav(ROOT / "experiments" / "E002" / "listener_slices" / excerpt)
        strength = librosa.onset.onset_strength(y=audio.samples.astype(float), sr=audio.sample_rate, hop_length=64, n_fft=256, aggregate=None)
        onsets = librosa.onset.onset_detect(onset_envelope=strength, sr=audio.sample_rate, hop_length=64, units="time", delta=delta, wait=wait)
        error += abs(len(onsets) - reference[excerpt])
    return error


def main() -> None:
    reference = labels()
    recursive_settings = [(128, 32, -38.0), (256, 64, -45.0), (256, 64, -40.0), (256, 64, -35.0)]
    recursive_scores = [{"setting": setting, "development_count_error": recursive_error(setting, DEV, reference)} for setting in recursive_settings]
    best_recursive = min(recursive_scores, key=lambda item: item["development_count_error"])
    librosa_settings = [(0.1, 10), (0.2, 10), (0.3, 10), (0.2, 20), (0.3, 20)]
    librosa_scores = [{"delta": delta, "wait": wait, "development_count_error": librosa_error(delta, wait, DEV, reference)} for delta, wait in librosa_settings]
    best_librosa = min(librosa_scores, key=lambda item: item["development_count_error"])
    holdout_recursive_error = recursive_error(tuple(best_recursive["setting"]), HOLDOUT, reference)
    holdout_librosa_error = librosa_error(best_librosa["delta"], best_librosa["wait"], HOLDOUT, reference)
    result = {
        "development": DEV,
        "holdout": HOLDOUT,
        "recursive_scores": recursive_scores,
        "best_recursive": best_recursive,
        "holdout_recursive_count_error": holdout_recursive_error,
        "librosa_scores": librosa_scores,
        "best_librosa": best_librosa,
        "holdout_librosa_count_error": holdout_librosa_error,
    }
    output = Path(__file__).with_name("tuning_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
