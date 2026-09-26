# Current Handover: E003 Note Segmentation

**Updated:** 2026-09-26
**Purpose:** Durable handover for a fresh session with no chat context.

## Research objective

The repository investigates whether measurable differences between Yamaha SLB-200 pickup/DI recordings and acoustic upright-bass microphone recordings can eventually support an impulse-response transformation. The project is still in Phase 1, Unified Corpus Characterization. No SLB-200 comparison or IR target claim is currently possible.

Preserve the reasoning chain:

`Observation -> Finding -> Interpretation -> Hypothesis -> Decision`

Do not treat frame rows as independent replicates, whole-file means as direct transformation targets, or the threshold detector as a validated note detector.

## Transformability clarification

A fixed IR does not "understand" an individual note. It is linear and time-invariant: the same filter is applied to every sample. It can change harmonic balance, transient coloration, and ringing in ways that interact with register and dynamics, but it cannot condition itself on note identity, articulation, loudness, or the current point in a note's life.

Unpaired acoustic and SLB events can support a candidate statistical magnitude transformation when distributions are conditioned on register, level, and articulation. They cannot uniquely identify a physical transfer function or establish event-specific temporal correspondence. Exact sample-synchronous dual performance is not required for the statistical question, but paired or controlled repeated material is needed to validate an actual transformation.

The next research gate is transformability, not perfect note slicing: determine whether stable, filter-addressable differences exist in conditional time-frequency distributions. If the desired behavior depends materially on register, dynamics, articulation, or note state, consider an IR bank or a time-varying/nonlinear model rather than one fixed IR.

E007 now contains `event_features.csv` and `conditional_comparison.json`, built from acoustic 30-second windows and E006 EUB events. The first conditional comparison populated only three register/level cells with both domains, all classified high register by the current f0 estimator; one cell had only six EUB events. Do not interpret the resulting deltas as IR evidence until register coverage, event quality, and articulation labels improve.

## Consolidated current state: 2026-09-26

### Event segmentation

- Production `detect_events` uses clustered pitch evidence, envelope-onset supplementation, and bounded two-level refinement for events longer than 0.75 seconds.
- Recursive refinement now uses 2048-sample pitch windows with a 256-sample hop; pitch-based splits require a nearby envelope onset. Continuous glissando and distinct-pluck regression tests cover these behaviors.
- Events now carry periodic-pitch quality metadata. Only very short, low-level slices with no periodic evidence are marked `disqualified`; weak evidence is retained as `pitch_unconfirmed`.
- E003 count benchmark at `256/64/-45` remains exact: `3/3, 3/3, 3/3, 5/5`; tests pass (`7 passed`).
- E009 is the separate revised SLB run: 449 slices, 5 strict nonperiodic-fragment disqualifications, and 2 pitch-unconfirmed events. E008's 578 slices and all prior human judgments were preserved and not remapped.
- Polyphony classification and precise attack/decay boundary accuracy remain unvalidated; do not treat the E009 detector labels as proof of clean monophonic notes.
- E004 real-recording hit-rate sample: `12/36` usable (`33.3%`); positive-control precision: `9/18` (`50%`).
- Event routing is conservative: recursive detector primary, aubio secondary evidence, Basic Pitch candidate context; no automatic scientific acceptance or blind fusion.

### Algorithm bake-off

E005 has measured recursive detector, librosa, aubio, Basic Pitch, and MuScriptor on the shared four-excerpt set with development/holdout tuning. Consolidated report: `experiments/E005/BAKEOFF_REPORT.md`; machine measurements: `measurement_report.json`.

- Recursive: total count error 0; mean ordered onset error 52 ms.
- Aubio tuned `specdiff/.7`: count error 2; mean ordered onset error 116 ms.
- MuScriptor tuned small model `cfg_coef=1.5`: count error 3 development / 1 holdout.
- Basic Pitch tuned default: count error 3 development / 3 holdout.
- Librosa tuned: count error 3 development / 2 holdout; weaker onset timing.
- Essentia: Windows build blocked; no result.
- MT3, commercial references: not tested.

These are count/timing measurements, not final usability rankings. The candidate raw outputs and tuning metadata are preserved in `experiments/E005/`.

### EUB proof of concept

