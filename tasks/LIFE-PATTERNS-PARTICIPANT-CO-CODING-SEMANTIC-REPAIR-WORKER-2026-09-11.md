# Life Patterns participant co-coding semantic repair — worker instructions — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Context boundary

Perform this work in a **fresh target-theory-blind context**. Do not use Human Design, AstroHD, astrology, birth data, chart outputs, model mappings, target-model scores, fit results, prediction logic, or any indication of which neutral behaviors would favor a candidate theory.

This task now incorporates an owner-directed root-cause audit. The audit found that a legitimate anti-leakage requirement was incorrectly converted into a fixed external-ontology requirement. The repair must solve the anti-leakage problem without assuming that a comprehensive externally coded taxonomy is the correct semantic core.

## Required reads

1. `docs/research/LIFE_PATTERNS_CODEBOOK_ARCHITECTURE_ROOT_CAUSE_AUDIT_2026-09-11.md`
2. `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`
3. `docs/research/LIFE_PATTERNS_PARTICIPANT_CO_CODING_ARCHITECTURE_2026-09-11.md`
4. `docs/product/DISCOVER_YOUR_UNIQUE_LIFE_PATTERNS_ROADMAP.md`
5. `docs/research/LIFE_PATTERNS_BEHAVIORAL_FREEZE_SPEC.md`
6. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`
7. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
8. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
9. the current resolved ontology / structured procedure implementation and tests, especially Other Specified handling and non-action gates.

Do not read target-model mapping/scoring material. Historical codebooks/contracts are evidence and reusable mechanics, not a requirement to preserve their fixed-taxonomy architecture.

## Architectural invariants

The repair must satisfy all of these:

1. **Neutrality does not imply taxonomy.** Do not assume a closed ontology is necessary merely because competing models need one shared frozen substrate.
2. **Participant-level recurrence requires participant adjudication.** External coding may propose candidate patterns but must not silently finalize typicality, scope, or recurrence.
3. **Separate epistemic layers.** Distinguish observed episode facts, narrator-reported appraisal/belief, system hypotheses, participant pattern judgments, and genuine absence/nonoccurrence claims.
4. **Absence gates apply only to absence claims.** Failure of a stronger nonoccurrence/counterfactual gate must never erase separately supported positive facts.
5. **Elicited examples are mainly nuance/boundary evidence.** They are not an unbiased recurrence sample merely because the participant can produce them.
6. **Complexity is diagnostic.** If common intelligible behavior repeatedly requires OS/abstention or expanding graph machinery, revisit the abstraction before adding schema.
7. **Every structured field must serve a clear decision.** Prefer fields that improve faithful source preservation, useful next-question generation, participant adjudication, or later frozen model comparison.
8. **Validation machinery must not dictate participant semantics.** The research record should adapt to faithful evidence, not force evidence into a convenient categorical scoring surface.
9. **Preserve open-world gap discovery.** Clear positive behavior must remain representable even when no named category fits.
10. **Recheck the north star.** The target is `Discover Your Unique Life Patterns`, not completion of a behavioral ontology.

## Repair questions

### 1. What is the minimum shared frozen substrate actually required?

Design the smallest theory-neutral record sufficient to prevent model-specific post-hoc reinterpretation. Explicitly compare at least these possibilities rather than presupposing one:

- structured participant-adjudicated pattern claims plus exact episode provenance;
- minimally structured episode facts plus participant-adjudicated person-level patterns;
- a compact extensible episode-fact vocabulary used only for indexing/question generation;
- any genuinely necessary categorical codes.

Explain why each retained structured category is needed.

### 2. Preserve positive behavior when absence claims fail

Keep strict awareness, opportunity, reasonable-feasibility, and established-nonoccurrence requirements for genuine absence/non-action assertions.

But preserve independently supported positive facts such as delay, postponement, rejection, consultation, active consideration, reported appraisal, and resolution. Never convert a narrator's appraisal into an objective fact: e.g. `narrator considered the course too difficult/infeasible`, not `the course was infeasible`, unless independently established.

### 3. Restore open-world gap discovery

Historical V2 supported `OS` / Other Specified with a concrete description. Determine whether the revised architecture still needs OS as a named code or whether open factual records make it unnecessary. Either way, clear behavior outside named categories must be retained with exact provenance and must feed later theory-blind refinement rather than disappearing into `insufficient`.

Do not force a generic fact into a facet if the facet itself is uncertain.

### 4. Simplify episode representation

The episode layer is not a complete taxonomy of personality traits. Prefer decomposable factual dimensions useful for follow-up questioning, for example:

- action/choice state or transition;
- timing/sequence;
- outcome/resolution;
- narrator-reported appraisal/reason;
- consultation/information/action where actually reported;
- context;
- strictly gated absence claims only where justified.

Assess whether current R05-type distinctions are unnecessary for the intended product. A simpler process/resolution/appraisal representation is acceptable if it preserves more information with less inference.

### 5. Make person-level patterns recursively participant-adjudicated

Specify the loop:

`episode -> factual decomposition -> candidate pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised question -> participant adjudication -> accepted/rejected/unresolved pattern`

The participant may correct both the proposed generalization and its scope/conditions. Preserve the system proposal and participant correction separately.

If a participant strongly endorses a pattern but cannot retrieve examples, preserve and probe the discrepancy. Do not automatically infer poor self-awareness; possible explanations include retrieval difficulty, vague identity belief, privacy, low salience, misunderstanding, or limited self-observation. A repeated discrepancy may become a candidate meta-pattern only through participant adjudication.

### 6. Reframe calibration targets

External human/automated calibration may evaluate literal episode-fact extraction. Person-level pattern calibration should instead test whether the system:

- preserves source facts;
- separates appraisal from objective condition;
- proposes useful non-leading candidate-pattern questions;
- incorporates participant corrections faithfully;
- preserves uncertainty, exceptions and rejected hypotheses;
- distinguishes elicited examples from generalized self-report;
- yields a participant-recognized, properly scoped pattern formulation.

Do not define success as external-coder agreement on a supposedly true person-level label that the participant has not adjudicated.

## Required outputs

Create versioned candidate artifacts only; do not overwrite historical V1/V2/V5 artifacts. At minimum produce:

- a disposition of which old mechanics remain useful and which are superseded;
- a minimal revised neutral measurement/pattern architecture;
- a candidate schema/contract for episode facts + participant pattern adjudication, if structured records are needed;
- an explicit statement of what model adapters consume later and how this avoids model-specific rereading;
- a compact review prompt for a **separate fresh target-theory-blind reviewer**;
- focused test requirements.

Do not implement production code until the separate blind review passes.

## Hard boundaries

- no target-theory information;
- no model-fit-driven construct changes;
- no weakening of genuine absence/non-action evidence requirements merely to make cases fit;
- no treating participant-supplied examples as unbiased frequency samples;
- no external classifier claiming final authority over participant-level recurrence;
- no requirement to preserve the fixed 22-observable taxonomy if a simpler neutral substrate is scientifically sufficient;
- no human collection, automated participant coding, target-model scoring/reveal, merge, or deployment from this task.
