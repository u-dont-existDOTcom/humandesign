# CF-003 secondary behavioral-target decision

Date: 2026-09-29
Status: owner-authorized DEVELOPMENT/SECONDARY module; not a primary-endpoint change and not yet a prospective freeze.

## Decision

Add a separate independent CF-003 behavioral-dominance target now, as a development-only combined hypothesis.

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

1. calculate and freeze CF-003 predictor scores/ranks from the predeclared chart-factor extraction convention;
2. commit that predictor file's SHA-256 before behavioral classification;
3. independently freeze a ten-construct behavioral target from sanitized participant source;
4. only then open the committed predictor and apply the evaluator-only construct-to-planet map.

The behavioral classifier receives only its neutral contract and sanitized behavioral source in a fresh tool-free context. Its packet contains no framework-identifying schema labels, map, predictor, external participant profile, repository, web, Memory, connected apps, or other files. The exact historical Mastro factor extraction remains unresolved and is explicitly preserved as such in the predictor artifact.

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

The evaluator map preserves those role texts as lineage, but the classifier definitions were narrowed after cross-family methodology review to reduce overlap (for example drive versus assertion, values/boundaries versus growth, communication activity versus thought content). The missing tenth category is represented only by a development self-expression/purpose proxy whose definition does not bake in centrality.

These meanings are mainly project/Human-Design-derived development meanings. They are **not** claimed to reconstruct the authors' unavailable historical CF-003 biographical target semantics. No existing primary scoring contract is edited.

## Small secondary module

The module adds three concealed-direction questions after the main behavioral record is frozen and before chart reveal:

1. a broad continuity/change question;
2. a cross-pattern centrality question that explicitly allows important patterns not yet discussed;
3. a peripheral/situational contrast question.

They are deliberately generic rather than direct prompts for one hidden construct. They remain only a development coverage probe, not a guarantee of complete ten-construct measurement. If any construct is insufficient, the target is incomplete; do not improvise a construct-specific follow-up after seeing missingness or predictor information. A balanced follow-up battery must be separately specified and frozen before prospective use.

The secondary record must carry the exact primary-record SHA-256 before packet assembly. Chart-familiarity and ChatGPT-Memory metadata are collected only after the behavioral answers are frozen, as collection metadata that never reaches the classifier.

## Frozen behavioral scale

Every neutral construct uses the same 0–4 ordinal dominance rubric:

- null = insufficient;
- 0 = explicit source supports non-recurring/non-central;
- 1 = isolated/situational/peripheral;
- 2 = recurring but narrow/mixed/secondary;
- 3 = recurring across contexts/stages and behaviorally important;
- 4 = repeatedly organizing/central across contexts/stages with consequential source support.

Absence of mention cannot produce 0. Exact source quotations are required and must contain at least four words; ratings 3-4 require at least two distinct support quotations, while rating 0 requires explicit counterevidence. Reused support quotes are reported rather than multiplied into extra weight. Conditions and counterevidence remain attached. Question count, verbosity and model confidence do not add points. Equal scores remain ties.

This is deliberately coarse to avoid false precision. Calibration or a different continuous score would require a new development version and untouched prospective participants after freeze.

## Endpoints

Primary per-person endpoint:

**mean behavioral midrank of the CF-003 predictor's top-score set.**

If the chart predictor has one unique top planet, this reduces to the simple question: where does that predicted planet rank in the blind behavioral target?

If the predictor ties, every top-tied planet is retained and their behavioral midranks are averaged. No tie-break is invented.

Secondary endpoints:

- tie-aware Spearman rho across all ten ranks; undefined per-person rho remains null rather than imputed;
- fractional top-3 overlap;
- fractional top-3 Jaccard.

A tied group crossing the top-3 boundary shares the remaining membership slots fractionally, so the top-3 endpoint always contains exactly three units of membership.

## Null

Use **complete behavioral-profile reassignment within preregistered birth-cohort strata**:

- keep every chart/predictor fixed;
- keep the evaluator construct-to-planet map fixed;
- reassign each participant's complete frozen behavioral profile to another participant within the same preregistered birth-cohort stratum;
- recompute the cohort primary statistic.

Cross-family review found that the earlier global construct-label permutation changes the semantic map rather than participant pairing. Simulation under independent chart/behavior generation showed false-positive rates as high as 0.133 at nominal 0.05 in tested unequal-marginal scenarios; whole-profile reassignment stayed near nominal. The old label permutation remains diagnostic only. See `tasks/cf003-secondary-module-20260929/NULL-CALIBRATION-20260929.md`.

The historical CF-003 target-shuffle null is not reused.

## Development versus prospective evidence

### Development now

Existing frozen participant records may be scored to debug the target and estimate missingness, ties, measurement balance and clarification burden.

Any apparent CF-003 relationship in those same records is exploratory because the behavioral target was created after those responses existed.

### Prospective later

Before opening new target responses, freeze:

- classifier-facing neutral construct contract and exact classifier model/version;
- evaluator-only construct-to-planet map after the literature-derived mapping decision;
- balanced source-coverage/follow-up rule and secondary question wording;
- quote/source validation rules;
- score/rank/tie rules and undefined-Spearman handling;
- primary and secondary endpoints;
- birth-cohort strata plus permutation algorithm, count and seed;
- CF-003 predictor factor-extraction convention/spec and committed predictor-file hash;
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
- scripts/freeze_cf003_predictor_scores_v0.py
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
