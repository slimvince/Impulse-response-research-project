from __future__ import annotations

import csv
import json
import math
import wave
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from ir_research.audio import read_wav

ROOT = Path(__file__).resolve().parents[2]
SOURCE_SLB = Path(r"C:\IR audio\slb200\vincents 1.wav")
VALIDATION = ROOT / "experiments" / "E013" / "results" / "candidate_validation.json"
E008_OLD_MANIFEST = ROOT / "experiments" / "E008" / "all_slices" / "manifest.json"
E008_LABELS = ROOT / "experiments" / "E008" / "audit_slices" / "slb200_event_review.csv"
OUTPUT = Path(__file__).resolve().parent
RESULTS = OUTPUT / "results"
EXTERNAL_OUTPUT = Path(r"C:\IR audio\results\E014")

ACOUSTIC_TRAIN_SETS = (
    "acoustic_bass_a_take_2_cubase_slices",
    "acoustic_bass_a_take_3_cubase_slices",
)
ACOUSTIC_HOLDOUT_SET = "acoustic_bass_b_take_1_cubase_slices"
SLB_CONFIRMED_LABEL = "Use"
SAMPLE_RATE = 44100
FFT_SIZE = 8192
FRAME_SIZE = 4096
FRAME_HOP = 2048
FIR_TAPS = 8192
GAIN_CAP_DB = 6.0


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, (float, np.floating)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, np.generic):
        return value.item()
    return value


