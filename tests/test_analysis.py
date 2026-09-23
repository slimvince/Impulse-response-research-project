from __future__ import annotations

import json
import wave

import numpy as np

from ir_research.audio import frame_signal
from ir_research.corpus import analyze_manifest, summarize
from ir_research.events import detect_events
from ir_research.features import analyze_frames, estimate_f0
from ir_research.report import write_outputs


def _write_wav(path, samples, sample_rate=8000):
    values = np.clip(samples, -1, 1)
    pcm = (values * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())


def test_frame_signal_has_stable_hop_positions():
    frames = frame_signal(np.arange(10, dtype=float), frame_size=4, hop_size=3)
    assert frames.shape == (3, 4)
    np.testing.assert_array_equal(frames[1], [3, 4, 5, 6])


def test_f0_and_spectral_features_are_consistent_for_synthetic_tone():
    sample_rate = 8000
    time = np.arange(sample_rate) / sample_rate
    samples = 0.7 * np.sin(2 * np.pi * 80 * time) + 0.2 * np.sin(2 * np.pi * 160 * time)
    assert 75 < estimate_f0(samples[:4096], sample_rate) < 85
    rows = analyze_frames(samples, sample_rate, frame_size=4096, hop_size=2048)
    assert rows[1]["spectral_centroid_hz"] > 80
    assert rows[1]["band_80_200_db"] > rows[1]["band_500_2000_db"]


def test_event_detection_finds_active_region():
    sample_rate = 8000
    samples = np.zeros(sample_rate)
    samples[1000:4000] = 0.5 * np.sin(2 * np.pi * 80 * np.arange(3000) / sample_rate)
    events = detect_events(samples, sample_rate, frame_size=256, hop_size=128, threshold_db=-35)
    assert len(events) == 1
    assert 0.1 < events[0]["start_s"] < 0.2
    assert events[0]["duration_s"] > 0.3


def test_manifest_pipeline_and_json_outputs(tmp_path):
    sample_rate = 8000
    time = np.arange(sample_rate) / sample_rate
    samples = 0.3 * np.sin(2 * np.pi * 80 * time)
    wav_path = tmp_path / "tone.wav"
    _write_wav(wav_path, samples, sample_rate)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"recordings": [{"recording_id": "tone", "domain": "slb_di", "split": "development", "path": str(wav_path)}]}), encoding="utf-8")
    result = analyze_manifest(manifest, frame_size=1024, hop_size=512)
    assert result["metadata"][0]["sha256"]
    assert result["frames"]
    output = tmp_path / "results"
    write_outputs(result, summarize(result), output)
    json.loads((output / "frames.json").read_text(encoding="utf-8"))
    assert (output / "report.md").exists()
