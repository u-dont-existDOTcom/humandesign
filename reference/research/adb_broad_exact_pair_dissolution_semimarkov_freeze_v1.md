# Broad Exact-Pair Dissolution Semi-Markov V1 — Frozen Development Specification

Status: **frozen model specification; DO NOT FIT until the source-only episode-readiness audit passes**.

Freeze date: 2026-08-26.

## Scientific question

Test whether preregistered individual timing, static pair structure, and dynamic pair-specific Western-astrology / Human-Design features improve prediction of a pair's **first observed nonfatal romantic exit** beyond a non-astrological duration-aware baseline.

This is a development test on the public Astro-Databank-derived exact-time pair universe. It is not independent confirmation and may not be used to claim calibrated relationship probabilities for Joel/Bee or any other pair.

The target is transition timing, not relationship quality.

## Frozen data basis

Pair universe and history are frozen before feature generation:

- `reference/research/adb_broad_exact_pair_universe_freeze_v4.md`
- `reference/research/adb_broad_exact_pair_universe_v4.json`
- `reference/research/adb_broad_exact_pair_history_v4_h1_h2.json`
- `reference/research/adb_broad_exact_pair_history_v4_h3.json`
- `reference/research/adb_broad_exact_pair_history_v4_h4.json`
- `reference/research/adb_broad_exact_pair_history_v4_final_audit.json`

The final source-only audit found:

- 322 birth-data-qualified exact-time romantic pairs;
- 311 pairs surviving the pinned-SWIEPH natal/design preflight and duplicate guards;
- 69 exact pairs with at least one clean nonfatal exit;
- 67 model-eligible pairs with at least one clean nonfatal exit;
- 62 model-eligible endpoint pairs with an explicit prior H1 state-entry datum;
- 103 clean nonfatal-exit transitions total, 101 among model-eligible pairs;
- only 1 strict same-partner exit -> later formation/restart pair.

Therefore the frozen >=50 dissolution gate passed and the >=30 reunion gate failed. **No reunion model may be fit under this specification.**

## Primary estimand

For a pair known to be in an active romantic state at the beginning of a calendar-year risk interval:

```text
P(first nonfatal exit during year y
  | still active entering y,
    years since observed state entry,
    baseline covariates,
    individual timing,
    static pair structure,
    pair-specific dynamic timing)
```

The fitted annual hazards imply 1-, 2-, and 5-year cumulative nonfatal-exit probabilities by multiplying annual survival probabilities.

This is a **discrete-time clock-reset semi-Markov approximation**. The state-transition hazard depends explicitly on time since entry into the active romantic state.

## Why annual resolution is primary

The final V4 audit contains many year-precision outcomes. Of 103 clean nonfatal exits, 80 are year precision, 5 month precision, and 18 day precision.

The primary model therefore uses calendar-year risk bins. It does not invent a day or month inside year-only source intervals. Day/month evidence is retained for source precedence and ambiguity checks, but all primary hazard rows are annual.

A later high-precision timing analysis is a separate experiment and is not authorized by this freeze.

# Part A — source-only episode construction

No astrology or HD features may be calculated until this section has been implemented and its readiness artifact committed.

## A1. Eligible pair

A pair may enter the primary modeling table only if:

1. it belongs to the frozen V4 322-pair universe;
2. it remains `model_eligible_birth_and_swieph` after all duplicate guards;
3. it has a usable active-state entry under A2;
4. it has either:
   - an accepted first nonfatal exit under A3, or
   - a usable source-supported censor under A4.

## A2. Active-state entry

Candidate entry evidence, in source-precedence order, is:

1. H1 structured `begin significant relationship` event;
2. H1 structured romantic relationship-range start;
3. H1 structured marriage event;
4. H4 exact-pair P26/P451 `P580` start time.

`meet significant person` is **not** an active-state entry.

For the first observed romantic episode, choose the earliest accepted active-state candidate that is not preceded by a clean nonfatal exit for the same pair.

If two source candidates overlap in calendar year, they are corroborating entry evidence. If they are in different years with no accepted exit between them, the earlier accepted active-state datum defines the first observed episode.

Later starts after a clean exit are not folded into the first episode. They belong to the separately blocked reunion problem.

The primary row construction uses the entry calendar year. Entry precision is retained as a nuisance/data-quality field but is not converted to a false exact date.

## A3. Event endpoint

The event is the earliest clean nonfatal exit after the chosen entry from the completed H1 -> H2 -> H3 -> H4 precedence chain.

If multiple same-year source intervals overlap, treat them as one event for the primary first-exit episode.

If distinct nonfatal exits occur after the first exit, ignore them in the primary first-episode model. They are not pooled as extra independent events.

## A4. Competing / right censoring

