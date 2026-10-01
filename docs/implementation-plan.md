# Implementation Plan

## Current phase: Unified Corpus Characterization and event benchmarking

### Current handover state: E014/E015/E016 transform diagnostics

- E005 algorithm bake-off and tuning are complete for the practical Windows candidates.
- E006 NS/Ergo EUB proof of concept is complete at pipeline level; expanded event audit is complete with 15/19 usable in a selected sample.
- E007 acoustic-vs-EUB descriptive comparison is complete but not a transformation result.
- E011 records an iterative evaluation of the repository slicer against the durable E008 audit. It remains useful as a reference, but is not the current candidate-generation priority.
- Cubase Pro 15 has produced 3,754 candidate slices across five external slice sets. Cubase is a candidate generator, not ground truth.
- E012 ran the initial 498-slice pass; E013 extends it to all five sets and reports 921 provisional accepts, 150 exact/effective-silence rejects, and 2,683 uncertain. Thresholds are exploratory; no candidate has a human reference label.
- E014 generated a full-length minimum-phase spectral-ratio trial from 24 listener-confirmed SLB intervals and provisional acoustic candidates. Its held-out normalized spectral-shape MAE worsened slightly, 9.10 to 9.20 dB; it is audition material, not a supported improvement or physical IR.
- E015 maps Cubase SLB candidate slices to source time and compares per-slice dry/filtered features with acoustic candidate distributions. The 24 confirmed SLB events are in-sample for E014; the 33 mapped validator-accepted Cubase events represent only high-register/low-level conditions. Do not infer general improvement from sparse cells.
- E016 tests one predeclared median per-event log-spectrum alternative and prepares loudness-matched full-file auditions. Aggregate median-profile metrics favor E014; a separate per-event metric slightly favors E016. Neither is validated; keep E014 as baseline pending listening and a genuinely untouched source-level test.
- E018 applied existing E014/E016 filters to the newly available 362 s recording two and made raw/RMS-matched full-file renders. This adds an audition source, not an independent filter validation.
- E017 prepares a deterministic 50-slice, five-set human audit with separate event-validity, reason-code, confidence, and f0-reliability labels. Do not tune and report performance on this same calibration sample; reserve a separate source/set-level holdout.
- Immediate priority is a manually labeled, stratified Cubase reference set and evaluation of the first-pass validator. Do not start SLB-vs-acoustic feature comparisons or IR optimization from unvalidated candidate slices.
- Preserve the distinction between descriptive source-domain differences, candidate filter-addressable effects, and validated IR behavior.

### Completed

- Python package scaffold and editable installation configuration
- Standard-library PCM WAV reader with source hashing
- Deterministic framing
- Initial frame and event measurements
- Manifest-driven unified pipeline
- JSON and Markdown outputs
- Synthetic test definitions
- Research documentation and licensing boundary
- Full test suite: 8 passing tests, including signed 24-bit PCM decoding
- Synthetic WAV CLI smoke test with all five expected output files
- Git initialization, commits, push, and clean synchronized worktree

### Immediate blockers

- Establish a manually labeled Cubase candidate-slice reference set (`usable`, `unusable`, `uncertain`) with reason codes and confidence. Keep the two slice sets grouped separately; `Audio 02` has no surviving unsplit source.
- Implement a reproducible validator that consumes candidate WAVs/manifests and outputs inspectable tests, accept/reject/uncertain, and one or more rejection reasons.
- Measure false positives, false negatives, precision, recall, F1, retained corpus size, and acceptance representativeness by slice set and measurable context. Keep uncertain labels out of initial threshold fitting.
- Keep event validity separate from feature reliability and transformation relevance. A valid excitation may have unmeasurable f0; a plausible f0 does not prove an isolated event.
- The E008/E011 human rulings are on a different boundary set and cannot be transferred as Cubase validator labels without interval/file identity evidence.
- Obtain or record a small licensed pilot corpus.
- Confirm permission and complete capture metadata for the external acoustic candidate recordings.
- Add later bass A and bass B recordings to their existing source groups, and register other acoustic basses as separate source groups.
- Implement within-group repeatability summaries for the bass A and bass B pairs before freezing the first `E001` manifest.
- Create a manually reviewed ground-truth subset and quantify split/merge/missed-boundary errors before proceeding to event-conditioned analysis.
- Register approved pilot recordings and freeze the first `E001` manifest.

### Current status after `E002`

- Basic Pitch is operationally useful as a candidate event generator for the current acoustic corpus, but the event population is still too ambiguous to be treated as a validated note detector.
- The `E002` gate is a conditional pass, and the listener review makes the conditional status sharper: the four candidate clips tested were not single-note events. `low_01_low` contained five notes; each of the `mid_*`, `bass_*`, and `broad_*` clips contained three notes. The pitch/frequency domain showed clear note-to-note changes with no glissandi or portamenti, and the notes were not tied, so this is a sequence of individually plucked notes rather than a single continuous note or hammer-on/legato event.
- This is not a minor boundary issue. It confirms that the current single-pass candidate events are not yet suitable as a note-level benchmark or as a direct basis for event-conditioned analysis, because the slices contain multiple distinct notes that must be segmented rather than treated as one event.
- Human auditioning of individual slices remains an important triage step for obvious false splits, merges, and missing events, and it clarifies that the selected candidate windows contain multiple distinct notes instead of isolated single-note examples.
- Event-validation work should proceed with a small manually reviewed subset of isolated notes and note transitions before any broader event-level dataset is treated as trusted.

### Current status after `E003`

