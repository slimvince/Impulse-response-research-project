from __future__ import annotations

import hashlib
import json
import math
import sys
import wave
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments.E014.build_and_render_candidate import fft_convolve_channels, read_stereo_pcm16

SOURCE = Path(r"C:\IR audio\slb200\recording two slices\yamaha bass slb200.wav")
E014_FILTER = ROOT / "experiments" / "E014" / "results" / "candidate_minimum_phase_fir.npz"
E016_FILTER = ROOT / "experiments" / "E016" / "results" / "candidate_per_event_median_fir.npz"
EXTERNAL_OUTPUT = Path(r"C:\IR audio\results\E018")
WORKSPACE_OUTPUT = Path(__file__).resolve().parent
LISTENING = WORKSPACE_OUTPUT / "listening"
BLOCK_FRAMES = 32768


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.asarray(values, dtype=np.float64) ** 2)))


def overlap_add_to_memmap(samples: np.ndarray, fir: np.ndarray, output_path: Path) -> np.memmap:
    output_frames = len(samples) + len(fir) - 1
    output = np.memmap(output_path, mode="w+", dtype=np.float32, shape=(output_frames, samples.shape[1]))
    output[:] = 0.0
    fft_size = 1 << (BLOCK_FRAMES + len(fir) - 2).bit_length()
    filter_spectrum = np.fft.rfft(fir, n=fft_size)
    for channel in range(samples.shape[1]):
        for start in range(0, len(samples), BLOCK_FRAMES):
            block = samples[start:start + BLOCK_FRAMES, channel]
            spectrum = np.fft.rfft(block, n=fft_size) * filter_spectrum
            convolved = np.fft.irfft(spectrum, n=fft_size)[:len(block) + len(fir) - 1]
            output[start:start + len(convolved), channel] += convolved.astype(np.float32)
    output.flush()
    return output


def write_pcm16(path: Path, samples: np.ndarray, gain: float = 1.0) -> dict[str, float | int]:
    peak = memmap_peak(samples) * gain
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(samples.shape[1])
        handle.setsampwidth(2)
        handle.setframerate(44100)
        safety_gain_db = 20.0 * math.log10(0.999 / peak) if peak > 0.999 else 0.0
        effective_gain = gain * 10 ** (safety_gain_db / 20.0)
        for start in range(0, len(samples), BLOCK_FRAMES):
            block = np.asarray(samples[start:start + BLOCK_FRAMES], dtype=np.float64) * effective_gain
            pcm = np.rint(np.clip(block, -1.0, 1.0) * 32767.0).astype(np.int16)
            handle.writeframes(pcm.tobytes())
    return {"peak_before_safety_gain": peak, "requested_gain": gain, "safety_gain_db": safety_gain_db, "frames": int(len(samples)), "duration_s": len(samples) / 44100.0}


def memmap_peak(samples: np.ndarray) -> float:
    peak = 0.0
    for start in range(0, len(samples), BLOCK_FRAMES):
        block = np.asarray(samples[start:start + BLOCK_FRAMES], dtype=np.float64)
        if block.size:
            peak = max(peak, float(np.max(np.abs(block))))
    return peak


def memmap_rms(samples: np.ndarray) -> float:
    square_sum = 0.0
    count = 0
    for start in range(0, len(samples), BLOCK_FRAMES):
        block = np.asarray(samples[start:start + BLOCK_FRAMES], dtype=np.float64)
        square_sum += float(np.sum(block**2))
        count += block.size
    return math.sqrt(square_sum / max(count, 1))


def main() -> None:
    EXTERNAL_OUTPUT.mkdir(parents=True, exist_ok=True)
    LISTENING.mkdir(parents=True, exist_ok=True)
    samples, sample_rate, channels = read_stereo_pcm16(SOURCE)
    if sample_rate != 44100:
        raise ValueError(f"E018 filters are 44.1 kHz; source is {sample_rate} Hz")
    dry_rms = rms(samples)
    render_records: dict[str, Any] = {}
    audition_files: dict[str, str] = {}

    variants = (
        ("E014", E014_FILTER, "recording_two_E014"),
        ("E016", E016_FILTER, "recording_two_E016"),
    )
    for name, filter_path, prefix in variants:
        fir = np.load(filter_path)["fir"].astype(np.float64)
        temp_path = EXTERNAL_OUTPUT / f".{prefix}_float32.tmp"
        rendered = overlap_add_to_memmap(samples, fir, temp_path)
        filtered_rms = memmap_rms(rendered)
        match_gain = dry_rms / max(filtered_rms, 1e-12)
        raw_path = EXTERNAL_OUTPUT / f"{prefix}_raw.wav"
        matched_path = EXTERNAL_OUTPUT / f"{prefix}_rms_matched.wav"
        raw_stats = write_pcm16(raw_path, rendered)
        matched_stats = write_pcm16(matched_path, rendered, gain=match_gain)
        raw_stats["output_sha256"] = hash_file(raw_path)
        matched_stats["output_sha256"] = hash_file(matched_path)
        raw_stats["output_sha256"] = hash_file(raw_path)
        matched_stats["output_sha256"] = hash_file(matched_path)
        render_records[name] = {
            "filter_path": str(filter_path),
            "tap_count": len(fir),
            "dry_rms_linear": dry_rms,
            "filtered_rms_linear": filtered_rms,
            "whole_file_rms_match_gain_db": 20.0 * math.log10(max(match_gain, 1e-12)),
            "raw": raw_stats,
            "rms_matched": matched_stats,
        }
        for variant, source_path in (("raw", raw_path), ("rms_matched", matched_path)):
            if name == "E014" and variant == "raw":
                continue
            listening_name = source_path.name
            destination = LISTENING / listening_name
            destination.write_bytes(source_path.read_bytes())
            audition_files[f"{name}_{variant}"] = f"listening/{listening_name}"
        del rendered
        temp_path.unlink(missing_ok=True)

    metadata = {
        "experiment_id": "E018",
        "source_path": str(SOURCE),
        "source_sha256": hash_file(SOURCE),
        "source_sample_rate": sample_rate,
        "source_channels": channels,
        "source_sample_width_bytes": 2,
        "source_duration_s": len(samples) / sample_rate,
        "source_relation_note": "User identified this as unsliced SLB-200 recording two; it is in the former Audio 02 slice folder. Identity with those Cubase slices is plausible but not assumed as verified provenance.",
        "renders": render_records,
        "audition_files": audition_files,
        "source_preserved": True,
        "interpretation": "Applies existing exploratory E014/E016 filters to a second complete SLB take; does not validate acoustic emulation.",
    }
    (WORKSPACE_OUTPUT / "render_metadata.json").write_text(json.dumps(metadata, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("source", metadata["source_duration_s"], "seconds", metadata["source_sha256"])
    for name, info in render_records.items():
        print(name, "raw", info["raw"], "matched_gain_db", info["whole_file_rms_match_gain_db"], "matched", info["rms_matched"])


if __name__ == "__main__":
    main()