A non-event pair may contribute only when observation of the active episode has a source-supported end. In decreasing precedence:

### A4a. Structured fatal H4 end

An exact pair P26/P451 statement with usable P582 and a P1534 cause in the frozen fatal families is a competing-event censor at its source interval.

### A4b. Structured unknown-cause H4 end

An exact pair P26/P451 statement with usable P582 but no qualifying nonfatal P1534 cause is an unknown-cause relationship-end censor. It is not silently relabeled as a breakup.

### A4c. H1 finite romantic range without accepted nonfatal exit

A finite H1 romantic relationship range whose end was not accepted as a nonfatal exit supplies a last-known-active / generic-end censor at the range-end year.

### A4d. Strong current-open relationship censor

A pair may be right-censored at the source snapshot year 2026 only when there are at least two structured current-open markers for the exact opposite partner.

Allowed markers are:

- H3 lead-infobox `spouse`/`spouses`/`partner`/`partners` entry that points to the exact opposite linked Wikipedia identity, has an explicit relationship start, and has no explicit end or non-current reason;
- H4 exact P26/P451 statement to the opposite QID with usable P580 and no usable P582.

The two markers must differ either by source family (H3 vs H4) or by subject direction (A->B vs B->A). A single open statement is insufficient for censoring at 2026.

No absence-of-divorce inference is allowed.

## A5. Ordering ambiguities

Use source intervals, not invented midpoints.

For an event interval E and competing/generic censor interval C:

- if `E.end < C.start`, event occurs first;
- if `C.end < E.start`, censor occurs first;
- if E and C overlap and source precedence does not directly establish the same transition cause, the first-episode outcome is ambiguous and the episode is excluded from the primary model.

An event and entry in the same calendar year are allowed as duration bin 0.

A censored episode must have `censor_year > entry_year` so that it contributes at least one meaningful non-event follow-up interval.

## A6. Pair-year table

For every accepted episode create one row for each calendar year from entry year through event/censor year inclusive.

Fields include at minimum:

- unordered `pair_key`;
- person A/B stable IDs;
- calendar year;
- integer duration since entry year;
- event indicator (`1` only in the first nonfatal-exit year);
- censor/competing indicator in final row when applicable;
- entry source/precision;
- exit/censor source/precision;
- relation-code indicators (`spouse`, `lover`, `spousal_equivalent`);
- source-coverage nuisance indicators known independently of the event label.

No rows occur before state entry or after first exit/censor.

## A7. Readiness gate before features

A source-only episode-readiness artifact must be committed before any astrological/HD feature generation.

The model remains blocked unless the primary table contains all of:

- >=50 model-eligible event pairs with usable entry and unambiguous first nonfatal exit;
- >=30 model-eligible censored/competing-risk non-event pairs with at least one follow-up year;
- >=200 total model-eligible pair-year rows;
- >=5 person-disjoint/connected-component groups containing at least one event.

If any condition fails, **do not fit this V1 model and do not lower the gate**.

# Part B — annual astronomical feature timing

## B1. Annual anchors

For each pair-year, dynamic astronomical features are evaluated on exactly 24 geocentric UTC anchors:

```text
12:00 UTC on the 1st and 15th of each calendar month
```

Astronomical positions for an entire future year are deterministic and therefore known at the beginning of the forecast year; using all 24 anchors is not outcome leakage.

## B2. Ephemeris

- tropical, geocentric;
- pinned Swiss Ephemeris `.se1` files only;
- hard abort on Moshier/JPL/other fallback when SWIEPH was requested;
- use the repository's verified natal/design-root engine and pinned ephemeris manifest;
- no pair lacking the frozen SWIEPH preflight may re-enter the model.

## B3. Western aspect kernel

Major aspects only:

```text
0°, 60°, 90°, 120°, 180°
```

For mover longitude `m`, target `t`, aspect `a`, sigma `s`:

```text
activation = exp(-0.5 * (wrapped_angular_residual(m,t,a) / s)^2)
```

Within one mover/target-set feature at one anchor, use the maximum activation across the five major aspects and across the specified target set.

Annual Western dynamic features use the **maximum across the 24 annual anchors**.

Secondary progression is exactly one ephemeris day per tropical year (`365.2422` days).

Frozen sigmas:

- progressed Moon: 1.5°;
- other progressed movers: 1.0°;
- transiting Jupiter: 2.5°;
- transiting Saturn: 2.0°;
- transiting Uranus/Neptune/Pluto: 1.5°.

Natal/secondary targets:

```text
Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, ASC, MC
```

Progressed movers:

```text
Sun, Moon, Mercury, Venus, Mars
```

Transit movers:

```text
Jupiter, Saturn, Uranus, Neptune, Pluto
```

# Part C — frozen nested model families

