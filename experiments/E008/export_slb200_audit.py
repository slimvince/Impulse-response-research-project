from __future__ import annotations

import argparse
import json
import wave
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav


DEFAULT_SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
DEFAULT_EVENTS = Path(r"C:\IR audio\results\slb200-candidate\events.json")
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "audit_slices"


def write_wav(path: Path, samples: np.ndarray, sample_rate: int) -> None:
    pcm = np.clip(samples, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())


def select_events(events: list[dict[str, object]]) -> list[tuple[str, dict[str, object]]]:
    selected: dict[int, tuple[str, dict[str, object]]] = {}

    def add(category: str, candidates: list[dict[str, object]]) -> None:
        for event in candidates[:12]:
            index = int(event["event"])
            selected.setdefault(index, (category, event))

    add("shortest", sorted(events, key=lambda event: float(event["duration_s"])))
    add("longest", sorted(events, key=lambda event: float(event["duration_s"]), reverse=True))
    add("quietest", sorted(events, key=lambda event: float(event["peak_db"])))
    add("late_attack", sorted(events, key=lambda event: float(event["attack_time_s"]), reverse=True))

    timeline_indices = np.linspace(0, len(events) - 1, num=min(12, len(events)), dtype=int)
    add("timeline", [events[index] for index in timeline_indices])
    return sorted(selected.values(), key=lambda item: int(item[1]["event"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    audio = read_wav(args.source)
    events = json.loads(args.events.read_text(encoding="utf-8"))
    selected = select_events(events)
    args.output.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, object]] = []
    links: list[str] = [
        "# SLB-200 Audit Slices",
        "",
        "These are exact detector-boundary slices from the analyzed mono signal. No fades, padding, normalization, or postprocessing were applied.",
        "",
        "| Category | Event | Time (s) | Duration (s) | Peak (dB) | Attack (s) | Median f0 (Hz) | File |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for category, event in selected:
        event_index = int(event["event"])
        median_f0 = event["median_f0_hz"]
        median_f0_text = "unknown" if median_f0 is None else f"{float(median_f0):.1f}"
        start_index = int(float(event["start_s"]) * audio.sample_rate)
        end_index = max(start_index + 1, int(float(event["end_s"]) * audio.sample_rate))
        filename = f"{category}_event_{event_index + 1:04d}.wav"
        output_path = args.output / filename
        write_wav(output_path, audio.samples[start_index:end_index], audio.sample_rate)
        relative_path = output_path.relative_to(Path(__file__).resolve().parents[1]).as_posix()
        links.append(
            f"| {category} | {event_index + 1} | {float(event['start_s']):.3f}-{float(event['end_s']):.3f} | "
            f"{float(event['duration_s']):.3f} | {float(event['peak_db']):.1f} | {float(event['attack_time_s']):.3f} | "
            f"{median_f0_text} | [{filename}]({relative_path}) |"
        )
        manifest.append({"category": category, **event, "file": relative_path})

    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (args.output / "AUDIT_LINKS.md").write_text("\n".join(links) + "\n", encoding="utf-8")
    print(f"Selected {len(selected)} events from {len(events)} total events")
    print(f"Wrote audit slices to {args.output}")


if __name__ == "__main__":
    main()
