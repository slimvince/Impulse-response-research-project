# E005 Bake-off Report

**Scope:** Real-recording event-boundary comparison on four E003 excerpts.

**Development:** `low_02_low.wav`, `bass_friendly_01_bass_friendly.wav`, `broad_03_broad.wav`

**Holdout:** `low_01_low.wav`

## Measured candidates

| Candidate | Configuration selected on development | Development count error | Holdout count error | Status |
|---|---|---:|---:|---|
| Recursive detector | `256/64/-45`, two-level long-event refinement | 0 | 0 | Best count transfer |
| Librosa onset | `delta=0.2`, `wait=10` | 3 | 2 | Inconsistent onset count |
| Aubio | `specdiff`, threshold `0.7` | 0 | 2 | Good count transfer; boundary quality pending |
| Basic Pitch | default: onset `0.5`, frame `0.3`, minimum length `127.7 ms` | 3 | 3 | Under-segments; candidate generator only |
| MuScriptor | small model, `cfg_coef=1.5`, greedy or beam-2 | 3 | 1 | Best neural count transfer; boundary quality pending |

These are count-transfer results, not final boundary-precision or usable-event results. Human audits and onset/split/merge metrics remain required.

## Consolidated measurements

Using the approximate E003 onset labels, the ordered comparison is:

| Candidate | Total count error | Mean ordered onset error |
|---|---:|---:|
| Recursive detector | 0 | 52 ms |
| Aubio tuned | 2 | 116 ms |
| Basic Pitch default | 6 | 222 ms |
| Librosa onset | 5 | 280 ms |

Human usability measurements:

- E003 reviewed detector outputs: `10/14 = 71.4%` usable;
- E004 real-recording stratified sample: `12/36 = 33.3%` usable;
- E004 positive-control sample: `9/18 = 50%` usable.

The candidate timing measurements are not equivalent to human usability: only the recursive detector has a complete listener audit on the shared E003 outputs, and the reference times are approximate.

## Environment status

- Recursive detector, librosa: active `.venv`.
- Basic Pitch: dedicated `.venv-basicpitch`.
- Aubio 0.4.9: dedicated `.venv-audioalgorithms`.
- Essentia: not run; Windows source build failed with an internal `IndexError`; no compatible distribution was available through the tested package path.
- MuScriptor 0.3.0: dedicated `.venv-muscriptor`, authenticated Hugging Face model access.
- MT3: not installed or benchmarked.
- Commercial reference systems: not benchmarked.

## Raw outputs

- [results.json](results.json)
- [tuning_results.json](tuning_results.json)
- [aubio_results.json](aubio_results.json)
- [aubio_tuning_results.json](aubio_tuning_results.json)
- [basic_pitch_results.json](basic_pitch_results.json)
- [basic_pitch_tuning_results.json](basic_pitch_tuning_results.json)
- [muscriptor_results.json](muscriptor_results.json)
- [muscriptor_tuning_results.json](muscriptor_tuning_results.json)

## Decision

No candidate is accepted as a final event detector from count results alone. The recursive detector is the current baseline; aubio and MuScriptor are promising independent candidates for further boundary audit; Basic Pitch remains a candidate generator; librosa is a supporting onset signal. The next comparison must measure false boundaries, split/merge rates, onset timing, event class, and usable-event yield.
