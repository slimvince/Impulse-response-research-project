# Experiment Registry

This file indexes experiments. The evidence itself belongs in versioned `experiments/E###/` directories. Start new experiments by copying `experiments/_template/`.

## Experiment identity

Every experiment directory must contain:

- `README.md`: question, interpretation, limitations, and status;
- `manifest.json`: exact recordings and development/held-out split;
- `config.json`: analysis parameters and feature-bank version;
- `results/`: generated machine-readable outputs and reports when appropriate;
- provenance linking the Git commit, manifest hash, configuration hash, source/corpus hashes, software versions, and random seed.

Do not overwrite an experiment directory. A changed question, manifest, configuration, or implementation creates a new experiment ID.

The manifest and configuration must be frozen before execution. If either changes, create a new experiment ID rather than silently replacing the evidence.

## Status vocabulary

- `planned`: definition exists, not run;
- `running`: execution in progress;
- `complete`: outputs and interpretation are recorded;
- `blocked`: dependency or data blocker;
- `superseded`: replaced by a later experiment while retained for history.

## Experiment index

| ID | Status | Question | Evidence | Related findings |
|---|---|---|---|---|
| E001 | planned | Validate the initial unified feature pipeline on a licensed pilot corpus. | Synthetic pipeline validation is complete; no real corpus is registered yet. | None |
| E002 | complete | Can Basic Pitch provide a trustworthy event-segmentation subset for the current acoustic corpus? | Four 30-second excerpts produced 82-96 default events and 15-41 stricter events; the threshold baseline produced 4-6. Listener review of the candidate slices showed `low_01_low` = 5 notes and each `mid_*`, `bass_*`, and `broad_*` clip = 3 notes. | Conditional pass only: useful as a candidate generator, not a validated note detector; the selected candidate clips are not single-note events and cannot support note-level benchmarking yet. |
| E012 | first-pass-complete / uncalibrated | Can explicit tests triage Cubase candidate slices into accept, reject, or uncertain while separating event validity from f0 reliability? | All 498 source hashes matched. First pass: 42 provisional accepts, 150 exact/effective-silence rejects, 306 uncertain. No human slice labels; no precision/recall estimate. | Not a validated classifier. See `experiments/E012/README.md`, `config.json`, `manifest.json`, and `results/`. |
| E013 | first-pass-complete / uncalibrated | How do the same explicit validator checks triage all five identified Cubase slice folders? | 3,754 candidates: 921 provisional accepts, 150 effective-silence rejects, 2,683 uncertain. The original pinned 498-file manifest matched; observed hashes for the added sets are stored in results. No human labels yet. | Not a validated classifier; precision/recall unavailable. See `experiments/E013/`. |
| E014 | exploratory-render-complete | Does a regularized magnitude-ratio minimum-phase FIR move SLB event spectra toward acoustic candidates on a held-out slice set, and how does it sound on the complete SLB file? | Rendered a 284.19-second candidate from 24 listener-confirmed SLB Use intervals and E013 provisional acoustic accepts. Held-out normalized spectral-shape MAE worsened from 9.10 to 9.20 dB. | Negative quantitative check; render is audition material, not a validated emulator or physical IR. See `experiments/E014/`. |
| E015 | per-slice-diagnostic-complete | What changes under E014 on source-aligned SLB Cubase slices, and how do per-slice profiles compare conditionally with acoustic candidates? | 160/363 SLB slices mapped uniquely (median correlation ~1); all 24 listener-confirmed intervals measured dry/filtered; 33 mapped Cubase-validator-accepted SLB slices used for candidate-population analysis. Pooled and per-event aggregation results differ. | Diagnostic only; acoustic candidates remain unlabeled and source metadata are confounded. See `experiments/E015/`. |
| E016 | alternative-render-complete / mixed | Does a median per-event log-spectrum objective improve the shared FIR candidate relative to E014? | Training/diagnostic-holdout median-profile MAE: E014 6.94/8.98 dB; E016 7.55/9.58 dB. Per-confirmed-event median distance slightly favored E016 (10.38→10.02 dB; 45.8% of events closer). Full-length raw and loudness-matched renders prepared. | Mixed metrics; do not replace E014 or claim improvement. B3 was already consulted in E014/E015 and is not an untouched holdout. See `experiments/E016/`. |
| E017 | labeling-in-progress (21/50) | What is the human-labeled validity/reason distribution for a stratified Cubase candidate subset? | 50 slices selected deterministically, 10 per set, across provisional accepts, uncertain failure modes, and hard-reject QC where available. Latest durable snapshot: 21 judged (16 usable, 5 unusable), across bass A2/A3 and bass B3. | Calibration sample only, not prevalence or final performance estimate. Reasons/confidence are blank so far. Reserve independent source/set holdout before reporting precision/recall. See `experiments/E017/`. |
| E018 | full-file-render-complete / exploratory | What do the existing E014/E016 filters do to the newly available unsliced SLB-200 recording two? | Applied both filters to the complete 362 s stereo source; generated raw and RMS-matched variants. The 135 associated Audio 02 Cubase slice durations sum to 360 s, but exact alignment is not verified. | Filter application only; no new fit or validation. Source context is unknown. See `experiments/E018/`. |

## Interpretation rule

An experiment produces evidence. It does not by itself establish a general finding. Results should be summarized in `research-findings.md` only after considering recording-level replication, conditioning variables, and confounds.