E006 runs the existing unified pipeline on one NS Design direct/EUB recording plus 16 representative Ergo EUB recordings. Original Ergo float files remain unchanged; derived PCM16 files and hashes are recorded in `experiments/E006/manifest.json`. Output: 17 recordings, 4,620 frames, 243 events. The NS microphone is not an acoustic target. EUB event-quality audit is pending.

### Environments

- Canonical `.venv`: Python 3.14; project pipeline, librosa, aubio-independent code.
- `.venv-basicpitch`: Basic Pitch/TensorFlow inference.
- `.venv-audioalgorithms`: Python 3.11; aubio 0.4.9.
- `.venv-muscriptor`: Python 3.11; authenticated MuScriptor small model.
- Essentia: source build failed on Windows with internal `IndexError`; WSL has no installed distribution.

### Immediate next session action

1. Audit representative E006 NS/Ergo events and classify silence, usable note, overlap/polyphony, fast passage, articulation, and ambiguity.
2. Use those results to decide whether the existing pipeline is sufficient for EUB characterization.
3. Run conditional time-frequency/distribution analysis across acoustic, NS, and Ergo only after event quality is characterized.
4. Do not start IR optimization or claim a final detector until transformability and held-out validation are defined.

## Current decision

Individual plucked notes and note-to-note transitions are the relevant analytical unit for temporal work. The current detector is a reference implementation and exploratory candidate generator. Event-conditioned analysis must wait for a manually reviewed benchmark and quantified split, merge, missed-note, onset, and offset errors.

A hybrid approach remains the working direction: candidate generation, pitch/onset evidence, boundary refinement, confidence labeling, and explicit handling of ambiguous events. No algorithm has been accepted as adequate.

## E003 benchmark state

Files:

- `experiments/E003/ground_truth.csv`: 14 approximate note intervals across four excerpts, confidence `2`.
- `experiments/E003/ground_truth_template.csv`: untouched example template.
- `experiments/E003/manifest.json`: status `partially_labeled`, records reviewed note counts, references `ground_truth.csv`.
- `experiments/E003/evaluate_benchmark.py`: evaluates five detector settings against the labels.
- `experiments/E003/benchmark_results.json`: latest generated benchmark output.
- `experiments/E003/export_detected_slices.py`: exports raw detector event slices.
- `experiments/E003/detected_slices/review_manifest.json`: latest event-slice manifest.

Reviewed reference counts:

- `low_02_low.wav`: 3 notes, approximate intervals 0.00-0.15, 0.15-0.73, 0.73-0.85 seconds.
- `bass_friendly_01_bass_friendly.wav`: 3 notes, approximate intervals 0.00-0.15, 0.15-0.61, 0.61-0.76 seconds.
- `broad_03_broad.wav`: 3 notes, approximate intervals 0.00-0.15, 0.15-0.65, 0.65-0.79 seconds.
- `low_01_low.wav`: 5 notes, approximate intervals 0.00-0.14, 0.14-0.41, 0.41-0.57, 0.57-0.77, 0.77-0.88 seconds.

These boundaries are approximate audition labels, not high-precision ground truth.

## Latest measured detector result

The best tested setting remains `frame_size=256`, `hop_size=64`, `threshold_db=-45`:

- `low_02_low.wav`: 3 detected / 3 reference.
- `bass_friendly_01_bass_friendly.wav`: 3 / 3.
- `broad_03_broad.wav`: 3 / 3.
- `low_01_low.wav`: 3 / 5.
- Total absolute count error: 2.

Other tested settings had total count errors of 6, 12, 25 or more in the earlier validated run. The remaining known failure is a merge in `low_01_low.wav`.

Latest listener audit of the raw `low_01` detector outputs refines this failure: event 1 contains the first note plus a very short piece of the second note; event 2 contains three notes; event 3 contains two notes, with its first note being the second half of the last note heard in event 2. Therefore the detector has both merge errors and boundary errors, including a musical note divided across adjacent detector events.

The corresponding audition of the other three reviewed excerpts found that their detector slicing was musically correct. The current empirical picture is therefore three successful reviewed excerpts and one known failure, not a blanket failure of the slicing approach.

Latest audition of the adaptive five-event `low_01` output refines the result: event 1 contains a short tail of note 2; event 2 is otherwise correct but misses the initial short part of note 2 because it is in event 1; event 3 contains two notes, with the second continuing into event 4; event 4 contains one note that began in event 3; event 5 is correct. Thus the adaptive rule fixes the event count but still has cross-event boundary continuity errors.

