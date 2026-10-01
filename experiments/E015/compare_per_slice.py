from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from ir_research.audio import read_wav
from ir_research.features import analyze_frames

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent
E013_VALIDATION = ROOT / "experiments" / "E013" / "results" / "candidate_validation.json"
E015_MAP = ROOT / "experiments" / "E015" / "results" / "source_time_map.json"
E008_OLD_MANIFEST = ROOT / "experiments" / "E008" / "all_slices" / "manifest.json"
E008_LABELS = ROOT / "experiments" / "E008" / "audit_slices" / "slb200_event_review.csv"
SLB_SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
FILTERED_SOURCE = Path(r"C:\IR audio\results\E014\vincents_1_candidate_acoustic_EQ_E014.wav")
RESULTS = OUTPUT / "results"
SAMPLE_RATE = 44100
FFT_SIZE = 8192
FRAME_SIZE = 4096
HOP_SIZE = 2048
THIRD_OCTAVE_CENTERS = 31.5 * 2 ** (np.arange(0, 29) / 3.0)
THIRD_OCTAVE_CENTERS = THIRD_OCTAVE_CENTERS[THIRD_OCTAVE_CENTERS <= 16000]


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, (float, np.floating)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, np.generic):
        return value.item()
    return value


def median_or_none(values: list[float]) -> float | None:
    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    return float(np.median(finite)) if len(finite) else None


def matches_condition(row: dict[str, Any], register_name: str | None, level_name: str | None) -> bool:
    return (register_name is None or row["register"] == register_name) and (
        level_name is None or row["level_bin"] == level_name
    )


