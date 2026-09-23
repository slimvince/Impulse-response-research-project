# Impulse Response Research

Phase 1 is **Unified Corpus Characterization** for comparing SLB-200 DI recordings with acoustic double-bass microphone recordings. It does not implement IR optimization.

## Current status

The Python reference pipeline uses one frame/event analysis path for both source domains and writes reproducible machine-readable outputs plus a descriptive report. Original audio is referenced by manifests and is intentionally excluded from Git.

## Windows setup

From PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[test]
python -m pytest -q
```

Create a copy of `configs/manifest.example.json`, replace its paths with licensed local WAV files, then run:

```powershell
ir-research path\to\manifest.json --output results\experiment-001
```

The output contains `metadata.json`, `frames.json`, `events.json`, `summary.json`, and `report.md`. Use development manifests for exploration and keep held-out recordings in separate manifests/splits.

## Research boundaries

Results are descriptive until the corpus has recording-level replication and metadata sufficient to examine player, instrument, microphone, room, level, pitch, articulation, and segmentation confounds. Frame rows are not independent observations. The IR optimization loop is intentionally deferred.

For a new session, start with [docs/project-context.md](docs/project-context.md). The durable project record is organized across [docs/requirements.md](docs/requirements.md), [docs/architecture.md](docs/architecture.md), [docs/feature-catalog.md](docs/feature-catalog.md), [docs/implementation-plan.md](docs/implementation-plan.md), and [docs/research-log.md](docs/research-log.md). The scientific rationale is in [docs/methodology.md](docs/methodology.md), [docs/decisions.md](docs/decisions.md), and [docs/hypotheses.md](docs/hypotheses.md).
