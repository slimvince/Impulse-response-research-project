# Research Log

## 2026-09-23 - Repository and Phase 1 foundation

- **Question:** What should be built before attempting IR optimization?
- **Decision:** Establish a unified corpus-characterization pipeline first.
- **Implemented:** Python package for WAV metadata, framing, initial features, event detection, manifest analysis, summaries, and reports.
- **Evidence:** Source diagnostics were clean. Runtime validation was completed later: the full suite passed with 4 tests, and a synthetic WAV passed through the CLI.
- **Interpretation:** The code is a validated reference scaffold, not a validated scientific result.
- **Confidence:** High for the architectural direction and basic execution path; low for the scientific usefulness of any current descriptor.
- **Next action:** Add real licensed pilot recordings and run E001.

## 2026-09-23 - Governing transformation objective

- **Objective:** Ultimately make an SLB-200 recording sound as close as possible to an acoustic upright-bass microphone recording using an impulse response.
- **Decision:** Treat this as the north-star objective while keeping Phase 1 focused on corpus characterization, repeatability, candidate descriptors, and evaluation design.
- **Interpretation:** Broad feature extraction is evidence gathering for the later objective, not the objective itself. A feature matters only if it is repeatable, relevant to perceived similarity, and plausibly addressable by a fixed linear time-invariant filter.
- **Limitation:** An IR cannot automatically correct unknown or drifting level, nonlinearities, player performance, room changes, or other effects outside the model. These must remain explicit evaluation factors.
- **Next action:** Define held-out measurable and perceptual criteria before any IR fitting or optimization begins.

## 2026-09-23 - WAV-only Phase 1 input contract

- **Question:** Is FLAC support necessary for the current research workflow?
- **Observation:** The available and planned pilot material can be analyzed as PCM WAV, and no current corpus blocker requires FLAC ingestion.
- **Decision:** Keep the Phase 1 input contract WAV-only and defer FLAC or broader container support.
- **Rationale:** Additional format dependencies would increase build and licensing surface without advancing the immediate repeatability or IR-evaluation objective.
- **Boundary:** If conversion is needed, preserve the original file, record conversion parameters, and retain the original source hash. Revisit native format support only if the corpus makes it necessary.

## 2026-09-23 - Preserve long source recordings

- **Question:** Does reducing memory use require manually cutting long recordings into smaller files?
- **Decision:** No. Preserve each original recording as one source; any future chunking is an internal streaming optimization only.
- **Rationale:** Manual splitting can alter event context and boundaries, complicate provenance, and make whole-recording distributions harder to interpret. Internal chunks must preserve frame overlap, hop continuity, event context, and the original source hash.

## 2026-09-23 - Durable handoff consolidation

- **Question:** What must survive when the next session begins?
- **Observation:** The repository now contains the Phase 1 reference pipeline, a broad exploratory feature bank at schema version `0.3`, the governing SLB-200-to-acoustic-upright IR objective, four external acoustic candidate inputs, and explicit constraints around unknown setup, uncontrolled level, unmatched content, correlated frames, WAV-only input, and intact source recordings.
- **Validated state:** HEAD `13d3591` is synchronized with `origin/main`; all 4 tests pass; the four external WAVs produced `47,055` frames and `105` events under the expanded pipeline. Generated audio results remain outside Git.
- **Interpretation:** The implementation is validated as a synthetic and real-audio extraction tool, not as evidence that any feature is an intrinsic bass characteristic or a useful IR target.
- **Immediate next action:** Implement recording/source-group aggregation, quality diagnostics, and distribution-level repeatability summaries for the bass A and bass B candidate groups; then add more recordings and freeze an approved E001 manifest.

## 2026-09-23 - Recording-level summaries and quality diagnostics

- **Question:** Can the pipeline report useful evidence without treating correlated frames as independent recordings?
- **Implemented:** Added per-recording feature summaries with mean, standard deviation, median, q10, q90, and missing counts; source-group summaries based on manifest metadata; event/frame counts as diagnostics; silence, clipping, DC offset, peak, RMS, duration, and sample-width metadata; manifest and configuration hashes in provenance.
- **Evidence:** The improved pipeline processed the four external recordings into two source groups, with `47,055` frames and `105` events. No clipping was detected. Silence fractions were approximately 0.00018-0.00236; DC offsets were approximately `0.00030` for Bass A and `-0.00334` to `-0.00340` for Bass B.
- **Interpretation:** The outputs now support recording/source-group inspection and quality review without claiming that frame rows are independent evidence. The Bass B DC offsets are a quality diagnostic requiring review, not an instrument finding.
- **Limitation:** The current source-group summary is descriptive and does not remove unknown level, unmatched content, or unknown setup/processing confounds. Robust repeatability distances and local-level trajectories remain future work.

## 2026-09-23 - Feature selection strategy

- **Question:** Should the initial feature list represent prior beliefs about relevance?
- **Decision:** Expand a broad, testable candidate measurement bank and use corpus evidence to evaluate relevance.
- **Interpretation:** Easy testability determines initial inclusion, not scientific importance. Library availability is not evidence of relevance.
- **Risks:** Multiple comparisons, redundant features, pitch and level confounds, and recording-chain effects.
- **Next action:** Maintain feature IDs and evaluate repeatability, conditional differences, redundancy, and confound sensitivity.

## 2026-09-23 - Broad open-source characteristic extraction

- **Question:** Should the project extract only characteristics already believed to matter?
- **Decision:** Extract as many characteristics as are practical through open-source libraries and tested reference code, then evaluate which ones matter for the use case.
- **Rationale:** The current phase is exploratory corpus characterization. Broad measurement reduces the risk of prematurely excluding useful descriptors.
- **Boundary:** A descriptor’s availability does not establish scientific relevance. Candidates must remain labeled exploratory and be evaluated for definition, validity, parameter sensitivity, redundancy, confounding, and recording-level repeatability before transformation use.
- **Next action:** Expand the feature bank in versioned, testable increments and record the library, version, license, algorithm, and limitations for each candidate.

## 2026-09-23 - Initial broad feature-bank increment

- **Question:** Which additional characteristics can be added immediately from the existing FFT frame representation?
- **Implemented:** Added spectral spread, skewness, kurtosis, slope, flatness, crest factor, broad-band ratios, and magnitudes near the first five f0-relative harmonics. Feature schema version advanced to `0.2`.
- **Evidence:** Synthetic analysis tests pass with finite values for the new descriptors.
- **Interpretation:** The pipeline now exposes a broader exploratory bank without changing the manifest, audio, event, or reporting interfaces.
- **Limitation:** These descriptors are exploratory; no relevance, repeatability, or transformation value has been established. Envelope trajectories, harmonic-to-noise estimators, inharmonicity, and richer temporal features remain future increments.
- **Next action:** Run the expanded bank on the four acoustic files, inspect missing values and parameter sensitivity, then add further candidates in tested increments.

## 2026-09-23 - Second broad feature-bank increment

- **Question:** Why were the remaining readily extractable candidates not implemented in the first increment?
- **Correction:** Added dominant spectral peak/bandwidth, frame envelope statistics, normalized f0 confidence, H1/H2 and H2/H3 ratios, harmonic-to-residual ratio, and f0-relative inharmonicity. Feature schema version advanced to `0.3`.
- **Evidence:** Focused synthetic tests pass after correcting confidence normalization against the unmasked autocorrelation zero-lag value.
- **Interpretation:** The catalogue now contains a broader set of concrete frame-level measurements; they remain exploratory descriptors rather than selected transformation targets.
- **Limitations:** Definitions are reference proxies, not replacements for reviewed perceptual or instrument-specific estimators. Rich event trajectories, event-to-event timing, and more specialized library backends remain future work.

## 2026-09-23 - Dependency strategy

