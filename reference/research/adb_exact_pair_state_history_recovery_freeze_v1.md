# ADB Exact-Pair State-History Recovery V1 — Frozen Data Extraction Specification

Status: **development data-recovery audit only; no astrology model is fit here**.

Freeze date: 2026-08-26.

## Purpose

Recover the richest defensible romantic state histories available for the exact-time A/AA Astro-Databank pairs already eligible for the exact-pair V3 timing study.

The immediate goal is to determine whether the public ADB wiki can supply enough formation, dissolution, separation, and reunion information to build the first semi-Markov development dataset in `docs/21_pair_transition_semimarkov_plan.md`.

This extraction is frozen before looking at recovered transition counts or any astrology/HD association with the recovered histories.

## Pair universe

Reconstruct the same high-quality exact-time pair universe used by exact-pair timing V3:

- romantic ADB relation type: spouse, lover, or spousal-equivalent;
- focal C-sample person has Rodden A or AA and exact `jd_ut` birth time;
- linked partner is either an internal C-sample A/AA exact-time record or a recovered external public ADB A/AA exact-time record;
- at least one focal C-sample relationship event is strictly attributable to that linked partner by the existing frozen name-token rule;
- unordered pairs are deduplicated.

This audit may recover more events for those already-eligible pairs, but it must not expand the pair universe based on newly discovered state-history content.

## Public source and identity gate

For each person in an eligible pair, fetch their public Astro-Databank wiki page.

Identity is accepted only when the page's `DatamainID` exactly equals the ADB person id. Name similarity alone is insufficient.

Resolution order:

1. known exact wiki title from the prior external exact-time recovery artifact, if available;
2. direct title from the person's C-sample display name;
3. MediaWiki title search;
4. reject as unresolved if no candidate page has the exact `DatamainID`.

Do not infer a person's wiki identity from biography text.

## Allowed evidence

Only structured public ADB page sections are used in V1:

1. `Relationships` section lines;
2. `Events` section lines.

Biography prose is deliberately excluded from V1 because it is harder to parse reproducibly and invites hand interpretation.

No Wikipedia, news, genealogy, or other outside source is used in this recovery pass.

## Partner attribution

A structured relationship or event line is attributable to pair A/B only when at least one normalized name token from the opposite partner appears in that line, or the relationship line links directly to the opposite partner's resolved ADB wiki title.

Normalization follows the existing project rule:

- casefold;
- non-alphanumeric characters -> spaces;
- use tokens length >=4;
- ignore generic relationship words such as `relationship`, `spouse`, `lover`, `with`, `born`, `family`, `associates`.

Ambiguous lines that could plausibly refer to another partner are preserved as rejected evidence rather than assigned.

## Structured Events extraction

From the `Events` section, accept only romantic transition labels corresponding to:

- meet a significant person -> formation;
- begin significant relationship -> formation;
- marriage -> committed formation;
- end significant relationship -> dissolution;
- divorce -> dissolution.

Parse date precision exactly as displayed:

- day precision: exact `YYYY-MM-DD`;
- month precision: interval covering that calendar month;
- year precision: interval covering that calendar year.

Do not invent day 15 for the state-history artifact. The interval itself is retained.

An event is accepted for pair A/B only if the same event line contains partner-attribution evidence under the frozen rule.

## Structured Relationships extraction

For spouse/lover/spousal-equivalent relationship lines linked to the opposite partner, parse a year range only if the notes contain an unambiguous two-year interval of the form:

`YYYY-YYYY`, `YYYY–YYYY`, or `YYYY—YYYY`.

Interpret this only as a coarse observed relationship-active interval:

- start interval = entire first calendar year;
- end interval = entire second calendar year.

Do not interpret words such as `bitter`, `close`, `affair`, `estranged`, or other quality descriptors as timing states.

Single years without an explicit range are retained as notes but are not converted to an active interval in V1.

## Combining both partners' pages

Extract evidence independently from A's and B's pages, then merge only after extraction.

Exact/near-duplicate transition evidence is merged when:

- same transition family and same exact day; or
- precision intervals overlap.

If two accepted sources for the same transition do not overlap, preserve both as a conflict. Do not choose the astrologically convenient date and do not silently average dates.

Source provenance must be retained for every accepted item.

## State-history construction

Construct conservative pair timelines from accepted evidence.

State labels used in this recovery artifact:

- `not_together_or_unobserved`;
- `romantic_active`;
- `committed_active`;
- `dissolved`;
- `reunited`.

Rules:

1. meet/begin -> romantic_active;
2. marriage -> committed_active;
3. end/divorce -> dissolved;
4. an accepted formation event occurring after a prior accepted dissolution event for the same pair -> reunited;
5. a structured spouse/lover year range supplies a coarse active interval but does not by itself establish whether the end was breakup, divorce, death, or censorship;
6. death/observation-end is not inferred unless a later modeling pass explicitly adds competing-risk data.

Because interval-censored evidence may overlap, the artifact must retain raw transitions plus a conservative derived timeline rather than collapsing uncertainty to single dates.

## Quality tiers

Each recovered pair receives a history tier:

- `T3`: at least one accepted formation and one accepted dissolution/reunion transition with month-or-better precision;
- `T2`: formation plus dissolution/reunion evidence where at least one endpoint is year precision;
- `T1`: formation only, or only a coarse structured relationship year range;
- `T0`: eligible exact-time pair but no additional structured public history recovered.

These tiers measure transition-history usefulness, not relationship quality and not birth-data quality.

## Required audit outputs

Report:

- eligible pair count;
- resolved wiki people / unresolved wiki people;
- accepted event evidence count by transition and precision;
- accepted relationship-range count;
- pair count by T0/T1/T2/T3;
- number of pairs with at least one dissolution endpoint;
- number with at least one inferred reunion sequence (formation after dissolution);
- number of evidence conflicts;
- compact per-pair provenance and interval-censored transitions.

## Stop/go rule for semi-Markov development

This extraction does not fit a model.

After recovery:

- if fewer than 30 exact-time pairs have a usable dissolution or reunion endpoint, do not fit a dissolution/reunion semi-Markov model from this ADB source;
- if >=30 have usable dissolution/reunion endpoints, a separate model specification must be frozen before fitting;
- regardless of count, this remains ADB development data and cannot serve as independent validation for V3-derived hypotheses.

## Anti-leakage rule

Do not inspect astrology/HD features while resolving ambiguous event dates, partner identity, conflicts, or history tiers.

Any manual correction to this artifact must be justified solely from source provenance and the frozen extraction rules, then versioned before downstream modeling.
