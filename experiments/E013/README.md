# E013: Expanded Cubase Candidate Validator Pass

E013 extends the E012 provisional validator pass to all five currently identified Cubase candidate directories. E012 remains the frozen 498-file baseline; its output is not overwritten. The validation logic and exploratory thresholds are unchanged from E012.

## Inputs

- `slb200_vincents_take_1_cubase_slices`: 363 slices, source available.
- `slb200_audio02_cubase_slices`: 135 slices, unsplit source unavailable.
- `acoustic_bass_a_take_2_cubase_slices`: 1,204 slices, source available.
- `acoustic_bass_a_take_3_cubase_slices`: 689 slices, source available.
- `acoustic_bass_b_take_1_cubase_slices`: 1,363 slices, source available.

Total expected candidates: 3,754. The pinned SHA-256 manifest covers the original 498 SLB slices. E013 records observed SHA-256 values for the additional 3,256 files in its candidate output; it does not modify the external manifest.

## First-pass outcome

The uncalibrated validator produced **921 provisional accepts, 150 hard rejects, and 2,683 uncertain** candidates across the five sets. All 150 rejects are exact/effective digital silence in the `vincents 1-*` set. The three added acoustic sets produced 879 provisional accepts and 2,377 uncertain candidates, with no hard rejects.

Most uncertainty in the longer acoustic slice sets comes from possible internal attacks/transients and tail-boundary flags. These are warnings, not proof of merged notes or truncation. The Audio 02 set has 126/135 uncertain candidates and no surviving unsplit source for cross-checking.

These are feature-rule outputs only, not human-validated decisions. Precision and recall are unknown.

## Run

```powershell
.\.venv\Scripts\python.exe experiments\E013\run_validator.py
```

## Interpretation

The outcomes are provisional diagnostic judgments, not validated accept/reject labels. No Cubase candidate has a human reference label yet. Do not claim precision/recall or treat provisional accepts as corpus-approved. See `results/summary.json` for counts by slice set and `results/candidate_validation.csv` / `candidate_validation.json` for candidate-level reasons and measurements.

Event validity, f0 feature reliability, and transformation relevance remain separate. Bowed-note classification is out of scope. The Audio 02 slice set has no unsplit source, so source-relative boundary cross-checking is unavailable.
