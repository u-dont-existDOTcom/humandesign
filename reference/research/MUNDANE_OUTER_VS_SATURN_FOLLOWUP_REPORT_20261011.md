# Transfer backtests: Uranus/Neptune/Pluto versus Saturn hard aspects (2026-10-11)

**Status:** `UNSUPPORTED` under the frozen external-outcome transfer criteria.
**Research classification:** `POST_DISCOVERY_DEVELOPMENT` — directional split was selected after observing earlier ERT regime data, not blindly preregistered.
**Freeze:** `reference/research/MUNDANE_OUTER_VS_SATURN_FOLLOWUP_FREEZE_20261011.md` committed before acquiring the two new outcome datasets.
**Executable:** `scripts/research/mundane_outer_saturn_transfer_20261011.py`
**Machine-readable:** `reference/research/mundane_outer_saturn_transfer_20261011/transfer_results.json`
**Source-completeness re-study:** `state/MUNDANE_ASTROLOGY_RESTUDY_AFTER_TEXT_AUDIT_20261011.md`

## Central result

The outer-minus-Saturn distinction is **not independently replicated** across the two new historical outcome domains. There is a potentially interesting association with intrastate-conflict onsets, but not with attempted coups. The former is statistically inconclusive under the frozen two-outcome threshold, is concentrated in the 1975–1999 historical era and reverses direction between chronological subperiods.

| Outcome | Five-year blocks | Detrended contrast r | One-sided 20,000-shuffle p | Corrected threshold | Verdict |
|---|---:|---:|---:|---:|---|
| Powell–Thyne attempted coups, 1950–2024 | 15 | **+0.0518** | **0.4352** | 0.025 | Null |
| UCDP v25.1 intrastate armed-conflict onsets, 1950–2024 | 15 | **+0.6028** | **0.0521** | 0.025 | Suggestive **but unsupported** |

The `outer_hard - saturn_hard` predictor was formed after seeing the old dataset, with no new orbs, aspect types, signs or weights tuned against these new endpoints. It compares the three U/N/P pairs against the three Saturn-to-U/N/P pairs using the prior geocentric tropical ephemeris and 3° hard-aspect (0/90/180°) definition. One independent unit is a **5-year calendar block**, not an aspect day, country-year or an individual coup.

Fifteen blocks offer modest power, and the three adjacent five-block era strata limit inference. Within each 25-year stratum, paired predictor/outcome values were mean-centered; predictor blocks were permuted within their strata (seed 20261012), with a separate circular-shift serial-dependence diagnostic. The one-sided directional expectation was fixed **before new outcomes were examined**, but was *derived* from the previous observed ERT correlation.

## Exact endpoint accounting

