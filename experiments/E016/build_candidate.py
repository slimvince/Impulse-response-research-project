from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

from ir_research.audio import read_wav

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments.E014.build_and_render_candidate import (
    FIR_TAPS,
    GAIN_CAP_DB,
    SAMPLE_RATE,
    fft_convolve_channels,
    minimum_phase_fir,
    read_stereo_pcm16,
    write_pcm16,
)

OUTPUT = Path(__file__).resolve().parent
RESULTS = OUTPUT / "results"
LISTENING = OUTPUT / "listening"
E015_FEATURES = ROOT / "experiments" / "E015" / "results" / "per_slice_features.csv"
E014_FILTER = ROOT / "experiments" / "E014" / "results" / "candidate_minimum_phase_fir.npz"
E014_RENDER = Path(r"C:\IR audio\results\E014\vincents_1_candidate_acoustic_EQ_E014.wav")
SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
OUTPUT_ROOT = Path(r"C:\IR audio\results\E016")
TRAIN_SETS = {"acoustic_bass_a_take_2_cubase_slices", "acoustic_bass_a_take_3_cubase_slices"}
HOLDOUT_SET = "acoustic_bass_b_take_1_cubase_slices"
MIN_EVENT_DURATION_S = 0.12


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


def parsed_profile(row: dict[str, str], field: str) -> np.ndarray:
    value = json.loads(row[field])
    return np.asarray(value["third_octave_power_db_normalized"], dtype=float)


def smooth_gain(source_profile: np.ndarray, target_profile: np.ndarray, centers: np.ndarray) -> np.ndarray:
    gain = target_profile - source_profile
    reference = (centers >= 100.0) & (centers <= 1000.0)
    gain -= float(np.median(gain[reference])) if np.any(reference) else float(np.median(gain))
    gain = np.clip(gain, -GAIN_CAP_DB, GAIN_CAP_DB)
    kernel = np.asarray([1.0, 2.0, 3.0, 2.0, 1.0])
    kernel /= kernel.sum()
    return np.convolve(np.pad(gain, (2, 2), mode="edge"), kernel, mode="valid")


def profile_mae(first: np.ndarray, second: np.ndarray, centers: np.ndarray) -> float:
    band = (centers >= 40.0) & (centers <= 8000.0)
    return float(np.mean(np.abs(first[band] - second[band])))


