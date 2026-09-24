# Implementation Plan

## Current phase: Unified Corpus Characterization and event benchmarking

### Completed

- Python package scaffold and editable installation configuration
- Standard-library PCM WAV reader with source hashing
- Deterministic framing
- Initial frame and event measurements
- Manifest-driven unified pipeline
- JSON and Markdown outputs
- Synthetic test definitions
- Research documentation and licensing boundary
- Full test suite: 4 passing tests
- Synthetic WAV CLI smoke test with all five expected output files
- Git initialization, commits, push, and clean synchronized worktree

### Immediate blockers

- Obtain or record a small licensed pilot corpus.
- Confirm permission and complete capture metadata for the four external acoustic candidate recordings.
- Establish reliable note/event segmentation as a first-class research problem rather than a later quality improvement.
- Benchmark onset/offset, pitch-tracking, note-segmentation, overlap/polyphony, and legato-handling methods on representative corpus recordings.
- Add later bass A and bass B recordings to their existing source groups, and register other acoustic basses as separate source groups.
- Implement within-group repeatability summaries for the bass A and bass B pairs before freezing the first `E001` manifest.
- Register approved pilot recordings and freeze the first `E001` manifest.

### Next implementation steps

1. Make the Python environment reproducible with a locked or recorded dependency set.
2. Add tests for silence, multichannel input, 24-bit PCM, invalid f0, and deterministic repeated runs.
3. Treat event detection and note segmentation as immediate research tasks, not as a post-hoc enhancement; benchmark the existing threshold detector against likely open-source alternatives and quantify errors on representative material.
4. Create a small manually reviewed ground-truth subset for onset, offset, note boundaries, pitch, overlap, and legato cases; compute onset timing error, offset timing error, missed/false events, incorrect boundaries, pitch error, and confidence metrics.
5. Continue the broad feature bank only where a concrete, testable descriptor remains justified; the current spectral-shape, band-ratio, crest-factor, f0-relative harmonic, peak/bandwidth, envelope, f0-confidence, harmonic-to-residual, and inharmonicity descriptors are implemented.
6. Add feature definitions and validity metadata to a versioned feature configuration.
7. Add paired-recording metadata and a distribution-level repeatability baseline for recordings expected to match without requiring matched musical content; recording/source-group summaries and missing counts are now implemented, with the current bass A/bass B candidates as the first input.
8. Add recording/event-level aggregation before any inferential statistics.
9. Add pitch/register and observed-local-level summaries without assuming absolute level calibration.
10. Add explicit confound tables and missing-metadata warnings; file quality diagnostics and per-feature missing counts are now implemented.
11. Compare selected reference algorithms with SciPy/librosa backends without changing the canonical schema silently.
12. Analyze a pilot corpus and update hypotheses based on measured results.

### Research stages for event-level evaluation

- Benchmark candidate onset and offset algorithms against a manually reviewed ground-truth subset.
- Evaluate bass pitch-tracking and note segmentation on isolated, overlapped, and legato excerpts.
- Assess overlap/polyphonic detection and confidence classification, and exclude ambiguous events when needed.
- Compare event-conditioned temporal and spectral measurements between SLB and acoustic notes while conditioning on register, dynamics, articulation, and overlap status.
- Build recording-level and event-level comparison models only after segmentation reliability is quantified.
- Freeze development and held-out corpus manifests only after the event-detection benchmark is accepted for the intended use case.
- Define a closed-loop transform evaluation protocol for held-out note-level comparisons.
- Only then investigate candidate FIR or other transformations.
- If long recordings make memory a practical problem, add internal streaming without requiring manual source splitting; preserve source hashes, frame continuity, event context, and whole-file semantics.
- Revisit broader audio-format support only if it becomes a concrete corpus blocker.

## Completion criteria for Phase 1

Phase 1 is not complete when a large CSV exists. It is complete when:

- both domains run through the same versioned pipeline;
- source hashes, parameters, splits, and metadata are recorded;
- candidate features have synthetic tests and documented limitations;
- event detection is benchmarked and confidence-labeled for note-level use;
- comparisons are recording-level and event-conditionable;
- repeatability variation is quantified before domain differences are selected as transformation targets;
- reports distinguish observation from interpretation and confound;
- held-out evaluation can be performed without corpus leakage;
- the corpus is large enough to support qualified conclusions.
