# Life Patterns — next-conversation handoff — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

GitHub is canonical. Before substantive work, fetch the current PR #24 head and read:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-11.md`
3. `docs/research/LIFE_PATTERNS_CODEBOOK_ARCHITECTURE_ROOT_CAUSE_AUDIT_2026-09-11.md`
4. `docs/research/LIFE_PATTERNS_PARTICIPANT_CO_CODING_ARCHITECTURE_2026-09-11.md`
5. `tasks/LIFE-PATTERNS-PARTICIPANT-CO-CODING-SEMANTIC-REPAIR-WORKER-2026-09-11.md`
6. `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`
7. `docs/product/DISCOVER_YOUR_UNIQUE_LIFE_PATTERNS_ROADMAP.md`
8. `docs/research/LIFE_PATTERNS_BEHAVIORAL_FREEZE_SPEC.md`
9. historical V5/codebook artifacts only as needed for reusable mechanics and regression constraints;
10. `state/CURRENT-STATE.md`.

## Controlling root-cause result

The codebook/V5 path is no longer treated as merely a UI or local semantic problem.

The owner-directed audit traced the architecture back to the 2026-09-03 design sequence and found:

1. The original Life Patterns product was already participant-centered: concrete episodes, participant-confirmed summaries, counterexamples/context, a participant-reviewed Life Patterns Map, and later immutable freeze.
2. The later model-tournament design correctly recognized that competing models cannot each reread raw narrative flexibly after target predictions/results exist.
3. That legitimate requirement for one frozen theory-blind representation was then **incorrectly converted into a requirement for one fixed externally coded behavioral ontology**.
4. The neutral bridge specification promoted the shared ontology/coder to the “main measurement instrument” and made person-level summaries frozen aggregations over episode codes.
5. Subsequent overlap/absence/facet/stage/containment work often made correct local repairs conditional on that premise, but it path-dependently increased schema complexity rather than retesting the premise.
6. Owner review finally exposed the inversion directly: obvious positive behavior could become hard to preserve because it did not satisfy a stronger named category.

Root-cause audit:

`docs/research/LIFE_PATTERNS_CODEBOOK_ARCHITECTURE_ROOT_CAUSE_AUDIT_2026-09-11.md`

The fixed 22-observable/V5 taxonomy remains immutable development history. It may contain reusable mechanics. It is **not presumed to be the future primary semantic architecture**.

## What remains valid

Retain:

- chart/model blindness before neutral freeze;
- participant review/correction of extracted evidence;
- exact source provenance and immutable/content-addressed freezes;
- no model-specific post-hoc rereading/recoding;
- thin frozen model adapters;
- missingness distinct from negative evidence;
- strict awareness/opportunity/reasonable-feasibility/nonoccurrence gates for genuine absence claims;
- theory-blind substantive repair/review;
- uncertainty, counterexamples and participant corrections.

Historical V5 mechanics passed their original gates:

- independent review `ce04642146c41a7d5d94f85360572c78de887682`;
- implementation head `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`;
- CI `34623829382`: 675 passed, 7 expected skips, Ruff clean, strict mypy clean across 174 source files.

Do not confuse those successful conditional mechanics with validation of the fixed-ontology architecture itself.

## Replacement direction

Person-level Life Patterns should be recursively participant-adjudicated:

`episode -> minimal factual decomposition -> candidate pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised question -> participant adjudication -> accepted/rejected/unresolved pattern`

External coding may organize literal episode facts and generate candidate questions. It does not have final authority over whether a recurring pattern characterizes the participant.

Keep epistemic layers separate:

- what happened;
- what the narrator explicitly perceived/believed/wanted/considered difficult;
- genuine absence/nonoccurrence claims;
- system-proposed generalization;
- participant adjudication/correction;
- accepted/rejected/unresolved person-level pattern.

Examples elicited after a pattern proposal are mainly nuance/boundary evidence, not an unbiased frequency sample. Failure to retrieve examples is a discrepancy to probe rather than automatic evidence of poor self-awareness.

## Exact next action

Run in a **fresh target-theory-blind context**:

`tasks/LIFE-PATTERNS-PARTICIPANT-CO-CODING-SEMANTIC-REPAIR-WORKER-2026-09-11.md`

The worker must begin from the root-cause audit and answer the upstream question:

> What is the **minimum shared frozen substrate actually required** to prevent target-model-specific reinterpretation?

It must not assume a comprehensive fixed ontology is necessary merely because one exists historically.

Produce versioned candidate architecture/schema artifacts plus a compact prompt for a **separate fresh target-theory-blind review**. Do not implement production code until that review passes.

The private V5 owner-review candidates are superseded for acceptance and retained only as development evidence of how the architecture problem was discovered.

## Hard boundaries

- no target-theory information in repair/review contexts;
- do not preserve the fixed taxonomy merely because it is sunk work;
- do not weaken genuine absence/non-action evidence requirements merely to make a case fit;
- do not discard supported positive behavior because a stronger absence claim fails;
- do not treat elicited examples as unbiased recurrence/frequency evidence;
- do not give an external classifier final authority over participant-level recurring patterns;
- no human collection, automated participant coding, target-model scoring/reveal, merge/deploy, recruitment/contact, or spending until the revised blind semantic chain authorizes it.