### Current status after `E005` and `E006`

- E005 completed the first real-recording algorithm bake-off: recursive detector, librosa, aubio, Basic Pitch, and MuScriptor were run/tuned with development/holdout separation.
- The recursive detector remains the count/onset baseline; aubio and MuScriptor are promising independent candidates. Essentia is blocked on Windows; MT3 and commercial references remain untested.
- E006 executed the unchanged unified pipeline on one NS Design direct/EUB recording and 16 representative Ergo EUB recordings, producing 4,620 frames and 243 diagnostic events.
- The next task is E006 event-quality auditing and EUB-vs-EUB/source-domain characterization. Do not start IR optimization or require perfect event pairing before testing transformability.

- A partially labeled benchmark exists at `experiments/E003/ground_truth.csv` with 14 approximate note intervals across four excerpts.
- The evaluator and raw-slice exporter are implemented in `experiments/E003/`.
- The best tested setting is `256/64/-45`, with total absolute count error 2: counts 3/3, 3/3, 3/3, and 3/5 against the reviewed references.
- The current detector still merges two or more notes in `low_01_low.wav`; it is not accepted as a reliable individual-note detector.
- A global increase from two to four pitch-based split points was tested and rejected because it introduced false splits in the other excerpts. The next change must be selective and benchmarked across all four clips.
- Audition outputs are raw exact-boundary slices with no fades, context, normalization, or other postprocessing. The original files under `experiments/E002/listener_slices` remain the only analysis inputs.

### Human audition protocol for slice validation

Use the listening pass only for triage and boundary sanity-checking. It is a way to identify obvious segmentation failures and to prioritize ambiguous cases for manual annotation; it is not a substitute for the quantitative benchmark.

Recommended workflow:

1. Select a small set of candidate events from the same excerpt: easy positives, obvious borderline cases, likely splits, likely merges, and low-confidence detections.
2. Export each event as a short slice centered on the event, with a small before/after buffer (for example 100-250 ms context around onset and offset).
3. Ask the listener to label each slice as one of: `clear single note`, `split`, `merged`, `missing/uncertain`, or `ambiguous legato`.
4. If the listener hears a split, record whether it is a false split in the middle of a single note or a true two-note event that the detector missed.
5. If the listener hears a merge, record whether the event should have been two separate notes with a boundary gap or a single note with a different envelope.
6. Capture a quick confidence score for each label (`1` = very confident, `3` = uncertain).
7. Keep the slice list and labels alongside the time-stamped detections so the results can be compared to the benchmark when the ground-truth subset is created.

This loop is especially valuable for low-register bass, overlapping notes, and legato passages, where split/merge errors are easiest to miss without listening.

### Next implementation steps

1. Validate the external Cubase slice manifest and file hashes before analysis; preserve `slice_set_id`, original filenames, source hashes where available, and Cubase provenance status.
2. Create a manually labeled reference subset stratified by slice set, duration, measured level, likely false positives, and likely false negatives. Capture verdict, confidence, and multi-valued reason codes.
3. Freeze a development/held-out split at the slice-set/source-group level before choosing validator thresholds.
4. Implement transparent quality measurements (duration, energy/SNR proxies, clipping, onset isolation, internal competing attacks, boundary bleed, pitch reliability, and spectral plausibility) without equating any single feature with event validity.
5. Evaluate accept/reject/uncertain against human labels; report confusion matrix, precision, recall, F1, candidate/accepted counts, rejection reasons, and acceptance rates by context.
6. Inspect false positives and false negatives, revise only explicit tests, and rerun the frozen holdout. Do not tune to maximize the accepted slice count.
7. Treat the existing threshold detector, E009/E011, aubio, and Basic Pitch as optional comparison/candidate sources, not as the primary Cubase candidate slicer.
8. Only after validator performance and representativeness are acceptable, extract event features and compare SLB/acoustic populations conditioned on register, local level, and articulation.
9. Continue provenance, metadata, repeatability, confound, and held-out evaluation work before any IR optimization.

### Research stages for event-level evaluation

- Benchmark candidate onset and offset algorithms against a manually reviewed ground-truth subset.
- Evaluate bass pitch-tracking and note segmentation on isolated, overlapped, and legato excerpts.
- Assess overlap/polyphonic detection and confidence classification, and exclude ambiguous events when needed.
- Compare event-conditioned temporal and spectral measurements between SLB and acoustic notes while conditioning on register, dynamics, articulation, and overlap status.
- Build recording-level and event-level comparison models only after segmentation reliability is quantified.
- Freeze development and held-out corpus manifests only after the event-detection benchmark is accepted for the intended use case.
- Define a closed-loop transform evaluation protocol for held-out note-level comparisons.
- Only then investigate candidate FIR or other transformations.
- If long recordings make memory a practical problem, add internal streaming without requiring manual source splitting; preserve source hashes, frame continuity, event context, and whole-file semantics.
- Revisit broader audio-format support only if it becomes a concrete corpus blocker.

## Completion criteria for Phase 1

Phase 1 is not complete when a large CSV exists. It is complete when:

- both domains run through the same versioned pipeline;
- source hashes, parameters, splits, and metadata are recorded;
- candidate features have synthetic tests and documented limitations;
- event detection is benchmarked and confidence-labeled for note-level use;
- comparisons are recording-level and event-conditionable;
- repeatability variation is quantified before domain differences are selected as transformation targets;
- reports distinguish observation from interpretation and confound;
- held-out evaluation can be performed without corpus leakage;
- the corpus is large enough to support qualified conclusions.