A probe that increased the pitch-aware split limit globally was rejected because it created false splits. The validated fix now uses clustered pitch evidence plus selective envelope-onset supplementation for long, pitch-sparse regions. At `256/64/-45`, it produces counts 3/3, 3/3, 3/3, and 5/5 for the four reviewed excerpts, with total count error 0. This is a benchmark improvement, but boundary accuracy still needs listener review and a larger labeled set.

## Audition-file policy

The user requires every instructed audition file to be a clickable workspace-relative Markdown link. Never provide plain filenames when asking for audition.

Audition files must contain exactly the raw analyzed samples: no fades, context padding, normalization, or other postprocessing. The current exporter uses exact detector boundaries from the original input samples. Hard-boundary clicks are expected and must not be hidden by fades.

Analysis inputs remain the original WAV excerpts under `experiments/E002/listener_slices`. Generated event slices under `experiments/E003/detected_slices` are raw outputs for listening to detector behavior. Do not use generated audition slices as corpus inputs. Faded/manual reference audition directories were removed.

## Event usability policy

The detector does not need to achieve perfect slicing for every event. Preserve all outputs and provenance, then classify events as `usable`, `ambiguous`, or `disqualified` for downstream analysis. Disqualified events remain in the experiment for detector evaluation and failure analysis but are excluded from event-conditioned feature analysis. Human audition should focus on difficult or high-impact cases rather than every obvious event.

The current human decisions are persisted in `experiments/E003/listener_audit.csv`: all events in `low_02_low.wav`, `bass_friendly_01_bass_friendly.wav`, and `broad_03_broad.wav` are `usable`; `low_01_low.wav` events 1 and 2 are `ambiguous`, events 3 and 4 are `disqualified`, and event 5 is `usable`.

## Validation

Latest direct Python validation:

- `pytest -q`: 5 passed.
- E003 benchmark evaluator ran successfully and wrote `experiments/E003/benchmark_results.json`.
- Raw detector exporter ran successfully and wrote `experiments/E003/detected_slices/review_manifest.json`.
- Static diagnostics reported no errors for the touched Python, JSON, CSV, and README files.

When terminal approval is unavailable, the VS Code/Pylance Python execution integration can run repository scripts with the selected interpreter at `.venv/Scripts/python.exe`.

## Immediate next work

1. Keep the raw-only audition policy.
2. Review the five adaptive `low_01` detector outputs using clickable links, focusing on boundary continuity rather than count.
3. Treat E003 usability classifications as provisional until the approximate labels are refined.
4. Expand the manually reviewed set beyond these four excerpts before accepting any detector for event-conditioned IR analysis.
5. Apply the same pipeline to the new bass C file only as an unlabeled stress test until it receives manual labels.
6. Update `docs/project-context.md`, `docs/implementation-plan.md`, `docs/research-log.md`, `docs/decisions.md`, and `docs/hypotheses.md` whenever the evidence or decision changes.

The first envelope-only retry was rejected: it produced six raw candidates for `low_01` because of a secondary rise near 0.261 seconds. Its temporary outputs were removed. Do not present envelope-only slices as a successful five-note detector.

## New external recording

An additional external acoustic recording is now available at `C:\IR audio\acoustic\bass C\5.wav`. It is registered as `acoustic_bass_c_take_1` in `docs/corpus.md` and `C:\IR audio\acoustic-repeatability-manifest.json`, source group `bass_c`, comparison group `acoustic_bass_c_repeatability`. Verified facts: stereo, 44.1 kHz, 16-bit PCM WAV, 48.16 seconds, SHA-256 `fc8b93807bc8e33e5da50e6691b884d844aec72e97bbcf55fb6befcbfa8c6c7f`. Player, instrument details beyond the source-group label, microphone, room, chain, and take metadata remain unknown. It is a candidate input, not an approved corpus entry, and must remain outside Git.

Additional external files are now available: `C:\IR audio\acoustic\bass A\3.wav`, `4.wav`, and `5.wav` are registered as bass A takes 3-5; `C:\IR audio\acoustic\bass D\1.wav` is registered as `acoustic_bass_d_take_1` in new source group `bass_d`. All are candidate inputs outside Git with unknown contextual metadata.

