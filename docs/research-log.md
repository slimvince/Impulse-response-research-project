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
