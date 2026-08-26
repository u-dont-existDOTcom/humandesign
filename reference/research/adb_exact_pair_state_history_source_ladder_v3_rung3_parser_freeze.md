# V3 State-History Source Ladder — Rung 3 Wikidata Parser Freeze

Status: **parser details frozen before Rung-3 endpoint counts are observed**.

This operationalizes Rung 3 of `reference/research/adb_exact_pair_state_history_source_ladder_freeze_v3.md`. It does not alter the 64-pair universe, source order, evidence precedence, or >=30 endpoint-pair sufficiency threshold.

## Starting clean endpoint count

The completed and audited Rung 2 resolved all 106 ADB-linked English-Wikipedia identities without source failure and increased the clean endpoint-pair count from 23 to **28**.

Rung 3 starts from those 28 clean endpoint-bearing pairs. Quarantined Rung-1 Biography-only additions remain excluded unless independently supported by a cleaner source.

## Identity chain

A Wikidata entity may be used only when its QID was returned as the `wikibase_item` of the exact English-Wikipedia page reached through the already frozen chain:

`exact ADB DatamainID -> explicit raw ADB [[wikipedia:...]] link -> redirect-resolved English Wikipedia page -> pageprops.wikibase_item`.

No Wikidata name search, label search, sitelink search, or fuzzy identity matching is allowed.

For pair A/B, relationship evidence is eligible only when both partners have such a linked QID.

## Allowed relationship properties

Inspect only non-deprecated statements from:

- `P26` — spouse;
- `P451` — unmarried partner.

A statement belongs to pair A/B only when its snak is an exact `wikibase-entityid` equal to the opposite partner's linked QID.

Statements pointing to any other QID are irrelevant, even if labels look similar.

## Allowed timing qualifiers

From an exact pair statement, retain only:

- `P580` — start time;
- `P582` — end time;
- `P1534` — end cause.

No other qualifier may be interpreted as relationship timing or termination semantics in Rung 3.

## Nonfatal endpoint rule

A Wikidata relationship statement contributes a new nonfatal exit only when all are true:

1. exact opposite-partner QID match under P26/P451;
2. a parseable `P582` end-time qualifier exists;
3. at least one `P1534` end-cause qualifier is present;
4. the end-cause item is resolved by exact QID and its English label matches one of the frozen nonfatal lexical families:
   - `divorc*`
   - `separat*`
   - `annul*`
   - `split*`
   - `breakup` / `break-up` / `break up`
   - `dissolv*`
   - `estrang*`.

The label match is case-insensitive after Unicode normalization and punctuation/whitespace normalization.

An end time with no P1534 end cause does **not** create a new nonfatal endpoint.

An end cause indicating death, widowhood, disappearance, or any cause outside the frozen nonfatal families does not count as a nonfatal relationship exit.

For the multiple-cause conflict rule below, an English end-cause label is treated as explicitly fatal/widowhood-related only when its normalized label contains one of the frozen lexical roots `death`, `deceas`, `widow`, `killed`, or `murder`. `disappear*` is non-qualifying but is not treated as a fatal-conflict root unless accompanied by one of those fatal roots.

### V1/V2 exception

If a P582 end time overlaps an already accepted V1/V2 nonfatal endpoint for that pair, it may be retained as corroborating provenance even without P1534. It cannot create a new endpoint-bearing pair because that pair is already in the clean baseline.

Rung-2 Wikipedia endpoints are also higher-precedence than Rung-3 Wikidata under the already frozen source ladder, so an overlapping Wikidata item corroborates rather than duplicates them.

## End-cause label resolution

Collect the exact QIDs used by P1534 on eligible exact-pair P26/P451 statements and resolve those entities directly through the Wikidata API (`wbgetentities` or equivalent exact-QID endpoint).

Use only their English `labels.en.value` for the frozen lexical check.

Do not use aliases, descriptions, article prose, parent classes, subclass reasoning, or model/world knowledge to expand an end-cause label into a qualifying category.

## Time parsing

Wikidata time datavalues encode a time string, precision integer, timezone, before/after uncertainty, and calendar model.

Retain all raw time metadata.

For the Rung-3 recovery artifact:

- precision >=11: day interval;
- precision 10: full calendar month interval;
- precision 9: full calendar year interval;
- precision <9: too coarse for a usable relationship endpoint and does not count.

If `before` or `after` is nonzero, retain the datum as uncertain provenance but do not count it toward the >=30 gate in Rung 3.

Gregorian calendar-model dates are converted directly to ISO intervals.

For a non-Gregorian calendar model, preserve the raw Wikidata time and calendar model but do not count it toward the >=30 gate unless the precision is only year-level, for which the civil year itself is sufficient for the source-recovery threshold. Exact calendar normalization would require a separately frozen downstream modeling rule.

## Multiple P582 values

If an exact relationship statement contains multiple distinct P582 intervals:

- if the intervals overlap, intersect them conservatively and retain all provenance;
- if they do not overlap, mark the statement end-time-conflicted and do not use it to create a new endpoint.

## Multiple P1534 values

If at least one exact end-cause label matches a frozen nonfatal family and none of the other resolved P1534 labels explicitly indicate death/widowhood, the statement may qualify.

If nonfatal and death/widowhood end causes coexist on the same statement, flag a cause conflict and do not use the statement to create a new endpoint.

Unresolved P1534 QIDs are retained as unresolved and do not qualify by themselves.

## Evidence merging and precedence

For each pair:

1. V1 structured ADB event evidence;
2. V2 conservative ADB range/later-life evidence;
3. audited Rung-2 Wikipedia-infobox evidence;
4. Rung-3 Wikidata evidence.

An overlapping lower-precedence endpoint is corroboration.

A non-overlapping Rung-3 endpoint for a pair that already has a higher-precedence endpoint is retained as a distinct possible state transition, but it does not change whether the pair counts toward the sufficiency threshold.

For a pair with no clean higher-precedence endpoint, a qualifying Rung-3 endpoint may add exactly one endpoint-bearing pair regardless of how many qualifying statements it contains.

## Reunion inference

Rung 3 does not infer a reunion from Wikidata end-time data alone.

A reunion can only be inferred if there is a later already accepted formation/start interval under a prior frozen source rule whose interval starts strictly after the qualifying nonfatal exit interval. Overlapping intervals do not establish reunion.

## Stop rule

After processing all 64 pairs:

- total clean endpoint-bearing pairs >=30 -> **STOP source acquisition** and proceed only to writing/freezing a separate semi-Markov model specification;
- total <30 -> the frozen three-rung public-source ladder is exhausted; declare this exact 64-pair public-figure source universe insufficient for the planned dissolution/reunion semi-Markov fit.

The >=30 threshold may not be lowered after seeing Rung-3 results.

## Anti-leakage

No astrology or Human Design feature may be computed, inspected, plotted, or used in Rung 3. Identity, end-cause classification, conflict handling, and endpoint counting are determined solely by the frozen linked-source structure above.
