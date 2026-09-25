from __future__ import annotations

import json
import wave
from pathlib import Path

import aubio

ROOT = Path(__file__).resolve().parents[2]
INPUTS = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav", "low_01_low.wav")


def detect(path: Path) -> list[float]:
    with wave.open(str(path), "rb") as handle:
        sample_rate = handle.getframerate()
        total_frames = handle.getnframes()
    source = aubio.source(str(path), samplerate=0, hop_size=64)
    onset = aubio.onset("specdiff", 256, 64, sample_rate)
    onset.set_threshold(0.7)
    processed = 0
    times: list[float] = []
    while processed < total_frames:
        frames, _ = source()
        if len(frames) == 0:
            break
        processed += len(frames)
        if onset(frames):
            times.append(float(onset.get_last_s()))
    return times


def main() -> None:
    output = {excerpt: {"onsets_s": detect(ROOT / "experiments" / "E002" / "listener_slices" / excerpt)} for excerpt in INPUTS}
    path = Path(__file__).with_name("aubio_tuned_results.json")
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
