# Corpus Protocol

This document specifies how recordings should be captured, labeled, checked, and admitted to the research corpus. It is separate from [corpus.md](corpus.md), which catalogs recordings that actually exist.

## Recording goals

Capture SLB-200 DI and acoustic double-bass microphone material that can be compared through the same analysis pipeline. Prefer controlled, repeated material while retaining enough natural variation to test generalization.

## Capture metadata

The pipeline can always record file-level facts at ingestion, including source hash, sample rate, bit depth, channel count, duration, and format. Contextual metadata must be recorded only when reliably known. For the expected historical recordings, the player may be the only known contextual field; unknown values must remain unknown, not inferred from album or file context.

When available, record:

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

Unknown values must be recorded as unknown, not guessed. In particular, do not assume that tracks from the same album share bass, room, microphone, placement, recording chain, processing, strings, or take conditions.

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
- metadata completeness and unknown contextual fields are reviewed;
- domain and split are assigned;
- exclusions or quality concerns are recorded.

## Split policy

Assign development, validation, and held-out status using recording identity, player, instrument, and take boundaries that prevent leakage. Freeze the relevant manifest before optimization or target-selection experiments. A transformed version of a development recording is not an independent held-out recording.

## Normalization policy

Never replace the original. The absolute recording level may be unknown, and recording level may drift within a file; normalizing a file cannot recover either quantity. Any gain normalization must be a named derived view with explicit parameters and must not be described as level matching. Reports must retain original-level results and distinguish them from any relative-level or locally conditioned view because level itself may interact with the measured feature. Unknown microphone, room, chain, processing, and setup metadata remain confounds rather than reasons to invent a control.
