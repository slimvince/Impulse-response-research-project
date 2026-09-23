from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import platform
import subprocess
from pathlib import Path
from typing import Any

import math


def provenance(result: dict[str, Any]) -> dict[str, Any]:
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "unavailable"
    parameters = result.get("analysis_parameters", {})
    return {"generated_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(), "platform": platform.platform(), "numpy": __import__("numpy").__version__, "git_commit": commit, "manifest_sha256": result.get("manifest_sha256"), "analysis_parameters": parameters, "configuration_sha256": hashlib.sha256(json.dumps(parameters, sort_keys=True).encode("utf-8")).hexdigest()}


def _json_safe(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    return value


def write_outputs(result: dict[str, Any], summary: dict[str, Any], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "metadata.json").write_text(json.dumps(_json_safe({"provenance": provenance(result), "metadata": result["metadata"], "feature_version": result["feature_version"]}), indent=2, allow_nan=False), encoding="utf-8")
    (output / "frames.json").write_text(json.dumps(_json_safe(result["frames"]), indent=2, allow_nan=False), encoding="utf-8")
    (output / "events.json").write_text(json.dumps(_json_safe(result["events"]), indent=2, allow_nan=False), encoding="utf-8")
    (output / "summary.json").write_text(json.dumps(_json_safe(summary), indent=2, allow_nan=False), encoding="utf-8")
    lines = ["# Unified Corpus Characterization", "", f"Generated: {provenance(result)['generated_utc']}", "", "## Interpretation", "", "Results below are descriptive observations, not claims of statistical significance. Frame-level counts do not replace recording-level replication.", "", "## Recording summaries", "", "| Recording | Source group | Frames | Events |", "|---|---|---:|---:|"]
    for recording in summary["by_recording"].values():
        lines.append(f"| {recording['recording_id']} | {recording['source_group']} | {recording['frame_count']} | {recording['event_count']} |")
    lines.extend(["", "## Domain comparisons", "", "| Feature | Domains | Mean difference | Standardized difference |", "|---|---|---:|---:|"])
    for row in summary["comparisons"]:
        lines.append(f"| {row['feature']} | {row['left_domain']} vs {row['right_domain']} | {row['mean_difference']:.4g} | {row['standardized_difference']:.4g} |" if row["mean_difference"] is not None and row["standardized_difference"] is not None else f"| {row['feature']} | insufficient data | | |")
    lines.extend(["", "## Limitations and possible confounds", ""] + [f"- {item}" for item in summary["limitations"]])
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
