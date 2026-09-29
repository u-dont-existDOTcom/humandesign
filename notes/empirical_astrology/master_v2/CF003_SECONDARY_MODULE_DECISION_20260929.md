# CF-003 secondary behavioral-target decision

Date: 2026-09-29
Status: owner-authorized DEVELOPMENT/SECONDARY module; not a primary-endpoint change and not yet a prospective freeze.

## Decision

Add a separate chart-blind CF-003 behavioral-dominance target now.

This supersedes only the earlier recommendation in CF003_SURVEY_IMPLICATIONS_20260929.md that no CF-003-specific module should yet be added. That earlier note remains historical evidence of the pre-authorization state. It is **not** superseded on the following points:

- TN-001 / same-hospital primary endpoint remains unchanged.
- CF-003 does not enter LiteratureModelV1.
- The historical chart-conditioned biographical target is not reused.
- Predictor and target must be frozen separately.
- Existing development participants are exploratory.
- New prospective participants must be untouched by target fitting.
- A held-out replication remains required.

## Why the module is now actionable

The published seven-factor **weighted score surface** is implemented once the seven binary factor flags for each candidate body are supplied. The repository does **not** yet reproduce the exact historical Mastro factor extraction from raw birth data: the source replay explicitly leaves the precise software/settings and factor implementation unresolved. Therefore a future prospective test must either obtain those missing historical conventions or freeze and label a new transparent CF-003 reimplementation of the seven factor flags before target responses. The missing historical target/null data are still not required to develop an independent behavioral target.

The stronger new experiment is:

1. calculate and freeze CF-003 predictor scores/ranks from birth/chart data only;
2. independently freeze a ten-construct behavioral target using chart-blind participant source;
3. only then apply the evaluator-only construct-to-planet map and compare rankings.

The behavioral classifier never receives planet names, chart data, predictor values, or the hidden map. Run it in a fresh tool-free context with no repository, web, Memory, connected apps, or other files available; the frozen classifier packet is its only input.

## Existing measurement coverage

The pre-existing chart-blind survey measurement contract already contains behavioral role definitions corresponding to nine of the ten evaluator categories:

- recurring drive/pressure;
- repeated communication/messages;
- values/boundaries;
- developmental maturation;
- recurring growth principles/opportunity;
- discipline/accountability/consequence;
- unconventional originality;
- mystery/imagination/opacity;
- long-duration transformation/deepening.

The new secondary contract preserves those role texts as lineage on the evaluator side. The missing construct is central identity/purpose/self-expression.

No existing primary scoring contract is edited to add it.

## Small secondary module

The module adds three concealed-direction questions after the main behavioral record is frozen and before birth/chart reveal:

1. an identity/purpose/self-expression question;
2. a cross-pattern centrality question;
3. a peripheral/situational contrast question.

Most evidence should still come from the already-collected autobiographical record. The three questions are not ten planet-by-planet probes and do not expose hidden categories.

The three-question supplement is only a sufficient module when the existing source already provides usable chart-blind coverage for the nine inherited behavioral domains. The new identity question is a coverage repair, not evidence that identity is more dominant. If another construct lacks source, do not score it low merely because it was not asked often enough.

For existing development participants, first classify the existing frozen source. If one or more constructs are insufficient, that target is incomplete unless separately frozen follow-up source is available. Do not impute a missing construct from the chart prediction.

## Frozen behavioral scale

Every neutral construct uses the same 0–4 ordinal dominance rubric:

- null = insufficient;
- 0 = explicit source supports non-recurring/non-central;
- 1 = isolated/situational/peripheral;
- 2 = recurring but narrow/mixed/secondary;
- 3 = recurring across contexts/stages and behaviorally important;
- 4 = repeatedly organizing/central across contexts/stages with consequential source support.

Absence of mention cannot produce 0. Exact source quotations are required. Conditions and counterevidence remain attached. Question count, verbosity and model confidence do not add points. Equal scores remain ties.

This is deliberately coarse to avoid false precision. Calibration or a different continuous score would require a new development version and untouched prospective participants after freeze.

## Endpoints

Primary per-person endpoint:

**mean behavioral midrank of the CF-003 predictor's top-score set.**

If the chart predictor has one unique top planet, this reduces to the simple question: where does that predicted planet rank in the blind behavioral target?

If the predictor ties, every top-tied planet is retained and their behavioral midranks are averaged. No tie-break is invented.

Secondary endpoints:

- tie-aware Spearman rho across all ten scores/ranks;
- inclusive top-3 overlap count;
- inclusive top-3 Jaccard overlap.

## Null

Use a **global label permutation**:

- apply the same permutation of the ten evaluator labels to every participant's behavioral profile;
- preserve each participant's behavioral score vector;
- preserve construct-specific marginal distributions across the cohort;
- recompute the complete group statistic.

This is preferable to independently shuffling finished labels within each participant because the ten behavioral constructs can have different base-rate/measurement distributions.

The historical CF-003 target-shuffle null is not reused.

## Development versus prospective evidence

### Development now

Existing frozen participant records may be scored to debug the target and estimate missingness, ties, measurement balance and clarification burden.

Any apparent CF-003 relationship in those same records is exploratory because the behavioral target was created after those responses existed.

### Prospective later

Before opening new target responses, freeze:

- classifier-facing neutral construct contract;
- classifier prompt/model/version;
- evaluator-only construct-to-planet map;
- secondary question wording;
- quote/source validation rules;
- score/rank/tie rules;
- primary and secondary endpoints;
- permutation algorithm, count and seed;
- CF-003 predictor implementation/spec;
- software commit and hashes.

No post-hoc repair on those participants.

## Files

- reference/empirical_astrology/cf003_published_predictor_spec_v0.json
- reference/empirical_astrology/cf003_behavioral_classifier_contract_v0.json
- reference/empirical_astrology/cf003_behavioral_classifier_prompt_v0.md
- reference/empirical_astrology/cf003_behavioral_planet_map_v0.json
- reference/empirical_astrology/cf003_secondary_question_module_v0.json
- reference/empirical_astrology/cf003_independent_behavioral_target_manifest_v0.json
- src/hdmatch/empirical_astrology/cf003.py
- src/hdmatch/empirical_astrology/cf003_target.py
- scripts/build_cf003_behavioral_packet_v0.py
- scripts/freeze_cf003_behavioral_target_v0.py
- scripts/compare_cf003_frozen_target_v0.py

## Non-goals

- no claim that the published aggregate p-values are calibrated;
- no reproduction of the historical biographical target;
- no modification of TN-001/IPIP-50;
- no modification of Life Patterns primary scoring;
- no chart-conditioned wording;
- no production Railway activation;
- no use of CF-003 to rescue another astrology model.
