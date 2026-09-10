# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
3. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-RECEIPT-2026-09-10.json`
4. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-SUMMARY-v1-2026-09-10.json`
5. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-RAW-v1-2026-09-10.jsonl`
6. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-PROMPT-v1-2026-09-10.txt`
7. `tasks/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-WORKER-2026-09-10.md`
8. `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-PROMPT-v1-2026-09-10.txt`
9. `tasks/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-WORKER-2026-09-10.md`
10. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
11. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v3-CANDIDATE-2026-09-10.json`
12. `state/LIFE-PATTERNS-OVERLAP-AUDIT-BLOCKER-RESOLUTION-v1-2026-09-10.jsonl`
13. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`
14. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
15. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
16. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
17. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
18. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
19. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
20. `state/CURRENT-STATE.md`
21. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The original blind overlap/absence audit, the first blind repair candidate, and the required second independent blind review are now all frozen. **The second review failed the implementation gate.** Do not implement v3.

No qualifying independent human first pass has been collected. No automated Life Patterns participant coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Frozen audit

Audit commit: `7ea0641e0913815306f8c182be5e7e8b18115fff`.

CI `34472686547`: SUCCESS.

- 22 observables;
- 134 material findings;
- 45 original blocking findings across 16 observables;
- `human_calibration_safe_to_start_without_revision=false`.

## First blind repair candidate

Candidate commit: `458bede3cf83b1947c332a408b47ec84236d69ed`.

- codebook clarification v2 candidate: SHA-256 `f179c04ff0940c701414abb10d48f8dafe574f3d1ff0727597802ffbf7bee8a0`, 29,122 bytes;
- facet/relation contract v3 candidate: SHA-256 `513716ddd39a89a10287f546d4fe647da9823079ebc01e4cb322fd7ec5ae98ee`, 26,037 bytes;
- blocker-resolution matrix: SHA-256 `4ec4b0d963932b5f1bff910e2464ef9754e7fee8dbbe5db601c681c124416309`, 25,324 bytes, 45 rows.

No implementation was performed and no target-model information was reported used. Candidate CI rerun completed successfully.

## Second independent blind review — authoritative result

Review commit: `4f51d075cb200e57820486e4f9686d81c7fc604f`.

CI `34509829399`: SUCCESS.

Review raw: worker-reported SHA-256 `0678acb8a4b24f0d8305cb8d5ed0dbf6022a07e74f6a94c674b406d2f1630b11`, 24,400 bytes.

Review summary: worker-reported SHA-256 `bfde3a4906d3aa1f2260e492c33794d50230f2769f4630db60935b68a5318aa4`, 693 bytes.

Counts:

- 45 OA rows;
- 38 RESOLVED;
- 7 PARTIAL;
- 0 UNRESOLVED;
- 1 new material finding (`NR-001`);
- R05 blockers resolved = true;
- absence/missingness semantics resolved = true;
- response-contract blockers resolved = false;
- `safe_for_implementation=false`.

Blocking IDs:

`OA-007, OA-011, OA-076, OA-084, OA-085, OA-114, OA-121, NR-001`.

The review commit adds only its two review artifacts; the candidate was not edited. The reviewer reported no target-model information used.

## Residual defect

This is now primarily a representation-contract problem, not a reopened substantive-codebook problem.

The v3 contract scopes facet cardinality at whole-response level. Some facets are `zero_or_one`, but the accepted semantic overlay permits distinct values in the same facet at different ordered events/stages/windows. That can make a valid multi-stage trajectory unrepresentable or allow an implementation to discard an earlier stage.

Named partial blockers:

- OA-007 / R02 search disposition;
- OA-011 / R03 temporal disposition;
- OA-076 and OA-084 / R15 endpoint extent/timing;
- OA-085 / R16 offer response/use;
- OA-114 / R20 interaction disposition;
- OA-121 / R21 contact disposition.

`NR-001` generalizes the defect and requires checking the entire contract, including similarly staged R10/R12 trajectories.

Do not reopen R05 or absence/missingness semantics merely because this contract issue remains; those passed the independent review.

## Exact next gate — fresh blind contract-only repair

Run:

`tasks/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-WORKER-2026-09-10.md`

in a NEW target-theory-blind context, following:

`state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-PROMPT-v1-2026-09-10.txt`.

It must create exactly:

1. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v4-CANDIDATE-2026-09-10.json`
2. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
3. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-SUMMARY-v1-2026-09-10.json`

The disposition must contain exactly the eight carried blocking IDs once each. Existing candidate and review files are immutable. The repair must remain contract-only; if a substantive codebook semantic change is required, the worker must report that and stop rather than making it.

## Mandatory independent re-review

After the v4 repair commit exists, use a distinct fresh target-theory-blind reviewer with:

- `tasks/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-WORKER-2026-09-10.md`
- `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-PROMPT-v1-2026-09-10.txt`.

The reviewer must re-grade **all 45 original OA blockers plus carried NR-001**, not merely the seven partial OA rows, so regressions in previously resolved semantics are detectable. It may add only genuine new findings as `NR2-*`.

Implementation is allowed only if the new summary sets `safe_for_implementation=true`, requiring all 46 carried findings resolved, no blocking NR2 finding, no semantic regression, all five original response-contract blockers resolved, R05 still resolved, absence/missingness still resolved, and `semantic_change_required=false`.

## Only after blind re-review passes

The exposed engineering context may mechanically implement the accepted versioned neutral measurement and relation contract, regenerate the private package/handoff/UI, and resume owner usability review.

Only after the revised UI is owner-accepted may the independent human first pass begin. Only after that first pass is frozen may automated Life Patterns participant coding begin.

## Existing corrections remain controlling

- generalized behavioral recurrence self-report is direct reported-recurrence evidence;
- self-selected confirming anecdotes are not independent frequency evidence;
- specificity is not evidential independence;
- machine schema is not the human interface;
- one-source provenance is automatic;
- temporal ordering is asked only where meaningful;
- affirmative behavior is not non-action merely because a separate clause depends on absence;
- absence gates name the exact absent proposition;
- `not reported`, `unknown`, and silence are not behavioral nonoccurrence.

## Hard boundaries

- all existing auditor kits remain ineligible for human collection;
- do not implement v3 or any v4 repair before a passing independent blind re-review;
- do not make theory-exposed substantive neutral-codebook repairs;
- no automated participant coding before the eventual revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
