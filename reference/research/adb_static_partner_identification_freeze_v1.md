# ADB Exact-Time Static Partner Identification V1 — Frozen Development Specification

Status: **development / model discovery**, not validation.

Freeze date: 2026-08-26.

## Question

Among high-quality exact-time people who are deliberately hard-matched to the real partner's age/generation, can static Western synastry or static Human Design connection mechanics identify the person who is actually recorded as the romantic partner?

This is a partner-selection test, not event timing and not relationship quality.

## Positive pairs

Use every unique internal C-sample romantic pair (`spouse`, `lover`, `spousal_equivalent`) for which both people:

- are present in the public C-sample;
- have Rodden A or AA data;
- have exact `jd_ut` birth times.

No dated transition event is required for this test. Based on the prior audit, approximately 45 pairs are expected.

Each unordered positive pair contributes two directed identification tasks, A→B and B→A, and both directions must remain in the same outer fold.

## Hard decoys

For each directed task A→B:

1. Candidate pool = all other C-sample people with A/AA exact-time data and the same recorded gender code as B.
2. Exclude A, B, and every person explicitly linked romantically to A in the C-sample.
3. Rank candidates by absolute difference between candidate birth JD and B birth JD.
4. Retain the nearest 50 as hard decoys.
5. If fewer than 50 eligible decoys exist, drop that directed task rather than widening the rule after seeing results.

Thus the true partner is compared with 50 people of the same recorded gender and almost the same age/generation. Pair-specific astrology/HD never enters decoy selection.

## Astronomy

- exact A/AA birth JD;
- tropical geocentric SWIEPH, hard abort on fallback;
- natal planets: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn;
- natal angles: ASC and MC from exact JD and recorded birthplace coordinates when parseable;
- exact Human Design natal gates from the existing verified HD engine.

## M0S — non-astrological baseline

Per focal/candidate pair:

- signed age difference in years;
- absolute age difference;
- focal birth year scaled;
- candidate birth year scaled.

Because decoys are selected to resemble the true partner's birth date, this is intentionally a hard baseline.

## MWS — Western static synastry

M0S plus exact aspect kernels for every ordered focal-body → candidate-body combination among:

`Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, ASC, MC`

and every major aspect:

`0°, 60°, 90°, 120°, 180°`.

Kernel:

`exp(-0.5 * (aspect_residual / 3.0°)^2)`

If ASC/MC cannot be calculated for one person, angle-dependent feature values for that row are set to 0 and explicit angle-availability indicators are included.

No aspect is pre-labelled good or bad. A sparse model may learn direction/sign from development data.

## MHDS — static Human Design connection mechanics

M0S plus:

- combined defined-center count;
- combined definition-component count;
- indicators for 9+0, 8+1, 7+2, 6+3, 5+4 center-count states;
- count of Electromagnetic channels;
- count of Companionship channels;
- count of focal-over-candidate Dominance channels;
- count of candidate-over-focal Dominance channels;
- count of focal-over-candidate Compromise channels;
- count of candidate-over-focal Compromise channels;
- count of shared activated Gates;
- count of channels in the combined connection chart.

These are source-defined mechanics only; no bespoke Joel/Bee features are added.

## MCOMB — combined static model

M0S + all Western synastry + all HD connection features.

## Fitting

Outer evaluation: 5-fold GroupKFold by unordered positive pair. Both directed tasks for a true pair stay in the same fold.

M0S and MHDS use L2 logistic regression.

MWS and MCOMB use L1 logistic regression to control the large synastry feature set.

Within each outer training fold select `C` by grouped inner CV from:

`[0.001, 0.01, 0.1, 1.0]`

Selection metric: mean true-partner percentile within each 51-person risk set. Standardization is fit on training rows only.

## Evaluation

For every directed task rank the real partner among 51 candidates using neutral average ranks for ties.

Report:

- mean/median true-partner percentile;
- top-1 rate;
- top-5 rate;
- mean reciprocal average-rank;
- risk-set softmax log loss;
- fold-level percentiles;
- A→B and B→A aggregate symmetry where available.

Primary incremental comparisons:

- MWS − M0S;
- MHDS − M0S;
- MCOMB − M0S.

## Development thresholds

A family is a **promising development signal** only if all are true:

1. mean true-partner percentile >= 60;
2. >= +5 percentile points over M0S;
3. improvement in at least 4 of 5 outer folds;
4. risk-set softmax log loss is not worse than M0S by >0.05.

A striking development signal requires mean percentile >=70 and >=+10 over M0S, but still requires independent validation.

## Permutation diagnostic

Select the best pair family by held-out mean-percentile improvement over M0S. Using the modal C from its real-data outer folds (ties → smaller C), run 200 within-risk-set label permutations. Re-run outer grouped folds at fixed C and report the empirical probability of a mean true-partner percentile at least as high as observed.

Because family selection occurs on this C-sample, the permutation is a development diagnostic, not a final p-value.

## Stopping rule

Run once. Preserve negative results. Do not alter bodies, aspects, orb, HD features, decoy rule, or thresholds after seeing results. Any new design is V2 and should preferably use an independent dataset.
