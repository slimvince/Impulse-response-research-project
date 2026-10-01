from __future__ import annotations

import csv
import argparse
import hashlib
import json
import math
import wave
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from ir_research.audio import read_wav
from ir_research.features import analyze_frames

MANIFEST = Path(r"C:\IR audio\slb200-cubase-slices-manifest.json")
OUTPUT = Path(__file__).resolve().parent
RESULTS = OUTPUT / "results"
CSV_OUTPUT = RESULTS / "candidate_validation.csv"
JSON_OUTPUT = RESULTS / "candidate_validation.json"
SUMMARY_OUTPUT = RESULTS / "summary.json"
ADDITIONAL_SETS = (
    {
        "slice_set_id": "acoustic_bass_a_take_2_cubase_slices",
        "directory": Path(r"C:\IR audio\acoustic\bass A\2 sliced"),
        "source_recording": Path(r"C:\IR audio\acoustic\bass A\2.wav"),
        "expected_count": 1204,
    },
    {
        "slice_set_id": "acoustic_bass_a_take_3_cubase_slices",
        "directory": Path(r"C:\IR audio\acoustic\bass A\3 sliced"),
        "source_recording": Path(r"C:\IR audio\acoustic\bass A\3.wav"),
        "expected_count": 689,
    },
    {
        "slice_set_id": "acoustic_bass_b_take_1_cubase_slices",
        "directory": Path(r"C:\IR audio\acoustic\bass B\3 split"),
        "source_recording": Path(r"C:\IR audio\acoustic\bass B\3.wav"),
        "expected_count": 1363,
    },
)


def decibels(value: float) -> float:
    return 20.0 * math.log10(max(float(value), 1e-12))


def envelope_metrics(samples: np.ndarray, sample_rate: int) -> dict[str, Any]:
    frame_size = max(128, int(round(sample_rate * 0.02)))
    hop_size = max(1, int(round(sample_rate * 0.005)))
    if len(samples) < frame_size:
        padded = np.pad(samples, (0, frame_size - len(samples)))
        frames = padded[None, :]
    else:
        count = 1 + (len(samples) - frame_size) // hop_size
        starts = np.arange(count) * hop_size
        frames = np.stack([samples[start:start + frame_size] for start in starts])
    levels_db = np.asarray([decibels(np.sqrt(np.mean(frame**2))) for frame in frames])
    peak_db = decibels(np.max(np.abs(samples))) if len(samples) else -120.0

    active = levels_db >= peak_db - 18.0
    onset_index = int(np.flatnonzero(active)[0]) if np.any(active) else len(levels_db)
    onset_s = onset_index * hop_size / sample_rate
    internal_attacks: list[float] = []
    last_attack = -1.0
    for index in range(max(4, onset_index + int(0.12 * sample_rate / hop_size)), len(levels_db) - 8):
        baseline = float(np.median(levels_db[max(0, index - 10):index - 2]))
        local_peak_index = index + int(np.argmax(levels_db[index:index + 8]))
        rise_db = float(levels_db[local_peak_index] - baseline)
        attack_s = local_peak_index * hop_size / sample_rate
        if rise_db >= 8.0 and attack_s - last_attack >= 0.12:
            internal_attacks.append(attack_s)
            last_attack = attack_s

    tail_size = min(len(samples), int(round(0.025 * sample_rate)))
    tail_rms_db = decibels(np.sqrt(np.mean(samples[-tail_size:] ** 2))) if tail_size else -120.0
    tail_active = tail_rms_db >= peak_db - 18.0
    return {
        "peak_dbfs": peak_db,
        "rms_dbfs": decibels(np.sqrt(np.mean(samples**2))) if len(samples) else -120.0,
        "onset_offset_s": onset_s,
        "internal_attack_candidates": len(internal_attacks),
        "internal_attack_times_s": internal_attacks,
        "tail_rms_dbfs": tail_rms_db,
        "tail_active_at_boundary": bool(tail_active),
        "all_zero_fraction": float(np.mean(samples == 0.0)) if len(samples) else 1.0,
        "clipped_fraction": float(np.mean(np.abs(samples) >= 0.999)) if len(samples) else 0.0,
        "frame_count": int(len(frames)),
    }


