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

## Last validated state

This describes the last validated committed state, not necessarily the current working tree. Documentation changes made after that validation must be committed before treating them as part of the canonical remote handoff state.

- `main` is synchronized with `origin/main`.
- `2493ca6` established the initial unified corpus characterization foundation.
- `66d98fe` added the research-memory and experiment documentation layers.
- `8d9663a` corrected the frame-quantized event-onset test expectation.
- The full automated suite passed: `4 passed`.
- A disposable synthetic 80 Hz WAV passed through the CLI smoke test.
- The smoke test produced `metadata.json`, `frames.json`, `events.json`, `summary.json`, and `report.md`.
- Temporary smoke-test files were removed; no audio or generated results were committed.
- The Git worktree was clean after validation.

The next real milestone is a licensed pilot corpus and experiment `E001`, not IR optimization.

## Current known limitations

- No real audio corpus is present.
- The f0 and event detectors are deliberately simple reference implementations.
- Comparisons are descriptive; frame rows are not independent observations.
- Phase labels, pitch/register conditioning, dynamics conditioning, and confound-aware statistical models still need development.
- The candidate feature bank should be expanded before selecting a final feature set.

Terminal and agent execution capabilities may differ between LLM sessions. Do not infer validation from a session that did not report actual command output; use the committed Git state and this validated-state section as the repository record.

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
14. `experiments/_template/README.md`, `manifest.json`, and `config.json`: the required shape of the next experiment.

## New-session handoff protocol

Before changing code or research documents, a new session must:

1. Read this file and the documents in the reading order above.
2. State the current phase, validated state, known limitations, immediate blockers, and next action.
3. Check the repository status and recent Git history when terminal access is available.
4. Identify any conflict between the session's assumptions and the repository record.
5. Preserve the distinction between synthetic implementation validation and empirical findings from real recordings.

If terminal access is unavailable, the session must say so explicitly and must not claim that tests, Git, or CLI commands were run.

## Session continuation rule

Before ending a substantial session, update `implementation-plan.md` and `research-log.md`. If a choice was made, add an entry to `decisions.md`. If evidence changed a research belief, update `hypotheses.md`. If code behavior changed, update the feature catalog or architecture document and add tests where practical.
