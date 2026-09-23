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

### Immediate blockers

- Configure a Python interpreter and install package dependencies.
- Run pytest and the CLI against synthetic WAV files.
- Initialize Git and create the first meaningful commit.
- Obtain or record a small licensed pilot corpus.

### Next implementation steps

1. Make the Python environment reproducible with a locked or recorded dependency set.
2. Execute and repair the existing synthetic tests.
3. Add tests for silence, multichannel input, 24-bit PCM, invalid f0, and deterministic repeated runs.
4. Expand the feature bank with spectral slope, envelope summaries, harmonic amplitudes, H1/H2, and phase labels.
5. Add feature definitions and validity metadata to a versioned feature configuration.
6. Add recording/event-level aggregation before any inferential statistics.
7. Add pitch/register and loudness-conditioned summaries.
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
- reports distinguish observation from interpretation and confound;
- held-out evaluation can be performed without corpus leakage;
- the corpus is large enough to support qualified conclusions.
