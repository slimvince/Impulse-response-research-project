# E015: Per-Slice Dry/Filtered Feedback Comparison

## Purpose

Map Cubase `vincents 1-*` slice WAVs back to the unsplit source, then compare per-slice features from the same time intervals in the dry source and full-file E014 render. Separately compare those SLB populations with E013 acoustic candidate slices conditioned by estimated register and acoustic-training level terciles.

## Source-time mapping

`results/source_time_map.json` and `.csv` use normalized waveform cross-correlation against `C:\IR audio\slb200\vincents 1.wav`. Only high-correlation, unique matches are mapped. Of the 363 SLB Cubase slices, 160 mapped, 49 were ambiguous, 150 were unmatchable silence, and 4 were too short/low-energy to map. Median correlation among mapped slices was approximately 1.0. Unmatched candidates remain excluded rather than receiving guessed source times.

## Comparison populations

- Paired dry/filtered Cubase SLB candidates: 33 E013 provisional accepts among the mapped slices. These are highly selected and concentrated in high register/low level.
- Listener-confirmed SLB diagnostic set: 24 E008 `Use` intervals, extracted at identical source times from dry and filtered full files. These intervals were used in E014 filter estimation, so this is an in-sample SLB diagnostic, not an independent SLB test.
- Acoustic reference: E013 provisional accepts from bass A2/A3 for training-profile comparison and bass B3 held out by slice set. Candidate acceptance remains uncalibrated and acoustic metadata are incomplete.

## Observations

- The 33 mapped Cubase validator-accepted SLB slices were all high-register/low-level by the current estimators. Their full-group normalized third-octave MAE was 11.11→12.13 dB against acoustic training and 9.17→10.44 dB against held-out B3, i.e. worse overall. In the high/low cell (33 SLB, 21 train, 11 holdout), MAE changed 9.96→7.77 dB against train and 7.03→6.93 dB against holdout.
- For the 24 listener-confirmed E008 Use intervals, the mean of per-event normalized spectral-shape profiles moved from 7.40→4.11 dB MAE against acoustic training and 7.34→4.21 dB against held-out B3. Register/level cell counts are sparse (16 low/low, 6 mid/low, one low/mid, one high/low).
- The two aggregate metrics do not agree. E014's pooled-power estimate and E015's mean per-event log-shape measure different quantities; slice selection also differs. This is evidence that aggregate scoring and selected populations materially affect the result, not proof of a robust perceptual improvement.
- Across the 33 mapped accepted SLB slices, median spectral-centroid shift was +40.8 Hz, median level shift -2.85 dB, and median f0 shift 0 Hz. Only 1/33 became closer by the per-slice training-profile distance used here.

## Limitations

- Acoustic candidate slices are not human-labeled; E013 accept is a heuristic triage result.
- Acoustic and SLB events are unpaired. Register/level bins do not control player, instrument, microphone, room, placement, or chain.
- The 24 human-confirmed SLB Use intervals are in-sample for E014 filter estimation.
- Only 160/363 Cubase SLB slice times mapped uniquely; unmatched cases were excluded.
- Feature profiles describe spectral shape; they do not evaluate transient perception, phase, note decay fidelity, or full-piece listener preference.
- E014's held-out acoustic metric slightly worsened. Do not call this candidate a successful acoustic-bass emulator.

## Outputs

- `results/source_time_map.json` / `.csv`: Cubase-to-source time matches and correlation confidence.
- `results/per_slice_features.csv`: dry/filtered SLB and acoustic candidate measurements.
- `results/accepted_mapped_slb_feedback.csv`: per-slice feedback for the 33 mapped provisional SLB accepts.
- `results/per_slice_comparison.json`: conditional and aggregate metrics.
