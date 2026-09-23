# Project Context and Session Handoff

**Purpose:** durable context for a new LLM or a compacted session. Read this file first, then the linked documents.

## Project

This repository investigates whether measurable, systematic characteristics distinguish Yamaha SLB-200 pickup/DI recordings from acoustic double-bass recordings captured with a microphone. The governing eventual goal is to make an SLB-200 recording sound as close as possible to an acoustic upright-bass microphone recording using an impulse response. The project is currently in Phase 1: **Unified Corpus Characterization**.

The IR optimizer, neural model, TONEX export, Teensy implementation, and any assumption that a static FIR is sufficient are explicitly out of scope for the current phase. Phase 1 identifies repeatable, relevant, and plausibly filter-addressable differences for later held-out IR evaluation.

## Current repository state

The repository began empty. It now contains a Python reference package under `src/ir_research`, synthetic tests under `tests`, an example manifest under `configs`, and research documentation under `docs`.

The current implementation performs:

- PCM WAV loading, mono reduction, and SHA-256 capture. WAV is the Phase 1 input contract; FLAC is deferred unless it becomes a corpus blocker;
- deterministic frame extraction;
- frame-level RMS, peak, crest factor, autocorrelation f0 and confidence, spectral centroid, spread, skewness, kurtosis, slope, flatness, rolloff, flux, spectral peak/bandwidth, harmonicity proxy, f0-relative harmonic amplitudes and ratios, harmonic-to-residual ratio, inharmonicity proxy, broad band energies, band ratios, and frame-envelope descriptors;
- threshold event detection with duration, attack, sustain, and decay measurements;
- manifest-driven analysis of both domains through the same code path;
- JSON outputs and a descriptive Markdown report.

There are no audio recordings in the repository. Four external candidate acoustic recordings exist outside Git: two user-reported similar files for bass/player group A and two for group B. They are free to use by user confirmation, but contextual metadata other than file facts and the player label may be unknown. The current feature bank is broad but exploratory; extracted differences are not automatically evidence of intrinsic bass or domain characteristics.

## Last validated state

This describes the last validated committed state, not necessarily the current working tree. Documentation changes made after that validation must be committed before treating them as part of the canonical remote handoff state.

- `main` is synchronized with `origin/main`.
- Latest validated code baseline before this handoff consolidation is `13d3591` (`Preserve intact long recordings`); the handoff commit that follows will supersede that hash without changing code.
- Recent decisions include WAV-only Phase 1 input (`789ef74`), unknown historical setup metadata (`544d4f8`), the governing IR objective (`904892d`), broad feature expansion (`1a9e3ef`, `a4a6f97`, `68a3cec`), and recording-level replication guidance (`d088209`).
- The full automated suite passes: `4 passed`.
- The four external acoustic WAVs were analyzed successfully with feature schema version `0.3`: `47,055` frames and `105` threshold-detected events.
- Expanded real-audio validation produced outputs under `C:\IR audio\results\acoustic-repeatability-v03`; the external manifest is `C:\IR audio\acoustic-repeatability-manifest.json`.
- New spectral and band-ratio features were valid for all frames. f0-dependent descriptors were valid for `47,029` frames and missing for `26` invalid-f0 frames.
- No audio or generated results are committed to Git. The worktree is clean after the latest commit.

The next milestone is grouped recording/source-level repeatability summaries and quality diagnostics, followed by more recordings and an approved/frozen `E001` manifest. The next real transformation milestone is held-out IR evaluation, not optimizer implementation now.

## Current known limitations

- No audio is stored in Git; the four external files are candidate inputs, not a complete or approved corpus.
- Only player identity may be known contextually; bass identity, room, microphone, placement, recording chain, processing, strings, take conditions, and absolute/time-varying level may be unknown.
- Pitch/register and musical content are intentionally unmatched; event counts are file-specific segmentation diagnostics and not similarity measures.
- The f0 and event detectors and several descriptors are deliberately simple reference/proxy implementations.
- Comparisons are descriptive; overlapping frame rows are not independent observations. Recordings and source groups are the replication units.
- Grouped repeatability summaries, quality diagnostics, observed-local-level summaries, parameter sensitivity, and confound-aware models still need development.
- Long recordings must remain intact; future memory optimization may use internal streaming only with frame/event continuity and provenance preservation.
- No SLB-200 recordings exist yet, so no SLB-to-acoustic comparison or IR target claim is currently possible.

Terminal and agent execution capabilities may differ between LLM sessions. Do not infer validation from a session that did not report actual command output; use the committed Git state and this validated-state section as the repository record.

## Required research posture

Treat measurements, interpretations, hypotheses, and implementation assumptions as different things. Preserve uncertainty. Do not optimize an IR against one recording or introduce a feature as an IR target merely because a library provides it. Broad extraction is exploratory evidence gathering; eventual IR success requires held-out measurable and perceptual evaluation.

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
