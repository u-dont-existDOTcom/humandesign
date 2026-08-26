# V3 State-History Source Ladder — Rung 2 Wikipedia Infobox Parser Freeze

Status: **parser details frozen before Rung-2 endpoint counts are observed**.

This operationalizes Rung 2 of `adb_exact_pair_state_history_source_ladder_freeze_v3.md`. It does not alter the 64-pair universe, 30-pair sufficiency threshold, or source order.

## Identity chain

1. Resolve the same ADB page by exact `DatamainID`.
2. Extract only an explicit raw ADB interwiki link of form `[[wikipedia:TITLE|...]]`.
3. Request that title from English Wikipedia's API with redirects enabled.
4. Do not search Wikipedia by name.
5. Record the canonical Wikipedia title returned by the redirect-resolved API.

If no ADB-provided Wikipedia link exists or the linked page cannot be resolved, that person has no Rung-2 source.

## Allowed Wikipedia content

Use only the first lead template whose name begins `Infobox`.

Only top-level infobox fields normalized to `spouse`, `spouses`, `partner`, or `partners` may provide relationship evidence.

Article prose, references, categories, navboxes, and later templates are excluded.

## Partner attribution

For a pair A/B, an infobox relationship entry belongs to B only when:

- it contains a wikilink whose normalized target equals B's canonical ADB-linked Wikipedia title; or
- if B has no ADB-linked Wikipedia identity, the entry contains at least one frozen normalized name token from B's ADB name.

When both partners have linked Wikipedia identities, exact linked-title matching takes precedence and token-only matching is not used.

## Marriage-template entries

Recognize balanced nested templates whose template name begins `marriage` or `married`.

An entry contributes a nonfatal exit only when:

1. it is attributed to the opposite partner under the rule above;
2. the template explicitly contains a nonfatal ending marker matching `divorc*`, `separat*`, `annul*`, `split*`, `breakup`/`broke up`, `dissolv*`, or `estrang*`;
3. an end date can be parsed from an explicit named end-date/end-year/to field, or, when the ending marker itself occupies an `end=`/reason parameter, from the latest dated positional parameter after the partner parameter;
4. at least one parseable date is distinct from the relationship start date when a start date is explicitly identifiable.

A template with an end reason but no recoverable end date is retained as undated provenance but does not count as an endpoint.

## Plain infobox entries

After marriage templates are separately extracted, plain spouse/partner text may be considered only in fragments separated by an explicit line break, HTML `<br>` break, or list-item boundary.

A plain fragment contributes a nonfatal exit only when the same fragment contains:

- the opposite partner attribution;
- an explicit nonfatal ending marker from the same list;
- a parseable date/year.

If multiple date expressions occur, choose the nearest parseable date expression to the ending marker by character distance. A tie between distinct dates is rejected.

A bare end year with no explicit nonfatal ending marker is not accepted.

## Dates

Preserve source precision:

- exact date -> one-day interval;
- month/year -> full calendar month;
- year -> full calendar year.

Recognize explicit year values and standard date templates such as `start date`, `birth date`, or `date` only when they occur inside the permitted spouse/partner entry. For marriage-template endpoints, named end-date fields take precedence over generic date candidates.

## Baseline after Rung-1 audit

Because the Rung-1 parser generated demonstrable false lexical/date associations, its additions are quarantined. Rung-2 model-sufficiency accounting starts from the last clean frozen V2 baseline of **23 endpoint pairs**.

Rung-1 evidence may be reported as independently corroborated when Rung 2 recovers the same transition, but it does not independently raise the threshold count.

## Duplicates and conflicts

- An infobox endpoint overlapping an existing V1/V2 endpoint is corroboration, not a new endpoint.
- Multiple distinct nonfatal states such as separation followed by divorce may both be retained.
- A source item that cannot be attributed to one partner entry unambiguously is excluded rather than guessed.

## Stop rule

After Rung 2:

- total clean endpoint pairs >=30 -> stop source acquisition and write/freeze a separate semi-Markov model specification;
- total <30 -> proceed to already-frozen Rung 3 (linked Wikidata qualifiers).

No astrology or Human Design feature may be calculated or inspected during extraction or adjudication.
