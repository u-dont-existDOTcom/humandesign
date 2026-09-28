# Empirical Astrology — Pro Chat Reasoning Instructions for Waves 3 and 4

Date: 2026-09-28

## Role

This task is specifically for a Pro reasoning chat.

Do not redo mechanical extraction work already completed by the Work chat.
Use the prepared evidence packets and inspect underlying sources only where necessary to resolve a material ambiguity.

## Wave 3 Pro decision

Read:
- notes/empirical_astrology/master/PRO_HANDOFF_WAVE3.md
- reference/empirical_astrology/pro_reasoning_packet_wave3.json
- notes/empirical_astrology/master/evidence_map.md
- data/empirical_astrology/master/candidate_feature_registry.jsonl
- data/empirical_astrology/master/negative_constraint_registry.jsonl
- notes/empirical_astrology/master/literature_derived_algorithm_spec.md

Decide and commit:
- reference/empirical_astrology/literature_model_v1_decision.json
- notes/empirical_astrology/master/PRO_DECISION_WAVE3.md

The decision must explicitly state:
1. included feature families;
2. excluded feature families;
3. exploratory-only features;
4. exact moderator/interaction terms;
5. weighting policy;
6. whether weights are effect-size-derived, equal-initialized, or learned only on development data;
7. dependency/corroboration controls;
8. negative constraints;
9. unresolved conflicts and what evidence would resolve them;
10. frozen version identifier.

Do not use owner-specific fit to choose the model.
Do not use known human outcomes as validation evidence.
Prefer simpler models when evidence support is equivalent.

## Wave 4 Pro decision

After the Work chat produces:
- notes/empirical_astrology/master/WAVE4_DEVELOPMENT_RESULTS.md
- data/empirical_astrology/master/wave4_results.jsonl
- notes/empirical_astrology/master/PRO_HANDOFF_WAVE4.md

decide:
1. whether any observed gains are robust to ablation and null baselines;
2. whether any feature family should be removed;
3. whether any interaction deserves a new development version;
4. whether results are plausibly explained by leakage, cohort structure, multiple testing, or dataset reuse;
5. which exact model should be frozen for untouched testing;
6. the smallest high-information prospective experiment.

Create:
- reference/empirical_astrology/literature_model_v2_decision.json, only if a revision is justified;
- notes/empirical_astrology/master/PRO_DECISION_WAVE4.md
- docs/empirical_astrology/02_prospective_validation_spec.md

## Prospective design rules

Keep these explicit:
- historical literature = development evidence;
- owner-known cases = development evidence;
- no post-hoc repair on untouched participants;
- same-hospital near-time-birth primary analysis remains theory-neutral;
- aspect/orb tightness and angularity are preregistered secondary moderators;
- specific aspect-to-trait mappings frozen before outcomes;
- held-out replication required;
- compare against date/time/location and non-astrological baselines;
- report failures.

## Git

Save all decisions in u-dont-existDOTcom/humandesign.

Suggested branch:
worker/empirical-astrology-pro-decisions
