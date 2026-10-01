# E016: Per-Event Median Spectral-Shape FIR Alternative

## Purpose

E016 tests one predeclared alternative to E014: fit a shared spectral-shape filter using the median per-event normalized third-octave log spectrum rather than a ratio of pooled linear-power profiles. E014 is preserved as the baseline. B3 was used only as a diagnostic set because it was already examined in E014/E015; no repeated tuning on it was performed.

## Data

- 24 listener-confirmed E008 `Use` intervals from the full SLB take (also used in filter estimation; source-side comparison is in-sample).
- Acoustic training: 327 accepted E013 slices from bass A take 2 and 332 from bass A take 3.
- Acoustic diagnostic set: 195 accepted E013 slices from bass B take 3. These are validator accepts, not human-labeled events, and B3 is not an untouched test after E014/E015.

## Filter

Per-event spectra are normalized to unit power. The target/source median log-profile difference is centered to zero median gain over 100-1000 Hz, smoothed with `[1,2,3,2,1]`, capped at +/-6 dB, converted to an 8192-tap minimum-phase FIR, and applied to both channels of the complete SLB recording. Whole-file RMS-matched audition copies are provided alongside the raw E016 render and E014 RMS-matched baseline. The source is unchanged.

## Results

Using median-profile MAE over 40-8000 Hz:

- Dry to acoustic training median: **7.52 dB**.
- E014 candidate to training median: **6.94 dB**.
- E016 candidate to training median: **7.55 dB**.
- Dry to previously inspected B3 diagnostic median: **8.23 dB**.
- E014 to B3 diagnostic median: **8.98 dB**.
- E016 to B3 diagnostic median: **9.58 dB**.

A separate per-event distance summary found E016 closer on 45.8% of the 24 listener-confirmed source events and a slightly lower median distance than E014 (10.02 vs 10.38 dB). These metrics disagree: aggregate median profiles favor E014; per-event median-distance favors E016 slightly but remains below half the events. This is mixed/negative evidence, not a basis to replace E014.

## Audition

[Open the A/B comparison page](listening/ab_compare.html). The options are dry, E014 whole-file RMS-matched, E016 raw, and E016 whole-file RMS-matched.

## Limits

The E013 acoustic validator is uncalibrated; the accepted acoustic slices have no human labels. The source SLB events are used to fit the filters. Acoustic capture metadata are unknown and the events are unpaired. The held-out-like B3 slice set has already been inspected in earlier experiments, so it is diagnostic rather than untouched test data. Neither candidate is a validated acoustic emulator or a uniquely identified physical room/microphone IR.
