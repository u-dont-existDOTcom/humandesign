# ADB Exact-Pair Relationship Timing V3 — Result Summary

Status: **negative development result with one weak cross-progression lead**.

This summary corresponds to the frozen specification `reference/research/adb_exact_pair_timing_freeze_v3.md` and raw result artifact `reference/research/adb_exact_pair_timing_results_v3.json`.

Freeze SHA-256: `2624ae221cdadf91b0e7145ff9e63659aa0abf1edfc15cf77fa4d6f083883fb3`.

## What V3 added

V3 was designed to test information unavailable in the earlier date-only ADB study:

- exact natal Moon;
- ASC/DSC, MC/IC, 5th- and 7th-house cusps;
- exact secondary progressions;
- exact cross-progressions between partners;
- exact natal midpoint-composite timing;
- progressed midpoint-composite timing;
- Davison relationship-chart timing;
- dynamic Human Design pair-state features.

The previously failed date-stable individual astrology family (`M1DATE`) was retained as the comparison baseline and was not retuned to V3 outcomes.

## Exact-time recovery and UTC validation

Public Astro-Databank wiki records recovered 65 additional high-Rodden-rating exact-time external people usable by the V3 pipeline.

The required local-time + `stmerid` -> UT reconstruction gate passed comfortably:

- validation records: **491**;
- median absolute error: **0.0288 seconds**;
- maximum absolute error: **0.0416 seconds**;
- parse failures: 9 records, which were not silently treated as valid.

The frozen gate required median error <=1 second and maximum error <=5 seconds.

## Final dataset

After SWIEPH and age preflight:

- **64 unique romantic pairs**;
- **81 relationship events** total;
- **70 formation/commitment events** used for the primary model;
- **11 dissolution events**;
- **1,245 formation candidate-date rows**;
- 225 control rows excluded by age constraints;
- 3 pair/event records excluded because natal or HD design calculations were outside the pinned Swiss ephemeris range.

The dissolution analysis was not fit because the frozen specification required at least 30 usable dissolution events.

This remains a C-sample-derived case-crossover development dataset, not an independent semi-Markov validation set.

## Frozen held-out-pair results

All models used grouped outer 5-fold cross-validation by unordered romantic pair.

The frozen usefulness threshold for an exact-time family, relative to `M1DATE`, required all three:

1. mean true-date percentile improvement >= +5 points;
2. softmax log loss no worse by more than +0.05;
3. positive mean-percentile improvement in at least 3/5 outer folds.

| Model | Mean true-date percentile | Δ vs M1DATE | Softmax log loss | Δ loss vs M1DATE | Positive folds | Clears threshold? |
|---|---:|---:|---:|---:|---:|---|
| M0EX non-astrological age/calendar | **61.83** | — | **2.835** | — | — | baseline |
| M1DATE date-stable individual astrology | 49.14 | 0.00 | 2.865 | 0.000 | — | baseline |
| M1EX exact-time individual additions | 47.15 | -1.98 | 5.704 | +2.839 | 2/5 | No |
| XEX exact cross-progressions | **54.70** | **+5.56** | 4.449 | **+1.584** | **5/5** | **No** |
| NCOMPEX natal midpoint-composite | 44.90 | -4.24 | 3.253 | +0.389 | 1/5 | No |
| PCOMPEX progressed midpoint-composite | 49.33 | +0.20 | 3.331 | +0.466 | 1/5 | No |
| DAVEX Davison timing | 52.66 | +3.53 | 4.054 | +1.189 | 4/5 | No |
| HDEX dynamic Human Design | 49.14 | 0.00 | 2.865 | approximately 0.000 | 0/5 | No |
| WESTEX all Western exact-time families | 53.68 | +4.54 | 5.289 | +2.424 | 4/5 | No |
| ALLSYS Western + Human Design | 54.02 | +4.89 | 5.269 | +2.404 | 4/5 | No |

**No exact-time family cleared the frozen threshold.**

