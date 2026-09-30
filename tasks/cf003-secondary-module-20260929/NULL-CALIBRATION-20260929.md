# CF-003 null calibration after cross-family review

Date: 2026-09-29
Status: development methodology receipt; not prospective evidence.

## Trigger

Claude Opus 5.5 Max found that the initial global construct-label permutation did not represent the intended chart-to-behavior null. It changes the evaluator semantics while preserving participant pairing, so unequal predictor-label and behavioral-construct base rates can distort type-I error.

The reviewer supplied two reproducibility scripts, preserved unchanged at:

- `reviewer-artifacts/opus_cf003_probes.py`
- `reviewer-artifacts/opus_cf003_null_sim.py`

The simulation was run with the existing repository Python environment; no paid API inference was used for the simulation.

## Simulation result

Nominal alpha was 0.05. Each small-N condition used 400 independent null datasets and 999 permutations.

| Behavioral marginals | N | Old global-label null | Whole-profile reassignment |
| --- | ---: | ---: | ---: |
| equal | 30 | 0.052 | 0.043 |
| equal | 60 | 0.045 | 0.037 |
| equal | 120 | 0.045 | 0.040 |
| T01/T07 elevated | 30 | 0.087 | 0.040 |
| T01/T07 elevated | 60 | 0.092 | 0.040 |
| T01/T07 elevated | 120 | 0.110 | 0.043 |
| T01/T05/T07 elevated, T10 low | 30 | 0.087 | 0.065 |
| T01/T05/T07 elevated, T10 low | 60 | 0.092 | 0.045 |
| T01/T05/T07 elevated, T10 low | 120 | 0.133 | 0.058 |
| T03 elevated only | 120 | 0.010 | 0.048 |

The old null was anti-conservative in several unequal-marginal scenarios and conservative in another. The whole-profile reassignment stayed near nominal across these checks.

A five-dataset N=3,000 stress check also showed severe distortion in the old method under unequal marginals. For one such scenario its p-values were 0.001, 0.028, 0.0045, 0.083 and 0.022, while the corresponding whole-profile reassignment p-values were 0.1175, 0.6025, 0.176, 0.8955 and 0.3185.

## Implemented correction

The inferential null now:

1. keeps each predictor fixed;
2. keeps the construct-to-planet map fixed;
3. reassigns each participant's complete frozen behavioral profile to another participant;
4. restricts reassignment to the same preregistered birth-cohort stratum;
5. recomputes the cohort primary statistic;
6. uses a preregistered Monte Carlo seed and count.

The previous global construct-label permutation remains only as diagnostic/historical code and is explicitly not the inferential chart-to-behavior null.

## Remaining prospective hold

The exact birth-cohort strata, Monte Carlo seed/count, classifier model/version, balanced source-coverage rule, and chart-factor extraction convention remain development decisions. They must be frozen before any new prospective target responses are opened.
