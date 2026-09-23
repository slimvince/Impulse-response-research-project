# Phase 1 Methodology

## Unified pipeline

Every manifest recording passes through the same WAV decode, mono reduction, frame extraction, spectral analysis, event detection, and reporting path. Domain and split are metadata labels, not alternate algorithms.

## Implemented measurements

Frame-level output currently includes RMS and peak level in dB, autocorrelation-based f0 estimate, spectral centroid, 85% spectral rolloff, frame-to-frame spectral flux, a coarse harmonicity ratio, and energy in 20-80, 80-200, 200-500, 500-2000, and 2000-8000 Hz bands. Event output includes threshold onset/end, duration, peak time/level, attack time, median late-event level, and a simple decay slope. Recording metadata includes SHA-256, sample rate, channel count, sample count, domain, split, and manifest metadata.

## Systematic-difference analysis

The current report computes descriptive per-domain means, standard deviations, and standardized differences. It labels these as descriptive only. Future analysis should aggregate at recording level and use event-derived measurements as within-file descriptors; detected event counts are file-specific segmentation diagnostics and are not expected to correlate across recordings or serve as similarity measures. Comparisons should stratify or model pitch/register and dynamics where supported, and evaluate source-domain interactions with temporal phase and articulation. Held-out splits must be fixed in manifests before any optimization work.

Potential confounds must be recorded rather than inferred away: unknown and time-varying recording level, microphone and placement, room, player, instrument, chain, and segmentation quality. A difference is strong only when it repeats across recordings and remains after conditioning that is actually supported by metadata. Global gain normalization cannot reconstruct an unknown or drifting recording level. Small or unbalanced corpora should produce an unresolved result, not a significance claim.

## Reproducibility

Manifests are explicit; original audio is not modified. Outputs retain source hashes, feature version, Python/platform information, UTC generation time, and Git commit when available. Experiment configuration and corpus split belong in version control; licensed audio remains outside the repository.
