# Implementation Plan

## Current phase: Unified Corpus Characterization

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
- Add later bass A and bass B recordings to their existing source groups, and register other acoustic basses as separate source groups.
- Implement within-group repeatability summaries for the bass A and bass B pairs before freezing the first `E001` manifest.
- Register approved pilot recordings and freeze the first `E001` manifest.
- Commit and push the current documentation handoff updates before starting a new session.

### Next implementation steps

1. Make the Python environment reproducible with a locked or recorded dependency set.
2. Add tests for silence, multichannel input, 24-bit PCM, invalid f0, and deterministic repeated runs.
3. Expand the feature bank broadly with readily extractable spectral, envelope, harmonic, periodicity, temporal, and dynamics descriptors. Initial spectral-shape, band-ratio, crest-factor, and f0-relative harmonic descriptors are implemented.
4. Add feature definitions and validity metadata to a versioned feature configuration.
5. Add paired-recording metadata and a distribution-level repeatability baseline for recordings expected to match without requiring matched musical content; use the current bass A/bass B candidates first and support later takes and source groups without changing prior experiment identities.
6. Add recording/event-level aggregation before any inferential statistics.
7. Add pitch/register and observed-local-level summaries without assuming absolute level calibration.
8. Add explicit confound tables and missing-metadata warnings.
9. Compare selected reference algorithms with SciPy/librosa backends without changing the canonical schema silently.
10. Analyze a pilot corpus and update hypotheses based on measured results.

### Later research stages

- Improve or annotate event segmentation.
- Build recording-level and mixed-effects comparison models.
- Freeze development and held-out corpus manifests.
- Define a closed-loop transform evaluation protocol.
- Only then investigate candidate FIR or other transformations.

## Completion criteria for Phase 1

Phase 1 is not complete when a large CSV exists. It is complete when:

- both domains run through the same versioned pipeline;
- source hashes, parameters, splits, and metadata are recorded;
- candidate features have synthetic tests and documented limitations;
- events and temporal phases can be inspected;
- comparisons are recording-level and conditionable;
- repeatability variation is quantified before domain differences are selected as transformation targets;
- reports distinguish observation from interpretation and confound;
- held-out evaluation can be performed without corpus leakage;
- the corpus is large enough to support qualified conclusions.
