# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
3. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-CANDIDATE-RECEIPT-2026-09-10.json`
4. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
5. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v3-CANDIDATE-2026-09-10.json`
6. `state/LIFE-PATTERNS-OVERLAP-AUDIT-BLOCKER-RESOLUTION-v1-2026-09-10.jsonl`
7. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-PROMPT-v1-2026-09-10.txt`
8. `tasks/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-WORKER-2026-09-10.md`
9. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`
10. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
11. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-EXPOSED-REVIEW-2026-09-10.md`
12. `state/LIFE-PATTERNS-R05-FACET-OVERLAP-AND-ABSENCE-SEMANTICS-DEFECT-2026-09-10.md`
13. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
14. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
15. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
16. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
17. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
18. `state/CURRENT-STATE.md`
19. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The valid overlap/absence audit and first blind repair proposal are both frozen. **The exact next gate is a second independent target-theory-blind review of the repair proposal.** Do not implement it yet.

No qualifying independent human first pass has been collected. No automated Life Patterns participant coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Frozen audit

Authoritative audit commit:

`7ea0641e0913815306f8c182be5e7e8b18115fff`

CI `34472686547`: SUCCESS.

- raw audit SHA-256 `37642f31135f3d446488a3a0a6736468b30b6114d5a292bcaf01096d65fb16e6`, 83,030 bytes, 134 findings;
- summary SHA-256 `7184f89a9d6c8fa0560e0ceba07287f101f559ddcf872b3db62e39de34cb7b47`, 1,170 bytes;
- 22 observables reviewed;
- 45 blocking findings across 16 observables;
- 5 response-contract limitations;
- `human_calibration_safe_to_start_without_revision=false`.

## Frozen repair candidate

Candidate commit:

`458bede3cf83b1947c332a408b47ec84236d69ed`

Candidate artifacts:

- codebook clarification v2 candidate: SHA-256 `f179c04ff0940c701414abb10d48f8dafe574f3d1ff0727597802ffbf7bee8a0`, 29,122 bytes;
- facet/relation contract v3 candidate: SHA-256 `513716ddd39a89a10287f546d4fe647da9823079ebc01e4cb322fd7ec5ae98ee`, 26,037 bytes;
- blocker-resolution matrix: SHA-256 `4ec4b0d963932b5f1bff910e2464ef9754e7fee8dbbe5db601c681c124416309`, 25,324 bytes, 45 rows.

Worker reported all 45 original blocking OA IDs exactly once, no software/UI/package implementation, and no target-model information used.

CI run `34506025354` initially hit an unrelated Node subprocess timeout in `test_natal_pilot_app` after 648 passed / 7 skipped. The failed job was rerun; verify job `102970354108` completed SUCCESS, including unit/integration tests, Ruff, and mypy. This is engineering baseline only, not semantic approval.

## Exact next gate — SECOND independent blind review

Use a **different fresh target-theory-blind context** that did not author candidate commit `458bede3cf83b1947c332a408b47ec84236d69ed`.

Run:

`tasks/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-WORKER-2026-09-10.md`

following:

`state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-PROMPT-v1-2026-09-10.txt`

The reviewer must independently evaluate each of the 45 original OA blockers; the candidate's blocker matrix is a claim to test, not an answer key. It must also scan the candidate for genuinely new material defects (`NR-*`).

Special checks:

- response-contract blockers: OA-029, OA-034, OA-085, OA-114, OA-121;
- all R05 blockers: OA-017, OA-019, OA-020, OA-021, OA-022, OA-026, OA-027, OA-029;
- missingness/absence semantics: nonmention/unknown/silence never become absence; every absence-dependent code names its exact absent proposition; the four-part gate applies to that proposition only; the affirmative half of a hybrid code is not mislabeled as non-action.

The review writes exactly:

1. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-RAW-v1-2026-09-10.jsonl`
2. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-SUMMARY-v1-2026-09-10.json`

It must contain exactly 45 `OA-*` review rows plus only genuine `NR-*` findings.

### Implementation criterion

Implementation is allowed only if the second blind summary sets `safe_for_implementation=true`, which requires:

- all 45 original blockers = RESOLVED;
- no blocking NR finding;
- all five response-contract blockers resolved;
- all R05 blockers resolved;
- absence semantics adequately bounded.

If any original/new blocker remains, route only those unresolved/new issues into another fresh theory-blind repair cycle. Do not patch around them in the exposed project context.

## Only after blind review passes

Mechanically implement the accepted versioned neutral measurement and facet/event relation contract; regenerate the private package/handoff/UI; then resume owner usability review.

Only after the revised UI is owner-accepted may the independent human first pass begin. Only after that first pass is frozen may automated Life Patterns participant coding begin.

## Existing owner corrections remain controlling

- generalized behavioral recurrence self-report is direct reported-recurrence evidence;
- self-selected confirming anecdotes are not independent frequency evidence;
- concrete incidents are requested only for information gain;
- specificity is not evidential independence;
- machine schema is not the human interface;
- ask substantive human questions directly;
- hide machine IDs and optional research busywork;
- one-source provenance is automatic;
- multi-value order is asked only where temporal order actually matters;
- affirmative behavior is not non-action merely because a separate clause depends on absence;
- absence gates name the exact absent proposition;
- `not reported`, `unknown`, and silence are not behavioral nonoccurrence.

## Hard boundaries

- all existing auditor kits remain ineligible for human collection;
- do not implement the candidate before the second blind review passes;
- do not make theory-exposed substantive neutral-codebook repairs;
- no automated participant coding before the eventual revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
