# Life Patterns v2 — dynamic cross-thread coverage repair — 2026-09-15

## Owner requirement

The owner clarified that scientific standardization must not turn the participant experience into a rigid category-by-category questionnaire. All required measurement dimensions still need to be covered, but the interview should reuse what the participant has already said, credit it across every dimension it genuinely informs, and avoid asking the same thing again later under a different category heading.

## Failure risk

The prior standardized coverage implementation had two distinct layers:

- participant-led natural pattern interviews whose evidence could already satisfy multiple required dimensions;
- a later `Continue required coverage` path that selected the **first incomplete dimension in registry order** and opened its canonical screener.

That meant the measurement contract was standardized, but the remaining coverage sweep still had a rigid-order fallback as its actual normal path. A participant could therefore experience the system as a sequence of categories, especially when a dimension was only partially covered and the canonical screener repeated information already supplied elsewhere.

## Repair

The scientific contract remains the same fixed `life-patterns-recoverability-coverage-v2` set of 23 required dimensions. The change is to the question-selection mechanism, not the measurement target.

New behavior:

1. Every completed thread is still assessed against **all** required dimensions, so one answer can satisfy several dimensions when its cited evidence genuinely supports them.
2. The client maintains aggregate coverage across threads.
3. `Continue interview` sends the aggregate coverage plus settled pattern summaries to a target-blind next-question selector.
4. Dimensions already `sufficient`, `unknown`, `inapplicable`, or `declined` are closed and cannot be re-asked merely because a canonical screener exists.
5. A `partial` dimension receives only a question about the missing discriminator, not a restart of the whole category.
6. Among still-open dimensions, the selector chooses the next question by expected information gain and conversational continuity rather than registry order.
7. One question may illuminate several still-open dimensions; the internal `primary_domain_id` is routing metadata only.
8. Canonical screeners remain a fallback/debug seam, not the normal participant script.
9. Participant-facing UI no longer lists every remaining category title. It shows only progress and states that prior answers will be reused.
10. The runtime remains target-theory-blind: no chart, birth target, expected answer direction, score, or AstroHD mapping is exposed to the selector.

## Implementation

- `src/hdmatch/api/life_patterns_v2_owner_recoverability.py`
  - cross-thread aggregate context request;
  - dynamic target-blind next-question planner;
  - completed-dimension skip logic;
  - partial-dimension missing-information rule;
  - dynamic next-session endpoint;
  - health flags for dynamic selection and cross-thread reuse.
- `src/hdmatch/api/life_patterns_v2_owner_dynamic_ui.py`
  - `Continue interview` uses the dynamic endpoint;
  - sends aggregate coverage and settled result summaries;
  - removes first-missing-category sequencing;
  - hides the category list from the participant-facing progress summary.
- `tests/unit/test_life_patterns_v2_owner_dynamic_coverage.py`
  - verifies completed dimensions are skipped;
  - verifies accepted prior patterns are available to the selector;
  - verifies the prompt prohibits script/order behavior and redundant re-asking;
  - verifies the UI does not call `startCoverageDomain(missing[0])` and does not expose the open-category list.

## Scientific interpretation

This preserves a real checklist without requiring a literal questionnaire script:

**fixed constructs + fixed evidence/missingness semantics + dynamic information-gain questioning.**

"Cover every required question" is operationalized as "every required construct ends in a supported complete state or explicit missingness state." A participant answer can pre-satisfy later constructs, so the literal canonical sentence for that construct does not need to be asked again.

## Mission Control capture

The exact owner correction is durably captured (branch-only) in the universal architecture Mission Control feedback branch as:

`feedback/mission-control/SDF-20260915-LIFE-PATTERNS-DYNAMIC-COVERAGE-008.json`

The capture remains `CAPTURED_BRANCH_ONLY` until its draft Mission Control PR is accepted into the canonical branch.

## Next evidence boundary

Owner consumer-seam test: the interview should flow naturally from prior answers, should not reveal a registry-order category march, should not re-ask completed material, and should still eventually close or explicitly mark every required recoverability dimension before freeze/scoring.
