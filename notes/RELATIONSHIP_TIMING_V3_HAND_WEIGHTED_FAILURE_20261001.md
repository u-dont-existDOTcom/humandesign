# Relationship Timing V3 hand-weighted candidate — failure record

Date: 2026-10-01

The first V3 candidate used a hierarchical state gate plus hand-weighted slow-transit triggers.

It was frozen before its future scan, but development evaluation showed it remained too nonspecific:
- many historical background months exceeded the score of known relationship windows;
- the weakest known event threshold produced roughly five above-threshold months per year;
- it therefore did not satisfy the false-positive objective.

A causal implementation refinement requiring the state gate in the center month removed one adjacent 2004 false peak but did not solve the broader false-alarm burden.

Disposition: **REJECTED / SUPERSEDED FOR DEVELOPMENT**.

It does not supersede V2 and must not be used by the reminder.

The replacement is the empirical contrastive V3 defined in:
- `notes/RELATIONSHIP_TIMING_V3_EMPIRICAL_FREEZE_20261001.md`
- `notes/RELATIONSHIP_TIMING_V3_FUTURE_SCAN_20261001.md`
