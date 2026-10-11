# Historical test of global mundane-astrology transformation claims (1820–2024)

**Analysis date:** 2026-10-11 UTC
**Status:** COMPLETED HISTORICAL DEVELOPMENT TEST — **NO STATISTICALLY SUPPORTED PREDICTIVE SIGNAL IN THE TWO FROZEN PRIMARY ENDPOINTS**.
**Original forward-facing interpretation:** `reference/research/MUNDANE_ASTROLOGY_GLOBAL_OUTLOOK_2036_2086_EXPLORATORY.md`.
**Methods frozen before outcome CSV acquisition:** `reference/research/MUNDANE_HISTORICAL_EVENT_BACKTEST_FREEZE_20261011.md`.
**Calculator:** `scripts/research/mundane_historical_backtest_20261011.py`; **tests:** `tests/test_mundane_historical_backtest_20261011.py`.
**Complete dated outcome results:** `mundane_historical_backtest_20261011/MUNDANE_HISTORICAL_BACKTEST_RESULTS_20261011.json`.
**Astronomical mode:** pyswisseph 2.10.03, verified Moshier flags (research-only, not canonical SWIEPH).

## Executive answer

No. **This initial quantitative historical test does not show that periods with many hard Saturn/Uranus/Neptune/Pluto aspects were more politically transformative or more likely to begin interstate wars than ordinary five-year periods.** The historical astrology effect is small and statistically unsupported for regime-change onsets, and essentially zero for interstate-war starts. That conclusion applies to the prespecified features and measured outcomes, *not* to all forms of historical transformation or all astrological hypotheses.

We tested outcomes from independent publicly maintained datasets rather than manually selecting famous revolutionary years. The astrological rule and method were committed to the research branch **before reading/downloading the endpoint CSV data**. Nevertheless this remains **retrospective development**, not independent blinding: major historical events are generally known and the 2026–2086 symbolic reading was itself constructed before this comparison.

## Frozen primary test results

| Independently recorded outcome | Nonoverlapping 5-year bins | Detrended correlation with hard-aspect activity | One-sided within-era permutation p | Decision |
|---|---:|---:|---:|---|
| New V-Dem ERT regime-transformation episodes (strict stable-to-active proxy, 1901–2024) | 25 | **+0.1900** | **0.2144** (20,000 permutations) | NO primary signal |
| New COW interstate wars (unique war IDs, 1820–2004) | 37 | **−0.0022** | **0.4913** (20,000 permutations) | NO primary signal |

Prespecified two-co-primary Bonferroni criterion: each one-sided p must be < **0.025** to declare that endpoint significant. Neither qualifies. Period-specific sample sizes are modest, so absence of statistical evidence is not proof of zero causal effect.

**Raw, easy-to-interpret effect sizes:** Seven highest-activity ERT five-year bins averaged **3.841** national episode starts per 100 eligible stable-country-years, versus **3.782** in the other 18 bins (**ratio 1.016**, just 1.6% greater). The ten highest-activity war bins averaged **2.50** newly started interstate wars, versus **2.59** in the remaining 27 (**ratio 0.964**, 3.6% fewer, not more). These descriptive splits are not substitutes for the predeclared tests.

**Astronomical-cycle-preserving shift check:** Exact alignment ranked 5th of 25 astronomical rotations for ERT (20% of rotations at least as positive), and 18th of 37 for war (48.6%). This is a diagnostic rank, not another calibrated p-value.

## What was actually measured?

The primary astronomy index is the five-year average count of distinct planet pairs among **Saturn, Uranus, Neptune and Pluto** at most 3° from a **conjunction, square, or opposition**, sampled daily in the geocentric tropical zodiac. Six unordered pairs; a pair counts at most once per day. Geometric coincidences within a three-body pattern are dependent and *must not* be represented as independent evidence.

The institutional endpoint comes from V-Dem's **Episodes of Regime Transformation (2026), processed by Our World in Data**. Country-years with prior stable codes **1 (stable autocracy) or 4 (stable democracy)** were eligible; a new episode was recorded only when the following year's regime code became dynamic **0, 2, 3, or 5**. The public CSV contains 19,128 unique coded country-years across 175 country codes in our filter. This deliberately strict proxy omits some episode restarts and does not measure subjective welfare, cultural progress, or innovation.

The warfare endpoint comes from **Correlates of War (COW), Inter-StateWarData v4.0**. We counted earliest `StartYear1` per unique `WarNum`, rather than mistakenly treating individual country participants as new wars; the resulting 1820–2004 analysis contains **95 unique wars**. It excludes civil wars, non-state conflict and other forms of societal change. State-system expansion and war-coding limitations remain uncorrected except for 25-year time strata.