- **Question:** Should one or many open-source audio libraries be used?
- **Decision:** Use NumPy as the foundation, add SciPy and possibly librosa/soundfile in replaceable roles, and keep GPL/AGPL alternatives optional pending licensing and behavior review.
- **Interpretation:** Multiple libraries are useful for independent algorithm comparisons, but permanent overlapping dependencies would add complexity without automatically improving validity.
- **Next action:** Record exact versions and compare outputs on synthetic and real signals before selecting alternative backends.

## Open questions

- Which features replicate across players, instruments, registers, and dynamics?
- How much of the observed difference is microphone, room, or recording-chain response?
- What event segmentation accuracy is required for temporal conclusions?
- Which features remain stable under explicitly labeled local-level sensitivity analyses and reasonable parameter changes?
- Is a static linear transform adequate? This remains unresolved.

## 2026-09-24 - Basic Pitch gate pilot

- **Question:** Can the candidate event detector produce a usable note/event segmentation on the current acoustic corpus?
- **Observation:** The pilot ran Basic Pitch on four 30-second acoustic excerpts from the two source groups using a default and a stricter parameter set. The results were 82-96 default events and 15-41 stricter events per excerpt, while the repository threshold baseline produced only 4-6 events.
- **Finding:** Basic Pitch is generating event-like structure on the real corpus, but its surface output is still too granular and ambiguous to be treated as a validated note detector without manual review. The listener review of selected candidate clips resolved this ambiguity further: `low_01_low` contained five notes, and each of the `mid_*`, `bass_*`, and `broad_*` clips contained three notes. The pitch/frequency domain showed clear note-to-note changes with no glissandi or portamenti, and the notes were not tied, so these are sequences of individually plucked notes rather than single-note or hammer-on events.
- **Interpretation:** The detector is promising as a candidate generator and conservative filter, but it is not yet reliable enough to support downstream event-conditioned conclusions without explicit confidence and ambiguity handling. The selected candidate clips are not valid single-note samples, and the real issue is boundary accuracy over a sequence of distinct plucks rather than a simple false-positive problem.
- **Hypothesis:** A manual reviewed subset of isolated notes and note transitions, plus confidence filtering on the note boundaries, should yield a usable event population for later event-level analysis, while the unfiltered output remains too noisy for direct scientific use.
- **Decision:** Classify the pilot as a conditional pass: useful for continued investigation and filtering, but not yet sufficient to claim a reliable note segmentation method. A small ground-truth benchmark on note boundaries and note sequences must still be created before proceeding to event-conditioned research.
- **Limitation:** This is a pilot on a small subset of excerpts only; it does not establish corpus-wide segmentation quality, legato handling, or missed-event rates. The current candidate slice test already shows that the relevant problem is multi-note segmentation within a phrase, not the presence of a single sustained note with a tied/hammer-on articulation.

## 2026-09-23 - Repeatability baseline for transformation targets

- **Question:** Can differences between recordings that should theoretically match improve later IR evaluation?
- **Observation:** Nominally equivalent recordings can still differ because of take variation, player technique, gain, setup, room, recording chain, event alignment, and feature sensitivity.
- **Finding:** No empirical finding has been established yet; the immediate value is methodological. These residuals can define a within-condition repeatability floor against which SLB-to-acoustic differences are judged.
- **Interpretation:** A feature difference is a plausible transformation target only when it exceeds relevant repeatability variation, is stable across recordings, and is consistent with an approximately linear and time-invariant effect.
- **Hypothesis:** Features with large between-domain variation relative to within-condition variation will be more useful and generalizable IR targets than features with large raw differences but poor repeatability.
- **Decision:** Add paired-recording metadata, event/frame alignment, recording-level repeatability summaries, and held-out repeatability checks before IR target selection.
- **Limitation:** This workflow has been documented but not implemented or tested on real recordings. Residual differences must not be treated as causal instrument characteristics.

## 2026-09-23 - Acoustic repeatability candidate inputs

- **Question:** Are there real recordings available to estimate the within-source noise floor before SLB-200 recordings exist?
- **Observation:** Four external stereo 44.1 kHz 16-bit PCM WAV files are available: two user-reported similar recordings for bass/player group A and two for bass/player group B. The SLB-200 directory is empty.
- **Evidence:** The existing unified extractor processed all four files, producing 47,055 frame rows and 105 detected events. Source hashes and file metadata are recorded in `docs/corpus.md` and the external manifest.
- **Finding:** The files are usable candidate inputs for a within-group uncertainty analysis, but no repeatability statistic has been computed yet. Cross-group differences are not a repeatability floor because the bass/player sources differ.
- **Interpretation:** The two within-group pairs can estimate variation attributable to takes, performance, setup, and analysis. Any result remains conditional on the still-unknown recording and licensing metadata.
- **Hypothesis:** Features that are stable within both groups may provide a stronger baseline for judging later SLB-to-acoustic differences than raw domain comparisons alone.
- **Decision:** Preserve the files outside Git, identify them by source hash, keep bass A and bass B as separate comparison groups, and implement grouped repeatability summaries before using them for IR target selection.
- **Limitation:** No SLB-200 recordings or formally approved corpus entries exist, and the current domain-level summary cannot yet calculate the grouped noise floor. The user has confirmed the four acoustic files are free to use; this permission basis is recorded but has not received independent legal review.

## 2026-09-23 - First extraction from four acoustic files

- **Question:** Can the current pipeline extract the defined characteristics from the four real acoustic recordings?
- **Observation:** The unified CLI processed all four files, producing 47,055 frames and 105 events. Bass A take 1 minus take 2 had mean differences of approximately 1.0 dB RMS, 27.6 Hz spectral centroid, and 10.8 dB in the 2-8 kHz band. Bass B take 1 minus take 2 had approximately -0.4 dB RMS, -2.3 Hz spectral centroid, and 6.0 dB in the 2-8 kHz band. The pooled bass A minus bass B differences were approximately 5.7 dB RMS, 9.0 Hz spectral centroid, and 18.0 dB in the 500-2000 Hz band.
- **Finding:** No empirical finding has been established. The pipeline successfully extracts the current feature bank from these real files, and the exploratory summaries show measurable within-pair and cross-group variation.
- **Interpretation:** Bass B appears more similar between its two files than bass A on the selected whole-file means, while the cross-group differences are larger for several level and band-energy measures. This could reflect recording level, musical content, performance, or setup rather than bass characteristics.
- **Hypothesis:** Distribution-level, level-conditioned comparisons may distinguish repeatable source characteristics from variation caused by unmatched musical content.
- **Decision:** Do not use these raw whole-file differences as IR targets. Implement grouped distributional and recording-level repeatability summaries without requiring matched events, with conditioning or weighting by loudness and pitch when available.
- **Limitations:** The current run pooled all frames by domain and did not condition on loudness or pitch; unmatched content is an intentional design constraint rather than a missing prerequisite. Event counts were unequal (9, 20, 49, and 27), and no SLB-200 comparison is possible until SLB recordings exist.

## 2026-09-23 - Event counts are file-specific diagnostics

- **Observation:** Threshold segmentation produced different event counts for different recordings, and those counts are not expected to correlate across files because musical content and active-region structure vary by file.
- **Finding:** Event count is not a cross-file similarity measure and is not suitable as part of the repeatability noise floor.
- **Decision:** Retain event counts to diagnose segmentation and describe within-file event-derived measurements, but base cross-file comparisons on frame distributions and recording-level summaries.

## 2026-09-23 - Unmatched pitch and recording-level replication

- **Question:** What does the lack of matched pitch/register and complete setup metadata imply for comparison confidence?
- **Observation:** Pitch/register distributions will never be matched, setup metadata will remain incomplete, and each recording contributes many correlated frame rows.
- **Finding:** Frame count cannot serve as replication count. The independent comparison units are recordings and, for broader generalization, source groups; frame distributions remain descriptive within those units.
- **Interpretation:** Permanent unmatched pitch and incomplete setup information do not prevent extraction or descriptive comparison, but they prevent clean attribution of differences to the bass or recording domain.
- **Decision:** Report these as standing limitations, avoid inferential claims based on frame-row counts, and summarize repeatability at recording and source-group level. Use available metadata for descriptive stratification only, never as an assumption that matching exists.

