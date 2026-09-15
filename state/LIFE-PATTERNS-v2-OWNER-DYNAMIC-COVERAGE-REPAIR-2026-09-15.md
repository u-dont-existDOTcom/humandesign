# Life Patterns v2 — dynamic cross-thread coverage repair — 2026-09-15

## Owner requirement

The owner clarified that scientific standardization must not turn the participant experience into a rigid category-by-category questionnaire. All required measurement dimensions still need to be covered, but the interview should reuse what the participant has already said, credit it across every dimension it genuinely informs, and avoid asking the same thing again later under a different category heading.

## Failure risk

The prior standardized coverage implementation had two distinct layers:

- participant-led natural pattern interviews whose evidence could already satisfy multiple required dimensions;
- a later `Continue required coverage` path that selected the **first incomplete dimension in registry order** and opened its canonical screener.

A second continuity gap existed between participant-led pattern threads: starting another pattern created a fresh server session without settled prior-thread context. The new thread could therefore ask for material already established elsewhere even though aggregate coverage knew the dimension was partly or fully covered.

The measurement contract was standardized, but those two seams could make the participant experience regress toward a category questionnaire and create duplicate questions.

## Repair

The scientific contract remains the same fixed `life-patterns-recoverability-coverage-v2` set of 23 required dimensions. The change is to question selection and continuity, not the measurement target.

New behavior:

1. Every completed thread is assessed against **all** required dimensions, so one answer can satisfy several dimensions when its cited evidence genuinely supports them.
2. The client maintains aggregate coverage across threads.
3. `Continue interview` sends aggregate coverage plus settled participant-adjudicated pattern summaries to a target-blind next-question selector.
4. Dimensions already `sufficient`, `unknown`, `inapplicable`, or `declined` are closed and cannot be re-asked merely because a canonical screener exists.
5. A `partial` dimension receives only a question about the missing discriminator, not a restart of the whole category.
6. Among still-open dimensions, the selector chooses the next question by expected information gain and conversational continuity rather than registry order.
7. One question may illuminate several still-open dimensions; the internal `primary_domain_id` is routing metadata only.
8. Canonical screeners remain a fallback/debug seam, not the normal participant script.
9. Participant-facing UI no longer lists every remaining category title. It shows only progress and states that prior answers will be reused.
10. `Explore another pattern` now creates a contextual participant-led thread carrying settled prior information for planning, so later threads can avoid asking the same thing again.
11. Cross-thread context is **planning-only**: accepted pattern wording can guide continuity, but rejected/unresolved wording is not treated as settled; coverage reasons are model-generated metadata; the context note is not a participant utterance, cannot create hidden facts, and is never quoted to the participant.
12. New evidence in a new thread must still come from the participant's current messages and the operative hidden ledger.
13. The runtime remains target-theory-blind: no chart, birth target, expected answer direction, score, or AstroHD mapping is exposed to the selector.

## Implementation

- `src/hdmatch/api/life_patterns_v2_owner_recoverability.py`
  - aggregate context request;
  - dynamic target-blind next-question planner;
  - completed-dimension skip logic;
  - partial-dimension missing-information rule;
  - dynamic next-session endpoint;
  - contextual participant-led session endpoint;
  - planning-only cross-thread context that excludes rejected wording as settled context;
  - health flags for dynamic selection and cross-thread reuse.
- `src/hdmatch/api/life_patterns_v2_owner_dynamic_ui.py`
  - `Continue interview` uses the dynamic endpoint;
  - `Explore another pattern` uses the contextual session endpoint;
  - sends aggregate coverage and settled result summaries;
  - removes first-missing-category sequencing;
  - hides the category list from the participant-facing progress summary.
- `src/hdmatch/api/life_patterns_v2_owner_scope.py`
  - explicit evidence firewall for internal cross-thread planning context;
  - preserves the global-label scope guard.
- `tests/unit/test_life_patterns_v2_owner_dynamic_coverage.py`
  - verifies completed dimensions are skipped;
  - verifies accepted prior patterns are available to the selector;
  - verifies rejected wording is not treated as settled context;
  - verifies planning-only context cannot stand in for participant evidence;
  - verifies the prompt prohibits script/order behavior and redundant re-asking;
  - verifies the UI does not call `startCoverageDomain(missing[0])` and does not expose the open-category list.
- `tests/unit/test_life_patterns_v2_owner_scope.py`
  - verifies cross-thread planning context is distinguished from participant evidence.

## Scientific interpretation

This preserves a real checklist without requiring a literal questionnaire script:

**fixed constructs + fixed evidence/missingness semantics + dynamic information-gain questioning.**

"Cover every required question" is operationalized as "every required construct ends in a supported complete state or explicit missingness state." A participant answer can pre-satisfy later constructs, so the literal canonical sentence for that construct does not need to be asked again.

The science is fixed at the **measurement layer**, not at the sentence/order layer.

## Verification / live deployment

Application head: `f660eee7efe5830f2701ea0b433361ddc6cc1e69`.

Regression-test head: `e4a2064a5c6dc1f984f4c70427ce2c72839d63f4`.

GitHub Actions run `35023996133`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `9dbd21d2-fe30-407d-90b6-917a7c77dd5a`: **SUCCESS** from exact application head `f660eee7efe5830f2701ea0b433361ddc6cc1e69`.

Runtime evidence:

- application startup completed;
- `GET /healthz` returned HTTP **200**.

## Mission Control capture

The exact owner correction is durably captured (branch-only) in the universal architecture Mission Control feedback branch as:

`feedback/mission-control/SDF-20260915-LIFE-PATTERNS-DYNAMIC-COVERAGE-008.json`

The capture remains `CAPTURED_BRANCH_ONLY` until its draft Mission Control PR is accepted into the canonical branch.

## Next evidence boundary

Owner consumer-seam test: the interview should flow naturally from prior answers, should not reveal a registry-order category march, should not re-ask completed material, should use only the missing part of partially covered constructs, and should still eventually close or explicitly mark every required recoverability dimension before freeze/scoring.
