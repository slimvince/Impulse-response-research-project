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

There are no audio recordings in the repository. Nine external candidate acoustic recordings exist outside Git: five for source group A, two for group B, one for group C, and one for new source group D. They are free to use by user confirmation, but contextual metadata other than file facts and the player label may be unknown. The current feature bank is broad but exploratory; extracted differences are not automatically evidence of intrinsic bass or domain characteristics.

## Current status after E003 note benchmark

## Current status after E005/E006

The algorithm bake-off and EUB proof of concept have now advanced beyond the original E003 state. E005 tested and tuned the recursive detector, librosa, aubio, Basic Pitch, and MuScriptor. The recursive detector remains the best count/onset baseline; aubio and MuScriptor are the strongest independent candidates by count transfer. E006 applies the unchanged unified pipeline to NS Design direct/EUB and representative Ergo EUB material. The immediate next gate is EUB event-quality audit followed by conditional source-domain/time-frequency analysis, not more blind detector tuning or IR optimization.

The immediate research gate is note/event segmentation. Four manually reviewed listener excerpts now have approximate note labels in `experiments/E003/ground_truth.csv`: three notes in `low_02_low.wav`, three in `bass_friendly_01_bass_friendly.wav`, three in `broad_03_broad.wav`, and five in `low_01_low.wav`. The labels are confidence-2 audition boundaries, not high-precision ground truth.

The E003 evaluator tested five frame/hop/threshold settings. The best count agreement was `frame_size=256`, `hop_size=64`, `threshold_db=-45`, producing 3/3, 3/3, 3/3, and 3/5 detected/reference counts, with total absolute count error 2. The detector still merges notes in `low_01_low.wav`; this is not evidence that it can reliably identify all individual notes.

The pitch-aware splitter remains a reference implementation with a two-break global cap. A probe raising the cap to four was rejected because it produced false splits and changed the conservative-setting counts to 5/5/5/5. The next implementation should use a selective rule for long multi-note regions, validated against all excerpts, rather than globally allowing more splits.

Audition exports under `experiments/E003/detected_slices` are raw exact-boundary sample slices: no fades, context, normalization, or other postprocessing. Analysis inputs remain the original WAVs under `experiments/E002/listener_slices`. The full current handover is in `docs/handover-current.md`.

## Current status after the E002 gate

## Current consolidated status: E005/E006/E007

The current research state is beyond the original E003 segmentation gate. E005 completed a first real-recording algorithm bake-off: recursive detector, librosa, aubio, Basic Pitch, and MuScriptor were run/tuned with development/holdout separation. The recursive detector is the count/onset baseline; aubio and MuScriptor are independent candidates requiring human boundary audits. E006 executed the unified pipeline on NS Design direct/EUB and representative Ergo EUB material. E007 began descriptive acoustic-vs-EUB analysis using real recordings, but its aggregate differences are confounded and are not IR targets.

The current transformability hypothesis is conditional per-event comparison: prioritize event-level spectral/temporal trajectories conditioned on register, local level, articulation, and onset-relative phase. Exact acoustic/EUB sample synchronization is not required for a statistical candidate transform, but controlled repeated material is needed for validation. Whole-piece averages remain secondary context.

The project is still in Phase 1, but the event-segmentation gate is now a first-class milestone. The repository includes a completed `E002` experiment under `experiments/E002/` that ran the Spotify Basic Pitch detector on four 30-second acoustic excerpts. The observed output was:

- default Basic Pitch setting: 82-96 events per excerpt;
- stricter filtered setting: 15-41 events per excerpt;
- repository threshold detector baseline: 4-6 events per excerpt.

The listener-review pass did not rescue the situation, but it corrected the interpretation. A small candidate set from the main settings was auditioned and every selected clip contained multiple distinct plucked notes in sequence: `low_01_low` contained five notes; the `mid_*` clips contained three notes each; the `bass_*` clips contained three notes each; the `broad_*` clips contained three notes each. The pitch/frequency domain showed clear note-to-note changes with no glissandi or portamenti, and the notes were not tied, so this was a series of individually plucked notes rather than a single sustained note or hammer-on/legato event.

This is decisive evidence that the current single-pass Basic Pitch candidate clips are not valid single-note segmentation samples, but the issue is not that the clips are musically wrong; it is that the selected windows contain multiple separate notes and therefore do not isolate a single note boundary. The detector may still be useful as a broad candidate generator, but it is not yet credible as a note-level segmentation method for downstream IR evaluation without explicit boundary labeling and a true single-note benchmark.

