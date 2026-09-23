# Architectural Decisions

## 2026-09-23: Python reference pipeline first

**Decision:** Build a small Python reference implementation before a native C++ application.

**Rationale:** The first milestone is research iteration and reproducibility, not real-time deployment. Python makes manifests, numerical experiments, synthetic tests, and report generation inexpensive. The analysis interfaces are kept modular so a later C++ implementation can replace individual components without changing the corpus contract.

## 2026-09-23: NumPy for numerical primitives

**Decision:** Use NumPy for arrays, FFTs, windows, and descriptive statistics.

**Rationale:** It is mature, widely deployed, testable, and avoids implementing FFT/STFT primitives. The initial project does not need a large audio framework.

## 2026-09-23: Standard-library PCM WAV reader initially

**Decision:** Use Python's `wave` module for PCM WAV input in the reference tool.

**Rationale:** It keeps the first dependency surface small and makes metadata/hash capture explicit. A production reader can be added behind `read_wav` if compressed, float, RF64, or broader WAV support becomes necessary.

## 2026-09-23: Descriptive comparisons only

**Decision:** Report domain means, standard deviations, and standardized differences with explicit limitations.

**Rationale:** Frame-level observations are correlated and an initial corpus may be small. Hierarchical or mixed-effects models should follow only when recording-level replication and confound metadata exist.

## Ecosystem recommendation

Use NumPy now; evaluate SciPy for filters, signal processing, and statistical distributions when those needs arise. Consider Essentia for a broad C++/Python feature catalog if the project later needs its specialized descriptors, but its AGPL-3.0 license is a material constraint for proprietary distribution. aubio is a focused, permissively licensed option for onset/pitch work, but it should be introduced only if its pitch/onset behavior demonstrably improves the corpus. libsndfile/libsndfile-derived bindings are candidates when WAV/AIFF/CAF and broader PCM/float coverage is needed. Timbre Toolbox is valuable as research literature/software context, but its MATLAB-oriented workflow and distribution/dependency model make it unsuitable as the core production dependency here.

All future library choices must record exact versions, license implications, and numerical behavior in experiment metadata.
