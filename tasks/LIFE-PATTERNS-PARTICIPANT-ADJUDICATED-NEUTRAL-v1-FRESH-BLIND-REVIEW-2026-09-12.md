# Life Patterns participant-adjudicated neutral substrate v1 — fresh blind semantic review

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

Role: **independent fresh target-theory-blind semantic reviewer**.

Do not implement production code. Do not collect participant data. Do not merge, deploy, recruit, contact, spend, score, reveal, or inspect target-model results.

## Independence boundary

You must be a different fresh context from the candidate producer and supervising context.

Do **not** read:

- target-model mapping/scoring material;
- fit/residual/result artifacts;
- birth/chart outputs or birth-derived predictions;
- prior target predictions;
- any document whose purpose is to reveal which neutral behaviors help or hurt a target theory;
- the candidate producer's private reasoning.

If a permitted file links to prohibited material, do not follow that link.

## Read order

After following `tasks/LIFE-PATTERNS-FRESH-THEORY-BLIND-SEMANTIC-REVIEW-LAUNCH-2026-09-12.md`, read only what is needed for this semantic review, in this order:

1. `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`
2. `docs/research/LIFE_PATTERNS_CODEBOOK_ARCHITECTURE_ROOT_CAUSE_AUDIT_2026-09-11.md`
3. `docs/research/LIFE_PATTERNS_PARTICIPANT_CO_CODING_ARCHITECTURE_2026-09-11.md`
4. `docs/research/LIFE_PATTERNS_BEHAVIORAL_FREEZE_SPEC.md`
5. `state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-SUBSTRATE-v1-CANDIDATE-2026-09-12.md`
6. `state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-CONTRACT-v1-CANDIDATE-2026-09-12.json`

Historical fixed-codebook/V5 artifacts are **not** required to judge this candidate. Do not let implementation history become an authority merely because it exists.

## Review objective

Decide whether the candidate provides the **minimum sufficient frozen theory-blind substrate** for fair downstream comparison while restoring participant-adjudicated Life Patterns and avoiding a hidden replacement ontology.

Review the literal candidate, not an imagined implementation.

### A. Substrate necessity and sufficiency

Check whether the candidate preserves the real prerequisite:

- all downstream adapters can consume one identical immutable behavioral substrate;
- raw narrative cannot be flexibly reread after downstream target information exists;
- the frozen substrate contains enough literal episode evidence and participant-approved person-level pattern information to remain auditable without source rereading.

Block if the candidate is too lossy to support those requirements, or if it quietly makes an unnecessary comprehensive taxonomy a prerequisite again.

### B. Episode-fact semantics

Check that:

- positive occurrences remain preservable even when no vocabulary term fits;
- reported appraisal/belief remains an attributed report, not objective fact;
- temporal/sequence claims require source support;
- missingness/silence is not negative evidence;
- factual records remain exactly traceable to source provenance.

Block any rule that can discard a clear positive fact solely because a stronger categorical or absence claim fails.

### C. Absence semantics

For a genuine nonoccurrence claim, verify that awareness, opportunity, reasonable feasibility, and established nonoccurrence are all required.

Check specifically that a failed/unclear absence assessment:

- remains auditable;
- does not instantiate a negative fact;
- cannot delete, weaken, recode, or demote independent positive facts.

Do not demand absence gating for ordinary positive facts.

### D. Open-world behavior

Check that the candidate truly allows behavior outside any current vocabulary without using `Other Specified` as a disguised closed-taxonomy escape hatch.

An optional index layer is acceptable only if removing it leaves the semantic substrate intact.

### E. Participant pattern authority

Check that system/external coding can propose a person-level pattern but cannot finalize recurrence/typicality without participant adjudication.

Verify that:

- participant acceptance can resolve a grounded pattern without an arbitrary minimum episode count;
- multiple similar episodes cannot override participant rejection;
- participant revision is append-only and traceable;
- counterexamples, conditions, and exceptions can narrow an accepted pattern;
- failure to recall a new example after a proposal is a discrepancy to probe, not automatic invalidation.

Do not reinterpret participant authority as permission to rewrite literal episode facts contrary to their source.

### F. Elicited-example bias

Verify that examples elicited after a candidate pattern has been proposed are explicitly distinguishable from preproposal anchors and cannot silently become an unbiased recurrence-frequency sample.

### G. Downstream anti-rereading boundary

Check whether the adapter projection is mechanically specifiable so that it:

- omits raw transcript/raw narrative text;
- exposes no source resolver;
- binds an exact freeze hash;
- requires the same freeze for all downstream adapters in one comparison;
- returns `unmeasured/not_represented` when the frozen substrate lacks a needed distinction rather than calling back to source narrative.

Block if a downstream adapter can legally reinterpret raw source material after the freeze.

### H. Complexity / manufactured prerequisites

For every required object or field, ask whether it is necessary for provenance, epistemic separation, participant adjudication, auditability, or the no-reread boundary.

Block if the candidate simply moved the old ontology burden into a new mandatory graph, category set, or coverage scheme without demonstrated need.

Do **not** block merely because a future implementation will need ordinary IDs, hashes, canonical serialization, or append-only records.

## Required response artifact

Commit one public-safe review artifact under `state/` with a versioned/date-stamped filename.

Use this exact disposition shape near the top:

```text
candidate_reviewed: LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-v1-CANDIDATE-2026-09-12
verdict: PASS | BLOCKED
semantic_change_required: true | false
safe_for_implementation: true | false
blocking_findings: <integer>
```

For every blocking finding provide:

- stable finding ID;
- exact candidate section/object/rule;
- literal failure mode;
- why it violates a permitted authority document or creates an under/over-specified semantic contract;
- smallest repair needed.

Separate nonblocking implementation suggestions from semantic blockers.

## Pass condition

Return `PASS`, `semantic_change_required=false`, and `safe_for_implementation=true` only if there are **zero semantic blockers** and the candidate is sufficient as a frozen, participant-adjudicated, open-world, theory-blind substrate.

A pass authorizes only the later production-implementation step in canonical state. It does **not** itself authorize human collection, automated participant coding, target-model scoring/reveal, merge/deploy, recruitment/contact, or spending.

If blocked, do not repair the candidate in the review context. Record the blockers and stop so a new semantic-repair cycle can be launched.
