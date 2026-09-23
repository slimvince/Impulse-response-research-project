from __future__ import annotations

import numpy as np

from .audio import frame_signal


FEATURE_VERSION = "0.2"


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


def _spectral_shape(frequencies: np.ndarray, power: np.ndarray, total: float, centroid: float) -> dict[str, float]:
    if total <= 0.0:
        return {"spectral_spread_hz": 0.0, "spectral_skewness": 0.0, "spectral_kurtosis": 0.0, "spectral_slope_db_per_hz": 0.0, "spectral_flatness_db": -120.0}
    centered = frequencies - centroid
    spread = float(np.sqrt(np.sum(power * centered ** 2) / total))
    if spread > 1e-12:
        skewness = float(np.sum(power * centered ** 3) / total / spread ** 3)
        kurtosis = float(np.sum(power * centered ** 4) / total / spread ** 4)
    else:
        skewness = 0.0
        kurtosis = 0.0
    valid = (frequencies > 0.0) & (power > 1e-12)
    slope = float(np.polyfit(frequencies[valid], _safe_db(power[valid]), 1)[0]) if np.count_nonzero(valid) >= 2 else 0.0
    flatness = float(_safe_db(np.exp(np.mean(np.log(np.maximum(power[valid], 1e-12)))) / np.mean(power[valid]))) if np.any(valid) else -120.0
    return {"spectral_spread_hz": spread, "spectral_skewness": skewness, "spectral_kurtosis": kurtosis, "spectral_slope_db_per_hz": slope, "spectral_flatness_db": flatness}


def _band_power(power: np.ndarray, frequencies: np.ndarray, low_hz: float, high_hz: float) -> float:
    return float(np.sum(power[(frequencies >= low_hz) & (frequencies < high_hz)]))


def _safe_ratio(numerator: float, denominator: float) -> float:
    return numerator / max(denominator, 1e-12)


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
        rms = float(np.sqrt(np.mean(frame ** 2)))
        peak = float(np.max(np.abs(frame)))
        centroid = weighted / total if total else 0.0
        shape = _spectral_shape(frequencies, power, total, centroid)
        band_powers = {
            "20_80": _band_power(power, frequencies, 20, 80),
            "80_200": _band_power(power, frequencies, 80, 200),
            "200_500": _band_power(power, frequencies, 200, 500),
            "500_2000": _band_power(power, frequencies, 500, 2000),
            "2000_8000": _band_power(power, frequencies, 2000, 8000),
        }
        harmonic_amplitudes = {}
        if np.isfinite(f0) and f0 > 0:
            for harmonic in (1, 2, 3, 4, 5):
                bin_index = int(np.argmin(np.abs(frequencies - harmonic * f0)))
                harmonic_amplitudes[f"harmonic_{harmonic}_db"] = float(_safe_db(magnitude[bin_index]))
        else:
            harmonic_amplitudes = {f"harmonic_{harmonic}_db": float("nan") for harmonic in (1, 2, 3, 4, 5)}
        row = {
            "frame": float(index),
            "time_s": float(index * hop_size / sample_rate),
            "rms_db": float(_safe_db(rms)),
            "peak_db": float(_safe_db(peak)),
            "crest_factor_db": float(_safe_db(peak / rms)) if rms > 0 else float("nan"),
            "spectral_centroid_hz": centroid,
            "spectral_rolloff_hz": float(frequencies[min(rolloff_index, len(frequencies) - 1)]),
            "spectral_flux": spectral_flux,
            "f0_hz": f0,
            "harmonicity_db": float(_safe_db(np.max(power[1:]) / total)) if total and len(power) > 1 else -120.0,
            "band_20_80_db": float(_safe_db(band_powers["20_80"])),
            "band_80_200_db": float(_safe_db(band_powers["80_200"])),
            "band_200_500_db": float(_safe_db(band_powers["200_500"])),
            "band_500_2000_db": float(_safe_db(band_powers["500_2000"])),
            "band_2000_8000_db": float(_safe_db(band_powers["2000_8000"])),
            "band_20_80_to_80_200_db": float(_safe_db(_safe_ratio(band_powers["20_80"], band_powers["80_200"]))),
            "band_200_500_to_80_200_db": float(_safe_db(_safe_ratio(band_powers["200_500"], band_powers["80_200"]))),
            "band_500_2000_to_200_500_db": float(_safe_db(_safe_ratio(band_powers["500_2000"], band_powers["200_500"]))),
            "band_2000_8000_to_500_2000_db": float(_safe_db(_safe_ratio(band_powers["2000_8000"], band_powers["500_2000"]))),
            **shape,
            **harmonic_amplitudes,
            "_spectrum": magnitude,
        }
        results.append(row)
    for row in results:
        del row["_spectrum"]
    return results