## 2026-09-23 - Unknown and time-varying recording level

- **Question:** Can file-level gain normalization solve the recording-level confound?
- **Observation:** Absolute recording level is not known for the four files, and recording level may change over time within a file.
- **Finding:** A global normalization can create a derived common reference level but cannot recover the original recording level or its time variation.
- **Interpretation:** Original-level measurements must remain primary. Level-dependent feature differences may reflect gain, playing dynamics, recording-chain behavior, or source characteristics, and cannot be separated by normalization alone.
- **Hypothesis:** Features and comparisons that remain stable across observed local-level ranges will be more useful than those whose apparent differences depend strongly on an arbitrary gain choice.
- **Decision:** Preserve original-level outputs, add observed local-level summaries, and label any normalized analysis as derived sensitivity analysis rather than level matching.
- **Limitation:** No calibration reference or reliable absolute level trajectory is currently available for the four acoustic files.

## 2026-09-23 - Contextual metadata is mostly unknown

- **Observation:** For the expected recordings, the player may be known, but bass identity, room, microphone, placement, recording chain, processing, strings, and take conditions may not be recoverable. Even tracks from the same album should not be assumed to share those conditions.
- **Finding:** File-level metadata can be measured directly, but contextual metadata cannot be reconstructed reliably from filenames, album membership, or player identity.
- **Interpretation:** The pipeline can still characterize recordings and compare distributions, but unknown setup and processing remain permanent confounds for attribution and IR generalization.
- **Decision:** Record the player when known, preserve all other contextual fields as unknown unless documented, and treat metadata absence as part of the uncertainty model rather than fabricating controls.
- **Limitation:** Historical recordings with unknown chain, room, microphone, bass, and processing cannot support clean causal claims about bass or instrument characteristics.

## 2026-09-23 - Planned acoustic corpus expansion

- **Question:** How should later recordings change the repeatability analysis?
- **Observation:** More recordings of bass A and bass B will become available, and other acoustic basses may be added later.
- **Finding:** The current four files are an initial candidate sample, not enough to represent the final within-source or across-source variation.
- **Interpretation:** Additional takes improve uncertainty estimates within bass/player groups. New basses should be separate source groups so between-instrument variation is not mistaken for within-source noise.
- **Hypothesis:** Features that remain stable across multiple takes within several source groups are stronger candidates for general acoustic characteristics than features stable only within one pair.
- **Decision:** Keep source-group identity immutable, append later takes as new recordings, and evaluate within-group repeatability separately from between-group differences.
- **Limitation:** The future recordings and their capture metadata are not yet available.

## 2026-09-23 - Durable research-memory layers

- **Question:** What must persist beyond chronological chat and implementation history?
- **Decision:** Separate accumulated findings, experiment evidence, external research, corpus state, and confounds from the existing requirements, architecture, decisions, hypotheses, and research log.
- **Rationale:** A chronological log records activity, but it is not an efficient knowledge base for evidence that accumulates across experiments. A new session must be able to reconstruct both what happened and what is currently believed.
- **Additional principle:** Preserve the chain `Observation -> Finding -> Interpretation -> Hypothesis -> Decision`.
- **Implementation boundary:** Python remains the Phase 1 research/reference implementation, not a commitment to the eventual runtime language.
- **Next action:** Commit the documentation layer, then create the first experiment directory when the pilot corpus is available.

## 2026-09-23 - Corpus protocol and experiment template

- **Question:** What structure is needed before real recordings and experiments arrive?
- **Decision:** Keep the actual corpus catalogue separate from the capture/ingestion protocol, and require every experiment to start from a versioned template.
- **Implementation:** Added `docs/corpus-protocol.md` and `experiments/_template/` with README, manifest, and configuration files.
- **Rationale:** This makes provenance, licensing, split policy, parameters, and interpretation requirements explicit before evidence accumulates.
- **Next action:** Use the template for the first licensed pilot-corpus experiment.

## 2026-09-23 - Initial runtime validation

- **Question:** Does the reference package execute its tested analysis path and CLI output path?
- **Evidence:** `python -m pytest -q` passed with `4 passed`. A disposable synthetic 80 Hz mono WAV was analyzed through the manifest-driven CLI and produced `metadata.json`, `frames.json`, `events.json`, `summary.json`, and `report.md`. Temporary files were removed.
- **Interpretation:** The Phase 1 reference pipeline is executable for the synthetic coverage currently tested.
- **Limitations:** This validates implementation behavior on synthetic material only. It does not establish that any feature discriminates SLB DI from acoustic microphone recordings.
- **Next action:** Run E001 with a small licensed pilot corpus and record its manifest, configuration, provenance, results, and interpretation.

## 2026-09-23 - Documentation handoff audit

- **Question:** Is the repository sufficient to preserve project knowledge across LLM sessions?
- **Audit result:** The core architecture was complete, but the handoff needed an explicit new-session protocol, a distinction between the last clean validated commit and later uncommitted edits, immutable manifest/configuration hashes for experiments, and removal of stale completed work from the implementation plan.
- **Correction:** Added those requirements and template fields. Corrected an inconsistent aubio licensing description in `decisions.md`.
- **Remaining limitation:** The current repository records synthetic validation and design knowledge, but no real corpus findings exist yet.
- **Next action:** Commit these documentation corrections, then begin E001 only after licensed pilot recordings are registered.

## 2026-09-24 - E003 note benchmark and raw audition policy

- **Question:** Does the pitch-aware reference detector reliably separate the individually plucked notes in the reviewed excerpts?
- **Observation:** Four excerpts were manually labeled by ear with approximate boundaries: 3, 3, 3, and 5 notes. The labels are confidence-2 screening labels, not high-precision ground truth. The E003 evaluator tested five frame/hop/threshold settings.
- **Finding:** The best tested setting, `256/64/-45`, produced counts 3/3, 3/3, 3/3, and 3/5, for total absolute count error 2. It still merges notes in `low_01_low.wav`.
- **Interpretation:** The setting is a useful exploratory baseline, but count agreement on three clips does not establish reliable individual-note segmentation or boundary accuracy.
- **Hypothesis:** A selective split rule for long multi-note regions may resolve the remaining merge, but a global increase in permitted split points is unsafe.
- **Probe result:** Raising the global pitch-aware split limit from two to four changed the conservative-setting counts to 5/5/5/5, introducing false splits in the first three excerpts. The change was rejected and the validated two-split implementation restored.
- **Decision:** Keep the current detector as a reference implementation only. Use the E003 benchmark as the gate for future detector changes. Export audition files as raw exact-boundary slices with no fades, context, normalization, or other postprocessing, while retaining the original WAV excerpts as the only analysis inputs.
- **Validation:** The latest direct Python run reported `5 passed`; the benchmark and raw-slice exporter completed successfully; touched-file diagnostics reported no errors.
- **Next action:** Continue with a selective, benchmarked boundary-refinement experiment and expand the manually reviewed set before event-conditioned IR analysis.

## 2026-09-24 - Listener audit refines the low_01 failure mode

- **Observation:** Audition of the raw detector outputs found that `low_01` event 1 contains the first note plus a short fragment of the second; event 2 contains three notes; event 3 contains two notes, with its first note being the second half of the last note in event 2.
- **Finding:** The detector failure is not only a merge of multiple notes. It also places boundaries inside notes and distributes one musical note across adjacent events.
- **Interpretation:** Event count alone understates the segmentation error. The current ordered-count metric can report three events while the event contents have incorrect musical boundaries and overlap the reference note structure.
- **Decision:** Add boundary-inside-note and cross-event note-fragment errors to the benchmark review. Do not evaluate a proposed detector only by matching total note counts.
- **Next action:** Build a boundary-aware evaluation for the reviewed excerpts, then test a selective refinement rule against both count and note-boundary errors.

