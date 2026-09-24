from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from ir_research.audio import read_wav
from ir_research.events import detect_events


SETTINGS = (
    (256, 64, -35.0),
    (256, 32, -35.0),
    (128, 32, -38.0),
    (128, 16, -38.0),
    (256, 64, -45.0),
)


def read_labels(path: Path) -> dict[str, list[dict[str, float]]]:
    labels: dict[str, list[dict[str, float]]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            labels.setdefault(row["excerpt_id"], []).append(
                {"start_s": float(row["start_s"]), "end_s": float(row["end_s"])}
            )
    return labels


def _overlap_seconds(first: dict[str, float], second: dict[str, float]) -> float:
    return max(0.0, min(first["end_s"], second["end_s"]) - max(first["start_s"], second["start_s"]))


def _classify_events(reference: list[dict[str, float]], detected: list[dict[str, float]]) -> list[dict[str, object]]:
    classifications: list[dict[str, object]] = []
    for event_index, event in enumerate(detected):
        if event_index >= len(reference):
            status = "disqualified"
            reason = "extra_event"
            reference_index = None
            onset_error = None
            offset_error = None
        else:
            reference_index = event_index
            reference_event = reference[reference_index]
            onset_error = abs(event["start_s"] - reference_event["start_s"])
            offset_error = abs(event["end_s"] - reference_event["end_s"])
            if onset_error <= 0.04:
                status = "usable"
                reason = "onset_within_tolerance"
            else:
                status = "ambiguous"
                reason = "onset_requires_audition"
        classifications.append(
            {
                "event_index": event_index + 1,
                "status": status,
                "reason": reason,
                "reference_index": reference_index + 1 if reference_index is not None else None,
                "onset_error_s": onset_error,
                "offset_error_s": offset_error,
            }
        )
    return classifications


def score_events(reference: list[dict[str, float]], detected: list[dict[str, float]]) -> dict[str, object]:
    matched = min(len(reference), len(detected))
    onset_errors = [
        abs(detected[index]["start_s"] - reference[index]["start_s"])
        for index in range(matched)
    ]
    offset_errors = [
        abs(detected[index]["end_s"] - reference[index]["end_s"])
        for index in range(matched)
    ]
    classifications = _classify_events(reference, detected)
    return {
        "reference_count": len(reference),
        "detected_count": len(detected),
        "missed_count": max(0, len(reference) - len(detected)),
        "extra_count": max(0, len(detected) - len(reference)),
        "matched_count": matched,
        "mean_onset_error_s": sum(onset_errors) / matched if matched else None,
        "mean_offset_error_s": sum(offset_errors) / matched if matched else None,
        "usable_count": sum(item["status"] == "usable" for item in classifications),
        "ambiguous_count": sum(item["status"] == "ambiguous" for item in classifications),
        "disqualified_count": sum(item["status"] == "disqualified" for item in classifications),
        "classifications": classifications,
    }


def evaluate(root: Path) -> dict[str, object]:
    labels = read_labels(root / "experiments" / "E003" / "ground_truth.csv")
    results: list[dict[str, object]] = []
    for frame_size, hop_size, threshold_db in SETTINGS:
        setting_results: list[dict[str, object]] = []
        for excerpt_id, reference in labels.items():
            audio = read_wav(root / "experiments" / "E002" / "listener_slices" / excerpt_id)
            detected = detect_events(
                audio.samples,
                audio.sample_rate,
                frame_size=frame_size,
                hop_size=hop_size,
                threshold_db=threshold_db,
            )
            setting_results.append(
                {
                    "excerpt_id": excerpt_id,
                    "events": detected,
                    "score": score_events(reference, detected),
                }
            )
        results.append(
            {
                "frame_size": frame_size,
                "hop_size": hop_size,
                "threshold_db": threshold_db,
                "excerpts": setting_results,
            }
        )
    return {
        "reference": "ground_truth.csv",
        "classification_note": "Usability classifications are provisional because the reviewed boundaries are approximate audition labels.",
        "settings": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate event detection against E003 labels.")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("benchmark_results.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = evaluate(root)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
