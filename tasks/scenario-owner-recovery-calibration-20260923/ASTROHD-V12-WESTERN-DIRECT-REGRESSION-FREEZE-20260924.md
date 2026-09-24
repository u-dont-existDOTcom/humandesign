# AstroHD V1.2 Western-only direct-regression freeze — 2026-09-24

Status: **FROZEN BEFORE OWNER V1.2 SCORES / POST-RESULT DEVELOPMENT / NOT VALIDATION**.

## Purpose

Test the smallest direct causal claim behind the transparent V1.2 Western replacement before spending a full century ranking or implementing the merged HD+Western layer.

The Western predicate registry is already frozen in:
`ASTROHD-V12-WESTERN-PREDICATE-FREEZE-20260924.json`.

No predicate, orb, house rule, behavioral confidence, cluster weight, location, or success rule may be changed after opening this regression result.

## Astronomy and universe for prevalence

- tropical zodiac;
- Swiss Ephemeris local-file mode (`SWIEPH | SPEED`), no Moshier fallback;
- Placidus houses;
- fixed Philadelphia recovery location from the frozen predicate registry;
- hourly prevalence universe: **1926-08-24 10:42 UTC through 2026-08-24 10:42 UTC, inclusive**;
- empirical feature prevalence under the frozen predicates;
- feature information: `min(6, -log2(prevalence))`;
- Western cluster score: maximum matched pathway evidence within each cluster;
- Western total: sum of cluster scores.

The direct query timestamps are computed exactly with Swiss-file ephemeris rather than interpolated cache positions.

## Direct comparison set

Required queries:

1. exact recorded moment: `1985-01-29T10:25:00Z`;
2. persistent 2013 comparator: `2013-01-28T08:30:00Z`;
3. one midpoint from each of the eight non-target stable Human-Design intervals overlapping 1985-01-29 UTC:

- `1985-01-29T00:08:59.783936Z`
- `1985-01-29T00:21:35.544935Z`
- `1985-01-29T04:16:12.622170Z`
- `1985-01-29T11:08:11.120061Z`
- `1985-01-29T11:25:24.314698Z`
- `1985-01-29T17:02:18.285443Z`
- `1985-01-29T22:40:39.868829Z`
- `1985-01-29T23:39:15.079937Z`

These same-date alternatives are fixed before Western scoring and are not changed after result reveal.

## Development success gate

Western-only V1.2 is `DEV_PASS_NONVALIDATING` only if **both** are true:

1. the exact recorded moment has a strictly higher Western score than the persistent 2013 comparator; and
2. no sampled same-date alternative has a higher Western score than the exact recorded moment.

A same-date tie is permitted for this *screening* gate but does not satisfy the final owner time-distinction outcome. If the gate passes with a tie, the next admitted step is a predeclared local refinement rule before any claim of time recovery.

If either condition fails:
- classify Western-only V1.2 as `DEV_FAIL`;
- do not run a century-wide rank scan;
- do not build the merged HD+Western layer;
- do not retune predicates/orbs/weights around the owner target.

## Evidence meaning

A pass is development evidence only. It cannot establish predictive validity because the V1.2 strategy was motivated by the revealed owner failure and historical V1.1 success.

A fail is sufficient to reject this frozen V1.2 Western candidate on the owner development case.