def normalized_event_spectrum(samples: np.ndarray, sample_rate: int) -> np.ndarray:
    if sample_rate != SAMPLE_RATE:
        raise ValueError(f"Expected {SAMPLE_RATE} Hz input, got {sample_rate}")
    if len(samples) < FRAME_SIZE:
        samples = np.pad(samples, (0, FRAME_SIZE - len(samples)))
    count = 1 + max(0, (len(samples) - FRAME_SIZE) // FRAME_HOP)
    starts = np.arange(count) * FRAME_HOP
    window = np.hanning(FRAME_SIZE)
    accumulated = np.zeros(FFT_SIZE // 2 + 1, dtype=np.float64)
    for start in starts:
        frame = samples[start:start + FRAME_SIZE]
        if len(frame) < FRAME_SIZE:
            frame = np.pad(frame, (0, FRAME_SIZE - len(frame)))
        magnitude = np.abs(np.fft.rfft(frame * window, n=FFT_SIZE))
        accumulated += magnitude**2
    accumulated /= max(count, 1)
    total = float(np.sum(accumulated))
    if total <= 1e-20:
        raise ValueError("Candidate has no measurable spectral energy")
    return accumulated / total


def third_octave_profile(frequencies: np.ndarray, power: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    centers = 31.5 * 2 ** (np.arange(0, 29) / 3.0)
    centers = centers[centers <= 16000]
    profile = []
    log_frequency = np.log2(np.maximum(frequencies, 1e-9))
    log_power = 10.0 * np.log10(np.maximum(power, 1e-15))
    half_width_octaves = 1.0 / 6.0
    for center in centers:
        mask = np.abs(log_frequency - np.log2(center)) <= half_width_octaves
        profile.append(float(np.median(log_power[mask])) if np.any(mask) else -150.0)
    return centers, np.asarray(profile, dtype=float)


def group_mean_profile(rows: list[dict[str, Any]], slice_set_id: str, frequencies: np.ndarray) -> tuple[np.ndarray, int]:
    spectra = []
    for row in rows:
        if row["slice_set_id"] != slice_set_id or row["event_validity"] != "accept":
            continue
        if float(row["duration_s"]) < 0.12:
            continue
        audio = read_wav(row["file"])
        spectra.append(normalized_event_spectrum(audio.samples, audio.sample_rate))
    if not spectra:
        raise ValueError(f"No eligible accepted slices for {slice_set_id}")
    power = np.mean(np.stack(spectra), axis=0)
    return third_octave_profile(frequencies, power), len(spectra)


def slb_use_profile() -> tuple[np.ndarray, int, list[int]]:
    old_manifest = json.loads(E008_OLD_MANIFEST.read_text(encoding="utf-8"))
    old_by_id = {int(event["event"]): event for event in old_manifest}
    with E008_LABELS.open(newline="", encoding="utf-8") as handle:
        labels = list(csv.DictReader(handle))
    audio = read_wav(SOURCE_SLB)
    spectra = []
    included_event_ids = []
    for label in labels:
        if label["verdict"] != SLB_CONFIRMED_LABEL:
            continue
        event = old_by_id[int(label["event"])]
        start = max(0, int(float(event["start_s"]) * audio.sample_rate))
        end = min(len(audio.samples), max(start + 1, int(float(event["end_s"]) * audio.sample_rate)))
        samples = audio.samples[start:end]
        if len(samples) < int(0.12 * audio.sample_rate):
            continue
        spectra.append(normalized_event_spectrum(samples, audio.sample_rate))
        included_event_ids.append(int(label["event"]))
    if not spectra:
        raise ValueError("No listener-confirmed SLB Use intervals available")
    power = np.mean(np.stack(spectra), axis=0)
    frequencies = np.fft.rfftfreq(FFT_SIZE, 1.0 / SAMPLE_RATE)
    return third_octave_profile(frequencies, power)[1], len(spectra), included_event_ids


def smooth_profile_difference(source_db: np.ndarray, target_db: np.ndarray, centers: np.ndarray) -> np.ndarray:
    difference = target_db - source_db
    # Normalize away unknown absolute recording gain using the 100-1000 Hz region.
    reference = (centers >= 100.0) & (centers <= 1000.0)
    difference -= float(np.median(difference[reference])) if np.any(reference) else float(np.median(difference))
    difference = np.clip(difference, -GAIN_CAP_DB, GAIN_CAP_DB)
    # A short [1, 2, 3, 2, 1] smoother suppresses isolated slice/room peaks.
    kernel = np.asarray([1, 2, 3, 2, 1], dtype=float)
    kernel /= np.sum(kernel)
    padded = np.pad(difference, (2, 2), mode="edge")
    return np.convolve(padded, kernel, mode="valid")


def minimum_phase_fir(centers: np.ndarray, gain_db: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n_fft = 65536
    frequencies = np.fft.rfftfreq(n_fft, 1.0 / SAMPLE_RATE)
    safe_centers = np.maximum(centers, 1.0)
    gain_full = np.interp(
        np.log2(np.maximum(frequencies, safe_centers[0])),
        np.log2(safe_centers),
        gain_db,
        left=float(gain_db[0]),
        right=float(gain_db[-1]),
    )
    gain_full = np.clip(gain_full, -GAIN_CAP_DB, GAIN_CAP_DB)
    log_magnitude = gain_full * (math.log(10.0) / 20.0)
    cepstrum = np.fft.irfft(log_magnitude, n=n_fft)
    minimum_cepstrum = np.zeros_like(cepstrum)
    minimum_cepstrum[0] = cepstrum[0]
    minimum_cepstrum[1:n_fft // 2] = 2.0 * cepstrum[1:n_fft // 2]
    minimum_cepstrum[n_fft // 2] = cepstrum[n_fft // 2]
    minimum_spectrum = np.exp(np.fft.rfft(minimum_cepstrum))
    impulse = np.fft.irfft(minimum_spectrum, n=n_fft)
    fir = impulse[:FIR_TAPS].copy()
    fade = min(1024, FIR_TAPS // 4)
    if fade:
        fir[-fade:] *= np.linspace(1.0, 0.0, fade, endpoint=True)
    return fir, frequencies, gain_full


def fft_convolve_channels(samples: np.ndarray, fir: np.ndarray) -> np.ndarray:
    if samples.ndim != 2:
        raise ValueError("Expected samples shaped (frames, channels)")
    block_size = 65536
    convolution_size = block_size + len(fir) - 1
    fft_size = 1 << (convolution_size - 1).bit_length()
    filter_spectrum = np.fft.rfft(fir, n=fft_size)
    output = np.zeros((len(samples) + len(fir) - 1, samples.shape[1]), dtype=np.float64)
    for channel in range(samples.shape[1]):
        for start in range(0, len(samples), block_size):
            block = samples[start:start + block_size, channel]
            spectrum = np.fft.rfft(block, n=fft_size) * filter_spectrum
            convolved = np.fft.irfft(spectrum, n=fft_size)[:len(block) + len(fir) - 1]
            output[start:start + len(convolved), channel] += convolved
    return output


def read_stereo_pcm16(path: Path) -> tuple[np.ndarray, int, int]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        width = handle.getsampwidth()
        sample_rate = handle.getframerate()
        frames = handle.getnframes()
        raw = handle.readframes(frames)
    if width != 2:
        raise ValueError(f"Expected 16-bit source WAV, got {width * 8}-bit")
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    return samples.reshape(-1, channels), sample_rate, channels


def write_pcm16(path: Path, samples: np.ndarray, sample_rate: int) -> dict[str, Any]:
    peak_before = float(np.max(np.abs(samples))) if samples.size else 0.0
    safety_gain_db = 0.0
    if peak_before > 0.999:
        safety_gain_db = 20.0 * math.log10(0.999 / peak_before)
        samples = samples * 10 ** (safety_gain_db / 20.0)
    clipped = np.clip(samples, -1.0, 1.0)
    pcm = np.rint(clipped * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(samples.shape[1])
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())
    return {"peak_before_safety_gain": peak_before, "safety_gain_db": safety_gain_db, "frames": int(len(pcm)), "channels": int(pcm.shape[1]), "duration_s": len(pcm) / sample_rate}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    EXTERNAL_OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = json.loads(VALIDATION.read_text(encoding="utf-8"))
    frequencies = np.fft.rfftfreq(FFT_SIZE, 1.0 / SAMPLE_RATE)
    source_profile_db, source_count, source_event_ids = slb_use_profile()
    set_profiles = {}
    set_counts = {}
    for slice_set in ACOUSTIC_TRAIN_SETS + (ACOUSTIC_HOLDOUT_SET,):
        set_profiles[slice_set], set_counts[slice_set] = group_mean_profile(rows, slice_set, frequencies)
    train_profile_db = np.mean(np.stack([set_profiles[name][1] for name in ACOUSTIC_TRAIN_SETS]), axis=0)
    holdout_profile_db = set_profiles[ACOUSTIC_HOLDOUT_SET][1]
    centers = set_profiles[ACOUSTIC_TRAIN_SETS[0]][0]
    gain_db = smooth_profile_difference(source_profile_db, train_profile_db, centers)
    fir, fir_frequencies, full_gain = minimum_phase_fir(centers, gain_db)

    comparison_band = (centers >= 40.0) & (centers <= 8000.0)
    predicted_profile_db = source_profile_db + gain_db
    before_error = float(np.mean(np.abs(source_profile_db[comparison_band] - holdout_profile_db[comparison_band])))
    after_error = float(np.mean(np.abs(predicted_profile_db[comparison_band] - holdout_profile_db[comparison_band])))

    np.savez_compressed(
        RESULTS / "candidate_minimum_phase_fir.npz",
        fir=fir.astype(np.float32),
        sample_rate=np.asarray([SAMPLE_RATE], dtype=np.int32),
        smoothed_gain_db=gain_db.astype(np.float32),
        third_octave_centers_hz=centers.astype(np.float32),
    )
    profile = {
        "sample_rate": SAMPLE_RATE,
        "source_use_event_count": source_count,
        "source_use_event_ids": source_event_ids,
        "acoustic_training_sets": {name: {"n": set_counts[name]} for name in ACOUSTIC_TRAIN_SETS},
        "acoustic_holdout_set": {"slice_set_id": ACOUSTIC_HOLDOUT_SET, "n": set_counts[ACOUSTIC_HOLDOUT_SET]},
        "gain_cap_db": GAIN_CAP_DB,
        "fir_taps": len(fir),
        "gain_db_by_third_octave": [{"center_hz": float(f), "gain_db": float(g)} for f, g in zip(centers, gain_db)],
        "holdout_spectral_shape_mae_db_before": before_error,
        "holdout_spectral_shape_mae_db_after": after_error,
        "interpretation": "Unpaired population spectral-shape trial. The holdout metric compares distributions of normalized average spectra, not perceptual quality or a physical transfer function.",
        "limitations": [
            "SLB reference consists of 24 user-confirmed E008 Use intervals from one take.",
            "Acoustic candidate slices are provisionally accepted by uncalibrated E013 rules; they have no human labels yet.",
            "Acoustic sets have unknown microphone, room, placement, chain, player/instrument conditions; A2/A3 train and B3 is held out only by slice set.",
            "Cubase boundaries are candidate intervals, not ground truth; slices without sufficient attack or decay may bias the estimated spectrum.",
            "The FIR matches averaged magnitude shape only, uses a minimum-phase assumption, and discards unknown original recording gain by normalization.",
            "This does not establish that a fixed FIR is sufficient or that the output perceptually emulates acoustic upright bass."
        ]
    }
    (RESULTS / "candidate_profile.json").write_text(json.dumps(json_safe(profile), indent=2, allow_nan=False) + "\n", encoding="utf-8")

    source_stereo, sample_rate, channels = read_stereo_pcm16(SOURCE_SLB)
    if sample_rate != SAMPLE_RATE:
        raise ValueError(f"Expected {SAMPLE_RATE} Hz source, got {sample_rate}")
    rendered = fft_convolve_channels(source_stereo, fir)
    output_path = EXTERNAL_OUTPUT / "vincents_1_candidate_acoustic_EQ_E014.wav"
    render_metadata = write_pcm16(output_path, rendered, sample_rate)
    metadata = {
        "source_path": str(SOURCE_SLB),
        "source_sha256": read_wav(SOURCE_SLB).sha256,
        "output_path": str(output_path),
        "output_sha256": read_wav(output_path).sha256,
        "filter_path": str(RESULTS / "candidate_minimum_phase_fir.npz"),
        "render": render_metadata,
        "filter": {"sample_rate": SAMPLE_RATE, "tap_count": len(fir), "minimum_phase_assumption": True, "gain_cap_db": GAIN_CAP_DB},
        "caveat": "Exploratory candidate transform only; not a validated acoustic-bass emulator or physical impulse response. Preserve the dry source."
    }
    (RESULTS / "render_metadata.json").write_text(json.dumps(json_safe(metadata), indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"SLB reference events: {source_count}; acoustic train per-set: {set_counts}")
    print(f"Holdout normalized spectral-shape MAE: {before_error:.2f} -> {after_error:.2f} dB")
    print(f"Rendered {output_path} ({render_metadata['duration_s']:.2f}s; safety gain {render_metadata['safety_gain_db']:.2f} dB)")


if __name__ == "__main__":
    main()
