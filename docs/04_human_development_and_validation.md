# 04 — Human Development and Validation

## Epistemic phase router

Before applying any freeze, holdout, preregistration, anti-overfitting, post-hoc, leakage, or model-selection rule, classify each material dataset or partition by its **current use**:

- `PHASE: DEVELOPMENT` — the data may influence hypotheses, chart representations, mathematical formulas, target definitions, preprocessing, feature selection, thresholds, hyperparameters, questionnaire design, or analysis choices. These data are for learning and may be optimized aggressively, but they cannot independently confirm generalization.
- `PHASE: VALIDATION` — the data are reserved to test a hypothesis/model/analysis package frozen before their outcomes are inspected. These data may support or refute generalization, but they may not influence the model while retaining the validation label.

Use the two-question checksum:

1. **May these data influence the hypothesis/model?**
2. **May these data support the claim that the resulting hypothesis/model generalizes?**

Development is normally `YES / NO`. Validation is normally `NO / YES`. If a validation result is inspected and then used to change the formula, target, threshold, preprocessing, controls, or analysis, those data become development data for subsequent claims and a new independent validation set is required.

Validation safeguards must not be applied indiscriminately to development. Cross-validation repeatedly consulted during development is a model-selection/search tool, not independent confirmation. If a genuinely independent future dataset is available or planned for confirmation, do not weaken discovery merely to preserve ceremonial internal untouchedness.

Core invariant: **freeze before VALIDATION, not before DISCOVERY. Do not optimize VALIDATION cases. Optimize DEVELOPMENT cases aggressively.**

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

Development may also include broad mathematical discovery beyond traditional HD representations: raw astronomical variables, harmonics, pairwise phases, alternative prenatal anchors, alternative lattices, symbolic regression, interactions, ablations, and other compact representations. Searching these post hoc is legitimate on development data. The scientific firewall is the later frozen test on genuinely independent validation data.

## Human development workflow

For each development participant:
1. collect verified birth tuple first and store it separately;
2. collect questionnaire without exposing chart interpretations where possible;
3. calculate chart deterministically;
4. fit/inspect mappings and candidate mathematical representations;
5. perform error analysis, ablation, stability checks, and repeated cross-validation as useful for model selection;
6. revise the next model version;
7. log every revision and label resulting claims development-selected.

This pool may be revisited repeatedly. No number of revisits invalidates its use for discovery; repeated reuse only means it cannot later be relabeled untouched validation.

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

A fourth discovery track may search compact raw astronomical representations directly. It remains development until a frozen formula is tested on independent data.

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

For unrestricted development discovery, a wider raw-astronomy grammar is allowed. Complexity penalties, internal cross-validation, stability selection, permutations, and null searches are used to rank candidates and avoid wasting external validation on obvious noise; they do not convert development performance into confirmatory evidence.

Candidate score:

```text
log_score(candidate) =
    Σ clusters log P(observed_cluster_response | candidate_chart)
```

Use cluster-level or hierarchical models where answers are dependent.

## Person-level splitting

Never split individual answers from one person across train/test when estimating person-level generalization.

All questionnaire responses and chart information for one person belong to exactly one partition within a particular resampling split.

Development may use repeated person-level cross-validation, bootstrap resampling, or nested cross-validation for search and model selection. A partition consulted during iterative model development is still development data.

For confirmatory claims, use a genuinely untouched validation dataset or partition whose outcomes did not influence model selection. Preserve an untouched final set when it is the only available independent confirmation source; do not confuse that requirement with a ban on exploiting the designated development pool fully.

## Adaptive questionnaire learning

Question selection policy may be learned on development humans:
- expected entropy reduction,
- expected reciprocal-rank improvement,
- cost-adjusted information gain,
- reliability-adjusted information gain.

Freeze the policy before testing on the untouched validation cohort.

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

Leakage prevention remains mandatory in both phases. Phase routing permits exploratory fitting; it does not permit accidental answer-key leakage or using a variable that trivially encodes the target.

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

Development should also use these controls where useful for candidate ranking. A discovery formula that only recovers season, geography, cohort, profession, or another ordinary confounder is a poor candidate for external validation.

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
