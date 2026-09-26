# Corpus Catalogue

This document describes the actual data available to the project. It is different from the corpus-protocol requirements and from per-experiment manifests.

## Corpus rules

- Original audio remains outside Git unless redistribution is explicitly licensed.
- Every usable recording receives a stable recording ID.
- Each recording has provenance, license/permission status, source hash, sample metadata, domain, split, and capture metadata where known.
- Exclusions are recorded with a reason rather than silently omitted.
- Development and held-out partitions are fixed before optimization experiments.

## Current inventory

No audio recordings are stored in the repository. Nine external candidate recordings are now available for a preliminary acoustic repeatability baseline. The user has confirmed that they are free to use. They remain candidate entries because that permission statement and full capture metadata have not yet been formalized as complete corpus approval records.

### Candidate acoustic repeatability inputs

The source-group labels below are user-provided. Recordings within each group are expected to be similar and are intended to estimate within-source noise and uncertainty. The player is the known contextual label; bass identity, room, microphone, placement, recording chain, processing, strings, and take conditions are unknown unless separately documented. The two groups are different bass/player sources and are not treated as repeatability pairs with each other.

| Recording ID | External path | Source group | SHA-256 | Format | Duration | Status |
|---|---|---|---|---|---:|---|
| acoustic_bass_a_take_1 | `C:\IR audio\acoustic\bass A\1.wav` | bass A | `e6071462ce5d89f7946f26ee437e5aff13071df1b4d60023fbb755c0c6fc2d3a` | stereo 44.1 kHz 16-bit PCM WAV | 287.58 s | candidate |
| acoustic_bass_a_take_2 | `C:\IR audio\acoustic\bass A\2.wav` | bass A | `588bf4876bb39c2fef26f85ec23e203d0c3857f1a817c8250ac2f013770f7408` | stereo 44.1 kHz 16-bit PCM WAV | 295.01 s | candidate |
| acoustic_bass_a_take_3 | `C:\IR audio\acoustic\bass A\3.wav` | bass A | `4835fdfbf9b52c6717b1c44fe4a02d9b3f3b8c29138168f91ebdc269e7907f31` | stereo 44.1 kHz 16-bit PCM WAV | 386.87 s | candidate |
| acoustic_bass_a_take_4 | `C:\IR audio\acoustic\bass A\4.wav` | bass A | `1d5fd4b5947af779c78726031a20946aefad89934fa2b85ab34ada414eebc4e7` | stereo 44.1 kHz 16-bit PCM WAV | 261.77 s | candidate |
| acoustic_bass_a_take_5 | `C:\IR audio\acoustic\bass A\5.wav` | bass A | `d282d09aa86bddb9002af1c522a767b64ca2133bb433713196c70c626aaa0800` | stereo 44.1 kHz 16-bit PCM WAV | 204.60 s | candidate |
| acoustic_bass_b_take_1 | `C:\IR audio\acoustic\bass B\3.wav` | bass B | `2b447de8fb902b83530497882c170f6a9a4f537636e0599de15f2bcd7b4452f6` | stereo 44.1 kHz 16-bit PCM WAV | 292.05 s | candidate |
| acoustic_bass_b_take_2 | `C:\IR audio\acoustic\bass B\4.wav` | bass B | `02c3bbc109c125f9dc8826383cfda80286ff192f1bfba244adbfba4a59939bf` | stereo 44.1 kHz 16-bit PCM WAV | 218.29 s | candidate |
| acoustic_bass_c_take_1 | `C:\IR audio\acoustic\bass C\5.wav` | bass C | `fc8b93807bc8e33e5da50e6691b884d844aec72e97bbcf55fb6befcbfa8c6c7f` | stereo 44.1 kHz 16-bit PCM WAV | 48.16 s | candidate |
| acoustic_bass_d_take_1 | `C:\IR audio\acoustic\bass D\1.wav` | bass D | `47752e8583fead843c283f2083cfa47f8c85d975d58f1268e3f3ceca9e2bf97d` | stereo 44.1 kHz 16-bit PCM WAV | 8.72 s | candidate |

### Candidate SLB-200 input

| Recording ID | External path | Source group | SHA-256 | Format | Duration | Status |
|---|---|---|---|---|---:|---|
| slb200_vincents_take_1 | `C:\IR audio\slb200\vincents 1.wav` | slb200_vincents | `138b5de97de26392c368c01e98c3804fcf040501cd35526f618239f7c82fd46e` | stereo 44.1 kHz 16-bit PCM WAV | 284.00 s | candidate |

The extraction manifest is outside Git at `C:\IR audio\acoustic-repeatability-manifest.json`; generated outputs are under `C:\IR audio\results\acoustic-repeatability`. The current pipeline extracted 47,055 frames and 105 events from the four files. Its existing domain summary does not yet calculate within-group repeatability statistics.

Permission basis: user-confirmed free-to-use audio, recorded in the external manifest as `user_confirmed_free_to_use`. This is a project provenance statement, not an independent legal review.

The SLB-200 file is user-provided and remains a candidate pending contextual metadata and permission-status confirmation. Player, instrument setup, strings, pickup/DI path, gain, articulation coverage, and take conditions are currently unknown.

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
