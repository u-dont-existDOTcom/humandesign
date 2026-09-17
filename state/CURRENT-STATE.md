# Current state — Life Patterns — 2026-09-17

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest`.

The owner approved **all four phases** of the survey review. Approval source: `tasks/LIFE-PATTERNS-SURVEY-APPROVED-IMPLEMENTATION-2026-09-17.md`. The review's earlier waiting-for-approval state is superseded.

## Current boundary

Coordinated implementation candidate verified locally; hosted CI and the existing prototype deployment must be reconciled before a live-completion claim. The development pull request remains draft/open/unmerged. No merge, public release, recruitment, model/provider change, or paid evaluation campaign is authorized.

Implementation receipt: `state/LIFE-PATTERNS-SURVEY-IMPLEMENTATION-2026-09-17.md`.
Browser evidence: `artifacts/life-patterns/survey-implementation-2026-09-17/browser-regressions.json`.

## Product implementation

One explicit revision-bound workflow controls current phase, single-flight/idempotent operations, preserved pending submissions, atomic server snapshot/view responses, restore reconciliation and pause/resume. The deployed UI is one template and one renderer, not another layer over the old HTML patch chain. Old open tabs keep the raw recovery-read contract and receive an explicit refresh boundary for old mutation routes.

All current question routes share source-bound conversation, operative evidence, pattern status and corrections. The final gate runs after runtime fallback/refinement, and cross-area admission can stop with incomplete coverage explicitly retained. A fallible formulation-fidelity review checks source context and the distinction between direct reports, plausible new inferences and unsupported/context-only material. These controls do not prove that all real model questions or syntheses are good.

The interface has one labeled response box, compact approximate coverage progress, no fabricated ETA, persistent Finish for now, explicit Resume, a stable patterns collection, source-context disclosure, append-only participant correction notes, visible retry/save status, separate summary/backup/research exports, reduced-motion handling and responsive layout. Corrections dispute the old interpretation; they do not manufacture another adjudication of an already accepted historical proposal.

## Preserved scientific boundary

The accepted v2 hidden evidence contract is unchanged: open-world episode facts, participant authority, append-only evidence corrections/provenance, genuine-absence gating, immutable evidence timing, and the episode-fact/person-pattern firewall. No private narrative was committed. The runtime receives no birth target, chart, expected direction, target mapping, candidate score or rank. The 23-dimension neutral blueprint remains `life-patterns-recoverability-coverage-v2`.

Direct participant statements may be recorded without redundant confirmation; added interviewer inferences need participant judgment. Familiar or conditional self-knowledge is not rejected merely for being obvious or dependent on context. No arbitrary episode/counterexample quota was added.

Working recovery is not scientific acceptance. Older transcript reconstruction remains explicitly non-scientific. The frozen development record now includes the evidence archive, blueprint/build identity, current statuses and unresolved corrections; hashing bytes does not validate their semantics. Historical accepted assertions remain in the archive, but disputed current items are unresolved in the current-result projection.

The owner-self historical recovery criterion remains a later post-freeze regression: exact recorded moment hourly rank no worse than #2; correct date #1 distinct refined neighborhood; refined peak within 11 minutes. This implementation does not claim that criterion is met on a new interview.

## Verification and remaining work

Local complete suite: 815 passed, 7 environment/shallow-history skips, one Starlette/httpx deprecation warning. Ruff production/tests passed with the repository's existing E501/I001 exclusions. Strict mypy passed across 207 source files. Thirteen executable local browser cases passed with zero page errors and zero live model calls. Initial/confirmation layout checks covered 320, 375, 414, 768, 1024 and 1440 CSS pixels. Native mobile keyboards, complete zoom/contrast/screen-reader conformance and live model latency/quality were not certified.

The new hosted `survey-browser` job executes these consumer tests against a loopback-only synthetic fixture, in addition to the existing Python/lint/typecheck job. Current deployment configuration and passwordless owner-prototype authority are unchanged; do not create another service or restore Basic Auth without an owner decision.

Next: verify the exact hosted runs and deployment, update this receipt with their identities, then a short owner retest of usefulness and correction burden. Do not ask for the already-given implementation approval again.

Historical overlay: `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-12.md` is retained as history where newer state supersedes it. Existing Mission Control captures remain on their separate correction branch; this task did not modify them.

Legacy affected completion command (retained for task preflight):

`python -m pytest tests/unit/test_life_patterns_v2_owner_continuous_flow.py tests/unit/test_life_patterns_v2_owner_natural_flow.py tests/unit/test_life_patterns_v2_owner_liveness.py tests/unit/test_life_patterns_v2_owner_import_resume.py tests/unit/test_life_patterns_v2_owner_persistent.py tests/unit/test_life_patterns_v2_owner_resilient.py tests/unit/test_life_patterns_v2_owner_finalization_flow.py tests/unit/test_life_patterns_v2_owner_dynamic_coverage.py tests/unit/test_life_patterns_v2_owner_scope.py tests/unit/test_life_patterns_v2_owner_recoverability.py tests/unit/test_life_patterns_v2_owner_recoverability_ui.py tests/unit/test_life_patterns_owner_recovery_gate.py -q`

Additional focused tests: `tests/unit/test_life_patterns_v2_owner_workflow.py`, `tests/unit/test_life_patterns_v2_owner_workflow_api.py`. Browser setup/command: `tests/browser/README.md`.

Owner correction preserved: **There was never a completion policy.** See `state/OWNER-CORRECTION-2026-09-02.md`. Do not invent a scientific-completeness blocker from task bookkeeping.
