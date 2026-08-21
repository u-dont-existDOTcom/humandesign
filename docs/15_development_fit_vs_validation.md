# 15 — Post-Hoc Human Fitting vs Validation

## Core rule

Post-hoc fitting is not a flaw. It is model development.

The flaw is using the same fitted cases as if they were an untouched test of prediction.

## Recommended loop

```text
known development humans
→ inspect errors
→ revise questions/mappings/model
→ refit
→ internal validation
→ freeze version
→ untouched humans
→ evaluate once
```

If the untouched result motivates redesign, increment the model version and obtain another untouched cohort for the next final test.

## What may be learned post hoc

- question wording;
- response coding;
- construct boundaries;
- chart-feature mappings;
- likelihoods;
- interaction terms;
- question order;
- adaptive selection policy;
- reliability model;
- model complexity/regularization.

## What must remain protected

- final untouched participant labels;
- hidden birth-day/time during prospective recovery;
- answer keys during blind synthetic runs.

## Generalization criterion

A useful rule is one that repairs or improves predictions across multiple people and continues to work on new people, not a one-person exception added solely to rescue one known chart.
