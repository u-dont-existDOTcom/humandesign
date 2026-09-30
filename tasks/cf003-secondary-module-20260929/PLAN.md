# CF-003 independent behavioral dominance secondary module

Date: 2026-09-29
Assurance lane: Decision/iteration for a reversible development-secondary research module. This task does not alter the frozen TN-001 primary endpoint, LiteratureModelV1, or the deployed dark Railway participant service.

## Owner outcome

Add a small, independent CF-003 development/secondary module now. Keep the published seven-factor astronomical predictor separate from the human target. Reuse existing rich autobiographical survey material where possible, add a development self-expression/purpose proxy for the missing tenth category, and support a clean prospective test only after predictor, target, classifier and null details are frozen.

## Current authority change

The existing CF003 survey-implications note is preserved as the earlier pre-authorization checkpoint that said not to add CF-003-specific questions yet. The owner has now explicitly authorized a separate development/secondary module, while retaining the rule that the TN-001 primary questionnaire/endpoint is unchanged.

## Scientific separation

- Astronomical predictor: the published CF-003 seven-factor weighted score surface, chart side only. The repository currently scores seven precomputed binary factor flags; exact historical Mastro factor extraction from raw birth data remains unresolved and must not be claimed reproduced.
- Behavioral target: participant behavior/autobiographical source only; no external profile, typology, chart, predictor or hidden-framework context may enter the classifier packet.
- The behavioral classifier must not receive the evaluator map or any framework-identifying schema labels.
- Main Life Patterns/TN-001 scoring is unchanged; CF-003 outputs cannot rescue or modify it.
- Existing development participants are exploratory only.
- Prospective evidence begins only after the target contract, mapping, classifier model/version, balanced source-coverage rule, predictor extraction convention and file commitment, tie rules, endpoints, birth-cohort strata, null seed/count and software hashes are frozen before new target responses.

## Behavioral target

Use ten neutral hidden constructs. Nine retain explicit lineage to behavioral role wording already present in `reference/core/survey_v2_human_measurement_scoring_contract_v1_0_0.json`; the added tenth is a development self-expression/purpose proxy. The mapping is therefore a **combined development hypothesis**, not a reconstruction of the authors' unavailable historical target semantics.

The classifier sees only neutral construct IDs/definitions plus the sanitized behavioral source. The evaluator applies the separate construct-to-planet map only after the behavioral score record is frozen. The literature review may replace the development mapping only in a new version before prospective freeze.

Use one common 0-4 dominance rubric for all constructs:
- null/insufficient: source cannot support a defensible rating;
- 0: explicit source indicates the construct is not recurrent/central;
- 1: isolated, situational or explicitly peripheral;
- 2: recurring but narrow/mixed/secondary;
- 3: recurring across multiple contexts or life stages and behaviorally important;
- 4: repeatedly organizing/central across contexts or life stages, with consequential source evidence and no equally strong evidence reducing it to a situational pattern.

Do not reward question count, verbosity, repeated paraphrases, or model confidence. Exact source quotes and counterevidence/conditions are required. Ties remain ties.

## Small secondary question module

After the main behavioral record is frozen, but before any chart reveal, a CF-003 development study may ask three concealed-direction probes:
1. broad continuity/change across life;
2. recurring patterns that most shape choices/priorities/action;
3. recurring patterns that are real but peripheral/situational.

These questions are a coverage probe, not a complete ten-construct battery. The separate secondary record must be cryptographically linked to the frozen primary record before packet assembly. Post-freeze chart-familiarity/Memory metadata is collection metadata only and never classifier evidence. These responses do not change the primary survey score.

## Endpoints

Per participant, preserve all ties.
Primary: mean behavioral midrank of the CF-003 predictor's top-score set. With a unique predictor top, this is simply that predicted planet's behavioral rank.
Secondary: tie-aware Spearman across all ten ranks, plus fractional top-3 overlap/Jaccard so a tie at the top-3 boundary shares the remaining slot mass rather than expanding the set.

Group null: keep every chart predictor and the evaluator map fixed, then reassign complete frozen behavioral profiles among participants within preregistered birth-cohort strata. Freeze strata, Monte Carlo seed and permutation count prospectively. The old global construct-label permutation remains diagnostic only; simulation showed it can be materially miscalibrated under unequal marginals. Do not reuse the historical target-shuffle null.

## Implementation

- import the already source-replayed CF-003 predictor scaffold;
- freeze classifier-facing neutral construct contract separately from evaluator-only planet mapping;
- freeze a secondary question module;
- implement pure validation/ranking/comparison helpers;
- implement a source-sanitizing packet builder that rejects profile/typology/chart leakage and requires explicit behavioral roles plus primary/secondary linkage;
- freeze predictor scores to a dedicated schema and commit their SHA-256 before behavioral classification;
- add tests for quote fidelity, completeness, leakage, commitment tampering, ties, fractional top-3 behavior, primary endpoint and participant-profile reassignment semantics;
- do not call Venice/OpenRouter or deploy Railway.

## Acceptance

- CF-003 predictor scaffold tests remain green.
- New target code has deterministic tests.
- classifier-facing contract contains no planet names.
- mapping is never included in classifier packet.
- packet builder rejects birth/chart/chart-score/predictor fields.
- primary TN-001 / Life Patterns scoring files are not modified.
- cross-family Opus methodology review completed with **FINDS_ERROR**; the identified defects are repaired and regression-tested, but prospective freeze remains held on the unresolved choices listed above.
