# Architectural Decisions

## Decision status vocabulary

Use `accepted`, `rejected`, `deferred`, or `superseded`. Rejected and superseded approaches remain documented so the project does not repeatedly rediscover them.

## 2026-09-23: Python reference pipeline first

- Status: accepted for Phase 1; not a commitment to the eventual runtime language.

**Decision:** Build a small Python reference implementation before a native C++ application.

**Rationale:** The first milestone is research iteration and reproducibility, not real-time deployment. Python makes manifests, numerical experiments, synthetic tests, and report generation inexpensive. The analysis interfaces are kept modular so a later C++ implementation can replace individual components without changing the corpus contract.

**Boundary:** The eventual studio, plugin, embedded, or real-time implementation may use C++, Rust, or another suitable language. Phase 1 Python code is the research/reference implementation.

## 2026-09-23: NumPy for numerical primitives

**Decision:** Use NumPy for arrays, FFTs, windows, and descriptive statistics.

**Rationale:** It is mature, widely deployed, testable, and avoids implementing FFT/STFT primitives. The initial project does not need a large audio framework.

## 2026-09-23: Broad open-source candidate feature bank

**Status:** accepted for Phase 1.

**Decision:** Extract as many readily available characteristics as practical through open-source libraries and small tested reference implementations, then use corpus evidence to determine which characteristics matter for the use case.

**Rationale:** Phase 1 is characterization and discovery. Restricting extraction to an early theory of relevance could omit useful signals. A broad candidate bank allows later evaluation of repeatability, redundancy, confound sensitivity, and relationship to the eventual transformation objective.

**Boundary:** Extraction is not endorsement. Every descriptor remains exploratory until its definition, units, valid range, missing-value behavior, parameter sensitivity, synthetic behavior, and recording-level repeatability are documented. No feature enters an IR objective merely because an open-source library provides it.

**Implementation direction:** Prefer mature open-source primitives, isolate optional backends, record exact versions and licenses, preserve the canonical schema, and compare candidate features against the uncertainty model before selecting targets.

## 2026-09-23: Standard-library PCM WAV reader initially

**Decision:** Use Python's `wave` module for PCM WAV input in the reference tool.

**Rationale:** It keeps the first dependency surface small and makes metadata/hash capture explicit. A production reader can be added behind `read_wav` if compressed, float, RF64, or broader WAV support becomes necessary.

## 2026-09-23: WAV-only input for Phase 1

**Status:** accepted for Phase 1.

**Decision:** Do not add FLAC or broader container support to the current pipeline unless the corpus requires it.

**Rationale:** The available and planned pilot material can be supplied as PCM WAV. WAV support is sufficient for the current characterization and repeatability work, while additional format libraries would increase dependency and build surface without directly improving the IR objective.

**Boundary:** Original files may remain in other formats outside the repository, but any conversion to WAV must preserve the original, record the conversion parameters, and retain the original source hash. Format support can be revisited if it becomes a concrete corpus blocker.

## 2026-09-23: Descriptive comparisons only

**Decision:** Report domain means, standard deviations, and standardized differences with explicit limitations.

**Rationale:** Frame-level observations are correlated and an initial corpus may be small. Hierarchical or mixed-effects models should follow only when recording-level replication and confound metadata exist.

## 2026-09-23: Establish a repeatability baseline before IR targeting

**Status:** accepted for Phase 1.

**Decision:** Add paired or grouped recordings expected to match as a repeatability analysis before selecting domain differences as IR targets.

**Rationale:** Residual differences between nominally equivalent recordings quantify player, take, setup, recording-chain, and analysis variation. A domain difference should be considered a candidate target only when it is larger than relevant within-condition variation and remains stable across recordings.

**Boundary:** A residual is a noise floor or uncertainty estimate until it is replicated and its source is understood. It is not evidence of an instrument characteristic and must not be fit directly as an IR.

**Implementation direction:** Record comparison-group and setup metadata, compare distributions and recording-level summaries across unmatched material, retain original-level results, and condition or weight by pitch/register and observed local level only where the data supports it. Any normalized view must be explicitly derived and must not be treated as recovery of unknown or drifting absolute level. Use held-out takes to test whether candidate differences generalize. Exact event matching is not required for the primary workflow.

