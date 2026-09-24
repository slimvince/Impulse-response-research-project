# Phase 1 Methodology

## Unified pipeline

Every manifest recording passes through the same WAV decode, mono reduction, frame extraction, spectral analysis, event detection, and reporting path. Domain and split are metadata labels, not alternate algorithms.

## Analytical unit: note/event, not whole recording

The eventual goal is an impulse response that makes an SLB-200 recording sound as close as possible to an acoustic upright-bass microphone recording. The relevant target is therefore not the complete-song recording as a whole, but the individual note or excitation event that an SLB-200 sample and a corresponding acoustic bass note should match.

This means that the current project treats whole-recording summary statistics as a descriptive layer, not as a direct transformation target. The complete recording's overall dynamic trajectory, overall timbral trajectory, and whole-recording RMS/mean spectral values are not the target of the eventual transformation. Even averages over all notes can be misleading if the recordings differ in pitch distribution, dynamics, articulation, overlap, or event density.

The relevant analysis flow is therefore:

`complete recording -> identify note/event -> characterize individual event -> condition on relevant context -> compare SLB vs acoustic`

The individual note/excitation event is therefore likely the primary analytical unit for the temporal transformation problem. This is a methodological conclusion, not yet a fully demonstrated empirical finding from the acoustic corpus.

## Event detection as a first-class research problem

The existing threshold-based event detector is a reference or initial implementation. It is not evidence that we can already reliably identify musical notes for IR-target analysis. Event detection must become a first-class research problem because the eventual transformation product is intended to work on individual notes, not on global statistics of a file.

The event-detection benchmark must include: onset detection, offset/end detection, bass pitch tracking, note/event segmentation, detection of overlapping notes, handling of legato and ambiguous boundaries, and, where necessary, polyphonic analysis or source separation. Open-source libraries can help, but they are not automatically sufficient simply because they provide onset, pitch, or transcription functionality. Candidate methods must be benchmarked on representative corpus recordings and compared using a manually reviewed ground-truth subset.

## Event-conditioned temporal and spectral analysis

For each usable event, the project should characterize, where possible:

- onset and offset;
- pitch/register;
- local excitation level or dynamics;
- attack;
- sustain;
- decay/release;
- spectral-envelope evolution through the event;
- harmonic amplitudes and their evolution through the event;
- articulation;
- isolated versus overlapping/polyphonic status;
- segmentation/analysis confidence.

This event-conditioned analysis should be compared across domains while conditioning on pitch, local loudness, articulation, and event quality. Segmentations with low confidence can be excluded for some analyses, and ambiguous or overlapping events can be labeled as such rather than forced into false one-note identities.

## Systematic-difference analysis

The current report computes descriptive per-domain means, standard deviations, and standardized differences. It labels these as descriptive only. Future analysis should aggregate at recording level and use event-derived measurements as within-file descriptors; detected event counts are file-specific segmentation diagnostics and are not expected to correlate across recordings or serve as similarity measures. Pitch/register distributions will remain unmatched by design, and setup metadata may remain incomplete; those limitations must be reported rather than treated as solved by conditioning. Comparisons may describe or stratify observed pitch/register and dynamics where available, but the recording or source group, not the frame row, is the replication unit. Held-out splits must be fixed in manifests before any optimization work.

Potential confounds must be recorded rather than inferred away: unknown and time-varying recording level, unmatched pitch/register, unknown bass identity, microphone, placement, room, recording chain, processing, strings, take conditions, overlap/polyphony, legato ambiguity, and segmentation quality. The player label may be known while the other contextual fields remain unknown; recordings from the same album or player must not be assumed to share them. Frame rows remain useful for describing within-recording distributions, but overlapping or adjacent frames from one recording are correlated and must not be counted as independent replication. A difference is strong only when it repeats across recordings or source groups and remains unresolved or qualified when those units are sparse. Global gain normalization cannot reconstruct an unknown or drifting recording level. Small or unbalanced corpora should produce an unresolved result, not a significance claim.

## Event quality and limitations

Some notes or excitations are unsuitable for direct comparison. Ambiguous note boundaries, overlap, polyphony, legato transitions, or low-confidence detections should be classified explicitly instead of silently merged into a single event. The project should preserve confidence and overlap/ambiguity classifications in the metadata model and exclude unsuitable events from analyses where they would distort the comparison.

## Reproducibility

Manifests are explicit; original audio is not modified or manually split for convenience. If long-file processing is later streamed in internal chunks, chunks must preserve frame/hop continuity, event context, and overlap behavior so results match whole-file processing. Outputs retain source hashes, feature version, Python/platform information, UTC generation time, and Git commit when available. Experiment configuration and corpus split belong in version control; licensed audio remains outside the repository.
