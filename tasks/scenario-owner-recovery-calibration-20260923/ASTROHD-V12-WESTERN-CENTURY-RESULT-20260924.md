# AstroHD V1.2 transparent Western-only — century ranking and minute refinement result — 2026-09-24

Status: **OWNER DEVELOPMENT TARGET MET / DEV_PASS_NONVALIDATING / WESTERN-ONLY BASELINE ACCEPTED / NOT VALIDATION**.

## Scope

This is a post-result development result on the owner case. The V1.2 strategy was motivated by the revealed failure of the behavior-only Human Design scorer and by the historical V1.1 merged result. It is therefore not independent validation.

No Western predicate, orb, house rule, location, cluster weight, behavioral confidence, or success rule was changed after opening the V1.2 owner scores.

## Frozen inputs and implementation

- Western predicate registry: ASTROHD-V12-WESTERN-PREDICATE-FREEZE-20260924.json
- direct-regression gate: ASTROHD-V12-WESTERN-DIRECT-REGRESSION-FREEZE-20260924.md
- refinement gate: ASTROHD-V12-WESTERN-REFINEMENT-FREEZE-20260924.md
- current Western module SHA-256: a5df6b3a2b13c09f6d8194d88a95d4691bfa39c021774627d3ce00f38541e543
- current century scorer SHA-256: caeb29a999ed7e3ea1a661397de6b4193a878bc82c3cb63a47bffbc5b00c09e5
- minute-refinement scorer SHA-256: 6cc766db18b70dcbc1b246d03a5a6d93ca3d5bbb48c02c802cdc8b1b998b7c2a
- focused unit-test file SHA-256: be014096a1c67ded2fe82c3fdf1ca19eef1b7ff3e8bf8568b056ebcef4a71b40
- focused Western tests: **6 passed**
- focused Ruff check: **PASS**
- test-efficiency telemetry: 3 focused runs, 7.60 seconds observed test time, zero forced redundant-green reruns.

The final refinement corrected one reporting-only draft defect before interpretation: Jan 29 is evaluated in America/New_York rather than by UTC calendar date. Global refined scores and the recorded-moment score were unaffected.

## Western-only century result

Private century result SHA-256: bf2afae1cbaf96ab9610da910464bcc5651fbb8d5392da5e41fffd1de2ed7ef5.

Universe: 1926-08-24 10:42 UTC through 2026-08-24 10:42 UTC inclusive; **876,601** hourly candidates; empirical feature prevalence under the frozen transparent predicates; exact query timestamps computed directly with Swiss Ephemeris local files.

### Exact recorded moment

Recorded moment: 1985-01-29 10:25 UTC.

Western score: **26.4757284838**.

Rank against the hourly universe: **#3–#4**.

Only two hourly states score strictly higher:
1. 1983-01-22 10:42 UTC — 27.4226606358
2. 1997-02-14 11:42 UTC — 27.3167811939

Two hourly candidates equal the exact target score: 1985-01-29 10:42 UTC and 1985-01-30 10:42 UTC.

### Persistent 2013 failure

Comparator: 2013-01-28 08:30 UTC.

Western score: **3.0139164145**.

Rank against the hourly universe: **#644,661–#644,833**.

The former persistent comparator is therefore no longer competitive under the frozen transparent Western model.

### Historical comparison

Historical V1.1 Western-only exact recorded-moment rank was #4. The new transparent V1.2 Western-only implementation reaches **#3–#4** without attempting to reconstruct the lost V1.1 Western predicate semantics.

Historical V1.1 merged HD+Western reached #2, but that extra merged layer is not necessary to satisfy the current owner-development target.

## Frozen minute refinement

Private minute-refinement result SHA-256: 627a1d64451d237680179d75080a4c88a3e7fd0d336ca49f37e08fa37f5138a8.

Procedure: top 10 frozen hourly candidates; ±12 hours around each; overlapping windows merged; **13,026** UTC minute states evaluated directly with file-backed Swiss Ephemeris; exact hourly-universe feature prevalences retained; no distance-to-target tie-break.

### Recorded neighborhood

The exact recorded moment is the **start of the highest-scoring Philadelphia-local Jan 29 plateau**:

1985-01-29 10:25 UTC through 1985-01-29 10:47 UTC.

Plateau score: **26.4757284838**.

The exact recorded minute is therefore locally optimal under the frozen minute refinement; distance from the start of the local best plateau is **0 minutes**.

### Higher global refined neighborhoods

The recorded plateau is not the global refined maximum. Higher-scoring plateaus remain, including:

- 1983-01-22 10:35–10:56 UTC — 27.4226606358
- 1997-02-14 11:37–11:49 UTC — 27.3167811939
- 1997-02-14 11:25–11:36 UTC — 27.0492584980
- 1986-02-15 09:44–09:51 UTC — 26.6387570680
- 1986-02-16 09:44–09:48 UTC — 26.6387570680

Thus V1.2 does **not** uniquely recover the owner globally at minute resolution.

Within the predeclared refined top-hour windows, the recorded minute ranks **#61–#106** because many minute states occupy higher or equal score plateaus. This statistic must not be confused with the century hourly rank.

## Owner-outcome interpretation

The stated owner-development target was to distinguish the recorded 1985-01-29 10:25 UTC Philadelphia neighborhood from the persistent 2013 competitor and nearby same-date alternatives.

That target is now met:
- 2013 is decisively separated;
- the exact recorded moment lies in the best local Jan 29 plateau;
- the local best plateau begins at the exact recorded minute;
- the century hourly rank is #3–#4.

Outcome advancement: **DIRECT_OUTCOME_ADVANCEMENT**.

Strategy efficacy: **VIABLE on owner development case / DEV_PASS_NONVALIDATING**.

Root owner-development outcome: **SATISFIED at the current authorized development boundary**.

## What does not follow

This result does not establish that Western astrology predicts birth time, Human Design, personality, or behavior in new people.

The next scientific boundary for generalization is fresh/held-out participants evaluated under the already-frozen V1.2 method. That is a separate validation task.

## Merged-layer disposition

Do not automatically build the merged HD+Western layer.

The simpler Western-only V1.2 model already meets the current owner-development target. Adding the merged layer now would be an optional development experiment, not unfinished owner work. It should be undertaken only for a new decision-relevant objective, not merely to chase rank #1 on this known case.