## 2026-09-24 - Qualitative audit separates three successes from one failure

- **Observation:** The listener found the detector slicing musically correct for `low_02_low.wav`, `bass_friendly_01_bass_friendly.wav`, and `broad_03_broad.wav`. `low_01_low.wav` is the one reviewed excerpt with incorrect internal boundaries and cross-event note fragmentation.
- **Finding:** The current detector is not uniformly failing on the reviewed material. It has three qualitative successes and one known difficult failure.
- **Interpretation:** The benchmark should preserve per-excerpt boundary outcomes rather than reduce the result to a single global count or a blanket accept/reject statement.
- **Decision:** Treat the current detector as a useful reference baseline for the three successful excerpts, while keeping it unvalidated for general note-level use because one failure remains and the reviewed set is small.
- **Next action:** Add per-excerpt boundary judgments and boundary-aware metrics before changing the detector.

## 2026-09-24 - Hard split cap identified as low_01 root cause

- **Question:** Is `low_01` failing because its audio lacks separable note evidence, or because the implementation limits the number of splits?
- **Observation:** At `256/64` with thresholds `-35`, `-38`, and `-45` dB, `low_01` produces one continuous active region from 0.000 to approximately 0.875 seconds. The splitter selects at most two pitch-change breaks because its loop stops at `len(selected_breaks) >= 2`.
- **Finding:** The current implementation mechanically cannot emit more than three pieces from that active region, even when the listener identifies five notes.
- **Interpretation:** The three-event result is partly an algorithmic ceiling, not evidence that the recording cannot be segmented. The earlier four-break probe was confounded by false candidate breaks in other excerpts.
- **Decision:** Treat the two-break cap as a known implementation limitation. Do not raise it globally; replace it with selective break validation using segment duration, pitch stability, and boundary evidence.
- **Next action:** Implement and benchmark a selective multi-break strategy, including boundary-aware metrics and per-excerpt qualitative judgments.

## 2026-09-24 - First envelope-onset retry rejected

- **Probe:** A separate raw-only envelope-rise probe was run on `low_01_low.wav` without changing the production detector. It used local RMS rises, a minimum spacing, and no fades or postprocessing.
- **Observation:** The probe found candidate boundaries near 0.126, 0.261, 0.401, 0.588, and 0.772 seconds, producing six slices. The 0.261-second candidate is a secondary envelope rise rather than a confirmed note boundary.
- **Finding:** Removing the hard split cap alone is insufficient; envelope candidates also require boundary-quality validation.
- **Decision:** Reject the probe output and remove its temporary files. Keep the production detector unchanged at the validated 3/3, 3/3, 3/3, 3/5 benchmark result.
- **Next action:** Combine pitch continuity, onset strength, local valleys, and minimum segment quality in a boundary-aware selective splitter, then benchmark it before exporting audition files.

## 2026-09-24 - Adaptive multi-break splitter succeeds on initial benchmark

- **Implementation:** Removed the fixed two-break ceiling. Nearby pitch candidates are clustered, and long active regions with sparse pitch evidence may receive widely spaced envelope-onset breaks. A one-cluster region receives at most one onset supplement; a two-cluster region requires at least four well-spaced onset candidates before supplementation.
- **Validation:** The existing suite passed with `5 passed`. At `256/64/-45`, the benchmark counts are `3/3`, `3/3`, `3/3`, and `5/5` for the reviewed excerpts, with total absolute count error `0`.
- **Interpretation:** The adaptive rule fixes the known five-note count failure without changing the three previously successful counts. This is stronger evidence than the former count-only baseline, but it does not yet establish precise onset/offset accuracy or generalization.
- **Decision:** Retain the adaptive splitter as the current experimental implementation. Keep raw exact-boundary exports for audition and continue boundary-aware qualitative review.
- **Next action:** Audition the five raw `low_01` outputs, then expand the labeled benchmark and measure boundary errors before treating the detector as reliable.

## 2026-09-24 - Adaptive five-event output still has boundary continuity errors

- **Observation:** The listener found event 1 contains a short tail of note 2; event 2 is otherwise correct but lacks the initial short part of note 2; event 3 contains two notes and its second continues into event 4; event 4 contains one note that began in event 3; event 5 is correct.
- **Finding:** The adaptive splitter reaches the correct five-event count but still places boundaries inside notes and distributes note energy across adjacent slices.
- **Interpretation:** Count error is now zero on this excerpt, while boundary error remains nonzero. The event count metric is therefore insufficient for accepting the detector.
- **Decision:** Retain the adaptive splitter as an experimental improvement, but do not claim precise note segmentation. Add boundary continuity, cross-event fragment, onset, and offset metrics to the benchmark.
- **Next action:** Refine candidate break positions toward attack/onset boundaries and evaluate boundary errors across all reviewed excerpts.

## 2026-09-24 - Imperfect events can be retained but disqualified

- **Observation:** Some detector outputs may remain imperfect even after automated refinement, especially in difficult transitions.
- **Finding:** Perfect slicing of every event is not required if unusable events can be identified and excluded without deleting their evidence.
- **Decision:** Preserve all detector outputs and classify them as `usable`, `ambiguous`, or `disqualified` for downstream analysis. Disqualified events remain available for detector evaluation and failure analysis but are excluded from event-conditioned feature analysis.
- **Interpretation:** Human audition can focus on difficult or high-impact cases, while clear cases can be classified through automated boundary metrics and confidence rules.

## 2026-09-24 - Manual usability audit recorded

- **Observation:** The listener reviewed all 14 adaptive detector outputs in the four-excerpt benchmark.
- **Finding:** All events in `low_02_low.wav`, `bass_friendly_01_bass_friendly.wav`, and `broad_03_broad.wav` were judged usable. In `low_01_low.wav`, events 1 and 2 were ambiguous, events 3 and 4 were disqualified, and event 5 was usable.
- **Decision:** Store these decisions in `experiments/E003/listener_audit.csv`; retain all audio outputs, exclude disqualified events from downstream event-conditioned analysis, and use the audit to calibrate automated triage.

## 2026-09-24 - Bass C unlabeled stress test

- **Observation:** The new `bass_c` file produced 77 events at `256/64/-45` and 175 events at `128/32/-38`. The shortest detected durations were 0.0029 and 0.0007 seconds, respectively.
- **Finding:** The new source is useful for stress-testing parameter sensitivity, but these counts cannot be interpreted as note counts without manual reference labels.
- **Decision:** Keep bass C outside the labeled E003 benchmark for now. Use it only as an unlabeled diagnostic until a small manually reviewed subset is created.

## 2026-09-24 - Bass C listener audit identifies long-block failure

- **Observation:** The listener audited seven representative raw bass C outputs. One was silence, three contained one acceptable note, two contained one note plus possible short-note noise at the end, and one approximately 10-second event contained an estimated 30-50 notes, too many to count reliably.
- **Finding:** The detector can isolate usable events in bass C, but it can also leave a long multi-note active region as one event. The top-level count of 77 events therefore does not imply note-level segmentation quality.
- **Decision:** Record the results in `experiments/E003/bass_c_listener_audit.csv`; classify the silence and multi-note block as disqualified, the two possible short-note cases as ambiguous, and the three isolated notes as usable.
- **Next action:** Target recursive splitting of long active regions and audition only the resulting ambiguous or high-duration cases.

## 2026-09-24 - Acoustic candidate corpus expanded

