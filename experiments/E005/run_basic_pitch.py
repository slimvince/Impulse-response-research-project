from __future__ import annotations

import json
from pathlib import Path

import soundfile as sf
from basic_pitch.inference import predict


ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = ROOT / "experiments" / "E002" / "listener_slices"
TEMP_DIR = Path(__file__).with_name("tmp_basic_pitch")
EXCERPTS = (
    "low_02_low.wav",
    "bass_friendly_01_bass_friendly.wav",
    "broad_03_broad.wav",
    "low_01_low.wav",
)
PARAMETER_SETS = (
    {
        "id": "default",
        "onset_threshold": 0.5,
        "frame_threshold": 0.3,
        "minimum_note_length": 127.7,
    },
    {
        "id": "stricter",
        "onset_threshold": 0.7,
        "frame_threshold": 0.5,
        "minimum_note_length": 200.0,
    },
)


def main() -> None:
    TEMP_DIR.mkdir(exist_ok=True)
    results: list[dict[str, object]] = []
    for excerpt in EXCERPTS:
        source = INPUT_DIR / excerpt
        samples, sample_rate = sf.read(str(source), dtype="float32", always_2d=True)
        temp_path = TEMP_DIR / excerpt
        sf.write(str(temp_path), samples, sample_rate)
        excerpt_result: dict[str, object] = {"excerpt_id": excerpt, "parameter_sets": []}
        for params in PARAMETER_SETS:
            _, _, note_events = predict(
                str(temp_path),
                onset_threshold=params["onset_threshold"],
                frame_threshold=params["frame_threshold"],
                minimum_note_length=params["minimum_note_length"],
                minimum_frequency=40.0,
                maximum_frequency=400.0,
                multiple_pitch_bends=False,
                melodia_trick=True,
            )
            events = [
                {
                    "start_s": float(start_s),
                    "end_s": float(end_s),
                    "duration_s": float(end_s - start_s),
                    "pitch_midi": int(pitch_midi),
                    "amplitude": float(amplitude),
                    "pitch_bends": [int(value) for value in pitch_bends] if pitch_bends is not None else [],
                }
                for start_s, end_s, pitch_midi, amplitude, pitch_bends in note_events
            ]
            excerpt_result["parameter_sets"].append(
                {
                    "id": params["id"],
                    "event_count": len(events),
                    "events": events,
                }
            )
        results.append(excerpt_result)
        temp_path.unlink(missing_ok=True)
    output = {"candidate": "basic_pitch", "results": results}
    output_path = Path(__file__).with_name("basic_pitch_results.json")
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
