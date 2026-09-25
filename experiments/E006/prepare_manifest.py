from __future__ import annotations

import hashlib
import json
from pathlib import Path

import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]
EXTERNAL = Path(r"C:/IR audio")
DERIVED = Path(r"C:/IR audio/derived/eub_poc/ergo_pcm16")
ERGO_FILES = (
    "A0_1_f.wav", "A0_1_mf.wav", "A0_1_p.wav",
    "A1_1_f.wav", "A1_1_mf.wav", "A1_1_p.wav",
    "A2_1_f.wav", "A2_1_mf.wav", "A2_1_p.wav",
    "C1_1_f.wav", "C1_1_mf.wav", "C1_1_p.wav",
    "A3_1.wav", "A3_2.wav", "A3_3.wav", "A3_4.wav",
)


def main() -> None:
    derived_dir = DERIVED
    derived_dir.mkdir(parents=True, exist_ok=True)
    recordings: list[dict[str, object]] = []
    ns_path = EXTERNAL / "NS Design" / "rr-eub-di.wav"
    recordings.append({
        "recording_id": "ns_design_eub_di",
        "domain": "eub_direct",
        "split": "development",
        "path": str(ns_path),
        "metadata": {
            "source_group": "ns_design_eub",
            "instrument": "NS Design EUB",
            "capture_type": "direct_eub",
            "target_role": "source_domain_only",
            "microphone_target": False,
            "original_sha256": hashlib.sha256(ns_path.read_bytes()).hexdigest(),
        },
    })
    for name in ERGO_FILES:
        source = EXTERNAL / "Ergo" / name
        samples, sample_rate = sf.read(str(source), dtype="float32", always_2d=True)
        derived = derived_dir / name
        sf.write(str(derived), samples.mean(axis=1), sample_rate, subtype="PCM_16")
        articulation = name.rsplit("_", 1)[-1].split(".")[0]
        recordings.append({
            "recording_id": f"ergo_eub_{name[:-4].lower()}",
            "domain": "eub_direct",
            "split": "development",
            "path": str(derived),
            "metadata": {
                "source_group": "ergo_eub",
                "instrument": "Karoryfer Ergo EUB",
                "capture_type": "derived_mono_pcm16",
                "original_path": str(source),
                "original_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "derived_sha256": hashlib.sha256(derived.read_bytes()).hexdigest(),
                "articulation_code": articulation,
                "target_role": "source_domain_only",
                "microphone_target": False,
            },
        })
    manifest = {"experiment_id": "E006", "purpose": "EUB proof of concept using existing unified pipeline", "recordings": recordings}
    path = Path(__file__).with_name("manifest.json")
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path} with {len(recordings)} recordings")


if __name__ == "__main__":
    main()
