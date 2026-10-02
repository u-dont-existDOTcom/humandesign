# Major Turning Point Contact-Density V1 — development freeze

Date: 2026-10-02
Status: DEVELOPMENT model; frozen before secondary checks against other owner life events.
Branch: research/six-rule-life-timing-20261001

## Purpose

Test the owner's impact-salience hypothesis with minimal symbolic interpretation:

> major person-level turning points may coincide with unusually dense, very tight dynamic contacts to the natal chart, regardless of event category.

This model was selected using only the two spiritual-transition development targets:
- first ayahuasca ego-death: approximately September 2010, chronology supported indirectly by Gmail showing psychedelic use began around August 2010; exact day unresolved;
- first reported nibbana/stream-entry breakthrough: sometime in 2013; exact date unresolved.

It was NOT selected using the father's death, relationship dates, son's birth, or other owner life events. Those may be checked only after this freeze.

## Feature universe

Natal targets:
- Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
- ASC
- MC

Qualifying aspects:
- 0, 60, 90, 120, 180 degrees

Timing families:

### Slow transits
Moving bodies:
- Jupiter, Saturn, Uranus, Neptune, Pluto
Orb:
- <=0.75 degrees

### Secondary progressions
Moving bodies:
- progressed Sun, Moon, Mercury, Venus, Mars
Orb:
- <=0.50 degrees

Convention:
- one ephemeris day after birth = one tropical year of elapsed life.

### Solar arcs
Directed bodies/points:
- Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, ASC, MC
Orb:
- <=0.50 degrees

Solar-arc Sun is excluded because its arc is mathematically dependent on progressed Sun.

## Causal time window

For each candidate date, inspect only:
- candidate date minus 14 days
through
- candidate date.

No post-candidate information may contribute.

## Dependency control

For each moving body within each timing family:
1. evaluate all qualifying contacts to the natal targets;
2. retain only the TWO strongest distinct target contacts in the trailing 15-day window;
3. discard weaker same-body target contacts.

This prevents one moving body crossing a dense natal cluster from contributing an arbitrarily large number of points.

A physical contact contributes once.

## Contact strength

For a qualifying contact:

strength = 1 - (orb / family_orb_limit)

Thus:
- exact = 1.0
- contact at the orb limit = 0

## Score

V1 score = sum of retained contact strengths across:
- slow transits;
- secondary progressions;
- solar arcs.

No planet, natal target, house, event type, or aspect type receives a symbolic bonus.

No learned coefficient is used.

## Development hyperparameter selection

A bounded search was performed over:
- trailing windows: 15, 21, 30, 45, 60 days;
- strongest contacts retained per moving body: 2;
- transit orbs from a small prespecified tight range;
- progression/solar-arc orbs from a small prespecified tight range.

Selection objective:
- maximize the weaker percentile of:
  - September 2010;
  - the strongest month anywhere in the unresolved 2013 event year;
against the full 1995-2026 monthly background.

Selected:
- 15-day causal window;
- top 2 targets per moving body;
- transit orb <=0.75 degrees;
- progression/solar-arc orb <=0.50 degrees.

This is explicit owner-case tuning and therefore non-validating.

## Development result on the two fitting targets

Using DAILY scores across 1995-01-01 through 2026-10-01:

### Approximate September 2010 event
- strongest September date: 2010-09-30
- score: 6.75625
- percentile of all daily candidate dates: ~95.46th
- August 2010 maximum: ~88.75th percentile
- October 2010 maximum: ~99.38th percentile

Interpretation:
- if the event occurred in late September, V1 captures an elevated causal period;
- if documentary recovery places it substantially earlier, performance weakens;
- October cannot be used to rescue a September event because the model is causal.

### 2013 event-year target
- strongest 2013 date: 2013-07-31
- score: 7.74981
- percentile of all daily candidate dates: ~99.01st

Because the exact 2013 date is unknown, this is only year-level localization, not an exact-event hit.

## Global score thresholds from development timeline

Daily score percentiles:
- p90: ~6.15545
- p95: ~6.70750
- p97: ~7.03302
- p99: ~7.74525

These are empirical rarity thresholds, not event probabilities.

## Secondary checks locked out during selection

The following known owner events were deliberately NOT inspected under V1 before this freeze:
- father's 2002 death;
- son's 2014 birth;
- 2005 relationship;
- 2013 relationship onset/danger;
- 2014 danger escalation;
- 2018 relationship;
- 2026 relationship period;
- mother's 2022 death.

They may now be used as secondary owner-history diagnostics, but they are not untouched validation because their dates are already known to the analyst.

## Engine provenance

Exploratory pyswisseph 2.10.03 with Moshier mode, consistent with earlier chat experiments.
Not canonical production SWIEPH.

## Scientific boundary

V1 is a tuned owner-development model.
It does not validate astrology.
The meaningful next step after secondary owner-history checks is a frozen cross-person test on independently dated high-impact transitions plus explicit low-impact/control periods.
