# E018: Full-Length FIR Trials on SLB-200 Recording Two

## Source

- File: `C:\IR audio\slb200\recording two slices\yamaha bass slb200.wav`
- SHA-256: `c00f60b0e6777171a03f69441083b2b47f90d34e27057c036a660e9eaffb4e08`
- Stereo, 44.1 kHz, 16-bit PCM; duration 362.00 s.
- The user identifies this as the unsliced SLB-200 recording “two.” The 135 Cubase `Audio 02 -*` slice durations sum to 360.00 s, consistent with this source, but waveform-level mapping has not been verified.

## Processing

Applied the existing E014 and E016 8,192-tap candidate filters to both channels of the full source using block overlap-add. The original source was not modified. For each filter, both a raw render and a whole-file RMS-matched comparison render were produced. No safety attenuation was needed.

- E014 whole-file RMS matching required +4.88 dB.
- E016 whole-file RMS matching required +4.51 dB.
- Full render length is 362.186 s, including the FIR tail.

## Audition

[Open the A/B/C/D comparison page](listening/ab_compare.html).

The page offers dry, E014 raw/matched, and E016 raw/matched playback, switching at the same timeline position. Full-length listening can reveal perceptual differences but does not validate acoustic similarity by itself.

## Limitations

- E014 and E016 were fitted using 24 listener-confirmed events from `vincents 1.wav` and provisional acoustic candidate slices; they were not fitted specifically to recording two.
- The acoustic slice validator is uncalibrated, and capture metadata remain incomplete.
- E014/E016 are spectral-shape research candidates, not physically identified room/microphone responses or validated acoustic-bass emulators.
- E016 did not outperform E014 on the reported aggregate median-profile metrics; the E018 renders are new source applications, not evidence that this changes.
