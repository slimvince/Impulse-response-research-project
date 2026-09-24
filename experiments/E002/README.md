# Experiment E002 - Basic Pitch event segmentation gate

## Question

Can Basic Pitch provide a trustworthy subset of note- or excitation-like events from the current acoustic corpus, with enough quality to support event-conditioned analysis?

## Status

- Status: complete
- Gate result: conditional pass

## Summary of evidence

This pilot ran the Spotify Basic Pitch detector on four 30-second acoustic excerpts, each drawn from one of the two available source groups. The repository threshold detector produced between 4 and 6 events on the same excerpts, while Basic Pitch produced 82-96 events under the default parameter set and 15-41 events under a stricter conservative parameter set.

A follow-up range sweep on one representative excerpt tested four settings: low-register (35 events), mid-range (55), bass-friendly (55), and broad-bass (88). This indicates that widening the maximum fundamental range immediately increases the event count, but the range alone does not yet establish adequacy. The low-register pass is cleaner but may miss valid upper-register notes; the broader pass may add noise or false detections. The result is not yet a validated segmentation method and still needs listener review and a small benchmark set.

The output shows that Basic Pitch is active and produces event-like structure on the actual corpus, but the event population is still too granular and ambiguous to be treated as a validated note detector without a manual benchmark. The stricter setting yields a smaller, more conservative subset that is more usable as a candidate filter, but the pilot is not yet a final scientific claim about segmentation accuracy.

## Interpretation

- Basic Pitch is operationally useful as a candidate event generator for the current acoustic corpus.
- The output still requires confidence filtering, overlap handling, and manual review before it can support event-conditioned temporal and spectral conclusions.
- The current evidence is enough to justify a conditional pass for further investigation, but not enough to claim that individual note events are already reliably segmented.

## Limitations

- No manual ground-truth set exists yet for the acoustic corpus.
- The excerpts are a small pilot subset, not a corpus-wide benchmark.
- The detector may still over-segment, merge legato notes, or mis-handle low-register or polyphonic segments.
- The observed event counts are descriptive and require held-out review before being used as scientific evidence.

## Next action

Create a small manually reviewed ground-truth subset and quantify boundary, split, merge, and missed-event error rates. Only after those metrics are set should event-conditioned analysis proceed without explicit caveats.