- **Observation:** Three additional bass A files and one bass D file are available: bass A takes 3-5 are 386.87 s, 261.77 s, and 204.60 s; bass D take 1 is 8.72 s. All are stereo 44.1 kHz 16-bit PCM WAVs.
- **Finding:** The external candidate inventory now contains nine recordings across four source groups: A, B, C, and D.
- **Decision:** Register bass A files as additional takes in `bass_a`; register bass D as a new `bass_d` source group. Preserve all files outside Git and keep unknown player/capture metadata explicit.
- **Next action:** Run the same manifest-driven diagnostics on the expanded inventory, without treating source-group counts as repeatability evidence until metadata and within-group coverage are reviewed.

## 2026-09-24 - Expanded source slicing scan

- **Observation:** At `256/64/-45` with bounded long-event refinement, bass A3 produced 2,187 events with 776 under 20 ms; A4 produced 1,018 with 31 under 20 ms; A5 produced 1,395 with 728 under 20 ms; bass D1 produced 50 with 25 under 20 ms.
- **Finding:** The expanded files expose strong source-to-source variation in fragmentation and event counts. Bass D is shorter and less fragmented than the new bass A files, while A3 and A5 contain many short artifacts.
- **Decision:** Preserve a 12-file shortest/longest audit set under `experiments/E003/expanded_source_audit/`; do not interpret counts as note counts.
- **Next action:** Use the audit to determine whether the current duration guard is too permissive for bass A or whether those recordings require different thresholds or source-specific escalation.

## 2026-09-24 - Expanded source listener audit

- **Observation:** The 12 shortest/longest audit slices contained three silence cases, one clear single note, double stops/simultaneous notes, and dense passages estimated at 10-16 or 12-16 fast notes.
- **Finding:** Most selected long events are not monophonic note events: they contain polyphony, simultaneous tails, or fast note sequences. The bass D long event was a clear single note; its longest selected event contained a short upbeat note followed by another note.
- **Decision:** Record the judgments in `experiments/E003/expanded_source_listener_audit.csv`. Disqualify silence and polyphonic/multi-note slices for the current monophonic event analysis, while retaining them as evidence about articulation and future polyphonic analysis.
- **Next action:** Separate monophonic-note, double-stop, fast-passage, and silence strata before judging detector accuracy on the expanded corpus.

## 2026-09-24 - Typical-duration audit sample created

- **Observation:** The shortest/longest audit was failure-biased, so eight additional raw slices were selected from the ordinary 0.08-0.8 second duration stratum, two each from bass A takes 3-5 and bass D take 1.
- **Decision:** Preserve the typical sample under `experiments/E003/expanded_source_typical_audit/` and use its listener results to estimate ordinary-event usability separately from stress-case performance.

## 2026-09-24 - Typical-duration listener audit

- **Observation:** The eight ordinary-duration slices contained four usable single notes, including two glissandi; one four-note merge; one short-upbeat two-note transition; and two very silent single-note candidates.
- **Finding:** Glissando is still one note and should not be treated as segmentation ambiguity. Short-upbeat transitions and very-silent cases require separate handling.
- **Decision:** Record 4 usable, 3 ambiguous, and 1 disqualified in `experiments/E003/expanded_source_typical_listener_audit.csv`; retain glissando as an articulation label.

## 2026-09-24 - Real-recording hit-rate sample created

- **Observation:** A stratified sample was generated from all nine actual external recordings, with four duration/risk strata per source file.
- **Result:** 36 raw exact-boundary detector slices were generated and recorded in `experiments/E004/real_hit_rate_sample/manifest.json`.
- **Decision:** Use this real-recording sample for hit-rate measurement; do not mix it with synthetic tests or the deliberately stress-biased E003 audit samples.
- **Next action:** Audit the 36 slices by source group and classify each as usable, ambiguous, or disqualified, then calculate hit rate with strata reported separately.

## 2026-09-24 - Real-recording hit-rate audit completed

- **Observation:** The 36-slice audit from all nine real external recordings contains 12 usable and 24 disqualified events, with no ambiguous labels.
- **Finding:** Overall usable rate is `33.3%`. By stratum: short-risk `0/9`, lower-typical `3/9`, median-typical `4/9`, upper-typical `5/9`.
- **Interpretation:** The detector is currently below the desired usable-event rate, and short-risk output is consistently unusable. The ordinary-duration strata are better but still below a high-accuracy target.
- **Limitation:** The sample was deliberately stratified by duration/risk, so `33.3%` is not a natural prevalence estimate. Source-level and stratum-level rates must remain separate.
- **Next action:** Improve artifact suppression and event-type classification, then repeat the same real-recording audit with an unchanged sampling protocol.

## 2026-09-24 - Positive-control audit sample created

- **Observation:** The overall real-recording hit rate is low and the first sample was deliberately stratified across risk levels.
- **Decision:** Create an 18-slice positive-control sample from all nine real recordings, selecting ordinary-duration, fast-attack, high-peak events that the detector would be most likely to trust.
- **Purpose:** Measure the precision of automatic high-confidence selection separately from overall event usability.
- **Status:** Files and direct-link index exist under `experiments/E004/positive_control_sample/`; human judgments are pending.

## 2026-09-24 - Positive-control audit completed

- **Observation:** The listener classified 18 events selected as the detector's most trustworthy ordinary-duration/high-signal candidates: 9 usable, 9 disqualified, and 0 ambiguous.
- **Finding:** Automatic high-confidence selection precision is only `50%`. Many-note merges and duophonic events survive the current duration/attack/peak filters.
- **Decision:** Do not trust the current heuristic confidence selection for automatic downstream inclusion. Preserve the result as the baseline for the algorithm bake-off.
- **Next action:** Benchmark independent event algorithms and add event-class/polyphony evidence before designing confidence fusion.

## 2026-09-24 - E005 algorithm bake-off started

- **Implementation:** Created `experiments/E005/` with manifest, configuration, README, and a reproducible baseline runner.
- **Observation:** On the four shared real excerpts, the recursive detector produced counts `3, 3, 3, 5`; librosa onset peak-picking produced `5, 2, 3, 3`.
- **Finding:** The independent onset baseline does not consistently improve event counts; it over-detects one excerpt and under-detects two.
- **Decision:** Do not select either method based on count alone. Preserve both raw outputs and run Basic Pitch next, followed by Essentia/aubio where practical.

## 2026-09-24 - E005 Basic Pitch comparison

- **Environment:** Dedicated `.venv-basicpitch` environment; inference completed successfully.
- **Observation:** Basic Pitch returned default event counts `2,2,2,2` and stricter counts `1,1,1,1` on the four shared excerpts.
- **Finding:** Basic Pitch under-segments this short-note benchmark under both tested settings, despite producing plausible candidate note events in the earlier pilot.
- **Decision:** Preserve its raw output but do not treat Basic Pitch as an adequate standalone event detector for this material. Continue the bake-off with Essentia/aubio where practical.

## 2026-09-24 - Bake-off parameter tuning requirement

- **Observation:** The first E005 candidate results used baseline settings: the current detector's selected configuration, librosa onset defaults, and Basic Pitch default/stricter settings.
- **Finding:** Baseline comparisons do not establish algorithm rankings because event boundaries are sensitive to source-specific parameters.
- **Decision:** Tune each candidate on development excerpts, preserve held-out excerpts for final evaluation, and score false boundaries, splitting, missed boundaries, ambiguity, and usable-event yield rather than count alone.

## 2026-09-24 - First E005 development/holdout tuning run

- **Setup:** Development excerpts were `low_02`, `bass_friendly`, and `broad`; `low_01` was held out.
- **Observation:** The recursive detector selected `256/64/-45` with count error 0 on development and holdout. Librosa selected `delta=0.2`, `wait=10`, with count error 3 on development and 2 on holdout.
- **Finding:** The recursive detector's count setting transfers better on this small split, but count transfer does not establish boundary quality.
- **Decision:** Preserve the tuning result in `experiments/E005/tuning_results.json`; continue evaluating boundary precision and usable-event yield rather than optimizing count alone.

## 2026-09-24 - Basic Pitch parameter tuning

