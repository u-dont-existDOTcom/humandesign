# Target-independent chart uniqueness v1 — first owner score

Date: 2026-09-28

## Freeze order

The scoring manifest was committed before the owner score was calculated:
- `reference/research/chart_uniqueness_metric_v1_manifest.json`
- freeze commit: `c1c92b30ca215072505a3282e4776ad7a2dffb3a`

No personality, biography, astrology-belief variable, owner six-rule feature, or owner-selected planet pair enters this metric.

## Metric

The chart is represented by 55 continuous geometry features:
- 45 Sun–Pluto unordered planet-pair distances to the nearest major aspect (0/60/90/120/180);
- 10 distances from each planet to the nearest ASC/MC/DSC/IC angle.

For the participant's birth location, 100,000 random century minutes form the baseline and 50,000 independent random century minutes form the calibration set.

Each feature is transformed by its baseline empirical CDF to a standard-normal marginal. The primary score is a 10%-shrunk Mahalanobis distance in the full 55-dimensional space. Final rarity is the empirical percentile against the untouched calibration sample.

Secondary frozen scores use the 45 planetary features alone, the 10 angular features alone, and mean marginal two-sided surprisal.

## Owner result

Recorded chart: 1985-01-29 10:25 UTC, Philadelphia.

| Frozen score | Rarity percentile | Upper-tail probability | Rarity bits |
|---|---:|---:|---:|
| Primary full 55D geometry | **63.75%** | 36.25% | 1.46 |
| Planetary-only 45D | **65.99%** | 34.01% | 1.56 |
| Angle-only 10D | **55.79%** | 44.21% | 1.18 |
| Mean marginal surprisal | **48.86%** | 51.14% | 0.97 |

The owner chart is therefore **not globally unusual under this first target-independent all-geometry metric**. It is modestly above the median on the multivariate geometry score, not an extreme outlier.

## Why this differs from the earlier results

This does not contradict the earlier findings; it separates three different concepts that had been getting conflated:

1. **Aspect concentration / "loudness".** The owner has an unusually dense collection of tight major aspects. In the prior 10,000-chart benchmark, the 3-degree exactness index was exceeded by only ~2.3% of random charts, and the joint 1°/2°/3° tight-count thresholds by ~1.48%.

2. **Owner-fitted six-rule structural specificity.** The V1.4d target-aware six-rule conjunction occurs at only 9 of 52,596,001 century minute positions. That is extremely rare, but the six rules were selected on the owner and cannot serve as a target-independent chart-uniqueness measure.

3. **Global chart-geometry rarity.** The new frozen v1 metric asks whether the entire 55-feature geometry is unusual relative to ordinary charts. On this measure the owner is around the 64th percentile.

A chart can therefore have a conspicuous cluster of tight aspects without being globally far from the ordinary manifold of planetary/angle geometry. Many of the owner's tight aspects arise from one correlated multi-planet configuration; a covariance-aware metric correctly avoids treating every resulting pairwise aspect as independent evidence of rarity.

## Scientific consequence

The "unique person -> globally unique chart" hypothesis remains testable, but the owner is **not** a motivating positive data point under the frozen primary chart-uniqueness metric.

A different, narrower hypothesis remains motivated:
- psychologically distinctive people may have more **concentrated/exact/salient** charts rather than globally rare charts.

That should be treated as a separate preregistered chart variable (aspect concentration) rather than redefining the primary uniqueness metric after seeing this result.

## Astrology engagement as a selection variable

The observation that people who go deeply into astrology may themselves be atypical is plausible as a selection hypothesis, but it must not enter the chart-rarity score.

For future participants, measure astrology engagement before chart feedback on a frozen ordinal ladder such as:
- 0: no interest / no meaningful familiarity;
- 1: casual sun-sign familiarity;
- 2: has looked at a natal chart / knows several placements;
- 3: regularly uses houses/aspects/transits or comparable techniques;
- 4: sustained technical study/practice/research.

Also collect a direct belief-strength item separately from technical engagement.

Then test three distinct relationships:
1. personality uniqueness -> astrology engagement;
2. target-independent chart uniqueness -> astrology engagement;
3. chart aspect-concentration/salience -> astrology engagement.

If relationship 1 exists, astrology communities will be personality-selected even if charts have no effect. If 2 or 3 predicts engagement after accounting for personality uniqueness, that would be a different and more interesting result. Recruitment must include non-astrology participants; an astrology-forum sample cannot estimate these population relationships.

## Runtime

Feature generation for the 150,000 reference/calibration charts took 18.75 seconds on the current host. The full scoring process including rank transforms/covariance took about 46 seconds wall time.

## Files

- `reference/research/chart_uniqueness_metric_v1_manifest.json`
- `scripts/compute_chart_uniqueness_v1.py`
- `experiments/astrohd/chart_uniqueness_v1_owner_20260928.json`
