# Empirical Astrology — Overnight Work-Chat Continuation

Date: 2026-09-28

## Role boundary

This task is for a Work / execution chat.

It may:
- normalize records;
- deduplicate citations/datasets mechanically;
- retrieve full texts;
- extract methods/results/statistics;
- build registries;
- implement already-specified feature calculations;
- run tests;
- run ablations once the model specification is frozen;
- prepare complete evidence packets for a Pro chat.

It must NOT make high-level scientific/model-design judgments that materially affect the research direction.

Whenever the next step requires deciding:
- which empirical findings are genuinely credible enough to include;
- how conflicting studies should be adjudicated;
- how to weight or combine features;
- whether an interaction should enter the model;
- whether an apparent positive survives methodological criticism;
- how to define the optimized model architecture;
- how to design the next confirmatory protocol;
- how to interpret surprising results;
then the Work chat must create a Pro-handoff packet and stop that decision branch rather than decide it itself.

Use:
- GPT-5.6 Sol Extra High for the execution worker if available.
- Pro chat for reasoning gates.

Do not use Deep Research.

## Prerequisite

First complete:
- tasks/EMPIRICAL_ASTROLOGY_SINGLE_WORKER_END_TO_END_20260928.md

Do not stop merely because the literature phase ends. Continue with the executable work below until a genuine Pro-only judgment is reached.

---

# Wave 3A — Mechanical model-preparation work

## Hard gate

Do not begin until the end-to-end literature outputs exist.

Required:
- notes/empirical_astrology/master/END_TO_END_REPORT_20260928.md
- data/empirical_astrology/master/source_registry.jsonl
- data/empirical_astrology/master/dataset_registry.jsonl
- data/empirical_astrology/master/candidate_feature_registry.jsonl
- data/empirical_astrology/master/negative_constraint_registry.jsonl
- notes/empirical_astrology/master/literature_derived_algorithm_spec.md

## Work-chat tasks

Create:
- reference/empirical_astrology/pro_reasoning_packet_wave3.json
- notes/empirical_astrology/master/PRO_HANDOFF_WAVE3.md

The packet must contain, for every candidate feature family:
- exact feature definition;
- all supporting source_document_ids;
- all contradicting/null source_document_ids;
- independent dataset count;
- reused-dataset warnings;
- effect sizes and uncertainty where available;
- replication status;
- multiplicity risk;
- confounds;
- whether the literature evidence is comparable enough to combine;
- any exact unresolved choices a Pro chat must make.

Also create executable feature calculators only for features whose calculation is already unambiguous from the literature:
- src/hdmatch/empirical_astrology/
- tests/empirical_astrology/

Do not assign final weights or decide final inclusion/exclusion.

## Pro gate

When the Wave 3 packet is complete, the next required action is:

A Pro chat must decide:
1. which features enter literature_model_v1;
2. which are excluded or exploratory-only;
3. which interactions/moderators are justified;
4. weighting policy;
5. dependency/corroboration caps;
6. negative constraints;
7. which unresolved findings need targeted replication before inclusion.

The Work chat must not make these decisions.

---

# Wave 3B — Implementation after Pro decision

Only after a Pro chat has written and committed a frozen model decision artifact, for example:

- reference/empirical_astrology/literature_model_v1_decision.json
- notes/empirical_astrology/master/PRO_DECISION_WAVE3.md

the Work chat may continue.

Implement exactly that decision into:
- reference/empirical_astrology/literature_feature_registry_v1.json
- reference/empirical_astrology/literature_model_v1.json
- docs/empirical_astrology/01_literature_model_v1.md
- src/hdmatch/empirical_astrology/
- tests/empirical_astrology/

Run unit tests and deterministic fixtures.

Do not improve, reinterpret, or retune the Pro decision.

---

# Wave 4A — Mechanical retrospective evaluation

After implementation, run only predeclared DEVELOPMENT evaluations.

Allowed:
- historical literature datasets where reconstructable;
- already-inspected owner/development cases;
- existing development cohorts;
- synthetic/negative controls;
- ablations and null models.

Required comparisons:
- full literature-derived model;
- feature-family ablations;
- date-only;
- time-only;
- location-only;
- season/cohort baselines;
- random-feature controls;
- negative-constraint-only checks where meaningful.

Create:
- experiments/empirical_astrology/wave4/
- notes/empirical_astrology/master/WAVE4_DEVELOPMENT_RESULTS.md
- data/empirical_astrology/master/wave4_results.jsonl

Do not tune to improve owner rank or known outcomes.

If any result is surprising, conflicting, or demands a model change, prepare:
- notes/empirical_astrology/master/PRO_HANDOFF_WAVE4.md

and defer interpretation/model changes to Pro.

---

# Wave 4B — Pro reasoning gate

A Pro chat must decide:
- whether Wave 4 supports any model revision;
- whether any feature family should be removed;
- whether any interactions deserve a new version;
- whether results are likely leakage/confounding;
- what untouched prospective test should come next;
- what should be frozen before that test.

The Work chat must not adjudicate these points.

---

# Overnight completion criterion

The overnight Work chat should keep going until it reaches the first genuine Pro-only decision gate.

If Wave 3 Pro decisions already exist, continue through implementation and Wave 4 mechanical evaluation.

If they do not exist, finish every preparatory artifact necessary so a Pro chat can make the decision immediately without re-reading the corpus.

Do not stop at a plan.
Do not ask routine questions.
Do not modify Wave 1 raw files.
Save all work in u-dont-existDOTcom/humandesign.

Work branch:
worker/empirical-astrology-overnight-execution

If shell Git auth fails, use the connected GitHub API.
