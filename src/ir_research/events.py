from __future__ import annotations

import numpy as np

from .audio import frame_signal
from .features import _estimate_f0_details, estimate_f0


def _f0_for_frame(frame: np.ndarray, sample_rate: int) -> float:
    if len(frame) == 0:
        return float("nan")
    if np.max(np.abs(frame)) < 1e-8:
        return float("nan")
    return float(estimate_f0(frame, sample_rate, low_hz=30.0, high_hz=400.0))


def _pitch_quality(samples: np.ndarray, sample_rate: int) -> tuple[float, float, float]:
    decimation = max(1, int(round(sample_rate / 11025.0)))
    analysis_samples = samples[::decimation]
    analysis_rate = sample_rate / decimation
    frame_size = 1024
    if len(analysis_samples) < frame_size:
        return 0.0, 0.0, float("nan")
    frames = frame_signal(analysis_samples, frame_size, frame_size // 4)
    estimates = [_estimate_f0_details(frame, int(analysis_rate), low_hz=30.0, high_hz=400.0) for frame in frames]
    confidences = np.asarray([item[1] for item in estimates], dtype=float)
    frequencies = np.asarray([item[0] for item in estimates], dtype=float)
    valid = np.isfinite(confidences)
    if not np.any(valid):
        return 0.0, 0.0, float("nan")
    tonal_fraction = float(np.mean(confidences[valid] >= 0.25))
    median_confidence = float(np.median(confidences[valid]))
    voiced = frequencies[np.isfinite(frequencies) & (confidences >= 0.25)]
    median_f0 = float(np.median(voiced)) if len(voiced) else float("nan")
    return tonal_fraction, median_confidence, median_f0


def _quality_label(duration_s: float, peak_db: float, tonal_fraction: float) -> tuple[str, str]:
    if duration_s <= 0.02:
        return "disqualified", "too short to represent a complete bass note"
    if duration_s <= 0.07 and peak_db <= -35.0 and tonal_fraction == 0.0:
        return "disqualified", "short low-level slice without periodic pitch evidence"
    if tonal_fraction < 0.25:
        return "pitch_unconfirmed", "insufficient periodic pitch evidence"
    return "tonal_candidate", "periodic pitch evidence present"


def _merge_edge_fragments(events: list[dict[str, float]], parent_duration_s: float) -> list[dict[str, float]]:
    merged: list[dict[str, float]] = []
    for event in sorted(events, key=lambda item: item["start_s"]):
        if not merged:
            merged.append(dict(event))
            continue
        previous = merged[-1]
        gap_s = max(0.0, event["start_s"] - previous["end_s"])
        previous_f0 = previous.get("median_f0_hz", float("nan"))
        event_f0 = event.get("median_f0_hz", float("nan"))
        edge_fragment = (
            event["duration_s"] <= 0.06
            and not np.isfinite(event_f0)
            and event["quality_status"] != "tonal_candidate"
            and parent_duration_s - event["end_s"] <= 0.02
            and gap_s <= 0.10
        )
        pitch_outlier = (
            gap_s <= 0.03
            and min(previous["duration_s"], event["duration_s"]) <= 0.15
            and np.isfinite(previous_f0)
            and np.isfinite(event_f0)
            and max(previous_f0, event_f0) > 300.0
            and min(previous_f0, event_f0) < 120.0
        )
        if not (edge_fragment or pitch_outlier):
            merged.append(dict(event))
            continue
        dominant = previous if previous["duration_s"] >= event["duration_s"] else event
        combined = dict(dominant)
        combined["start_s"] = min(previous["start_s"], event["start_s"])
        combined["end_s"] = max(previous["end_s"], event["end_s"])
        combined["duration_s"] = combined["end_s"] - combined["start_s"]
        peak_event = previous if previous["peak_db"] >= event["peak_db"] else event
        combined["peak_db"] = peak_event["peak_db"]
        combined["peak_s"] = peak_event["peak_s"]
        combined["attack_time_s"] = max(0.0, combined["peak_s"] - combined["start_s"])
        merged[-1] = combined
    return merged


def _onset_breaks(db: np.ndarray, frame_start: int, frame_stop: int, hop_size: int, sample_rate: int, minimum_rise_db: float = 3.0) -> list[int]:
    rise = np.maximum(0.0, np.diff(db[frame_start:frame_stop], prepend=db[frame_start]))
    minimum_spacing = max(1, int(0.16 * sample_rate / hop_size))
    selected: list[int] = []
    for index in range(1, len(rise) - 1):
        if rise[index] < minimum_rise_db or rise[index] < rise[index - 1] or rise[index] < rise[index + 1]:
            continue
        candidate = frame_start + index
        if selected and candidate - selected[-1] < minimum_spacing:
            continue
        selected.append(candidate)
    return selected


def _split_active_region(samples: np.ndarray, sample_rate: int, frame_size: int, hop_size: int, frame_start: int, frame_stop: int, db: np.ndarray) -> list[tuple[int, int]]:
    if frame_stop <= frame_start + 2:
        return [(frame_start, frame_stop)]

    f0_values: list[float] = []
    for frame_index in range(frame_start, frame_stop):
        sample_offset = frame_index * hop_size
        frame = samples[sample_offset:sample_offset + frame_size]
        if len(frame) < frame_size:
            frame = np.pad(frame, (0, frame_size - len(frame)))
        f0_values.append(_f0_for_frame(frame, sample_rate))

    valid = np.asarray([np.isfinite(value) for value in f0_values], dtype=bool)
    if np.count_nonzero(valid) < 3:
        return [(frame_start, frame_stop)]

    candidate_breaks: list[tuple[int, float]] = []
    for index in range(2, len(f0_values) - 2):
        if not valid[index]:
            continue
        if index <= int(0.2 * len(f0_values)) or index >= int(0.8 * len(f0_values)):
            continue
        left_window = np.asarray(f0_values[max(0, index - 3):index], dtype=float)
        right_window = np.asarray(f0_values[index + 1:min(len(f0_values), index + 4)], dtype=float)
        if np.count_nonzero(np.isfinite(left_window)) < 2 or np.count_nonzero(np.isfinite(right_window)) < 2:
            continue
        left_mean = float(np.nanmean(left_window[np.isfinite(left_window)]))
        right_mean = float(np.nanmean(right_window[np.isfinite(right_window)]))
        if not np.isfinite(left_mean) or not np.isfinite(right_mean):
            continue
        delta = abs(right_mean - left_mean)
        if delta < 12.0:
            continue
        relative_change = delta / max(max(abs(left_mean), abs(right_mean)), 1.0)
        if relative_change < 0.18:
            continue
        candidate_breaks.append((index, delta))

    if not candidate_breaks:
        return [(frame_start, frame_stop)]

    pitch_onsets = _onset_breaks(db, frame_start, frame_stop, hop_size, sample_rate, minimum_rise_db=2.0)
    onset_window = max(1, int(0.10 * sample_rate / hop_size))
    candidate_breaks = [
        (index, delta)
        for index, delta in candidate_breaks
        if any(abs(onset - (frame_start + index)) <= onset_window for onset in pitch_onsets)
    ]
    if not candidate_breaks:
        return [(frame_start, frame_stop)]

    onset_breaks = _onset_breaks(db, frame_start, frame_stop, hop_size, sample_rate)
    candidate_breaks.sort(key=lambda item: item[1], reverse=True)
    cluster_spacing = max(1, int(0.08 * sample_rate / hop_size))
    clusters: list[list[tuple[int, float]]] = []
    for item in sorted(candidate_breaks):
        if not clusters or item[0] - clusters[-1][-1][0] >= cluster_spacing:
            clusters.append([item])
        else:
            clusters[-1].append(item)

    selected_breaks: list[int] = []
    for cluster in clusters:
        selected_breaks.append(frame_start + max(cluster, key=lambda item: item[1])[0])

    if len(clusters) <= 2 and (frame_stop - frame_start) * hop_size / sample_rate >= 0.8:
        if len(clusters) == 1 and onset_breaks:
            onset_breaks = onset_breaks[:1]
        elif len(onset_breaks) < 4:
            onset_breaks = []
        if onset_breaks:
            for candidate in onset_breaks:
                if any(abs(candidate - existing) < cluster_spacing for existing in selected_breaks):
                    continue
                selected_breaks.append(candidate)

    if not selected_breaks:
        return [(frame_start, frame_stop)]

    segments: list[tuple[int, int]] = []
    cursor = frame_start
    for break_point in sorted(selected_breaks):
        if break_point <= cursor:
            continue
        segments.append((cursor, break_point))
        cursor = break_point
    segments.append((cursor, frame_stop))

    merged: list[tuple[int, int]] = []
    for start, stop in segments:
        if not merged:
            merged.append((start, stop))
            continue
        if stop - start <= 3:
            previous_start, _ = merged[-1]
            merged[-1] = (previous_start, stop)
            continue
        merged.append((start, stop))
    return merged


def detect_events(
    samples: np.ndarray,
    sample_rate: int,
    frame_size: int = 2048,
    hop_size: int = 512,
    threshold_db: float = -45.0,
    refine_long_events: bool = True,
    max_event_duration_s: float = 0.75,
    _refinement_depth: int = 0,
) -> list[dict[str, float]]:
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
        split_ranges = _split_active_region(padded, sample_rate, frame_size, hop_size, start, stop, db)
        for region_start, region_stop in split_ranges:
            if region_stop <= region_start:
                continue
            segment = db[region_start:region_stop]
            if len(segment) == 0:
                continue
            peak = int(np.argmax(segment)) + region_start
            start_s = float(region_start * hop_size / sample_rate)
            end_s = float(region_stop * hop_size / sample_rate)
            sample_start = max(0, int(start_s * sample_rate))
            sample_end = min(len(samples), max(sample_start + 1, int(end_s * sample_rate)))
            event_samples = samples[sample_start:sample_end]
            tonal_fraction, median_pitch_confidence, median_f0 = _pitch_quality(event_samples, sample_rate)
            peak_db = float(np.max(segment))
            duration_s = float((region_stop - region_start) * hop_size / sample_rate)
            quality_status, quality_reason = _quality_label(duration_s, peak_db, tonal_fraction)
            events.append({
                "start_s": start_s,
                "end_s": end_s,
                "duration_s": duration_s,
                "peak_s": float(peak * hop_size / sample_rate),
                "peak_db": peak_db,
                "attack_time_s": float((peak - region_start) * hop_size / sample_rate),
                "sustain_db": float(np.median(segment[max(0, len(segment) // 3):])),
                "decay_db_per_s": float((segment[-1] - segment[max(0, len(segment) // 2)]) / max((len(segment) / 2) * hop_size / sample_rate, 1e-6)),
                "tonal_frame_fraction": tonal_fraction,
                "median_pitch_confidence": median_pitch_confidence,
                "median_f0_hz": median_f0,
                "quality_status": quality_status,
                "quality_reason": quality_reason,
            })
    if not refine_long_events or _refinement_depth >= 2:
        return events

    refined: list[dict[str, float]] = []
    for event in events:
        if event["duration_s"] <= max_event_duration_s:
            refined.append(event)
            continue
        start_index = max(0, int(event["start_s"] * sample_rate))
        end_index = min(len(samples), max(start_index + 1, int(event["end_s"] * sample_rate)))
        children = detect_events(
            samples[start_index:end_index],
            sample_rate,
            frame_size=2048,
            hop_size=256,
            threshold_db=-35.0,
            refine_long_events=True,
            max_event_duration_s=max_event_duration_s,
            _refinement_depth=_refinement_depth + 1,
        )
        children = _merge_edge_fragments(children, event["duration_s"])
        children = [child for child in children if child["duration_s"] >= 0.02]
        if len(children) <= 1:
            refined.append(event)
            continue
        for child in children:
            shifted = dict(child)
            shifted["start_s"] += event["start_s"]
            shifted["end_s"] += event["start_s"]
            shifted["peak_s"] += event["start_s"]
            refined.append(shifted)
    return refined