The primary test removed the 25-year-era mean from both series and permuted the astro five-year-bin exposure **within each fixed 25-year era**, 20,000 permutations at seed 20261011. This reduces—but does not eliminate—slow secular trends and dependence. War and political-institutional onsets are not a validated omnibus historical-transformation index. The two domains have non-identical geographic and temporal coverage.

## Illustrative hits and misses (not statistical evidence)

- **1990–1994**: among the strongest astrological five-year windows (**0.761 active hard pair-days per day**) and the highest ERT onset proxy rate (**11.52 per 100 eligible country-years**). This supports the *possibility* of a positive match for this one interval, not a general rule.
- **1905–1909**: almost equally high astronomical exposure (**0.760**), but extremely low ERT onset rate (**0.99**). Strong counterexample to the simple universal inference.
- **1935–1939**: the COW data count **6 new interstate wars**, while astronomical hard-pair activity was only **0.229**. This is a missed high-activity historical interval under the frozen aggregate feature.
- **1820–1824**: exceptionally high angular index (**1.219**), but only **one** new COW interstate war in the bin. A notable exposure-positive/non-event contrast.
- **1965–1969**: relatively high astro activity (**0.684**) and six COW interstate wars; one illustrative co-occurrence amid misses.

**Stability challenge:** When excluding the entire **1975–1999** era and recalculating on the remaining eras, the ERT correlation reverses sign to **−0.259**. The original +0.190 value is strongly era-sensitive, a serious reason not to treat the positive direction as a stable rule.

Exploratory anatomy also illustrates the selection danger: Saturn-to-outer hard contacts alone have ERT r **−0.385**, whereas Uranus/Neptune/Pluto hard contacts alone have ERT r **+0.331** (and their concurrency r **+0.320**). These are **unadjusted exploratory correlations**, compared across several candidate predictors and outcomes. Choosing only the positive outer component after seeing this table would be hindsight tuning. No component was promoted.

## Implications for the 2036–2085 outlook

The measured *astronomical configurations* remain real calculations, but the historical test **does not establish that they foreshadow wars, political transformations, or beneficial versus harmful innovation**. Highest-scoring selected five-year windows of the future astronomical index:

| Window | Mean number of active hard planet pairs per day |
|---|---:|
| 2061–2065 | **0.850** |
| 2076–2080 | **0.791** |
| 2041–2045 | **0.719** |
| 2066–2070 | **0.542** |
| 2071–2075 | **0.381** |

High-score windows are periods of **orb-defined planetary geometry**. They should **not** be advertised as historically calibrated crisis years or as a ranking of human progress. For comparison, observed 1820–1824 exceeded those future values (**1.219**) without a corresponding high number of interstate-war starts in the selected dataset. The distinctive **2061–2065 Neptune–Pluto squares** and **2079 Saturn–Uranus–Neptune geometry** each lack enough truly repeated independent historical analogues within 1820–2024 to calibrate a 50-year prediction.

Modern outer-planet symbolism is not a source-native application of Ptolemy's mundane eclipse/region technique. Historical positive associations would need prospective replication, geographic controls, preregistered interpretation direction, suitable social-outcome benchmarks, and a held-out period. These remain OPEN and are not claimed here.

## Reproducibility and exact source provenance

Input files stored as public snapshots under `data/mundane_historical_backtest_20261011`:

- ERT (V-Dem 2026 via OWID, fetched 2026-10-11): `ERT_v16_OWID.csv`, **404,508 bytes**, SHA-256 `b577f348db501c4c1f6b77c5588db507f33866af039901cab067659eaab60274`. Source: https://ourworldindata.org/grapher/political-regime-ert-within-regimes
- COW (Sarkees & Wayman 2010, 1816–2007): `Inter-StateWarData_v4.0.csv`, **31,698 bytes**, SHA-256 `2535e30b145141c331a07d12d91e498ad8bdd3db32ba8d3bd88c4fda54817731`. Source: https://correlatesofwar.org/data-sets/cow-war/

To reproduce from committed snapshots on Linux with installed pyswisseph version 2.10.03:
```bash
python3 -m unittest tests.test_mundane_historical_backtest_20261011 -v
python3 scripts/research/mundane_historical_backtest_20261011.py
```
`--fetch` intentionally refreshes external data and can change input hashes and results if the sources update; a paper referencing this test must use the pinned source snapshots, not a live silent refresh.

**Verification:** Four focused unit tests passed; 1900, 1930, 1950, 1965, 2061, 2079 daily aspect-index means were independently cross-checked against a separately coded ephemeris calculation; a complete rerun without downloading sources produced **byte-for-byte identical outputs**. No claims of complete Swiss ephemeris production verification, genuine blinding or general historical predictive validity.

**Research verdict:** The frozen global hard-aspect activity model has **NOT passed historical validation** for the two specified real-world event outcomes. Preserve this negative evidence alongside the prior evocative future outlook instead of tuning the same test until it appears to fit.
