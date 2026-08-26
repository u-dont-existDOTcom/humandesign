# Exact-Pair State-History Recovery V3 — Frozen External Source Ladder

Status: **state-history ascertainment only; no astrology/HD model fitting**.

Freeze date: 2026-08-26.

## Purpose

V1 recovered 22 exact-time pairs with explicit dissolution/reunion endpoints. V2 conservatively increased that to 23. The fixed minimum for writing a separate semi-Markov dissolution/reunion model remains 30 endpoint pairs.

V3 freezes the remaining source-acquisition order before any of the new source counts are observed. This prevents choosing or abandoning data sources based on astrology/model performance or on which histories look convenient.

## Pair universe

Exactly the 64 unordered exact-time pairs already present in V1/V2.

No new pair may enter V3.

## Fixed source ladder

Apply the following sources in order. After each rung, recompute the number of pairs with a usable nonfatal dissolution/reunion endpoint.

### Rung 1 — strict ADB Biography sentence extraction

Use the `Biography` section of the same exact-`DatamainID` public ADB pages.

Accept a nonfatal ending sentence only when all are true:

1. the sentence contains at least one normalized name token of the opposite partner;
2. the sentence contains an explicit ending verb/term from:
   - `divorc*`
   - `separat*`
   - `split*`
   - `broke up` / `broken up`
   - `annul*`
   - `dissolv*`
   - `estrang*`;
3. the same sentence contains an explicit 4-digit year or a parseable day/month/year;
4. the sentence is clearly about the romantic relationship, not an unrelated legal/business separation.

Operationalize condition 4 by additionally requiring a same-sentence romantic cue from `marri*`, `wife`, `husband`, `spouse`, `lover`, `relationship`, `dating`, `dated`, `romance`, `couple`, `affair`, or `partner`.

No pronoun resolution across sentences is allowed. No manual inference from context outside the accepted sentence is allowed.

The extracted date remains at its source precision. A year-only statement is a full-year interval.

When a qualifying ending sentence contains multiple date expressions, choose the parseable date expression with the smallest character-distance to the matched ending term. If two distinct date expressions are tied for nearest distance, reject the sentence as date-ambiguous. This rule is frozen before Rung-1 counts are observed.

Formation sentences may also be accepted under the same same-sentence partner rule when they contain `met`, `began dating`, `started dating`, `married`, or `wedding` plus an explicit date/year, but formation recovery is secondary; V3's stop/go count concerns nonfatal exit/reunion endpoints.

### Rung 2 — ADB-linked English Wikipedia infobox only

Run this rung only if Rung 1 leaves fewer than 30 endpoint pairs.

From each resolved ADB page, use only an explicit ADB-provided link to the subject's English Wikipedia biography. Do not name-search Wikipedia when the ADB page supplies no such link.

On the linked Wikipedia page, use only the lead infobox wikitext, not article prose.

Accept spouse/partner history only when the infobox entry can be attributed to the opposite partner by an exact linked Wikipedia title or the frozen normalized name-token rule.

Accept a nonfatal ending only when the infobox/template explicitly marks an end as divorce, separation, annulment, breakup, or equivalent nonfatal termination. A bare end year with no end reason is not a nonfatal dissolution unless already supported by V1/V2 evidence.

Preserve exact source precision and provenance.

### Rung 3 — Wikidata spouse/partner statements with qualifiers

Run this rung only if Rungs 1+2 still leave fewer than 30 endpoint pairs.

Use a Wikidata entity only when it is linked from the already identity-resolved Wikipedia page from Rung 2; do not resolve Wikidata by name search.

Use spouse/partner statements only when the statement object resolves to the opposite partner's linked Wikidata identity.

Accept dates from structured statement qualifiers such as start time and end time. An end time alone is not assumed to be nonfatal. Count it as a nonfatal dissolution endpoint only when the structured statement or linked qualifiers explicitly identify divorce/separation/annulment, or when an already frozen V1/V2 nonfatal rule independently establishes that both partners survived the endpoint.

If Wikidata lacks a structured end-reason qualifier, retain the end time as a generic relationship exit/censoring datum but do not count it toward the 30 nonfatal-endpoint threshold.

## Stop rule

After each completed rung:

- if total usable nonfatal dissolution/reunion endpoint pairs is **>=30**, stop source acquisition and proceed only to writing/freeze of a separate semi-Markov model specification;
- if total is **<30**, continue to the next already-frozen rung;
- if all three rungs finish below 30, stop and declare the current public-figure source universe insufficient for this model.

This is a sample-size/data-ascertainment stopping rule, not a statistical-significance or astrology-performance stopping rule.

## Evidence precedence

When sources disagree:

1. exact structured V1 ADB event evidence;
2. V2 source-structured nonfatal exit evidence;
3. V3 ADB Biography same-sentence evidence;
4. V3 Wikipedia infobox evidence;
5. V3 Wikidata qualifiers.

Lower-precedence evidence may corroborate higher-precedence evidence but may not overwrite its date silently.

Non-overlapping conflicts are retained and excluded from the endpoint count until a source-only resolution rule can decide them. Astrology/HD information must never be used to adjudicate a conflict.

## Duplicate handling

Evidence from multiple sources that refers to the same transition and has overlapping precision intervals is merged as corroboration, not counted as multiple transitions.

## Reunion inference

A reunion is inferred only when a later accepted formation/relationship-start interval begins strictly after an accepted nonfatal exit interval for the same pair.

If intervals overlap, do not infer reunion.

## Frozen sufficiency threshold

The threshold remains **30 exact-time pairs** with at least one usable nonfatal dissolution/reunion endpoint.

Crossing 30 does not validate astrology and does not authorize immediate model fitting. It authorizes only the creation of a separately frozen semi-Markov model specification.

## Anti-leakage

Throughout V3 source recovery:

- do not compute astrology/HD features;
- do not inspect existing pair feature values;
- do not choose source interpretations based on whether an event produces a better astrological fit;
- do not lower the 30-pair threshold;
- do not expand the 64-pair universe.
