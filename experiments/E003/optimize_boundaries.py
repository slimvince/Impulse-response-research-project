from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav
from ir_research.events import _onset_breaks, detect_events


def _db_frames(samples: np.ndarray, frame_size: int, hop_size: int) -> np.ndarray:
    padded = np.pad(samples, (0, max(0, frame_size - len(samples))))
    rms = [
        np.sqrt(np.mean(padded[start:start + frame_size] ** 2))
        for start in range(0, len(padded) - frame_size + 1, hop_size)
    ]
    return 20.0 * np.log10(np.maximum(rms, 1e-12))


def optimize_events(samples: np.ndarray, sample_rate: int, detected: list[dict[str, float]], frame_size: int = 256, hop_size: int = 64) -> list[dict[str, float]]:
    if len(detected) < 2:
        return detected
    db = _db_frames(samples, frame_size, hop_size)
    current_boundaries = [round(event["start_s"] * sample_rate / hop_size) for event in detected[1:]]
    onset_boundaries = _onset_breaks(db, 0, len(db), hop_size, sample_rate)
    candidates = sorted(set(current_boundaries + onset_boundaries))
    candidates = [candidate for candidate in candidates if int(0.08 * sample_rate / hop_size) <= candidate <= len(db) - 2]
    candidate_scores = {candidate: max(0.0, float(db[candidate] - db[candidate - 1])) for candidate in candidates}
    segment_count = len(detected)
    boundary_count = segment_count - 1
    states: dict[tuple[int, int], tuple[float, list[int]]] = {}
    for candidate in candidates:
        movement_penalty = abs(candidate - current_boundaries[0]) * hop_size / sample_rate * 12.0
        states[(1, candidate)] = (candidate_scores[candidate] - movement_penalty, [candidate])
    for level in range(2, boundary_count + 1):
        next_states: dict[tuple[int, int], tuple[float, list[int]]] = {}
        for (previous_level, previous), (score, path) in states.items():
            if previous_level != level - 1:
                continue
            for candidate in candidates:
                if candidate <= previous:
                    continue
                duration = (candidate - previous) * hop_size / sample_rate
                if duration < 0.04:
                    continue
                reference_boundary = current_boundaries[level - 1]
                movement_penalty = abs(candidate - reference_boundary) * hop_size / sample_rate * 12.0
                candidate_score = score + candidate_scores[candidate] - movement_penalty - max(0.0, duration - 1.5) * 0.5
                key = (level, candidate)
                if key not in next_states or candidate_score > next_states[key][0]:
                    next_states[key] = (candidate_score, path + [candidate])
        states.update(next_states)
    paths = [value for (level, _), value in states.items() if level == boundary_count]
    if not paths:
        return detected
    _, boundaries = max(paths, key=lambda item: item[0])
    points = [0] + boundaries + [int(round(detected[-1]["end_s"] * sample_rate / hop_size))]
    return [
        {"start_s": points[index] * hop_size / sample_rate, "end_s": points[index + 1] * hop_size / sample_rate}
        for index in range(segment_count)
    ]


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    excerpts = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav", "low_01_low.wav")
    output: dict[str, object] = {}
    for excerpt in excerpts:
        audio = read_wav(root / "experiments" / "E002" / "listener_slices" / excerpt)
        detected = detect_events(audio.samples, audio.sample_rate, frame_size=256, hop_size=64, threshold_db=-45)
        optimized = optimize_events(audio.samples, audio.sample_rate, detected)
        output[excerpt] = {"detected": detected, "optimized": optimized}
    path = root / "experiments" / "E003" / "optimized_boundary_probe.json"
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
