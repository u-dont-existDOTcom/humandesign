# Life Patterns V5 owner usability review — R2 — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Goal

Owner reviews the repaired private V5 calibration interface for comprehensibility and usability. This is **not** an annotation pass and does not authorize human collection.

Private R2 package supplied to the owner:

`Life-Patterns-V5-PRIVATE-Owner-Review-R2-2026-09-11.zip`

Public-safe owner-feedback disposition:

`state/LIFE-PATTERNS-V5-OWNER-USABILITY-FEEDBACK-001-2026-09-11.json`

The earlier package `Life-Patterns-V5-PRIVATE-Owner-Review-2026-09-11.zip` is superseded for owner review.

## Why R2 exists

Owner review found that the broad behavioral question could clearly be answered Yes while the closest specific value was absence-dependent and correctly could not be asserted because the required four evidence checks were not all established.

That is a presentation problem, not permission to weaken the absence gate. R2 explicitly separates:

1. whether the general observable situation applies; from
2. whether one of the specific coded behaviors is sufficiently established.

The relevant evidence-state choices now read:

- **Yes — a specific behavior below is established**
- **Doesn't apply to this story**
- **Not enough information for a specific behavior**

The third choice explicitly explains that the general situation can still clearly apply.

Absence-dependent choices are also labelled before selection. If the four-part gate is incomplete, the error explains that the specific value cannot count and points to the specific-value insufficient state rather than implying that the story itself is irrelevant.

## What the owner should review

Open the HTML inside the R2 ZIP in the normal intended browser. Browse representative units rather than completing the 66-unit calibration pass.

First revisit the previously problematic choice-construction/resolution unit and check whether the distinction above now feels natural. In particular, it should be possible to think **“yes, this is clearly a choice story”** while still choosing **“Not enough information for a specific behavior”** when the closest absence-dependent subcode cannot satisfy all four evidence checks.

Then evaluate whether:

- the narrator's exact source is easy to read first;
- the general behavioral question is understandable;
- the evidence-state choices no longer contradict the general question;
- `Doesn't apply to this story` clearly means the prerequisite situation itself is affirmatively absent;
- `Not enough information for a specific behavior` clearly means the situation may apply while the specific distinction is unsupported;
- absence-dependent choices are visibly different from ordinary affirmative choices before selection;
- behavioral choices are understandable without internal Rxx identifiers;
- facets feel like meaningful separate dimensions rather than duplicated choices;
- hybrid affirmative/absence UI is understandable when encountered;
- the four absence checks are understandable and not misleading;
- provenance questions appear only when genuinely needed;
- stage/chronology questions appear only when they make sense;
- recurrence questions for repeated-series units are understandable;
- navigation, save state, backup, and final-download affordances are understandable.

Do not manufacture substantive participant-coding judgments merely to exercise conditional controls.

## Owner outcome

Return one of:

1. **Accepted for presentation** — the R2 interaction is understandable enough to preserve as the target human surface; or
2. **Usability defects** — identify the concrete interaction/text/layout problem and what made it confusing or burdensome.

Acceptance is an owner usability judgment only. It does not by itself authorize human collection.

## After acceptance

Promote the same presentation-only distinction into the canonical public V5 builder with focused tests and green CI. The four-part absence gate and accepted V5 scientific semantics remain unchanged.

Once reproducibility is green, persist a public-safe owner-acceptance/reproducibility receipt and update canonical state. Only then may the independent human first pass begin.

## Hard boundaries

- do not weaken the four-part absence gate to make a narrative fit;
- no private calibration HTML or participant exact text in public GitHub;
- no human collection before explicit owner acceptance plus reproducible generation;
- no automated participant coding before the revised independent human pass is complete and frozen;
- no target-model scoring/reveal;
- no merge/deploy, recruitment/contact, or spending without separate authorization.
