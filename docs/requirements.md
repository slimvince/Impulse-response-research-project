# Requirements

## Scope

The system must support reproducible investigation of differences between SLB-200 DI recordings and acoustic double-bass microphone recordings. It must use the same analysis pipeline for both domains and later for candidate-transformed SLB recordings.

The eventual application objective is to find, evaluate, and if justified implement an impulse response that makes an SLB-200 recording sound as close as possible to an acoustic upright-bass microphone recording. “As close as possible” must be defined by held-out perceptual and measurable evaluation, not by matching one recording or optimizing arbitrary exploratory features.

## Functional requirements

### RQ-001: Unified analysis

Every recording domain must pass through the same decoding, preprocessing, framing, event, feature, and reporting interfaces. Domain labels may affect grouping and comparison, not measurement definitions.

### RQ-002: Manifest-driven corpus

Recordings, domain, split, identity, and relevant capture metadata must be declared in versioned manifests. Development and held-out recordings must be distinguishable before analysis or optimization.

### RQ-003: Reproducible provenance

Outputs must record source hashes, sample metadata, analysis parameters, software/library versions where practical, random seeds where applicable, feature schema version, and Git commit.

### RQ-004: Broad candidate measurement bank

The first research implementation should measure a broad set of well-defined, testable candidate descriptors. Inclusion in the bank is exploratory and does not imply scientific importance.

### RQ-005: Event-level analysis

The system must support replaceable note/event segmentation and event-level measurements without coupling segmentation to feature implementation.

### RQ-006: Conditional comparisons

Reports must support comparisons conditioned on pitch/register, loudness/dynamics, articulation, recording identity, and temporal phase when the corpus contains the required metadata and events.

### RQ-007: Confound reporting

Reports must identify plausible effects from recording level, microphone, room, placement, player, instrument, recording chain, and segmentation quality.

### RQ-008: Machine-readable and human-readable output

An experiment must produce structured outputs suitable for later analysis and a human-readable report that distinguishes measurements, interpretations, hypotheses, and unresolved limitations.

### RQ-009: Held-out evaluation support

The architecture must support applying the same analysis to candidate-transformed SLB recordings and comparing them to target-corpus distributions without training/evaluation leakage.

### RQ-010: Testability

Numerical and audio-analysis components must have synthetic tests for known signals and edge cases. The pipeline must have manifest and output-format tests.

### RQ-011: Durable research memory

The repository must preserve requirements, architecture, feature definitions, decisions, hypotheses, chronological progress, findings, experiment evidence, external research, corpus state, and confounds separately enough that a new session can reconstruct the project without relying on chat history.

### RQ-012: Session handoff verification

The project context must tell a new session what to read, what state to report, what it may claim as validated, and how to behave when terminal access or source data is unavailable.

### RQ-013: Immutable experiment identity

Each experiment must identify the exact Git commit, manifest hash, configuration hash, source hashes, software versions, and random seed where applicable. Changing experimental inputs or parameters creates a new experiment identity.

### RQ-014: Transformation objective

The later transformation-evaluation phase must apply candidate IRs to held-out SLB-200 recordings and assess whether the transformed outputs move toward acoustic-upright recording distributions and perceptual judgments without overfitting recordings, players, instruments, or setups.

## Research requirements

### RR-001: No premature optimizer

Do not implement IR optimization until Phase 1 identifies robust targets and a defensible evaluation protocol.

### RR-002: No unsupported claims

Small or unbalanced corpora must produce qualified descriptive observations, not claims of general statistical significance.

### RR-003: No destructive source processing

Original recordings must remain unchanged. Derived files and processing parameters must be explicit.

### RR-004: Licensing discipline

Only audio and software with suitable redistribution rights may enter the repository or a distributed product.

### RR-005: Model-appropriate improvement

Do not use an IR to compensate for effects that are primarily level-dependent, time-varying, nonlinear, performance-dependent, or otherwise outside a fixed linear time-invariant model. Such effects must be measured and reported even when they cannot be corrected by the eventual IR.

## Non-goals for Phase 1

- Fixed IR length or IR optimization
- TONEX, Teensy, VST, or other deployment-specific conversion
- Neural modeling
- Universal acoustic-bass representation
- A hand-selected universal feature weighting
- Conclusions from a single recording
