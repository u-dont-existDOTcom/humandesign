# Life Patterns current state — 2026-09-10

Status: public-safe controlling overlay for the active Life Patterns development-transfer task. Historical artifacts remain immutable.

## Current scientific gate

**Human calibration and engineering implementation remain paused.** The contract-only v4 facet-cardinality repair exists and is CI-green, but it is only a candidate. The exact next gate is an independent target-theory-blind re-review of the entire carried blocker set before implementation.

No qualifying independent human first-pass annotations have been collected. No automated Life Patterns participant coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Frozen audit and first repair

Authoritative overlap/absence audit commit: `7ea0641e0913815306f8c182be5e7e8b18115fff`; CI `34472686547`: SUCCESS.

The audit reviewed 22 observables and produced 134 material findings, including 45 blockers. It set `human_calibration_safe_to_start_without_revision=false`.

First blind repair candidate: `458bede3cf83b1947c332a408b47ec84236d69ed`.

- codebook clarification v2 candidate: SHA-256 `f179c04ff0940c701414abb10d48f8dafe574f3d1ff0727597802ffbf7bee8a0`, 29,122 bytes;
- facet/relation contract v3 candidate: SHA-256 `513716ddd39a89a10287f546d4fe647da9823079ebc01e4cb322fd7ec5ae98ee`, 26,037 bytes;
- blocker-resolution matrix: SHA-256 `4ec4b0d963932b5f1bff910e2464ef9754e7fee8dbbe5db601c681c124416309`, 45 rows.

## Independent review of v3

Review commit: `4f51d075cb200e57820486e4f9686d81c7fc604f`; CI `34509829399`: SUCCESS.

Result:

- 45 original OA blockers reviewed;
- 38 RESOLVED;
- 7 PARTIAL;
- 0 UNRESOLVED;
- one new material blocker, `NR-001`;
- R05 blockers resolved = true;
- absence/missingness semantics resolved = true;
- response-contract blockers resolved = false;
- `safe_for_implementation=false`.

Carried blockers:

`OA-007, OA-011, OA-076, OA-084, OA-085, OA-114, OA-121, NR-001`.

The common residual defect was response-wide facet cardinality: values such as `zero_or_one` could suppress legitimate ordered same-facet changes at distinct events/stages/windows. This did **not** reopen the already accepted substantive R05 or absence/missingness semantics.

## V4 facet-cardinality repair candidate — completed, awaiting blind re-review

Fresh target-theory-blind repair commit:

`7ba5654fe99017e1c84a4b8868e5a3da50c55be6`

GitHub Actions CI `34517777654`: **SUCCESS**.

Artifacts:

1. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v4-CANDIDATE-2026-09-10.json`
   - SHA-256 `84159a22c38be9efa2673aca2f5aaa4dc127630ca6fa67151f9c92ec80f4f6a3`
   - 40,339 bytes
2. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
   - SHA-256 `008073f71b3a014c6af97c2d0695a648fe3eec9f6dd480fb653ec7ae04b29a8d`
   - 4,922 bytes
   - exactly 8 rows
3. `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-SUMMARY-v1-2026-09-10.json`
   - SHA-256 `30be764c938336d5ac27e0cf15f0ff3388eb6611f5d9437ac01e229cb9e85ad8`
   - 832 bytes

Public-safe receipt:

`state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-CANDIDATE-RECEIPT-2026-09-10.json`.

The worker reports:

- all eight carried blockers addressed;
- `semantic_change_required=false`;
- substantive codebook not edited;
- existing candidate/review artifacts not edited;
- no target-model information used;
- `safe_for_blind_re_review=true`.

### What v4 claims to change

The repair is contract-only. Its central claim is that facet cardinality is now scoped to a **stage/event/window**, not to the observable response as a whole. Distinct stages may therefore retain different values from the same facet when the accepted semantics allow a trajectory, while same-stage exclusivity and same-act anti-double-count rules remain in force.

The repair must preserve ordered same-facet trajectories for the previously blocked R02, R03, R15, R16, R20, and R21 cases and avoid analogous silent loss in R10/R12. The worker reports no substantive semantic rewrite.

These are candidate claims, not yet accepted conclusions.

## Exact next gate — independent blind re-review of v4

Run, in a **different fresh target-theory-blind context** from the author of `7ba5654fe99017e1c84a4b8868e5a3da50c55be6`:

- `tasks/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-WORKER-2026-09-10.md`
- following `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-PROMPT-v1-2026-09-10.txt` exactly.

The reviewer must re-grade **all 45 original OA blockers plus NR-001**, not merely the eight carried blockers, and may add only genuine new `NR2-*` material findings.

The re-review must specifically verify:

- `zero_or_one` / `one_or_more` cardinality is stage-local rather than observable-wide;
- legitimate same-facet values can occur at distinct ordered stages;
- deduplication cannot erase a legitimate later/earlier stage;
- provenance and evidence-unit identity remain stage-preserving;
- R02/R03/R15/R16/R20/R21 trajectories are representable;
- analogous R10/R12 stage changes are not lost;
- same-act double counting remains prevented;
- all R05 blockers remain resolved;
- absence/missingness semantics remain resolved.

Implementation is allowed only if the resulting summary sets `safe_for_implementation=true`, all 45 OA findings plus NR-001 are RESOLVED, and no blocking `NR2-*` finding remains.

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

- existing auditor kits remain ineligible for new human collection;
- no engineering implementation before v4 receives a passing independent blind re-review;
- no theory-exposed substantive neutral-codebook repair;
- no automated participant coding before the eventual revised human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