- **Observation:** A four-setting Basic Pitch sweep selected the default configuration with development count error 3 and holdout count error 3. A permissive short-note configuration produced development error 106.
- **Finding:** Lower Basic Pitch thresholds do not automatically recover useful short events; they can sharply increase over-detection.
- **Decision:** Keep Basic Pitch default settings as its current benchmark configuration, preserve all raw outputs, and treat it as a candidate generator rather than a standalone slicer.

## 2026-09-24 - E005 unattended bake-off completed

- **Scope:** Recursive detector, librosa onset, aubio, and Basic Pitch were run/tuned on the same real excerpts with development/holdout separation.
- **Results:** Recursive `0/0` count error; librosa `3/2`; aubio `0/2`; Basic Pitch `3/3` for development/holdout. Full report: `experiments/E005/BAKEOFF_REPORT.md`.
- **Limitations:** These are count-transfer results only. Essentia was blocked by its Windows build, and MuScriptor, MT3, and commercial references were not run.
- **Decision:** Keep the recursive detector as baseline, retain aubio as a promising next boundary-audit candidate, and do not select a final algorithm until false-boundary, split/merge, and usable-event metrics are measured.

## 2026-09-24 - E005 measurements consolidated

- **Observation:** Ordered measurements over approximate E003 onsets are: recursive count error 0 / mean onset error 52 ms; aubio tuned 2 / 116 ms; Basic Pitch 6 / 222 ms; librosa 5 / 280 ms.
- **Human evidence:** Usable rates are 10/14 (71.4%) for E003 listener-audited outputs, 12/36 (33.3%) for the stratified real-recording E004 sample, and 9/18 (50%) for positive controls.
- **Limitation:** Candidate timing metrics and human usability metrics are not interchangeable; only the recursive candidate has complete listener judgments on the shared E003 outputs.
- **Decision:** Use the recursive detector as the current count/onset baseline, keep aubio as the strongest independent candidate for further human boundary audit, and do not claim final algorithm superiority yet.

## 2026-09-24 - Tailored algorithm usage policy

- **Decision:** Route the recursive detector as the primary conservative boundary source, use tuned aubio as secondary onset evidence for long/uncertain events, and retain Basic Pitch for candidate proposals and pitch context.
- **Exclusion policy:** Exclude or manually review silence, polyphony, fast passages, merged events, and unresolved boundaries for strict monophonic analysis.
- **Boundary:** Do not fuse detector boundaries until individual candidates have comparable human boundary audits. The current high-confidence filter precision is only 50 percent.

## 2026-09-24 - Tailored routing prototype executed

- **Implementation:** Ran `experiments/E005/execute_strategy.py` on the shared excerpts using recursive primary events, tuned aubio onset evidence, and Basic Pitch candidate context.
- **Result:** `low_02` routed 3 candidates; bass-friendly routed 2 candidates and 1 ambiguous; broad routed 2 candidates and 1 ambiguous; `low_01` routed 5 candidates. No event was auto-declared scientifically usable.
- **Decision:** Keep routing as a review-prioritization layer, not a final fusion or acceptance mechanism.

## 2026-09-24 - Remaining candidate environment check

- **Observation:** The active `.venv` contains librosa and the repository/basic-pitch tooling, but not Essentia, aubio, or madmom.
- **Decision:** Do not interpret missing packages as algorithm failures. Create a compatible dedicated environment with exact versions before running those candidates.

## 2026-09-24 - Aubio bake-off result and Essentia build blocker

- **Environment:** Created `.venv-audioalgorithms` from the Basic Pitch-compatible runtime. aubio 0.4.9 installed successfully.
- **Observation:** Aubio default onset detection returned `5,6,6,7` events on the four E005 excerpts, versus reviewed counts `3,3,3,5`.
- **Finding:** Aubio's default onset detector over-detects this benchmark and requires tuning before comparison is fair.
- **Limitation:** Essentia's available source distribution failed to build with an internal `IndexError`; no Essentia result was obtained.
- **Decision:** Preserve aubio raw output in `experiments/E005/aubio_results.json`; treat Essentia as an environment blocker, not an algorithm failure.

## 2026-09-24 - Aubio parameter tuning

- **Observation:** A development sweep over aubio onset methods and thresholds selected `specdiff` at threshold `0.7` with development count error `0` and holdout count error `2`.
- **Finding:** Aubio can transfer count behavior after tuning better than its default configuration on this small split.
- **Limitation:** Count transfer does not establish onset boundary precision, false split rate, or usable-event yield.
- **Decision:** Preserve the tuning result in `experiments/E005/aubio_tuning_results.json`; evaluate its raw boundaries against the listener audits before considering it a candidate for fusion.

## 2026-09-24 - MuScriptor model-access blocker

- **Observation:** MuScriptor 0.3.0 installed successfully in `.venv-muscriptor`, and its CLI exposes transcription, model, and decoding parameters.
- **Blocker:** The MuScriptor model weights are gated on Hugging Face and require license acceptance plus machine authentication. No token or authenticated model access is available in this session.
- **Decision:** Do not fabricate a MuScriptor result. Record the installation and CLI verification, and resume the benchmark only after model access is authorized.

## 2026-09-25 - MuScriptor bake-off and tuning

- **Environment:** Authenticated `.venv-muscriptor`; MuScriptor small model downloaded and ran on all four shared excerpts.
- **Observation:** Default/greedy counts were `2,11,2,27`. A four-variant decoding sweep found `cfg_coef=1.5` with greedy or beam-2 counts `5,3,2,4`, development count error `3`, holdout error `1`.
- **Finding:** MuScriptor improves substantially with guidance tuning on this split, but its count pattern still does not establish event-boundary quality.
- **Decision:** Retain MuScriptor as a serious independent candidate for human boundary audit; preserve all raw JSON outputs and tuning metadata.

## 2026-09-25 - Transformability question clarified

- **Observation:** Exact sample-synchronous performances by an acoustic upright bass and an SLB-200 are not realistically available. The research goal is to understand whether acoustic note-life behavior can be represented by a fixed IR.
- **Finding:** A fixed IR does not understand note identity or note state. It can alter harmonic balance and waveform evolution through an LTI filter, but cannot condition itself on register, dynamics, articulation, or note age.
- **Interpretation:** Unpaired events can test conditional distribution-level spectral differences, but cannot identify a unique event-specific transfer function. Exact pairing is not necessary for a candidate statistical transform, but controlled repeated material is needed for validation.
- **Decision:** Make transformability the next gate. Test whether conditional time-frequency differences are stable and filter-addressable before investing further in perfect event slicing or IR optimization.

## 2026-09-25 - E006 EUB proof of concept executed

- **Observation:** The existing unified pipeline processed one NS Design direct/EUB recording and 16 representative Ergo EUB recordings after explicit float-to-PCM16 derivation. It produced 4,620 frame rows and 243 threshold events.
- **Finding:** The pipeline executes on both EUB source types without an EUB-specific feature path. Event counts remain diagnostics until audited.
- **Boundary:** The NS microphone track is not an acoustic target and is excluded from transformation interpretation.
- **Decision:** Proceed with a representative NS/Ergo event-quality audit, then compare EUB source-domain structure before any acoustic-vs-EUB transform hypothesis.

## 2026-09-25 - E006 representative audit set prepared

- **Implementation:** Generated raw exact-boundary audit slices from NS shortest/median/longest events and representative Ergo events across two phrase groups and `f`/`mf`/`p` source codes.
- **Location:** `experiments/E006/audit_slices/AUDIT_LINKS.md` and `manifest.json`.
- **Status:** Human audit pending; no EUB source-domain or acoustic-vs-EUB interpretation should be made before review.

## 2026-09-25 - E006 representative audit completed

