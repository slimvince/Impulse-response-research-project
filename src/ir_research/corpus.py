from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
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


def _quality_diagnostics(samples: np.ndarray) -> dict[str, float | int]:
    absolute = np.abs(samples)
    rms = float(np.sqrt(np.mean(samples ** 2))) if len(samples) else 0.0
    return {
        "silence_fraction": float(np.mean(absolute <= 1e-8)) if len(samples) else 1.0,
        "clipping_fraction": float(np.mean(absolute >= 0.999969)) if len(samples) else 0.0,
        "dc_offset": float(np.mean(samples)) if len(samples) else 0.0,
        "peak_linear": float(np.max(absolute)) if len(samples) else 0.0,
        "rms_linear": rms,
    }


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
    manifest_path = Path(manifest_path)
    manifest = load_manifest(manifest_path)
    frames: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    for recording in manifest:
        audio = read_wav(recording.path)
        metadata.append({"recording_id": recording.recording_id, "domain": recording.domain, "split": recording.split, "path": recording.path, "sha256": audio.sha256, "sample_rate": audio.sample_rate, "channels": audio.channels, "sample_width_bytes": audio.sample_width_bytes, "samples": len(audio.samples), "duration_s": len(audio.samples) / audio.sample_rate, "quality": _quality_diagnostics(audio.samples), **recording.metadata})
        for row in analyze_frames(audio.samples, audio.sample_rate, frame_size, hop_size):
            frames.append({"recording_id": recording.recording_id, "domain": recording.domain, "split": recording.split, **row})
        detected = detect_events(audio.samples, audio.sample_rate)
        events.extend(_event_rows(recording, audio, detected))
    return {"feature_version": FEATURE_VERSION, "manifest": str(manifest_path), "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(), "analysis_parameters": {"frame_size": frame_size, "hop_size": hop_size}, "metadata": metadata, "frames": frames, "events": events}


def _feature_names(result: dict[str, Any]) -> list[str]:
    excluded = {"frame", "time_s", "recording_id", "domain", "split"}
    return [key for key in result["frames"][0] if key not in excluded] if result["frames"] else []


def _feature_stats(rows: list[dict[str, Any]], feature_names: list[str]) -> dict[str, dict[str, float | int | None]]:
    summary = {}
    for key in feature_names:
        values = np.array([row[key] for row in rows], dtype=float)
        values = values[np.isfinite(values)]
        summary[key] = {
            "n": int(values.size),
            "missing": int(len(rows) - values.size),
            "mean": float(np.mean(values)) if values.size else None,
            "std": float(np.std(values)) if values.size else None,
            "median": float(np.median(values)) if values.size else None,
            "q10": float(np.quantile(values, 0.10)) if values.size else None,
            "q90": float(np.quantile(values, 0.90)) if values.size else None,
        }
    return summary


def summarize(result: dict[str, Any]) -> dict[str, Any]:
    numeric = _feature_names(result)
    metadata_by_id = {item["recording_id"]: item for item in result["metadata"]}
    recording_rows = {}
    for recording_id, metadata in metadata_by_id.items():
        rows = [row for row in result["frames"] if row["recording_id"] == recording_id]
        recording_rows[recording_id] = {"recording_id": recording_id, "domain": metadata["domain"], "split": metadata["split"], "source_group": metadata.get("comparison_group_id", metadata.get("source_group", metadata["domain"])), "frame_count": len(rows), "event_count": sum(1 for event in result["events"] if event["recording_id"] == recording_id), "features": _feature_stats(rows, numeric)}
    groups: dict[str, list[str]] = {}
    for recording_id, item in recording_rows.items():
        groups.setdefault(str(item["source_group"]), []).append(recording_id)
    source_groups = {}
    for group, recording_ids in groups.items():
        source_groups[group] = {"source_group": group, "recording_ids": recording_ids, "recording_count": len(recording_ids), "features": {feature: {"n_recordings": sum(recording_rows[recording_id]["features"][feature]["n"] > 0 for recording_id in recording_ids), "mean_of_recording_means": float(np.mean([recording_rows[recording_id]["features"][feature]["mean"] for recording_id in recording_ids if recording_rows[recording_id]["features"][feature]["mean"] is not None])) if any(recording_rows[recording_id]["features"][feature]["mean"] is not None for recording_id in recording_ids) else None} for feature in numeric}}
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
    return {"by_domain": by_domain, "by_recording": recording_rows, "by_source_group": source_groups, "comparisons": comparisons, "limitations": ["Frame rows are not independent observations; recording-level and source-group replication are required.", "Source-group summaries use the mean of recording means and do not remove unknown level, content, or setup confounds.", "Comparisons are descriptive and are not claims of statistical significance."]}


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
