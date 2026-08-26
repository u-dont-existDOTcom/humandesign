# ADB Pair-Timing Astro Model Search V1 — Frozen Development Specification

Status: **development/model selection**, not final validation.

Freeze date: 2026-08-26.

## Goal

Given a known romantic pair and a documented relationship transition date, test whether frozen astrology feature families rank the true transition date above nearby control years on **held-out couples**.

This is a data-limited precursor to the full semi-Markov model in `docs/21_pair_transition_semimarkov_plan.md`. It tests temporal discrimination, not relationship quality and not partner identity.

## Dataset

Source: Astro-Databank public C-sample (`https://www.astro.com/adbexport/c_sample.xml`).

Use only records where:

- focal person Rodden rating is A or AA;
- focal person has a timed birth (`jd_ut` present);
- focal person has a romantic relationship link of type spouse (843), spousal equivalent (859), or lover (858);
- linked partner birth date is available either from an internal C-sample record or parseable from the relationship text `born: YYYY/MM/DD`;
- a relationship event is strictly attributable to that linked partner by a >=4-character partner-name token in event notes;
- event is one of: meet significant person (807), begin significant relationship (808), marriage (810), divorce (811), end significant relationship (809);
- event date has day or month precision; year-only events are excluded from V1 timing fitting;
- both natal dates and event/control dates fall within the available verified Swiss ephemeris file range used by the project (1800–2399).

Deduplicate mirrored/internal reports by unordered pair ID + event type + normalized event year/month/day.

## Partner time uncertainty

For linked partners without an exact timed internal C-sample record:

- use birth date only;
- evaluate date-only Western features at **12:00 UT**;
- exclude Moon, angles, houses, Vertex, lots, and all other time-sensitive features;
- exclude Human Design from the primary V1 fit because exact gates/Design moment can vary with unknown birth time;
- later sensitivity analysis may recalculate date-only features at 00:00 and 23:59 UT, but that is not part of primary model selection.

Internal exact-time partners are intentionally reduced to the same time-robust planet set for parity with external date-only partners.

## Transition classes

Primary pooled transition set:

- formation/commitment: 807, 808, 810;
- dissolution: 811, 809.

Also report formation-only and dissolution-only results if each subset has >=20 unique events.

Event type is available to the non-astrological baseline as a categorical feature.

## Candidate dates per event

Represent a day-precision event by its actual date.
Represent a month-precision event by the 15th of the documented month.

For each true event generate control dates at the same month/day shifted by:

```text
-10,-9,...,-1,+1,...,+9,+10 years
```

Discard a control if:

- either partner would be younger than 16 or older than 85;
- the date lies outside 1800–2399;
- calendar construction is invalid (e.g. Feb 29 in a non-leap year; in that case use Feb 28 and record adjustment).

Each event therefore has up to 21 candidate dates including the true date.

## Cross-validation

Group by unordered romantic pair; all events from a pair must remain in the same fold.

Use deterministic 5-fold GroupKFold when >=25 unique pairs are available; otherwise use the largest grouped fold count that keeps >=5 pairs per test fold.

The C-sample is **development data**. Candidate feature-family choice from this study must later be frozen and tested on an independent relationship dataset/full ADB export.

## Astronomy

- verified Swiss Ephemeris `.se1` only; abort on fallback;
- tropical, geocentric;
- secondary progressions: one ephemeris day per tropical year (365.2422 days);
- no houses/angles/Moon for pair date-only parity;
- major aspects: 0, 60, 90, 120, 180;
- aspect kernel: `exp(-0.5*(residual/sigma)^2)`;
- sigma = 1.0 degree for progressed/relationship planet aspects and 1.5 degrees for slow transits.

Natal/time-robust planets used:

```text
Sun, Mercury, Venus, Mars, Jupiter, Saturn
```

Progressed moving planets used:

```text
Sun, Mercury, Venus, Mars
```

Slow transiting planets:

```text
Jupiter, Saturn, Uranus, Neptune, Pluto
```

## Nested candidate models

All fitted models use regularized logistic regression. Standardize continuous predictors within each training fold only. Use class weights to balance true dates vs controls.

### M0 — non-astrological baseline

Features:

- age of person A at candidate date;
- age of person B at candidate date;
- absolute age difference;
- candidate calendar year scaled;
- transition-class / event-type indicators.

### M1 — individual astrology

M0 plus, for each person separately:

- maximum slow-transit activation to own natal Sun/Mercury/Venus/Mars/Jupiter/Saturn;
- maximum secondary-progressed Sun/Mercury/Venus/Mars activation to own natal time-robust planets.

Keep bodies separate as feature groups where computationally practical; regularization may shrink irrelevant coefficients.

### M3A — cross-progressions

M1 plus:

- progressed A -> natal B activation;
- progressed B -> natal A activation;
- progressed A -> progressed B activation.

Use time-robust planets only.

### M3B — natal-composite transits

M1 plus slow-planet transits to midpoint-composite Sun/Mercury/Venus/Mars/Jupiter/Saturn.

Planetary midpoint is the shorter-arc zodiac midpoint.

### M3C — progressed-composite transits

M1 plus slow-planet transits to the midpoint composite of the two secondary-progressed personal planets (Sun/Mercury/Venus/Mars).

### M3ALL — combined pair dynamics

M1 + M3A + M3B + M3C.

No static synastry is included because it is constant across candidate dates within the same pair and therefore cannot explain the event year in this case-crossover design.

## Regularization search

Within each outer training fold only, choose logistic-regression inverse regularization strength from:

```text
C = [0.01, 0.1, 1.0, 10.0]
```

using grouped inner cross-validation and mean true-date percentile as the selection metric.

Do not tune aspect sets/orbs/body lists after results.

## Evaluation

For each held-out event, rank the true date against its control dates using model decision score.

Report:

- mean true-date percentile rank;
- median true-date percentile rank;
- top-1 rate;
- top-3 rate;
- mean reciprocal rank;
- group-normalized softmax log loss;
- results pooled and, if sufficiently sized, by formation vs dissolution.

Primary model-selection comparison:

```text
M1 - M0
M3A - M1
M3B - M1
M3C - M1
M3ALL - M1
```

An astrology family is considered promising for later independent validation only if it improves mean true-date percentile over its nested baseline by >=5 percentile points and does not materially worsen softmax log loss.

## Falsification / permutation

Run 100 label permutations within event strata for the best observed pair-dynamic family **after** the frozen candidate-family comparison. Permutation shuffles which candidate date is marked as the event while retaining each event's candidate dates/features.

Report empirical p-value for the observed mean true-date percentile.

This permutation is a development diagnostic, not final confirmatory significance because the best family is selected on the same C-sample.

## Stopping rule

Run this frozen specification once. Preserve all model results, including null/negative findings.

Do not add a new body, aspect, orb, midpoint definition, or feature after inspecting V1 results. Any such change becomes V2 and must be tested on a new development split or independent dataset.
