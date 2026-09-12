# Survey-v2 Impact of the 2026-09-07 Reasoning Selection Supplement

Status: design-impact memo only. No frozen Survey-v2 artifact is changed by this memo.

## Decision

**Do not change the frozen Survey-v2 questionnaire, classifier contract, scoring contract, or freeze package solely because of the new reasoning-selection supplement.**

The supplement materially improves how future survey/model work should be reasoned about, but the main measurement safeguards it implies are already present in Survey-v2.

## Existing Survey-v2 controls that already implement the relevant principles

Survey-v2 already:

- asks for recurring patterns rather than isolated salient anecdotes;
- requires evidence across life stages;
- requires negative contrasts/counterexamples rather than support-only narratives;
- preserves `Other`, mixed, context-dependent, unsure, insufficient and unclassifiable outcomes rather than forcing a favorable label;
- distinguishes capacity, preference, motivation, behavior and outcome;
- uses follow-up questions to resolve ambiguity rather than steer toward a candidate prediction;
- freezes predicted archetype labels before participant evidence;
- requires mandatory contrast evidence for scored binary fields;
- treats unmentioned channels as abstentions rather than absences;
- caps dependent/redundant fields rather than counting repeated probes as independent evidence;
- keeps structural recoverability separate from empirical human accuracy;
- requires prospective empirical evaluation, failures, abstentions and controls rather than treating synthetic perfect recovery as Human Design validation.

Relevant current artifacts include:

- `reference/core/survey_v2_behavioral_domains.json`
- `reference/core/survey_v2_human_measurement_scoring_contract_v1_0_0.json`
- `docs/23_survey_v2_recoverability.md`
- `docs/SURVEY-V2-HUMAN-MEASUREMENT-METHODS-CHECK-v1.0.0.md`

## What the supplement changes

The supplement changes **reasoning governance around future development**, not the frozen respondent-facing measurement chain.

For future survey/model development:

1. Identify whether the current phase is exploration, decision, confirmation or release before deciding what kind of reasoning/evidence is admissible.
2. Prefer discriminating contrasts over merely collecting features shared by positive cases.
3. Keep reported observation, participant interpretation and causal explanation distinct where doing so improves measurement reliability.
4. Use abductive/causal reasoning to choose tests that distinguish rival explanations rather than merely elaborate one preferred model.
5. Compare theory-specific predictions against strong non-HD, generic-personality, matched-decoy and chance baselines as appropriate.
6. Test incremental out-of-sample value rather than treating resonance or within-model recoverability as specificity.
7. Preserve mismatches as mismatches; do not rescue them with post-hoc narrative reinterpretation.
8. Revise development models openly and evaluate revisions on new eligible evidence.

## Candidate Survey-v3 experiments, not Survey-v2 edits

The following are reasonable future **measurement-development experiments** if a new survey version is authorized. They are not automatic improvements and should be tested before adoption:

### A. Observation / interpretation / causal-explanation separation

For some narrative domains, capture separately:

- what concretely happened;
- what the participant thinks it meant;
- what the participant thinks caused it.

Hypothesis: this may reduce coder contamination from participant theory while preserving phenomenology. Counter-risk: extra structure may increase burden and suppress useful natural narrative.

### B. Matched-discriminator probes

Where two or more candidate constructs share a generic feature, ask for the feature that distinguishes them rather than re-asking the shared feature.

Hypothesis: this should improve specificity. Counter-risk: discriminator prompts may become more leading or theory-revealing if not carefully blinded.

### C. Explicit falsifier probes

For high-weight constructs, test whether a narrowly defined situation that should be uncommon under the proposed pattern is actually common for the participant.

Hypothesis: this may improve counterevidence sensitivity. Counter-risk: poorly chosen falsifiers can confuse context-dependence with contradiction.

Any such change creates a new version and requires new freeze hashes, new fixtures, and fresh eligible development/validation evidence. It must not be backported into already-frozen Survey-v2 runs.

## Non-change rationale

Changing a frozen instrument simply because a later reasoning document uses better language would create avoidable researcher degrees of freedom. The correct integration is to preserve the frozen instrument, document where the new principles are already satisfied, and route genuinely new ideas into a future-version development lane.