Event counts are retained for segmentation diagnostics only. They are not assumed to correlate between files and are not used as evidence that files or sources are similar or dissimilar.

## 2026-09-23: Preserve unknown and time-varying recording level

**Status:** accepted for Phase 1.

**Decision:** Treat absolute recording level as unknown unless a calibration reference exists, and allow level to vary within a recording. Preserve original-level measurements as primary evidence; do not assume that file-wide normalization creates a valid level-matched comparison.

**Rationale:** A single gain operation can make two files have the same selected summary level while discarding information about their original gain and failing to represent within-file level drift. Level also interacts with performance, spectral descriptors, and possible nonlinearities in the recording chain.

**Implementation direction:** Capture frame-level level trajectories, use explicitly labeled local-relative or derived normalized views only for sensitivity analysis, and report whether conclusions survive reasonable level handling choices.

## 2026-09-23: Expand repeatability across takes and acoustic sources

**Status:** accepted for Phase 1.

**Decision:** Treat future recordings of bass A and bass B as additional takes within their existing source groups, and treat other acoustic basses as new source groups.

**Rationale:** More takes improve estimates of within-source variation. Additional basses and players are needed to test whether a characteristic generalizes beyond the initial sources. Pooling all acoustic recordings into one group would confound within-source repeatability with between-instrument variation.

**Implementation direction:** Preserve stable source-group identifiers, record each file as a new immutable recording entry, and analyze within-group repeatability separately from between-group variation.

## Ecosystem recommendation

Use NumPy now; evaluate SciPy for filters, signal processing, and statistical distributions when those needs arise. Consider Essentia for a broad C++/Python feature catalog if the project later needs its specialized descriptors, but its AGPL-3.0 license is a material constraint for proprietary distribution. aubio is a focused onset/pitch option, but its GPL licensing is a material constraint for proprietary distribution and it should be introduced only if its pitch/onset behavior demonstrably improves the corpus. libsndfile/libsndfile-derived bindings are candidates when WAV/AIFF/CAF and broader PCM/float coverage is needed. Timbre Toolbox is valuable as research literature/software context, but its MATLAB-oriented workflow and distribution/dependency model make it unsuitable as the core production dependency here.

All future library choices must record exact versions, license implications, and numerical behavior in experiment metadata.

## 2026-09-24: Benchmark-first note segmentation and raw audition outputs

**Status:** accepted for current Phase 1 work.

**Decision:** Use the small manually reviewed E003 set as the current gate for detector changes. Keep the best tested threshold configuration as an exploratory baseline, but do not accept it as a reliable note detector while `low_01_low.wav` remains merged. All audition exports must be raw exact-boundary slices from the original analysis inputs, with no fades, context, normalization, or other postprocessing.

**Evidence:** The `256/64/-45` configuration matched counts on three excerpts and undercounted the five-note excerpt as 3/5. Raising the global pitch-split limit from two to four produced false splits and worsened the other excerpts.

**Boundary:** Count agreement alone does not establish onset/offset accuracy or scientific validity. Approximate listener labels remain screening evidence until a larger, more precise benchmark exists.

## 2026-09-25: Separate transformability from perfect event pairing

**Status:** accepted for Phase 1 research direction.

**Decision:** Do not require sample-synchronous acoustic/SLB note pairs as a prerequisite for investigating a candidate statistical IR transform. Use unpaired event populations to test conditional, distribution-level, filter-addressable differences, while reserving paired or controlled repeated material for transformation validation.

**Rationale:** A fixed IR cannot model note identity or note state directly; it applies one LTI transformation whose effect interacts with the input spectrum and waveform. Unpaired data can estimate conditional average spectral behavior, but cannot identify a unique physical transfer function or event-specific temporal mapping.

**Boundary:** If the desired transformation depends materially on register, dynamics, articulation, or note state, a single fixed IR is not an adequate model. Consider an IR bank or a time-varying/nonlinear approach only after held-out testing demonstrates the limitation.
