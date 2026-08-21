# 10 — Metrics

## Rank metrics
For every concealed case:
- true date rank;
- true state rank;
- top-1;
- top-3;
- top-5;
- mean reciprocal rank;
- percentile;
- rank margin to runner-up.

## Timing
- stable predicted interval width;
- whether true time lies inside top predicted interval;
- nearest-boundary error;
- absolute time error only when a point estimate is justified.

## Information acquisition
- rank after each restored dependency cluster;
- rank after each active question;
- questions/clusters required to reach top-k;
- entropy of candidate distribution;
- information gain per question.

## Robustness
- confidence/reliability perturbations;
- leave-one-cluster-out;
- mapping variants;
- question-order permutations;
- missingness;
- answer noise;
- date aggregation variants.

## Human baselines
Compare:
1. chance/permutation;
2. date prior;
3. month/season features;
4. demographics, if collected;
5. mismatched HD;
6. symbolic V4;
7. empirical HD;
8. hybrid HD.

## Statistical testing
For human validation use empirical permutation tests wherever feasible:
- shuffle chart assignments across people subject to the same candidate-universe constraints;
- rerun the full decoding metric;
- compare observed top-k/MRR/rank statistics with null distribution.

Correct for repeated model comparisons when choosing among many model families.

## Calibration
Do not call rank-derived scores probabilities until validated probability calibration exists.
Rubric bits remain rubric bits.
