# ADB Pair-Timing High-Resolution Model Discovery V2 — Result Summary

Status: **negative development result**.

The first V2 execution had a tie-ranking evaluator bug and is invalid; see `adb_pair_timing_model_discovery_v2_erratum.md`. The corrected rerun uses neutral average ranks for tied candidate dates and supersedes that initial artifact.

## Dataset

- 84 formation/commitment events from 75 unique romantic pairs;
- 74 marriages, 7 meet-significant-person events, 3 begin-significant-relationship events;
- 72 day-precision and 12 month-precision event dates;
- each true date compared against the same month/day shifted by up to +/-10 years, subject to age constraints;
- 1,522 candidate-date rows;
- verified SWIEPH only;
- most linked partners are birth-date-only, so Moon, houses, angles, and Human Design are excluded.

## Corrected held-out-couple results

Mean true-event-date percentile:

- M0HR non-astrological age/calendar baseline: **60.54**;
- M1HR high-resolution individual astrology: **47.66**;
- XPROGHR cross-progressions: **49.39**;
- NCOMPHR natal-composite transits: **48.74**;
- PCOMPHR progressed-composite transits: **46.72**;
- ALLHR all pair-dynamic families combined: **51.00**.

The frozen requirement for a promising pair family was:

1. >= +5 mean percentile points over M1HR;
2. softmax log loss no worse by >0.05;
3. improvement not confined to one fold.

No family cleared the threshold.

The best observed family by mean-percentile improvement was ALLHR:

- +3.34 percentile points relative to M1HR;
- improved softmax loss relative to M1HR by about 0.44;
- positive percentile improvement in 3/5 folds;
- still only 51.00 mean true-date percentile and still below the 60.54 non-astrological baseline.

## Permutation diagnostic

The selected ALLHR family was tested with 100 within-event label permutations using the frozen fixed-C diagnostic.

- observed mean true-date percentile: 51.00;
- permutation null mean: 50.48;
- permutation null SD: 3.53;
- empirical p-value: **0.416**.

This is completely compatible with chance.

## Feature-stability observation

One pair-specific feature was relatively stable in the failed ALLHR development model:

- slow transiting Saturn sextile natal midpoint-composite Venus (`nc_tr_Saturn_Venus_a60`) was selected with a positive coefficient in 4/5 outer folds.

Several individual-timing features also recurred, including Saturn/Jupiter/Uranus contacts.

Because the overall model failed its frozen performance threshold and the selected-family permutation was null, none of these coefficients should be treated as discovered astrological rules. At most they are candidates to preregister on a genuinely independent dataset.

## Conclusion

Under the current public Astro-Databank C-sample/date-only design, **no tested Western-astrology timing model has demonstrated useful held-out prediction of romantic formation dates**.

The simple non-astrological age/calendar baseline outperformed every tested astrology model in mean true-date rank.

Therefore do not tune additional aspect/body/orb choices on this same sample. The next legitimate step is a richer independent dataset, ideally with both partners' exact birth times and dated relationship-state histories, followed by the nested semi-Markov M0-M4 test in `docs/21_pair_transition_semimarkov_plan.md`.
