# External Research Record

This document records durable knowledge obtained from sources outside this repository. It is separate from architectural decisions and from the chronological research log.

## Source record format

```markdown
## X### - Source title

- Source:
- Maintainer/author:
- Date checked:
- Version/date:
- License:
- What it establishes:
- What it does not establish:
- Relevance to this project:
- Follow-up leads:
```

## Current records

### X001 - NumPy

- Source: https://numpy.org/
- Date checked: 2026-09-23
- What it establishes: Mature numerical arrays and FFT primitives are available under a permissive open-source license.
- What it does not establish: That any particular feature is relevant to SLB-to-acoustic transformation.
- Relevance: Numerical foundation for the Phase 1 reference implementation.
- Follow-up leads: Record exact installed versions in experiment provenance.

### X002 - SciPy

- Source: https://scipy.org/
- Date checked: 2026-09-23
- What it establishes: Mature signal-processing and statistical building blocks are available under a permissive open-source license.
- What it does not establish: That SciPy's default algorithms are appropriate without validation on low-register pizzicato bass.
- Relevance: Candidate backend for filtering, peak finding, resampling, correlation, and statistics.
- Follow-up leads: Compare relevant routines with reference implementations and document numerical behavior.

### X003 - Essentia, aubio, libsndfile, and Timbre Toolbox

- Source: Project documentation and repositories; exact URLs and versions must be recorded before dependency adoption.
- Date checked: 2026-09-23
- What it establishes: These projects provide potentially useful audio-analysis, pitch/onset, file-I/O, or timbre-analysis capabilities.
- What it does not establish: That their outputs are interchangeable, scientifically superior, or suitable for proprietary redistribution without license review.
- Relevance: Optional comparison and future integration candidates.
- Follow-up leads: Verify current licenses, maintenance, Windows/MSVC build behavior, and test outputs on representative bass material.
