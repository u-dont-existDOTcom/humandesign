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

Features are assigned to dependency clusters. Contributions within a cluster are averaged before being added.

Examples:
- Type / Authority / Profile core architecture;
- center states;
- channel states;
- gate states;
- declared interaction/substructure families.

This prevents a representation from appearing stronger merely because the same underlying structure was expanded into many correlated flags.

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

## Minimization

Once a whole-chart signal exists on DEVELOPMENT data, minimize it by feature group.

Start with the declared full representation and repeatedly remove the feature group whose removal harms person-to-chart identification least.

Stop when the next removal would exceed a predeclared tolerance.

Report the full ablation path, not only the winning subset.

The purpose is to distinguish:
- indispensable core;
- substitutable representations;
- redundant symbolic expansion;
- candidate raw/minimal mathematical object.

Do not use VALIDATION people to choose the minimized representation.

## Recommended progression

```text
whole chart
→ whole-profile identification
→ dependency-controlled ablation
→ compact HD representation
→ raw astronomical compression
→ frozen external validation
```

Marginal one-feature/one-trait tests remain useful diagnostics and falsifications. They are not assumed to be equivalent to the whole-profile question.

## Synthetic acceptance tests

The implementation must demonstrate that:
- an injected whole-profile law ranks true charts above decoys;
- unrecorded labels contribute zero evidence;
- duplicate features in one dependency cluster cannot multiply support;
- matched-decoy strata are enforced;
- minimization removes known noninformative groups while preserving injected signal.
