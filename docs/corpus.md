# Corpus Catalogue

This document describes the actual data available to the project. It is different from the corpus-protocol requirements and from per-experiment manifests.

## Corpus rules

- Original audio remains outside Git unless redistribution is explicitly licensed.
- Every usable recording receives a stable recording ID.
- Each recording has provenance, license/permission status, source hash, sample metadata, domain, split, and capture metadata where known.
- Exclusions are recorded with a reason rather than silently omitted.
- Development and held-out partitions are fixed before optimization experiments.

## Current inventory

No audio recordings are stored in the repository. Four external candidate recordings are now available for a preliminary acoustic repeatability baseline. The user has confirmed that they are free to use. They remain candidate entries because that permission statement and full capture metadata have not yet been formalized as complete corpus approval records.

### Candidate acoustic repeatability inputs

The source-group labels below are user-provided. Recordings within each group are expected to be similar and are intended to estimate within-source noise and uncertainty. The player is the known contextual label; bass identity, room, microphone, placement, recording chain, processing, strings, and take conditions are unknown unless separately documented. The two groups are different bass/player sources and are not treated as repeatability pairs with each other.

| Recording ID | External path | Source group | SHA-256 | Format | Duration | Status |
|---|---|---|---|---|---:|---|
| acoustic_bass_a_take_1 | `C:\IR audio\acoustic\bass A\1.wav` | bass A | `e6071462ce5d89f7946f26ee437e5aff13071df1b4d60023fbb755c0c6fc2d3a` | stereo 44.1 kHz 16-bit PCM WAV | 287.58 s | candidate |
| acoustic_bass_a_take_2 | `C:\IR audio\acoustic\bass A\2.wav` | bass A | `588bf4876bb39c2fef26f85ec23e203d0c3857f1a817c8250ac2f013770f7408` | stereo 44.1 kHz 16-bit PCM WAV | 295.01 s | candidate |
| acoustic_bass_b_take_1 | `C:\IR audio\acoustic\bass B\3.wav` | bass B | `2b447de8fb902b83530497882c170f6a9a4f537636e0599de15f2bcd7b4452f6` | stereo 44.1 kHz 16-bit PCM WAV | 292.05 s | candidate |
| acoustic_bass_b_take_2 | `C:\IR audio\acoustic\bass B\4.wav` | bass B | `02c3bbc109c125f9dc8826383cfda80286ff192f1bfba244adbfba4a59939bf` | stereo 44.1 kHz 16-bit PCM WAV | 218.29 s | candidate |

The extraction manifest is outside Git at `C:\IR audio\acoustic-repeatability-manifest.json`; generated outputs are under `C:\IR audio\results\acoustic-repeatability`. The current pipeline extracted 47,055 frames and 105 events from the four files. Its existing domain summary does not yet calculate within-group repeatability statistics.

Permission basis: user-confirmed free-to-use audio, recorded in the external manifest as `user_confirmed_free_to_use`. This is a project provenance statement, not an independent legal review.

The `C:\IR audio\slb200` directory is currently empty; no SLB-200 recordings are registered.

### Planned corpus expansion

Additional recordings of bass A and bass B are expected and should be added as new takes under their existing source groups. Additional acoustic basses should receive new stable source-group identifiers rather than being merged into bass A or bass B. More takes improve within-source uncertainty estimates; new basses test whether observed characteristics generalize beyond the initial instruments and players.

## Planned domains

### SLB-200 DI

Expected metadata: recording ID, player, instrument, strings/setup where relevant, pickup/DI chain, gain, sample rate, bit depth, articulation, pitch/register, dynamic level, note/phrase identity, room if relevant, license, and split.

### Acoustic double bass microphone

Expected metadata: recording ID, player, instrument, strings/setup where relevant, microphone model, placement, preamp/interface, gain, room, sample rate, bit depth, articulation, pitch/register, dynamic level, note/phrase identity, license, and split.

## Recording status vocabulary

- `candidate`: known source not yet checked;
- `approved`: metadata and license checked;
- `excluded`: deliberately not used, with reason;
- `held_out`: reserved for validation;
- `development`: available for method development.

## Catalogue entries

Add one entry per recording only after provenance and permission have been checked. Manifests used by experiments must reference these stable IDs and preserve the source hash observed at analysis time.
