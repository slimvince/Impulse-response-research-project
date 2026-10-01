# E017: Stratified Cubase Candidate Human Audit

## Purpose

Create a small, auditable human-reference subset for calibrating E012/E013 validator rules. Cubase boundaries remain candidate events, not ground truth. The validator suggestion is shown as context only; the reviewer supplies event-validity and reason labels.

## Sample

- 50 candidate slices total: 10 from each of the five Cubase slice sets.
- Fixed random seed: `20261001`.
- Within each set, target strata are 2 provisional accepts, 2 possible internal-attack flags, 2 possible tail/boundary flags, 1 short/low/edge flag, 1 hard reject QC example if available, and 2 additional uncertain examples. Empty strata are recorded and replaced with remaining uncertain examples.
- The `Audio 02` set has no hard rejects, so its QC slot is replaced by an uncertain candidate.
- Candidate files are exact copies of E013 input WAV bytes; hashes were verified during sample generation. Original files are untouched.
- The Audio 02 source `C:\IR audio\slb200\recording two slices\yamaha bass slb200.wav` is now available and is associated by the user with that Cubase slice set. Its 362 s duration is consistent with the 135 slices totaling 360 s, but waveform alignment is unverified; the review UI therefore does not show an allegedly aligned source window.

Audit progress on 2026-10-01: **21/50** judged (16 usable, 5 unusable), across bass A takes 2/3 and bass B take 3. These judgments currently have no reason code, confidence value, or free-text note. The latest durable snapshot and joined CSV are `results/browser_review_snapshot_latest.json` and `results/human_labels_partial_latest.csv`; the earlier 8-judgment snapshot is retained as a historical checkpoint. Browser state may advance beyond the latest snapshot; capture it again before analysis or handoff.

## Review labels

For each candidate, record:

- Event validity: `usable`, `unusable`, or `uncertain`.
- One or more reasons: clean isolated excitation, silence, unpitched noise, multiple sequential excitations, possible overlap/polyphony, missing/late onset, truncated tail, neighbor bleed, low SNR, clipping/artifact, or other.
- F0 feature reliability separately from event validity.
- Judgment confidence (1 high, 2 medium, 3 low) and an optional note.

Bowed-note detection/classification remains out of scope. The GUI state is local to this browser under `cubase-validator-e017-v1`; use its Export CSV control to create a durable label artifact before relying on the judgments in another environment.

## Files

- `manifest.json`: deterministic 50-slice selection, validator suggestions, sampling strata, and original hashes.
- `prepare_audit.py`: recreates exact slice copies and manifest using the fixed seed.
- `audit_slices/`: copied candidates for browser playback.
- `review.html`: review interface with independent E017 storage and CSV export.
- `results/browser_review_snapshot_2026-10-01.json`: earlier 8-judgment checkpoint.
- `results/browser_review_snapshot_latest.json` and `results/human_labels_partial_latest.csv`: latest 21-judgment checkpoint.
- `export_review_snapshot.py`: joins a captured browser-state snapshot to sample metadata for durable analysis.

## Interpretation

This is an initial calibration sample, not a representative prevalence estimate. Use it to inspect false positives and false negatives by validator stratum. Do not tune on all 50 and report performance on the same 50; reserve a source-group/set-level holdout or collect a later independent labeled sample before claiming precision/recall.
