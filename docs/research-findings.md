# Research Findings

This is the accumulated scientific knowledge layer. It is different from `research-log.md`, which records what happened chronologically.

Do not promote an observation to a finding without recording the evidence, replication level, uncertainty, and confounds. Findings may be weakened, superseded, or unresolved as new experiments arrive.

## Finding format

```markdown
## F001 - Short title

- Status: proposed | supported | weakened | unresolved | superseded
- Date first recorded:
- Last reviewed:
- Confidence: low | moderate | high

### Observation

### Evidence

- Experiment:
- Corpus and recording-level replication:

### Interpretation

### Confounds and limitations

### Related hypotheses

### Related decisions
```

## Current findings

There are currently no empirical findings from the acoustic corpus. The following methodological conclusion is a proposed research finding, not yet an empirically demonstrated result.

## F001 - Individual note/excitation events are the primary analytical unit for temporal transformation targeting

- Status: proposed
- Date first recorded: 2026-09-24
- Last reviewed: 2026-09-24
- Confidence: moderate for the methodological conclusion; low for any claim that all relevant differences are note-local and fixed-FIR-recoverable

### Observation

The eventual objective is to transform an SLB-200 signal so that an individual bass note, when processed by the candidate transformation, sounds and behaves as closely as possible to the corresponding acoustic double-bass microphone signal. Complete-song recordings are useful because they contain many real note events, but the transformation target is the individual event, not the file-level trajectory.

### Evidence

- Experiment: project methodology and current analysis pipeline; no final IR evaluation has been performed yet.
- Corpus and recording-level replication: no held-out event-level acoustic corpus has been established yet. The current pipeline has only descriptive, recording-level summaries and exploratory frame-level outputs; it is not evidence of a proven event-level target.
- Current evidence indicates that whole-recording summary statistics can be dominated by level, pitch distribution, articulation, dynamics, room response, and musical content rather than by a fixed transformation target.

### Interpretation

The individual note or excitation event is likely the fundamental analytical unit for the temporal transformation problem. The complete recording's overall dynamic trajectory, overall timbral trajectory, and whole-recording RMS or mean spectral values are not the direct target of the transformation. Averages over all notes can also be misleading when recordings contain different pitch, dynamics, articulation, or overlap distributions.

The relevant analysis flow is therefore:

`complete recording -> identify note/event -> characterize individual event -> condition on relevant context -> compare SLB vs acoustic`

For each usable event, the project should seek onset/offset, pitch/register, local excitation level, attack, sustain, decay, spectral-envelope evolution, harmonic amplitudes, articulation, overlap status, and segmentation confidence. This is especially important because the eventual IR or temporal transformation must work on individual notes rather than just making the global statistics of a particular song look more acoustic.

### Confounds and limitations

- The current threshold-based event detector is a reference implementation and not yet evidence of reliable note detection.
- Overlap, legato, and ambiguous boundaries are not solved problems.
- Pitch/register, dynamics, articulation, and recording level vary within and across files.
- File-level averages do not represent a fixed note-level target.
- This is not yet an empirical finding about the acoustic corpus; it is a methodological hypothesis that still requires event-level validation.

### Related hypotheses

- Individual note/excitation events are the primary analytical unit for temporal transformation targeting.
- Event segmentation quality and confidence are required for any robust attack/sustain or temporal-timbre comparison.

### Related decisions

- Treat event detection as a first-class research problem instead of an afterthought.
- Benchmark open-source onset, offset, pitch, note-segmentation, and overlap/polyphony methods on representative corpus recordings.
- Create a manually reviewed ground-truth subset and quantify segmentation errors before making event-level comparisons central to IR candidate evaluation.

## Evidence discipline

A descriptive difference in frame-level output is not automatically a finding about the instrument or desired transformation. Findings should, where practical, describe recording-level replication, pitch/register and dynamics conditioning, temporal phase, robustness to analysis parameters, plausible alternative explanations, and segmentation confidence. Whole-recording means and averages remain descriptive diagnostics; they are not transformation targets unless event-level evidence shows otherwise.
