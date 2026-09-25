# Life Patterns human UI — redundant citation-control defect — 2026-09-09

Status: blocking human-transport usability defect found by owner inspection before any qualifying independent human first pass.

## Observed defect

After the auditor answers **Yes — clearly shown** and selects the behavior shown by the exact source, the current plain-language UI displays source-level checkboxes saying:

- `Use this quote as evidence for the behavior I selected`
- `This quote qualifies or goes against my selected behavior`

For the common case where a unit contains one exact source segment, the first checkbox asks the auditor to repeat a judgment already made by answering Yes and choosing the behavioral value. The second checkbox is also presented as a peer decision even when no counterevidence is present. This creates unnecessary cognitive burden and makes provenance bookkeeping look like a second substantive coding question.

## Scientific distinction

Exact source provenance remains important. The response contract requires at least one exact supporting source-segment ID for an observed code, and optional counterevidence provenance can preserve exceptions/conflicts.

But **provenance is not a second behavioral judgment**.

The correct human interaction is:

1. auditor decides whether the behavior question is Yes / No / Can't tell;
2. if Yes, auditor selects the behavioral value;
3. if there is exactly one exact source segment, that segment is automatically bound as the supporting provenance — no extra click;
4. if there are multiple exact source segments, ask only which quote(s) the auditor relied on for the selected behavior;
5. counterevidence/qualification marking is optional and visually secondary, used only when an exact source segment genuinely limits or conflicts with the selected behavior.

This preserves the exact exported response schema and source-segment IDs without converting bookkeeping into redundant questioning.

## Required correction

Presentation layer only:

- single-source observed units: auto-bind the sole exact segment as `supporting_source_segment_ids` and show a small informational note, not a checkbox;
- multi-source observed units: show `Which quote(s) show the behavior you selected?` and require at least one source segment as already required by the response validator;
- move optional counterevidence selection into a collapsed/secondary control labelled as an exception/conflict rather than as a peer yes/no judgment;
- No / Can't-tell units show no citation controls;
- preserve exact embedded handoff bytes, selected 44+22 units, response schemas, code values, recurrence semantics, blinding, and network boundary;
- no automated labels or target-model information may be introduced.

## Gate consequence

All auditor kits generated before this correction are superseded for new human collection. Independent human first-pass collection remains blocked until the corrected private HTML and replacement kit receive exact engineering/browser verification.
