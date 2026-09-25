from __future__ import annotations

import json
from pathlib import Path

import librosa

from ir_research.audio import read_wav
from ir_research.events import detect_events


ROOT = Path(__file__).resolve().parents[2]
INPUTS = (
    "low_02_low.wav",
    "bass_friendly_01_bass_friendly.wav",
    "broad_03_broad.wav",
    "low_01_low.wav",
)


def run() -> dict[str, object]:
    output: dict[str, object] = {"candidates": {}, "provenance": {}}
    for excerpt in INPUTS:
        path = ROOT / "experiments" / "E002" / "listener_slices" / excerpt
        audio = read_wav(path)
        recursive = detect_events(audio.samples, audio.sample_rate, frame_size=256, hop_size=64, threshold_db=-45.0)
        onset_strength = librosa.onset.onset_strength(
            y=audio.samples.astype(float),
            sr=audio.sample_rate,
            hop_length=64,
            n_fft=256,
            aggregate=None,
        )
        onset_frames = librosa.onset.onset_detect(
            onset_envelope=onset_strength,
            sr=audio.sample_rate,
            hop_length=64,
            units="time",
            backtrack=False,
            pre_max=6,
            post_max=6,
            pre_avg=6,
            post_avg=6,
            delta=0.2,
            wait=10,
        )
        output["candidates"][excerpt] = {
            "recursive_detector": recursive,
            "librosa_onset": [float(value) for value in onset_frames],
        }
        output["provenance"][excerpt] = {
            "source_path": str(path),
            "source_sha256": audio.sha256,
            "sample_rate": audio.sample_rate,
        }
    return output


def main() -> None:
    output_path = Path(__file__).with_name("results.json")
    output_path.write_text(json.dumps(run(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
