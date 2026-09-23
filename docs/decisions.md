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

## 2026-09-23: Standard-library PCM WAV reader initially

**Decision:** Use Python's `wave` module for PCM WAV input in the reference tool.

**Rationale:** It keeps the first dependency surface small and makes metadata/hash capture explicit. A production reader can be added behind `read_wav` if compressed, float, RF64, or broader WAV support becomes necessary.

## 2026-09-23: Descriptive comparisons only

**Decision:** Report domain means, standard deviations, and standardized differences with explicit limitations.

**Rationale:** Frame-level observations are correlated and an initial corpus may be small. Hierarchical or mixed-effects models should follow only when recording-level replication and confound metadata exist.

## 2026-09-23: Establish a repeatability baseline before IR targeting

**Status:** accepted for Phase 1.

**Decision:** Add paired or grouped recordings expected to match as a repeatability analysis before selecting domain differences as IR targets.

**Rationale:** Residual differences between nominally equivalent recordings quantify player, take, setup, recording-chain, and analysis variation. A domain difference should be considered a candidate target only when it is larger than relevant within-condition variation and remains stable across recordings.

**Boundary:** A residual is a noise floor or uncertainty estimate until it is replicated and its source is understood. It is not evidence of an instrument characteristic and must not be fit directly as an IR.

**Implementation direction:** Record comparison-group and setup metadata, compare distributions and recording-level summaries across unmatched material, retain original-level results, and condition or weight by pitch/register and observed local level only where the data supports it. Any normalized view must be explicitly derived and must not be treated as recovery of unknown or drifting absolute level. Use held-out takes to test whether candidate differences generalize. Exact event matching is not required for the primary workflow.

## 2026-09-23: Preserve unknown and time-varying recording level

**Status:** accepted for Phase 1.

**Decision:** Treat absolute recording level as unknown unless a calibration reference exists, and allow level to vary within a recording. Preserve original-level measurements as primary evidence; do not assume that file-wide normalization creates a valid level-matched comparison.

**Rationale:** A single gain operation can make two files have the same selected summary level while discarding information about their original gain and failing to represent within-file level drift. Level also interacts with performance, spectral descriptors, and possible nonlinearities in the recording chain.

**Implementation direction:** Capture frame-level level trajectories, use explicitly labeled local-relative or derived normalized views only for sensitivity analysis, and report whether conclusions survive reasonable level handling choices.

## Ecosystem recommendation

Use NumPy now; evaluate SciPy for filters, signal processing, and statistical distributions when those needs arise. Consider Essentia for a broad C++/Python feature catalog if the project later needs its specialized descriptors, but its AGPL-3.0 license is a material constraint for proprietary distribution. aubio is a focused onset/pitch option, but its GPL licensing is a material constraint for proprietary distribution and it should be introduced only if its pitch/onset behavior demonstrably improves the corpus. libsndfile/libsndfile-derived bindings are candidates when WAV/AIFF/CAF and broader PCM/float coverage is needed. Timbre Toolbox is valuable as research literature/software context, but its MATLAB-oriented workflow and distribution/dependency model make it unsuitable as the core production dependency here.

All future library choices must record exact versions, license implications, and numerical behavior in experiment metadata.
