# MoBa 5–15 external validation freeze v1

**PHASE: VALIDATION**

Freeze SHA-256: `0add35ce61fda20b649f4c2a99ed56e01a194e490552b4024b66feed1c3a0274`

This protocol freezes the smallest Gauquelin-development candidate before any individual MoBa outcome values are accessed.

## Predictor

`Z=1` iff the standard Personality/Design activation set contains at least one longitude in each frozen half-open window:

- Gate-5-equivalent window: `[251.375°, 257.000°)`
- Gate-15-equivalent window: `[88.250°, 93.875°)`

The Design moment remains the exact backward 88° solar-arc root. Window positions, width, separation, activation set, anchor, and predicted positive direction may not be retuned from MoBa outcomes.

## Primary outcome

MoBa Q5 at 18 months, EAS Activity:

- `EE417` “always on the go”: aligned score `6 - EE417`
- `EE419` “off and running as soon as ... wakes up”: aligned score `6 - EE419`
- `EE423` prefers quiet/inactive games: aligned score `EE423`

Primary Activity score = mean of all three aligned items, requiring all three; higher means more active.

This is a **construct-transport test** of the Gauquelin VITALITY/energy signal, not a claim that the two instruments are identical.

## Primary analysis

Linear regression of Activity score on frozen `Z`, with family/mother-cluster-robust standard errors. Controls are frozen to child sex, birth-year indicators, two day-of-year Fourier harmonics, and two local-clock-time Fourier harmonics.

The primary coefficient test is two-sided. The predicted direction is positive.

## Eligibility

MoBa must permit linkage of questionnaire data to Medical Birth Registry `FDATO` (date) and `FKLOKKEN` (HHMM birth time), either in an approved secure environment or by custodian-side execution of the frozen derivation code. If not, stop before outcome access and record **dataset ineligible**, not replication failure.

## Feasibility

A Moshier parity-only sample of 10,000 uniformly distributed 1999–2008 birth moments gave frozen `Z` prevalence ≈ **14.19%**, so predictor variation should be ample. Canonical validation must be recomputed with the repository's verified Swiss Ephemeris engine.

## Interpretation

- Positive frozen primary result: independent construct-transport evidence.
- Null/opposite result: failed MoBa replication/transport test; no MoBa retuning.
- Birth-field/linkage unavailable: eligibility failure, not a negative result.
