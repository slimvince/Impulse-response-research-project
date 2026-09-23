from __future__ import annotations

from dataclasses import dataclass
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from .audio import read_wav
from .events import detect_events
from .features import FEATURE_VERSION, analyze_frames


@dataclass(frozen=True)
class ManifestItem:
    recording_id: str
    domain: str
    split: str
    path: str
    metadata: dict[str, Any]


def load_manifest(path: str | Path) -> list[ManifestItem]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [ManifestItem(item["recording_id"], item["domain"], item["split"], item["path"], item.get("metadata", {})) for item in raw["recordings"]]


def _event_rows(recording: ManifestItem, audio, events):
    rows = []
    for index, event in enumerate(events):
        frame_data = [row for row in analyze_frames(audio.samples[int(event["start_s"] * audio.sample_rate):int(event["end_s"] * audio.sample_rate)], audio.sample_rate)]
        f0_values = [row["f0_hz"] for row in frame_data if np.isfinite(row["f0_hz"])]
        rows.append({"recording_id": recording.recording_id, "domain": recording.domain, "split": recording.split, "event": index, **event, "median_f0_hz": float(np.median(f0_values)) if f0_values else float("nan")})
    return rows


def analyze_manifest(manifest_path: str | Path, frame_size: int = 4096, hop_size: int = 1024) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    frames: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    for recording in manifest:
        audio = read_wav(recording.path)
        metadata.append({"recording_id": recording.recording_id, "domain": recording.domain, "split": recording.split, "path": recording.path, "sha256": audio.sha256, "sample_rate": audio.sample_rate, "channels": audio.channels, "samples": len(audio.samples), **recording.metadata})
        for row in analyze_frames(audio.samples, audio.sample_rate, frame_size, hop_size):
            frames.append({"recording_id": recording.recording_id, "domain": recording.domain, "split": recording.split, **row})
        detected = detect_events(audio.samples, audio.sample_rate)
        events.extend(_event_rows(recording, audio, detected))
    return {"feature_version": FEATURE_VERSION, "manifest": str(manifest_path), "metadata": metadata, "frames": frames, "events": events}


def summarize(result: dict[str, Any]) -> dict[str, Any]:
    numeric = [key for key in result["frames"][0] if key not in {"frame", "time_s", "recording_id", "domain", "split"}] if result["frames"] else []
    by_domain: dict[str, dict[str, Any]] = {}
    domains = sorted({row["domain"] for row in result["frames"]})
    for domain in domains:
        rows = [row for row in result["frames"] if row["domain"] == domain]
        by_domain[domain] = {key: {"n": len([row[key] for row in rows if np.isfinite(row[key])]), "mean": float(np.nanmean([row[key] for row in rows])), "std": float(np.nanstd([row[key] for row in rows]))} for key in numeric}
    comparisons = []
    if len(domains) == 2:
        left, right = domains
        for key in numeric:
            a = np.array([row[key] for row in result["frames"] if row["domain"] == left], dtype=float)
            b = np.array([row[key] for row in result["frames"] if row["domain"] == right], dtype=float)
            a, b = a[np.isfinite(a)], b[np.isfinite(b)]
            pooled = np.sqrt((np.var(a) + np.var(b)) / 2.0) if len(a) and len(b) else 0.0
            comparisons.append({"feature": key, "left_domain": left, "right_domain": right, "left_mean": float(np.mean(a)) if len(a) else None, "right_mean": float(np.mean(b)) if len(b) else None, "mean_difference": float(np.mean(a) - np.mean(b)) if len(a) and len(b) else None, "standardized_difference": float((np.mean(a) - np.mean(b)) / pooled) if pooled > 1e-12 else None, "interpretation": "descriptive_only"})
    return {"by_domain": by_domain, "comparisons": comparisons, "limitations": ["Frame rows are not independent observations; recording-level replication is required.", "No causal separation of microphone, room, player, or instrument effects is attempted without matched metadata.", "Comparisons are descriptive and are not claims of statistical significance."]}


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
