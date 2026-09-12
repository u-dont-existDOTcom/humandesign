# Life Patterns current state — 2026-09-12

Status: public-safe controlling overlay for `codex/discover-life-patterns-mvp`, draft PR #24.

## Current gate

The required fresh target-theory-blind independent semantic review of the participant-adjudicated open-world neutral-substrate v1 candidate is complete.

Review artifact:

`state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-v1-INDEPENDENT-SEMANTIC-REVIEW-2026-09-12.md`

Review commit:

`9ef485b4b96603a895cacecb1fa60246eff306ae`

Disposition:

- `verdict: BLOCKED`
- `semantic_change_required: true`
- `safe_for_implementation: false`
- `blocking_findings: 6`

Production implementation remains blocked. Human collection and downstream target-model activity remain blocked.

## Reviewed candidate identity

Candidate-producing head:

`d5f95598c2f48b0a6a4ddfedd35b6e6e9e58d7eb`

Candidate architecture:

`state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-SUBSTRATE-v1-CANDIDATE-2026-09-12.md`

Candidate contract:

`state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-CONTRACT-v1-CANDIDATE-2026-09-12.json`

Candidate-specific independent review prompt:

`tasks/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-v1-FRESH-BLIND-REVIEW-2026-09-12.md`

The reviewed candidate blobs at the live review head matched the blobs at the candidate-producing head exactly.

## Review conclusion

The candidate **does correct the main upstream architecture error**. It does not recreate a comprehensive fixed behavioral ontology, fixed 22-observable coverage scheme, universal event-stage graph, recurrence threshold, or `Other Specified` escape hatch as the semantic core. Open-world source-grounded facts plus participant-adjudicated person-level patterns remain the correct direction.

The candidate is nevertheless not yet semantically safe to implement because six narrower contract defects remain:

1. `LP-PAN-v1-REV-001` — a genuine real-world nonoccurrence can be encoded under a non-absence free-text assertion type and thereby bypass the four-part absence gate.
2. `LP-PAN-v1-REV-002` — evidence timing is proposal-relative, so an example elicited after the first pattern proposal can be relabeled `preproposal_anchor` for a later revision.
3. `LP-PAN-v1-REV-003` — only the first proposal is required to have a preproposal anchor; a revised terminal accepted proposition can drift from the factual anchor while inheriting an earlier link.
4. `LP-PAN-v1-REV-004` — participant correction of episode facts has no deterministic append-only provenance/supersession semantics; `participant_correction_note` alone does not determine the current admissible fact.
5. `LP-PAN-v1-REV-005` — uncertainty exists only as optional episode-level notes and is not guaranteed to travel with the affected episode fact into the downstream projection.
6. `LP-PAN-v1-REV-006` — downstream adapters receive episode facts while rejected/unresolved pattern threads are omitted, but no explicit rule prevents target-specific post-freeze aggregation of those facts into a person-level recurrence claim that functionally overrides participant rejection.

These blockers require semantic repair, not a return to the fixed-codebook architecture.

## Corrective invariants that remain accepted

1. neutrality does not imply a closed taxonomy;
2. person-level recurrence/typicality is participant-adjudicated;
3. episode fact, reported appraisal, absence assessment, system proposal, participant adjudication and accepted pattern remain distinct;
4. absence gates apply only to genuine real-world absence/nonoccurrence claims;
5. failed/unclear absence assessment cannot damage independent positive facts;
6. silence is not nonoccurrence;
7. examples elicited after the first pattern proposal are selected scope/boundary evidence, not an unbiased recurrence sample, and revision must not reset that status;
8. participant recognition is not automatically invalidated by failure to recall a new example on demand;
9. multiple similar episodes cannot override participant rejection of the person-level generalization, including downstream after freeze;
10. open-world positive behavior must remain losslessly representable without fixed categorical membership;
11. participant corrections and epistemic uncertainty must remain exact enough to survive into the admissible frozen projection without silent mutation or flattening;
12. downstream adapters receive the same frozen projection and cannot call back into raw source narrative;
13. there is no completion denominator or inferred completion policy.

## Exact next action

Run a **new fresh target-theory-blind semantic-repair context**, different from both the v1 candidate producer and this independent reviewer.

The new repair worker must use the review artifact above as the exact blocker ledger and:

1. preserve the open-world participant-adjudicated architecture;
2. repair the six blocking findings with the smallest semantic changes required;
3. publish a new versioned candidate architecture/contract rather than mutate the reviewed v1 artifacts;
4. produce an exact compact candidate-specific prompt for another separate fresh target-theory-blind reviewer;
5. update `tasks/ACTIVE-TASK.json`, `state/CURRENT-STATE.md`, and this overlay with the new candidate-producing head and review prompt;
6. stop before production implementation.

The next candidate must then receive a separate fresh blind semantic review. No review context may self-repair and self-approve the same candidate.

## Hard boundaries

Until canonical state records a later passing independent semantic review:

- no production implementation of the candidate;
- no human collection;
- no automated participant coding;
- no target-model mapping/scoring/reveal;
- no reading target-model fit/results in the blind repair/review contexts;
- no birth/chart outputs or prior predictions in those contexts;
- no merge/deploy;
- no recruitment/contact;
- no spending.

The private historical V5 owner-review materials remain frozen development evidence and are not acceptance inputs for the semantic repair/review cycle.

## Preserved owner correction

**There was never a completion policy.** Do not infer one from artifact counts, calibration counts, review status, or gating state.