- **Observation:** The listener audited nine representative EUB slices: NS had two usable events and one silence; Ergo had two usable events, three noise/silence cases, and one silence.
- **Finding:** 4/9 selected EUB events were usable; failures were mostly silence/noise rather than confirmed note merges.
- **Limitation:** The sample is small and duration-selected, so it is not an EUB-wide hit-rate estimate.
- **Decision:** Retain the audit in `experiments/E006/audit_slices/listener_audit.csv`; expand the EUB audit before interpreting NS-vs-Ergo source-domain structure.

## 2026-09-25 - E006 expanded source-balanced audit prepared

- **Implementation:** Generated 19 raw audit slices: one high-signal ordinary-duration event per E006 recording plus NS shortest/longest controls.
- **Location:** `experiments/E006/audit_slices_expanded/AUDIT_LINKS.md` and `manifest.json`.
- **Status:** Human judgments pending; no EUB-vs-EUB interpretation should be made until this expanded audit is complete.

## 2026-09-25 - E006 expanded audit completed

- **Observation:** The listener audited all 19 source-balanced NS/Ergo slices: 15 usable and 4 disqualified.
- **Finding:** Usable yield was 15/19 (`78.9%`) in this selected high-signal sample. Failures were three Ergo noise/too-short events and one NS silence control; no broad overlap/polyphony failure was reported in this sample.
- **Limitation:** This is a selected high-signal audit, not an unbiased EUB-wide accuracy estimate.
- **Decision:** The existing pipeline is sufficiently promising to proceed with EUB source-domain characterization while retaining event quality labels and excluding disqualified events.

## 2026-09-25 - E007 first acoustic-vs-EUB descriptive comparison

- **Observation:** The first 30 seconds of nine acoustic candidates were analyzed with the existing pipeline and compared descriptively to E006 NS/Ergo EUB frames.
- **Finding:** Acoustic 30-second windows averaged RMS -25.246 dB, centroid 130.879 Hz, rolloff 166.663 Hz, flux 1.025, f0 80.803 Hz, and harmonicity -9.135 dB. EUB combined frames averaged RMS -35.415 dB, centroid 304.491 Hz, rolloff 534.270 Hz, flux 0.139, f0 104.138 Hz, and harmonicity -9.460 dB. NS and Ergo also differed descriptively.
- **Interpretation:** These differences are confounded by level, content, articulation, window selection, capture chain, and source-group coverage. They are not acoustic/EUB causal findings or IR targets.
- **Decision:** Use E007 only as pipeline/source-domain evidence. Condition future comparisons by register, local level, articulation, and source group before testing transformability.

## 2026-09-25 - Conditional per-event differences are feasible without sync

- **Clarification:** Exact acoustic/EUB note pairing is not required to compare event populations conditionally.
- **Decision:** Use measured register, local level, articulation, and onset-relative phase to compare acoustic and EUB event trajectories. Treat repeated conditional differences as candidate filter-addressable effects, not as one-to-one transfer ratios.
- **Next action:** Build the conditional event-level summaries before deciding whether a fixed IR, IR bank, or time-varying model is justified.

## 2026-09-25 - First conditional event analysis is coverage-limited

- **Implementation:** Built `experiments/E007/event_features.csv` with four onset-relative phases and `conditional_comparison.json` with register/level bins.
- **Observation:** 3,201 event rows were generated, but only three register/level cells contained both acoustic and EUB events; all were high-register by the current estimator, and one had six EUB events.
- **Finding:** Conditional comparison is technically feasible without synchronization, but the current corpus/event labels do not yet provide balanced register coverage.
- **Decision:** Treat current deltas as exploratory only. Improve event quality, pitch/register coverage, and articulation metadata before estimating candidate IR effects.

## 2026-09-25 - SLB-200 acquisition made highest priority

- **Observation:** The corpus has acoustic, NS Design EUB, and Ergo EUB material but no registered SLB-200 recordings.
- **Finding:** Further EUB/acoustic work can validate methodology, but cannot answer the governing SLB-200 transformation question without SLB source material.
- **Decision:** Prioritize multiple SLB-200 takes across register, dynamics, articulation, and setup, with at least one held-out take. Follow `docs/recording-acquisition-plan.md` for provenance and capture metadata.

## 2026-09-25 - First SLB-200 candidate registered

- **Observation:** `C:\IR audio\slb200\vincents 1.wav` is available as a stereo 44.1 kHz 16-bit PCM WAV of 284 seconds with SHA-256 `138b5de97de26392c368c01e98c3804fcf040501cd35526f618239f7c82fd46e`.
- **Finding:** The project now has one SLB-200 candidate for file-quality checks and exploratory event analysis, but not enough documented material for a source-domain comparison or held-out transformation evaluation.
- **Decision:** Register it as `slb200_vincents_take_1` in candidate status, preserve the original outside Git, and keep metadata and permission status explicit until confirmed.

## 2026-09-26 - Revised SLB event slicing in E009

- **Observation:** The existing 578-event SLB slicing pass included short nonperiodic fragments and pitch evidence from 256-sample recursive windows, too short to resolve bass fundamentals at 44.1 kHz.
- **Implementation:** Recursive refinement now uses 2048-sample windows with a 256-sample hop; pitch-step splits require a nearby envelope onset. Event outputs include periodic-pitch quality metadata, with only strict short/low-level/nonperiodic fragments marked disqualified.
- **Finding:** E003 still matches its selected count benchmark exactly (`3, 3, 3, 5`), and the SLB rerun produces 449 events: 5 strict fragment disqualifications and 2 pitch-unconfirmed cases. The synthetic glissando test stays intact as one event.
- **Decision:** Preserve E008 raw slices and browser judgments; keep revised slices and review state separate under E009. Continue to treat E009 boundaries, polyphony flags, and quality labels as provisional pending review.

## 2026-09-25 - Per-event evidence prioritized over whole-piece averages

- **Hypothesis:** Per-event conditional behavior is more relevant to the eventual IR target than averages over entire pieces of music.
- **Rationale:** Whole-piece averages mix register, loudness, articulation, phrase content, player behavior, and capture conditions. These mixtures can hide or manufacture apparent source-domain differences.
- **Decision:** Treat whole-recording averages as secondary QC/context. Prioritize event-level spectral and temporal trajectories conditioned on register, local level, articulation, and onset-relative phase.

## 2026-09-25 - E006 first NS-vs-Ergo descriptive comparison

- **Observation:** The unified summary shows NS mean RMS -32.100 dB versus Ergo -39.569 dB; spectral centroid 153.701 versus 571.286 Hz; rolloff 213.415 versus 1000.826 Hz; spectral flux 0.226 versus 0.074; f0 75.317 versus 133.482 Hz; f0 confidence 0.587 versus 0.741; harmonicity -10.371 versus -8.627 dB.
- **Finding:** The pipeline exposes measurable source-group differences in this proof-of-concept set.
- **Interpretation:** These differences may reflect content, articulation, level, instrument/source construction, recording chain, and processing. They are not generic EUB characteristics or acoustic-target evidence.
- **Decision:** Keep the result descriptive and proceed with conditional, repeatability-aware EUB characterization before acoustic-vs-EUB transformation analysis.

## 2026-09-24 - Bass C failure traced to localized under-segmentation

- **Observation:** At `256/64/-45`, bass C contains four threshold-active regions. The first lasts approximately 47.864 seconds. The detector produces 77 outputs overall, but its first output lasts 10.0325 seconds and contains an estimated 30-50 notes.
- **Finding:** The detector is identifying activity and subdividing the long region, but it misses many internal boundaries near the beginning of that region. The 77-event total therefore hides a severe localized merge.
- **Interpretation:** The failure is caused by the interaction of long contiguous activity with incomplete internal onset/pitch evidence, not by an absence of audible note structure.
- **Decision:** Add a maximum event-duration warning and recursively reprocess unusually long outputs; do not treat a high top-level event count as evidence of note-level success.

## 2026-09-24 - Bass C parameter sweep separates resolution from fragmentation

