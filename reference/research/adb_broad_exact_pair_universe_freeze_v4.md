# ADB Broad Exact-Time Romantic Pair Universe V4 — Frozen Inclusion and History-Recovery Specification

Status: **development-data universe expansion; frozen before broad-universe pair or endpoint counts are observed**.

Freeze date: 2026-08-26.

## Motivation

The prior exact-pair V3 timing/state-history universe contained only 64 pairs because pair membership required at least one pre-existing strictly partner-attributed C-sample relationship transition event. That requirement is useful for an event-timing case-crossover study but is undesirable for a longitudinal state-transition dataset because it conditions inclusion on documented outcome/event availability.

The audited C-sample contains 584 directed romantic links, including 454 external romantic links. V4 broadens the development pair universe using relationship-link structure and exact birth-data quality only, before inspecting whether each pair has a formation, separation, divorce, or reunion endpoint.

This remains Astro-Databank development data. It is not independent validation of any astrology or Human Design hypothesis.

## Source

Primary relation/birth universe:

`https://www.astro.com/adbexport/c_sample.xml`

External exact records and structured histories:

public Astro-Databank wiki pages resolved by exact `DatamainID`.

Optional structured corroboration/history augmentation uses only the already-audited source chain defined below.

## Romantic-link definition

Only C-sample relationship records with these fixed relation IDs are eligible:

- 843 — spouse;
- 858 — lover;
- 859 — spousal equivalent.

No friendship, family, associate, affair-only event, or generic relationship category is added unless the structured relationship itself has one of those three romantic relation IDs.

## Focal C-sample birth-data gate

A directed romantic link can seed a candidate pair only when the focal C-sample record:

- has Rodden rating A or AA;
- has a non-unknown exact birth time;
- contains the C-sample `jd_ut` exact-time value.

No relationship event is required.

## Partner identity and birth-data gate

### Partner is internal to C-sample

Include the unordered pair only when the linked internal partner independently has:

- Rodden A or AA;
- exact non-unknown birth time;
- C-sample `jd_ut`.

### Partner is external to C-sample

Resolve the public ADB record using the structured `rel_adb_id` as the immutable identity key.

Resolution order:

1. direct public-wiki title derived from the relationship display string;
2. MediaWiki search fallback only to locate candidate titles;
3. accept a candidate page **only when its `DatamainID` exactly equals `rel_adb_id`**.

External partner inclusion then requires:

- Rodden rating A or AA on the exact public ADB record;
- explicit birth clock time (`sbtime`) with `t_unknown` absent/false;
- enough public ADB time-zone/meridian metadata to reconstruct UTC under the already validated exact-time V3 conversion method.

A missing public `jd_ut` is not itself exclusion because V3 already validated deterministic reconstruction from local clock time + ADB meridian metadata against 491 known records to sub-second error. If required conversion fields are missing or the conversion fails closed, exclude from exact-time modeling eligibility.

## Outcome-independent inclusion

The following must **not** affect pair-universe membership:

- presence or absence of marriage/divorce/separation events;
- presence or absence of explicit relationship year-ranges;
- whether the pair has a breakup, reunion, or death endpoint;
- relationship duration;
- whether astrology/HD features look interesting;
- whether a pair improves any model score.

This is the key anti-selection change from the 64-pair V3 event-linked universe.

## Unordered-pair deduplication

Pair key:

`adb:min(ID_A,ID_B)|adb:max(ID_A,ID_B)`.

Multiple directed C-sample links or multiple eligible relation codes between the same two ADB IDs merge into one pair while preserving all source relation records/codes.

Self-links where both ADB IDs are identical are excluded.

## Duplicate-person safeguard

Because public databases can contain duplicate/alternate records for the same real person, a candidate pair is flagged as `possible_same_person_duplicate` and excluded from modeling eligibility only when all of the following hold:

1. the two records resolve to the same ADB-linked English-Wikipedia/Wikidata identity **or** their normalized public names are identical;
2. birth calendar date is identical;
3. reconstructed UTC birth times differ by <=60 seconds;
4. birth-place coordinates, when present for both, differ by <=0.01 degrees in both latitude and longitude.

A shared Wikipedia article alone is insufficient for exclusion, because legitimate couples such as jointly documented creative partners can share one article.

All duplicate-person exclusions must retain provenance.

## Ephemeris/model-eligibility preflight

History recovery itself may retain every birth-data-qualified pair.

Before any later exact astrology/HD model is fit, both members' natal and HD design-root dates must fall within the pinned Swiss ephemeris files and return SWIEPH, not Moshier fallback. Unsupported pairs are excluded from model eligibility before feature calculation.

Pinned file hashes remain:

- `sepl_18.se1`: `ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66`;
- `semo_18.se1`: `1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7`.

## State-history source hierarchy

Biography prose is excluded from V4 because the attempted Rung-1 prose parser produced demonstrable lexical/date-association errors.

