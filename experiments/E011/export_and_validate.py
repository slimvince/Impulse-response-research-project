from __future__ import annotations

import csv
import json
import math
import wave
from collections import Counter
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav
from ir_research.events import detect_events

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
E008_MANIFEST = ROOT / "experiments" / "E008" / "all_slices" / "manifest.json"
E008_LABELS = ROOT / "experiments" / "E008" / "audit_slices" / "slb200_event_review.csv"
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

    old_events = json.loads(E008_MANIFEST.read_text(encoding="utf-8"))
    old_by_id = {int(event["event"]): event for event in old_events}
    with E008_LABELS.open(newline="", encoding="utf-8") as handle:
        labels = list(csv.DictReader(handle))
    rows = []
    for label in labels:
        old = old_by_id[int(label["event"])]
        old_start = float(old["start_s"])
        old_end = float(old["end_s"])
        old_duration = old_end - old_start
        overlaps = []
        for event in manifest:
            overlap = max(0.0, min(old_end, event["end_s"]) - max(old_start, event["start_s"]))
            if overlap > 0:
                overlaps.append((event, overlap))
        covered = sum(overlap for _, overlap in overlaps)
        strong = [(event, overlap) for event, overlap in overlaps if overlap / old_duration >= 0.90]
        exact_match = len(strong) == 1 and strong[0][1] / max(strong[0][0]["duration_s"], 1e-12) >= 0.90
        if label["verdict"] == "Use":
            outcome = "use_contained_tightly" if exact_match else "use_contained_in_longer_or_split_event"
        elif label.get("annotation", "").strip().lower() in {"silence", "silcence"}:
            exact_disq = any(
                abs(event["start_s"] - old_start) < 0.001
                and abs(event["end_s"] - old_end) < 0.001
                and event["quality_status"] == "disqualified"
                for event, _ in overlaps
            )
            if exact_disq:
                outcome = "silence_disqualified"
            elif overlaps and max(event["duration_s"] for event, _ in overlaps) > 0.10:
                outcome = "silence_interval_absorbed"
            else:
                outcome = "silence_unresolved"
        else:
            outcome = "negative_interval_retained_or_absorbed"
        rows.append({
            "old_event": int(label["event"]),
            "verdict": label["verdict"],
            "annotation": label.get("annotation", ""),
            "old_start_s": old_start,
            "old_end_s": old_end,
            "covered_fraction": covered / old_duration if old_duration else 0.0,
            "outcome": outcome,
            "overlaps": [{"event": event["event"], "start_s": event["start_s"], "end_s": event["end_s"], "duration_s": event["duration_s"], "quality_status": event["quality_status"], "overlap_s": overlap} for event, overlap in overlaps],
        })
    counts = Counter(event["quality_status"] for event in manifest)
    validation = {
        "validation_source": "durable E008 listener audit CSV, mapped by source-time overlap",
        "reviewed_label_count": len(rows),
        "verdict_counts": dict(Counter(row["verdict"] for row in rows)),
        "outcome_counts": dict(Counter(row["outcome"] for row in rows)),
        "quality_status_counts": dict(counts),
        "event_count": len(manifest),
        "labels": rows,
        "limitations": [
            "Only the durable 57-row E008 audit CSV was available; later browser-only rulings were not present in the workspace.",
            "E008 verdicts are interval usability labels, not precise ground-truth onset/offset labels.",
            "A Use label means the old interval was judged usable; it does not prove the new event must have identical endpoints.",
            "Silence/noise is automatically rejected only for strict short, low-level, nonperiodic cases. Longer user-labeled silence cases with periodic-looking content remain unresolved or are absorbed into longer events.",
            "This experiment does not validate polyphony classification or prove all tonal candidates are clean monophonic notes."
        ]
    }
    (OUTPUT / "validation.json").write_text(json.dumps(validation, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    metadata = {
        "source": str(SOURCE),
        "source_sha256": audio.sha256,
        "sample_rate": audio.sample_rate,
        "source_channels": audio.channels,
        "sample_width_bytes": audio.sample_width_bytes,
        "event_count": len(events),
        "quality_status_counts": dict(counts),
        "slice_policy": "Exact detector-boundary samples from the mono analysis signal; no fades, padding, normalization, or postprocessing.",
        "validation": "Compared to saved E008 labels by source-time overlap. E008/E009 artifacts and labels are untouched."
    }
    (OUTPUT / "run_metadata.json").write_text(json.dumps(metadata, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"E011 events: {len(events)}")
    print(f"Quality: {dict(counts)}")
    print(f"Validation outcomes: {dict(Counter(row['outcome'] for row in rows))}")


if __name__ == "__main__":
    main()
