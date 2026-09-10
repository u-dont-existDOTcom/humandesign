# Current state

## Authoritative branch overlay — Life Patterns — 2026-09-10

This is the concise branch pointer for `codex/discover-life-patterns-mvp`, draft PR #24. Historical state remains preserved in Git history and dated artifacts. Do **not** infer a current next action from older sections or earlier UI/calibration artifacts.

Before substantive continuation:

1. fetch the live PR #24 head;
2. read `tasks/ACTIVE-TASK.json`;
3. read `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`;
4. read `tasks/NEXT-CONVERSATION-HANDOFF-2026-09-07.md`.

## Current gate

The independent target-theory-blind v4 contract review is frozen at:

`f5f02c976b11fbabc7c136f9c80fbd312600d91d`

CI `34524321911`: SUCCESS.

It re-reviewed all 45 original OA blockers plus `NR-001` and found:

- 46/46 carried findings RESOLVED;
- no PARTIAL, UNRESOLVED, or REGRESSED carried finding;
- R05 still resolved;
- absence/missingness still resolved;
- response-contract blockers resolved;
- `semantic_change_required=false`;
- one new material blocker: `NR2-001`;
- `safe_for_implementation=false`.

`NR2-001` is a record-model containment/referential-integrity defect: referenced value assertions, component assertions, absence conditions, and source provenance are not all normatively contained, and component assertions are not uniquely bound to one event stage and that stage's evidence unit.

The exact next action is a **fresh target-theory-blind contract-only repair** using:

- `tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-WORKER-2026-09-10.md`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-PROMPT-v1-2026-09-10.txt`

followed by a distinct fresh blind re-review using:

- `tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-WORKER-2026-09-10.md`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-PROMPT-v1-2026-09-10.txt`.

Implementation may begin only if that re-review resolves all 45 OA findings, `NR-001`, and `NR2-001`, finds no blocking `NR3-*`, reports no semantic regression, and sets `safe_for_implementation=true`.

## Human-calibration chronology remains unchanged

No qualifying independent human first pass has been collected. Existing auditor kits are superseded/ineligible for new collection until the accepted neutral measurement is mechanically implemented and the regenerated human UI passes owner usability review.

Only after the revised independent human first pass is frozen may automated Life Patterns participant coding begin. Target-model scoring/reveal remains later and separately unauthorized.

## Hard boundaries

- no theory-exposed substantive neutral-codebook repair;
- no engineering implementation before the passing v5 blind review;
- no automated participant coding before the revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated recruitment/contact, or spending without separate authorization.

## Preserved owner correction

The unrelated owner-test invariant remains binding: **“there was never a completion policy. that was invented nonsense by codex.”** Do not recreate a completion-policy premise or silently turn artifact counts into such a policy.
