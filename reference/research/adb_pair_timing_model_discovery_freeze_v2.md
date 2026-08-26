# ADB Pair-Timing High-Resolution Model Discovery V2 — Frozen Development Specification

Status: **openly developmental model discovery**, not validation.

Freeze date: 2026-08-26.

V1 found no useful signal from coarse collapsed astrology features. V2 asks whether a sparse model using **specific planet -> planet -> aspect combinations** can improve held-out relationship-formation timing.

## Dataset

Use exactly the V1 extraction/control-date rules in `reference/research/adb_pair_timing_model_search_freeze_v1.md`.

Primary target: formation/commitment events only (ADB event IDs 807, 808, 810), because V1 produced 84 formation events but only 18 dissolution events.

All splits remain grouped by unordered couple.

Partner time uncertainty remains date-only/noon UT for parity; exclude Moon, houses, angles, HD, and other time-sensitive features.

## Raw astrology feature representation

Instead of V1's maximum activation across targets/aspects, preserve each specific aspect kernel separately.

Planets:

- natal targets: Sun, Mercury, Venus, Mars, Jupiter, Saturn;
- progressed movers: Sun, Mercury, Venus, Mars;
- slow transits: Jupiter, Saturn, Uranus, Neptune, Pluto;
- aspects: 0, 60, 90, 120, 180 degrees.

Kernel:

`exp(-0.5 * (exact_aspect_residual / sigma)^2)`

with sigma 1.0 degree for progressed aspects and 1.5 degrees for slow-transit aspects.

### M0-HR baseline

- age A;
- age B;
- candidate year.

### M1-HR individual timing

M0 plus raw aspect features for, separately for A and B:

- every slow-transiting planet -> every own natal target -> every major aspect;
- every progressed personal planet -> every own natal target -> every major aspect.

### XPROG-HR cross-progressions

M1 plus:

- progressed A -> natal B, all allowed mover/target/aspect combinations;
- progressed B -> natal A;
- progressed A -> progressed B among Sun/Mercury/Venus/Mars, all aspects.

### NCOMP-HR natal-composite transit model

M1 plus every slow transit -> each same-name midpoint-composite natal planet -> every aspect.

### PCOMP-HR progressed-composite transit model

M1 plus every slow transit -> each same-name midpoint of progressed Sun/Mercury/Venus/Mars -> every aspect.

### ALL-HR

M1 + XPROG-HR + NCOMP-HR + PCOMP-HR.

No static synastry is included because it cannot discriminate the event year within a pair.

## Fitting

Use L1-penalized logistic regression (`liblinear`) with class balancing.

Within each outer training fold choose C using grouped inner CV from:

`[0.001, 0.01, 0.1, 1.0]`

Selection metric: mean true-date percentile among candidate years.

Standardize features using training-fold statistics only.

Outer evaluation: deterministic 5-fold GroupKFold by couple, if dataset still has >=25 unique pairs.

## Evaluation

Same event-ranking metrics as V1:

- mean/median true-date percentile;
- top-1 and top-3;
- mean reciprocal rank;
- group-softmax log loss.

Primary comparison is each pair model versus M1-HR.

Promising development signal requires:

- >=5 percentile-point mean true-date improvement over M1-HR;
- softmax log loss no worse by more than 0.05;
- improvement not confined to one outer fold.

Also report sparse feature stability:

- feature selected (nonzero) in how many outer folds;
- sign consistency across selected folds;
- mean standardized coefficient when selected.

Do not interpret a single coefficient as a discovered astrological law.

## Permutation diagnostic

After selecting the best pair family by observed outer-CV percentile improvement:

- take the modal C selected across the real-data outer folds for that family (ties -> smaller C);
- run 100 within-event label permutations;
- for each permutation, rerun the 5 outer grouped folds with that fixed C (no hyperparameter retuning);
- report empirical p-value for mean true-date percentile >= observed.

This remains a development diagnostic because the family itself was selected on the C-sample.

## Stopping rule

Run once. If no pair family clears the frozen threshold, conclude that this C-sample/date-only design has not found a useful pair-dynamic timing model.

Do not inspect coefficients and then alter aspect or body sets within V2. Further feature engineering becomes V3 and should preferably use a different development dataset or the eventual full Astro-Databank export.
