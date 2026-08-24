# 22 — Holistic Whole-Profile Identification and Minimization

## Phase boundary

This module supports both DEVELOPMENT and frozen VALIDATION, but the operations are not interchangeable.

### DEVELOPMENT

Development people may be used repeatedly to:
- fit whole-profile likelihoods;
- inspect failures;
- define or revise feature groups;
- search declared interactions;
- choose matching strata;
- run ablations;
- minimize chart representations;
- tune regularization and complexity.

Cross-validation or matched-decoy performance inside DEVELOPMENT is a search/model-selection instrument, not independent confirmation.

Development evaluation used for model selection should be person-level cross-fitted whenever practical: each reported person's score is produced by a model fitted without that person. Reusing the same DEVELOPMENT population across folds is allowed; it improves development hygiene but does not create an untouched validation set.

### VALIDATION

Validation people may be scored only with a previously frozen model, evidence-tokenization rule, feature schema, matching policy, decoy policy, and analysis. Validation outcomes must not select a new chart representation.

## Why this exists

Sparse archival and real-world biographical datasets often record reliable positive facts but do not record exhaustive negatives. In Astro-Databank, for example, the absence of a personality tag usually means `not annotated`, not `this person definitely lacks the trait`.

A model that converts every missing annotation into a negative answer therefore tests the annotation process as much as the person.

The holistic model instead asks:

> Given the positive behaviors/features actually observed for this person, does their true chart explain that observed set better than matched alternative charts?

Unrecorded behavior is unknown. It is not contradiction.

## Positive-evidence score

For each observed label `y` and chart feature token `x`, the development model estimates a smoothed enrichment ratio:

```text
P(x | y observed) / P(x | all development people)
```

The candidate chart score is the weighted sum of log2 enrichment for the person's observed labels.

No term is added for an unrecorded label.

This is deliberately different from a standard multi-label classifier that scores both presences and absences.

## Dependency control

Dependency control is required on **both sides** of the comparison.

### Chart-feature dependencies

Chart features are assigned to dependency clusters. Contributions within a cluster are averaged before being added.

Examples:
- Type / Authority / Profile core architecture;
- center states;
- channel states;
- gate states;
- declared interaction/substructure families;
- deterministic astronomical families such as Sun/Earth and North/South Node oppositions.

This prevents a representation from appearing stronger merely because the same underlying structure was expanded into many correlated flags.

### Observed-behavior dependencies

Observed positive labels may also be correlated. Multiple labels describing the same behavioral or biographical branch must not be counted as independent confirmation merely because the source taxonomy contains several names for related material.

`cluster_normalized_evidence_weights()` keeps all observed labels available for specificity while capping their total possible contribution within a declared dependency cluster. Reliability may reduce a label's weight but may not inflate the cluster above one independent evidence unit.

The dependency ontology itself is DEVELOPMENT-tunable. It must be frozen before VALIDATION.

## Person-level cross-fitting

`cross_fitted_identification()` is the preferred DEVELOPMENT evaluation path.

For each deterministic fold:

1. Fit the positive-evidence model on all other DEVELOPMENT folds.
2. Score only the held-out people.
3. Rank each held-out person's true chart against their matched decoys.
4. Repeat until every person has an out-of-fold development rank.

Feature-group minimization should likewise use `greedy_cross_fitted_minimize_feature_groups()` rather than fitting and selecting on the same people's scores when the dataset is large enough to support cross-fitting.

Cross-fitting reduces direct in-sample optimism. Repeatedly consulting cross-fitted results while changing the model still makes those data DEVELOPMENT.

## Person-to-chart identification

For each person:

1. Keep their observed behavioral profile fixed.
2. Score the profile against the person's true chart.
3. Score the same profile against charts from other people satisfying the frozen matching strata.
4. Report the true chart percentile/rank among those candidates.

Typical matching strata may include sex, cohort/decade, geography, recruitment source, or other conventional variables that could otherwise make chart identity trivial.

Primary group summaries include:
- mean true-chart percentile;
- median percentile;
- reciprocal rank;
- randomization/permutation result.

## Randomization

The full candidate-score vector is retained for each person.

Under the chart-label null, the designated true chart is exchangeable with another matched candidate. Randomization therefore repeatedly selects a candidate from each person's frozen score vector and compares the null mean percentile with the observed true-chart mean.

This tests chart identity rather than relying on a nominal parametric p-value.

When the analysis **selects** among chart representations, feature groups, carrier subsets, matching rules, interaction structures, thresholds, or other model variants, the relevant null must rerun that entire selection procedure. A p-value for the final chosen subset alone does not account for development search.

## Minimization

Once a whole-chart signal exists on DEVELOPMENT data, minimize it by feature group.

Start with the declared full representation and repeatedly remove the feature group whose removal harms person-to-chart identification least, or exhaustively enumerate the declared low-dimensional subset space when computationally cheap.

Stop when the next removal would exceed a predeclared tolerance, and/or report the complete complexity/performance frontier.

Report the full ablation path or subset frontier, not only the winning subset.

The purpose is to distinguish:
- indispensable core;
- substitutable representations;
- redundant symbolic expansion;
- candidate raw/minimal mathematical object.

Do not use VALIDATION people to choose the minimized representation.

## Recommended progression

```text
whole chart
→ whole-profile positive-evidence identification
→ person-level cross-fitting
→ dependency-controlled ablation / subset frontier
→ full-selection permutation null
→ compact HD representation
→ raw astronomical compression
→ frozen external validation
```

Marginal one-feature/one-trait tests remain useful diagnostics and falsifications. They are not assumed to be equivalent to the whole-profile question.

## Synthetic acceptance tests

The implementation must demonstrate that:
- an injected whole-profile law ranks true charts above decoys;
- unrecorded labels contribute zero evidence;
- duplicate chart features in one dependency cluster cannot multiply support;
- correlated observed labels can share one dependency-cluster evidence unit;
- matched-decoy strata are enforced;
- cross-fitted development scoring does not train on the person it reports;
- minimization removes known noninformative groups while preserving injected signal.
