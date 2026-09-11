# Life Patterns participant co-coding semantic repair — worker instructions — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Context boundary

Perform this work in a **fresh target-theory-blind context**. Do not use Human Design, AstroHD, astrology, birth data, chart outputs, model mappings, target-model scores, fit results, prediction logic, or any indication of which neutral behaviors would favor a candidate theory.

This task arises from an owner audit of the neutral measurement architecture. The audit found that the current V5 representation can preserve strict absence/non-action gates while still losing clear positive behavioral information, and that the person-level recurring pattern should be participant-adjudicated rather than inferred solely by external coding.

## Required reads

1. `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`
2. `docs/research/LIFE_PATTERNS_PARTICIPANT_CO_CODING_ARCHITECTURE_2026-09-11.md`
3. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`
4. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
5. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
6. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
7. the current resolved ontology / structured procedure implementation and tests, especially Other Specified handling and non-action gates.

Do not read target-model mapping/scoring material.

## Repair questions

Produce a minimal theory-neutral repair that answers all of the following.

### 1. Preserve positive behavior when absence claims fail

A strict absence/non-action assertion may require awareness, opportunity, reasonable feasibility, and established nonoccurrence. Keep that protection.

But failure of such a gate must not erase separately supported positive facts such as delay, postponement, rejection, consultation, active consideration, reported appraisal, or other observed behavior.

Separate:

- what happened;
- what the narrator explicitly reported perceiving/believing/wanting/considering difficult or infeasible;
- stronger absence/counterfactual claims that require a gate.

Never convert a narrator's appraisal into an objective fact. For example, encode 'narrator considered the course infeasible/difficult' rather than 'the course was infeasible' unless the source independently establishes the latter.

### 2. Restore a usable Other Specified / gap-discovery path

Historical V2 supported `OS` / Other Specified with a concrete description. Determine how V5 should preserve this function without creating facet ambiguity.

The development purpose of OS is not a permanent miscellaneous bin. It is a gap-discovery mechanism:

- preserve clear behavior not adequately represented by enumerated values;
- bind the concrete description to exact source provenance and the appropriate facet/stage when determinable;
- allow later theory-blind review to decide whether it fits an existing code, needs wording clarification, reveals a missing recurring category, belongs to another facet, or should remain OS.

Do not force generic OS into a facet if the facet itself is genuinely uncertain; represent that uncertainty explicitly and mechanically.

### 3. Simplify episode coding where possible

The primary episode layer is not intended to be a complete taxonomy of personality traits. Prefer decomposable factual dimensions that are useful for follow-up questioning, such as:

- action/choice state or transition;
- timing/sequence;
- outcome/resolution;
- narrator-reported appraisal/reason;
- context;
- strictly gated absence claims only where justified.

Assess whether current R05-type distinctions are unnecessarily elaborate for this purpose. If a simpler process/resolution/reported-appraisal decomposition retains more source information with less inference, specify it as a candidate repair while preserving historical artifacts.

### 4. Make person-level patterns participant-adjudicated

The final recurring Life Pattern is not to be inferred solely from selected episodes by an external coder.

Specify a recursive participant co-coding loop:

`episode -> factual decomposition -> candidate pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised question -> participant adjudication -> accepted/rejected/unresolved pattern`

Examples elicited after a candidate pattern is proposed are primarily for nuance, boundary finding, contradiction, and question refinement. They are not automatically independent frequency evidence.

If a participant endorses a pattern but cannot retrieve examples, preserve the discrepancy and probe it. Do not automatically infer poor self-awareness; possible explanations include retrieval difficulty, vague identity belief, privacy, low salience, misunderstanding, or limited self-observation. Repeated discrepancies may themselves become a candidate meta-pattern only through participant adjudication.

### 5. Reframe calibration targets

External human/automated calibration may still evaluate episode-fact extraction. But person-level pattern calibration should focus on whether the system:

- preserves source facts;
- separates appraisal from objective condition;
- generates non-leading candidate-pattern questions;
- updates from participant corrections;
- preserves uncertainty/counterexamples;
- distinguishes examples from generalized self-report;
- produces a final pattern formulation the participant recognizes as accurate and properly scoped.

Do not define success as external-coder agreement on one supposedly true person-level label when the participant has not adjudicated that label.

## Required outputs

Create versioned candidate artifacts only; do not overwrite historical V1/V2/V5 artifacts. At minimum produce:

- a repair rationale/disposition document;
- a candidate revised neutral measurement/pattern architecture sufficient to resolve OS + participant co-coding semantics;
- any required candidate schema/contract changes;
- a compact review prompt for a **separate fresh target-theory-blind reviewer**;
- focused test requirements, but do not implement production code until the separate blind review passes.

## Hard boundaries

- no target-theory information;
- no model-fit-driven construct changes;
- no weakening of absence/non-action evidence requirements solely to make cases fit;
- no treating participant-supplied examples as unbiased frequency samples;
- no external classifier claiming final authority over participant-level recurrence;
- no human collection, automated participant coding, target-model scoring/reveal, merge, or deployment from this task.
