# Historical mundane-astrology backtest: pre-outcome analysis freeze

**Freeze date:** 2026-10-11 UTC.
**Status:** FROZEN BEFORE OUTCOME CSV DOWNLOAD/ANALYSIS; *not* a prospective or fully blind preregistration. Broad historical events are public knowledge to the analyst. This is a historical test of a previously constructed **2026–2086 modern symbolic outlook**, not an independent source-complete Ptolemaic mundane forecast.
**Parent:** `MUNDANE_ASTROLOGY_GLOBAL_OUTLOOK_2036_2086_EXPLORATORY.md`; methodology `ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.md`.

## Motivation and falsifiable target

Test whether years with **more hard configurations among Saturn, Uranus, Neptune and Pluto** are associated with more *new national political transformation episodes* and more *new interstate wars*, compared with ordinary calendar windows, after partial secular-trend control. These are imperfect objective proxies for societal change, **not** an encompassing measure of transformation, technological progress, progress/welfare or uniquely major world events. Do not replace primary endpoints after seeing outcomes.

## Fixed astronomy

- Geocentric tropical ecliptic longitude, UT midnight daily, with Python `swisseph` v2.10.03, requested and confirmed Moshier ephemeris `FLG_MOSEPH` for `Saturn,Uranus,Neptune,Pluto,Jupiter`; this is research mode, not production `SWIEPH`.
- Six unordered pairs of `Saturn,Uranus,Neptune,Pluto`. The primary hard contact is longitude separation (shortest arc 0–180°) within **3.0° of 0°, 90°, or 180°**. Evaluate daily inclusive endpoints. No weighting by planet, sign, degree, historical salience or claimed goodness.
- PRIMARY `hard_pair_days`: five-year-period arithmetic mean of **number of distinct hard-contact pairs active per UTC day**; a pair contributes at most one per day. Overlapping pair observations are correlated and are not independent testimony.
- Exploratory subindices: `saturn_hard` (three pairs), `outer_hard` (three U/N/P pairs), `concurrent_hard` (fraction of days >=2 distinct pair activations).
- Specificity comparator, **not** placebo: `soft_pair_days` computed analogously for sextile 60° and trine 120°, 3° orb. No claims that harmonious geometry prevents social change.
- Descriptive timeline for annual values 1816–2025 inclusive and future five-year aggregates 2036–2085. No search over alternative aspects, orbs, lead/lags, weighting, or exceptional-year lists to boost historical association.

## Outcome A: ERT national regime transformation **onset** (co-primary)

Source: Our World in Data `political-regime-ert-within-regimes.csv?v=1&csvType=full&useColumnShortNames=false`, based on Episodes of Regime Transformation v16 and V-Dem; provider lists 1900–2025. Source URL: https://ourworldindata.org/grapher/political-regime-ert-within-regimes.csv?v=1&csvType=full&useColumnShortNames=false .

Countries whose current and previous year are both observed are eligible. Stable prior regimes are ERT codes **1 and 4**. A new active transformation starts when the previous year was stable (1/4) and current year is **0,2,3,5** (hardening autocracy, liberalizing autocracy, eroding democracy or deepening democracy). This strict stable-to-episode transition misses some stop/restart events and should be called a proxy, not all true episodes. Count at most one start per country-year. Countries appearing only in the current year never count as an onset.

Rate in each fixed five-year bin: **100 × number of onsets / country-years with previous-year stable classification and both years observed**. Use completed years **1901–2024**, binned **1900–1904, ... 2020–2024**; first bin contains only 1901–1904 eligible years. Do not drop time bins with no onsets; if eligible country-years are zero, exclude with disclosure.

## Outcome B: new Correlates of War interstate wars (co-primary)

Source: Correlates of War inter-state wars v4.0, covering **1816–2007**: https://correlatesofwar.org/wp-content/uploads/Inter-StateWarData_v4.0.csv ; codebook/source: https://correlatesofwar.org/data-sets/cow-war/ .

Count **unique `WarNum` (or actual war-number column after documented case/spacing normalization) by the earliest valid `StartYear1` among participants**. An interstate war is one unit irrespective of how many states or war participants; do not count participants as separate wars. Exclude invalid negative-code years, and wars outside the horizon. Sum starts in nonoverlapping calendar 5-year bins 1820–1824, ..., 2000–2004. Main war series unnormalized count per five years (declared limitation due to expanding state system).

## Frozen inference

- Unit = non-overlapping **calendar five-year block**. Complete bins fixed before CSV access.
- For each outcome independently, compute correlation (Pearson covariance standardized as a correlation) between `hard_pair_days` and outcome, **after subtracting within-25-year-era mean** from both variables. ERT eras = 1900–1924, ..., 2000–2024. COW eras = 1820–1844, ..., 1970–1994, plus 1995–2004 final 2-bin incomplete era. Annual observations are not independent units.
- One-sided hypothesis positive (more hard geometry → more transformations/wars). Monte Carlo **20,000 independently seeded** permutations **within each 25-year era** of predictor five-year-block scores while outcomes fixed; seed **20261011**; finite-sample permutation p=(1+#permuted correlations ≥ observed)/(1+20,000). Re-demean within eras after permutation. If predictor/outcome variance zero report UNDEFINED rather than a zero signal.
- The two co-primary comparisons use **Bonferroni p<0.025 each**, without choosing a favored endpoint post hoc; also report raw p, signed r and bin counts. Report uncertainty and whether era or outcome data issues invalidate interpretation.
- Mandatory robustness: the 5-year series at zero lag; circularly rotate the entire astro series by each nonzero multiple of 5-year bins and show rank of observed correlation against shifted correlations (preserves predictor serial autocorrelation but does not resolve secular outcome trends). Report shifts as diagnostic **not** a second primary p.
- Also report outcome mean in top quartile (`hard_pair_days` among all bins) vs remaining three quartiles, with exposure denominators, as descriptive effect size; may not substitute that group comparison for the prespecified correlation if it looks stronger.
- Exploratory only: Saturn-only vs Uranus/Neptune/Pluto-only vs concurrency vs soft, 1900–2004 common-years subset, five-year lags/leads and ten-year aggregation. Clearly mark multiplicity and retain both positive and null patterns. No post-hoc 'WWI/WWII example' as significance proof.
- If a source cannot be read, mark its entire endpoint NOT_EXECUTED; do not substitute an ad hoc event list. Explain that any positive retrospective result is development evidence rather than predictive validation. Astronomical ephemeris precision is not empirical test validity.

## Interpretation restrictions and historical support

Most rare Uranus/Neptune/Pluto aspects recur on century-scale synodic intervals. **A 125–185-year history cannot independently calibrate predictions for a one-off Neptune–Pluto 2061–65 square or the 2079 Saturn–Uranus–Neptune cluster.** A result on the 5-year common hard-contact index cannot be presented as validation of specific dates, event types, countries, outcome sign, or future world claims. Explicitly compare time-only baseline and note war coverage ends 2007. All 2026–2086 claims remain symbolic unless a genuinely new predictive evaluation is run.
