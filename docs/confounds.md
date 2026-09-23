# Confounds Register

A confound is a factor that can create an apparent domain difference without being the transformation characteristic we intend to study. This is a living register, not an exhaustive claim that every factor can be eliminated.

| ID | Confound | Initial severity | Why it matters | Control or diagnostic | Status |
|---|---|---:|---|---|---|
| C001 | Microphone frequency response | high | Can create spectral differences unrelated to the bass/source transformation. | Multiple microphones or calibrated/reference capture; retain model and placement metadata. | unresolved |
| C002 | Room and room modes | high | Resonances and reflections alter the acoustic target. | Same room documentation, close/reference mic comparisons, room measurements where practical. | unresolved |
| C003 | Microphone placement | high | Small position changes can alter low-frequency balance and attack. | Stable placement protocol and measured position metadata. | unresolved |
| C004 | Recording level/gain | high | Level changes affect amplitude descriptors and nonlinear equipment behavior. | Preserve original levels; analyze calibrated and gain-normalized views separately. | unresolved |
| C005 | Player technique | high | Pluck position, force, timing, and muting affect timbre and envelope. | Repeated players, controlled material, player metadata, recording-level replication. | unresolved |
| C006 | Instrument construction/setup | high | Different basses and setups have different spectra and decays. | Multiple instruments or controlled reference instrument; instrument metadata. | unresolved |
| C007 | Recording chain | medium/high | Preamps, converters, EQ, and DI loading may shape the signal. | Document chain and compare alternate chains where possible. | unresolved |
| C008 | Segmentation error | high | Incorrect event boundaries corrupt attack, sustain, and decay features. | Inspect event overlays, annotate a subset, compare segmenters. | unresolved |
| C009 | Pitch/register imbalance | high | A domain imbalance in note distribution can mimic timbral differences. | Stratify or model pitch/register; record f0 confidence. | unresolved |
| C010 | Dynamic-level imbalance | high | Playing level changes spectral and temporal behavior. | Match or condition on dynamics; record level calibration. | unresolved |
| C011 | Corpus leakage | high | Reusing development material for validation overstates generalization. | Immutable manifests and explicit splits before optimization. | unresolved |
| C012 | Feature and parameter sensitivity | medium | Window, hop, FFT size, and algorithm choice can create apparent effects. | Parameter sensitivity checks and versioned feature definitions. | unresolved |

## Interpretation rule

A candidate feature should not enter a future transformation objective solely because it separates two uncontrolled recording groups. The separation must be examined against this register and, where possible, measured under controlled or conditioned comparisons.