def summarize_audio(samples: np.ndarray, sample_rate: int) -> dict[str, Any]:
    if sample_rate != SAMPLE_RATE:
        raise ValueError(f"Expected {SAMPLE_RATE} Hz, got {sample_rate}")
    if len(samples) < FRAME_SIZE:
        samples = np.pad(samples, (0, FRAME_SIZE - len(samples)))
    count = 1 + max(0, (len(samples) - FRAME_SIZE) // HOP_SIZE)
    starts = np.arange(count) * HOP_SIZE
    window = np.hanning(FRAME_SIZE)
    spectra = []
    frames = []
    for start in starts:
        frame = samples[start:start + FRAME_SIZE]
        if len(frame) < FRAME_SIZE:
            frame = np.pad(frame, (0, FRAME_SIZE - len(frame)))
        frames.append(frame)
        spectra.append(np.abs(np.fft.rfft(frame * window, n=FFT_SIZE)) ** 2)
    mean_power = np.mean(np.stack(spectra), axis=0)
    total_power = float(np.sum(mean_power))
    frequencies = np.fft.rfftfreq(FFT_SIZE, 1.0 / sample_rate)
    band_power = []
    for center in THIRD_OCTAVE_CENTERS:
        mask = (frequencies >= center / (2 ** (1 / 6))) & (frequencies < center * (2 ** (1 / 6)))
        band_power.append(float(np.sum(mean_power[mask])))
    band_power_array = np.asarray(band_power, dtype=float)
    normalized_third_octave_db = 10.0 * np.log10(np.maximum(band_power_array / max(float(np.sum(band_power_array)), 1e-30), 1e-15))
    spectral_rows = analyze_frames(samples, sample_rate, frame_size=FRAME_SIZE, hop_size=HOP_SIZE)
    f0 = [float(row["f0_hz"]) for row in spectral_rows]
    confidence = [float(row["f0_confidence"]) for row in spectral_rows]
    valid_f0 = [value for value, conf in zip(f0, confidence) if np.isfinite(value) and np.isfinite(conf) and conf >= 0.25]
    rms = float(np.sqrt(np.mean(samples**2))) if len(samples) else 0.0
    centroid = float(np.sum(frequencies * mean_power) / total_power) if total_power else 0.0
    flatness_mask = (frequencies >= 20.0) & (frequencies <= 16000.0)
    flat_power = mean_power[flatness_mask]
    flatness_db = float(10.0 * np.log10(np.exp(np.mean(np.log(np.maximum(flat_power, 1e-30)))) / max(float(np.mean(flat_power)), 1e-30))) if len(flat_power) else None
    return {
        "duration_s": len(samples) / sample_rate,
        "rms_dbfs": float(20.0 * np.log10(max(rms, 1e-12))),
        "spectral_centroid_hz": centroid,
        "spectral_flatness_db": flatness_db,
        "f0_hz": median_or_none(valid_f0),
        "f0_confidence": median_or_none(confidence),
        "f0_coverage": len(valid_f0) / max(len(spectral_rows), 1),
        "third_octave_power_db_normalized": normalized_third_octave_db.tolist(),
    }


def register(f0: float | None) -> str:
    if f0 is None:
        return "unknown"
    if f0 < 80.0:
        return "low"
    if f0 < 140.0:
        return "mid"
    return "high"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value) if isinstance(value, (list, dict)) else value for key, value in row.items()})


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    validation_rows = json.loads(E013_VALIDATION.read_text(encoding="utf-8"))
    alignment = json.loads(E015_MAP.read_text(encoding="utf-8"))["slices"]
    aligned_by_name = {row["filename"]: row for row in alignment}
    slb_candidates = [row for row in validation_rows if row["slice_set_id"] == "slb200_vincents_take_1_cubase_slices"]
    slb_candidate_by_name = {Path(row["filename"]).name: row for row in slb_candidates}
    slb = read_wav(SLB_SOURCE)
    filtered = read_wav(FILTERED_SOURCE)
    if slb.sample_rate != filtered.sample_rate:
        raise ValueError("Dry and filtered source sample rates differ")

    per_slice: list[dict[str, Any]] = []
    accepted_mapped_rows = []
    for candidate in slb_candidates:
        filename = candidate["filename"]
        mapping = aligned_by_name.get(filename)
        if not mapping or mapping["status"] != "mapped":
            per_slice.append({"record_type": "slb_candidate", "candidate_id": candidate["candidate_id"], "slice_set_id": candidate["slice_set_id"], "filename": filename, "validator_status": candidate["event_validity"], "alignment_status": mapping["status"] if mapping else "missing_map"})
            continue
        start = int(mapping["start_sample"])
        duration_samples = int(round(candidate["duration_s"] * slb.sample_rate))
        end = min(len(slb.samples), start + duration_samples)
        filtered_end = min(len(filtered.samples), end)
        dry_metrics = summarize_audio(slb.samples[start:end], slb.sample_rate)
        wet_metrics = summarize_audio(filtered.samples[start:filtered_end], filtered.sample_rate)
        row = {
            "record_type": "slb_candidate",
            "candidate_id": candidate["candidate_id"],
            "slice_set_id": candidate["slice_set_id"],
            "filename": filename,
            "source_start_s": mapping["start_s"],
            "source_end_s": mapping["end_s"],
            "alignment_correlation": mapping["correlation"],
            "validator_status": candidate["event_validity"],
            "validator_reasons": candidate["reasons"],
            "dry": dry_metrics,
            "filtered": wet_metrics,
            "register": register(dry_metrics["f0_hz"]),
            "level_dbfs": dry_metrics["rms_dbfs"],
        }
        per_slice.append(row)
        if candidate["event_validity"] == "accept":
            accepted_mapped_rows.append(row)

    old_manifest = json.loads(E008_OLD_MANIFEST.read_text(encoding="utf-8"))
    old_by_id = {int(row["event"]): row for row in old_manifest}
    human_labels = load_csv(E008_LABELS)
    human_confirmed_rows: list[dict[str, Any]] = []
    for label in human_labels:
        if label["verdict"] != "Use":
            continue
        old_event = old_by_id[int(label["event"])]
        start = max(0, int(float(old_event["start_s"]) * slb.sample_rate))
        end = min(len(slb.samples), max(start + 1, int(float(old_event["end_s"]) * slb.sample_rate)))
        dry_metrics = summarize_audio(slb.samples[start:end], slb.sample_rate)
        wet_metrics = summarize_audio(filtered.samples[start:min(end, len(filtered.samples))], filtered.sample_rate)
        human_confirmed_rows.append({
            "record_type": "slb_listener_confirmed_use",
            "candidate_id": f"E008:event:{label['event']}",
            "slice_set_id": "slb200_vincents_take_1_listener_confirmed_E008_Use",
            "old_event_id": int(label["event"]),
            "source_start_s": float(old_event["start_s"]),
            "source_end_s": float(old_event["end_s"]),
            "human_verdict": "Use",
            "dry": dry_metrics,
            "filtered": wet_metrics,
            "register": register(dry_metrics["f0_hz"]),
            "level_dbfs": dry_metrics["rms_dbfs"],
        })

    acoustic_sets = {
        "acoustic_bass_a_take_2_cubase_slices": "training",
        "acoustic_bass_a_take_3_cubase_slices": "training",
        "acoustic_bass_b_take_1_cubase_slices": "held_out",
    }
    acoustic_rows: list[dict[str, Any]] = []
    for candidate in validation_rows:
        split = acoustic_sets.get(candidate["slice_set_id"])
        if split is None or candidate["event_validity"] != "accept":
            continue
        audio = read_wav(candidate["file"])
        metrics = summarize_audio(audio.samples, audio.sample_rate)
        acoustic_rows.append({
            "record_type": "acoustic_candidate",
            "candidate_id": candidate["candidate_id"],
            "slice_set_id": candidate["slice_set_id"],
            "split": split,
            "validator_status": candidate["event_validity"],
            "f0_reliability": candidate["f0_reliability"],
            "features": metrics,
            "register": register(metrics["f0_hz"]),
            "level_dbfs": metrics["rms_dbfs"],
        })

    level_edges = np.quantile([row["level_dbfs"] for row in acoustic_rows if row["split"] == "training"], [1 / 3, 2 / 3])
    def level_bin(value: float) -> str:
        return "low" if value < level_edges[0] else "high" if value >= level_edges[1] else "mid"
    for row in accepted_mapped_rows:
        row["level_bin"] = level_bin(row["level_dbfs"])
    for row in human_confirmed_rows:
        row["level_bin"] = level_bin(row["level_dbfs"])
    for row in acoustic_rows:
        row["level_bin"] = level_bin(row["level_dbfs"])

    def profile(rows: list[dict[str, Any]], profile_key: str, selected_register: str | None = None, selected_level: str | None = None) -> np.ndarray | None:
        chosen = [row for row in rows if (selected_register is None or row["register"] == selected_register) and (selected_level is None or row["level_bin"] == selected_level)]
        if not chosen:
            return None
        if profile_key in {"dry", "filtered"}:
            values = [row["dry"]["third_octave_power_db_normalized"] for row in chosen]
            if profile_key == "filtered":
                values = [row["filtered"]["third_octave_power_db_normalized"] for row in chosen]
        else:
            values = [row["features"]["third_octave_power_db_normalized"] for row in chosen]
        return np.mean(np.asarray(values, dtype=float), axis=0)

    comparisons = []
    training = [row for row in acoustic_rows if row["split"] == "training"]
    holdout = [row for row in acoustic_rows if row["split"] == "held_out"]
    conditions = [(None, None)] + [(reg, lev) for reg in ("low", "mid", "high") for lev in ("low", "mid", "high")]
    for reg, lev in conditions:
        slb_dry = profile(accepted_mapped_rows, "dry", reg, lev)
        slb_filtered = profile(accepted_mapped_rows, "filtered", reg, lev)
        acoustic_train = profile(training, "acoustic", reg, lev)
        acoustic_holdout = profile(holdout, "acoustic", reg, lev)
        if slb_dry is None or slb_filtered is None or acoustic_train is None or acoustic_holdout is None:
            continue
        comparisons.append({
            "register": reg or "all",
            "level_bin": lev or "all",
            "slb_n": sum(matches_condition(row, reg, lev) for row in accepted_mapped_rows),
            "acoustic_train_n": sum(matches_condition(row, reg, lev) for row in training),
            "acoustic_holdout_n": sum(matches_condition(row, reg, lev) for row in holdout),
            "dry_vs_acoustic_train_mae_db": float(np.mean(np.abs(slb_dry - acoustic_train))),
            "filtered_vs_acoustic_train_mae_db": float(np.mean(np.abs(slb_filtered - acoustic_train))),
            "dry_vs_acoustic_holdout_mae_db": float(np.mean(np.abs(slb_dry - acoustic_holdout))),
            "filtered_vs_acoustic_holdout_mae_db": float(np.mean(np.abs(slb_filtered - acoustic_holdout))),
        })

    human_comparisons = []
    for reg, lev in conditions:
        slb_dry = profile(human_confirmed_rows, "dry", reg, lev)
        slb_filtered = profile(human_confirmed_rows, "filtered", reg, lev)
        acoustic_train = profile(training, "acoustic", reg, lev)
        acoustic_holdout = profile(holdout, "acoustic", reg, lev)
        if slb_dry is None or slb_filtered is None or acoustic_train is None or acoustic_holdout is None:
            continue
        human_comparisons.append({
            "register": reg or "all",
            "level_bin": lev or "all",
            "slb_human_use_n": sum(matches_condition(row, reg, lev) for row in human_confirmed_rows),
            "acoustic_train_n": sum(matches_condition(row, reg, lev) for row in training),
            "acoustic_holdout_n": sum(matches_condition(row, reg, lev) for row in holdout),
            "dry_vs_acoustic_train_mae_db": float(np.mean(np.abs(slb_dry - acoustic_train))),
            "filtered_vs_acoustic_train_mae_db": float(np.mean(np.abs(slb_filtered - acoustic_train))),
            "dry_vs_acoustic_holdout_mae_db": float(np.mean(np.abs(slb_dry - acoustic_holdout))),
            "filtered_vs_acoustic_holdout_mae_db": float(np.mean(np.abs(slb_filtered - acoustic_holdout))),
            "status": "in_sample_diagnostic_filter_estimated_using_these_events",
        })

    for row in accepted_mapped_rows:
        slb_profile = row["dry"]["third_octave_power_db_normalized"]
        row["third_octave_mae_dry_vs_training"] = float(np.mean([np.mean(np.abs(np.asarray(slb_profile) - np.asarray(train["features"]["third_octave_power_db_normalized"]))) for train in training]))
        row["third_octave_mae_filtered_vs_training"] = float(np.mean([np.mean(np.abs(np.asarray(row["filtered"]["third_octave_power_db_normalized"]) - np.asarray(train["features"]["third_octave_power_db_normalized"]))) for train in training]))

    write_rows(RESULTS / "per_slice_features.csv", per_slice + human_confirmed_rows + acoustic_rows)
    write_rows(RESULTS / "accepted_mapped_slb_feedback.csv", accepted_mapped_rows)
    summary = {
        "source_slb_file": str(SLB_SOURCE),
        "filtered_slb_file": str(FILTERED_SOURCE),
        "cubase_source_time_mapped_count": len([row for row in per_slice if row.get("alignment_status") == "mapped" or row.get("source_start_s") is not None]),
        "slb_candidate_count": len(slb_candidates),
        "slb_validator_accept_count": sum(row["event_validity"] == "accept" for row in slb_candidates),
        "accepted_slb_candidates_mapped_count": len(accepted_mapped_rows),
        "listener_confirmed_slb_use_event_count": len(human_confirmed_rows),
        "acoustic_train_count": len(training),
        "acoustic_holdout_count": len(holdout),
        "level_tercile_edges_dbfs_from_acoustic_training": [float(level_edges[0]), float(level_edges[1])],
        "conditional_comparisons": comparisons,
        "listener_confirmed_slb_in_sample_diagnostic": human_comparisons,
        "per_slice_summary": {
            "median_centroid_shift_hz": median_or_none([row["filtered"]["spectral_centroid_hz"] - row["dry"]["spectral_centroid_hz"] for row in accepted_mapped_rows]),
            "median_level_shift_db": median_or_none([row["filtered"]["rms_dbfs"] - row["dry"]["rms_dbfs"] for row in accepted_mapped_rows]),
            "median_f0_shift_hz": median_or_none([row["filtered"]["f0_hz"] - row["dry"]["f0_hz"] for row in accepted_mapped_rows if row["filtered"]["f0_hz"] is not None and row["dry"]["f0_hz"] is not None]),
            "fraction_per_slice_closer_to_training_shape": float(np.mean([row["third_octave_mae_filtered_vs_training"] < row["third_octave_mae_dry_vs_training"] for row in accepted_mapped_rows])) if accepted_mapped_rows else None,
        },
        "limitations": [
            "Waveform alignment recovers timing only for unique high-correlation Cubase slices; unmatched/ambiguous slices are excluded from paired dry/filtered analysis.",
            "The E013 acoustic accept set is heuristic and uncalibrated; acoustic candidates have no human labels.",
            "Acoustic and SLB events are unpaired populations; the conditional comparisons are distribution-level diagnostics, not event matches.",
            "Register/level cells with empty or small counts are omitted; no inferential significance is claimed.",
            "The E014 filter is one shared candidate FIR; this report diagnoses residuals but does not retune the held-out set.",
        ],
    }
    (RESULTS / "per_slice_comparison.json").write_text(json.dumps(json_safe(summary), indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("mapped SLB candidates", summary["cubase_source_time_mapped_count"], "accepted mapped", len(accepted_mapped_rows))
    print("acoustic train/holdout", len(training), len(holdout))
    print("per-slice closer fraction", summary["per_slice_summary"]["fraction_per_slice_closer_to_training_shape"])
    print("listener-confirmed SLB comparison cells", len(human_comparisons), "(in-sample diagnostic)")
    for comparison in comparisons:
        print(comparison)


if __name__ == "__main__":
    main()
