from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
E005 = ROOT / "experiments" / "E005"
MATCH_TOLERANCE_S = 0.08
LONG_EVENT_S = 0.75


def nearby(time_s: float, candidates: list[float]) -> bool:
    return any(abs(time_s - candidate) <= MATCH_TOLERANCE_S for candidate in candidates)


def main() -> None:
    baseline = json.loads((E005 / "results.json").read_text(encoding="utf-8"))
    aubio = json.loads((E005 / "aubio_tuned_results.json").read_text(encoding="utf-8"))
    basic_pitch = json.loads((E005 / "basic_pitch_results.json").read_text(encoding="utf-8"))
    basic_pitch_by_excerpt = {
        item["excerpt_id"]: next(setting for setting in item["parameter_sets"] if setting["id"] == "default")["events"]
        for item in basic_pitch["results"]
    }
    routed: dict[str, object] = {}
    for excerpt, candidates in baseline["candidates"].items():
        primary = candidates["recursive_detector"]
        aubio_onsets = aubio[excerpt]["onsets_s"]
        basic_pitch_onsets = [event["start_s"] for event in basic_pitch_by_excerpt[excerpt]]
        events = []
        for index, event in enumerate(primary, 1):
            primary_start = event["start_s"]
            aubio_support = nearby(primary_start, aubio_onsets)
            basic_pitch_support = nearby(primary_start, basic_pitch_onsets)
            long_event = event["duration_s"] > LONG_EVENT_S
            if long_event:
                route = "secondary_review"
            elif aubio_support or basic_pitch_support:
                route = "candidate"
            else:
                route = "ambiguous"
            events.append({
                "event_index": index,
                "start_s": primary_start,
                "end_s": event["end_s"],
                "duration_s": event["duration_s"],
                "route": route,
                "aubio_onset_support": aubio_support,
                "basic_pitch_support": basic_pitch_support,
                "long_event": long_event,
            })
        routed[excerpt] = {
            "primary_detector": "recursive_detector",
            "secondary_detector": "aubio_specdiff_threshold_0.7",
            "candidate_context": "basic_pitch_default",
            "events": events,
        }
    output = {
        "strategy": "recursive primary + aubio secondary evidence + Basic Pitch candidate context",
        "match_tolerance_s": MATCH_TOLERANCE_S,
        "long_event_threshold_s": LONG_EVENT_S,
        "limitations": [
            "Routing is a prototype; it does not fuse or auto-accept events as scientifically usable.",
            "Human audits remain required for ambiguous and secondary-review routes.",
            "Basic Pitch and aubio outputs are candidate evidence, not ground truth.",
        ],
        "excerpts": routed,
    }
    output_path = E005 / "strategy_results.json"
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    for excerpt, result in routed.items():
        counts: dict[str, int] = {}
        for event in result["events"]:
            counts[event["route"]] = counts.get(event["route"], 0) + 1
        print(excerpt, counts)


if __name__ == "__main__":
    main()
