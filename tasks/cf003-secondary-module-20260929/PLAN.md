# CF-003 chart-blind behavioral dominance secondary module

Date: 2026-09-29
Assurance lane: Decision/iteration for a reversible development-secondary research module. This task does not alter the frozen TN-001 primary endpoint, LiteratureModelV1, or the deployed dark Railway participant service.

## Owner outcome

Add a small, chart-blind CF-003 development/secondary module now. Keep the published seven-factor astronomical predictor separate from the human target. Reuse existing rich autobiographical survey material where possible, add the missing Sun-like behavioral construct and minimal cross-construct dominance probes, and support a clean prospective test after the target scorer is frozen.

## Current authority change

The existing CF003 survey-implications note is preserved as the earlier pre-authorization checkpoint that said not to add CF-003-specific questions yet. The owner has now explicitly authorized a separate development/secondary module, while retaining the rule that the TN-001 primary questionnaire/endpoint is unchanged.

## Scientific separation

- Astronomical predictor: the published CF-003 seven-factor weighted score surface, chart side only. The repository currently scores seven precomputed binary factor flags; exact historical Mastro factor extraction from raw birth data remains unresolved and must not be claimed reproduced.
- Behavioral target: participant behavior/autobiographical source only, no birth/chart/predictor/astrology labels.
- The behavioral classifier must not receive planet names or the construct-to-planet mapping.
- Main Life Patterns/TN-001 scoring is unchanged; CF-003 outputs cannot rescue or modify it.
- Existing development participants are exploratory only.
- Prospective evidence begins only after the behavioral target contract, mapping, prompts, tie rules, endpoints, null and software hash are frozen before new target responses.

## Behavioral target

Use ten neutral hidden constructs. Nine inherit the chart-blind behavioral role wording already present in reference/core/survey_v2_human_measurement_scoring_contract_v1_0_0.json; add the missing central identity/purpose/self-expression construct.

The participant never sees planet names. The classifier sees neutral construct IDs/definitions only. The evaluator applies the frozen construct-to-planet map only after the behavioral score record is frozen.

Use one common 0-4 dominance rubric for all constructs:
- null/insufficient: source cannot support a defensible rating;
- 0: explicit source indicates the construct is not recurrent/central;
- 1: isolated, situational or explicitly peripheral;
- 2: recurring but narrow/mixed/secondary;
- 3: recurring across multiple contexts or life stages and behaviorally important;
- 4: repeatedly organizing/central across contexts or life stages, with consequential source evidence and no equally strong evidence reducing it to a situational pattern.

Do not reward question count, verbosity, repeated paraphrases, or model confidence. Exact source quotes and counterevidence/conditions are required. Ties remain ties.

## Small secondary question module

After the main behavioral record is frozen, but before any birth/chart reveal, a CF-003 study may ask three concealed-direction questions:
1. central identity/purpose/self-expression across life;
2. which recurring patterns are most organizing/central;
3. which recurring patterns are real but peripheral/situational.

These responses live in a separate secondary-module record. They do not change the primary survey score.

## Endpoints

Per participant, preserve all ties.
Primary: mean behavioral midrank of the CF-003 predictor's top-score set. With a unique predictor top, this is simply that predicted planet's behavioral rank.
Secondary: tie-aware Spearman correlation across all ten planet scores/ranks and inclusive top-3 overlap.

Group null: globally permute the ten construct-to-planet labels using the same permutation across every participant, preserving each participant profile and each construct's marginal distribution. Do not reuse the historical target-shuffle null.

## Implementation

- import the already source-replayed CF-003 predictor scaffold;
- freeze classifier-facing neutral construct contract separately from evaluator-only planet mapping;
- freeze a secondary question module;
- implement pure validation/ranking/comparison helpers;
- implement a chart-blind packet builder that rejects birth/chart target leakage;
- add tests for quote fidelity, completeness, ties, hidden mapping, primary endpoint and global-label permutation semantics;
- do not call Venice/OpenRouter or deploy Railway.

## Acceptance

- CF-003 predictor scaffold tests remain green.
- New target code has deterministic tests.
- classifier-facing contract contains no planet names.
- mapping is never included in classifier packet.
- packet builder rejects birth/chart/chart-score/predictor fields.
- primary TN-001 / Life Patterns scoring files are not modified.
- one cross-family methodology check before calling the target contract a frozen prospective candidate.