- **Coups:** Powell and Thyne's public August 29, 2026 event-level update, date and country-coded. Count successful plus failed coup attempts, exactly one per distinct country/coup date, years 1950–2024. **493 coup attempts**, of which **246 successful**, over the 15 blocks. No duplicate keys or undated in-scope events. The full public download contains 497 events from 1950 through 2026, with four excluded outside the fixed period. [Powell source](https://jonathanmpowell.com/coups/) and Powell & Thyne, *Journal of Peace Research* 48(2), 249–259, DOI 10.1177/0022343310397436.
- **Armed-conflict onsets:** Uppsala Conflict Data Program, `ucdp-intrastate-conflict-onset-251.csv`, version 25.1, year 1946–2024. Use **`onset1==1`**, one event per country / numeric `conflict_ids` / year; exclude continuing/conflict-inactive rows and anything before 1950. **499 onset records** in 1950–2024. A country-year with multiple separate onset conflict IDs may legitimately contribute several events, whereas multiple country-year rows without onset do not. [Official historical version catalog](https://ucdp.uu.se/downloads/olddw.html). UCDP distributes datasets under CC BY 4.0 with attribution.
- Pinned SHA-256 `powell_thyne_20260829.csv` = `1e8f933b22f4b9a77d0ba5eb59bf0d8158adcaab27746adcf345195be87a9012` (20,089 bytes). UCDP CSV = `a5a64b749693c85fd3b50a1311608a44c0846d528352baeb3767f25e50d52fe1` (522,945 bytes). Both links, exact bytes and SHA are recorded in `transfer_results.json`, along with the hashes of the original astronomical/ERT/COW derived inputs.
- Provider source files are archived privately for the owner, not republished indiscriminately in the public GitHub repository. The repo preserves their immutable hashes, versioned acquisition URLs, exact acquisition script, derived annual and 5-year counts, test fixtures and outputs. A third party must fetch the pinned source to reproduce the original parsing if the provider hasn't changed it.

## Components and secondary/negative controls

| Outcome | Outer hard alone r | Saturn hard alone r | Combined all-hard r | Contrast r |
|---|---:|---:|---:|---:|
| Coup attempts (new) | +0.018 | −0.126 | −0.023 | **+0.052** |
| UCDP conflict onsets (new) | +0.541 | −0.436 | +0.416 | **+0.603** |
| Successful coups (secondary) | See exact JSON | See exact JSON | See exact JSON | **−0.171** |
| COW interstate wars, 1820–2004 (earlier source; negative-control endpoint) | See exact JSON | See exact JSON | See exact JSON | **+0.051** |
| ERT regime onsets, 1901–2024 (**original discovery dataset**) | +0.331 | −0.385 | +0.190 | **+0.442** |

The successful-coup-only comparison was prespecified as secondary and points the *opposite way*: r **−0.171**, one-sided p **0.702**. Neither whole-history war onset comparison (r **+0.051**, p **0.343**) nor the 1950–2004 war subset (r **+0.283**, p **0.173**) independently validates the split. Original ERT contrast r **+0.442** is **post-hoc discovery, not a fresh confirmatory test** (its nominal permutation p **0.114** is not selection-adjusted).

The two new co-primary outcomes each show the *component signs* of the original distinction (+ outer, − Saturn), but in coups both effects are too small to matter. A direction-only consistency check is extremely weak evidence when selected based on earlier data and can occur by chance.

## Robustness that changes the interpretation

**Excluding whole historical eras:**

| Omitted 25-year era | Coup contrast r | UCDP onset contrast r |
|---|---:|---:|
| 1950–1974 | +0.040 | +0.680 |
| 1975–1999 | +0.064 | **+0.095** |
| 2000–2024 | +0.057 | +0.797 |

The UCDP aggregate r **+0.603** drops to only **+0.095** if the 1975–1999 era is excluded. The apparent effect is not uniform across historical eras.

**Chronological split**, also planned in advance: UCDP contrast r **−0.150** for 1950–1984 versus **+0.662** for 1985–2024. The two eras contain different reporting conditions, conflict bases and outer-planet background. These cannot be interpreted as a stable forward forecasting rule.

**No cherry-picked blockbuster years:** The contrast index is strongest in **1990–1994** (+0.480 hard-pair days/day), when the UCDP series records 74 distinct intrastate onset events. However, **2015–2019** records almost as many (69) with *negative* contrast (−0.036). These are illustrations only. Critically, excluding **1990–1994** from the *original ERT discovery dataset* flips the contrast from r +0.442 to **r −0.058**. This disallows using the initial ERT evidence as stable independent support for the UCDP association.

**Circular temporal rotations** of the frozen predictor: actual UCDP alignment ranks 1st out of 15 five-year rotations (1/15 ≈ 0.067 of shifts as strong or stronger), while the coup alignment ranks 8th/15. A rotation rank is a descriptive check preserving astronomical serial shape, **not** a separately calibrated significance test.

**Top-quartile descriptive effect sizes:** in four top-contrast bins vs eleven others, UCDP had 37.25 vs 31.82 onset events per five-year interval (ratio **1.17**); coups had 39.0 vs 30.64 attempts (ratio **1.27**). This simplistic high-vs-low ranking is neither era-detrended nor an inferential substitute. Its coup ratio conflicts with the nearly null era-detrended correlation, illustrating the importance of secular/era controls.

## Implications

1. The very weak coup result undercuts any broad claim that the outer-minus-Saturn pattern universally tracks societal upheaval.
2. The UCDP r may motivate **one future methodologically fresh** targeted preregistration, but present results are selection-exposed, low-N, uneven across eras, and fail the frozen corrected threshold; cannot label **replicated or validated**.
3. Nothing here supports describing 2061–65, 2078–81, other future years, named regions or political systems as unusually dangerous or beneficial.
4. The long-running *full astrology primary-text study lane* is **still OPEN**. The owner explicitly requested a **new source-native mundane backtest** once that corpus reaches its stated completion point. The durable follow-up tracker is `state/MUNDANE_ASTROLOGY_RESTUDY_AFTER_TEXT_AUDIT_20261011.md`. Do not make the current exploratory split an active predictive rule.
5. An independent review may recheck UCDP `onset1` codebook semantics and secular-rate normalization before any promotion, including changes in the state-system denominator; these are OPEN methodological limitations, not steps silently claimed executed.

## Verification

Reproduce with the original astronomy/datasets from the previous backtest and pinned Powell/UCDP source snapshots:

```bash
python3 -m unittest tests.test_mundane_outer_saturn_transfer_20261011 -v
python3 scripts/research/mundane_outer_saturn_transfer_20261011.py --fetch
python3 scripts/research/mundane_outer_saturn_transfer_20261011.py
```

Seven focused parser/index/source tests passed (source hash test skips cleanly if snapshots not present). All predeclared new outcome results, old discovery comparisons, permutations, rotations, leave-one-era-out checks and chronological splits are in the machine-readable result. Recompute/corrected code creates a new version/commit; do not overwrite history or improve appearance by selecting endpoints after seeing outcomes.
