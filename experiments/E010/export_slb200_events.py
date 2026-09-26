from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav
from ir_research.events import detect_events

SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
OUTPUT = Path(__file__).resolve().parent
SLICE_DIR = OUTPUT / "slices"


def json_safe(value):
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, (float, np.floating)) and not np.isfinite(value):
        return None
    if isinstance(value, np.generic):
        return value.item()
    return value


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
    events = detect_events(audio.samples, audio.sample_rate)
    SLICE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for index, event in enumerate(events, start=1):
        start = max(0, int(event["start_s"] * audio.sample_rate))
        end = min(len(audio.samples), max(start + 1, int(event["end_s"] * audio.sample_rate)))
        filename = f"event_{index:04d}.wav"
        write_wav(SLICE_DIR / filename, audio.samples[start:end], audio.sample_rate)
        manifest.append({"event": index, **event, "file": f"slices/{filename}"})
    manifest = json_safe(manifest)
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    counts = {status: sum(event["quality_status"] == status for event in events) for status in sorted({event["quality_status"] for event in events})}
    metadata = {
        "source": str(SOURCE),
        "source_sha256": audio.sha256,
        "sample_rate": audio.sample_rate,
        "source_channels": audio.channels,
        "sample_width_bytes": audio.sample_width_bytes,
        "event_count": len(events),
        "quality_status_counts": counts,
        "slice_policy": "Exact detector-boundary samples from the mono analysis signal; no fades, padding, normalization, or postprocessing.",
        "note": "Independent E010 iteration. E008/E009 slices and judgments were not modified or remapped."
    }
    (OUTPUT / "run_metadata.json").write_text(json.dumps(metadata, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Exported {len(events)} events to {SLICE_DIR}; quality={counts}")


if __name__ == "__main__":
    main()
