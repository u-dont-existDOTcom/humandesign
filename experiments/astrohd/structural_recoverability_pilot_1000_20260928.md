# Structural recoverability pilot — 1,000 random century charts

Date: 2026-09-28

## Scope

This is a direct computational pilot using the current V1.4d six-rule model, not the legacy V3.6 model.

- 1,000 distinct minute-grid moments sampled uniformly from the current century universe:
  1926-08-24 10:42 UTC through 2026-08-24 10:42 UTC.
- RNG: PCG64, seed 20260928.
- Exact chart snapshots: Swiss Ephemeris file-backed calculations.
- Location: Philadelphia, PA (39.9526, -75.1652).
- Each chart is represented by the six frozen V1.4d rule booleans, giving at most 64 signatures.
- The script also recomputes the ten-planet major-aspect tightness metrics used in the prior 10,000-chart benchmark.

## Runtime

The 1,000-chart exact pilot took **0.930 seconds of measured compute time** (about **1.35 seconds wall time** including process startup/output), or **1,075 charts/second**.

A naive full 52,596,001-minute extrapolation of this exact per-chart pipeline would be about **13.6 hours on one process**.

That is not the best way to compute six-rule structural recoverability. The already-optimized V1.4d exact minute-grid evaluator processed the entire 52,596,001-minute century in **132.206 seconds** for the maximum-score search. Adapting that optimized scan to accumulate all 64 signature counts should therefore be expected to take minutes rather than 13.6 hours. A full ten-planet geometry record at every minute is a separate, more expensive task and is not required to measure six-rule signature rarity.

## Six-rule signature distribution

The pilot observed **31 of 64 possible signatures**.

The most common signatures were:
- signature 0: 430/1000 = 43.0%
- signature 32: 167/1000 = 16.7%
- signature 1: 103/1000 = 10.3%
- signature 4: 97/1000 = 9.7%
- signature 8: 55/1000 = 5.5%

Eleven observed signatures occurred only once in the 1,000-chart sample.

For a random sampled chart, plug-in self-information based on the pilot signature frequency had:
- mean: **2.80 bits**
- median: **2.58 bits**
- 90th percentile: **5.16 bits**
- 95th percentile: **6.80 bits**
- sample maximum: **9.97 bits** (one occurrence in 1,000)

These are pilot estimates. A 1,000-chart sample cannot accurately estimate extremely rare signatures.

## Owner comparison

The recorded owner chart (1985-01-29 10:25 UTC) has all six V1.4d conditions active:
- rule values: [1,1,1,1,1,1]
- packed signature: 63

**Signature 63 appeared 0 times among the 1,000 random charts.**

The existing exhaustive V1.4d century scan provides much stronger information for this particular signature: score 6 / all six conditions occurs at only **9 of 52,596,001 minute-grid moments**, all on 1985-01-29 from 10:18 through 10:26 UTC.

That frequency is approximately **1.71e-7**, corresponding descriptively to **22.48 bits** of minute-grid self-information: log2(52,596,001 / 9).

This does not validate the behavioral mapping. The six-rule model was target-aware fitted on the known owner case. It does show that the final owner rule conjunction is astronomically very rare within the frozen century search.

## Geometry sanity check

The pilot independently reproduced the owner geometry:
- major aspects <=1 degree: 4
- <=2 degrees: 9
- <=3 degrees: 11
- 3-degree exactness index: 18.90985

Pilot means/medians were approximately:
- <=1 degree: mean 2.03, median 2
- <=2 degrees: mean 3.99, median 4
- <=3 degrees: mean 5.99, median 6
- exactness index: mean 9.00, median 8.45

This is consistent with the prior 10,000-chart benchmark.

## Interpretation

The pilot confirms that **structural recoverability is highly heterogeneous under the six-rule model**. Some signatures are common enough to cover a large fraction of century moments; others are rare even in 1,000 random samples. The owner signature is far beyond the resolution of this pilot and is already known from the exhaustive target scan to be exceptionally rare.

This supports a testable prospective hypothesis: chart signatures that are rare *before behavioral outcomes are examined* may be easier to recover from accurate behavioral labels than common signatures. That hypothesis still requires untouched participants. Rarity alone does not establish that the behavioral labels correspond to astrology.

## Files

- `scripts/pilot_structural_recoverability_1000.py`
- `experiments/astrohd/structural_recoverability_pilot_1000_20260928.json`
- prior 10,000-chart geometry benchmark: `experiments/astrohd/owner_orb_tightness_10k_20260928.md`
