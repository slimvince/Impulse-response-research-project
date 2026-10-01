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

As of 2026-09-28, `C:\IR audio\slb200\` also contains 498 Cubase-produced candidate slice files across two slice sets (see "Cubase-produced SLB-200 candidate slices" below) that were added directly to the external audio directory outside of any experiment run. They are unvalidated Cubase candidates, not corpus-approved events.

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
| slb200_recording_two_take_1 | `C:\IR audio\slb200\recording two slices\yamaha bass slb200.wav` | slb200_recording_two_unknown_source | `c00f60b0e6777171a03f69441083b2b47f90d34e27057c036a660e9eaffb4e08` | stereo 44.1 kHz 16-bit PCM WAV | 362.00 s | candidate |

The extraction manifest is outside Git at `C:\IR audio\acoustic-repeatability-manifest.json`; generated outputs are under `C:\IR audio\results\acoustic-repeatability`. The current pipeline extracted 47,055 frames and 105 events from the four files. Its existing domain summary does not yet calculate within-group repeatability statistics.

Permission basis: user-confirmed free-to-use audio, recorded in the external manifest as `user_confirmed_free_to_use`. This is a project provenance statement, not an independent legal review.

The SLB-200 file is user-provided and remains a candidate pending contextual metadata and permission-status confirmation. Player, instrument setup, strings, pickup/DI path, gain, articulation coverage, and take conditions are currently unknown.

### Cubase-produced candidate slices

These are physical audio files exported from Cubase Pro 15 using the workflow in `docs/cubase-slicing-workflow.md` (Hitpoints → Create Slices → Dissolve Part → Event/Range as Region → Bounce Selection). They are Cubase candidate slices, not validated events — see `docs/decisions.md` 2026-09-28 ("Cubase Hitpoints as a fast candidate-event generator, not ground truth"). E012 has run an initial uncalibrated validator pass; no candidate slice has a human reference label yet, and no precision/recall claim is available. E008-E011 triage the recursive detector's own output on `vincents 1.wav`, not these Cubase files.

| Slice set | External path | Count | Format | Duration range | Source recording |
|---|---|---:|---|---|---|
| `slb200_vincents_take_1_cubase_slices` | `C:\IR audio\slb200\vincents 1-00.wav` … `vincents 1-362.wav` | 363 | stereo 44.1 kHz 24-bit PCM WAV | 0.050 s – 4.274 s (mean 0.78 s) | `slb200_vincents_take_1` (`vincents 1.wav`) |
| `slb200_audio02_cubase_slices` | `C:\IR audio\slb200\recording two slices\Audio 02 - 1.wav` … `Audio 02 - 135.wav` | 135 | mono 44.1 kHz 16-bit PCM WAV | 0.073 s – 5.066 s (mean 2.67 s) | user identifies `slb200_recording_two_take_1` as the unsplit source; waveform alignment not yet verified |
| `acoustic_bass_a_take_2_cubase_slices` | `C:\IR audio\acoustic\bass A\2 sliced\` | 1,204 | stereo 44.1 kHz 16-bit PCM WAV | 0.034 s – 10.151 s | `acoustic_bass_a_take_2` (`bass A\2.wav`) |
| `acoustic_bass_a_take_3_cubase_slices` | `C:\IR audio\acoustic\bass A\3 sliced\` | 689 | stereo 44.1 kHz 16-bit PCM WAV | 0.056 s – 9.910 s | `acoustic_bass_a_take_3` (`bass A\3.wav`) |
| `acoustic_bass_b_take_1_cubase_slices` | `C:\IR audio\acoustic\bass B\3 split\` | 1,363 | stereo 44.1 kHz 16-bit PCM WAV | 0.023 s – 7.578 s | `acoustic_bass_b_take_1` (`bass B\3.wav`) |

Per-file SHA-256 hashes and format/duration/size for the original 498 SLB slices are pinned in `C:\IR audio\slb200-cubase-slices-manifest.json` (generated 2026-09-28), keyed by `slice_set_id`. At manifest creation time the `Audio 02` slices were the only surviving files from that take; the user has since added a likely unsplit source, documented below. Recompute and diff hashes before trusting any later copy of these slices.

The three additional acoustic slice sets are enumerated separately in E013; their observed hashes are recorded in `experiments/E013/results/candidate_validation.json`. E013 does not modify the external 498-file manifest. The combined current Cubase candidate inventory is 3,754 files.

Open items, recorded rather than resolved:

- **Bit-depth mismatch:** the `vincents 1-*.wav` slices are 24-bit, but their stated source `vincents 1.wav` is 16-bit (confirmed by direct inspection, hash `138b5de9...`). Cubase's slice/bounce path appears to upconvert bit depth on export. This means slice bytes are not a raw sub-extraction of the original file at matching bit depth; do not assume byte-for-byte equivalence when cross-checking a slice against the original.
- **`Audio 02` source is now available.** The user identifies `C:\IR audio\slb200\recording two slices\yamaha bass slb200.wav` as the unsplit “recording two.” It is stereo 44.1 kHz 16-bit PCM WAV, 362.00 s, SHA-256 `c00f60b0e6777171a03f69441083b2b47f90d34e27057c036a660e9eaffb4e08`. The 135 Cubase slice durations sum to 360.00 s, consistent with this source; exact waveform alignment has not yet been verified. The external Cubase manifest still records `source_recording: null` because it predates this upload; E018 records the current user-supplied association. Player/take/session metadata remain unknown.
- Neither slice set has Cubase-side provenance metadata (hitpoint sensitivity, export settings, take date/session) the way `slb200-manifest.json` documents contextual metadata for the unsplit take. If these slices are promoted beyond `candidate` status, that metadata gap should be closed first — the new manifest covers file integrity only, not recording context.

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
