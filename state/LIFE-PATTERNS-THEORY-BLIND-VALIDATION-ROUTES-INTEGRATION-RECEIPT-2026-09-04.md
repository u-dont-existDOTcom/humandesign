# Life Patterns — Theory-Blind Validation Routes Integration Receipt

Date: 2026-09-04

Status: **implemented structural research boundary; no validation promotion or target-model execution**.

## Decision implemented

Life Patterns no longer treats full-corpus human-human coding or legacy H1 human-only content authority as the only software-representable path to measurement validation.

The neutral measurement layer now supports exactly one frozen validation-evidence route:

1. `human_human_benchmark`;
2. `statistically_justified_llm_substitution`;
3. `automated_measurement_instrument`.

Route choice must be frozen before target-model results exist.

LLM self-consistency alone is not validation evidence. Automated routes require independent human calibration provenance. The human auditor's first-pass labels must be frozen before the auditor sees automated labels.

## Production contracts

### `src/hdmatch/evaluation/theory_blind_authority.py`

Added/updated:

- `ValidationRoute`;
- `StatisticalLLMSubstitutionReceipt`;
- `AutomatedMeasurementInstrumentReceipt`;
- mutually exclusive route validation in `TheoryBlindContentAuthorityPayload`;
- compact authority receipts carrying the frozen validation route;
- exact content binding and chronology checks;
- preserved independent replication/reconciliation requirement for theory-exposed detailed seed prompts.

The legacy `BlindHumanReliabilityReceipt` remains a valid Route-A object.

### `src/hdmatch/evaluation/neutral_measurement.py`

Integrated:

- legacy stricter `HumanContentAuthorityReceipt` path;
- generic `TheoryBlindContentAuthorityReceipt` path;
- mutual exclusion of the two ontology authority fields;
- exact ontology-content binding for either path;
- validation-stage requirement for generic theory-blind authority;
- `human_baseline_evaluated` **or** `automation_evaluated` observable readiness;
- frozen calibration/validation receipt requirement for automated coders.

The former Life Patterns H1-only core gate is therefore no longer present as a mandatory path. Legacy H1 artifacts remain backward-compatible.

### `src/hdmatch/evaluation/automated_annotation_calibration.py`

Already provides content-addressed provenance for:

- isolated automated coding passes;
- >=3-pass automated ensembles;
- unanimous/majority/unresolved outcomes;
- blind human calibration passes completed before exposure to LLM labels;
- automated-human calibration comparison artifacts.

## Structural tests

Updated/added:

- `tests/unit/test_theory_blind_authority.py`
- `tests/unit/test_neutral_measurement.py`
- `tests/unit/test_neutral_measurement_readiness.py`
- `tests/unit/test_neutral_measurement_theory_blind_routes.py`
- `tests/unit/test_automated_annotation_calibration.py`

The dedicated integration test proves that a validation ontology with **no legacy H1 receipt** can use a theory-blind LLM-substitution authority and `automation_evaluated` readiness, while an automated coder remains blocked until it carries its frozen calibration/validation receipt.

It also proves that:

- development authority cannot carry validation-route evidence;
- validation authority requires exactly one route;
- generic theory-blind authority must bind exact ontology content;
- a development-stage theory-blind receipt cannot freeze an ontology for validation;
- legacy and theory-blind authority cannot both be asserted for one ontology release.

## Verified implementation milestone

Implementation head: `4e9310e375f9f2d22cbe2dd70924d3d66c6a7ccd`

GitHub Actions CI: `33873917019` (`ci`, run #1174) — **success**.

- pytest: **432 passed, 6 expected skips**
- Ruff: **all checks passed**
- mypy: **success, no issues in 140 source files**

The six skips are the existing shallow-checkout / Swiss Ephemeris environment skips, not failures of this implementation.

## Documentation alignment

Updated:

- `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`
- `docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_BRIDGE_SPEC.md`
- `docs/research/LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md`

The older blind-human document is retained as the conventional Route-A protocol, not the default development workflow.

## What this does **not** establish

This implementation does not establish that:

- the 22-observable codebook is reliable or valid;
- GPT/another LLM is accurate enough to replace humans;
- one particular validation route should be chosen;
- any Human Design/AstroHD/astrology model predicts the neutral measurements.

The current reconciled codebook remains a **development candidate**.

## Remaining empirical dependency

Before validation promotion:

1. pin the exact automated coding prompt/model/corpus;
2. freeze repeated isolated theory-blind automated development passes;
3. obtain an independent blind human calibration subset before exposing that auditor to automated labels;
4. analyze stability and automated-human disagreement;
5. perform theory-blind revision if needed;
6. freeze one Route A/B/C validation decision and its acceptance evidence;
7. only then freeze the validation-candidate ontology/coding pipeline.

No merge, deploy, participant/coder contact, spending, target-model adapter execution, model scoring, or validation promotion is authorized by this receipt.
