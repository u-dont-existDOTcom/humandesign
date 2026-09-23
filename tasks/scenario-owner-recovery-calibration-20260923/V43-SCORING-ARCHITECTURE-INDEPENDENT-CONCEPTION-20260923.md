# V4.3 scoring-architecture independent conception — 2026-09-23

Status: **PRE-PRIOR-WORK-SCAN SNAPSHOT**. This records the internal diagnosis before consulting outside methodological literature. It is post-result development work and may not overwrite the frozen calibration results.

## Problem

The current owner-recovery experiment measures behavior at the participant-observable level but ranks candidate birth intervals using V4.3 pathway-level rarity/support. The question is whether this scorer is using distinctions that the participant measurement did not actually contain, and whether that architecture is appropriate for reverse recovery from noisy human behavior.

## Direct internal evidence already established

With the frozen Opus 5.5 translation, the 2013 rank-1 interval and best 1985-date interval have the **same supported participant-observable fingerprint**. They match the same supported behavioral constructs.

Their entire `1.664636`-bit V4.3 score separation comes from three alternative structural pathways for the same observables:

- `CONSEQUENTIAL_CORRECTION`: 2013 channel 18-58 vs 1985 gate-58 alternative;
- `PURPOSE_STRUGGLE`: 2013 channel 28-38 vs 1985 gate-28 alternative;
- `RETREAT_PRIVACY`: 2013 channel 13-33 vs 1985 gate-33 alternative.
The exact cache decomposition reproduces the whole gap:

- correction channel-over-gate bonus: `0.559619` bits;
- purpose channel-over-gate bonus: `0.777665` bits;
- retreat channel-over-gate bonus: `0.327353` bits;
- total: `1.6646366` bits.

The existing holistic-profile information audit already distinguishes **participant-observable fingerprints** from **mapping-pathway fingerprints** and states that pathway identity is only a mechanical upper bound unless the mechanisms are converted into distinguishable behavioral predictions.

Across all 19 clean V3.6 observables, 2013 and the best 1985-date interval differ on only two: `ORGANIZED_DETAIL` and `RHYTHM_ROUTINE`. Both were `not_established` by the frozen scenario measurement. Thus the supported survey evidence itself contains no clean observable that distinguishes those two candidate neighborhoods.

## Candidate architectural failure mechanisms

1. **Pathway-specific rarity leakage.** Alternative channel/gate mechanisms for one reported behavior compete using their own prevalence, salience, directness and flexibility. A rarer/stronger hidden mechanism can beat another candidate even though the participant reported the same behavior.
2. **Structural rarity substituted for behavioral likelihood.** `-log2(P(structural anchor))` rewards rare chart structure; it is not an empirical estimate of `P(observed behavior | structure)` or a likelihood ratio.
3. **Cross-observable dependence.** Dependency control is local to named clusters; additive rubric bits may still count correlated observables as though their evidence contributions were separable.
4. **Positive-only heuristic evidence.** Missing support is neutral, so the primary score is not a calibrated likelihood of the complete observed response vector. Candidate fit can be dominated by a few rare supported anchors.
5. **Observable/cluster mismatch for Profile.** The holistic audit treats `PROFILE_24`, `PROFILE_LINE5_PROJECTION`, and `PROFILE_LINE6_PHASES` as distinct participant observables, while the V4.3 scorer collapses all three inside `PROFILE_STRUCTURE` and keeps only one winning pathway.
6. **Parent-prevalence validity.** Mapping rarity may be conditioned on historical Type/Authority parents even though `score_one` tests only the mapping predicate and does not require the scored candidate to satisfy those parent conditions.

## Strongest internal alternative already in the repo

Survey-v2 uses a materially different measurement/scoring contract: candidate values are normalized at the **observable** level (`1 when any frozen predicate grouped under the observable matches`), eligible fields are macro-averaged within dependency clusters, abstentions are explicit, and later noise/recovery work models answer perturbation rather than using pathway rarity as the primary fit signal.

## Cheapest discriminating tests

- normalize the current Opus-supported evidence to observable-level candidate matches and check 2013 vs 1985 without pathway bonuses;
- compare an observable-union-rarity variant against the current pathway-rarity scorer;
- inspect whether Survey-v2-style equal/macro-weighted matching removes the false 2013-vs-1985 separation while preserving honest ambiguity;
- only after this internal test, scan established statistical/information-retrieval methods before committing a new scorer.

Prediction: collapsing pathway identity should make 2013 and the best 1985-date interval tie under the evidence actually measured; any valid future separation must come from additional measured observables (notably the currently unestablished `ORGANIZED_DETAIL` / `RHYTHM_ROUTINE`) or empirically learned behavioral likelihoods.
