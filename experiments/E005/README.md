# E005: Event-segmentation algorithm bake-off

## Purpose

Compare substantially different event-boundary candidates on real excerpts before selecting or fusing a production detector. The current recursive detector is the baseline, not the presumed solution.

## First round

- repository recursive detector;
- librosa onset-strength/peak-picking baseline;
- Basic Pitch raw/intermediate output where available.

Later candidates: Essentia pitch-contour segmentation and contour output, aubio, MuScriptor, MT3, and commercial reference systems where practical.

Environment status: `librosa`, `basic_pitch`, and the repository package are available in the active `.venv`; `essentia`, `aubio`, and `madmom` are not installed there. Their absence is an environment blocker, not a negative algorithm result. Install and record them in a dedicated compatible environment before benchmarking.

An isolated `.venv-audioalgorithms` was created from the Basic Pitch-compatible Python runtime. aubio 0.4.9 installed and ran; its default onset detector returned counts `5,6,6,7` on the shared excerpts, over-detecting relative to the reviewed counts `3,3,3,5`. Essentia installation failed while building the available source distribution with an internal `IndexError`; no Essentia algorithm result exists yet.

Aubio tuning on the development excerpts selected onset method `specdiff` with threshold `0.7`: development count error `0`, holdout count error `2`. This is count-transfer evidence only; raw onsets are in `aubio_results.json` and boundary/usability quality remains to be evaluated.

MuScriptor 0.3.0 installed in `.venv-muscriptor` and its CLI was verified, but the small model weights are gated on Hugging Face and require license acceptance plus authentication. No MuScriptor result was generated.

## Evaluation posture

The primary unit is an excitation/event, not necessarily a MIDI note. Prioritize false boundaries, note splitting, missed boundaries, onset timing, event identity, ambiguity, and usable-event yield. Pitch accuracy is secondary. Preserve raw outputs, parameters, versions, input hashes, and provenance.

Use the manually reviewed E003 excerpts as the initial shared reference set. Approximate timing labels are screening evidence; listener usability audits remain authoritative for difficult cases.

## Current baseline

The recursive detector passes the initial E003 count benchmark at `256/64/-45` with counts `3/3`, `3/3`, `3/3`, and `5/5`. Its E004 positive-control precision is 9/18 = 50 percent.

Basic Pitch was run successfully through the dedicated `.venv-basicpitch` environment. On the four shared excerpts it produced default counts `2,2,2,2` and stricter counts `1,1,1,1`, so it under-segments this short-note set. Full raw event output is preserved in `basic_pitch_results.json`.

## Parameter-tuning rule

These are baseline runs, not final algorithm rankings. Each candidate has source-sensitive parameters that must be tuned on a development subset and evaluated on held-out real excerpts. Tuning must consider false boundaries, note splitting, missed boundaries, ambiguity, and usable-event yield rather than event count alone. The held-out set must not be used to select parameters.

The first lightweight tuning run used `low_02`, `bass_friendly_01`, and `broad_03` for development and held out `low_01`. The recursive detector selected `256/64/-45` with count error 0 on development and 0 on holdout. Librosa selected `delta=0.2`, `wait=10`, with count error 3 on development and 2 on holdout. This is count-transfer evidence only, not boundary-quality validation.

Basic Pitch tuning over four parameter sets selected its default configuration (`onset=0.5`, `frame=0.3`, `minimum_note_length=127.7 ms`) with development count error 3 and holdout count error 3. A permissive short-note setting produced development error 106, so lower thresholds are not automatically better. Treat Basic Pitch as a candidate generator rather than a standalone slicer.

## Tailored usage policy

The current operational policy is in `usage_policy.json`: use the recursive detector as the conservative primary boundary source; use tuned aubio as independent onset evidence for long or uncertain events; retain Basic Pitch for candidate proposals and pitch context; and exclude silence, polyphony, fast passages, and merged events from strict monophonic analysis. Do not auto-trust current high-confidence filters: audited precision is only 50 percent. Do not fuse detector boundaries until individual boundary audits exist.

The first routing prototype is implemented in `execute_strategy.py` and writes `strategy_results.json`. It routes long events to secondary review, flags events lacking aubio/Basic Pitch support as ambiguous, and preserves detector evidence. It does not auto-accept events or fuse boundaries; human usability audits remain required.