def pitch_metrics(samples: np.ndarray, sample_rate: int) -> dict[str, Any]:
    if len(samples) < 2048:
        return {"f0_reliability": "insufficient_duration", "f0_coverage": 0.0, "median_f0_hz": None, "median_f0_confidence": None}
    frames = analyze_frames(samples, sample_rate, frame_size=2048, hop_size=512)
    f0 = np.asarray([row["f0_hz"] for row in frames], dtype=float)
    confidence = np.asarray([row["f0_confidence"] for row in frames], dtype=float)
    valid = np.isfinite(f0) & np.isfinite(confidence) & (confidence >= 0.25)
    coverage = float(np.mean(valid)) if len(valid) else 0.0
    pitch_values = f0[valid]
    reliability = "reliable" if len(pitch_values) >= 3 and coverage >= 0.35 else "weak"
    finite_confidence = confidence[np.isfinite(confidence)]
    return {
        "f0_reliability": reliability,
        "f0_coverage": coverage,
        "median_f0_hz": float(np.median(pitch_values)) if len(pitch_values) else None,
        "median_f0_confidence": float(np.median(finite_confidence)) if len(finite_confidence) else None,
    }


def classify(metrics: dict[str, Any], duration_s: float) -> tuple[str, list[str]]:
    reasons: list[str] = []
    peak_db = metrics["peak_dbfs"]
    rms_db = metrics["rms_dbfs"]
    clipped_fraction = metrics["clipped_fraction"]
    if peak_db <= -90.0 or (metrics["all_zero_fraction"] >= 0.995 and peak_db <= -70.0):
        return "reject", ["digital_or_effective_silence"]
    if clipped_fraction >= 0.01:
        return "reject", ["severe_clipping"]

    if clipped_fraction > 0.0:
        reasons.append("possible_clipping")
    if duration_s < 0.08:
        reasons.append("very_short_candidate")
    if peak_db < -50.0 or rms_db < -60.0:
        reasons.append("low_signal_level")
    if metrics["onset_offset_s"] > 0.15:
        reasons.append("possible_leading_bleed_or_missing_attack")
    if metrics["internal_attack_candidates"]:
        reasons.append("possible_multiple_excitation_or_internal_transient")
    if metrics["tail_active_at_boundary"]:
        reasons.append("possible_truncated_sustain_or_decay")
    if reasons:
        return "uncertain", reasons
    return "accept", ["no_flagged_event_validity_issue"]


