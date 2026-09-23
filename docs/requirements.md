# Requirements

## Scope

The system must support reproducible investigation of differences between SLB-200 DI recordings and acoustic double-bass microphone recordings. It must use the same analysis pipeline for both domains and later for candidate-transformed SLB recordings.

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

## Research requirements

### RR-001: No premature optimizer

Do not implement IR optimization until Phase 1 identifies robust targets and a defensible evaluation protocol.

### RR-002: No unsupported claims

Small or unbalanced corpora must produce qualified descriptive observations, not claims of general statistical significance.

### RR-003: No destructive source processing

Original recordings must remain unchanged. Derived files and processing parameters must be explicit.

### RR-004: Licensing discipline

Only audio and software with suitable redistribution rights may enter the repository or a distributed product.

## Non-goals for Phase 1

- Fixed IR length or IR optimization
- TONEX, Teensy, VST, or other deployment-specific conversion
- Neural modeling
- Universal acoustic-bass representation
- A hand-selected universal feature weighting
- Conclusions from a single recording
