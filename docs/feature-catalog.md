# Feature Catalog

This catalog distinguishes **implemented exploratory measurements** from planned candidates. A feature being listed does not mean it is relevant to the eventual transformation.

## Status vocabulary

- `implemented`: available in the current package.
- `candidate`: intended for the broad exploratory bank.
- `deferred`: requires more corpus metadata, validation, or a dependency decision.
- `rejected`: not currently justified; record the reason.

## Current features

| ID | Scope | Measurement | Units | Status | Role | Main risks |
|---|---|---|---|---|---|---|
| LVL-RMS | frame | Root-mean-square amplitude | dB | implemented | level/control | gain and calibration |
| LVL-PEAK | frame | Maximum absolute sample amplitude | dB | implemented | level/control | transient sensitivity |
| PIT-F0-AUTOCORR | frame | Autocorrelation lag estimate | Hz | implemented | pitch/register control | octave errors, noisy frames |
| SPEC-CENTROID | frame | Power-weighted frequency mean | Hz | implemented | candidate descriptor | level/noise/window sensitivity |
| SPEC-ROLLOFF85 | frame | Frequency below 85% cumulative power | Hz | implemented | candidate descriptor | threshold/window sensitivity |
| SPEC-FLUX | frame | Frame-to-frame magnitude change | relative | implemented | attack/evolution descriptor | normalization and hop dependence |
| HARM-PROXY | frame | Largest non-DC bin relative to total power | dB | implemented | exploratory proxy | not a true harmonicity measure |
| BAND-* | frame | Broad frequency-band power | dB | implemented | exploratory descriptor | band definitions and sample rate |
| EVT-START/END | event | Threshold active-region boundaries | s | implemented | segmentation | threshold and noise floor |
| EVT-DURATION | event | Event end minus start | s | implemented | temporal descriptor | segmentation |
| EVT-PEAK | event | Peak time and level | s/dB | implemented | temporal descriptor | transient and threshold behavior |
| EVT-ATTACK | event | Start to peak time | s | implemented | attack descriptor | peak definition |
| EVT-SUSTAIN | event | Median late-event level | dB | implemented | sustain descriptor | arbitrary phase definition |
| EVT-DECAY | event | Simple late-event level slope | dB/s | implemented | decay descriptor | noisy tails and segmentation |

## Candidate expansion

These should be added when they are readily available through an open-source library or modest reference implementation and can be defined and tested reproducibly. Availability makes a descriptor eligible for the exploratory bank; it does not establish relevance or justify using it as an optimization target.

### Spectrum and envelope

- Spectral slope and regression residual
- Spectral spread, skewness, and kurtosis
- Smoothed spectral envelope at fixed or f0-relative frequencies
- Spectral peaks, dips, prominence, and bandwidth
- Frequency-band ratios rather than only absolute energy
- Time-varying envelope trajectories through attack, sustain, and decay

### Harmonics and periodicity

- Harmonic frequencies and amplitudes relative to f0
- H1/H2 and adjacent harmonic ratios
- Harmonic rolloff
- Harmonic-to-noise ratio with a documented estimator
- Inharmonicity
- Periodicity and f0 confidence

### Temporal and dynamics

- Loudness-normalized amplitude envelope
- Attack slope and curvature
- Sustain modulation and decay curvature
- Crest factor and dynamic range
- Event-to-event timing and level consistency

### Controls and metadata

- Pitch/register and f0 confidence
- Loudness/dynamic level
- Note duration and articulation
- Player, instrument, microphone, placement, room, and recording-chain identifiers
- Temporal phase labels: attack, sustain, decay

## Evaluation rule

For every candidate, record definition, units, valid range, required inputs, synthetic tests, missing-value behavior, sensitivity to analysis parameters, and whether it adds information beyond existing features. Relevance is assessed from recording-level repeatability, conditional domain differences, redundancy, and confound sensitivity.
