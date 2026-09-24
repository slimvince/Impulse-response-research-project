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
| E002 | complete | Can Basic Pitch provide a trustworthy event-segmentation subset for the current acoustic corpus? | Four 30-second excerpts produced 82-96 default events and 15-41 stricter events; the threshold baseline produced 4-6. | Conditional pass only: useful as a candidate generator, not a validated note detector. |

## Interpretation rule

An experiment produces evidence. It does not by itself establish a general finding. Results should be summarized in `research-findings.md` only after considering recording-level replication, conditioning variables, and confounds.