The current recursive scan at `256/64/-45` produced: bass A3 = 2,187 events with 776 under 20 ms and longest 1.543 s; bass A4 = 1,018 events with 31 under 20 ms and longest 1.547 s; bass A5 = 1,395 events with 728 under 20 ms and longest 2.707 s; bass D1 = 50 events with 25 under 20 ms and longest 1.357 s. Twelve raw shortest/longest audit slices are in `experiments/E003/expanded_source_audit/` with manifest metadata.

The expanded listener audit is in `experiments/E003/expanded_source_listener_audit.csv`: only the selected bass D long event was a clear single note. The other selected slices were silence, double stops/simultaneous notes, or dense fast-note passages. These are disqualified for the current monophonic note-analysis target, but they also document real polyphonic and fast-articulation content rather than automatically proving detector failure.

An unbiased follow-up sample of eight ordinary-duration events, two per new bass A/D source file, is in `experiments/E003/expanded_source_typical_audit/`. These raw slices were selected from the 0.08-0.8 second duration stratum to estimate typical usability rather than stress-case failure rates.

The typical-duration listener audit is in `experiments/E003/expanded_source_typical_listener_audit.csv`: four events are usable, three are ambiguous because of short-upbeat or very-silent conditions, and one four-note event is disqualified. Glissando events remain usable single notes and should retain an articulation label rather than being treated as ambiguous.

At `256/64/-45`, the unlabeled bass C stress test produced 77 events with a shortest duration of 0.0029 seconds and longest duration of 10.0325 seconds. At `128/32/-38`, it produced 175 events with a shortest duration of 0.0007 seconds. These are diagnostics only, not note counts.

A bass C parameter sweep shows the long merge is tuning-sensitive but not solved by one global setting: `64/16/-35` gives 1.034 s longest events but 1,220 events, including 903 shorter than 20 ms; `256/64/-35` gives 1.617 s longest events and 192 events; `128/32/-38` gives 5.777 s longest events and 175 events; `256/64/-45` gives 10.032 s longest events and 77 events. Smaller frames/hops improve temporal resolution at the cost of severe fragmentation. No global setting is accepted; long-event recursive refinement is the next target.

The first targeted recursive refinement of `bass_c_event_07_source_index_001.wav` used `256/64/-35` on the 10.0325-second parent and discarded only child events shorter than 20 ms. It produced 31 raw child slices, with the longest child 0.83 seconds. These are experimental replacement candidates, not yet accepted note boundaries; their manifest is `experiments/E003/bass_c_recursive_event_07/manifest.json`.

Bounded long-event refinement is now enabled in `src/ir_research/events.py`: events over 0.75 seconds are reprocessed at `256/64/-35` for at most two levels, children shorter than 20 ms are removed, and the parent is retained if no useful children result. On bass C this raises the event count from 77 to 161 and reduces the longest event from 10.032 to 1.387 seconds. The former 10-second block is exported in the v2 audit set; a fresh v3 set should be generated after further detector changes.

An initial spectral-flux candidate experiment was rejected: it increased E003 best-setting count error from 0 to 3 and over-split `low_01` from 5 to 8 events. The production splitter was restored to the validated adaptive pitch/envelope version; spectral flux should not be reintroduced without stronger candidate validation.

The installed `librosa 1.0.0` onset detector was also probed as a standalone alternative. With `hop_length=64`, it found 3 onsets in the 5-note `low_01` excerpt, 2 in `bass_friendly_01_bass_friendly.wav`, and 3 in `broad_03_broad.wav`; it is not adequate as a standalone slicer. The next algorithmic candidate is global optimization over combined pitch and envelope candidates.

The isolated global-boundary probe is in `experiments/E003/optimize_boundaries.py`. It improved proposed boundaries for `low_02` and `low_01`, but shifted boundaries incorrectly in the bass-friendly and broad excerpts. It remains experimental and is not integrated into production.

The representative recursive audit is recorded in `experiments/E003/bass_c_recursive_listener_audit.csv`: children 1, 5, and 20 contain one usable note; child 3 contains two notes with hammer-on ambiguity; child 31 contains four and possibly five notes; children 2, 10, and 30 contain merged multiple notes and are disqualified. The recursive pass substantially reduces the original merge but still requires another refinement pass for multi-note children.

