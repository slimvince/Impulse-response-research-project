# E003: Minimal note-ground-truth benchmark

## Purpose

Create a small manually reviewed ground-truth set for note segmentation on the acoustic candidate recordings. The benchmark is intended to answer one concrete question:

> Can candidate event detectors reliably separate the observed plucks into individual notes with acceptable onset and offset boundaries?

This is a benchmark gate, not a final scientific conclusion.

## Ground-truth format

Each excerpt should be labeled as a short sequence of notes. Record the approximate note onset and offset times in seconds, together with a confidence score and notes about ambiguity.

## Recommended initial subset

Use a compact set of 3-5 short excerpts from the current acoustic candidate recordings, covering:

- one low-register example;
- one mid-register example;
- one broader or harder example;
- a couple of note sequences with clear pitch changes.

## Required fields

For each note entry in the labels table:

- `excerpt_id`: short identifier for the excerpt;
- `note_index`: sequential note number within the excerpt;
- `start_s`: onset time in seconds;
- `end_s`: offset time in seconds;
- `pitch_hint`: optional approximate pitch class or register label;
- `confidence`: `1` = very confident, `2` = moderate, `3` = uncertain;
- `notes`: short comment describing ambiguity, attack, or overlap.

## Example

```csv
excerpt_id,note_index,start_s,end_s,pitch_hint,confidence,notes
low_01,1,0.00,0.18,low,1,clear attack and note decay
low_01,2,0.22,0.40,low,1,distinct pitch change
low_01,3,0.45,0.62,low,1,clear next note
```

## How to use it

1. Listen to each selected excerpt.
2. Mark the note start and end times by ear.
3. Write the note boundaries into a CSV or JSON file.
4. Use the same ground-truth to compare candidate detectors.
5. Score split, merge, missed-note, and boundary error rates.

## First-pass evaluator

Run the reproducible comparison from the repository root:

```powershell
python experiments/E003/evaluate_benchmark.py
```

The evaluator writes `benchmark_results.json` and compares the detector's ordered events with the reviewed labels for five frame, hop, and threshold settings. It reports note-count misses and extras plus mean onset and offset errors. Because the current labels are approximate and the first pass matches events by time order, these results are screening evidence for parameter selection, not a final segmentation claim.

The boundary-aware classifications in `benchmark_results.json` are also provisional. The current labels were entered by ear with approximate times, so the evaluator uses ordered onset error for triage and does not treat approximate decay ends as authoritative boundaries. It can still flag an event you consider musically acceptable; final usability disqualification requires more precise onset labels or listener review.

The current listener-reviewed usability authority is `listener_audit.csv`. It records the human decision for each exported event without deleting any output. Use these labels to evaluate the automated triage rules; do not replace them with approximate timing scores.

## First benchmark result

The best tested setting by note-count agreement is `frame_size=256`, `hop_size=64`, `threshold_db=-45`. It produced counts of `3/3`, `3/3`, `3/3`, and `3/5` for `low_02_low.wav`, `bass_friendly_01_bass_friendly.wav`, `broad_03_broad.wav`, and `low_01_low.wav`, respectively. Its total absolute count error is `2`, compared with `6` for `128/32/-38` and `25` or more for the other tested settings.

This is an improvement in count stability, not proof of reliable note segmentation. The remaining failure is a merge in `low_01_low.wav`, and boundary errors remain subject to the approximate manual labels. The next experiment should target that five-note excerpt and test whether pitch-aware splitting can separate its two merged regions without reintroducing short artifacts.

## Targeted split-limit probe

A probe that raised the maximum number of pitch-based split points from two to four was rejected. At `256/64/-45`, it changed the counts from `3/3/3/3` to `5/5/5/5` against references `3/3/3/5`, creating false splits in the first three excerpts. The validated two-split limit remains in place until a more selective rule is tested.

## Current rule

This benchmark is the shared reference set. It is the ground truth for detector comparison. Auditioning is the method used to create it.

## Analysis versus audition files

The benchmark and detector exporters analyze the original WAV excerpts under `experiments/E002/listener_slices`. Audition links under `experiments/E003/detected_slices` are raw sample slices at the detector's exact boundaries: no fades, context, normalization, or other postprocessing is applied. A click at a hard boundary is therefore part of the raw cut and should not be mistaken for audio content.