The simple non-astrological age/calendar baseline (`M0EX`) remained substantially better in mean true-date percentile than every astrology or Human Design model.

## The XEX lead

`XEX` was the best exact-time family by mean-percentile improvement over `M1DATE`:

- mean true-date percentile: **54.70**;
- improvement over `M1DATE`: **+5.56 points**;
- positive improvement in **5/5 folds**;
- top-1 rate: 7.14%;
- top-3 rate: 28.57%;
- mean reciprocal rank: 0.233.

However, its softmax log loss worsened from 2.865 to 4.449, a deterioration of **+1.584**, far beyond the frozen +0.05 tolerance. Therefore XEX is not a successful model under the preregistered rule.

The two most stable XEX-specific features selected with the same positive sign in all five outer folds were:

- `x_pb_na_Moon_Jupiter_a120`: progressed partner-B Moon trine partner-A natal Jupiter;
- `x_pa_nb_Mercury_Mercury_a60`: progressed partner-A Mercury sextile partner-B natal Mercury.

Other cross-progression features recurred in fewer folds, but because V3 failed its overall frozen criterion they are exploratory hypotheses only.

## Permutation diagnostic

Although no family cleared the complete frozen threshold, the implementation ran the planned 200 within-event label-permutation diagnostic on the best exact family by mean-percentile improvement, XEX, using fixed `C=0.01`.

- observed mean true-date percentile: **54.7006**;
- permutation null mean: **50.0622**;
- permutation null SD: **3.6675**;
- null permutations >= observed: **19/200**;
- empirical p-value: **0.0995**.

This is a weak descriptive lead, not statistically compelling evidence. Family selection occurred on this same development dataset, so the p-value is diagnostic rather than confirmatory.

## Davison and combined-model observations

`DAVEX` reached 52.66 mean percentile and improved on `M1DATE` in 4/5 folds, but its log loss worsened by +1.189. It therefore failed the frozen rule.

Several Davison features were relatively stable in the failed development fits, including:

- transiting Neptune trine Davison Moon;
- transiting Jupiter sextile Davison Venus;
- transiting Jupiter sextile Davison Sun.

The combined Western and Western+HD models reached 53.68 and 54.02 mean percentile respectively, but both suffered very large log-loss deterioration. They should be interpreted as overfit ranking movement rather than successful probability models.

## Recurrent exploratory feature

The earlier V2 date-only study found `nc_tr_Saturn_Venus_a60` — transiting Saturn sextile natal midpoint-composite Venus — selected with a positive sign in 4/5 folds of its failed combined model.

In V3 the same feature again appeared with a positive sign in 4/5 folds of the failed combined Western/ALLSYS models.

This recurrence is interesting enough to preregister in an independent study, but it is not evidence that the aspect is predictive because both source models failed their overall frozen performance criteria and both were inspected during model development.

## Human Design result

The deliberately low-dimensional dynamic Human Design additions did not improve the date-stable baseline. `HDEX` produced effectively the same held-out ranking and log loss as `M1DATE`, implying that the HD additions contributed no stable useful signal under this specification.

This result applies only to the frozen V3 dynamic-HD feature set; it is not a test of every possible Human Design relationship rule.

## Conclusion

Under the frozen V3 exact-time specification, **exact birth times did not rescue relationship-event prediction**.

The strongest new family, exact cross-progressions, showed a reproducible-in-fold ranking lead but failed probability calibration badly and produced only a development-stage permutation p-value of about 0.10. Every astrology/HD model remained below the non-astrological age/calendar baseline in mean true-date percentile.

Therefore V3 should not be tuned further on these same 70 formation events.

The legitimate next step is to freeze a very small hypothesis set from the recurrent development signals and test it on genuinely new couples with independently collected dated relationship-state histories. The higher-value target is the semi-Markov transition question already specified in `docs/21_pair_transition_semimarkov_plan.md`: whether pair-specific features predict transitions such as separated -> reunited, conditional on current relationship state and time already spent in that state.