No coefficient or feature may be added after outcome-model results are inspected. A materially different feature registry is V2 and requires a new freeze.

## M0 — non-astrological semi-Markov baseline

Frozen baseline covariates:

- duration bins: `0`, `1`, `2`, `3-4`, `5-9`, `10-19`, `20-29`, `30+` years;
- younger-partner age at risk year;
- older-partner age at risk year;
- absolute age difference;
- centered calendar year and centered-calendar-year squared;
- relation-code indicators: spouse / lover / spousal-equivalent;
- entry-source indicators: H1-begin / H1-range / H1-marriage / H4-P580;
- entry-precision indicators: day / month / year;
- natal Rodden-quality combination: AA-AA / AA-A / A-A;
- fixed source-coverage indicators available for the pair independently of whether an exit occurred: H1 ADB exact page coverage, H3 linked-Wikipedia coverage, H4 linked-Wikidata coverage.

Outcome precision, endpoint source, future censor type, and any other post-outcome metadata are **not predictor features**.

## M1 — individual timing, no cross-person timing

M0 plus frozen individual timing for each partner separately.

### Western individual features

For each partner and each annual year:

- 5 slow-transit activation features: Jupiter, Saturn, Uranus, Neptune, Pluto -> any own natal target;
- 5 progressed activation features: progressed Sun, Moon, Mercury, Venus, Mars -> any own natal target.

This yields 20 Western individual-timing features across two partners.

### HD individual conditioning features

At each anchor, overlay the full frozen transit-gate set onto each person's natal Personality+Design gate set and derive:

- number of newly completed channels relative to natal;
- number of newly defined Centers relative to natal;
- number of Definition components in the overlay;
- total defined Center count in the overlay.

For count features use annual mean across 24 anchors. This yields 8 individual HD timing features across two partners.

M1 contains no A->B aspect, pair composite, pair split-bridge, or other cross-person feature.

## M2 — static pair structure

M1 plus time-invariant pair structure.

### Western static pair features

Using natal charts only and a fixed 2.0° Gaussian sigma, maximum major-aspect activation in four preregistered groups:

1. luminary: Sun/Moon cross-person combinations;
2. attraction: Venus/Mars cross-person combinations;
3. communication: Mercury -> partner Sun/Moon/Mercury in both directions;
4. angle: Sun/Moon/Mercury/Venus/Mars -> partner ASC/MC in both directions.

### HD static pair features

Using the natal pair connection only:

- defined Center count;
- Definition component count;
- complete channel count;
- Electromagnetic connection count;
- Companionship connection count;
- Dominance connection count;
- Compromise connection count.

This layer controls for baseline pair architecture before testing dynamic pair timing.

## M3W — dynamic Western pair timing

M2 plus exactly these annual feature families:

- progressed A Sun/Moon/Mercury/Venus/Mars -> any natal target of B: 5 features;
- progressed B Sun/Moon/Mercury/Venus/Mars -> any natal target of A: 5 features;
- progressed A movers -> progressed B Sun/Moon/Mercury/Venus/Mars, maximum target activation per A mover: 5 features;
- transiting Jupiter/Saturn/Uranus/Neptune/Pluto -> natal midpoint-composite targets: 5 features;
- the same five slow transits -> progressed midpoint-composite targets: 5 features.

Total: 25 dynamic Western pair-timing features.

Davison timing, houses beyond ASC/MC, asteroids, minor aspects, harmonics, declinations, zodiacal releasing, solar arcs, and feature-mined named aspects are excluded from V1.

## M3H — dynamic Human Design pair timing

M2 plus a frozen low-dimensional structural transit overlay.

At every annual anchor, union both natal Personality+Design gate sets with the full current geocentric transit gate set, then derive:

- number of additional defined Centers relative to the static pair;
- number of additional complete channels relative to the static pair;
- Definition component count;
- indicator of Single Definition;
- indicator of exactly 8 defined Centers;
- indicator of all 9 Centers defined;
- structural split-bridge reduction = `max(0, static_components - overlay_components)`.

Annual aggregation:

- count/component features: arithmetic mean across 24 anchors;
- indicators: fraction of 24 anchors true.

No specific gate/channel (including 21-45, 28-38, etc.) is singled out in V1.

The transit overlay uses current transit planetary gate activations once each; it does not create a second 88-day-prior 'transit Design chart'. Natal people retain their ordinary Personality+Design activations.

## M4 — joint pair timing

M2 + M3W + M3H.

M4 tests whether the two pair-specific systems jointly add value.

# Part D — fitting

## D1. Model form

Primary model: discrete-time logistic hazard on pair-year rows.

```text
logit(h_pair,year) = intercept + duration baseline + frozen covariates/features
```

No class balancing or outcome reweighting is used in the primary fit because calibrated probabilities/log likelihood are primary outcomes.

