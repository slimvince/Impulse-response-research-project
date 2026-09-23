# Corpus Catalogue

This document describes the actual data available to the project. It is different from the corpus-protocol requirements and from per-experiment manifests.

## Corpus rules

- Original audio remains outside Git unless redistribution is explicitly licensed.
- Every usable recording receives a stable recording ID.
- Each recording has provenance, license/permission status, source hash, sample metadata, domain, split, and capture metadata where known.
- Exclusions are recorded with a reason rather than silently omitted.
- Development and held-out partitions are fixed before optimization experiments.

## Current inventory

No real audio recordings are currently available in the repository or registered in the corpus catalogue.

## Planned domains

### SLB-200 DI

Expected metadata: recording ID, player, instrument, strings/setup where relevant, pickup/DI chain, gain, sample rate, bit depth, articulation, pitch/register, dynamic level, note/phrase identity, room if relevant, license, and split.

### Acoustic double bass microphone

Expected metadata: recording ID, player, instrument, strings/setup where relevant, microphone model, placement, preamp/interface, gain, room, sample rate, bit depth, articulation, pitch/register, dynamic level, note/phrase identity, license, and split.

## Recording status vocabulary

- `candidate`: known source not yet checked;
- `approved`: metadata and license checked;
- `excluded`: deliberately not used, with reason;
- `held_out`: reserved for validation;
- `development`: available for method development.

## Catalogue entries

Add one entry per recording only after provenance and permission have been checked. Manifests used by experiments must reference these stable IDs and preserve the source hash observed at analysis time.
