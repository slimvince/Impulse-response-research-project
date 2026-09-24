# Current Handover: E003 Note Segmentation

**Updated:** 2026-09-24
**Purpose:** Durable handover for a fresh session with no chat context.

## Research objective

The repository investigates whether measurable differences between Yamaha SLB-200 pickup/DI recordings and acoustic upright-bass microphone recordings can eventually support an impulse-response transformation. The project is still in Phase 1, Unified Corpus Characterization. No SLB-200 comparison or IR target claim is currently possible.

Preserve the reasoning chain:

`Observation -> Finding -> Interpretation -> Hypothesis -> Decision`

Do not treat frame rows as independent replicates, whole-file means as direct transformation targets, or the threshold detector as a validated note detector.

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

A second recursive probe on children 2, 3, 10, 30, and 31 was mixed. `128/32/-38` left all but child 2 as one event; `64/16/-45` split child 2 and child 31 into two events but left children 10 and 30 merged. Finer recursion can help selectively, but frame-size changes alone do not solve the hardest multi-note children.

The first bass C audit is now recorded in `experiments/E003/bass_c_listener_audit.csv`: three events are usable, two are ambiguous because of possible short notes at their ends, one is silence, and the approximately 10-second event contains an estimated 30-50 notes merged into one, too many to count reliably. This confirms that the detector can produce acceptable isolated events in bass C but still fails severely on long multi-note active regions.

Trace detail: at `256/64/-45`, bass C has four threshold-active regions, with the first lasting approximately 47.864 seconds. The splitter subdivides that long region into 77 outputs overall, but its first output still lasts 10.0325 seconds and contains an estimated 30-50 notes. The failure is therefore localized under-segmentation inside the beginning of a very long active region, not a total failure to detect activity in the recording.

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
