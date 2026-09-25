# Life Patterns human calibration UI — human-first correction

Status: owner-directed presentation correction before any qualifying independent human first pass.

## Defects found by owner browser review

The previous UI remained too close to the machine response schema even after plain-language cleanup:

- after selecting multiple behaviors it asked whether they occurred in “this order” before showing any order;
- when the user then chose ordered sequence, the ordering list appeared only afterward and used opaque code IDs;
- optional influence/counterevidence/context/missingness/note fields were presented despite not being part of the minimum planned human-calibration comparison, creating predictable skipped/missing data and needless burden;
- a one-quote influence/source-provenance question asked the human to confirm the only possible source again;
- validation errors surfaced internal schema concepts such as value relation and non-action registry semantics instead of telling the human what action to take;
- internal source/code identifiers were still leaking into human-facing controls.

No independent human first-pass data had been collected, so this is corrected before collection.

## Controlling correction

The UI is for a human auditor, not for the response schema author.

1. One behavioral question per unit: Yes / No / Can't tell.
2. One selected behavior -> `single` recorded automatically; no relation control.
3. Multiple selected behaviors -> ask **whether the story establishes an order**, without presupposing one.
4. Only after the auditor says an order exists, show the selected behaviors in plain language and let the auditor arrange them.
5. Machine code IDs and source IDs are hidden from human-facing labels.
6. One exact quote -> source provenance auto-bound.
7. Multiple exact quotes -> show actual quote text and ask which quote(s) the auditor relied on.
8. Generic optional counterevidence, influence, missingness, context, language and note fields are not shown in the normal human pass; their valid schema defaults are exported automatically.
9. Conditionally necessary work remains visible and required: multi-behavior relation, ordered sequence, Other Specified description, non-action prerequisites, required repeated-series recurrence/exception judgments, and multi-source provenance.
10. Validation errors must state the concrete corrective action in ordinary language.

## Scientific rationale

Optional human metadata is not free information. If it is displayed but not required, completion will vary by auditor patience and perceived relevance, producing missing-not-at-random auxiliary data. If a field is necessary to the planned comparison, make it conditionally required. If it is not necessary, omit it from the first-pass task.

The minimum human-calibration comparison already prioritizes applicability, substantive values, IE/NA, non-action prerequisites, sequence, Other Specified, and recurrence-v2 fields. Exact source remains available for later disagreement adjudication, so the human first pass does not need every auxiliary transport field.

## Boundary

Presentation only. Do not alter:

- exact private handoff/evidence;
- selected 44 episode + 22 repeated-series units;
- episode/series response schemas;
- recurrence-v2 semantics;
- target-theory blind;
- no-network boundary;
- first-pass-before-automated-label chronology;
- development-only / validation-use-forbidden status.
