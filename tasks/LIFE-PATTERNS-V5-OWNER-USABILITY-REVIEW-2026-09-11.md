# Life Patterns V5 owner usability review — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Goal

Owner reviews the generated private V5 calibration interface for comprehensibility and usability. This is **not** an annotation pass and does not authorize human collection.

Private review package supplied to the owner:

`Life-Patterns-V5-PRIVATE-Owner-Review-2026-09-11.zip`

Public-safe candidate receipt:

`state/LIFE-PATTERNS-V5-PRIVATE-UI-OWNER-REVIEW-CANDIDATE-2026-09-11.json`

## What the owner should review

Open the HTML inside the private ZIP in the normal intended browser. Browse representative units rather than completing the 66-unit calibration pass.

Evaluate whether:

- the narrator's exact source is easy to read first;
- the main question and fallback choices are understandable;
- `Doesn't apply to this story` clearly means the prerequisite is affirmatively absent;
- `Not enough information` clearly means evidence is insufficient;
- behavioral choices are understandable without knowing internal Rxx identifiers;
- facets feel like meaningful separate dimensions rather than duplicated choices;
- hybrid affirmative/absence UI is understandable when encountered;
- four absence checks are understandable and not misleading;
- provenance questions appear only when genuinely needed;
- stage/chronology questions appear only when they make sense;
- recurrence questions for repeated-series units are understandable;
- navigation, save state, backup, and final-download affordances are understandable.

Do not make substantive participant-coding judgments merely to test the interface. If a conditional control is inconvenient to reach without doing real annotation, report the usability concern rather than manufacturing an answer.

## Owner outcome

Return one of:

1. **Accepted for presentation** — the interaction is understandable enough to preserve as the target human surface; or
2. **Usability defects** — identify the concrete interaction/text/layout problem and what made it confusing or burdensome.

Acceptance is an owner usability judgment only. It does not by itself authorize human collection.

## After acceptance

Before collection, make the accepted surface reproducible through one of two routes:

- promote the portable adapter implementation and focused public-only tests to the repo, then obtain green CI against the accepted V5 validator; or
- regenerate the accepted interface through `scripts/build_life_patterns_human_calibration_ui_v5_final.py` in an environment with the complete local repository/template chain and smoke that exact output.

Once reproducibility is green, persist a public-safe owner-acceptance/reproducibility receipt and update canonical state. Only then may the independent human first pass begin.

## Hard boundaries

- no private calibration HTML or participant exact text in public GitHub;
- no human collection before explicit owner acceptance plus reproducible generation;
- no automated participant coding before the revised independent human pass is complete and frozen;
- no target-model scoring/reveal;
- no merge/deploy, recruitment/contact, or spending without separate authorization.
