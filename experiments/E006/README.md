# E006: EUB proof of concept

## Purpose

Test whether the existing unified corpus/event/feature pipeline can characterize real electric upright bass material before SLB-200-specific work. This is a source-domain proof of concept, not an acoustic target substitution.

## Sources

- `ns_design_eub_di`: NS Design direct/EUB recording.
- `ergo_eub_*`: representative Karoryfer Ergo EUB recordings converted from original float WAVs to derived mono PCM16 WAVs because the canonical reader requires integer PCM.

The NS live microphone track, if supplied separately, must not be treated as an acoustic-bass target. It is supplementary provenance only.

## Run

The existing `ir_research.corpus.analyze_manifest` path was used with `frame_size=4096`, `hop_size=1024`, without an EUB-specific feature pipeline.

Initial output: 17 recordings, 4,620 frame rows, 243 threshold events. Results are under `results/`.

## Interpretation status

These event counts are diagnostics, not note counts. Event quality has not yet been audited. The next step is a representative audit across NS and Ergo covering quiet/loud, short/sustained, pizzicato/arco or equivalent articulation, overlap, and source-specific cases.

The first representative raw audit set is under `audit_slices/`; direct clickable links are in `audit_slices/AUDIT_LINKS.md`. It contains NS shortest/median/longest events and Ergo examples from two phrase groups across `f`, `mf`, and `p` source codes. Human judgments are pending.

The completed listener audit is `audit_slices/listener_audit.csv`: 4 usable events and 5 disqualified events. The disqualifications were silence or noise/silence, concentrated in the selected A0 Ergo examples and the Ergo A1 pizzicato example. This is a small, duration-selected audit and not an EUB-wide usability estimate.

An expanded source-balanced audit set is under `audit_slices_expanded/`; direct links are in `audit_slices_expanded/AUDIT_LINKS.md`. It contains one high-signal ordinary-duration event per E006 recording plus NS short/long controls, for 19 raw slices. Human judgments are pending.

The expanded audit is now recorded in `audit_slices_expanded/listener_audit.csv`: 15/19 usable (`78.9%`) and 4/19 disqualified. Disqualified cases were three Ergo noise/too-short events and one NS silence control.

The first descriptive NS-vs-Ergo source-group comparison is in [REPORT.md](REPORT.md). It is explicitly not an acoustic-target or IR result; level, content, articulation, capture, and source-group confounds remain unresolved.

## Constraints

- Original EUB files remain external and unchanged.
- Derived Ergo files and hashes are recorded in `manifest.json`.
- Player, capture chain, room, processing, and exact articulation semantics remain unknown unless documented by the source.
- No acoustic-vs-EUB transformation or IR claim is made from this run.