def main() -> None:
    global RESULTS, CSV_OUTPUT, JSON_OUTPUT, SUMMARY_OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-additional-sets", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=RESULTS)
    args = parser.parse_args()
    RESULTS = args.output_dir
    CSV_OUTPUT = RESULTS / "candidate_validation.csv"
    JSON_OUTPUT = RESULTS / "candidate_validation.json"
    SUMMARY_OUTPUT = RESULTS / "summary.json"
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    RESULTS.mkdir(parents=True, exist_ok=True)
    groups = list(manifest["sets"])
    for extra in ADDITIONAL_SETS if args.include_additional_sets else ():
        files = []
        for path in sorted(extra["directory"].glob("*.wav"), key=lambda item: item.name.casefold()):
            with wave.open(str(path), "rb") as handle:
                files.append({
                    "file": path.name,
                    "sha256": None,
                    "duration_s": handle.getnframes() / handle.getframerate(),
                    "sample_rate": handle.getframerate(),
                    "channels": handle.getnchannels(),
                    "sample_width_bytes": handle.getsampwidth(),
                })
        if len(files) != extra["expected_count"]:
            raise RuntimeError(
                f"Unexpected candidate count for {extra['slice_set_id']}: "
                f"expected {extra['expected_count']}, found {len(files)}"
            )
        if not extra["source_recording"].is_file():
            raise FileNotFoundError(f"Missing source recording: {extra['source_recording']}")
        groups.append({
            "slice_set_id": extra["slice_set_id"],
            "directory": str(extra["directory"]),
            "source_recording": str(extra["source_recording"]),
            "file_count": len(files),
            "files": files,
            "integrity_basis": "sha256_recorded_during_E012_validation",
        })
    rows: list[dict[str, Any]] = []
    input_sets = []
    for group in groups:
        root = Path(group["directory"])
        input_sets.append({
            "slice_set_id": group["slice_set_id"],
            "directory": str(root),
            "source_recording": group.get("source_recording"),
            "source_available": bool(group.get("source_recording") and Path(group["source_recording"]).is_file()),
            "file_count": len(group["files"]),
            "integrity_basis": group.get("integrity_basis", "external_pinned_manifest"),
        })
        for item in group["files"]:
            path = root / item["file"]
            row: dict[str, Any] = {
                "slice_set_id": group["slice_set_id"],
                "candidate_id": f"{group['slice_set_id']}:{item['file']}",
                "file": str(path),
                "filename": item["file"],
                "source_recording": group.get("source_recording"),
                "source_available": bool(group.get("source_recording") and Path(group["source_recording"]).is_file()),
                "manifest_sha256": item["sha256"],
                "integrity_basis": group.get("integrity_basis", "external_pinned_manifest"),
                "duration_s": item["duration_s"],
                "sample_rate": item["sample_rate"],
                "channels": item["channels"],
                "sample_width_bytes": item["sample_width_bytes"],
            }
            reasons: list[str] = []
            try:
                audio = read_wav(path)
                row["observed_sha256"] = audio.sha256
                row["hash_matches_manifest"] = (
                    audio.sha256.lower() == item["sha256"].lower()
                    if item.get("sha256") else None
                )
                if row["hash_matches_manifest"] is False:
                    row.update({"event_validity": "reject", "reasons": ["manifest_hash_mismatch"]})
                    rows.append(row)
                    continue
                row.update(envelope_metrics(audio.samples, audio.sample_rate))
                row.update(pitch_metrics(audio.samples, audio.sample_rate))
                row["event_validity"], reasons = classify(row, float(item["duration_s"]))
                row["reasons"] = reasons
            except Exception as error:
                row["event_validity"] = "reject"
                row["reasons"] = ["unreadable_or_unsupported_file"]
                row["error"] = f"{type(error).__name__}: {error}"
            row["feature_reliability"] = {
                "f0": row.get("f0_reliability", "not_measured"),
                "spectral": "not_assessed_by_event_validator",
            }
            row["transformation_relevance"] = "not_assessed"
            rows.append(row)

    fields = list(dict.fromkeys(key for row in rows for key in row))
    with CSV_OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=True) if isinstance(value, (list, dict)) else value for key, value in row.items()})
    JSON_OUTPUT.write_text(json.dumps(rows, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    summary = {
        "manifest": str(MANIFEST),
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "candidate_count": len(rows),
        "input_sets": input_sets,
        "by_slice_set": {},
        "definitions": {
            "accept": "No current heuristic flag. Provisional only; not human-validated.",
            "reject": "Only file hash/read failure, effective digital silence, or >=1% clipped samples.",
            "uncertain": "One or more inspectable concerns; no hard exclusion implied.",
            "thresholds": "Exploratory starting values, not established validator thresholds.",
        },
        "scope": "Event validity is separate from feature reliability and transformation relevance; bowed-note classification is out of scope.",
    }
    for slice_set in sorted({row["slice_set_id"] for row in rows}):
        subset = [row for row in rows if row["slice_set_id"] == slice_set]
        summary["by_slice_set"][slice_set] = {
            "count": len(subset),
            "judgments": dict(Counter(row["event_validity"] for row in subset)),
            "reason_counts": dict(Counter(reason for row in subset for reason in row.get("reasons", []))),
            "f0_reliability": dict(Counter(row.get("f0_reliability", "unavailable") for row in subset)),
        }
    SUMMARY_OUTPUT.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (RESULTS / "input_sets.json").write_text(json.dumps(input_sets, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Validated {len(rows)} Cubase candidates")
    for slice_set, result in summary["by_slice_set"].items():
        print(slice_set, result["judgments"], "f0", result["f0_reliability"])


if __name__ == "__main__":
    main()
