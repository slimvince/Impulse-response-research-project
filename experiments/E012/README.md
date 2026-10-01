# E012: Cubase Candidate Slice Validator, First Pass

## Question

Can explicit signal-quality checks triage the 498 Cubase Hitpoint slices before feature extraction, while preserving `accept`, `reject`, and `uncertain` separately and keeping feature reliability distinct from event validity?

## Inputs and provenance

The input manifest is the external `C:\IR audio\slb200-cubase-slices-manifest.json`. All 498 files were checked against their manifest SHA-256 before analysis: zero missing files and zero hash mismatches. The two candidate sets remain separate:

- `slb200_vincents_take_1_cubase_slices`: 363 stereo 44.1 kHz 24-bit files; the unsplit source exists.
- `slb200_audio02_cubase_slices`: 135 mono 44.1 kHz 16-bit files; the unsplit source is unavailable.
## First-pass outcome

- `vincents 1-*`: 33 provisional accepts, 180 uncertain, 150 rejects.
- `Audio 02 -*`: 9 provisional accepts, 126 uncertain, 0 rejects.
- Overall: 42 provisional accepts, 306 uncertain, 150 rejects.
- All 150 hard rejects are exact/effective digital-silence WAVs in the `vincents 1-*` set.

The Audio 02 set has 125 candidates flagged for possible internal attacks/transients. These remain uncertain, not rejected: Cubase candidate boundaries and the missing source do not establish whether they contain multiple excitations.

## Validator tests and interpretation

The implementation is in `validate_cubase_candidates.py`. It records:

- file integrity/hash match;
- duration, peak/RMS, exact-zero fraction, and clipping fraction;
- approximate onset offset from the slice edge;
- possible internal envelope attacks;
- energy at the slice end as a possible truncation flag;
- f0 coverage/reliability as a separate feature-reliability field.

Current hard rejection is limited to unreadable/hash-mismatched input, effective digital silence, or severe clipping (at least 1% full-scale samples). Other signal concerns yield `uncertain`; slices without any current heuristic warning are `accept`, provisionally.

The numeric thresholds are exploratory and not established. In particular, internal-attack, onset-offset, tail-energy, low-level, and clipping policies require comparison to manually labeled Cubase slices. `accept` is not yet a validated scientific verdict. `f0_unreliable` does not itself change event validity. Transformation relevance is not assessed here. Bowed-note detection/classification is out of scope.

## Files

- `results/candidate_validation.csv`: sortable per-candidate decision, reasons, and measurements.
- `results/candidate_validation.json`: full per-candidate details, including internal attack times.
- `results/summary.json`: decision/reason counts by slice set and the initial rule definitions.
- `manifest.json` and `config.json`: frozen input-set description and exploratory rules.

## Limitations and next gate

No Cubase candidate slices in this experiment have human reference labels yet. Do not report precision, recall, F1, or a final accepted corpus size from this run. The next gate is a manually labeled, stratified subset with verdict, confidence, and multiple reason codes, followed by development/held-out evaluation. Keep the two slice sets separate; the Audio 02 source is missing. Do not transfer E008/E011 rulings onto Cubase files.
