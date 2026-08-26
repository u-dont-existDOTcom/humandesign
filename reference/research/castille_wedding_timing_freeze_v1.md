# Castille Large-N Wedding Timing V1 — Frozen Independent Test

Status: **independent development + untouched final-test design**.

Freeze date: 2026-08-26, before any Castille astrology result was inspected.

## Question

Given an observed mother/father pair and their birth dates, can date-stable individual or pair-specific Western astrology distinguish their actual wedding date from nearby same-month/day alternative years after ordinary age/calendar effects are modeled?

This is a relationship-transition timing test. It does not test relationship quality.

## Universe

Use the same source and eligibility rules as `castille_static_synastry_freeze_v1.md`:

- semicolon-delimited Castille `a00.csv`;
- valid Gregorian mother DOB, father DOB, wedding date;
- both parents age 14–85 at wedding;
- deduplicate exact `(mother DOB, father DOB, wedding date)` tuples;
- do not use `id`/`id2` for outcome construction.

## Independent deterministic partition

Use a separate salted SHA-256 split, independent of the static-synastry split:

`SHA256("wedding-timing-v1|" + canonical_tuple)`

First 8 hex digits modulo 100:

- 0–39 discovery/training;
- 40–59 validation/model selection;
- 60–99 untouched final.

## Candidate dates

For every real wedding, form alternatives at the **same month/day** shifted by:

`±1, ±2, ..., ±10 years`.

If February 29 is invalid in a shifted year, use February 28 and record the adjustment.

Exclude an alternative if either partner would be younger than 14 or older than 85 on that date.

### Efficient binary development/control date

For binary discovery/validation training, choose exactly one valid shifted control date per pair without astrology:

1. list valid shifts in numeric order `[-10..-1,+1..+10]`;
2. compute SHA-256 of `"control|" + canonical_tuple`;
3. choose `hash_integer mod number_of_valid_shifts`.

Thus every binary pair contributes one true and one deterministic control row.

### Full final timing risk set

On the untouched final partition, the primary timing-ranking metric uses the actual date plus **all valid ±1..10-year controls**. No refitting occurs on this risk set.

## Deterministic runtime caps

After salted partitioning and sorting by the salted hash:

- discovery: first 60,000 real pairs;
- validation: first 30,000 real pairs;
- final binary test: first 60,000 real pairs;
- final full timing-risk-set test: first 20,000 real pairs.

Caps are fixed before astrology and not outcome dependent.

## Birth-time convention and retained bodies

Births are untimed. Primary natal positions use **12:00 UTC on the recorded civil birth date**.

Exclude Moon, angles, houses, and Human Design.

Natal bodies:

`Sun, Mercury, Venus, Mars, Jupiter, Saturn`.

Secondary progressed movers:

`Sun, Mercury, Venus, Mars`.

Slow transiting movers:

`Jupiter, Saturn, Uranus, Neptune, Pluto`.

Primary candidate event time is 12:00 UTC on the wedding/control date.

## Astronomy

- tropical, geocentric;
- pinned SWIEPH `.se1` only; hard abort on fallback;
- secondary progression = one ephemeris day per tropical year of life;
- major aspects `0°, 60°, 90°, 120°, 180°`;
- Gaussian exactness kernel `exp(-0.5*(residual/3°)^2)`.

## M0T — non-astrological timing baseline

At every candidate date:

- mother age;
- father age;
- signed age difference;
- absolute age difference;
- candidate calendar year scaled;
- actual wedding month encoded as sin/cos annual phase (constant across same-month controls, retained only for calibration across couples).

## M1T — individual astrology timing

M0T plus high-resolution aspect kernels, separately for mother and father:

### Slow transits → own natal

Every combination of:

- moving Jupiter/Saturn/Uranus/Neptune/Pluto;
- natal Sun/Mercury/Venus/Mars/Jupiter/Saturn;
- five major aspects.

### Secondary progression → own natal

Every combination of:

- progressed Sun/Mercury/Venus/Mars;
- natal Sun/Mercury/Venus/Mars/Jupiter/Saturn;
- five major aspects.

No feature is labelled supportive/adverse in advance.

## M3T — pair-specific dynamic astrology

M1T plus:

### Cross-progressions

- progressed mother Sun/Mercury/Venus/Mars → father's natal six retained bodies;
- progressed father Sun/Mercury/Venus/Mars → mother's natal six retained bodies;
- progressed mother four movers → progressed father four movers;
- all five major aspects.

### Transits → natal midpoint composite

For each retained natal body, form the shortest-arc midpoint between mother and father natal longitude.

Every slow transiting mover → every composite retained body → five major aspects.

### Transits → progressed midpoint composite

For Sun/Mercury/Venus/Mars form the midpoint between the two progressed longitudes at each candidate date.

Every slow transiting mover → every progressed-composite body → five major aspects.

## Model fitting

Use `SGDClassifier(loss='log_loss', penalty='elasticnet', l1_ratio=0.5)`.

Candidate alpha values:

`[1e-5, 1e-4, 1e-3, 1e-2]`.

For M0T, M1T, and M3T separately:

1. fit each alpha on discovery binary rows;
2. choose best validation ROC-AUC, ties within 1e-4 → larger alpha;
3. refit selected alpha on discovery + validation;
4. evaluate exactly once on untouched final binary rows and full final timing risk sets.

Standardize M0 continuous features using training data; leave aspect kernels [0,1] unchanged.

Random seed: `202608261433`.

## Final metrics

Binary final:

- ROC-AUC;
- log loss;
- Brier score;
- calibration intercept/slope.

Full timing risk-set final:

- mean/median true-date percentile;
- top-1 rate;
- top-3 rate;
- mean reciprocal average-rank.

Primary incremental comparisons:

- M1T − M0T;
- M3T − M1T.

## Promising thresholds

Individual timing is a promising signal only if:

- M1T AUC >=0.52;
- delta AUC vs M0T >=+0.01;
- log loss improves by >=0.002;
- full-risk mean true-date percentile >=55.

Pair-specific timing is a promising incremental signal only if:

- M3T AUC >=0.52;
- delta AUC vs M1T >=+0.01;
- log loss improves by >=0.002 vs M1T;
- full-risk mean true-date percentile >=55;
- full-risk percentile improves >=+5 points over M1T.

A strong pair-specific signal requires delta AUC >=+0.03 and risk-set improvement >=+10 points.

## Sensitivity / falsification

After primary final evaluation:

- recompute selected final predictions using 00:00 and 23:59 UTC birth-date positions;
- within the first 20,000 final binary pairs, randomly swap true/control labels 200 times and report an empirical null for selected-model AUC;
- time-shift the dynamic astrology features by exactly +3 calendar years while keeping candidate labels unchanged and report whether discrimination collapses.

## Interpretation and stopping

Only a family meeting the frozen promising threshold may be promoted into a candidate empirical timing formula. Otherwise coefficients are not mined to design V2.

Run once and preserve all results. Any changed body list, aspect set, orb, control-year rule, split, cap, or threshold creates V2 and may not treat the V1 final partition as untouched evidence.