Continuous predictors are standardized using training-fold statistics only.

Categorical predictors use a deterministic reference level frozen in implementation.

## D2. Regularization

L2-penalized logistic regression.

Frozen regularization grid:

```text
C in {0.001, 0.01, 0.1, 1.0}
```

Select C inside training data only by mean pair-year log loss under inner person-component grouped cross-validation. Ties choose the smaller C.

No coefficient-sign or feature-selection filtering is allowed before evaluation.

## D3. Split leakage control

A person may appear in multiple romantic pairs. Therefore pairs sharing any person must never be split across train/test folds.

Construct the undirected graph:

- node = ADB person ID;
- edge = eligible modeled pair.

All edges in one connected component form one inseparable split group.

Primary evaluation uses 5 outer folds if at least 5 event-containing components exist. Components are assigned by a deterministic event-balanced greedy algorithm frozen before feature-model fitting:

1. compute component event count and pair-year count from the source-only episode table;
2. sort components by decreasing event count, then decreasing row count, then stable component hash;
3. assign each component to the fold currently having the fewest events, then fewest rows, then lowest fold index.

This uses outcomes only to balance folds; it is deterministic and fixed before fitting any astrological/HD model.

If fewer than 5 event-containing components exist, V1 does not fit.

Inner regularization folds use the same component grouping within the outer-training set.

# Part E — primary comparisons and metrics

## E1. Primary pair-timing hypotheses

Two co-primary development contrasts:

```text
M3W - M2   dynamic Western pair timing
M3H - M2   dynamic HD pair timing
```

Secondary contrasts:

```text
M1  - M0   individual timing
M2  - M1   static pair structure
M4  - M2   joint dynamic pair timing
M4  - M3W  HD incremental after Western
M4  - M3H  Western incremental after HD
```

Do not present M4-M3W alone as 'the HD test' or M4-M3H alone as 'the astrology test'.

## E2. Primary scoring

On pooled outer-fold predictions report:

- pair-year Bernoulli log loss;
- total held-out log likelihood;
- Brier score;
- calibration intercept and slope;
- 1-, 2-, and 5-year cumulative-risk calibration where adequate follow-up exists;
- event-year rank percentile within each event pair's observed risk years as a timing diagnostic;
- fold-level deltas against the immediate frozen comparator.

## E3. Development-lead rule

A co-primary pair-dynamic family is called a **development lead worth independent replication** only if all are true:

1. pooled held-out log loss is lower than M2;
2. held-out total log likelihood is higher than M2;
3. the log-loss improvement is positive in at least 4 of 5 outer folds;
4. a 500-permutation component-preserving outcome-timing test gives familywise-adjusted `p <= 0.05` across the two co-primary contrasts.

Anything weaker is reported as no preregistered development lead, regardless of interesting coefficients or anecdotes.

The exact effect size is still development-only and is not a calibrated real-world astrology effect.

## E4. Permutation

For each permutation, preserve:

- pair identity;
- entry/censor years;
- duration structure;
- number of event pairs;
- each event pair's allowable at-risk years.

Randomize the event year within that pair's allowable observed risk years for event pairs, leaving non-event censored episodes non-event.

Use the same outer folds and regularization procedure.

For the two co-primary statistics use max-T / minimum-p familywise control across M3W-M2 and M3H-M2.

# Part F — falsification / sensitivity

Run, without changing the primary decision rule:

1. +1-year and -1-year shifts of dynamic pair features;
2. +3-year and -3-year shifts;
3. shuffled partner identities within age/calendar strata, recomputing only pair-specific features;
4. natal birth-time permutation within date while preserving dates, for time-sensitive angle/HD checks;
5. Western pair model without collective Neptune/Pluto features;
6. pair-equal-weight sensitivity so exceptionally long relationships do not dominate person-year likelihood;
7. restrict to endpoint pairs with day/month exit precision as a descriptive high-precision sensitivity only; never use the small subset for a new primary claim.

A valid timing signal should peak near the actual event year rather than equally at large time shifts.

# Part G — reporting restrictions

- Report all frozen models M0/M1/M2/M3W/M3H/M4, not only the winner.
- Preserve failed folds and null results.
- Do not mine coefficients to write a new interpretation on the same data and call it validation.
- Do not use Joel/Bee as a tuning case.
- Do not convert within-ADB holdout performance into a claim of scientific confirmation.
- Any model used prospectively on private individuals must be frozen after this development stage and validated on independent external couples.
- Relationship quality remains a separate Track Q model.

# Next authorized action

Implement and commit the **source-only episode-readiness audit in Part A**.

If Part A passes all readiness gates, freeze the exact machine-readable feature registry / implementation hash and astronomy-engine audit. Only after those artifacts are committed may the first M0-M4 development fit run.
