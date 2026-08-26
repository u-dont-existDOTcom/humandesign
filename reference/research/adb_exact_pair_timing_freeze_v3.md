# ADB Exact-Pair Relationship Timing Model V3 — Frozen Development Specification

Status: development / model discovery, not independent validation.

Freeze date: 2026-08-26.

## Purpose

Test whether exact birth-time information that was unavailable in the date-only ADB studies improves held-out prediction of documented romantic formation/commitment dates.

This V3 specifically tests information newly enabled by exact times: natal Moon, angles/houses, exact cross-progressions, exact midpoint-composite timing, and dynamic Human Design. The previously failed date-stable astrology remains a baseline and is not retuned to these outcomes.

## Dataset inclusion

Use only romantic pairs satisfying all of:

- spouse, lover, or spousal-equivalent ADB relationship link;
- both partners have exact/timed public ADB records;
- both partners have Rodden rating A or AA;
- at least one relationship event can be strictly attributed to the linked partner by the frozen partner-name token rule;
- event has at least month precision;
- both birth moments and the event/control dates lie inside the pinned Swiss ephemeris range.

Include internal C-sample exact pairs plus external partners recovered by exact `DatamainID` match from the public ADB wiki.

No approximate or inferred birth time is allowed.

## UTC reconstruction gate

External wiki records expose local birth time and `stmerid` but generally not `jd_ut`.

Before any model fit:

1. implement ADB's documented local-time + `stmerid` -> UT conversion;
2. validate it on at least 100 timed C-sample records that already provide `jd_ut`;
3. require median absolute error <=1 second and maximum absolute error <=5 seconds;
4. abort V3 if this validation fails.

Both Gregorian and Julian calendars and hour/meridian-degree `stmerid` forms must be supported.

## Outcome and control dates

Primary outcome: formation/commitment events:

- meet significant person (807);
- begin significant relationship (808);
- marriage (810).

Secondary dissolution outcome, only if >=30 usable events:

- divorce (811);
- end significant relationship (809).

For each true event date, construct same-month/day control dates at year shifts:

`-10..-1, +1..+10 years`

subject to both partners being age 16–85 on the control date. Month-only events use day 15. Year-only events are excluded from V3.

This remains an event-date case-crossover precursor, not the final semi-Markov hazard model.

## Astronomy

- verified SWIEPH only, fail closed on Moshier fallback;
- tropical geocentric ecliptic longitudes;
- secondary progression = one ephemeris day per tropical year (365.2422 days);
- Placidus houses for exact-time natal and Davison charts;
- major aspects: 0, 60, 90, 120, 180 degrees;
- exactness kernel: `exp(-0.5*(residual/sigma)^2)`.

Sigma:

- progressed Moon mover: 1.5 deg;
- other progressed movers: 1.0 deg;
- Jupiter transit: 2.5 deg;
- Saturn transit: 2.0 deg;
- Uranus/Neptune/Pluto transit: 1.5 deg.

## Feature families

### M0EX — non-astrological baseline

- partner A age;
- partner B age;
- calendar year;
- event-type one-hot;
- date-precision one-hot.

### M1DATE — date-stable individual astrology baseline

Add the date-only individual timing family already available without birth times:

- slow transits Jupiter–Pluto to each person's natal Sun, Mercury, Venus, Mars, Jupiter, Saturn;
- progressed Sun, Mercury, Venus, Mars to those same own-natal targets;
- explicit mover-target-aspect kernels.

No Moon, houses, or angles in M1DATE.

### M1EX — exact-time individual additions

Add only exact-time dependent individual features:

- slow transits Jupiter–Pluto to own natal Moon, ASC, DSC, MC, IC, 5th cusp, 7th cusp;
- progressed Sun/Moon/Mercury/Venus/Mars to own natal Moon, ASC, DSC, MC, IC, 5th cusp, 7th cusp;
- explicit mover-target-aspect kernels.

### XEX — exact cross-progressions

Add progressed A -> natal B and progressed B -> natal A contacts involving:

moving: Sun, Moon, Mercury, Venus, Mars;

targets: Sun, Moon, Mercury, Venus, Mars, Saturn, ASC, DSC, MC, IC, 5th cusp, 7th cusp.

Also include progressed A -> progressed B contacts among Sun/Moon/Mercury/Venus/Mars.

### NCOMPEX — exact natal midpoint-composite timing

Construct circular midpoints for Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn. Add Jupiter–Pluto transits to those composite points by explicit aspect.

### PCOMPEX — exact progressed midpoint-composite timing

At each candidate event date construct circular midpoint positions from both partners' progressed Sun/Moon/Mercury/Venus/Mars. Add Jupiter–Pluto transits to those points.

### DAVEX — Davison relationship chart timing

Construct a Davison chart at the midpoint of the two birth JDs and the geographic midpoint of the two birth locations. Use its Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, ASC, DSC, MC, IC, 5th cusp, and 7th cusp as relationship-chart targets. Add Jupiter–Pluto transits by explicit aspect.

### HDEX — dynamic Human Design pair state

Calculate both exact natal HD gate sets using the frozen Swiss/design-root engine. For each candidate event date overlay the same slow-transit gate set used in the existing relationship timing module.

Features are deliberately low-dimensional and source-structural:

- defined-center count;
- connection definition-component count;
- indicator for Single Definition;
- indicator for exactly 8 defined centers (8+1);
- indicator for exactly 9 defined centers (9+0);
- active-channel count.

Do not include a hand-picked channel such as 21-45.

### WESTEX

M1DATE + M1EX + XEX + NCOMPEX + PCOMPEX + DAVEX.

### ALLSYS

WESTEX + HDEX.

## Model and selection

Use grouped outer 5-fold cross-validation by unordered pair. The same pair may never appear in train and test simultaneously.

Within each outer training fold, select L1-logistic `C` only from:

`0.001, 0.01, 0.1, 1.0`

using grouped inner CV and mean true-date percentile. Standardize predictors on training data only.

Ties are evaluated by neutral average rank; all-equal candidate scores equal the 50th percentile, never rank 1.

## Primary metrics

For held-out pairs report:

- mean and median true-event-date percentile within each event's candidate dates;
- top-1 and top-3 rate;
- mean reciprocal rank;
- within-event softmax log loss;
- fold-level metrics;
- number and sign stability of selected features.

## Frozen usefulness threshold

An exact-time feature family is **promising** only if, relative to M1DATE:

1. mean true-date percentile improves by >=5 points;
2. softmax log loss is not worse by >0.05;
3. improvement is positive in at least 3/5 outer folds.

A Western exact-time model should also be compared with M0EX. Beating M1DATE while remaining worse than M0EX is not evidence of useful predictive astrology.

## Permutation diagnostic

For the best exact-time family selected by the frozen rule, run 200 within-event label permutations with model regularization fixed to the modal outer-fold C. Report empirical p-value for mean true-date percentile.

This is still a development diagnostic because family selection occurs on this dataset.

## Interpretation

- If no exact-time family clears the threshold, conclude that the current C-sample-derived exact-pair dataset has not found a useful timing model.
- Do not tune aspects, bodies, houses, HD features, or orbs after inspecting V3 results; any such change is V4.
- Any candidate feature/model that survives V3 must be frozen and tested on a genuinely independent relationship dataset before being called predictive.
