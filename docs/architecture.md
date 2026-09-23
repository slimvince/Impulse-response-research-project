# Architecture

## Principles

The system is a research instrument, not yet a real-time processor. The eventual objective is to evaluate whether a candidate impulse response can make SLB-200 recordings sound as close as possible to acoustic upright-bass microphone recordings. Components should be replaceable, outputs should be explicit, and source-domain labels must not select different measurement algorithms.

## Current data flow

```text
manifest.json
    -> audio reader
    -> immutable AudioData + source hash
    -> mono sample array
    -> frame extraction
    -> frame feature bank
    -> replaceable event detector
    -> event feature rows
    -> corpus aggregation
    -> JSON outputs + Markdown report
```

## Current modules

- `audio.py`: PCM WAV decoding, channel reduction, frame extraction, and source hashing.
- `features.py`: frame-level numerical measurements and reference f0 estimation.
- `events.py`: threshold-based active-region detection and event descriptors.
- `corpus.py`: manifest loading, unified recording traversal, aggregation, and descriptive comparisons.
- `report.py`: provenance and machine/human-readable output.
- `cli.py`: command-line entry point.

## Ownership boundaries

The audio layer owns sample representation and input metadata. It does not decide whether a recording is SLB or acoustic.

The feature layer owns definitions, units, invalid-value behavior, and feature schema versions. It does not perform domain comparisons.

The event layer owns segmentation interfaces and event geometry. It must be replaceable without changing frame feature definitions.

The corpus layer owns grouping, splits, recording identity, conditioning variables, and aggregation. It must not silently normalize away recording-level differences.

The report layer owns provenance, interpretation labels, limitations, and output serialization. It must not present exploratory effect sizes as confirmed causal findings.

## Planned extension points

- `AudioReader`: broader PCM/float/container support only if a future corpus requires it; WAV remains the Phase 1 input contract.
- `PitchEstimator`: reference autocorrelation plus optional SciPy/librosa/aubio backends for comparison.
- `EventSegmenter`: threshold baseline, onset-based alternative, and reviewed annotations.
- `FeatureExtractor`: broad candidate bank with explicit feature IDs and versions.
- `ComparisonModel`: recording-level summaries, stratification, mixed-effects models, and held-out evaluation.
- `TransformEvaluator`: future closed-loop evaluation only; this is not an optimizer.
- `TransformEvaluator`: future held-out perceptual and measurable evaluation of candidate IRs; it must distinguish filter-addressable differences from level, nonlinear, temporal, and performance effects.

## Dependency strategy

NumPy is the numerical foundation. SciPy and librosa are optional research backends to add when their behavior is tested against the reference implementation. FLAC and broader container support are deferred and not required for Phase 1. Optional libraries must not change the core schema without a recorded decision and versioned comparison.

## Data contracts

Manifest items require `recording_id`, `domain`, `split`, and `path`; `metadata` is extensible. Frame and event rows must retain recording identity, domain, and split. Generated outputs must retain feature version and provenance. Audio files remain external unless licensing explicitly permits redistribution.
