from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav
from ir_research.events import detect_events


ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = ROOT / "experiments" / "E002" / "listener_slices"
OUTPUT_DIR = ROOT / "experiments" / "E003" / "detected_slices"
INPUTS = (
    "low_02_low.wav",
    "bass_friendly_01_bass_friendly.wav",
    "broad_03_broad.wav",
    "low_01_low.wav",
)
SETTINGS = {
    "baseline_256_64_minus35": (256, 64, -35.0),
    "conservative_256_64_minus45": (256, 64, -45.0),
}


def write_wav(path: Path, samples: np.ndarray, sample_rate: int) -> None:
    pcm = np.clip(samples, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []
    for setting_name, (frame_size, hop_size, threshold_db) in SETTINGS.items():
        setting_dir = OUTPUT_DIR / setting_name
        setting_dir.mkdir(parents=True, exist_ok=True)
        for input_name in INPUTS:
            audio = read_wav(INPUT_DIR / input_name)
            events = detect_events(
                audio.samples,
                audio.sample_rate,
                frame_size=frame_size,
                hop_size=hop_size,
                threshold_db=threshold_db,
            )
            excerpt_id = Path(input_name).stem
            files: list[str] = []
            for event_index, event in enumerate(events, start=1):
                start = event["start_s"]
                end = event["end_s"]
                start_index = int(start * audio.sample_rate)
                end_index = max(start_index + 1, int(end * audio.sample_rate))
                output_path = setting_dir / f"{excerpt_id}_event_{event_index:02d}.wav"
                write_wav(output_path, audio.samples[start_index:end_index], audio.sample_rate)
                files.append(str(output_path.relative_to(ROOT)).replace("\\", "/"))
            manifest.append(
                {
                    "setting": setting_name,
                    "source": input_name,
                    "frame_size": frame_size,
                    "hop_size": hop_size,
                    "threshold_db": threshold_db,
                    "event_count": len(events),
                    "events": events,
                    "files": files,
                }
            )
    manifest_path = OUTPUT_DIR / "review_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    main()
