from __future__ import annotations

import numpy as np


def detect_events(samples: np.ndarray, sample_rate: int, frame_size: int = 2048, hop_size: int = 512, threshold_db: float = -45.0) -> list[dict[str, float]]:
    if len(samples) == 0:
        return []
    padded = np.pad(samples, (0, max(0, frame_size - len(samples))))
    starts = np.arange(0, max(1, len(padded) - frame_size + 1), hop_size)
    rms = np.array([np.sqrt(np.mean(padded[start:start + frame_size] ** 2)) for start in starts])
    db = 20.0 * np.log10(np.maximum(rms, 1e-12))
    active = db > threshold_db
    transitions = np.diff(np.r_[False, active, False].astype(int))
    begin = np.flatnonzero(transitions == 1)
    end = np.flatnonzero(transitions == -1)
    events: list[dict[str, float]] = []
    for start, stop in zip(begin, end):
        if stop <= start:
            continue
        segment = db[start:stop]
        peak = int(np.argmax(segment)) + start
        events.append({
            "start_s": float(start * hop_size / sample_rate),
            "end_s": float(stop * hop_size / sample_rate),
            "duration_s": float((stop - start) * hop_size / sample_rate),
            "peak_s": float(peak * hop_size / sample_rate),
            "peak_db": float(np.max(segment)),
            "attack_time_s": float((peak - start) * hop_size / sample_rate),
            "sustain_db": float(np.median(segment[max(0, len(segment) // 3):])),
            "decay_db_per_s": float((segment[-1] - segment[max(0, len(segment) // 2)]) / max((len(segment) / 2) * hop_size / sample_rate, 1e-6)),
        })
    return events
