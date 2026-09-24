# Note segmentation benchmark plan

## Objective

Create the smallest credible benchmark needed to decide whether any candidate event detector is good enough to support note-conditioned IR work on the acoustic bass corpus.

This benchmark is not a final scientific claim. It is a gate: the detector must meet explicit note-level quality criteria before event-conditioned analyses are treated as trustworthy.

## Core principle

A detector is not considered valid just because it produces event counts. It must be evaluated on genuine note boundaries and note sequences.

The project is currently operating under the following interpretation:

- the acoustic corpus contains sequences of individually plucked notes;
- the notes are distinct and not tied or legato in the selected validation clips;
- the main challenge is note-level segmentation, not coarse note presence detection;
- a single global setting is unlikely to be adequate across the full register;
- a hybrid pipeline is a stronger candidate than any single algorithm.

## Benchmark design

### Benchmark data

Select a small, manually reviewed subset from the current acoustic recordings, with the following coverage:

- isolated single notes;
- two-note transitions;
- three-note sequences;
- low-register examples;
- mid/high-register examples;
- a few ambiguous or noisy boundary cases;
- a small number of examples with clear attack transients and decay.

Target size: 10-30 note events or 5-10 short note sequences, enough to evaluate boundary behavior without pretending the corpus is fully benchmarked.

### Ground-truth label schema

For each note or candidate note event, record:

- source file;
- time range in seconds;
- onset time;
- offset time;
- note identity or pitch estimate;
- label: `single`, `split`, `merged`, `missed`, `ambiguous`;
- confidence: `1`, `2`, `3`;
- notes explaining boundary or articulation ambiguity.

This should live alongside the detector outputs in a small benchmark directory under `experiments/`.

## Candidate algorithms to compare

Evaluate all candidates on the same benchmark set:

1. repository threshold reference detector;
2. Spotify Basic Pitch candidate output;
3. a pitch-tracker or pYIN-style candidate;
4. a simple onset detector (for example librosa or equivalent)
5. a hybrid post-processed pipeline combining candidate generation and boundary refinement.

The goal is not to declare a universal winner. The goal is to identify which approach is adequate for note-level work on this corpus and in this register.

## Hybrid pipeline to prototype

A realistic first hybrid design is:

1. detect candidate note onsets with a transient or onset detector;
2. estimate pitch continuity and note stability over time;
3. use Basic Pitch or a pitch tracker to propose note-like segments;
4. split or merge events using pitch continuity, attack timing, and decay; 
5. discard or flag low-confidence detections and ambiguous transitions;
6. compare the result to the manually reviewed ground truth before using it downstream.

This logic reflects the actual data pattern: bass notes are individual plucks with distinct frequency changes, but boundary accuracy is the real challenge.

## Evaluation metrics

Score each candidate method on the benchmark subset using the following metrics:

- onset timing error;
- offset timing error;
- missed-note rate;
- false-positive rate;
- split rate;
- merge rate;
- boundary precision / recall;
- confidence-weighted score for high-certainty notes.

Keep the benchmark result simple enough to be interpreted without a large statistical apparatus.

## Usability and disqualification

Perfect segmentation is not required for every detected event. Preserve all detector outputs and provenance, but classify each event for downstream analysis as one of:

- `usable`: one interpretable note or transition with acceptable boundaries;
- `ambiguous`: potentially useful, but requires listener review or has unresolved boundary uncertainty;
- `disqualified`: merged, split, truncated, or otherwise unsuitable for the intended analysis.

Disqualified slices remain available for detector evaluation and failure analysis. They must not be silently deleted or included in event-conditioned feature analysis. Human audition is reserved for difficult or high-impact cases, while clear cases can be classified automatically from benchmark metrics and confidence rules.

## Decision thresholds

The detector is not considered adequate for event-conditioned IR work unless all of the following are true:

- missed notes are rare on the benchmark subset;
- split and merge errors are low and explicitly documented;
- onset timing error is small enough to respect the intended IR analysis window;
- the hybrid or selected method remains stable across register and note-to-note transitions.

If the benchmark shows that no single method is adequate, the project should continue with a hybrid algorithm plus explicit confidence filtering and a manual review for ambiguous cases.

## Handoff / persistence

This benchmark plan should be treated as the current operating decision for the next implementation session. It should remain in the repository alongside the current project context and implementation plan.

The next session should:

1. create the benchmark subset;
2. label the note events manually;
3. run the candidate detectors on the same excerpts;
4. compute the defined metrics;
5. select the strongest hybrid candidate;
6. document the result in the experiment directory and update the project status.

## Current status

The project has not yet reached a validated note detector. E003 now contains 14 approximate labels across four excerpts and a reproducible evaluator. The best tested setting, `256/64/-45`, has total absolute count error 2, matching three excerpts and undercounting the five-note `low_01_low.wav` excerpt as three events. A global increase in pitch-split capacity was tested and rejected because it introduced false splits in the other excerpts. The current evidence supports a selective hybrid benchmark path rather than a final decision on a single algorithm.

Audition exports must be raw exact-boundary slices from the original analysis inputs. Do not add fades, context, normalization, or other postprocessing to files used for listening to detector behavior; any hard-boundary click is part of the raw cut and must remain observable.
