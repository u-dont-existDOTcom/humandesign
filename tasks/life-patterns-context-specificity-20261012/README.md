# Context-dependent answer evidence — Life Patterns offline pilot

**Status:** experimental source-preserving offline interface, not the live survey and not a birth-chart scoring engine.

## Why

In a single development pilot, 13 of 25 questions received all four example answers. Those examples often described compatible and context-dependent behaviors, not four independent stable traits. The solution is not to force a winner: elicit the conditions behind the strategy and an actual recent example, while permitting uncertainty or no stable default.

## Implemented

The separately installed offline V3 experiment adds three OPTIONAL source fields to each answered question:

- `context_rule`: under what conditions would the participant choose among the selected options?
- `recent_case`: one recent situation, the first action taken, and a counterexample if remembered.
- `no_stable_default`: explicit acknowledgment that there is no consistent default across varied situations.

There are source-neutral targeted clarifiers for 16 question routes; all other routes get a generic contextual probe. The original multiple-choice answer options, `Other`, uncertainty, skip and unusual-behavior inventory remain available. Import of an existing V3 local export requires no new data fields; the optional fields persist on subsequent exports and do not overwrite the original participant reply. Selecting all four opens the optional probe to make it visible, not mandatory.

The prototype intentionally avoids birth data, natal outcomes, clinical diagnostic claims, automatic personality labels, and any network traffic. No data are scored or sent to Railway. The live GPT and previously independently reviewed records stay unchanged.

## Tests and scientific interpretation

1. The original V3 JSON roundtrip and distinct-behavior editing smoke test must still pass.
2. The new browser test imports all 25 synthetic answers, opens the contextual probe on an all-four question, records optional context and a real example, switches questions, exports and reimports, and verifies original answers/behavior items are unchanged.
3. Unknown context value types are rejected, and all user text is rendered through text nodes rather than HTML interpretation.
4. Mobile-width layout, browser script errors, external requests, and chart-label leakage are checked.
5. Research outcomes must later compare examples-only versus examples-plus-context questions on **new people**, using blinded neutral coders and measuring information gain, response burden, stability, counterexamples and agreement. Longer answers by themselves are not proof of discriminating trait information.

A separate historical Neptune source audit preserves the distinction between spiritual practice, deliberate altered-state pursuit, psychoactive-substance exploration and clinical dependence. It was selected after hearing one development person's known story and is **not** an independent natal validation claim. The historical-source language is not shown to a respondent.

## Methodological source

COSMIN content validity and response process guidance: https://pmc.ncbi.nlm.nih.gov/articles/PMC5891557/ . This is a survey-design methodology reference, not scientific support for astrology or Human Design.
