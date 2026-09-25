from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
INPUT = Path(__file__).with_name("event_features.csv")
OUTPUT = Path(__file__).with_name("conditional_comparison.json")


def value(row: dict[str, str], key: str) -> float | None:
    try:
        parsed = float(row[key])
        return parsed if np.isfinite(parsed) else None
    except (ValueError, KeyError):
        return None


def register(f0: float | None) -> str:
    if f0 is None:
        return "unknown"
    if f0 < 80:
        return "low"
    if f0 < 140:
        return "mid"
    return "high"


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    enriched = []
    levels = []
    for row in rows:
        f0_values = [value(row, f"{phase}_f0_hz") for phase in ("attack", "early_sustain", "sustain", "decay")]
        rms_values = [value(row, f"{phase}_rms_db") for phase in ("attack", "early_sustain", "sustain", "decay")]
        f0_values = [item for item in f0_values if item is not None]
        rms_values = [item for item in rms_values if item is not None]
        if not f0_values or not rms_values:
            continue
        event = dict(row)
        event["event_f0_hz"] = float(np.median(f0_values))
        event["event_rms_db"] = float(np.median(rms_values))
        levels.append(event["event_rms_db"])
        enriched.append(event)
    low_level, high_level = np.quantile(levels, [1 / 3, 2 / 3])
    for event in enriched:
        event["register"] = register(event["event_f0_hz"])
        event["level_bin"] = "low" if event["event_rms_db"] < low_level else "high" if event["event_rms_db"] >= high_level else "mid"
    feature_pairs = (("event_rms_db", "event level"), ("attack_spectral_centroid_hz", "attack centroid"), ("sustain_spectral_centroid_hz", "sustain centroid"), ("decay_spectral_centroid_hz", "decay centroid"), ("attack_harmonicity_db", "attack harmonicity"), ("decay_harmonicity_db", "decay harmonicity"), ("attack_spectral_flux", "attack flux"), ("decay_spectral_flux", "decay flux"))
    comparisons = []
    for register_name in ("low", "mid", "high"):
        for level_name in ("low", "mid", "high"):
            acoustic = [event for event in enriched if event["domain"] == "acoustic_mic" and event["register"] == register_name and event["level_bin"] == level_name]
            eub = [event for event in enriched if event["domain"] == "eub_direct" and event["register"] == register_name and event["level_bin"] == level_name]
            if not acoustic or not eub:
                continue
            item = {"register": register_name, "level_bin": level_name, "acoustic_n": len(acoustic), "eub_n": len(eub), "features": {}}
            for key, label in feature_pairs:
                acoustic_values = [float(event[key]) for event in acoustic if value(event, key) is not None]
                eub_values = [float(event[key]) for event in eub if value(event, key) is not None]
                if acoustic_values and eub_values:
                    item["features"][label] = {"acoustic_median": float(np.median(acoustic_values)), "eub_median": float(np.median(eub_values)), "acoustic_minus_eub": float(np.median(acoustic_values) - np.median(eub_values)), "acoustic_n": len(acoustic_values), "eub_n": len(eub_values)}
            comparisons.append(item)
    output = {"event_count": len(enriched), "level_tercile_edges_db": [float(low_level), float(high_level)], "comparisons": comparisons, "limitations": ["E003/E006 event boundaries and articulations are not fully audited for every row.", "Register and level bins are descriptive; they do not make the recordings paired.", "Comparisons are exploratory and do not establish causal instrument effects or IR targets."]}
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}; populated cells: {len(comparisons)}")


if __name__ == "__main__":
    main()
