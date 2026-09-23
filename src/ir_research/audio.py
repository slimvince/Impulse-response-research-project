from __future__ import annotations

from dataclasses import dataclass
import hashlib
import wave
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class AudioData:
    samples: np.ndarray
    sample_rate: int
    channels: int
    source_path: str
    sha256: str


def read_wav(path: str | Path) -> AudioData:
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_rate = handle.getframerate()
        sample_width = handle.getsampwidth()
        frame_count = handle.getnframes()
        raw = handle.readframes(frame_count)
    if sample_width not in (2, 3, 4):
        raise ValueError(f"Unsupported PCM sample width: {sample_width} bytes")
    dtype = {2: np.int16, 3: np.int32, 4: np.int32}[sample_width]
    if sample_width == 3:
        values = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
        signed = (values[:, 0].astype(np.int32) | (values[:, 1].astype(np.int32) << 8) | (values[:, 2].astype(np.int32) << 16))
        signed[signed & 0x800000] -= 1 << 24
        samples = signed.astype(np.float32) / float(1 << 23)
    else:
        samples = np.frombuffer(raw, dtype=dtype).astype(np.float32) / float(1 << (8 * sample_width - 1))
    samples = samples.reshape(-1, channels)
    if channels > 1:
        samples = samples.mean(axis=1, keepdims=True)
    return AudioData(samples[:, 0], sample_rate, channels, str(path), digest)


def frame_signal(samples: np.ndarray, frame_size: int, hop_size: int) -> np.ndarray:
    if samples.ndim != 1 or frame_size <= 0 or hop_size <= 0:
        raise ValueError("samples must be mono and frame/hop sizes must be positive")
    if len(samples) < frame_size:
        samples = np.pad(samples, (0, frame_size - len(samples)))
    count = 1 + (len(samples) - frame_size) // hop_size
    starts = np.arange(count)[:, None] * hop_size
    offsets = np.arange(frame_size)[None, :]
    return samples[starts + offsets]
