# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical.

## Read order

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
3. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-CANDIDATE-RECEIPT-2026-09-10.json`
4. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
5. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
6. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-SUMMARY-v1-2026-09-10.json`
7. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-PROMPT-v1-2026-09-10.txt`
8. `tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-WORKER-2026-09-10.md`
9. `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-SUMMARY-v1-2026-09-10.json`
10. `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-RAW-v1-2026-09-10.jsonl`
11. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
12. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v4-CANDIDATE-2026-09-10.json`
13. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
14. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
15. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
16. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
17. `state/CURRENT-STATE.md`

## Current controlling result

The fresh target-theory-blind v5 record-containment repair is committed at:

`320cb577f4adfbcc644c986f7f532feef0fbe80b`

CI `34526916770`: **SUCCESS**.

Exactly three repair files were added:

- `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-SUMMARY-v1-2026-09-10.json`

The disposition has exactly one row, `NR2-001`, marked `ADDRESSED`.

The summary reports:

- addressed = 1;
- not addressed = 0;
- `semantic_change_required=false`;
- substantive codebook not edited;
- prior candidate/review artifacts not edited;
- no target-model information used;
- `safe_for_blind_re_review=true`.

V5 claims to repair only record containment/referential integrity: assertion/component/absence/provenance records become normatively contained, typed ID references resolve exactly once, and retained component assertions bind uniquely to one event stage and that stage's evidence unit. Previously accepted semantics are supposed to remain unchanged.

## Preceding blind result

Independent v4 re-review:

`f5f02c976b11fbabc7c136f9c80fbd312600d91d`

CI `34524321911`: SUCCESS.

That review resolved all **45 original OA blockers plus NR-001**, with no partial/unresolved/regressed carried finding. It found only one new blocker, `NR2-001`, and reported `semantic_change_required=false`.

Thus the v5 review must test regression across all prior findings, not just NR2-001.

## Exact next gate — independent v5 review

Use a **different fresh target-theory-blind context from the author of `320cb577f4adfbcc644c986f7f532feef0fbe80b`**. Prefer a context also distinct from the earlier v4 reviewer.

Run:

`tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-WORKER-2026-09-10.md`

following:

`state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-PROMPT-v1-2026-09-10.txt`

exactly.

Bind the review to repair commit `320cb577f4adfbcc644c986f7f532feef0fbe80b`.

The reviewer must re-grade exactly the **47 carried findings**:

- all 45 original OA blockers;
- `NR-001`;
- `NR2-001`;

and may add only genuine new findings as `NR3-*`.

Mandatory review focus includes normative containment, exact-one referential integrity, unique assertion/component stage and evidence-unit binding, hybrid parent/component/absence ownership, provenance ownership, stage-local cardinality, same-act anti-double-counting, R05, and absence/missingness.

The review writes exactly:

- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-RAW-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-SUMMARY-v1-2026-09-10.json`

Implementation may begin only if:

- all 47 carried findings are RESOLVED;
- no PARTIAL, UNRESOLVED, or REGRESSED carried finding remains;
- no blocking `NR3-*` finding exists;
- response-contract/R05/absence semantics remain resolved;
- record containment is mechanically complete;
- `semantic_change_required=false`;
- `safe_for_implementation=true`.

## After a passing v5 re-review only

The exposed engineering context may mechanically implement the accepted versioned neutral measurement and relation contract, regenerate the private package/handoff/UI, and resume owner usability review.

Only after the revised UI is owner-accepted may the independent human first pass begin. Only after that pass is frozen may automated Life Patterns participant coding begin.

## Hard boundaries

- existing auditor kits remain ineligible for new human collection;
- no implementation before a passing v5 blind re-review;
- no theory-exposed substantive neutral-codebook repair;
- no automated participant coding before the revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated recruitment/contact, or spending without separate authorization.
