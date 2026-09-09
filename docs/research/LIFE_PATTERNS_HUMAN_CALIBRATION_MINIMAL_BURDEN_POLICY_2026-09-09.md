# Life Patterns human calibration — minimal-burden human UI policy

Status: controlling presentation policy for the independent theory-blind human first pass. This policy changes **presentation and collection burden only**. It does not change the frozen v2 evidence, selected 44+22 units, behavioral code values, recurrence semantics, response schemas, package/handoff identities, or target-model blind.

## Trigger

Owner browser review before any qualifying human pass exposed a repeated design error: the interface was exposing machine-oriented representation choices as if they were meaningful human questions. Examples included source-segment IDs, a value-relation dropdown when only one behavior was selected, asking whether behaviors happened in “this order” before showing any order, optional metadata that most humans would rationally skip, opaque validation errors, and a second source-citation question after the behavioral judgment was already made.

## Governing rule

> The human auditor should make only judgments that can change the calibration result. Machine bookkeeping is automatic. A conditionally required judgment appears only when the condition is actually present. If a field is truly optional and is not part of the planned human-calibration comparison, do not ask the human to fill it.

## Required human-facing flow

For each selected unit:

1. read the exact source;
2. answer one plain behavior question: **Yes / No / Can't tell**;
3. if Yes, select the behavior(s) shown;
4. only if two or more behaviors are selected, answer whether the source establishes an order;
5. only if order is established, arrange the selected behaviors in that order using their plain-language labels;
6. only if a selected behavior is a substantive non-action value, answer the four required prerequisite checks in plain language;
7. only if Other Specified is selected, describe it;
8. for repeated-series units, answer the required recurrence/exception questions in plain language;
9. source provenance is automatic for a one-quote unit; with multiple exact quotes, select the quote text actually relied on.

## Do not expose machine representation as a task

The auditor does not need to understand or see:

- `EP-002-SEG-01`-style source IDs;
- `R05-R8`-style code IDs;
- `value_relation=single` when only one behavior is selected;
- internal ontology/registry terminology;
- source hashes/content-address IDs;
- hidden defaults used only to satisfy the response transport schema.

These remain in the exported machine record where required.

## Ordering

Never ask “did these happen in this order?” before an order has been shown.

When multiple behaviors are selected, ask first:

> Did the story say these happened in a particular order?

If Yes, then show the selected behaviors by their human-readable wording and allow the auditor to arrange them. If No, export unordered-multiple semantics. For a single selected behavior, export `single` automatically and show no relation control.

## Optional-field rule

Optional controls create predictable missing-not-at-random data because conscientious auditors will vary in how much unpaid optional work they perform. Therefore:

- if a field is required for the planned calibration comparison or schema validity, make it conditionally required and explain why;
- if it is not required for the human comparison, do not show it in the first-pass UI;
- keep auxiliary metadata available to automated coding/adjudication elsewhere rather than burdening the independent human pass.

For the current first pass, generic context qualifiers, language, free-form coder note, generic missingness flags, generic influence metadata, and optional counterevidence tagging are not primary human-calibration targets and should not appear in the normal unit flow. Their transport defaults remain valid. The exact source itself remains available for later disagreement adjudication.

## Source provenance

Source provenance is bookkeeping, not a second behavioral decision.

- one exact source segment: bind it automatically for an observed answer;
- multiple exact source segments: ask which **quote text** the auditor relied on;
- never show the internal segment ID as the human-facing label.

## Validation/error copy

Never surface errors such as:

- “Observed requires a value relation”;
- “non-action flag disagrees with registry”;
- “value outside frozen ontology.”

Translate a recoverable problem into the exact action the human can take, e.g.:

- “Choose at least one behavior.”
- “You selected more than one behavior. Tell us whether the story gives a clear order.”
- “This ‘did not act’ behavior only counts when all four extra checks are Yes. Choose another behavior or Can't tell.”
- “Choose the quote(s) you relied on for this Yes answer.”

Unexpected internal corruption should fail closed with one nontechnical message telling the auditor to stop and report the technical problem.

## Scientific boundary

This policy is intentionally presentation-only. It must preserve:

- exact private handoff bytes;
- selected 44 episode + 22 repeated-series units;
- episode/series response schema versions;
- recurrence-v2 method;
- blinding and no-network requirements;
- first-pass chronology;
- development-only / validation-use-forbidden status.

No automated label or target-model information may be used to tune this UI.
