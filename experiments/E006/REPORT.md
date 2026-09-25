# E006 EUB proof-of-concept report

## Scope

E006 applies the existing unified pipeline to one NS Design direct/EUB recording and 16 representative Ergo EUB recordings. The NS live microphone track is excluded from target interpretation.

## Execution

- Recordings: 17
- Frame rows: 4,620
- Threshold events: 243
- Existing pipeline only; no EUB-specific feature path
- Results: `results/metadata.json`, `events.json`, `frames.json`, `summary.json`

## Source-group descriptive comparison

Mean-of-recording-means from the current summary:

| Feature | NS Design EUB | Ergo EUB |
|---|---:|---:|
| RMS dB | -32.100 | -39.569 |
| Spectral centroid Hz | 153.701 | 571.286 |
| Spectral rolloff Hz | 213.415 | 1000.826 |
| Spectral flux | 0.226 | 0.074 |
| f0 Hz | 75.317 | 133.482 |
| f0 confidence | 0.587 | 0.741 |
| Harmonicity dB | -10.371 | -8.627 |

## Interpretation limits

These are descriptive source-group differences, not findings about generic EUB behavior. They may reflect musical content, articulation, level, source construction, recording chain, processing, and the uneven number/duration of recordings. Event counts are diagnostics, not note counts. No acoustic target or IR claim is made.

## Current decision

The unified pipeline executes on both EUB source groups. Before acoustic-vs-EUB interpretation, expand event-quality auditing, condition comparisons by register/level/articulation, and quantify within-source repeatability.