The v2 audit is recorded in `experiments/E003/bass_c_recursive_v2_listener_audit.csv`: children 1, 5, and 20 contain one usable note; child 3 contains two notes with hammer-on ambiguity; child 31 contains five notes; children 2, 10, and 30 contain 4, 2, and 2 merged notes. The v2 sample therefore has 3 usable, 1 ambiguous, and 4 disqualified children.

The v3 audit is recorded in `experiments/E003/bass_c_recursive_v3_listener_audit.csv`: children 1, 5, and 20 are usable; child 3 is hammer-on ambiguous; child 30 is uncertain; children 2 and 10 remain merged; child 35 is duophonic, with one voice playing two notes while another sustains one. The v3 sample has 3 usable, 2 ambiguous, and 3 disqualified children.

The real-recording hit-rate sample is in `experiments/E004/real_hit_rate_sample/manifest.json`. It contains 36 raw slices across all nine external recordings: four duration strata (`short_risk`, `lower_typical`, `median_typical`, `upper_typical`) per source file. The generation run timed out before adding the optional four long-risk extras, so the sample count is explicitly 36 rather than an inflated 40.

The completed human audit is in `experiments/E004/real_hit_rate_sample/hit_rate_audit.csv`: 12/36 usable (`33.3%`), 24/36 disqualified, and no ambiguous labels. By stratum, usable rates are short-risk `0/9`, lower-typical `3/9`, median-typical `4/9`, and upper-typical `5/9`. This is a real-recording measurement, but the duration-stratified sample is not a natural corpus prevalence estimate; report the strata separately.

A positive-control audit sample is now in `experiments/E004/positive_control_sample/`: 18 raw slices, two per source file, selected by duration `0.08-0.8 s`, attack time `<=0.12 s`, and highest peak among eligible events. Its purpose is to measure whether events the detector would automatically trust are actually usable. The direct-link index is `AUDIT_LINKS.md`; no positive-control judgments have been recorded yet.

The positive-control audit is now complete in `experiments/E004/positive_control_sample/positive_control_audit.csv`: 9 usable (`U`), 9 disqualified (`D`), and 0 ambiguous (`A`). Thus the current high-confidence selection precision is `50%`, far below a useful automatic-trust target. Disqualified cases included many-note merges, two-note merges, and duophonic events.

E005 has started the real-recording algorithm bake-off. The first lightweight comparison is in `experiments/E005/results.json`: recursive detector counts are `3, 3, 3, 5` for the four shared excerpts, while librosa onset counts are `5, 2, 3, 3`. Neither candidate dominates; Basic Pitch is the next candidate to run. The current detector remains the baseline, not the chosen architecture.

Basic Pitch has now been run in the dedicated `.venv-basicpitch` environment. On the same four excerpts it produced default counts `2,2,2,2` and stricter counts `1,1,1,1`; it under-segments the reviewed short-note material. Raw outputs are in `experiments/E005/basic_pitch_results.json` and are candidate note events, not validated excitation boundaries.

Essentia, aubio, and madmom are not installed in the active `.venv`; no result has been obtained from them. Treat this as an environment/setup blocker, not evidence against those algorithms. A compatible dedicated environment and exact package versions must be recorded before their bake-off runs.

The dedicated `.venv-audioalgorithms` now contains aubio 0.4.9, and its default onset detector was run on E005: counts were `5,6,6,7` against reviewed counts `3,3,3,5`, indicating over-detection. Essentia installation was attempted in the same environment but the available source build failed with an internal `IndexError`; no Essentia result should be inferred.

Aubio development tuning selected method `specdiff` with threshold `0.7`: development count error `0`, holdout count error `2`. This improves aubio count transfer relative to defaults, but it is not yet evidence of accurate boundaries or usable-event yield.

MuScriptor 0.3.0 is installed in `.venv-muscriptor`, authenticated, and benchmarked. Default/greedy counts were `2,11,2,27`; the best tested setting was `cfg_coef=1.5` with greedy or beam-2 decoding, counts `5,3,2,4`, development count error `3`, holdout count error `1`. Raw outputs are in `experiments/E005/muscriptor_results.json` and `muscriptor_tuning_outputs/`; tuning metadata is in `muscriptor_tuning_results.json`.

