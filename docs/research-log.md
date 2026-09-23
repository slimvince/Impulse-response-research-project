# Research Log

## 2026-09-23 - Repository and Phase 1 foundation

- **Question:** What should be built before attempting IR optimization?
- **Decision:** Establish a unified corpus-characterization pipeline first.
- **Implemented:** Python package for WAV metadata, framing, initial features, event detection, manifest analysis, summaries, and reports.
- **Evidence:** Source diagnostics were clean. Synthetic pytest tests were written but not successfully executed because the local terminal approval gate and Python interpreter configuration were unavailable.
- **Interpretation:** The code is a scaffold, not a validated analysis result.
- **Confidence:** High for the architectural direction; low for the scientific usefulness of any current descriptor.
- **Next action:** Configure Python, run tests, then add real licensed pilot recordings.

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
- Which features remain stable under gain normalization and reasonable parameter changes?
- Is a static linear transform adequate? This remains unresolved.
