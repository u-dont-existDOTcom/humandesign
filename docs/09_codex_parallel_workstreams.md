# 09 — Codex Parallel Workstreams

Codex currently supports multi-agent parallel work and isolated worktrees. Use that for engineering throughput, not as the sole blinding mechanism.

## Coordinator
Owns:
- integration plan;
- interfaces;
- merge order;
- acceptance test status;
- unresolved decisions.

It should delegate bounded work and request written handoff notes from each workstream.

## Workstream A — Chart engine
Tasks:
- ephemeris adapter;
- timezone handling;
- 88° Design moment;
- gate/line mapping;
- channels/centers/Type/Authority/Profile;
- event boundaries;
- independent golden tests.

Must not modify scoring theory.

## Workstream B — Model compiler
Tasks:
- typed observation schema;
- compile V4/V3.2 symbolic mappings;
- dependency graph;
- source/rationale tracking;
- unresolved mapping report.

Must not alter chart calculations.

## Workstream C — Synthetic harness
Tasks:
- canonical response simulator;
- noise models;
- blind packaging;
- encryption/sealing;
- restoration/ablation datasets.

Must not alter evaluator metrics.

## Workstream D — Search and adaptive questions
Tasks:
- candidate universes;
- interval search;
- date aggregation;
- ranker;
- expected information gain selector;
- stopping rules.

No access to answer keys during blind tests.

## Workstream E — Human empirical modeling
Tasks:
- person-level split manager;
- regularized `P(answer|chart)` models;
- hybrid priors;
- calibration;
- baselines.

Must not access untouched test labels during tuning.

## Workstream F — Evaluation/audit
Tasks:
- prediction freeze verification;
- leakage scanner;
- permutation tests;
- top-k/rank metrics;
- robustness;
- reporting;
- audit trail.

Ideally separate from decoder during blind runs.

## Workstream G — API/Custom GPT integration
Tasks:
- backend endpoints compatible with existing contract;
- opaque result API;
- answer submission;
- final report;
- transit functionality kept separate from scientific validation.

## Review workstream
A separate reviewer agent should inspect:
- data leakage;
- hidden coupling between generator/decoder;
- untested boundaries;
- dependency double counting;
- in-sample metrics presented as validation;
- non-determinism.