def rms(samples: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.asarray(samples, dtype=np.float64) ** 2)))


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    LISTENING.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(E015_FEATURES.open(newline="", encoding="utf-8")))
    slb_rows = [row for row in rows if row["record_type"] == "slb_listener_confirmed_use"]
    acoustic_train_rows = [
        row for row in rows
        if row["record_type"] == "acoustic_candidate"
        and row["slice_set_id"] in TRAIN_SETS
        and float(json.loads(row["features"])["duration_s"]) >= MIN_EVENT_DURATION_S
    ]
    acoustic_holdout_rows = [
        row for row in rows
        if row["record_type"] == "acoustic_candidate"
        and row["slice_set_id"] == HOLDOUT_SET
        and float(json.loads(row["features"])["duration_s"]) >= MIN_EVENT_DURATION_S
    ]
    if len(slb_rows) < 10 or not acoustic_train_rows or not acoustic_holdout_rows:
        raise RuntimeError("Insufficient SLB or acoustic profiles for E016")

    slb_profiles = np.stack([parsed_profile(row, "dry") for row in slb_rows])
    train_profiles = np.stack([parsed_profile(row, "features") for row in acoustic_train_rows])
    holdout_profiles = np.stack([parsed_profile(row, "features") for row in acoustic_holdout_rows])
    centers = np.asarray([31.5 * 2 ** (index / 3.0) for index in range(slb_profiles.shape[1])], dtype=float)
    source_median = np.median(slb_profiles, axis=0)
    train_median = np.median(train_profiles, axis=0)
    holdout_median = np.median(holdout_profiles, axis=0)
    gain_db = smooth_gain(source_median, train_median, centers)

    old_filter = np.load(E014_FILTER)["smoothed_gain_db"].astype(float)
    if len(old_filter) != len(gain_db):
        raise ValueError("E014 and E016 gain grids differ")
    dry_train_mae = profile_mae(source_median, train_median, centers)
    dry_holdout_mae = profile_mae(source_median, holdout_median, centers)
    e014_train_mae = profile_mae(source_median + old_filter, train_median, centers)
    e014_holdout_mae = profile_mae(source_median + old_filter, holdout_median, centers)
    e016_train_mae = profile_mae(source_median + gain_db, train_median, centers)
    e016_holdout_mae = profile_mae(source_median + gain_db, holdout_median, centers)

    old_maes = np.mean(np.abs(slb_profiles[:, None, :] - train_profiles[None, :, :])[:, :, (centers >= 40) & (centers <= 8000)], axis=2)
    new_maes = np.mean(np.abs((slb_profiles + gain_db)[:, None, :] - train_profiles[None, :, :])[:, :, (centers >= 40) & (centers <= 8000)], axis=2)
    old_per_event = np.median(old_maes, axis=1)
    new_per_event = np.median(new_maes, axis=1)

    fir, _, _ = minimum_phase_fir(centers, gain_db)
    np.savez_compressed(
        RESULTS / "candidate_per_event_median_fir.npz",
        fir=fir.astype(np.float32),
        sample_rate=np.asarray([SAMPLE_RATE], dtype=np.int32),
        third_octave_centers_hz=centers.astype(np.float32),
        gain_db=gain_db.astype(np.float32),
    )

    source_stereo, sample_rate, _ = read_stereo_pcm16(SOURCE)
    dry_render_meta = {"safety_gain_db": 0.0, "frames": len(source_stereo), "duration_s": len(source_stereo) / sample_rate}
    e014_stereo, e014_rate, _ = read_stereo_pcm16(E014_RENDER)
    if e014_rate != sample_rate:
        raise ValueError("E014 render and source sample rates differ")
    e016_stereo = fft_convolve_channels(source_stereo, fir)
    e014_matched = e014_stereo * (rms(source_stereo) / max(rms(e014_stereo), 1e-12))
    e016_matched = e016_stereo * (rms(source_stereo) / max(rms(e016_stereo), 1e-12))

    output_files = {
        "e014_loudness_matched": OUTPUT_ROOT / "vincents_1_E014_loudness_matched.wav",
        "e016_raw": OUTPUT_ROOT / "vincents_1_E016_per_event_median_raw.wav",
        "e016_loudness_matched": OUTPUT_ROOT / "vincents_1_E016_per_event_median_loudness_matched.wav",
    }
    render_stats = {
        "e014_loudness_matched": write_pcm16(output_files["e014_loudness_matched"], e014_matched, sample_rate),
        "e016_raw": write_pcm16(output_files["e016_raw"], e016_stereo, sample_rate),
        "e016_loudness_matched": write_pcm16(output_files["e016_loudness_matched"], e016_matched, sample_rate),
    }
    for key, path in output_files.items():
        audition_path = LISTENING / path.name
        audition_path.write_bytes(path.read_bytes())

    profile_report = {
        "source_event_count": len(slb_rows),
        "acoustic_train_event_count": len(acoustic_train_rows),
        "acoustic_train_set_counts": {name: sum(row["slice_set_id"] == name for row in acoustic_train_rows) for name in sorted(TRAIN_SETS)},
        "acoustic_holdout_event_count": len(acoustic_holdout_rows),
        "heldout_set": HOLDOUT_SET,
        "objective": "median per-event unit-power third-octave log-spectrum; filter fit is median acoustic-minus-SLB profile, centered over 100-1000 Hz, smoothed and gain-capped",
        "metrics_mae_db": {
            "dry_to_train_median_profile": dry_train_mae,
            "dry_to_holdout_median_profile": dry_holdout_mae,
            "E014_to_train_median_profile": e014_train_mae,
            "E014_to_holdout_median_profile": e014_holdout_mae,
            "E016_to_train_median_profile": e016_train_mae,
            "E016_to_holdout_median_profile": e016_holdout_mae,
        },
        "per_confirmed_slb_event_median_distance_to_train_population_mae_db": {
            "E014_median": float(np.median(old_per_event)),
            "E016_median": float(np.median(new_per_event)),
            "E016_closer_event_fraction": float(np.mean(new_per_event < old_per_event)),
        },
        "gain_db_by_third_octave": [{"center_hz": float(center), "gain_db": float(gain)} for center, gain in zip(centers, gain_db)],
        "render_source_duration_s": dry_render_meta["duration_s"],
        "render_duration_s": render_stats["e016_raw"]["duration_s"],
        "render_stats": render_stats,
        "limitations": [
            "The 24 source events are listener-confirmed, but they are the same SLB events used to fit E014/E016; their per-event comparison is in-sample.",
            "The acoustic training and holdout slices are E013 heuristic accepts, not manually validated events.",
            "The B3 acoustic slice set was examined in earlier experiments; treat its result as a diagnostic, not a fresh untouched test.",
            "Median event log-spectrum objective differs from E014's pooled linear-power objective, so metrics are reported for this explicit objective and should not be directly interchanged with E014's score.",
            "This remains a shared spectral-shape FIR candidate, not a physical room/microphone impulse response or perceptually validated emulator."
        ],
    }
    (RESULTS / "candidate_profile.json").write_text(json.dumps(json_safe(profile_report), indent=2, allow_nan=False) + "\n", encoding="utf-8")
    metadata = {
        "source_path": str(SOURCE),
        "source_sha256": read_wav(SOURCE).sha256,
        "filter_path": str(RESULTS / "candidate_per_event_median_fir.npz"),
        "outputs": {key: str(path) for key, path in output_files.items()},
        "render_stats": render_stats,
        "loudness_match": "E014 and E016 audition variants scaled to dry whole-file RMS; raw E016 also provided.",
    }
    (RESULTS / "render_metadata.json").write_text(json.dumps(json_safe(metadata), indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("source/train/holdout events", len(slb_rows), len(acoustic_train_rows), len(acoustic_holdout_rows))
    print("MAE", json.dumps(json_safe(profile_report["metrics_mae_db"])))
    print("per-event E014/E016 median", float(np.median(old_per_event)), float(np.median(new_per_event)), "E016 closer fraction", float(np.mean(new_per_event < old_per_event)))
    print("renders", json.dumps(json_safe(render_stats)))


if __name__ == "__main__":
    main()
