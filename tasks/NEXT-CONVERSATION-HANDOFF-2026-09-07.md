# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical.

## Read order

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
3. `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-RECEIPT-2026-09-10.json`
4. `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-SUMMARY-v1-2026-09-10.json`
5. `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-RAW-v1-2026-09-10.jsonl`
6. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-PROMPT-v1-2026-09-10.txt`
7. `tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-WORKER-2026-09-10.md`
8. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-PROMPT-v1-2026-09-10.txt`
9. `tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-WORKER-2026-09-10.md`
10. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v4-CANDIDATE-2026-09-10.json`
11. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
12. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
13. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
14. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
15. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
16. `state/CURRENT-STATE.md`

## Current controlling result

Independent v4 re-review commit:

`f5f02c976b11fbabc7c136f9c80fbd312600d91d`

CI `34524321911`: **SUCCESS**.

Review artifacts:

- raw: SHA-256 `3a268d95132451a69a36e7dcbb965c9f6ac3b1d3f3742173570c98b61a5ff1f2`, 30,180 bytes;
- summary: SHA-256 `76e2c372b5d0485a8ee762123a9e2c69858134300be1aeb829b0075e0721e1b4`, 1,121 bytes.

Review counts/results:

- 45 original OA blockers reviewed and **all RESOLVED**;
- `NR-001` reviewed and **RESOLVED**;
- PARTIAL = 0;
- UNRESOLVED = 0;
- REGRESSED = 0;
- response-contract blockers resolved = true;
- R05 blockers resolved = true;
- absence/missingness semantics resolved = true;
- `semantic_change_required=false`;
- one new material blocker: `NR2-001`;
- `safe_for_implementation=false`.

## NR2-001

The remaining defect is representation integrity, not substantive codebook semantics.

V4 references `value_assertion`, `component_assertion`, `absence_condition`, and `source_provenance` records, but `observable_response` does not normatively contain/store all of them. `component_assertion` also lacks a mechanically unique binding to one `event_stage` and that stage's `evidence_unit`.

A conforming implementation could therefore allow dangling or duplicate/ambiguous references, omit a required record, or attach one hybrid component to multiple stages/evidence units. This could corrupt stage-preserving evidence identity.

The reviewer explicitly says no substantive semantic change is required.

## Exact next gate — fresh blind contract-only repair

Run:

`tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-WORKER-2026-09-10.md`

in a **new target-theory-blind context distinct from the reviewer at `f5f02c976b11fbabc7c136f9c80fbd312600d91d`**, following:

`state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-PROMPT-v1-2026-09-10.txt`.

It must create exactly:

1. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
2. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
3. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-SUMMARY-v1-2026-09-10.json`

Required repair behavior:

- normative containment for every referenced assertion/component/absence/provenance record;
- exact-one referential integrity for IDs;
- every value assertion and retained component assertion uniquely attached to one event stage and that stage's evidence unit;
- hybrid components remain non-independent for occurrence counting;
- provenance remains assertion-specific;
- stage-local cardinality stays intact;
- R05 and absence/missingness stay unchanged;
- no substantive neutral-codebook edit.

If the worker decides substantive semantic change is required, it must stop and report that rather than make the change.

## Mandatory re-review after v5

After v5 is committed, run a **different fresh target-theory-blind reviewer** using:

- `tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-WORKER-2026-09-10.md`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-PROMPT-v1-2026-09-10.txt`.

The reviewer must re-grade all **47 carried findings**:

- all 45 original OA blockers;
- `NR-001`;
- `NR2-001`;

and may add only genuine new findings as `NR3-*`.

Implementation may begin only if all 47 carried findings are RESOLVED, no blocking `NR3-*` exists, no regression is found, `semantic_change_required=false`, and `safe_for_implementation=true`.

## After a passing v5 re-review only

The exposed engineering context may mechanically implement the accepted neutral measurement/contract, regenerate the private package/handoff/UI, and resume owner usability review.

Only after the revised UI is owner-accepted may the independent human first pass begin. Only after that pass is frozen may automated Life Patterns participant coding begin.

## Hard boundaries

- existing auditor kits remain ineligible for new human collection;
- no implementation before a passing v5 blind re-review;
- no theory-exposed substantive neutral-codebook repair;
- no automated participant coding before the revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated recruitment/contact, or spending without separate authorization.