Important bake-off qualification: these are baseline parameter runs. Do not conclude that an algorithm is poor from default settings alone. Candidate parameters must be tuned on development excerpts and evaluated on held-out real recordings, with false boundaries and usable-event yield weighted appropriately. Basic Pitch's default/stricter result is not an optimized comparison.

Basic Pitch tuning selected its default configuration (`onset=0.5`, `frame=0.3`, `minimum_note_length=127.7 ms`) with development count error 3 and holdout count error 3. A permissive short-note setting produced development error 106; lower thresholds are not automatically better.

The unattended E005 bake-off report is in `experiments/E005/BAKEOFF_REPORT.md`. Current count-transfer results: recursive detector `0/0` development/holdout error; librosa `3/2`; aubio tuned `specdiff/.7` `0/2`; Basic Pitch tuned default `3/3`. Essentia is blocked by the Windows source build; MuScriptor, MT3, and commercial systems remain untested. No candidate is accepted as final without boundary and usability evaluation.

Consolidated measurements: recursive detector total count error 0 / mean ordered onset error 52 ms; aubio tuned error 2 / 116 ms; Basic Pitch default error 6 / 222 ms; librosa error 5 / 280 ms. Human usable rates are E003 10/14 (71.4%), E004 stratified real sample 12/36 (33.3%), and E004 positive controls 9/18 (50%).

The tailored algorithm usage policy is `experiments/E005/usage_policy.json`: recursive detector is primary; aubio `specdiff/.7` supplies secondary onset evidence for long/uncertain events; Basic Pitch supplies candidate proposals/pitch context; silence, polyphony, fast passages, merged events, and unresolved boundaries are excluded or manually reviewed for strict monophonic analysis. Fusion is deferred until individual boundary audits are complete.

The strategy has now been executed as a conservative routing prototype in `experiments/E005/strategy_results.json`: recursive events are primary, aubio and Basic Pitch provide secondary evidence, long events are sent to review, and unsupported events are flagged ambiguous. It does not automatically declare events usable or perform boundary fusion.

The first E005 development/holdout tuning run used `low_02`, `bass_friendly`, and `broad_03` for development and held out `low_01`. The recursive detector selected `256/64/-45` with count error 0 on both development and holdout. Librosa selected `delta=0.2`, `wait=10`, with count error 3 on development and 2 on holdout. These are count-transfer results only; they do not establish boundary precision or usable-event yield.

A second recursive probe on children 2, 3, 10, 30, and 31 was mixed. `128/32/-38` left all but child 2 as one event; `64/16/-45` split child 2 and child 31 into two events but left children 10 and 30 merged. Finer recursion can help selectively, but frame-size changes alone do not solve the hardest multi-note children.

The first bass C audit is now recorded in `experiments/E003/bass_c_listener_audit.csv`: three events are usable, two are ambiguous because of possible short notes at their ends, one is silence, and the approximately 10-second event contains an estimated 30-50 notes merged into one, too many to count reliably. This confirms that the detector can produce acceptable isolated events in bass C but still fails severely on long multi-note active regions.

Trace detail: at `256/64/-45`, bass C has four threshold-active regions, with the first lasting approximately 47.864 seconds. The splitter subdivides that long region into 77 outputs overall, but its first output still lasts 10.0325 seconds and contains an estimated 30-50 notes. The failure is therefore localized under-segmentation inside the beginning of a very long active region, not a total failure to detect activity in the recording.

## E006 EUB proof of concept

E006 runs the existing unified pipeline on 17 representative EUB recordings: one NS Design direct/EUB recording and 16 derived PCM16 Ergo files. Original Ergo float WAVs remain unchanged; conversion and hashes are recorded in `experiments/E006/manifest.json`. Initial output is 4,620 frame rows and 243 threshold events. The NS live microphone track must not be treated as an acoustic-bass target. Event quality is not yet audited; no acoustic-vs-EUB or IR claim has been made.

The first E006 representative raw audit set is in `experiments/E006/audit_slices/`, with clickable links in `audit_slices/AUDIT_LINKS.md` and metadata in `audit_slices/manifest.json`. Human judgments are pending.

The E006 listener audit is now in `experiments/E006/audit_slices/listener_audit.csv`: 4/9 usable and 5/9 disqualified. NS contributed two usable events and one silence; Ergo contributed two usable events, three noise/silence cases, and one silence. This is a small duration-selected audit, not a general EUB accuracy estimate.

