# Partner Future-Concordance 1,000-Partner Null Benchmark V1

Status: **development / exploratory**. Freeze before observing null ranks.

Freeze date: 2026-08-25.

Protocol parent: `docs/19_partner_future_concordance.md`.

## Question

How unusual is the Joel-Bee future timing/relationship structure compared with age-matched random potential partners, in both directions?

This is not a soulmate probability. It is a development null benchmark.

## Null pools

### Joel -> random women

- N = 1,000.
- Uniform random UTC birth moments from `1984-06-19T00:00:00Z` through `1994-06-19T00:00:00Z`.
- This is +/- 5 years around Bee's birth date.
- Sex is a demographic label only; astrology/HD calculations do not use sex.

### Bee -> random men

- N = 1,000.
- Uniform random UTC birth moments from `1980-01-29T00:00:00Z` through `1990-01-29T00:00:00Z`.
- This is +/- 5 years around Joel's birth date.
- Sex is a demographic label only.

Random seed: `202608252037`.

## Fairness under Bee's unknown birth time

Bee is carried as three predeclared representative Cameroon-day states:

- B_early: 1989-06-19T05:00:00Z;
- B_mid: 1989-06-19T12:00:00Z;
- B_late: 1989-06-19T17:00:00Z.

Report ranks for all three. The conservative pair result is the worst rank/percentile across the three states. Do not choose the state that ranks best.

Houses, angles, progressed angles, and astrocartography are EXCLUDED from this benchmark for everyone because Bee's exact birth time is unresolved. This deliberately sacrifices information from Joel's known time to keep the null comparison symmetric.

## Forecast horizon and resolution

- 2026-01 through 2040-12 inclusive.
- One snapshot at the 15th of each calendar month at 12:00 UTC.
- Verified SWIEPH only; Moshier fallback aborts the run.

## Western raw-timing concordance metric

This benchmark does not yet claim to infer full life-state categories. It measures similarity in the timing of individually specific Western activation patterns.

### Target domains

Equal-weight domains:

1. relationship/attachment: natal Moon, Venus, Mars;
2. resources/structure: natal Venus, Jupiter, Saturn;
3. identity/restructuring: natal Sun, Saturn, Uranus;
4. work/purpose: natal Sun, Mercury, Mars, Saturn.

### Moving layers

Transits:

- Jupiter, Saturn, Uranus, Neptune, Pluto.

Secondary progressions:

- progressed Sun, Moon, Mercury, Venus, Mars;
- one ephemeris day per tropical year, 365.2422 days.

### Aspect channels

Keep the five major aspects separate rather than treating all aspects as equivalent:

- 0, 60, 90, 120, 180 degrees.

At each monthly snapshot, each moving-body -> natal-target pair contributes a Gaussian proximity kernel to its closest exact major-aspect channel.

Frozen orbs (1-sigma kernel widths):

- transiting Jupiter: 2.5 deg;
- transiting Saturn: 2.0 deg;
- transiting Uranus/Neptune/Pluto: 1.5 deg;
- progressed Moon: 1.5 deg;
- progressed Sun/Mercury/Venus/Mars: 1.0 deg.

Within each domain/layer/aspect/month cell, average across eligible moving-target pairs so domains with more targets do not automatically receive more weight.

Specificity weights from the partner protocol:

- progression layer = 1.00;
- slow-transit-to-natal layer = 0.60.

Flatten all domain x layer x aspect x month cells, L2-normalize each person's vector, and define `western_timing_similarity` as cosine similarity between the two vectors.

This metric measures timing-pattern resemblance only. It does not call an aspect good/bad and does not identify a specific life event.

## Human Design dynamic-structure metric

At each monthly snapshot:

1. calculate each natal Gate set with exact 88-degree Design moment;
2. union the two natal Gate sets;
3. add slow transit gates from Jupiter, Saturn, Uranus, Neptune, Pluto, and true Node;
4. derive complete Channels, Centers, and connection Definition.

Report three non-calibrated structural metrics separately:

- `single_definition_fraction`: fraction of months in one connected component;
- `eight_plus_one_fraction`: fraction of months with exactly 8 defined Centers / 1 open Center;
- `single_and_eight_plus_one_fraction`: fraction of months satisfying both simultaneously.

The primary HD null rank uses `single_and_eight_plus_one_fraction` because the current pair hypothesis specifically predeclared that joint state. This is a symbolic structural benchmark, not an empirically validated relationship-quality score.

## Joint exploratory rank

For each null pool separately:

1. z-score `western_timing_similarity` against that pool;
2. z-score `single_and_eight_plus_one_fraction` against that pool;
3. `joint_z = z_western + z_hd`;
4. rank the real pair against the same null partners by `joint_z`.

Because the two components may be correlated, do not convert `joint_z` into a theoretical p-value. Report only empirical rank and percentile.

## Required output

For Joel -> women and Bee -> men, report for every Bee state:

- real Western similarity and rank;
- real HD joint-state fraction and rank;
- joint exploratory rank;
- empirical percentile;
- number of null partners exceeding the real pair;
- conservative worst-state result.

Also report null means/SDs and seed.

## Interpretation

- Top 10/1001: unusually strong development signal worth further study.
- Top 50/1001: interesting but not decisive.
- Middle of null: no evidence that the pair is unusual under this benchmark.

These thresholds are descriptive only and were frozen before observing results.
