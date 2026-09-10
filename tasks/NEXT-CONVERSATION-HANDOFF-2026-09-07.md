# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical.

## Read order

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
3. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-CANDIDATE-RECEIPT-2026-09-10.json`
4. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v4-CANDIDATE-2026-09-10.json`
5. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
6. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-SUMMARY-v1-2026-09-10.json`
7. `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-PROMPT-v1-2026-09-10.txt`
8. `tasks/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-WORKER-2026-09-10.md`
9. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-SUMMARY-v1-2026-09-10.json`
10. `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-RAW-v1-2026-09-10.jsonl`
11. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
12. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v3-CANDIDATE-2026-09-10.json`
13. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`
14. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
15. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
16. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
17. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
18. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
19. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
20. `state/CURRENT-STATE.md`
21. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The original blind audit, first blind semantic repair, independent review, and narrow v4 facet-cardinality repair are all frozen. **The v4 repair has not yet passed its independent blind re-review. Do not implement it yet.**

No qualifying independent human first pass has been collected. No automated Life Patterns participant coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Frozen audit

Audit commit: `7ea0641e0913815306f8c182be5e7e8b18115fff`; CI `34472686547`: SUCCESS.

- 22 observables;
- 134 material findings;
- 45 original blockers across 16 observables;
- human calibration unsafe without revision.

## First repair and independent review

First repair candidate: `458bede3cf83b1947c332a408b47ec84236d69ed`.

Second independent blind review: `4f51d075cb200e57820486e4f9686d81c7fc604f`; CI `34509829399`: SUCCESS.

That review found:

- 38/45 original blockers RESOLVED;
- 7 PARTIAL;
- 0 UNRESOLVED;
- one new material blocker `NR-001`;
- R05 blockers resolved = true;
- absence/missingness semantics resolved = true;
- response-contract blockers resolved = false;
- `safe_for_implementation=false`.

Carried blockers:

`OA-007, OA-011, OA-076, OA-084, OA-085, OA-114, OA-121, NR-001`.

Their common defect was response-wide facet cardinality where valid same-facet states may occur at different ordered stages/windows.

## V4 contract-only repair candidate

Fresh blind repair commit:

`7ba5654fe99017e1c84a4b8868e5a3da50c55be6`

CI `34517777654`: **SUCCESS**.

Artifacts:

- v4 contract: SHA-256 `84159a22c38be9efa2673aca2f5aaa4dc127630ca6fa67151f9c92ec80f4f6a3`, 40,339 bytes;
- 8-row disposition: SHA-256 `008073f71b3a014c6af97c2d0695a648fe3eec9f6dd480fb653ec7ae04b29a8d`, 4,922 bytes;
- summary: SHA-256 `30be764c938336d5ac27e0cf15f0ff3388eb6611f5d9437ac01e229cb9e85ad8`, 832 bytes.

Worker reported:

- 8/8 carried blockers addressed;
- `semantic_change_required=false`;
- no substantive codebook edit;
- no modification to previous candidate/review artifacts;
- no target-model information used;
- `safe_for_blind_re_review=true`.

The v4 contract's central claim is stage-local facet cardinality: same-stage cardinality/exclusivity remains enforceable, while distinct ordered stages may retain different same-facet values when the accepted semantics permit a trajectory. This is not yet independently accepted.

## Exact next gate — fresh independent v4 re-review

Use a **different fresh target-theory-blind context** from the worker that authored `7ba5654fe99017e1c84a4b8868e5a3da50c55be6`.

Run:

`tasks/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-WORKER-2026-09-10.md`

following:

`state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-PROMPT-v1-2026-09-10.txt`.

Bind exactly:

- frozen audit `7ea0641e0913815306f8c182be5e7e8b18115fff`;
- v2 codebook clarification / first repair `458bede3cf83b1947c332a408b47ec84236d69ed`;
- prior blind review `4f51d075cb200e57820486e4f9686d81c7fc604f`;
- v4 contract repair `7ba5654fe99017e1c84a4b8868e5a3da50c55be6`.

The reviewer must re-grade **all 45 original OA blockers plus NR-001**, not only the eight carried blockers. It may add genuine new defects only as `NR2-*`.

Mandatory checks:

- cardinality is stage-local, not observable-wide;
- same-facet values can occupy distinct ordered stages where semantics allow;
- deduplication cannot erase legitimate stage transitions;
- provenance/evidence-unit identity remains stage-preserving;
- R02/R03/R15/R16/R20/R21 trajectories work;
- analogous R10/R12 changes are not silently lost;
- same-act double counting remains prevented;
- R05 remains resolved;
- absence/missingness remains resolved.

The review must write exactly the two artifacts specified by its worker wrapper and set `safe_for_implementation=true` only if all 45 OA findings plus NR-001 are resolved and no blocking NR2 finding remains.

## After a passing blind re-review only

Then the exposed engineering context may mechanically implement the accepted versioned codebook/contract, regenerate the private package/handoff/UI, and resume owner usability review.

Only after the revised UI is owner-accepted may the independent human first pass begin. Only after that first pass is frozen may automated Life Patterns participant coding begin.

## Hard boundaries

- existing auditor kits are ineligible for new human collection;
- no implementation before a passing v4 blind re-review;
- no theory-exposed substantive neutral-codebook repair;
- no automated participant coding before the revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated recruitment/contact, or spending without separate authorization.
