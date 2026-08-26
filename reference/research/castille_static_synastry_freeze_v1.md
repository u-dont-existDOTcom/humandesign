# Castille Large-N Static Synastry V1 — Frozen Independent Test

Status: **independent development + untouched final-test design**.

Freeze date: 2026-08-26.

## Source and caveat

Source: Didier Castille `a00` data publicly mirrored in `tig12/g5-other`.

The source README states that these are Castille's adaptations of INSEE files, not official INSEE files, and that their scientific validity depends on Castille's good faith. The data are untimed.

The prior non-astrological audit found:

- 591,936 rows;
- 321,838 with valid mother DOB + father DOB + wedding date;
- 321,761 with both parents age 14–85 at wedding;
- 316,475 unique `(mother DOB, father DOB, wedding date)` tuples.

No astrology was inspected before freezing this specification.

## Primary question

Can date-stable Western synastry distinguish the actual father/marital partner from a synthetic alternative father whose birth cohort and wedding cohort are deliberately matched?

This tests **partner selection / pairing**, not relationship quality and not birth-time-specific astrology.

## Analysis universe

1. Read the semicolon-delimited `a00.csv`.
2. Require valid Gregorian mother DOB, father DOB, and wedding date.
3. Require both parents age 14–85 on the wedding date.
4. Deduplicate exact `(mother DOB, father DOB, wedding date)` tuples.
5. Do not use `id`/`id2` for outcome construction.

## Deterministic data partition

Hash the canonical string

`motherDOB|fatherDOB|weddingDOB`

with SHA-256 and use the first 8 hex digits modulo 100:

- 0–39: **discovery/training**;
- 40–59: **validation/model selection**;
- 60–99: **untouched final test**.

The final-test labels are not used for feature/hyperparameter selection.

## Synthetic hard negatives

Negatives are generated independently within each partition.

Stratum:

`(wedding year, father's birth year)`.

Within each stratum:

1. sort real records by SHA-256 of their canonical tuple;
2. pair each mother with the father DOB from the next record cyclically;
3. if the synthetic father DOB equals the true father DOB, continue forward until a different father DOB is found;
4. if no different father DOB exists, drop that record from the binary-pair analysis.

Thus the synthetic alternative has the same father birth year and wedding year as the real partner. No astrological quantity enters negative construction.

The binary dataset is balanced 1:1 real versus synthetic pairs.

## Birth-time convention

All natal positions are calculated at **12:00 UTC on the recorded civil birth date**.

Because birth times are unknown, V1 excludes:

- Moon;
- Ascendant/MC;
- houses;
- Human Design;
- any feature that materially depends on birth time.

Bodies retained:

`Sun, Mercury, Venus, Mars, Jupiter, Saturn`.

This convention is an approximation for the fast retained planets, so a sensitivity analysis on the final test must recompute the selected model at 00:00 and 23:59 UTC for both partners and report whether the qualitative result changes. The primary frozen convention remains noon.

## Astronomy

- tropical, geocentric;
- pinned SWIEPH `.se1` files only;
- hard abort on fallback;
- major aspects `0, 60, 90, 120, 180` degrees.

Aspect kernel:

`exp(-0.5 * (residual / 3.0°)^2)`.

## M0C — non-astrological baseline

Features:

- mother age at wedding;
- father age at wedding;
- signed mother-minus-father age difference;
- absolute age difference;
- wedding year scaled;
- mother birth year scaled;
- father birth year scaled.

## MWSC — high-resolution static Western synastry

M0C plus every mother-body → father-body → major-aspect kernel for the 6 retained bodies:

`6 × 6 × 5 = 180` synastry features.

No aspect is pre-labelled beneficial or adverse.

## Automated hyperparameter/model selection

Use `SGDClassifier(loss='log_loss', penalty='elasticnet', l1_ratio=0.5)` with standardized baseline features and unchanged [0,1] aspect kernels.

Candidate `alpha` values:

`[1e-5, 1e-4, 1e-3, 1e-2]`.

For M0C and MWSC separately:

1. train each alpha on the discovery partition;
2. choose the alpha with best validation ROC-AUC;
3. ties within 1e-4 choose the larger alpha (more regularization);
4. refit the selected model on discovery + validation;
5. evaluate once on the untouched final partition.

Random seed: `202608261432`.

For runtime stability, each partition may be deterministically capped after hashing:

- discovery: first 100,000 real pairs;
- validation: first 60,000 real pairs;
- final binary test: first 100,000 real pairs.

Caps are applied before negative generation and are not outcome-dependent.

## Primary final metrics

Report on the untouched final binary test:

- ROC-AUC;
- log loss;
- Brier score;
- calibration slope/intercept if estimable;
- MWSC − M0C delta AUC;
- MWSC − M0C delta log loss.

## Secondary final risk-set ranking

From the untouched final partition, take the first 20,000 real pairs by the same deterministic hash.

For each mother, construct a 21-candidate risk set:

- true father DOB;
- 20 distinct father DOB decoys from the same `(wedding year, father birth year)` stratum, chosen by deterministic forward offsets in hash order;
- skip a task if 20 distinct decoy DOBs are unavailable.

Using the already-frozen final models, report:

- mean true-partner percentile;
- median percentile;
- top-1 rate;
- top-5 rate;
- mean reciprocal rank.

No refitting on risk-set outcomes.

## Development interpretation thresholds

A date-stable Western synastry model is a **promising independent signal** only if on the untouched final test all are true:

1. MWSC final ROC-AUC >= 0.52;
2. delta AUC over M0C >= +0.01;
3. final log loss improves by at least 0.002;
4. final risk-set mean true-partner percentile >= 55.

A **strong signal** requires:

- ROC-AUC >= 0.55;
- delta AUC >= +0.03;
- risk-set percentile >= 60.

Tiny statistically significant effects below these thresholds may be reported as small effects but not as useful partner prediction.

## Model interpretation

Only if the promising threshold is reached may the largest stable MWSC coefficients be promoted into a candidate astrology formula. Otherwise coefficient inspection is descriptive only and must not be used to retune V1.

## Sensitivity / falsification

After the primary final result is frozen:

- recompute selected MWSC final predictions using 00:00 and 23:59 UTC birth-date positions;
- run a label permutation diagnostic on a deterministic 20,000-pair subset;
- report whether the primary effect survives.

## Stopping rule

Run once. Preserve the result. No body/aspect/orb/negative-stratum/threshold changes after final-test access. Any changed design is V2 and must not reuse the V1 final partition as untouched evidence.
