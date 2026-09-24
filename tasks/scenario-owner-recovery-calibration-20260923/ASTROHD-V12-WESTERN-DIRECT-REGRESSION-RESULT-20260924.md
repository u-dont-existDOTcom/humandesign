# AstroHD V1.2 transparent Western — direct development regression result — 2026-09-24

Status: **DEV_PASS_NONVALIDATING / CENTURY WESTERN-ONLY RANKING ADMITTED / NOT VALIDATION**.

## Frozen inputs

- independent conception: `ASTROHD-V12-TRANSPARENT-MERGED-INDEPENDENT-CONCEPTION-20260924.md`
- prior-work scan: `ASTROHD-V12-TRANSPARENT-MERGED-PRIOR-WORK-SCAN-20260924.md`
- Western predicate registry: `ASTROHD-V12-WESTERN-PREDICATE-FREEZE-20260924.json`
- direct-regression gate: `ASTROHD-V12-WESTERN-DIRECT-REGRESSION-FREEZE-20260924.md`
- historical cluster model SHA-256: `07d6afb96ae28307990bef693e3134684aa11a2c9dc87d42970fa9f6c02ed25e`
- frozen current behavioral translation SHA-256: `dbb92b270c2720cabed823e61ddc735dced579628c33f12df540e38b172d147d`

The implementation uses Swiss Ephemeris local-file mode consistently for the cached prevalence universe and exact query timestamps. A pre-result draft still used Moshier for exact queries; that mismatch was detected and corrected **before any V1.2 owner score was opened**.

## Generic implementation

- transparent Western predicate/scoring module SHA-256: `a5df6b3a2b13c09f6d8194d88a95d4691bfa39c021774627d3ce00f38541e543`
- direct-regression scorer SHA-256: `5f52c42019db0554074e44d6e344d054ffc29060eefdb0c0702032b5338f9862`
- focused tests SHA-256: `be014096a1c67ded2fe82c3fdf1ca19eef1b7ff3e8bf8568b056ebcef4a71b40`
- focused predicate tests: **5 passed**
- focused Ruff check on the three new files: **PASS**
- end-to-end two-year consumer-seam smoke: **PASS**

## Direct regression

Private result SHA-256: `3f8cfec03f5c7944158a32bc9005e5ba3eda22623103c8c6acff8dda1c591598`.

Prevalence universe:
- 1926-08-24 10:42 UTC through 2026-08-24 10:42 UTC inclusive;
- 876,601 hourly candidates;
- frozen 39-feature transparent Western registry;
- fixed Philadelphia recovery location;
- empirical prevalence under the exact frozen predicates.

Scores:
- exact recorded moment `1985-01-29T10:25:00Z`: **26.4757284838**
- persistent comparator `2013-01-28T08:30:00Z`: **3.0139164145**
- strongest of the eight predeclared same-date alternative midpoints: **21.6527218247**

Frozen gate:
1. target strictly beats persistent 2013 comparator: **PASS**;
2. no sampled same-date alternative beats target: **PASS**.

Therefore Western-only V1.2 is **DEV_PASS_NONVALIDATING** on the owner development regression.

This is direct owner-outcome advancement relative to the immediately preceding failed behavior-only strategies, but it remains post-result development evidence and cannot establish predictive validity.

## Next admitted action

Run the already-declared 876,601-hour **Western-only century rank** using the same frozen predicates, feature prevalences, behavior translation, and scoring algebra.

Report:
- exact recorded-moment rank against the hourly universe;
- best hourly candidate/neighborhood;
- best recorded-date hourly candidate;
- persistent 2013 comparator rank;
- whether the exact target remains meaningfully distinguished globally.

Do **not** build the merged HD+Western layer until the Western-only century result is known.

Do **not** retune predicates, orbs, houses, location, cluster weights, behavioral confidence, or success rules after this result.
