from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(r"C:/IR research")
SRC = Path(r"C:/IR audio/acoustic/bass A/1.wav")
OUT_DIR = ROOT / "experiments" / "E002" / "listener_slices"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Selected candidate events from the range-probe experiment.
# We use a short context buffer so the listener can judge boundaries and merges.
SELECTED = [
    {
        "id": "low_01",
        "setting": "low",
        "start_s": 27.1492,
        "end_s": 27.7297,
        "reason": "Likely sustained note; good candidate for split/merge sanity check",
    },
    {
        "id": "low_02",
        "setting": "low",
        "start_s": 26.2088,
        "end_s": 26.7545,
        "reason": "Lower-register note near the edge of the conservative pass",
    },
    {
        "id": "mid_01",
        "setting": "mid",
        "start_s": 27.5672,
        "end_s": 27.7413,
        "reason": "Shorter event: likely false split or legitimate brief note",
    },
    {
        "id": "mid_02",
        "setting": "mid",
        "start_s": 27.1492,
        "end_s": 27.5672,
        "reason": "Longer event likely to reveal merge or boundary issues",
    },
    {
        "id": "bass_friendly_01",
        "setting": "bass_friendly",
        "start_s": 27.7529,
        "end_s": 28.2186,
        "reason": "Candidate positive; good baseline for comparing settings",
    },
    {
        "id": "broad_01",
        "setting": "broad",
        "start_s": 29.6118,
        "end_s": 29.7743,
        "reason": "Potential extra note or spurious fragment; likely false-positive candidate",
    },
    {
        "id": "broad_02",
        "setting": "broad",
        "start_s": 29.1474,
        "end_s": 29.3448,
        "reason": "Short broad-range event; useful for split-vs-merge judgment",
    },
    {
        "id": "broad_03",
        "setting": "broad",
        "start_s": 27.7529,
        "end_s": 28.2418,
        "reason": "Overlap case in the broader pass; likely to show boundary drift",
    },
]

x, sr = sf.read(str(SRC), dtype="float32", always_2d=True)
# Convert to mono if stereo.
if x.ndim == 2:
    x = x.mean(axis=1)

meta = []
for item in SELECTED:
    start = max(0.0, item["start_s"] - 0.15)
    end = item["end_s"] + 0.15
    start_i = int(start * sr)
    end_i = int(end * sr)
    slice_data = x[start_i:end_i]
    out_path = OUT_DIR / f"{item['id']}_{item['setting']}.wav"
    sf.write(str(out_path), slice_data, sr)
    meta.append({
        "id": item["id"],
        "setting": item["setting"],
        "start_s": item["start_s"],
        "end_s": item["end_s"],
        "file": str(out_path),
        "reason": item["reason"],
    })

(OUT_DIR / "review_manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
print(json.dumps(meta, indent=2))
