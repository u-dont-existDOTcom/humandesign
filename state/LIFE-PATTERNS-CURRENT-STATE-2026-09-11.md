# Life Patterns current state — 2026-09-11

Status: public-safe controlling overlay for `codex/discover-life-patterns-mvp`, draft PR #24.

## Current gate

The previously accepted V5 record-containment/facet implementation remains mechanically verified, but owner review exposed a **new substantive measurement-architecture problem**. Owner UI review is therefore paused; human collection remains unauthorized.

Two linked issues now control continuation:

1. strict absence/non-action gates are valid and must remain strict, but failure of an absence gate must not erase separately supported positive behavioral facts or narrator-reported appraisals;
2. person-level recurring Life Patterns should be **participant-adjudicated recursively**, not inferred solely by an external human/automated classifier from elicited episodes.

Historical V2 also supported `OS` / Other Specified with a concrete description as a gap-discovery path. V5 dropped that route. This can turn a clearly informative episode into `insufficient` merely because no enumerated V5 value fits cleanly.

The next action is a fresh target-theory-blind semantic repair, not more UI polishing.

## Preserved accepted mechanics

- independent V5 review: `ce04642146c41a7d5d94f85360572c78de887682`
- implementation head: `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`
- CI `34623829382`: SUCCESS
- 675 passed, 7 expected skips, Ruff clean, strict mypy clean across 174 source files

These remain useful implementation history. The new finding does not justify weakening record containment, stage/evidence ownership, provenance, or the four-part absence gate.

## New architecture correction

Public-safe owner-directed architecture:

`docs/research/LIFE_PATTERNS_PARTICIPANT_CO_CODING_ARCHITECTURE_2026-09-11.md`

Core principle:

> Episodes are concrete elicitation/evidence anchors. The participant is the primary authority on whether a proposed recurring person-level pattern actually characterizes them. GPT/human coding organizes episode facts, notices candidate structure, formulates non-leading follow-up hypotheses, and recursively incorporates participant corrections.

Preferred loop:

`episode -> minimal factual decomposition -> candidate pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised question -> participant adjudication -> accepted/rejected/unresolved pattern`

Examples elicited after a candidate pattern is proposed are mainly useful for nuance, scope, contradiction, and better subsequent questions. Their existence is not intrinsically important as empirical recurrence, because the examples were elicited rather than sampled from an unbiased opportunity frame.

If a participant endorses a pattern but cannot retrieve examples, preserve and probe that discrepancy. It may reflect retrieval difficulty, vague identity belief, low salience, privacy, misunderstanding, limited self-observation, or something else. Do not infer lack of self-awareness from one such failure. Repeated retrieval/awareness discrepancies may themselves become a candidate meta-pattern only through participant adjudication.

## Episode coding implication

The primary episode layer is not meant to be a complete taxonomy of personality traits. It should preserve useful factual dimensions with minimal inference, including where relevant:

- what happened / choice or action state;
- timing and sequence;
- outcome or resolution;
- narrator-reported appraisal or reason, explicitly attributed to the narrator rather than converted into an objective condition;
- context;
- strictly gated absence/non-action claims only when their stronger prerequisites are established.

For example, `choice delayed`, `narrator considered proposed course too difficult`, and `later rejected proposed course` are distinct positive facts. None should disappear merely because a stronger claim such as `remained unresolved during a feasible window` fails its feasibility gate.

## Other Specified / gap discovery

Historical V2's `OS` function must be restored or replaced by an equivalent V5 mechanism that:

- preserves clear substantive behavior not adequately represented by enumerated values;
- captures a concrete behavioral description with exact provenance;
- binds it to the appropriate facet/stage when known, without inventing facet certainty when it is not known;
- feeds later theory-blind codebook refinement rather than becoming a permanent miscellaneous bucket.

OS/gap cases can then be reviewed theory-blind to determine whether they fit an existing code with clearer wording, reveal a missing recurring category, belong to another facet, or should remain open-ended.

## Calibration implication

External human/automated calibration remains useful for the episode-fact layer. Person-level pattern calibration should instead evaluate whether the system faithfully preserves source facts, separates appraisal from objective condition, generates useful non-leading candidate-pattern questions, incorporates participant corrections, preserves uncertainty and counterexamples, and yields a final pattern formulation the participant recognizes as accurate and properly scoped.

Do not define person-level success as external-coder agreement on one supposedly true recurring label that the participant has not adjudicated.

## Exact next action

Run in a **fresh target-theory-blind context**:

`tasks/LIFE-PATTERNS-PARTICIPANT-CO-CODING-SEMANTIC-REPAIR-WORKER-2026-09-11.md`

The worker must produce versioned candidate semantic/contract repairs and a separate blind-review prompt. Do not implement production changes until that separate blind review passes.

## Private calibration source remains frozen

The exact private transport and inner receipt remain verified and unchanged:

- outer ZIP SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- inner LPHB2 receipt SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- selected coverage remains 44 episode + 22 series units.

The existing private owner-review candidates are superseded for acceptance by this semantic finding. Keep them only as development evidence of how the problem was discovered.

## Hard boundaries

- no target-theory information in the semantic repair context;
- do not weaken absence/non-action gates merely to force a case into a value;
- do not discard supported positive behavior because a stronger absence claim fails;
- do not treat elicited examples as unbiased frequency evidence;
- do not give an external classifier final authority over person-level recurrence;
- no human collection, automated participant coding, target-model scoring/reveal, merge/deploy, recruitment/contact, or spending until the revised blind semantic chain authorizes it.

## Preserved owner correction

**There was never a completion policy.** That premise was invented earlier and must not be recreated or inferred from artifact counts.
