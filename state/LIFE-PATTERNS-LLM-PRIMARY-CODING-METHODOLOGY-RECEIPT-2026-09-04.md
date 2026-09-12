# Life Patterns — LLM-Primary Coding Methodology Receipt

Date: 2026-09-04

Status: owner-approved development methodology. No target-model execution, participant/coder contact, spending, validation promotion, merge, or deployment authorized.

## Decision

Full-corpus dual-human coding is no longer the required default development route.

Default development design:

1. freeze exact neutral codebook, corpus, coding procedure, and prompt;
2. run a high-capability theory-blind automated coder over the full development corpus in at least three isolated passes when feasible;
3. freeze every raw pass before consensus/adjudication;
4. preserve unanimous, majority, and unresolved outcomes separately;
5. obtain an independent theory-blind human calibration pass on a strategically sampled subset before exposing that auditor to automated labels;
6. use human/model disagreement to detect codebook ambiguity and systematic model failure;
7. allow theory-exposed owner coding only as a separate post-freeze sensitivity analysis;
8. perform any substantive revision in a theory-blind context;
9. choose/freeze the final validation route before target-model results.

## Why

The 22-observable reconciled codebook contains many prerequisite, missingness, sequence, and context decisions. Full-corpus human annotation creates substantial fatigue/attention burden and exact human-human identity is neither expected nor required for measurement reliability.

Automated consistency is useful but not proof of correctness. Therefore repeated model stability is paired with independent human calibration rather than treated as self-validating.

## Validation routes left open

Before confirmatory model scoring, freeze one route:

- conventional independent human benchmark;
- statistically justified automated-annotator substitution on a human calibration subset;
- explicit automated measurement instrument with preregistered stability/human-audit criteria and no claim of human-gold-standard equivalence.

Route selection cannot depend on target-model performance.

## Implemented artifacts

- `docs/research/LIFE_PATTERNS_LLM_PRIMARY_CODING_PROTOCOL.md`
- `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`
- `docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_BRIDGE_SPEC.md`
- `docs/research/LIFE_PATTERNS_BLIND_CODER_PACKET.md`
- `src/hdmatch/evaluation/automated_annotation_calibration.py`
- `tests/unit/test_automated_annotation_calibration.py`

Automated calibration implementation commit: `92a4debc82f1065070c5292a354294ac217fd0b6`.

CI run `33823816163`: success for tests, Ruff, and mypy.

## Human assignment

- owner-designated external person: pseudonymous `BLIND-HUMAN-AUDITOR-A`, calibration subset only, eligibility pending blind attestation;
- owner: theory-exposed sensitivity coder only, after blind outputs freeze;
- second external human: not required to begin development.

## Remaining software debt

Current validation authority gates remain stricter than this revised policy and still require legacy human/H1 or human-human receipts. They fail closed and are not bypassed. They must be generalized before a non-human-benchmark validation route can be represented.