This is not a final note detector validation; it is a conditional pass with a more precise conclusion than before. The evidence supports using Basic Pitch as a candidate event generator and conservative filter only for exploratory triage, not as a fully trusted note-segmentation method. The project must still create a small manually reviewed ground-truth subset of isolated notes and note transitions, then quantify split/merge/missed-boundary errors before event-conditioned analyses can be treated as scientifically reliable.

Human auditory validation remains valuable. Individual event slices can be auditioned by a listener to judge whether detections are split, merged, or missed, and to provide a quick sanity check before full benchmark scoring. This does not replace quantitative measurement, but it helps quickly identify obvious failure modes and prioritize manual review. In the current setting, the audition clarifies that the selected candidate windows contain multiple distinct notes and therefore cannot be treated as isolated single-note examples.

## Last validated state

This describes the last validated committed state, not necessarily the current working tree. Documentation changes made after that validation must be committed before treating them as part of the canonical remote handoff state.

- `main` is synchronized with `origin/main`.
- Current validated commit: `50f899b` (`Finalize Basic Pitch gate metadata`).
- The full automated suite passes: `4 passed`.
- The event gate experiment `E002` is recorded with `manifest.json`, `config.json`, the execution script, and a summary JSON under `experiments/E002/`.
- The Basic Pitch pilot is considered a conditional pass, not a final scientific conclusion.
- The next milestone is a manually reviewed event benchmark on a small ground-truth subset; only then should more event-conditioned pipeline work proceed confidently.
- No audio or generated results are committed to Git beyond the intentionally small experiment metadata and summary outputs. The worktree is clean after the latest commit.

The next real transformation milestone is held-out IR evaluation, not optimizer implementation now. Prior to that, the project needs a conservative event-quality benchmark, explicit confidence labeling, and human review of split/merge behavior.

## Current known limitations

- No audio is stored in Git; the nine external files are candidate inputs, not a complete or approved corpus.
- Only player identity may be known contextually; bass identity, room, microphone, placement, recording chain, processing, strings, take conditions, and absolute/time-varying level may be unknown.
- Pitch/register and musical content are intentionally unmatched; event counts are file-specific segmentation diagnostics and not similarity measures.
- The f0 and event detectors and several descriptors are deliberately simple reference/proxy implementations.
- Comparisons are descriptive; overlapping frame rows are not independent observations. Recordings and source groups are the replication units.
- Grouped repeatability summaries, quality diagnostics, observed-local-level summaries, parameter sensitivity, and confound-aware models still need development.
- The Basic Pitch pilot demonstrates a candidate event generator but does not yet validate segmentation quality; it remains a conditional pass pending manual benchmark review.
- Long recordings must remain intact; future memory optimization may use internal streaming only with frame/event continuity and provenance preservation.
- One user-provided SLB-200 candidate is now available outside Git, but no SLB-to-acoustic comparison or IR target claim is currently possible. Multiple documented takes and contextual metadata are still required.

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

1. `docs/handover-current.md`: most recent E003 state, validation, raw-audition policy, and next actions.
2. This file: current state and constraints.
3. `docs/requirements.md`: what the system must eventually provide.
4. `docs/architecture.md`: ownership boundaries and data flow.
5. `docs/feature-catalog.md`: feature definitions and status.
6. `docs/implementation-plan.md`: next work and blockers.
7. `docs/note-segmentation-benchmark.md`: the current benchmark-first plan for note and event segmentation.
8. `docs/research-findings.md`: accumulated evidence and current knowledge.
9. `docs/experiments.md`: experiment registry and evidence locations.
10. `docs/corpus-protocol.md` and `docs/corpus.md`: how data must be captured and what data exists.
11. `docs/confounds.md`: threats to interpretation.
12. `docs/external-research.md` and `docs/ecosystem.md`: source ledger and current dependency summary.
13. `docs/decisions.md`, `docs/methodology.md`, and `docs/hypotheses.md`: rationale and research method.
14. `docs/research-log.md`: dated progress and unresolved questions.
15. `README.md`: setup and command reference.
16. `experiments/_template/README.md`, `manifest.json`, and `config.json`: the required shape of the next experiment.

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
