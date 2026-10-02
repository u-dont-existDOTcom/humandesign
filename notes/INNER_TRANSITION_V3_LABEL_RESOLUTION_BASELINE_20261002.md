# Inner Transition V3 — label-resolution baseline

Date: 2026-10-02
Status: post-freeze diagnostic; no model changes.

## Why resolution matters

A p98 daily peak inside a known month is much more restrictive than a p98 peak anywhere inside a known year.

Under frozen V3 across 1995-01 through 2026-10:

- total months: 382
- months containing at least one p98 V3 day: 24
- monthly-window prevalence: ~6.28%

Across calendar years represented in the scan:

- years: 32
- years containing at least one p98 V3 day: 13
- year-window prevalence: ~40.63%

Years containing a p98 day:
1996, 1998, 1999, 2000, 2003, 2007, 2010, 2011, 2013, 2021, 2022, 2023, 2024.

## Consequence

2010:
- current chronology is roughly late Aug/Sep 2010;
- V3 produces a p99.5 local peak on 2010-08-30 and p98.9 on 2010-09-01;
- this is comparatively informative because the target resolution is about a month.

2013:
- target chronology is only "sometime in 2013";
- V3 produces a p98.7 peak on 2013-04-27;
- but a p98 peak appears somewhere in ~41% of years under this model;
- additionally, Apr 2013 overlaps the independently known Ann relationship-onset period.

Therefore the 2013 result must remain unresolved rather than counted as a strong fit.

## Rule

Report match strength at the resolution of the historical label.
Do not present a within-year peak as if it were an exact-date or month-level hit.
