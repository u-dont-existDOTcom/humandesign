# 11 — Empirical Learning Track

## Rationale

Post-hoc fitting to known humans is standard model development.

The project's current V4 protocol already anticipates replacing symbolic rarity weights with empirical behavioral likelihoods. This workstream operationalizes that idea.

## Two complementary questions

### Theory-validation question
Does the predeclared HD interpretation predict people?

Use frozen symbolic mappings.

### Signal-discovery question
Do birth-derived HD chart features predict people even if traditional descriptions are imperfect?

Learn mappings from development humans.

The second can succeed even if the first fails.

## Generative decoder

Preferred first empirical model:

For each question/cluster `q`, estimate:

```text
P(response_q | chart_features)
```

Then for candidate chart `c`:

```text
log_likelihood(c)
  = Σ_q reliability_q * log P(response_q | features(c))
```

Normalize across the candidate universe only for ranking unless probability calibration has been validated.

## Why generative is attractive
- directly supports candidate search;
- naturally supports missing answers;
- naturally supports adaptive question selection;
- can expose which questions discriminate;
- can be regularized at each structural layer.

## Modeling progression

Start simple:
1. Type/Authority/Profile/Centers;
2. add channels;
3. add cardinal gates/lines;
4. add selected lower-salience activations only if sample size supports them;
5. add interactions using shrinkage and explicit validation.

Do not jump to arbitrary exact-chart memorization.

## Regularization
Use one or more:
- hierarchical Bayesian partial pooling;
- L1/L2-regularized multinomial/ordinal regression;
- target-encoded models with nested CV;
- gradient boosting only with careful held-out tuning.

Rare structures must shrink toward broader parent estimates.

## Human questionnaire refinement

On development humans it is legitimate to:
- add questions where chart states predict divergent behavior;
- remove ambiguous questions;
- split conflated questions;
- revise wording;
- change response formats;
- discover counterexamples;
- learn measurement reliability.

Every such change increments questionnaire/model version.

## Avoiding the “fit anything” trap

A sufficiently flexible model can memorize development humans.

Controls:
- person-level nested validation;
- regularization;
- complexity penalties;
- predeclared candidate universe;
- chart-assignment permutation;
- non-HD calendar baselines;
- untouched final cohort.

The objective is not maximum training accuracy.
It is maximum out-of-sample birth-state recovery.

## Model comparison

Freeze several candidate models and compare on validation:
- symbolic;
- empirical-simple;
- empirical-expanded;
- hybrid.

Select once, then test the winner on untouched humans.

## Learning curve

Always plot/record performance versus number of training humans.

If performance rises with more data and persists out of sample, that supports a learnable signal.
If training accuracy rises while validation remains at chance, the model is overfitting.
