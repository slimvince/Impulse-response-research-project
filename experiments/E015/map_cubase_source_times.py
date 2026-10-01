from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.signal import correlate, find_peaks

from ir_research.audio import read_wav

CUBASE_MANIFEST = Path(r"C:\IR audio\slb200-cubase-slices-manifest.json")
SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
OUTPUT = Path(__file__).resolve().parent
RESULTS = OUTPUT / "results"
DECIMATION = 8
MINIMUM_CORRELATION = 0.75
MINIMUM_PEAK_MARGIN = 0.025
REMOTE_PEAK_SEPARATION_S = 0.75


def normalized_match(source: np.ndarray, template: np.ndarray, sample_rate: int) -> dict[str, Any]:
    template = np.asarray(template, dtype=np.float64)
    if len(template) < 128 or float(np.sqrt(np.mean(template**2))) < 1e-7:
        return {"status": "unmatchable_silence_or_short", "correlation": None, "runner_up": None, "peak_margin": None, "start_sample": None}

    source_coarse = np.asarray(source[::DECIMATION], dtype=np.float64)
    template_coarse = np.asarray(template[::DECIMATION], dtype=np.float64)
    template_coarse = template_coarse - np.mean(template_coarse)
    template_energy = float(np.sum(template_coarse**2))
    if template_energy < 1e-16:
        return {"status": "unmatchable_low_energy", "correlation": None, "runner_up": None, "peak_margin": None, "start_sample": None}

    correlation = correlate(source_coarse, template_coarse, mode="valid", method="fft")
    template_length = len(template_coarse)
    cumulative = np.concatenate(([0.0], np.cumsum(source_coarse)))
    cumulative_sq = np.concatenate(([0.0], np.cumsum(source_coarse**2)))
    sums = cumulative[template_length:] - cumulative[:-template_length]
    sums_sq = cumulative_sq[template_length:] - cumulative_sq[:-template_length]
    centered_energy = np.maximum(sums_sq - (sums**2 / template_length), 1e-20)
    scores = correlation / np.sqrt(centered_energy * template_energy)
    np.clip(scores, -1.0, 1.0, out=scores)

    best_index = int(np.argmax(scores))
    best_score = float(scores[best_index])
    separation = max(1, int(round(REMOTE_PEAK_SEPARATION_S * sample_rate / DECIMATION)))
    remote_mask = np.ones(len(scores), dtype=bool)
    remote_mask[max(0, best_index - separation):min(len(scores), best_index + separation + 1)] = False
    runner_score = float(np.max(scores[remote_mask])) if np.any(remote_mask) else -1.0
    margin = best_score - runner_score

    coarse_start = best_index * DECIMATION
    radius = 2 * DECIMATION
    local_start = max(0, coarse_start - radius)
    local_end = min(len(source), coarse_start + len(template) + radius)
    local = np.asarray(source[local_start:local_end], dtype=np.float64)
    local_template = template - np.mean(template)
    local_corr = correlate(local, local_template, mode="valid", method="fft")
    local_n = len(template)
    local_cum = np.concatenate(([0.0], np.cumsum(local)))
    local_cum_sq = np.concatenate(([0.0], np.cumsum(local**2)))
    local_sum = local_cum[local_n:] - local_cum[:-local_n]
    local_sum_sq = local_cum_sq[local_n:] - local_cum_sq[:-local_n]
    local_energy = np.maximum(local_sum_sq - (local_sum**2 / local_n), 1e-20)
    local_scores = local_corr / np.sqrt(local_energy * np.sum(local_template**2))
    refined_offset = int(np.argmax(local_scores))
    refined_start = local_start + refined_offset
    refined_score = float(local_scores[refined_offset])
    refined_status = "mapped" if refined_score >= MINIMUM_CORRELATION and margin >= MINIMUM_PEAK_MARGIN else "ambiguous_match"
    return {
        "status": refined_status,
        "start_sample": refined_start if refined_status == "mapped" else None,
        "start_s": refined_start / sample_rate if refined_status == "mapped" else None,
        "correlation": refined_score,
        "coarse_correlation": best_score,
        "remote_runner_up_correlation": runner_score,
        "peak_margin": margin,
        "source_candidates_checked": int(len(scores)),
        "alignment_decimation": DECIMATION,
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    external_manifest = json.loads(CUBASE_MANIFEST.read_text(encoding="utf-8"))
    slb_set = next(item for item in external_manifest["sets"] if item["slice_set_id"] == "slb200_vincents_take_1_cubase_slices")
    source = read_wav(SOURCE)
    rows: list[dict[str, Any]] = []
    for item in slb_set["files"]:
        path = Path(slb_set["directory"]) / item["file"]
        audio = read_wav(path)
        hash_matches = audio.sha256.lower() == item["sha256"].lower()
        alignment = normalized_match(source.samples, audio.samples, audio.sample_rate) if hash_matches else {
            "status": "slice_hash_mismatch", "start_sample": None, "start_s": None,
            "correlation": None, "coarse_correlation": None,
            "remote_runner_up_correlation": None, "peak_margin": None,
        }
        duration_s = len(audio.samples) / audio.sample_rate
        mapped_start = alignment.get("start_s")
        row = {
            "slice_set_id": slb_set["slice_set_id"],
            "filename": item["file"],
            "slice_path": str(path),
            "slice_sha256": audio.sha256,
            "pinned_hash_matches": hash_matches,
            "duration_s": duration_s,
            **alignment,
            "end_s": mapped_start + duration_s if mapped_start is not None else None,
        }
        rows.append(row)

    summary = {
        "source": str(SOURCE),
        "source_sha256": source.sha256,
        "candidate_manifest": str(CUBASE_MANIFEST),
        "candidate_manifest_sha256": hashlib.sha256(CUBASE_MANIFEST.read_bytes()).hexdigest(),
        "slice_count": len(rows),
        "alignment_status": {key: sum(row["status"] == key for row in rows) for key in sorted({row["status"] for row in rows})},
        "median_correlation_of_mapped": float(np.median([row["correlation"] for row in rows if row["status"] == "mapped"])) if any(row["status"] == "mapped" for row in rows) else None,
        "thresholds": {"minimum_correlation": MINIMUM_CORRELATION, "minimum_peak_margin": MINIMUM_PEAK_MARGIN, "remote_peak_separation_s": REMOTE_PEAK_SEPARATION_S},
        "note": "Source-time mapping is accepted only for strong, unique waveform matches. Silence/ambiguous candidates remain unmapped.",
    }
    (RESULTS / "source_time_map.json").write_text(json.dumps({"summary": summary, "slices": rows}, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (RESULTS / "source_time_map.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("alignment_status", summary["alignment_status"])
    print("median_mapped_correlation", summary["median_correlation_of_mapped"])


if __name__ == "__main__":
    main()
