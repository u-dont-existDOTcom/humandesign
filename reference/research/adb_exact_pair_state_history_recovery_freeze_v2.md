# ADB Exact-Pair State-History Recovery V2 — Frozen Competing-Risk Augmentation

Status: **development data-recovery augmentation only; no astrology or Human Design model is fit here**.

Freeze date: 2026-08-26.

## Motivation fixed before V2 extraction

V1 successfully recovered structured histories for all 64 exact-time V3 pairs, but only 22 pairs had an explicit dissolution/reunion endpoint, below the frozen 30-pair minimum for a semi-Markov dissolution/reunion development model.

V1 explicitly reserved death/observation-end and competing-risk evidence for a later pass. V2 implements that reserved step without changing the pair universe, without lowering the 30-pair threshold, and without inspecting astrology/HD features.

## Pair universe

Exactly the 64 unordered exact-time romantic pairs in V1.

No pair may be added or removed because of V2 history content, except that an unresolved/broken source record may be reported as a technical failure rather than silently replaced.

## Source restriction

Use only the same public Astro-Databank wiki pages already identity-resolved by exact `DatamainID`.

V2 may use:

1. V1 accepted structured `ASTRODATABANK_rel` relationship templates;
2. V1 accepted structured romantic `ASTRODATABANK_evn` transition templates;
3. dates of other structured `ASTRODATABANK_evn` events solely to establish that the subject was demonstrably alive after a relationship-range endpoint.

Biography prose, Wikipedia, Wikidata, news, genealogy, and manual web research remain excluded.

## V1 evidence remains authoritative

All V1 explicit formation, marriage, end, and divorce evidence remains unchanged.

V2 must not move, average, or reinterpret an explicit V1 transition date to agree with a relationship range.

## Finite relationship ranges

For each V1 relationship range with an explicit finite `YYYY-YYYY` endpoint, V2 may infer a coarse **nonfatal relationship exit interval** only under one of the following frozen rules.

### Rule A — explicit nonfatal wording

`RelationshipNotes` contains an unambiguous nonfatal relationship-ending term:

- `divorc*`
- `separat*`
- `split*`
- `broke up` / `broken up`
- `annul*`
- `dissolv*`
- `estrang*`

The word must describe that relationship note itself; do not infer from unrelated page prose.

### Rule B — both partners demonstrably alive later

Both partners have at least one structured ADB event whose earliest possible date is strictly after 31 December of the relationship range's end year.

Any structured event type may establish later life because its only role here is proving the person was alive at that later date. Its semantic category is otherwise ignored.

If Rule B is satisfied, a finite romantic range is taken as structured evidence that the relationship had exited its active state during the end calendar year while both people were still alive.

This does **not** claim whether the exit was divorce, separation, breakup, estrangement, or another nonfatal termination. The derived transition label is `nonfatal_exit_range`.

## Date precision

A V2 range-derived exit remains interval-censored to the full endpoint calendar year:

`YYYY-01-01 .. YYYY-12-31`.

Do not convert the endpoint to January 1, June 30, July 1, December 31, or a midpoint for the recovery artifact.

Downstream modeling, if ever allowed by the stop/go gate, must use an interval-censoring method or a separately frozen approximation/sensitivity analysis.

## Duplicate and overlap handling

If an explicit V1 `end` or `divorce` transition overlaps the same range-end year, the V1 explicit transition remains primary and the V2 range-derived item is retained only as corroborating provenance, not a second endpoint.

If a V2 inferred range exit conflicts with an explicit V1 formation/marriage event for the same pair in the same interval, flag the pair for conflict review and do not count the inferred V2 exit toward the stop/go threshold until resolved from source structure alone.

No astrology/HD information may be used in conflict resolution.

## Later-life evidence parser

For every `ASTRODATABANK_evn` template on an involved person's page:

- read `sevdate` first;
- fall back to `EventString` only when needed;
- preserve day/month/year precision;
- malformed or undated events do not establish later life.

The later-life proof date is conservative: use the earliest possible date represented by the event interval. It must be strictly later than the relationship end year's last day.

## Reunion inference

A new reunion may be inferred only when:

1. the pair has an explicit V1 dissolution OR a valid V2 `nonfatal_exit_range`; and
2. a later accepted V1 formation/meet/begin/marriage transition starts strictly after that exit interval.

A continuous relationship range plus a later marriage within that same active span is not a reunion.

## Quality accounting

Preserve V1 T0/T1/T2/T3 and additionally report:

- V2 range-derived nonfatal exits;
- how many are Rule A, Rule B, or both;
- pairs newly gaining a usable nonfatal exit;
- total endpoint pairs after V2 augmentation;
- inferred reunion sequences after V2;
- conflicts and excluded inferred exits.

## Frozen stop/go threshold

The threshold remains exactly the V1 threshold:

- `<30` exact-time pairs with a usable explicit or V2-supported nonfatal dissolution/reunion endpoint -> **STOP; do not fit the semi-Markov dissolution/reunion model**;
- `>=30` -> **GO only to writing and freezing a separate model specification**. Do not fit before that new model freeze exists.

The threshold must not be changed after V2 counts are observed.

## Anti-leakage

V2 is state-history ascertainment only.

Do not calculate, inspect, rank, plot, or use astrology/Human Design features while deciding whether a finite range qualifies, whether later-life evidence is sufficient, or whether a conflict is retained/excluded.
