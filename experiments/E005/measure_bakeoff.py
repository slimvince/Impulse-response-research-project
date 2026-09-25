from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCERPTS = ("low_02_low.wav", "bass_friendly_01_bass_friendly.wav", "broad_03_broad.wav", "low_01_low.wav")


def read_ground_truth() -> dict[str, list[dict[str, float]]]:
    values: dict[str, list[dict[str, float]]] = {}
    with (ROOT / "experiments" / "E003" / "ground_truth.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            values.setdefault(row["excerpt_id"], []).append({"start_s": float(row["start_s"]), "end_s": float(row["end_s"])})
    return values


def score(reference: list[dict[str, float]], starts: list[float]) -> dict[str, object]:
    matched = min(len(reference), len(starts))
    errors = [abs(starts[index] - reference[index]["start_s"]) for index in range(matched)]
    return {
        "reference_count": len(reference),
        "detected_count": len(starts),
        "count_error": abs(len(starts) - len(reference)),
        "mean_ordered_onset_error_s": sum(errors) / matched if matched else None,
        "max_ordered_onset_error_s": max(errors) if errors else None,
    }


def load_candidate_starts() -> dict[str, dict[str, list[float]]]:
    candidates: dict[str, dict[str, list[float]]] = {name: {} for name in ("recursive_detector", "librosa_onset", "aubio_tuned", "basic_pitch_default")}
    results = json.loads((ROOT / "experiments" / "E005" / "results.json").read_text(encoding="utf-8"))
    for excerpt, item in results["candidates"].items():
        candidates["recursive_detector"][excerpt] = [event["start_s"] for event in item["recursive_detector"]]
        candidates["librosa_onset"][excerpt] = item["librosa_onset"]
    aubio = json.loads((ROOT / "experiments" / "E005" / "aubio_tuned_results.json").read_text(encoding="utf-8"))
    for excerpt, item in aubio.items():
        candidates["aubio_tuned"][excerpt] = item["onsets_s"]
    basic = json.loads((ROOT / "experiments" / "E005" / "basic_pitch_results.json").read_text(encoding="utf-8"))
    for item in basic["results"]:
        default = next(setting for setting in item["parameter_sets"] if setting["id"] == "default")
        candidates["basic_pitch_default"][item["excerpt_id"]] = [event["start_s"] for event in default["events"]]
    return candidates


def audit_counts(path: Path) -> dict[str, object]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    counts = Counter(row["status"] for row in rows)
    return {"total": len(rows), "statuses": dict(counts), "usable_rate": counts["usable"] / len(rows) if rows else None}


def main() -> None:
    reference = read_ground_truth()
    candidates = load_candidate_starts()
    comparison = {
        candidate: {excerpt: score(reference[excerpt], starts) for excerpt, starts in excerpts.items()}
        for candidate, excerpts in candidates.items()
    }
    report = {
        "reference_labels": "E003/ground_truth.csv; approximate manual times",
        "candidates": comparison,
        "human_audits": {
            "e003_listener_audit": audit_counts(ROOT / "experiments" / "E003" / "listener_audit.csv"),
            "e004_hit_rate": audit_counts(ROOT / "experiments" / "E004" / "real_hit_rate_sample" / "hit_rate_audit.csv"),
            "e004_positive_control": audit_counts(ROOT / "experiments" / "E004" / "positive_control_sample" / "positive_control_audit.csv"),
        },
        "limitations": [
            "Ordered onset errors use approximate manual labels.",
            "Only the recursive detector has a complete listener usability audit on E003.",
            "Candidate count/onset metrics do not measure split/merge correctness without human labels for each candidate.",
            "Essentia, MuScriptor, MT3, and commercial systems are not included.",
        ],
    }
    path = Path(__file__).with_name("measurement_report.json")
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
