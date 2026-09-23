# Research Log

## 2026-09-23 - Repository and Phase 1 foundation

- **Question:** What should be built before attempting IR optimization?
- **Decision:** Establish a unified corpus-characterization pipeline first.
- **Implemented:** Python package for WAV metadata, framing, initial features, event detection, manifest analysis, summaries, and reports.
- **Evidence:** Source diagnostics were clean. Runtime validation was completed later: the full suite passed with 4 tests, and a synthetic WAV passed through the CLI.
- **Interpretation:** The code is a validated reference scaffold, not a validated scientific result.
- **Confidence:** High for the architectural direction and basic execution path; low for the scientific usefulness of any current descriptor.
- **Next action:** Add real licensed pilot recordings and run E001.

## 2026-09-23 - Feature selection strategy

- **Question:** Should the initial feature list represent prior beliefs about relevance?
- **Decision:** Expand a broad, testable candidate measurement bank and use corpus evidence to evaluate relevance.
- **Interpretation:** Easy testability determines initial inclusion, not scientific importance. Library availability is not evidence of relevance.
- **Risks:** Multiple comparisons, redundant features, pitch and level confounds, and recording-chain effects.
- **Next action:** Maintain feature IDs and evaluate repeatability, conditional differences, redundancy, and confound sensitivity.

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

## 2026-09-23 - Unknown and time-varying recording level

- **Question:** Can file-level gain normalization solve the recording-level confound?
- **Observation:** Absolute recording level is not known for the four files, and recording level may change over time within a file.
- **Finding:** A global normalization can create a derived common reference level but cannot recover the original recording level or its time variation.
- **Interpretation:** Original-level measurements must remain primary. Level-dependent feature differences may reflect gain, playing dynamics, recording-chain behavior, or source characteristics, and cannot be separated by normalization alone.
- **Hypothesis:** Features and comparisons that remain stable across observed local-level ranges will be more useful than those whose apparent differences depend strongly on an arbitrary gain choice.
- **Decision:** Preserve original-level outputs, add observed local-level summaries, and label any normalized analysis as derived sensitivity analysis rather than level matching.
- **Limitation:** No calibration reference or reliable absolute level trajectory is currently available for the four acoustic files.

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
