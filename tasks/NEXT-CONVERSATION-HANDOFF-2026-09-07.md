# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
3. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`
4. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
5. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-EXPOSED-REVIEW-2026-09-10.md`
6. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-PROMPT-v1-2026-09-10.txt`
7. `tasks/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-WORKER-2026-09-10.md`
8. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-PROMPT-v1-2026-09-10.txt`
9. `tasks/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-WORKER-2026-09-10.md`
10. `state/LIFE-PATTERNS-R05-FACET-OVERLAP-AND-ABSENCE-SEMANTICS-DEFECT-2026-09-10.md`
11. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
12. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
13. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
14. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
15. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
16. `state/CURRENT-STATE.md`
17. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The overlap/absence audit is **complete and authoritative**. The earlier malformed run remains rejected wholesale and is historical only.

Authoritative audit commit:

`7ea0641e0913815306f8c182be5e7e8b18115fff`

CI `34472686547`: SUCCESS.

Frozen audit identities:

- raw JSONL: SHA-256 `37642f31135f3d446488a3a0a6736468b30b6114d5a292bcaf01096d65fb16e6`, 83,030 bytes, 134 findings;
- summary JSON: SHA-256 `7184f89a9d6c8fa0560e0ceba07287f101f559ddcf872b3db62e39de34cb7b47`, 1,170 bytes.

The summary reports:

- 22 observables reviewed;
- 48 presentation-only findings;
- 5 response-contract limitations;
- 40 substantive-codebook-overlap findings;
- 41 no-change-needed findings;
- 45 blocking findings;
- `human_calibration_safe_to_start_without_revision=false`;
- R05 requires `versioned_codebook_clarification`.

The 45 blockers affect 16 observables:

`R02, R03, R05, R06, R07, R10, R11, R12, R13, R14, R15, R16, R18, R19, R20, R21`.

## Scientific conclusion from exposed review

This is **not** another UI-only problem. Do not build or distribute another auditor kit against the current measurement.

The audit confirms three distinct repair classes:

1. presentation/facet grouping issues;
2. response-contract insufficiency;
3. substantive neutral-codebook overlap/boundary/absence problems.

Exactly five original findings require response-contract change:

- OA-029 / R05;
- OA-034 / R07;
- OA-085 / R16;
- OA-114 / R20;
- OA-121 / R21.

The existing one-global-relation representation cannot encode co-present facet attributes plus meaningful within-episode sequence without false ordering or information loss.

Substantive blockers additionally include nested/general-specific values, composite values duplicating components, hybrid affirmative-plus-absence semantics, missingness accidentally treated as nonoccurrence, underbounded absence targets, and same-act double-count risk.

## Exact next gate — fresh blind repair proposal

Run:

`tasks/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-WORKER-2026-09-10.md`

in a **NEW target-theory-blind context**.

It follows:

`state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-PROMPT-v1-2026-09-10.txt`

and creates exactly:

1. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
2. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v3-CANDIDATE-2026-09-10.json`
3. `state/LIFE-PATTERNS-OVERLAP-AUDIT-BLOCKER-RESOLUTION-v1-2026-09-10.jsonl`

The blocker matrix must contain all and only the 45 blocking OA IDs exactly once. The worker may clarify, split, retire redundant composites, assign facets, or define specificity/precedence rules only as needed to resolve the blind audit. Historical artifacts remain immutable. It must not implement software/UI/package changes or run any participant coding.

## Mandatory second blind review

After the repair proposal is committed, use a **different fresh target-theory-blind context** with:

- `tasks/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-WORKER-2026-09-10.md`
- `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-PROMPT-v1-2026-09-10.txt`

The reviewer must independently grade every one of the 45 original blockers and scan for new material defects. Engineering implementation remains blocked unless:

- all 45 blockers are RESOLVED;
- no new material blocker remains;
- all five response-contract limitations are resolved;
- all R05 blockers are resolved;
- absence/missingness semantics are adequately bounded;
- summary sets `safe_for_implementation=true`.

## Only after blind review passes

The exposed engineering context may mechanically implement the accepted versioned neutral measurement and response contract, regenerate the private package/handoff/UI, and resume owner usability review.

Only after the revised UI is owner-accepted may the independent human first pass begin. Only after that first pass is frozen may automated Life Patterns participant coding begin.

## Existing corrections remain controlling

- generalized behavioral recurrence self-report is direct reported-recurrence evidence;
- self-selected confirming anecdotes are not independent frequency evidence;
- concrete incidents are requested only for information gain;
- specificity is not evidential independence;
- machine schema is not the human interface;
- ask substantive human questions directly;
- hide machine IDs and optional research busywork;
- one-source provenance is automatic;
- multi-value order is asked only when order matters;
- affirmative behavior is not non-action merely because a separate absence condition exists;
- absence gates must name the exact absent proposition;
- `not reported` / `unknown` is not behavioral nonoccurrence.

## Hard boundaries

- all existing auditor kits remain ineligible for new human collection;
- do not make theory-exposed substantive neutral-codebook repairs;
- do not implement the repair before the second blind review passes;
- no automated participant coding before the eventual revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
