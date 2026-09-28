# Empirical Astrology — Pro Reasoning After Full-Text Expansion and Wave 4

Date: 2026-09-28

This file defines two Pro reasoning gates.

Do not redo mechanical literature extraction or implementation work.

---

# PRO GATE 1 — Wave 3B after expanded full-text recovery

Read:
- frozen prior decision:
  - `notes/empirical_astrology/master/PRO_DECISION_WAVE3.md`
  - `reference/empirical_astrology/literature_model_v1_decision.json`
- expanded evidence:
  - `notes/empirical_astrology/master_v2/FULLTEXT_EXPANSION_REPORT.md`
  - `notes/empirical_astrology/master_v2/evidence_map.md`
  - `data/empirical_astrology/fulltexts_v2/primary_feature_extractions.jsonl`
  - `data/empirical_astrology/master_v2/candidate_feature_registry.jsonl`
  - `data/empirical_astrology/master_v2/negative_constraint_registry.jsonl`
  - `reference/empirical_astrology/pro_reasoning_packet_wave3b.json`
  - `notes/empirical_astrology/master_v2/PRO_HANDOFF_WAVE3B.md`

Question:
Does the expanded original-source evidence justify changing any part of the frozen Wave 3 decision?

Adjudicate CF-001 through CF-008 individually.

For each:
- exact operational definition;
- independent cohort count;
- effect size / uncertainty;
- replication status;
- multiplicity;
- selection/control quality;
- dataset reuse;
- transportability to our target domain;
- whether it should be:
  - included;
  - exploratory only;
  - secondary moderator only;
  - excluded;
  - unresolved pending specific evidence.

Decide:
- included feature families;
- excluded families;
- exact interactions/moderators;
- weighting policy;
- dependency/corroboration caps;
- negative constraints;
- whether the primary theory-neutral same-hospital time-distance hypothesis remains primary;
- which exact version should be frozen for Wave 4.

Do not optimize on owner-known outcomes.
Do not count reanalyses as independent replications.

Commit:
- `reference/empirical_astrology/literature_model_v1b_decision.json`
- `notes/empirical_astrology/master_v2/PRO_DECISION_WAVE3B.md`

Use a dedicated Pro branch:
`worker/empirical-astrology-pro-wave3b-wave4`

---

# PRO GATE 2 — Wave 4 development-result adjudication

After Work creates:
- `notes/empirical_astrology/master_v2/WAVE4_DEVELOPMENT_RESULTS.md`
- `data/empirical_astrology/master_v2/wave4_results.jsonl`
- `notes/empirical_astrology/master_v2/PRO_HANDOFF_WAVE4.md`

Adjudicate:
1. robustness to ablation;
2. null/baseline comparisons;
3. leakage;
4. cohort/site/date structure;
5. multiplicity;
6. dataset reuse;
7. whether any apparent gain is practically meaningful;
8. whether any feature should be removed;
9. whether any interaction deserves a new development version;
10. what exact model should be frozen for untouched testing.

Do not fit to Wave 4 outcomes merely because a feature looks better after inspection.

If revision is justified, create a new version rather than rewriting the old decision.

Create:
- `notes/empirical_astrology/master_v2/PRO_DECISION_WAVE4.md`
- `docs/empirical_astrology/02_prospective_validation_spec.md`
- `reference/empirical_astrology/literature_model_v2_decision.json` only if a revision is scientifically justified.

The prospective spec must retain:
- historical literature = development evidence;
- owner-known cases = development evidence;
- same-hospital near-time-birth primary analysis remains theory-neutral unless a strong reason to change is documented;
- any aspect/orb/angularity analysis is secondary unless an exact mapping was frozen outcome-blind;
- specific aspect-to-trait mappings frozen before participant outcomes;
- held-out replication;
- conventional date/time/location/season baselines;
- failures reported;
- no post-hoc rescue by astrological interpretation.
