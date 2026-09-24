from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import soundfile as sf

sys.path.insert(0, str(Path(r"C:/IR research/src")))

from basic_pitch.inference import predict
from ir_research.events import detect_events

ROOT = Path(r"C:/IR research")
EXPERIMENT = ROOT / "experiments" / "E002"
RESULTS = EXPERIMENT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

EXCERPTS = [
    {"id": "bassA_1_0_30", "path": "C:/IR audio/acoustic/bass A/1.wav", "start_s": 0.0, "end_s": 30.0},
    {"id": "bassA_2_0_30", "path": "C:/IR audio/acoustic/bass A/2.wav", "start_s": 0.0, "end_s": 30.0},
    {"id": "bassB_3_0_30", "path": "C:/IR audio/acoustic/bass B/3.wav", "start_s": 0.0, "end_s": 30.0},
    {"id": "bassB_4_0_30", "path": "C:/IR audio/acoustic/bass B/4.wav", "start_s": 0.0, "end_s": 30.0},
]

PARAMETER_SETS = [
    {
        "id": "default",
        "onset_threshold": 0.5,
        "frame_threshold": 0.3,
        "minimum_note_length": 127.7,
        "minimum_frequency": 40.0,
        "maximum_frequency": 400.0,
        "multiple_pitch_bends": False,
        "melodia_trick": True,
    },
    {
        "id": "stricter",
        "onset_threshold": 0.7,
        "frame_threshold": 0.5,
        "minimum_note_length": 200.0,
        "minimum_frequency": 40.0,
        "maximum_frequency": 400.0,
        "multiple_pitch_bends": False,
        "melodia_trick": True,
    },
]


def mono_excerpt(path: str, start_s: float, end_s: float) -> tuple[float, list[float]]:
    x, sr = sf.read(path, dtype="float32", always_2d=True)
    start_i = int(start_s * sr)
    end_i = int(end_s * sr)
    clip = x[start_i:end_i]
    mono = clip.mean(axis=1)
    return float(sr), mono.tolist()


summary = {"experiment_id": "E002", "status": "complete", "results": []}

for excerpt in EXCERPTS:
    sr, mono = mono_excerpt(excerpt["path"], excerpt["start_s"], excerpt["end_s"])
    threshold_events = detect_events(
        mono,
        int(sr),
        frame_size=2048,
        hop_size=512,
        threshold_db=-45.0,
    )

    entry = {
        "recording_id": excerpt["id"],
        "source_path": excerpt["path"],
        "excerpt_start_s": excerpt["start_s"],
        "excerpt_end_s": excerpt["end_s"],
        "threshold_detector_event_count": len(threshold_events),
        "basic_pitch": [],
    }

    # write a temporary audio excerpt for Basic Pitch
    temp_path = EXPERIMENT / f"{excerpt['id']}_excerpt.wav"
    x, sr2 = sf.read(excerpt["path"], dtype="float32", always_2d=True)
    start_i = int(excerpt["start_s"] * sr2)
    end_i = int(excerpt["end_s"] * sr2)
    sf.write(temp_path, x[start_i:end_i], sr2)

    for params in PARAMETER_SETS:
        output, midi, note_events = predict(
            str(temp_path),
            onset_threshold=params["onset_threshold"],
            frame_threshold=params["frame_threshold"],
            minimum_note_length=params["minimum_note_length"],
            minimum_frequency=params["minimum_frequency"],
            maximum_frequency=params["maximum_frequency"],
            multiple_pitch_bends=params["multiple_pitch_bends"],
            melodia_trick=params["melodia_trick"],
        )

        normalized = []
        for start_s, end_s, pitch_midi, amplitude, pitch_bends in note_events:
            normalized.append(
                {
                    "start_s": float(start_s),
                    "end_s": float(end_s),
                    "duration_s": float(end_s - start_s),
                    "pitch_midi": int(pitch_midi),
                    "amplitude": float(amplitude),
                    "pitch_bends": [int(v) for v in pitch_bends] if pitch_bends is not None else [],
                }
            )

        durations = [ev["duration_s"] for ev in normalized]
        mean_duration = float(sum(durations) / len(durations)) if durations else 0.0
        entry["basic_pitch"].append(
            {
                "parameter_set": params["id"],
                "event_count": len(normalized),
                "mean_duration_s": mean_duration,
                "min_duration_s": float(min(durations)) if durations else 0.0,
                "max_duration_s": float(max(durations)) if durations else 0.0,
                "events": normalized[:10],
            }
        )

    summary["results"].append(entry)

summary_path = RESULTS / "basic_pitch_gate_summary.json"
summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
