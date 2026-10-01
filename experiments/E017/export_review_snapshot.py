from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"
SNAPSHOT = ROOT / "results" / "browser_review_snapshot_latest.json"
OUTPUT = ROOT / "results" / "human_labels_partial_latest.csv"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    items = {item["audit_id"]: item for item in manifest["labels"]}
    fields = (
        "audit_id",
        "slice_set_id",
        "candidate_id",
        "filename",
        "sampling_stratum",
        "validator_suggestion",
        "validator_reasons",
        "verdict",
        "reason_codes",
        "f0_reliability",
        "confidence",
        "annotation",
        "file",
        "sha256",
    )
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for judgment in snapshot["judgments"]:
            item = items[judgment["audit_id"]]
            writer.writerow({
                "audit_id": judgment["audit_id"],
                "slice_set_id": item["slice_set_id"],
                "candidate_id": item["candidate_id"],
                "filename": item["filename"],
                "sampling_stratum": item["sampling_stratum"],
                "validator_suggestion": item["validator_suggestion"],
                "validator_reasons": ";".join(item["validator_reasons"]),
                "verdict": judgment["verdict"],
                "reason_codes": ";".join(judgment["reasons"]),
                "f0_reliability": judgment["f0_reliability"],
                "confidence": judgment["confidence"],
                "annotation": judgment["note"],
                "file": item["file"],
                "sha256": item["sha256"],
            })
    print(f"Wrote {OUTPUT} with {len(snapshot['judgments'])} judgments")


if __name__ == "__main__":
    main()
