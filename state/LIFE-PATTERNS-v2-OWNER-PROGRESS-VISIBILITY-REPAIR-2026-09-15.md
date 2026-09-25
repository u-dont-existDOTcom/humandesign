# Life Patterns v2 — owner progress-visibility repair — 2026-09-15

## Owner finding

A dynamic interview can feel indefinitely open-ended if the participant cannot see whether they are near the beginning or near the end. Hiding the internal category queue correctly made the interview more natural, but it also removed the only visible completion horizon.

## Product requirement

Keep the fixed scientific coverage contract hidden from the participant as a rigid script, while exposing enough aggregate progress to answer the practical question: am I likely to be here for another minute, another ten minutes, or much longer?

## Repair

The live dynamic UI now includes a persistent **Interview progress** card near the top of the page.

It shows:

- a progress bar;
- approximate percentage through required coverage;
- a rough remaining substantive-question range;
- a rough remaining-time range;
- an explicit note that the estimate can shrink faster than a fixed questionnaire because one answer may cover several required dimensions.

The estimate uses the fixed coverage state without exposing domain names or a category queue. Fully resolved dimensions count as complete; `partial` dimensions contribute half-weight to the rough progress estimate; unassessed dimensions remain open.

This is an orientation aid, not a scientific endpoint or promise of an exact number of questions/minutes. The actual interview remains dynamic and target-theory-blind.

## Regression

`tests/unit/test_life_patterns_v2_owner_dynamic_coverage.py` now requires the persistent progress card, percentage calculation, remaining-question estimate, time-range copy, and progress refresh hooks.

## Mission Control

The exact owner correction is also captured on the existing Mission Control logic-correction branch as:

`feedback/mission-control/SDF-20260915-LIFE-PATTERNS-PROGRESS-VISIBILITY-009.json`

Its truth state remains `CAPTURED_BRANCH_ONLY` until that draft Mission Control PR is accepted.

## Verification boundary

Owner consumer-seam check: the progress card should be visible throughout the interview, update after coverage changes, and provide useful orientation without exposing or forcing a category-by-category script.
