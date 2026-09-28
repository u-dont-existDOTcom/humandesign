# V1.4d six-rule structural recoverability — 1,000,000-chart century sample

Date: 2026-09-28

## Why this is a sample rather than a new exhaustive scan

A 1,000,000-minute benchmark of the exact all-six-bit evaluator took 19.59 seconds with six workers. That implies roughly 15–18 minutes for all 52,596,001 minutes on the current 8-core host. The prior 132-second exhaustive run was faster because it short-circuited as soon as a necessary rule failed; it did not calculate every rule bit for every minute.

Because the user asked to proceed only if the full calculation was quick, the full all-signature scan was not run. Instead, 1,000,000 exact minute-grid positions were sampled uniformly across the full century. This is enough to estimate common and moderately rare signature frequencies precisely. The owner's 6/6 signature already has an exact full-century count from the previous exhaustive maximum-score scan.

## Method

- Universe: 52,596,001 UTC minute positions from 1926-08-24 10:42 through 2026-08-24 10:42.
- Sample: 1,000,000 draws uniformly with replacement across the minute grid.
- Seed: 20260928.
- Location: Philadelphia, PA.
- Exact Swiss-Ephemeris-backed V1.4d rule evaluation.
- Eight worker processes.
- Runtime: 28.73 seconds for the random sample.
- All six Boolean rule values were evaluated for every sampled chart.

## Distribution

59 of the 64 possible signatures appeared at least once.

The four most common signatures alone account for **80.9499%** of sampled birth moments:
- signature 0: 44.0121%
- signature 32: 15.8173%
- signature 1: 10.5789%
- signature 4: 10.5416%

Five signatures were not observed: 27, 30, 31, 59, and 63.

The Shannon entropy of the sampled six-rule signature distribution is **2.772 bits**, far below the theoretical six-bit maximum because the signatures are very unevenly distributed.

For a randomly selected chart, plug-in signature self-information has approximately:
- median: 2.66 bits
- 75th percentile: 3.25 bits
- 90th percentile: 5.23 bits
- 95th percentile: 6.63 bits
- 99th percentile: 9.32 bits
- 99.9th percentile: 12.52 bits

Only **4.6585%** of sampled moments belong to signatures occurring <=1% of the time.
Only **0.5935%** belong to signatures occurring <=0.1% of the time.
Only **0.0577%** belong to signatures occurring <=0.01% of the time.

## Owner signature

The owner chart has signature 63: all six rules active.

Signature 63 appeared **0 times in the 1,000,000 random sample**. This is expected given the exact prior exhaustive result: signature 63 / score 6 occurs at only **9 of 52,596,001** minute-grid moments, all on 1985-01-29 from 10:18 through 10:26 UTC.

Exact owner-signature frequency:
- 9 / 52,596,001 = 1.711e-7
- about 1 occurrence per 5.84 million minute positions
- descriptive self-information = **22.48 bits**

At that true frequency, a one-million-draw random sample expects only 0.171 occurrences; the probability of observing zero is about 84.3%. Therefore the zero count in the new sample is consistent with the exact exhaustive owner result.

## Interpretation

Under this fixed six-rule geometry, structural specificity is strongly heterogeneous. Most birth moments fall into a few common signatures, while a small fraction fall into much rarer combinations. The owner signature is exceptionally rare within this fitted model.

This supports the *possibility* that some DOBs can be structurally much easier to identify than others. It does not establish behavioral recoverability, because a rare astronomical signature is useful only if behavioral measurements reliably identify the corresponding rule states.

A further limitation is crucial: V1.4d's six rules were target-aware selected on the owner development case. The owner cannot be used to validate the proposition that rare signatures predict easier recovery. That proposition must be frozen and tested prospectively on untouched people. A future general method also needs a target-independent rule-selection policy; otherwise each person's post-hoc selected signature rarity is not comparable.

## Files

- `scripts/count_astrohd_v14_six_rule_signatures.py`
- `scripts/sample_astrohd_v14_six_rule_signatures_1m.py`
- `experiments/astrohd/six_rule_signature_benchmark_1m_20260928.json`
- `experiments/astrohd/six_rule_signature_random_1m_20260928.json`
- prior exact owner result: `experiments/astrohd/v14_exact_century_20260925/result.json`
