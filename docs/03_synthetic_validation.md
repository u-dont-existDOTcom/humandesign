# 03 — Synthetic Validation

## Purpose

Synthetic testing validates the decoder, search engine, adaptive questioning, information accounting, blinding, and robustness machinery.

It does NOT validate Human Design in humans.

## Generator

Synthetic answers MUST be generated from the same frozen mapping library used by the decoder.

Pipeline:

```text
hidden local birth tuple
        ↓
historical timezone → UTC
        ↓
exact HD chart state
        ↓
frozen mapping library
        ↓
canonical response distribution
        ↓
declared noise model
        ↓
blind questionnaire response record
```

No free-form chart-inspired biographies in the core benchmark.

## Difficulty tiers

### Oracle
- canonical response whenever mapping is diagnostic;
- unknown when construct is not predicted;
- no random error;
- reliability 1.0.

### Low noise
- small predefined answer noise;
- modest unknown rate;
- mild confidence variability.

### Medium noise
- contextual answers;
- missingness;
- correlated/redundant signals;
- moderate reliability loss.

### Adversarial
- higher missingness;
- misleading but model-legal responses;
- domain-specific reliability degradation;
- near-neighbor candidate charts.

Noise is seeded and chart-independent except where the declared simulator explicitly conditions on a measurement domain.

## Blindness

Generator creates:
- `blind_cases.json`
- `answer_key.json.enc`

The decoder gets only the blind file.
The key is encrypted or stored outside the project/workspace.

The prediction file is hashed before decryption/reveal.

## Candidate universes

Implement:
1. known month/year;
2. known year;
3. known local date;
4. bounded multi-year;
5. 100-year UTC.

A date is not represented by a single noon/midnight chart.
Search all exact state intervals intersecting the local day.

## Date aggregation

Do not use only the maximum-scoring minute.

Support at minimum:
- best-state score,
- duration-weighted mean score,
- duration-weighted log-likelihood/evidence integration,
- proportion of day above declared score thresholds.

Make aggregation rule explicit and frozen per experiment.

## Restoration and ablation

For each case record:
- rank with zero response clusters;
- rank after each randomly restored independent cluster;
- rank after each actively selected cluster;
- final rank;
- leave-one-cluster-out rank.

The active selector must not know the hidden answer.
It chooses the next question by expected information gain over the current candidate distribution.

## Optimization

Development synthetic cases may be used aggressively to optimize:
- decoder formulas,
- dependency handling,
- date aggregation,
- adaptive question selection,
- questionnaire length,
- caching/search algorithms.

Then freeze and evaluate on newly generated untouched synthetic cases with a new seed.
