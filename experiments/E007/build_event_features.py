from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav
from ir_research.events import detect_events
from ir_research.features import analyze_frames

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).with_name("event_features.csv")
FEATURES = ("rms_db", "spectral_centroid_hz", "spectral_rolloff_hz", "spectral_flux", "f0_hz", "f0_confidence", "harmonicity_db")


def summarize_phase(samples: np.ndarray, sample_rate: int) -> dict[str, float | None]:
    if len(samples) < 256:
        return {feature: None for feature in FEATURES}
    rows = analyze_frames(samples, sample_rate, frame_size=256, hop_size=64)
    result: dict[str, float | None] = {}
    for feature in FEATURES:
        values = np.asarray([row[feature] for row in rows], dtype=float)
        values = values[np.isfinite(values)]
        result[feature] = float(np.median(values)) if len(values) else None
    return result


def main() -> None:
    manifest = json.loads((ROOT / "experiments" / "E007" / "manifest.json").read_text(encoding="utf-8"))
    output_rows: list[dict[str, object]] = []
    for recording in manifest["recordings"]:
        audio = read_wav(recording["path"])
        samples = audio.samples[:min(len(audio.samples), int(30 * audio.sample_rate))] if recording["domain"] == "acoustic_mic" else audio.samples
        events = detect_events(samples, audio.sample_rate, frame_size=256, hop_size=64, threshold_db=-45.0)
        for event_index, event in enumerate(events, 1):
            start = max(0, int(event["start_s"] * audio.sample_rate))
            end = min(len(samples), max(start + 1, int(event["end_s"] * audio.sample_rate)))
            event_samples = samples[start:end]
            phase_samples = np.array_split(event_samples, 4)
            row: dict[str, object] = {
                "recording_id": recording["recording_id"],
                "domain": recording["domain"],
                "source_group": recording.get("metadata", {}).get("source_group", recording["domain"]),
                "articulation": recording.get("metadata", {}).get("articulation_code", "unknown"),
                "event_index": event_index,
                "start_s": event["start_s"],
                "end_s": event["end_s"],
                "duration_s": event["duration_s"],
                "peak_db": event["peak_db"],
            }
            for phase_index, phase_name in enumerate(("attack", "early_sustain", "sustain", "decay")):
                summary = summarize_phase(phase_samples[phase_index], audio.sample_rate)
                for feature, value in summary.items():
                    row[f"{phase_name}_{feature}"] = value
            output_rows.append(row)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Wrote {OUTPUT} with {len(output_rows)} events")


if __name__ == "__main__":
    main()
