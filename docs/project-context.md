# Project Context and Session Handoff

**Purpose:** durable context for a new LLM or a compacted session. Read this file first, then the linked documents.

## Project

This repository investigates whether measurable, systematic characteristics distinguish Yamaha SLB-200 pickup/DI recordings from acoustic double-bass recordings captured with a microphone. The eventual goal may be a transformation that makes the SLB signal resemble the acoustic microphone result. The project is currently in Phase 1: **Unified Corpus Characterization**.

The IR optimizer, neural model, TONEX export, Teensy implementation, and any assumption that a static FIR is sufficient are explicitly out of scope for the current phase.

## Current repository state

The repository began empty. It now contains a Python reference package under `src/ir_research`, synthetic tests under `tests`, an example manifest under `configs`, and research documentation under `docs`.

The current implementation performs:

- PCM WAV loading, mono reduction, and SHA-256 capture;
- deterministic frame extraction;
- frame-level RMS, peak, autocorrelation f0, spectral centroid, spectral rolloff, spectral flux, harmonicity proxy, and broad band energies;
- threshold event detection with duration, attack, sustain, and decay measurements;
- manifest-driven analysis of both domains through the same code path;
- JSON outputs and a descriptive Markdown report.

There are no real corpus recordings in the repository. The current feature bank is exploratory and incomplete. Results must not be described as evidence of domain differences until real recordings are analyzed.

## Current known limitations

- No real audio corpus is present.
- No Python environment has been configured or verified in the workspace.
- The automated pytest suite exists but has not yet been successfully executed in this environment.
- Terminal execution and Git initialization were previously blocked by the local approval gate.
- The f0 and event detectors are deliberately simple reference implementations.
- Comparisons are descriptive; frame rows are not independent observations.
- Phase labels, pitch/register conditioning, dynamics conditioning, and confound-aware statistical models still need development.
- The candidate feature bank should be expanded before selecting a final feature set.

## Required research posture

Treat measurements, interpretations, hypotheses, and implementation assumptions as different things. Preserve uncertainty. Do not optimize an IR against one recording or introduce a feature merely because a library provides it.

## Reasoning chain

Keep this chain explicit when turning discussion into project knowledge:

```text
Observation -> Finding -> Interpretation -> Hypothesis -> Decision
```

An observation is measured or directly documented. A finding is a replicated or qualified evidence statement. An interpretation explains a finding without pretending to be proven causation. A hypothesis is a proposed explanation or next research claim. A decision records what the project will do in response.

## Reading order for a new session

1. This file: current state and constraints.
2. `docs/requirements.md`: what the system must eventually provide.
3. `docs/architecture.md`: ownership boundaries and data flow.
4. `docs/feature-catalog.md`: feature definitions and status.
5. `docs/implementation-plan.md`: next work and blockers.
6. `docs/research-findings.md`: accumulated evidence and current knowledge.
7. `docs/experiments.md`: experiment registry and evidence locations.
8. `docs/corpus-protocol.md` and `docs/corpus.md`: how data must be captured and what data exists.
9. `docs/confounds.md`: threats to interpretation.
10. `docs/external-research.md` and `docs/ecosystem.md`: source ledger and current dependency summary.
11. `docs/decisions.md`, `docs/methodology.md`, and `docs/hypotheses.md`: rationale and research method.
12. `docs/research-log.md`: dated progress and unresolved questions.
13. `README.md`: setup and command reference.

## Session continuation rule

Before ending a substantial session, update `implementation-plan.md` and `research-log.md`. If a choice was made, add an entry to `decisions.md`. If evidence changed a research belief, update `hypotheses.md`. If code behavior changed, update the feature catalog or architecture document and add tests where practical.
