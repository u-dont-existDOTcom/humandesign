# Partner Hard-Decoy Residual Benchmark V3 — Frozen Specification

Status: development / exploratory.

Freeze date: 2026-08-26.

This benchmark is frozen before inspecting its Joel/Bee rank results.

## Research question

Does the Joel/Bee pair show unusually strong **pair-specific dynamic relationship activation** after controlling for the fact that each person may independently be in a relationship-active period?

This is a Track T / relationship-transition test. It is **not** a relationship-quality test and does not estimate whether being together would be good for either person.

## Astronomy

- Tropical, geocentric Western positions.
- Verified Swiss Ephemeris `.se1` only; any Moshier fallback aborts.
- Secondary progressions use one ephemeris day per tropical year of life (365.2422 days).
- Monthly evaluation grid: 15th of each month, 12:00 UTC.
- Horizon: January 2026 through December 2040 inclusive.

## Known data

Person A:
- 1985-01-29T10:25:00Z, Philadelphia chart treated as exact.

Person B:
- 1989-06-19, Cameroon;
- exact time unknown;
- carry three previously declared representative states:
  - early 05:00 UTC;
  - mid 12:00 UTC;
  - late 17:00 UTC;
- never choose a B state because it ranks better.

## Hard-decoy selection

Run the benchmark reciprocally.

### A → B direction

1. Generate 5,000 random candidate partner birth moments uniformly from 1984-06-19 through 1994-06-19.
2. For each B time state separately, calculate the frozen V2 four-domain individual future-state vector (`relationship`, `economy`, `home_community`, `work_purpose`).
3. Calculate the same individual vector for every candidate.
4. Hard-match by the mean cosine similarity across the four domains to that B state.
5. Retain the 1,000 nearest candidate timelines as the null risk set.
6. No pair-specific information may influence hard-decoy selection.

### B → A direction

1. Generate 5,000 random candidate partner birth moments uniformly from 1980-01-29 through 1990-01-29.
2. Hard-match every candidate to A's four-domain individual future-state vector using the same rule.
3. Retain the 1,000 nearest candidates.
4. Use the same retained risk set for every B time state.

Random seed: `202608260043`.

## Primary Western pair-specific dynamic score

The primary score deliberately excludes static synastry and excludes individual transit similarity because hard matching is intended to control those individual trajectories.

For each month calculate three pair-specific activation families:

1. **pA→nB** — progressed A personal planets to B natal relationship planets;
2. **pB→nA** — progressed B personal planets to A natal relationship planets;
3. **pA→pB** — progressed personal planets of A to progressed personal planets of B.

Moving personal planets:

```text
Sun, Moon, Venus, Mars
```

Natal targets:

```text
Sun, Moon, Venus, Mars, Saturn
```

For pA→pB, use all cross-pairs among Sun/Moon/Venus/Mars.

Major aspects are activation markers rather than quality markers:

```text
0°, 60°, 90°, 120°, 180°
```

All five aspects receive equal activation weight in V3.

Aspect exactness kernel:

```text
exp(-0.5 * (residual_deg / sigma)^2)
```

Sigma:

- progressed Moon moving: 1.5°;
- other progressed moving planets: 1.0°.

For each family/month take the maximum kernel across its allowed planet-pair/aspect combinations.

Monthly Western pair activation:

```text
mean(pA_to_nB, pB_to_nA, pA_to_pB)
```

This arithmetic mean preserves directional asymmetry rather than requiring both directions to be simultaneously exact.

### Temporal transition score

Relationships can form during concentrated windows rather than from a high 15-year average.

For the monthly Western pair-activation series calculate:

```text
peak12 = maximum 12-month rolling mean
peak24 = maximum 24-month rolling mean
western_pair_dynamic = 0.60 * peak12 + 0.40 * peak24
```

Also report the start month of the winning 12- and 24-month windows.

## Human Design corroboration

HD remains a separate system but is included in an equal-standardized joint exploratory score.

At each month overlay the frozen slow transits used in the earlier partner pilot onto the pair connection chart.

Monthly HD state score:

```text
0.5 * I(connection is Single Definition)
+ 0.5 * I(connection has exactly 8 defined Centers / 8+1)
```

Do **not** include Gate 21-45 or any other specific channel in the primary HD score because that feature was noticed in Joel/Bee before V3 and would be pair-targeted overfitting.

Temporal HD score:

```text
hd_peak12 = maximum 12-month rolling mean
hd_peak24 = maximum 24-month rolling mean
hd_pair_dynamic = 0.60 * hd_peak12 + 0.40 * hd_peak24
```

## Joint exploratory score

Within each hard-decoy risk set:

```text
z_west = z-score(western_pair_dynamic)
z_hd   = z-score(hd_pair_dynamic)
joint_residual_v3 = mean(z_west, z_hd)
```

Rank the real pair against the 1,000 hard decoys.

Report Western, HD, and joint ranks separately.

## Interpretation thresholds

Per direction:

- ≥95th percentile: strong exploratory signal;
- ≥99th percentile: striking exploratory signal;
- 80–95th: modest signal;
- 20–80th: ordinary/null-range;
- <20th: below-null concordance.

A strong pair-specific finding requires **≥95th percentile joint rank in both reciprocal directions** for at least one B state without selecting that state post hoc.

Because B's time is unknown, the strongest robust claim requires ≥95th in all materially plausible B states. A single-state hit is conditional only.

## Preserved limitations

- This is not trained on historical transition outcomes.
- Pair-activation rules are symbolic/practitioner-derived, not calibrated probabilities.
- Exact relationship geography is absent.
- Static synastry attraction is intentionally excluded from the primary score.
- Relationship quality is intentionally excluded.
- The previously discussed 2030 window is not a blind timing discovery; V3's valid new information is the **hard-decoy rank**, not whether 2030 appears again.

## Stopping rule

Run once with this frozen specification. Preserve the result whether positive or negative. Any changed aspect set, weights, body list, hard-match pool, or temporal aggregation creates V4 and requires a new null pool.