- **Observation:** On the original bass C recording, `64/16/-35` produced 1,220 events with 903 shorter than 20 ms and a longest event of 1.034 s. `256/64/-35` produced 192 events with a longest event of 1.617 s. `128/32/-38` produced 175 events with a longest event of 5.777 s. The baseline `256/64/-45` produced 77 events with a longest event of 10.032 s.
- **Finding:** The 10-second merge is parameter-sensitive: finer resolution reduces long merges, but aggressive settings create many false fragments. No single global setting is adequate.
- **Interpretation:** The next solution should apply fine-resolution analysis selectively to unusually long active regions, then filter or disqualify short artifacts, rather than making the whole recording use the most aggressive setting.
- **Decision:** Preserve `256/64/-45` as the conservative baseline and prototype recursive long-event refinement with provenance for the parent event and child events.

## 2026-09-24 - Recursive retry of bass C long event

- **Experiment:** Reprocessed only the 10.0325-second `bass_c_event_07_source_index_001.wav` parent with `256/64/-35`, then discarded child events shorter than 20 ms.
- **Result:** 31 raw child slices remained; the longest was 0.83 seconds, compared with the original 10.0325-second merged event. All child files and parent provenance are recorded in `experiments/E003/bass_c_recursive_event_07/manifest.json`.
- **Interpretation:** Selective recursive refinement is substantially better than applying aggressive settings to the entire bass C recording, but the 31 children still require listener audit before being treated as notes.
- **Next action:** Audit a representative spread of the 31 children, then adjust the recursive minimum-duration and boundary rules based on observed false splits and merges.

## 2026-09-24 - Bounded long-event refinement enabled

- **Implementation:** `detect_events` now recursively reprocesses events longer than 1.5 seconds once at `256/64/-35`, filters children shorter than 20 ms, and falls back to the parent when refinement produces no useful children.
- **Validation:** Existing tests pass. Bass C changes from 77 events with a 10.032-second maximum event to 144 events with a 1.474-second maximum event. The former 10-second region becomes 31 production child outputs.
- **Decision:** Keep this bounded refinement enabled as the current production experiment. Preserve parent-child provenance and continue human auditing of representative child events.

## 2026-09-24 - Second bounded recursion level retained

- **Implementation:** Long-event refinement now escalates events over 0.75 seconds for at most two levels, using `256/64/-35` and filtering children shorter than 20 ms.
- **Validation:** E003 remains at exact counts `3/3, 3/3, 3/3, 5/5`; the suite passes with `5 passed`. Bass C improves from 144 to 161 events and its longest event decreases from 1.474 to 1.387 seconds, with two sub-20 ms fragments.
- **Decision:** Retain the second bounded level. It improves the stress case without changing the labeled benchmark counts.

## 2026-09-24 - Spectral-flux candidate experiment rejected

- **Probe:** Added normalized spectral-flux onset candidates to the long, pitch-sparse fallback path.
- **Result:** E003 best-setting count error worsened from 0 to 3, with `low_01` changing from 5 to 8 events. Bass C changed only marginally.
- **Decision:** Remove the spectral-flux addition and restore the validated adaptive pitch/envelope splitter. Do not treat an independent onset signal as beneficial without candidate agreement or stronger filtering.

## 2026-09-24 - Librosa onset detector probe

- **Probe:** Tested the installed `librosa 1.0.0` onset-strength and peak-picking detector on the four E003 excerpts.
- **Result:** It returned 3 onsets for the 5-note `low_01`, 2 for `bass_friendly_01_bass_friendly`, and 3 for `broad_03_broad`; it also produced extra early onsets in `low_02_low`.
- **Decision:** Do not adopt librosa onset detection as a standalone slicer. Use it only as a possible candidate source inside a globally scored hybrid method.

## 2026-09-24 - Global boundary optimizer probe rejected

- **Probe:** Implemented an isolated dynamic boundary optimizer over current detector boundaries and envelope-onset candidates, with penalties for boundary movement and long segments.
- **Result:** Proposed boundaries improved on `low_02` and `low_01`, but moved incorrectly on the bass-friendly and broad excerpts.
- **Decision:** Do not integrate the optimizer into production. It needs stronger pitch/transition evidence and per-class constraints before it can replace the current detector.

## 2026-09-24 - Bass C recursive v2 audit

- **Observation:** The v2 audit found one note in children 1, 5, and 20; two hammer-on notes in child 3; four notes in child 2; two notes in children 10 and 30; and five notes in child 31.
- **Finding:** The v2 refinement produces usable isolated-note children, but four of the eight audited children remain merged or articulation-ambiguous.
- **Decision:** Store the corrected v2 judgments in `experiments/E003/bass_c_recursive_v2_listener_audit.csv`: 3 usable, 1 ambiguous, 4 disqualified.
- **Next action:** Recursively reprocess disqualified v2 children and treat hammer-on articulation as a separate event class.

## 2026-09-24 - Bass C recursive v3 audit

- **Observation:** V3 children 1, 5, and 20 contained one note; child 3 contained two hammer-on notes; child 30 was possibly one note but uncertain; children 2 and 10 contained two or four merged notes; child 35 was duophonic, with one voice playing two notes while another sustained one.
- **Finding:** The second recursion level preserves the three clear usable examples, reduces some merged material, and exposes duophonic content that should not be forced into a monophonic slicer.
- **Decision:** Store the v3 judgments in `experiments/E003/bass_c_recursive_v3_listener_audit.csv`: 3 usable, 2 ambiguous, 3 disqualified.
- **Next action:** Keep monophonic, hammer-on, and duophonic events as separate analysis strata rather than treating all multi-note material as one detector problem.

## 2026-09-24 - Recursive bass C child audit

- **Observation:** The listener audited eight representative children from the recursive pass: children 1, 5, and 20 contained one note; child 3 contained two notes with hammer-on articulation; child 31 contained four and possibly five notes; children 2, 10, and 30 contained 4, 3, and 2 merged notes respectively.
- **Finding:** Recursive refinement materially reduces the 10-second merge, but several child events still contain multiple notes.
- **Decision:** Preserve the child audit in `experiments/E003/bass_c_recursive_listener_audit.csv`; classify three children as usable, three as disqualified, and two as ambiguous.
- **Next action:** Recursively reprocess only multi-note children, while preserving parent-child provenance and treating hammer-on cases separately from plucked-note segmentation.

## 2026-09-24 - Second recursive pass is selectively useful

- **Observation:** Reprocessing audited children with `128/32/-38` left most merged children as one event. `64/16/-45` split child 2 into two events and child 31 into two events, but left children 10 and 30 merged.
- **Finding:** Recursive finer-resolution analysis improves some children but does not solve the hardest multi-note merges.
- **Interpretation:** The remaining failures require onset/pitch-transition evidence or another detector, not only smaller frames and hops.
- **Decision:** Keep recursive refinement as a selective stage, but add a long/merged-child escalation path that can invoke onset or alternate candidate generation and then apply usability classification.

## 2026-09-24 - Third acoustic player/bass candidate added

- **Observation:** A new external file was added at `C:\IR audio\acoustic\bass C\5.wav`. Verified metadata is stereo 44.1 kHz 16-bit PCM WAV, 48.16 seconds, SHA-256 `fc8b93807bc8e33e5da50e6691b884d844aec72e97bbcf55fb6befcbfa8c6c7f`.
- **Finding:** This is a distinct third source group, not an additional take for bass A or bass B.
- **Interpretation:** The file can expand the candidate acoustic repeatability inventory, but one file does not establish within-group repeatability for bass C and unknown capture metadata remain confounds.
- **Decision:** Register it as `acoustic_bass_c_take_1` / source group `bass_c`, preserve it outside Git, and leave player, microphone, room, chain, and other contextual metadata explicitly unknown.
- **Next action:** Verify permission and metadata, then analyze it through the same manifest-driven pipeline without pooling it into bass A or bass B.
