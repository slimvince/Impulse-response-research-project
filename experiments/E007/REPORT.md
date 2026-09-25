# E007: Acoustic versus EUB descriptive comparison

## Scope

This is a first descriptive comparison between the nine external acoustic candidates and the E006 NS/Ergo EUB proof-of-concept set. The acoustic side uses the first 30 seconds of each recording because the full combined run exceeded the execution window; EUB uses the completed E006 results. This is not a matched or calibrated comparison and is not an IR estimate.

## Mean frame features

| Feature | Acoustic 30 s windows | All EUB frames | NS EUB | Ergo EUB |
|---|---:|---:|---:|---:|
| RMS dB | -25.246 | -35.415 | -32.100 | -37.637 |
| Spectral centroid Hz | 130.879 | 304.491 | 153.701 | 405.563 |
| Spectral rolloff Hz | 166.663 | 534.270 | 213.415 | 749.334 |
| Spectral flux | 1.025 | 0.139 | 0.226 | 0.081 |
| f0 Hz | 80.803 | 104.138 | 75.317 | 123.425 |
| f0 confidence | 0.653 | 0.642 | 0.587 | 0.679 |
| Harmonicity dB | -9.135 | -9.460 | -10.371 | -8.850 |

## Interpretation

These are observations only. The level, musical content, duration windows, articulation, source-group coverage, capture chains, and processing are not matched. The apparent spectral and level differences cannot be attributed to acoustic-versus-EUB construction or treated as IR targets.

The result does show that the unified pipeline can expose descriptive differences between the domains and between NS and Ergo. The next analysis must condition on register, local level, articulation, and recording/source group, then assess repeatability before any transformation hypothesis.

## Per-event comparison without synchronization

Exact note-to-note synchronization is not required to establish conditional per-event differences. The next analysis can compare populations of events matched by measured context, for example:

```text
acoustic low-register pizzicato events at comparable local level
versus
EUB low-register pizzicato events at comparable local level
```

For each event, retain onset-relative feature trajectories and summarize attack, early sustain, sustain, and decay. Compare distributions and recording/source-group repeatability rather than calculating a one-to-one waveform ratio. A repeated, conditionally stable difference in harmonic balance, transient spectrum, or decay coloration is evidence for a candidate filter-addressable effect; it is not proof of a unique physical transfer function.

This is a feasible next gate with the current corpus. It requires better event/articulation labels and level/register conditioning, not sample-synchronous performances. If the conditional differences vary strongly by register, dynamics, or articulation, the result will point toward an IR bank or time-varying processing rather than one universal IR.

## First conditional event analysis

The first event-level table is `event_features.csv`, with 3,201 detected events and four onset-relative phases. The first conditional comparison is `conditional_comparison.json`, using register and local-level bins.

Only three register/level cells contained both acoustic and EUB events. The populated cells were all high-register according to the current f0 estimator; one had only six EUB events. The resulting attack/sustain/decay differences are therefore exploratory and too sparsely supported for an IR conclusion. This result is itself useful: the next corpus work must improve register coverage and event labels before conditional transformability can be judged.

## Working hypothesis: per-event evidence is primary

Whole-recording averages are likely to be dominated by the mix of registers, dynamics, articulations, phrases, and recording conditions in each file. They are useful for corpus QC and broad orientation, but they are weak evidence for an IR target.

The primary transformation question should therefore be evaluated at the event level:

```text
event-level spectral and temporal behavior
conditioned on register, level, articulation, and phase
```

The project should prefer a smaller, quality-controlled population of trustworthy events over large whole-recording averages. Whole-recording summaries remain secondary context and repeatability diagnostics.
