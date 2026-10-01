# E014: Candidate SLB-200 to Acoustic Spectral-Shape Transform

## Status

Exploratory render generated for listening. It is **not** a validated acoustic-bass emulator or a uniquely identified physical IR.

## Data used

- SLB input: full `C:\IR audio\slb200\vincents 1.wav` (SHA-256 in `manifest.json`).
- SLB reference population: 24 `Use` intervals from the user's E008 listener CSV on this same take.
- Acoustic training population: E013 provisional accepts from bass A takes 2 and 3 (327 + 332 slices; equal weight by slice-set profile).
- Held-out acoustic population: E013 provisional accepts from bass B take 3 (195 slices).
- All acoustic candidate slices have unknown microphone/placement/room/recording-chain details and lack human labels. They are not a controlled paired target.

## Method

For each selected event, compute a unit-total-power spectrum from Hann-windowed 4096-sample frames with 2048-sample hop and 8192-point FFT. Average events within each acoustic slice set, then equal-weight the two training set profiles. Derive a smoothed target/source spectral ratio, normalize away absolute gain in 100-1000 Hz, cap the EQ at +/-6 dB, and construct an 8192-tap minimum-phase FIR candidate. Apply the same filter to both stereo channels of the complete SLB source; preserve the original and do not loudness-normalize the result. A small peak-protection attenuation is recorded if required.

## Held-out check

On normalized third-octave spectral shape over 40-8000 Hz, the mean absolute difference from the held-out bass B candidate profile was **9.10 dB before** and **9.20 dB after**. This is a slight regression on this coarse spectral metric. Therefore, the candidate filter is **not supported as an improvement by the held-out statistic**; audition is exploratory and may reveal perceptual effects not captured by this metric.

## Limitations

- The acoustic candidates are Cubase-generated and E013 validator-accepted, but not human-labeled; E013 thresholds remain uncalibrated.
- The SLB reference is one recording/take and 24 selected listener-Use events; accepted Cubase SLB candidates had poor low-register coverage and were not used as the primary reference.
- Acoustic source groups have unknown recording chains and are unpaired with the SLB performance.
- Equalized average magnitude does not recover phase, room impulse, microphone response, or event correspondence. Minimum phase is an engineering assumption.
- No precision/recall, perceptual validation, or generalization claim is established.

## Outputs

- `results/candidate_minimum_phase_fir.npz`: 8192-tap filter and spectral ratio.
- `results/candidate_profile.json`: training/holdout counts, gain curve, metric, and limitations.
- `results/render_metadata.json`: hashes and full-render details.
- Full rendered WAV: `C:\IR audio\results\E014\vincents_1_candidate_acoustic_EQ_E014.wav`.
- Audition copies: [dry full recording](listening/vincents_1_dry_reference.wav) and [candidate transformed full recording](listening/vincents_1_candidate_acoustic_EQ_E014.wav). These are untracked audition conveniences; authoritative source/render stay outside Git.
