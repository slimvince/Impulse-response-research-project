from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
EVENTS = Path(r"C:\IR audio\results\slb200-candidate\events.json")
OUTPUT = ROOT / "experiments" / "E008" / "all_slices"


def write_wav(path: Path, samples: np.ndarray, sample_rate: int) -> None:
    pcm = np.clip(samples, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())


def main() -> None:
    audio = read_wav(SOURCE)
    events = json.loads(EVENTS.read_text(encoding="utf-8"))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for index, event in enumerate(events, start=1):
        start_index = int(float(event["start_s"]) * audio.sample_rate)
        end_index = max(start_index + 1, int(float(event["end_s"]) * audio.sample_rate))
        filename = f"event_{index:04d}.wav"
        write_wav(OUTPUT / filename, audio.samples[start_index:end_index], audio.sample_rate)
        item = dict(event)
        item["event"] = index
        item["file"] = filename
        manifest.append(item)
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(manifest)} raw event slices to {OUTPUT}")


if __name__ == "__main__":
    main()
