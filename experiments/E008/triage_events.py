from __future__ import annotations

import csv
import json
import math
import wave
from pathlib import Path

import numpy as np

from ir_research.audio import read_wav
from ir_research.features import analyze_frames

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(r"C:\IR audio\slb200\vincents 1.wav")
EVENTS = Path(r"C:\IR audio\results\slb200-candidate\events.json")
OUTPUT = Path(__file__).with_name("triage.csv")


def db(value: float) -> float:
    return 20.0 * math.log10(max(value, 1e-12))


def pitch_diagnostics(samples: np.ndarray, sample_rate: int) -> tuple[int, float, bool]:
    frames = analyze_frames(samples, sample_rate, frame_size=256, hop_size=64)
    f0 = np.asarray([row["f0_hz"] for row in frames], dtype=float)
    confidence = np.asarray([row["f0_confidence"] for row in frames], dtype=float)
    valid = np.isfinite(f0) & (confidence >= 0.25)
    steps: list[float] = []
    for index in range(3, len(f0) - 3):
        left = f0[index - 3:index][valid[index - 3:index]]
        right = f0[index + 1:index + 4][valid[index + 1:index + 4]]
        if len(left) < 2 or len(right) < 2:
            continue
        left_median = float(np.median(left))
        right_median = float(np.median(right))
        delta = abs(right_median - left_median)
        if delta >= max(12.0, 0.18 * max(left_median, right_median)):
            steps.append(delta)
    residual = np.asarray([row["harmonic_to_residual_db"] for row in frames], dtype=float)
    flatness = np.asarray([row["spectral_flatness_db"] for row in frames], dtype=float)
    residual = residual[np.isfinite(residual)]
    flatness = flatness[np.isfinite(flatness)]
    possible_polyphony = bool(
        (len(residual) and float(np.median(residual)) < -8.0)
        or (len(flatness) and float(np.median(flatness)) > -18.0)
    )
    return len(steps), max(steps, default=0.0), possible_polyphony


def main() -> None:
    audio = read_wav(SOURCE)
    events = json.loads(EVENTS.read_text(encoding="utf-8"))
    rows = []
    for index, event in enumerate(events, start=1):
        start = int(float(event["start_s"]) * audio.sample_rate)
        end = max(start + 1, int(float(event["end_s"]) * audio.sample_rate))
        samples = audio.samples[start:end]
        peak_db = db(float(np.max(np.abs(samples))))
        rms_db = db(float(np.sqrt(np.mean(samples**2))))
        duration = float(event["duration_s"])
        obvious_silence = duration <= 0.02 and peak_db <= -42.0 and rms_db <= -45.0
        pitch_step_count, max_pitch_step_hz, possible_polyphony = pitch_diagnostics(samples, audio.sample_rate)

        duration_score = max(0.0, 1.0 - abs(duration - 0.30) / 0.30)
        level_score = np.clip((peak_db + 35.0) / 25.0, 0.0, 1.0)
        rms_score = np.clip((rms_db + 45.0) / 25.0, 0.0, 1.0)
        attack_score = np.clip(1.0 - float(event["attack_time_s"]) / 0.20, 0.0, 1.0)
        candidate_score = 0.30 * duration_score + 0.25 * level_score + 0.25 * rms_score + 0.20 * attack_score
        candidate_score -= 0.15 * min(pitch_step_count, 1)
        candidate_score -= 0.20 * possible_polyphony
        if obvious_silence:
            auto_verdict = "Review"
            rationale = "possible threshold-level fragment"
            suggested_annotation = "Review flag: possible threshold-level fragment; audition required."
        else:
            auto_verdict = "Review"
            flags = []
            if pitch_step_count:
                flags.append("large pitch change")
            if possible_polyphony:
                flags.append("possible polyphony")
            rationale = "; ".join(flags) if flags else "candidate ranking only"
            if duration >= 0.5 and peak_db > -30.0 and not pitch_step_count:
                suggested_annotation = "Likely use candidate: duration and level match the calibrated labeled set; no large pitch step detected."
            elif duration >= 0.2 and peak_db > -30.0 and not pitch_step_count:
                suggested_annotation = "Review candidate: duration and level are favorable, but audition remains required."
            elif flags:
                suggested_annotation = f"Review flag: {rationale}."
            else:
                suggested_annotation = "Review candidate: no decisive automated exclusion."
        rows.append({
            "event": index,
            "start_s": event["start_s"],
            "end_s": event["end_s"],
            "duration_s": duration,
            "peak_db": peak_db,
            "rms_db": rms_db,
            "attack_time_s": event["attack_time_s"],
            "median_f0_hz": event.get("median_f0_hz"),
            "pitch_step_count": pitch_step_count,
            "max_pitch_step_hz": max_pitch_step_hz,
            "possible_polyphony": possible_polyphony,
            "auto_verdict": auto_verdict,
            "rationale": rationale,
            "suggested_annotation": suggested_annotation,
            "candidate_score": candidate_score,
        })

    rows.sort(key=lambda row: (row["auto_verdict"] != "Disq", -row["candidate_score"]))
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        OUTPUT.with_suffix(".json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(rows)} events")
    print(f"Automatic silence disqualifications: {sum(row['auto_verdict'] == 'Disq' for row in rows)}")
    print("Top review candidates:")
    for row in [row for row in rows if row["auto_verdict"] == "Review"][:20]:
        print(f"  event {row['event']}: score={row['candidate_score']:.3f}, duration={row['duration_s']:.3f}s, peak={row['peak_db']:.1f}dB")


if __name__ == "__main__":
    main()
