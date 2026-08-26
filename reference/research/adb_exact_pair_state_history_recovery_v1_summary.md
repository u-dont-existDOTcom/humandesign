# ADB Exact-Pair State-History Recovery V1 — Result Summary

Status: **successful structured-data recovery, but insufficient dissolution/reunion endpoints for the frozen semi-Markov go threshold**.

Frozen extraction specification:
`reference/research/adb_exact_pair_state_history_recovery_freeze_v1.md`

Result artifact:
`reference/research/adb_exact_pair_state_history_recovery_v1.json`

Freeze SHA-256:
`57cedb775249ff4cf182dc3858f55de3fece439091e3921fd3ca89782251f004`

## Why this recovery was run

The exact-pair timing V3 study produced 64 high-quality exact-time romantic pairs but only 11 dissolution events under the original C-sample event linkage. Before fitting a semi-Markov relationship-state model, V1 attempted to recover richer public Astro-Databank state histories for those same pairs, without inspecting any astrology or Human Design features.

The pair universe was frozen to the V3 exact-time sample; newly discovered relationship-history content could not add new pairs.

## Engineering correction

The first parser implementation returned zero histories because it expected rendered bullet-style wikitext. A separate raw-page structure probe showed that public ADB stores the relevant sections as structured templates:

- `ASTRODATABANK_rel` for Relationships;
- `ASTRODATABANK_evn` for Events.

The engineering runner was therefore adapted to those existing structured fields without changing the frozen research rules. In particular, relationship identity could be checked against `RelatedDatamainID`, while event attribution continued to require the frozen partner-name rule in event notes.

## Pair and identity recovery

- eligible exact-time V3 pairs: **64**;
- people involved: **123**;
- public ADB wiki people resolved by exact `DatamainID`: **123/123**;
- unresolved people: **0**.

Resolution methods:

- direct page name: 75;
- previously recovered known title: 48.

## Structured history recovered

Across the 64 pairs:

- accepted raw event evidence items: **164**;
- merged transition events: **108**;
- explicit structured relationship year-ranges: **52**.

Raw event evidence by kind:

- marriage: **109**;
- meet significant person: **14**;
- begin significant relationship: **4**;
- end significant relationship: **8**;
- divorce: **29**.

Event evidence by precision:

- exact day: **117**;
- calendar month: **18**;
- calendar year: **29**.

Seven non-overlapping same-kind reports were retained as evidence conflicts rather than silently reconciled.

## History usefulness tiers

- T3 — formation plus dissolution/reunion with month-or-better precision: **13 pairs**;
- T2 — formation plus dissolution/reunion with at least one year-precision endpoint: **9 pairs**;
- T1 — formation only and/or coarse active range: **42 pairs**;
- T0 — no structured history: **0 pairs**.

Thus every exact-time pair gained some structured relationship-history evidence, but only **22/64 pairs** had a usable dissolution or reunion endpoint under the frozen conservative rules.

No reunion sequence was inferred from the accepted structured events.

## Frozen stop/go result

The preregistered recovery rule required at least **30 exact-time pairs** with a usable dissolution or reunion endpoint before a separate semi-Markov dissolution/reunion model could even be specified for this ADB development source.

Observed endpoint pairs: **22**.

Therefore:

**DO NOT FIT the dissolution/reunion semi-Markov model from V1.**

Reducing the threshold after observing 22 would be post-selection and is not permitted.

## What the null reunion count means

The zero inferred reunions should not be interpreted as evidence that reunion is rare in real relationships. It means the structured ADB fields available under this deliberately narrow extraction rule do not document a clear dissolution-followed-by-new-formation sequence for these 64 exact-time pairs.

ADB is also a public-figure database whose relationship data are heavily weighted toward marriages and notable events, so it is not a representative longitudinal relationship panel.

## Next defensible data step

The V1 specification explicitly left death/observation-end competing risks for a later pass. A natural non-astrological augmentation is therefore to recover structured death/last-observation evidence and use it to interpret finite ADB relationship year-ranges conservatively:

- a finite relationship range whose end is demonstrably before both partners' death/censoring evidence can support a nonfatal relationship-exit interval;
- a range ending at a partner's death must remain a competing-risk exit rather than a breakup;
- exact structured divorce/end events remain higher-quality endpoints;
- no astrology/HD feature may be inspected during this augmentation.

That augmentation must be frozen before counting how many additional usable endpoints it produces.

## Bottom line

The state-history recovery itself worked well: 123/123 people resolved and all 64 pairs acquired structured history. But the conservative V1 endpoint count was **22**, below the frozen **30-pair** minimum. The correct action is to improve state-history ascertainment under a new frozen source/competing-risk specification, not to fit an underpowered relationship-reunion model or lower the threshold after the fact.
