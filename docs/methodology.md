# Phase 1 Methodology

## Unified pipeline

Every manifest recording passes through the same WAV decode, mono reduction, frame extraction, spectral analysis, event detection, and reporting path. Domain and split are metadata labels, not alternate algorithms.

## Eventual transformation objective

The eventual goal is an impulse response that makes an SLB-200 recording sound as close as possible to an acoustic upright-bass microphone recording. Phase 1 does not fit that IR. It identifies measurable candidate differences, estimates their repeatability, and determines which differences are plausibly addressable by a fixed linear time-invariant filter. Level drift, nonlinear processing, player technique, room changes, and other non-filter effects remain evaluation factors rather than automatic IR targets.

## Implemented measurements

Frame-level output currently includes RMS and peak level in dB, autocorrelation-based f0 estimate, spectral centroid, 85% spectral rolloff, frame-to-frame spectral flux, a coarse harmonicity ratio, and energy in 20-80, 80-200, 200-500, 500-2000, and 2000-8000 Hz bands. Event output includes threshold onset/end, duration, peak time/level, attack time, median late-event level, and a simple decay slope. Recording metadata includes SHA-256, sample rate, channel count, sample count, domain, split, and manifest metadata.

## Systematic-difference analysis

The current report computes descriptive per-domain means, standard deviations, and standardized differences. It labels these as descriptive only. Future analysis should aggregate at recording level and use event-derived measurements as within-file descriptors; detected event counts are file-specific segmentation diagnostics and are not expected to correlate across recordings or serve as similarity measures. Pitch/register distributions will remain unmatched by design, and setup metadata may remain incomplete; those limitations must be reported rather than treated as solved by conditioning. Comparisons may describe or stratify observed pitch/register and dynamics where available, but the recording or source group, not the frame row, is the replication unit. Held-out splits must be fixed in manifests before any optimization work.

Potential confounds must be recorded rather than inferred away: unknown and time-varying recording level, unmatched pitch/register, unknown bass identity, microphone, placement, room, recording chain, processing, strings, take conditions, and segmentation quality. The player label may be known while the other contextual fields remain unknown; recordings from the same album or player must not be assumed to share them. Frame rows remain useful for describing within-recording distributions, but overlapping or adjacent frames from one recording are correlated and must not be counted as independent replication. A difference is strong only when it repeats across recordings or source groups and remains unresolved or qualified when those units are sparse. Global gain normalization cannot reconstruct an unknown or drifting recording level. Small or unbalanced corpora should produce an unresolved result, not a significance claim.

## Reproducibility

Manifests are explicit; original audio is not modified or manually split for convenience. If long-file processing is later streamed in internal chunks, chunks must preserve frame/hop continuity, event context, and overlap behavior so results match whole-file processing. Outputs retain source hashes, feature version, Python/platform information, UTC generation time, and Git commit when available. Experiment configuration and corpus split belong in version control; licensed audio remains outside the repository.