Apply the already-audited structured sources to all broad-universe pairs in this fixed order, retaining provenance and precision:

### H1 — public ADB structured Relationships and Events

- `ASTRODATABANK_rel` exact `RelatedDatamainID` romantic relationship templates;
- `ASTRODATABANK_evn` romantic event codes;
- event-to-partner attribution requires the same strict normalized partner-token rule used in V1;
- explicit finite `YYYY-YYYY` relationship-note ranges are retained as interval-censored active ranges;
- event dates retain day/month/year source precision.

### H2 — conservative finite-range nonfatal-exit augmentation

Reuse the frozen V2 rule:

- explicit nonfatal ending wording in the structured relationship note, or
- both partners demonstrably alive via structured dated ADB events strictly after the finite range endpoint.

A range-derived exit remains the full endpoint calendar year.

### H3 — ADB-linked English-Wikipedia lead infobox

Reuse the audited Rung-2 parser rules:

- only an explicit ADB `[[wikipedia:...]]` identity link;
- no name-search Wikipedia;
- first lead Infobox only;
- spouse/spouses/partner/partners fields only;
- exact linked-partner attribution when both identities exist;
- a new nonfatal endpoint requires an explicit nonfatal marker such as divorce/separation/annulment plus a parseable end date/year;
- bare end year without nonfatal semantics does not count.

### H4 — exact linked Wikidata qualifiers

Reuse the frozen Rung-3 rules:

- QID inherited only through exact ADB -> explicit ADB-linked Wikipedia -> `wikibase_item` chain;
- exact opposite-partner P26 spouse / P451 unmarried-partner statement only;
- P580 start, P582 end, P1534 end-cause qualifiers only;
- a new nonfatal endpoint requires usable P582 plus P1534 whose exact English label matches the frozen nonfatal families;
- death/widowhood end causes do not count as nonfatal dissolution.

## Evidence precedence

1. exact structured ADB romantic event;
2. conservative H2 ADB range-derived exit;
3. audited Wikipedia-infobox evidence;
4. exact Wikidata evidence.

Overlapping lower-precedence evidence corroborates rather than duplicates a transition. Non-overlapping claims are retained as separate possible transitions or conflicts according to the existing source-specific rules; they are never averaged to improve astrological fit.

## Conservative state labels

The history artifact may represent:

- `not_together_or_unobserved`;
- `romantic_active`;
- `committed_active`;
- `nonfatal_exit` / `dissolved`;
- `reunited`;
- death/censoring as a competing risk when explicitly structured.

A reunion requires a later accepted formation/start interval whose earliest date is strictly after the prior accepted nonfatal-exit interval's latest date. Overlapping intervals do not establish reunion.

Separate structured Wikidata statements for the same pair may establish a repeated start only if each start/end interval is explicit and ordered without overlap.

## Required broad-universe audit outputs before any model spec

Report at minimum:

- directed eligible romantic links from A/AA exact-time C-sample focal records;
- internal candidate pairs and internal final exact-time pairs;
- unique external target IDs;
- external public pages exactly ID-resolved / unresolved;
- external exact-time A/AA partners recovered;
- final unique birth-data-qualified exact-time pairs;
- possible-same-person duplicate exclusions;
- pair count surviving Swiss natal/design-root preflight;
- history evidence counts by source/transition/precision;
- unique pairs with at least one usable nonfatal exit;
- unique pairs with at least one strict reunion sequence;
- number of conflicts/interval-censored endpoints.

## Frozen sufficiency gates for later development models

Do not fit any astrology/HD transition model during universe/history recovery.

After history recovery:

### Dissolution/nonfatal-exit transition model

A separate model specification may be written/frozen only if there are at least:

- **50 unique exact-time pairs** with at least one usable nonfatal-exit endpoint.

### Same-partner reunion transition model

A separate reunion-hazard specification may be written/frozen only if there are at least:

- **30 unique exact-time pairs** with a strict nonfatal-exit -> later same-partner formation/reunion sequence.

### General multi-state semi-Markov model

Any fitted transition family must have at least **30 observed transitions** of that type, and the overall model dataset must contain at least **50 unique exact-time pairs with an observed nonfatal transition**.

If a specific transition type fails its gate, do not pool unlike transitions merely to reach sample size.

Crossing a gate authorizes only writing and freezing a separate model specification. It does not authorize immediate feature fitting.

## Anti-leakage

During V4 pair-universe construction and state-history recovery:

- do not calculate or inspect astrology/HD pair features;
- do not use prior V3 XEX/Davison/composite feature results to select people or histories;
- do not require a documented outcome for pair membership;
- do not lower sufficiency gates after counts are observed;
- do not manually resolve ambiguous event dates based on whether they improve model fit.

## Development/validation status

All V4 ADB data remain **development** data because the source and many feature families have already been examined during prior project work.

Any model emerging from V4 requires genuinely independent couples for confirmatory validation before being described as predictive evidence for astrology or Human Design.
