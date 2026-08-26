# ADB Exact-Time Pair Transition Pilot V1 — Frozen Exploratory Specification

Status: **underpowered development / hypothesis generation only**.

Freeze date: 2026-08-26.

## Purpose

The public Astro-Databank C-sample has only 19 high-quality (A/AA), both-timed romantic pairs with a strictly partner-linked transition event. This is below the project's declared minimum of 50 exact pairs for a first full transition model.

This pilot therefore asks a narrower question:

> Does adding time-sensitive Moon/angle information and exact Human Design pair state produce such a large event-date signal in the 19-pair subset that acquiring a larger exact-time dataset is especially worthwhile?

This is **not validation**, and no positive result from 19 pairs may be used as a calibrated Joel/Bee prediction.

## Data

Use only internal C-sample romantic pairs (`spouse`, `lover`, `spousal_equivalent`) where:

- both partners are present in the C-sample;
- both are Rodden A or AA;
- both have exact `jd_ut` birth times;
- a relationship event is strictly linked to the other partner by name token in the event note;
- event date is at least month precision;
- Gregorian birth/event dates fall within the available SWIEPH range.

Deduplicate mirrored pair events exactly as in the prior date-only model.

Primary analysis: **formation/commitment events** (meet, begin significant relationship, marriage). If fewer than 10 usable formation events remain, report insufficiency and do not fit.

Dissolution events are reported descriptively but not modeled unless at least 10 are available.

## Candidate dates

For each event compare the true event date with the same month/day shifted by `±1..10` years, subject to both partners being age 16–85. Month-only events use day 15, exactly as in the prior C-sample timing work.

All model splits are grouped by unordered couple.

## Astronomy

- tropical, geocentric;
- verified SWIEPH `.se1` only, hard abort on fallback;
- secondary progressions = one ephemeris day per tropical year;
- natal houses/angles use exact birth JD and recorded birthplace coordinates when parseable;
- exact-time Human Design gates use the existing verified HD timing engine.

## Frozen feature families

Major Western aspects are `0, 60, 90, 120, 180` degrees.

For this small pilot, aspect-specific coefficients are **not** fit. Each moving-body feature is the maximum Gaussian aspect activation over its allowed targets and the five major aspects. This keeps dimensionality modest.

### M0X — non-astrological baseline

- age A;
- age B;
- absolute age difference;
- candidate calendar year;
- event-type indicators.

### M1X — exact individual Western timing

M0X plus, separately for A and B:

- transiting Jupiter, Saturn, Uranus, Neptune, Pluto → own natal Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, ASC, MC;
- progressed Sun, Moon, Mercury, Venus, Mars → same own natal targets.

Sigma:

- progressed Moon: 1.5°;
- other progressed movers: 1.0°;
- slow transits: 1.5°.

If an entry's coordinates cannot be parsed, ASC/MC targets are omitted for that pair rather than invented.

### M3X — exact pair-specific Western timing

M1X plus:

- progressed A → natal B targets;
- progressed B → natal A targets;
- progressed A → progressed B among Sun, Moon, Mercury, Venus, Mars;
- slow transits → natal midpoint-composite Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn.

Again use mover-level maximum major-aspect activation rather than aspect-specific coefficients.

### M4X-HD — dynamic HD corroboration

M1X plus two pair-time-state features at each candidate event date:

- `I(connection is Single Definition)`;
- `I(connection has exactly 8 defined Centers / 8+1)`.

No specific channel, including 21-45, is used. Static HD features are omitted because they cannot distinguish event years within a pair.

### M3X+HD

M3X plus the two frozen HD dynamic features.

## Fitting

Use L2-penalized logistic regression with class balancing and standardized continuous features.

Because the exact sample is tiny, use a fixed `C=0.1`; do not tune hyperparameters on these 19 pairs.

Outer evaluation uses GroupKFold by unordered couple with the largest number of folds up to 4 that leaves at least 3 couples per fold. If fewer than 10 unique formation pairs remain, do not fit.

## Metrics

Report:

- mean and median true-date percentile using neutral average ranks for ties;
- top-1 and top-3 rate;
- mean reciprocal average-rank;
- within-event softmax log loss;
- fold-level percentile results.

Primary comparisons:

- M1X − M0X;
- M3X − M1X;
- M4X-HD − M1X;
- M3X+HD − M1X.

## Interpretation

This pilot is intentionally underpowered.

- `< +5` mean percentile points over M1X: no notable development lead;
- `+5 to +10`: weak lead worth independent exact-time replication;
- `>= +10` with improvement in at least 3/4 folds: large development lead, still not validation.

Any apparently strong family receives a 200-permutation within-event label diagnostic with fixed model settings.

No coefficient mining or feature modification is allowed after results. A new model requires a new dataset or a separately frozen V2.
