from __future__ import annotations

import hashlib
import json
import random
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SOURCE_RESULTS = ROOT / "experiments" / "E013" / "results" / "candidate_validation.json"
OUTPUT = Path(__file__).resolve().parent
SLICE_DIR = OUTPUT / "audit_slices"
SEED = 20261001
PER_SET = 10
AUDIO02_SOURCE = Path(r"C:\IR audio\slb200\recording two slices\yamaha bass slb200.wav")


def pick(pool: list[dict[str, Any]], count: int, chosen: set[str], rng: random.Random) -> list[dict[str, Any]]:
    available = [row for row in pool if row["candidate_id"] not in chosen]
    rng.shuffle(available)
    selected = available[:count]
    chosen.update(row["candidate_id"] for row in selected)
    return selected


def main() -> None:
    rows = json.loads(SOURCE_RESULTS.read_text(encoding="utf-8"))
    SLICE_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    selected_rows: list[dict[str, Any]] = []
    per_set_summary = {}
    for slice_set in sorted({row["slice_set_id"] for row in rows}):
        group = [row for row in rows if row["slice_set_id"] == slice_set]
        chosen: set[str] = set()
        selection: list[tuple[str, dict[str, Any]]] = []

        def add(stratum: str, pool: list[dict[str, Any]], count: int) -> None:
            selected = pick(pool, count, chosen, rng)
            selection.extend((stratum, row) for row in selected)

        add("provisional_accept", [row for row in group if row["event_validity"] == "accept"], 2)
        add("possible_internal_attack", [row for row in group if "possible_multiple_excitation_or_internal_transient" in row["reasons"]], 2)
        add("possible_tail_boundary", [row for row in group if "possible_truncated_sustain_or_decay" in row["reasons"]], 2)
        add("short_or_low_or_edge", [row for row in group if any(reason in row["reasons"] for reason in ("very_short_candidate", "low_signal_level", "possible_leading_bleed_or_missing_attack", "possible_clipping"))], 1)
        reject_pool = [row for row in group if row["event_validity"] == "reject"]
        add("hard_reject_qc" if reject_pool else "uncertain_fallback_no_hard_rejects", reject_pool if reject_pool else [row for row in group if row["event_validity"] == "uncertain"], 1)
        add("uncertain_random", [row for row in group if row["event_validity"] == "uncertain"], PER_SET - len(selection))

        if len(selection) < PER_SET:
            add("fallback_random", group, PER_SET - len(selection))
        if len(selection) != PER_SET:
            raise RuntimeError(f"Could not select {PER_SET} unique rows for {slice_set}; selected {len(selection)}")

        for index, (stratum, row) in enumerate(selection, start=1):
            source = Path(row["file"])
            if not source.is_file():
                raise FileNotFoundError(source)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if digest != row["observed_sha256"]:
                raise RuntimeError(f"Candidate changed since E013: {source}")
            safe_set = slice_set.replace("_cubase_slices", "")
            filename = f"{safe_set}_{index:02d}_{source.name}"
            destination = SLICE_DIR / filename
            shutil.copyfile(source, destination)
            copied_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
            if copied_hash != digest:
                raise RuntimeError(f"Copy hash mismatch for {destination}")
            source_recording = row.get("source_recording")
            source_available = bool(row.get("source_available"))
            source_relation = "E013 manifest source field"
            if slice_set == "slb200_audio02_cubase_slices" and AUDIO02_SOURCE.is_file():
                source_recording = str(AUDIO02_SOURCE)
                source_available = True
                source_relation = "user-identified recording two; duration-consistent, waveform alignment unverified"
            selected_rows.append({
                "audit_id": f"{slice_set}:{index:02d}",
                "slice_set_id": slice_set,
                "source_recording": source_recording,
                "candidate_id": row["candidate_id"],
                "filename": filename,
                "file": f"audit_slices/{filename}",
                "original_path": str(source),
                "source_available": source_available,
                "source_relation": source_relation,
                "sha256": digest,
                "duration_s": row["duration_s"],
                "peak_dbfs": row.get("peak_dbfs"),
                "rms_dbfs": row.get("rms_dbfs"),
                "f0_reliability": row.get("f0_reliability"),
                "median_f0_hz": row.get("median_f0_hz"),
                "validator_suggestion": row["event_validity"],
                "validator_reasons": row["reasons"],
                "sampling_stratum": stratum,
            })
        per_set_summary[slice_set] = {
            "candidate_count": len(group),
            "sampled_count": len(selection),
            "sampled_strata": dict(Counter(stratum for stratum, _ in selection)),
        }

    manifest = {
        "experiment_id": "E017",
        "selection_seed": SEED,
        "source_results": str(SOURCE_RESULTS),
        "per_set_summary": per_set_summary,
        "audit_policy": "10 stratified candidate slices per set; exact copies of E013 candidates; Cubase output is not ground truth.",
        "labels": selected_rows,
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Prepared {len(selected_rows)} audit candidates in {SLICE_DIR}")
    for name, summary in per_set_summary.items():
        print(name, summary["sampled_strata"])


if __name__ == "__main__":
    main()
