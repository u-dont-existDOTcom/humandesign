# Life Patterns Neutral Codebook — Reconciliation / Pilot Milestone Receipt

Date: 2026-09-04

Status: development milestone only. No merge, deploy, recruitment, spending, validation promotion, or target-model execution is authorized.

## Preserved substantive artifacts

- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-DRAFT-v1-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-REPLICATION-DRAFT-v1-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-REPLICATION-CROSSWALK-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-RECONCILIATION-PROMPT-v1-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

The reconciled candidate was produced in a theory-blind context from the two preserved source drafts. It contains 22 primary episode-level observables and moves cross-episode recurrence, context variability, temporal change, and several state-linked comparisons into metadata/derived summaries to avoid double-counting the same underlying evidence.

## Theory-leakage disposition

No obvious direct Human Design/AstroHD/astrology-specific construct leakage was identified in the first draft, minimally seeded replication, or reconciled candidate.

The initial detailed prompt was authored by a theory-exposed project context and remains documented as a prompt-steering contamination risk. That risk is addressed at the development stage by the separately preserved minimally seeded replication and blind reconciliation. It is not represented as proof of zero pretraining exposure or construct validity.

## Owner methodology correction — LLM-primary coding

The earlier default plan required two humans to code the full development corpus. The owner identified a practical and methodological weakness: a 22-observable codebook with prerequisite, missingness, sequence, and context decisions creates substantial human attention burden, and exact human-human agreement is neither realistic nor the scientific objective.

The default development route is now:

- high-capability theory-blind LLM as primary full-corpus coder;
- at least three isolated repeated automated passes when feasible;
- all raw passes frozen before consensus/adjudication;
- unresolved model disagreement preserved rather than forced;
- one theory-blind human auditor codes a strategically sampled subset independently, without seeing model labels first;
- theory-exposed owner may code only as a separate post-freeze sensitivity analysis.

Canonical protocol:

- `docs/research/LIFE_PATTERNS_LLM_PRIMARY_CODING_PROTOCOL.md`

The prior all-human protocol remains available as a stricter alternative:

- `docs/research/LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md`

A second human is not required to begin the development pilot.

## Machine-checkable contracts

Implemented:

- `src/hdmatch/evaluation/theory_blind_authority.py`
- `src/hdmatch/evaluation/pilot_reliability.py`
- `src/hdmatch/evaluation/automated_annotation_calibration.py`
- corresponding unit tests.

The automated calibration layer content-addresses repeated isolated model passes, frozen consensus/stability reporting, blind human calibration output, and the model-human comparison. It explicitly records that model self-consistency does not establish correctness or construct validity.

## Validation-route policy

Full-corpus human coding is no longer a universal scientific requirement.

Before confirmatory model scoring, the project must freeze one validation route without seeing target-model results:

1. conventional independent human benchmark;
2. statistically justified automated-annotator substitution on a human calibration subset; or
3. explicitly preregistered automated measurement instrument with replicated stability plus independent human audit, without claiming a human gold standard.

The current software validation authority contracts are still stricter than this revised policy and fail closed on the legacy human-human/H1 path. That mismatch must be generalized before a non-human-benchmark validation route can be represented. It must not be bypassed with fabricated receipts.

## Current human role assignment

The owner-designated external person is represented only as pseudonymous `BLIND-HUMAN-AUDITOR-A`, pending blind attestation. Personal identity is not stored in the public repository.

The owner is theory-exposed and may perform a post-freeze sensitivity pass, but does not count as a blind auditor.

## Scientific next dependency

The next substantive development step is to pin the exact primary automated coder/model and coding prompt, select/freeze a development corpus, run independent blinded automated passes, and obtain the blind human calibration subset. No human contact or spending is authorized by this receipt.

## CI baseline

Implementation head `77de467c66be30c90902a83bfb4fa3fa66c7c1b2` previously passed:

- 422 tests, 6 expected skips;
- Ruff all checks passed;
- mypy success, no issues in 139 source files.

The later LLM-primary/calibration extension has its own normal CI runs and must pass before merge consideration.
