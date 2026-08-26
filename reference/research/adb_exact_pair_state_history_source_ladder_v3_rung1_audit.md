# V3 State-History Source Ladder — Rung 1 Engineering Audit

Status: **Rung-1 additions quarantined from the model-sufficiency count pending independent corroboration.**

This audit was triggered by inspecting the extractor's own source-provenance output, not by any astrology or Human Design result. No astrology/HD features were calculated or consulted.

## Frozen-count result

The automated Rung-1 implementation reported:

- V2 baseline endpoint pairs: 23;
- newly endpoint-bearing pairs from Biography extraction: 2;
- optimistic total: 25;
- threshold: 30.

Thus the source-ladder branching decision is unaffected by any audit outcome: both 23 and 25 are below 30, so the already-frozen Rung 2 must run.

## Observed implementation defects

The provenance artifact reveals several unambiguous lexical/date-association false positives:

1. `MET` as a timezone abbreviation was matched by the case-insensitive `met` formation regex.
2. Generic occurrences of `marriage` / `wedding` were sometimes attached to unrelated dates in the same sentence, including death dates and birth dates.
3. The same-sentence partner rule is insufficient when one sentence discusses two different romantic partners. A sentence on Victoria Melita, for example, describes a split from one partner and later marriage to another partner in the same sentence; the implementation can attribute the earlier split to the later named partner.
4. A sentence such as `annulment announced ... on 15 September` without an explicit year next to the latter date can cause the nearest fully parseable date to fall back to the earlier marriage date, falsely assigning the marriage date as the annulment date.
5. Reunion inference inherited these false formation/exit associations and therefore cannot be trusted independently of the underlying evidence.

These are instrument/parser defects, not ambiguous astrological interpretations.

## Consequence

Do not use the Rung-1 additions or inferred reunions to satisfy the >=30 endpoint-pair gate.

For the next rung's sufficiency accounting, use the last clean frozen baseline, V2 = **23 endpoint pairs**, and add only independently valid Rung-2 evidence. Rung-1 Biography evidence may be retained as an exploratory/provenance artifact and can be marked corroborated when a cleaner structured source independently establishes the same endpoint, but it does not independently increase the threshold count.

This is deliberately conservative. It can only make it harder, not easier, to reach the model-fitting gate.

## Source-order integrity

The frozen source ladder itself is not altered:

1. ADB Biography was attempted first;
2. because even its optimistic automated result was <30, proceed to ADB-linked Wikipedia infoboxes;
3. proceed to linked Wikidata only if the clean cumulative endpoint count remains <30.

The 30-pair threshold and 64-pair universe remain unchanged.
