# CODEX MASTER PROMPT

Build the full research harness described by this repository.

Start by reading `AGENTS.md` and `ARCHITECTURE.md`, then the numbered docs in `docs/`. Treat `reference/core/` as normative source material for the existing Human Design V4/V3.2 symbolic model.

## Objective

Deliver a reproducible Python project and CLI that can:

1. calculate exact HD chart-state intervals with historical timezone handling and exact Design moment;
2. compile the existing symbolic behavioral model into machine-readable rules;
3. generate blinded synthetic questionnaire cases from that same frozen model;
4. recover hidden birth day/time from known month/year and broader candidate universes;
5. restore/ablate independent response clusters and run adaptive information-gain questioning;
6. cryptographically freeze predictions before answer-key reveal;
7. evaluate synthetic recovery;
8. import known human development cases;
9. fit empirical chart→response models post hoc on development humans;
10. compare symbolic, empirical, and hybrid decoders;
11. perform person-level validation and preserve an untouched final test pathway;
12. produce transparent reports including failures/ties/unresolved intervals.

## Use parallel agents/worktrees

Delegate separable work to parallel agents:
- exact chart engine,
- model compiler,
- synthetic harness,
- search/adaptive questioning,
- human empirical modeling,
- evaluation/audit,
- API integration.

Keep interfaces explicit and merge only after tests.

## Critical scientific constraints

- Post-hoc fitting on development humans is ALLOWED.
- Do not present development-set performance as predictive validation.
- Never let decoder/evaluator see answer keys before prediction freeze.
- Do not silently invent missing HD mappings.
- Do not use coarse time grids as proof of minute precision.
- Report stable intervals.
- Split human data by person.
- Include chance/permutation and calendar/season baselines.
- Preserve all failures.
- Rubric bits are not probabilities.
- Human Design is treated as an experimental symbolic hypothesis.

## First deliverable

Do not attempt the full century search first.

Implement an end-to-end **known-month synthetic oracle benchmark**:
- generator uses the frozen model;
- 1,000 blinded cases;
- exact candidate intervals for all days in each month;
- blind decoder;
- prediction freeze;
- answer-key reveal;
- top-1/top-3/top-5/MRR report;
- ablation/restoration curves;
- leakage audit.

Then add noise tiers and known-date time rectification.

## Definition of done for the initial milestone

The repository has:
- installable package;
- documented environment;
- tests;
- exact run manifests/hashes;
- one command to generate a blind experiment;
- one command to recover it without key access;
- one command to freeze;
- one command to reveal/evaluate;
- a report explaining every oracle failure.

When a requirement is underspecified, mark it unresolved rather than choosing whatever improves recovery.
