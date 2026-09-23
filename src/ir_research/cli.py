from __future__ import annotations

import argparse
from pathlib import Path

from .corpus import analyze_manifest, summarize
from .report import write_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze SLB and acoustic-bass WAV corpora with one feature pipeline.")
    parser.add_argument("manifest", type=Path, help="JSON manifest containing recording paths and domains")
    parser.add_argument("--output", type=Path, default=Path("results/latest"))
    parser.add_argument("--frame-size", type=int, default=4096)
    parser.add_argument("--hop-size", type=int, default=1024)
    args = parser.parse_args()
    result = analyze_manifest(args.manifest, args.frame_size, args.hop_size)
    write_outputs(result, summarize(result), args.output)
    print(f"Analyzed {len(result['metadata'])} recordings, {len(result['frames'])} frames, and {len(result['events'])} events.")
    print(f"Wrote {args.output.resolve()}")
    return 0
