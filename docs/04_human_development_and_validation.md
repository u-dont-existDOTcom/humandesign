# 04 — Human Development and Validation

## Post-hoc fitting is allowed

The project explicitly supports post-hoc model fitting on human DEVELOPMENT data.

This is the easiest and most sensible way to learn:
- which questionnaire items humans can answer reliably;
- which distinctions are actually behaviorally meaningful;
- which HD structures predict which answers;
- which hand-coded mappings are wrong;
- which interactions matter;
- which questions are redundant;
- how much chart signal exists relative to ordinary noise.

The restriction is not “never fit humans.”
The restriction is “never call in-sample fit predictive validation.”

## Human development workflow

For each development participant:
1. collect verified birth tuple first and store it separately;
2. collect questionnaire without exposing chart interpretations where possible;
3. calculate chart deterministically;
4. fit/inspect mappings;
5. perform error analysis;
6. revise the next model version;
7. log every revision.

This pool may be revisited repeatedly.

## Human model families

Implement three comparable tracks.

### A. Theory model
Frozen V4 symbolic mapping.

Question:
Does standard/predeclared HD interpretation recover real birth states?

### B. Empirical model
Learn `P(answer | chart features)` from human development data.

Question:
Does any HD-derived chart information predict human responses, even when hand-coded interpretation is imperfect?

### C. Hybrid model
Use theory mappings as priors/features, then shrink/update them using development humans.

Question:
Does theory help sample efficiency while allowing empirical correction?

## Recommended empirical formulation

For each categorical/ordinal question, estimate a regularized response model from chart features.

Possible feature layers:
- Type/Strategy
- Authority
- Center states
- Profile lines
- Definition
- Channels
- cardinal activations
- selected line/substructure features only when sample size permits

Avoid unconstrained thousands-of-feature conjunction mining.

Candidate score:

```text
log_score(candidate) =
    Σ clusters log P(observed_cluster_response | candidate_chart)
```

Use cluster-level or hierarchical models where answers are dependent.

## Person-level splitting

Never split individual answers from one person across train/test.

All questionnaire responses and chart information for one person belong to exactly one partition.

Use:
- train/development,
- validation,
- untouched test.

For small datasets, nested cross-validation is acceptable for development estimates, but preserve an untouched final set whenever making a substantive public claim.

## Adaptive questionnaire learning

Question selection policy may be learned on development humans:
- expected entropy reduction,
- expected reciprocal-rank improvement,
- cost-adjusted information gain,
- reliability-adjusted information gain.

Freeze the policy before testing on the untouched cohort.

## Prevent trivial leakage

Questionnaire must not ask or encode:
- birthday clues,
- zodiac sign,
- season preferences obviously tied to birthday,
- age-specific events that reveal date,
- school cohort timing,
- holiday birthdays,
- literal astrology/HD chart knowledge.

Keep birthplace/month/year inputs separate from behavioral responses.

## Controls and baselines

Human validation must compare against:
- random/permuted chart assignments;
- candidate-date prior only;
- calendar/season model without HD features;
- demographic baseline if demographics are collected;
- mismatched HD model;
- symbolic V4 model;
- empirical HD model;
- hybrid model.

If an HD model beats chance but not a simple calendar/season baseline, do not claim HD-specific information.

## Validation endpoint

Primary endpoint for known-month tests:
- true local birth day rank among all local days/times in that month.

Secondary:
- top-1 / top-3 / top-5,
- reciprocal rank,
- percentile,
- holdout stability,
- recovered time-window width.

For documented-time tests:
- whether true UTC moment lies inside the predicted stable interval;
- absolute timing error only when a single-point estimator is justified.