An expanded E006 source-balanced audit set is prepared under `experiments/E006/audit_slices_expanded/`: 19 raw slices, one high-signal ordinary-duration event per recording plus NS short/long controls. Direct clickable links are in `AUDIT_LINKS.md`; human judgments are pending.

The expanded E006 audit is complete in `experiments/E006/audit_slices_expanded/listener_audit.csv`: 15/19 usable (`78.9%`) and 4/19 disqualified. The failures were three Ergo noise/too-short cases and one NS silence control. This supports continuing EUB characterization, while remaining a selected audit rather than a corpus-wide hit rate.

E007 produced a first descriptive acoustic-vs-EUB comparison in `experiments/E007/REPORT.md`: nine acoustic 30-second windows versus completed E006 NS/Ergo outputs. The table shows level/spectral/f0 differences, but content, level, articulation, windows, capture, and source-group confounds are unmatched; no IR target interpretation is allowed.

Exact synchronization is not a prerequisite for the next E007 step. We can establish conditional per-event population differences by matching register, local level, articulation, and onset-relative phase across acoustic and EUB events. This yields statistical evidence for filter-addressable effects, not a unique physical transfer function. The E007 report now records this as the feasible next gate.

Working priority: per-event conditional evidence is more relevant to the eventual IR target than averages over complete pieces of music. Whole-recording averages remain secondary QC/context because they mix register, loudness, articulation, phrase content, player behavior, and capture conditions.

The first descriptive NS-vs-Ergo source-group comparison is `experiments/E006/REPORT.md`: NS and Ergo differ in level, spectral centroid/rolloff, flux, f0 distribution, and f0 confidence. These are observations only; no generic EUB finding or acoustic/IR claim is justified until register, level, articulation, repeatability, and capture confounds are addressed.

## Session closeout: 2026-09-25

### Current conclusions

- A fixed IR applies a static LTI rule to a time-varying signal; it can alter spectral balance, phase, transients, and ringing, but cannot adapt to note identity, loudness, register, articulation, or note age.
- Exact acoustic/EUB sample synchronization is not required for conditional per-event population analysis, but controlled repeated material is needed to validate a physical transformation.
- Per-event conditional evidence is more relevant than whole-piece averages for the eventual IR question.
- E005 is a first bake-off, not a final winner: recursive detector is the count/onset baseline; tuned aubio and MuScriptor are independent candidates; Basic Pitch is a candidate generator; librosa is supporting evidence.
- E006 proves the unified pipeline runs on NS Design direct/EUB and Ergo EUB. Expanded selected audit: 15/19 usable; NS microphone is not an acoustic target.
- E007 aggregate acoustic-vs-EUB differences are descriptive and confounded. The next useful analysis is conditional event-level characterization.

### Next session checklist

1. Read this handover, project context, implementation plan, E005 report, E006 report, and E007 report.
2. Preserve all original external audio and source hashes; do not use NS microphone as an acoustic target.
3. Audit or expand E006 event labels only where needed for conditional analysis.
4. Build event-level tables with register/f0, local level, articulation, and onset-relative phase.
5. Compare conditional distributions and repeatability across acoustic, NS, and Ergo groups.
6. Test whether differences are stable and filter-addressable before estimating any candidate IR.

One user-provided SLB-200 candidate is now registered outside Git at `C:\IR audio\slb200\vincents 1.wav`. Its file facts and hash are recorded in `docs/corpus.md`, but player, setup, chain, articulation, and permission-status metadata remain pending. Acquiring multiple documented SLB-200 takes across register, dynamics, articulation, and setup remains the highest-priority external dependency.

## Relevant code ownership

- `src/ir_research/events.py`: threshold active-region detector plus clustered pitch breaks and selective envelope-onset supplementation.
- `src/ir_research/audio.py`: WAV reading and framing.
- `src/ir_research/features.py`: f0 estimation and frame features.
- `tests/test_analysis.py`: five passing tests, including the synthetic distinct-pitch split regression.

## Do not forget

- Do not modify the audio corpus.
- Do not silently turn approximate labels into precise ground truth.
- Do not use Basic Pitch or threshold events as validated note evidence without benchmark support.
- Do not commit generated audio unless explicitly decided; preserve provenance and source hashes.
- Do not commit or push unless the user explicitly requests it in the active session.
