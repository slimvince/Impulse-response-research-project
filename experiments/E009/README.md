# E009: Revised SLB-200 Event Slicing

This rerun applies the corrected event detector to the same external SLB-200 source used for E008. E008 slices and browser judgments are unchanged; event IDs are not interchangeable across the two runs.

## Detector changes

- Recursive refinement uses 2048-sample pitch windows with a 256-sample hop instead of 256-sample pitch windows, which were too short to estimate bass fundamentals at 44.1 kHz.
- A pitch discontinuity must have a nearby envelope onset before it can split an event. Continuous glissando is therefore retained as one event unless a new attack supports a split.
- Pitch-onset corroboration uses a 2 dB rise; envelope-only candidate supplementation keeps its validated 3 dB threshold.
- Each event includes periodic-pitch quality metadata. Only slices at most 50 ms, with event peak at or below -35 dB and no periodic frames, are marked `disqualified`. Other weak pitch evidence is `pitch_unconfirmed`, not automatically excluded.

## Output

- `manifest.json`: 449 revised event boundaries and quality labels.
- `run_metadata.json`: source hash, analysis settings, output counts, and slice policy.
- `slices/`: exact detector-boundary mono WAV slices, without fades, padding, normalization, or postprocessing.
- `review.html`: isolated review UI with a separate E009 browser-storage key.

The revised detector produced 449 events from the source; 5 met the strict nonperiodic-fragment disqualification rule and 2 remained pitch-unconfirmed. This is not a claim of perfect note segmentation. Human judgments from E008 have not been copied or mapped to E009 because the segmentation changed.

## Validation

The automated suite passes (`7 passed`). The existing E003 count benchmark remains exact at the selected `256/64/-45` setting: 3, 3, 3, and 5 events for the four reviewed excerpts. Synthetic checks confirm a continuous glissando stays in one event and a short nonperiodic fragment receives the disqualification status.
