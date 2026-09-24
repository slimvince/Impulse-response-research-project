# Hypotheses

| Hypothesis | Status | Evidence needed |
|---|---|---|
| Individual note/excitation events are the primary analytical unit for temporal transformation targeting. | proposed | Event-level segmentation benchmarks, event-level ground truth, and held-out comparisons across notes, registers, dynamics, and articulation. |
| One global threshold/split setting is unlikely to segment all note sequences reliably. | supported by initial benchmark; not yet generalizable | Larger manually reviewed benchmark across registers, dynamics, and articulation; compare selective hybrid rules. |
| Spectral-envelope behavior differs between SLB DI and acoustic microphone recordings. | proposed | Repeated recording-level comparisons conditioned on pitch and dynamics. |
| Some apparent differences are dominated by microphone, room, or recording-chain response. | proposed | Multiple microphones/placements/chains and controlled metadata. |
| Differences vary by register. | proposed | Sufficient notes across low, middle, and high registers in both domains. |
| Attack and sustain have different domain signatures. | proposed | Reliable event segmentation and event-level ground truth with confidence labels; phase-conditioned comparisons across notes. |
| A static linear FIR can explain the useful transformation. | unresolved | Held-out closed-loop experiments after Phase 1 identifies robust targets. |
| A static linear FIR is insufficient. | unresolved | Same evidence; do not assume nonlinearity before testing. |
