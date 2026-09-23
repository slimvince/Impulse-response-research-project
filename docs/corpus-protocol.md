# Corpus Protocol

This document specifies how recordings should be captured, labeled, checked, and admitted to the research corpus. It is separate from [corpus.md](corpus.md), which catalogs recordings that actually exist.

## Recording goals

Capture SLB-200 DI and acoustic double-bass microphone material that can be compared through the same analysis pipeline. Prefer controlled, repeated material while retaining enough natural variation to test generalization.

## Required capture metadata

For every recording, record:

- stable recording ID;
- domain: `slb_di` or `acoustic_mic`;
- player ID and instrument ID;
- articulation and material identity;
- intended pitch/register and dynamic level;
- sample rate, bit depth, channel count, and file format;
- gain settings and calibration reference where available;
- for acoustic recordings: microphone model, polar pattern, placement, preamp/interface, room, and take conditions;
- for SLB recordings: pickup/DI path, instrument setup, strings if known, and take conditions;
- date, operator, and source/license status;
- development or held-out split assignment.

Unknown values must be recorded as unknown, not guessed.

## Capture protocol

1. Preserve original files without destructive normalization, denoising, EQ, compression, or trimming.
2. Record clean takes and any calibration/reference signal separately.
3. Use consistent sample rate and bit depth within a comparison set where practical.
4. Record repeated notes across low, middle, and high registers.
5. Record multiple dynamics, note durations, attacks, sustains, decays, and representative phrases.
6. Repeat selected material across players and instruments.
7. Document room and microphone placement with enough detail to reproduce the setup.
8. Preserve the original filename and calculate a source hash at ingestion.

## Ingestion checks

A recording may enter the approved corpus only after:

- the file opens and metadata is readable;
- the source hash is recorded;
- clipping, silence, corruption, and unexpected channel layout are checked;
- license or permission is documented;
- metadata completeness is reviewed;
- domain and split are assigned;
- exclusions or quality concerns are recorded.

## Split policy

Assign development, validation, and held-out status using recording identity, player, instrument, and take boundaries that prevent leakage. Freeze the relevant manifest before optimization or target-selection experiments. A transformed version of a development recording is not an independent held-out recording.

## Normalization policy

Never replace the original. Any gain normalization must be a named derived view with explicit parameters. Reports should distinguish level-matched comparisons from original-level comparisons because level itself may interact with the measured feature.
