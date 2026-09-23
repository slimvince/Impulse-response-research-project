from __future__ import annotations

import numpy as np

from .audio import frame_signal


FEATURE_VERSION = "0.1"


def _safe_db(value: np.ndarray | float, floor: float = 1e-12):
    return 20.0 * np.log10(np.maximum(value, floor))


def estimate_f0(frame: np.ndarray, sample_rate: int, low_hz: float = 30.0, high_hz: float = 250.0) -> float:
    centered = frame - np.mean(frame)
    if np.max(np.abs(centered)) < 1e-8:
        return float("nan")
    minimum = max(1, int(sample_rate / high_hz))
    maximum = min(len(centered) - 1, int(sample_rate / low_hz))
    if maximum <= minimum:
        return float("nan")
    correlation = np.correlate(centered, centered, mode="full")[len(centered) - 1:]
    correlation[:minimum] = 0.0
    lag = minimum + int(np.argmax(correlation[minimum:maximum + 1]))
    if correlation[lag] <= 0:
        return float("nan")
    return float(sample_rate / lag)


def analyze_frames(samples: np.ndarray, sample_rate: int, frame_size: int = 4096, hop_size: int = 1024) -> list[dict[str, float]]:
    frames = frame_signal(samples, frame_size, hop_size)
    window = np.hanning(frame_size)
    frequencies = np.fft.rfftfreq(frame_size, 1.0 / sample_rate)
    results: list[dict[str, float]] = []
    for index, frame in enumerate(frames):
        windowed = frame * window
        magnitude = np.abs(np.fft.rfft(windowed))
        power = magnitude ** 2
        total = float(np.sum(power))
        weighted = float(np.sum(frequencies * power))
        cumulative = np.cumsum(power)
        rolloff_index = int(np.searchsorted(cumulative, 0.85 * total)) if total else 0
        spectral_flux = 0.0
        if results:
            previous = results[-1]["_spectrum"]
            spectral_flux = float(np.sqrt(np.mean((magnitude - previous) ** 2)))
        f0 = estimate_f0(frame, sample_rate)
        row = {
            "frame": float(index),
            "time_s": float(index * hop_size / sample_rate),
            "rms_db": float(_safe_db(np.sqrt(np.mean(frame ** 2)))),
            "peak_db": float(_safe_db(np.max(np.abs(frame)))),
            "spectral_centroid_hz": weighted / total if total else 0.0,
            "spectral_rolloff_hz": float(frequencies[min(rolloff_index, len(frequencies) - 1)]),
            "spectral_flux": spectral_flux,
            "f0_hz": f0,
            "harmonicity_db": float(_safe_db(np.max(power[1:]) / total)) if total and len(power) > 1 else -120.0,
            "band_20_80_db": float(_safe_db(np.sum(power[(frequencies >= 20) & (frequencies < 80)]))),
            "band_80_200_db": float(_safe_db(np.sum(power[(frequencies >= 80) & (frequencies < 200)]))),
            "band_200_500_db": float(_safe_db(np.sum(power[(frequencies >= 200) & (frequencies < 500)]))),
            "band_500_2000_db": float(_safe_db(np.sum(power[(frequencies >= 500) & (frequencies < 2000)]))),
            "band_2000_8000_db": float(_safe_db(np.sum(power[(frequencies >= 2000) & (frequencies < 8000)]))),
            "_spectrum": magnitude,
        }
        results.append(row)
    for row in results:
        del row["_spectrum"]
    return results
