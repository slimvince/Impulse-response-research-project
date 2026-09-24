# Event-slice listening review

Use this pass as a quick sanity check for split/merge and boundary errors. It is a triage step, not a replacement for the quantitative benchmark.

## Label options

- `single note`: a clean, single note-like event
- `split`: the slice contains a single note that was falsely split into multiple events
- `merged`: two notes have been merged together into one event
- `missing/uncertain`: the note is not clear or the event should not be trusted
- `ambiguous legato`: two notes are connected and boundary detection is uncertain

## Quick instructions

1. Play each slice once without looking at the detector output.
2. Decide whether the slice is one note or more than one note.
3. If it is split or merged, note which setting seems most responsible.
4. Keep a confidence score: `1 = very confident`, `2 = somewhat confident`, `3 = uncertain`.
5. Flag the worst 3-5 cases for a future ground-truth subset.

## Candidate slices

| ID | Setting | File | Why it is included |
|---|---|---|---|
| low_01 | low | [listener_slices/low_01_low.wav](listener_slices/low_01_low.wav) | likely sustained note; good split/merge check |
| low_02 | low | [listener_slices/low_02_low.wav](listener_slices/low_02_low.wav) | lower-register note near the conservative cut-off |
| mid_01 | mid | [listener_slices/mid_01_mid.wav](listener_slices/mid_01_mid.wav) | short event; likely false split or legitimate brief note |
| mid_02 | mid | [listener_slices/mid_02_mid.wav](listener_slices/mid_02_mid.wav) | long event that may show merge/boundary drift |
| bass_friendly_01 | bass_friendly | [listener_slices/bass_friendly_01_bass_friendly.wav](listener_slices/bass_friendly_01_bass_friendly.wav) | baseline candidate for comparing settings |
| broad_01 | broad | [listener_slices/broad_01_broad.wav](listener_slices/broad_01_broad.wav) | likely false-positive or short extra note |
| broad_02 | broad | [listener_slices/broad_02_broad.wav](listener_slices/broad_02_broad.wav) | short broad-range event; good split-vs-merge judge |
| broad_03 | broad | [listener_slices/broad_03_broad.wav](listener_slices/broad_03_broad.wav) | overlap/boundary-drift case |

## Sample review row

Use a row like this while listening:

- slice ID:
- verdict: single note / split / merged / missing/uncertain / ambiguous legato
- confidence: 1 / 2 / 3
- notes: what looked wrong (boundary, extra event, missed note, etc.)

## Interpretation rule

Do not treat the audition pass as proof of correctness. It is only a way to identify obvious failure modes and to decide which candidate events deserve manual annotation for the next benchmark set.
