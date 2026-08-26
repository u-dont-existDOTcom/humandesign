# Joel–Bee Hard-Decoy Pair Residual V3 — Result Summary

Status: **development / exploratory negative result**.

Run date: 2026-08-26.

Frozen specification:

`reference/research/partner_hard_decoy_residual_freeze_v3.md`

Research target: **pair-specific relationship-transition activation**, not relationship quality.

## Run integrity

- Frozen rules were committed before the run.
- 5,000 age-matched candidate birth moments were generated per reciprocal direction.
- For each comparison, the 1,000 hardest decoys were selected using only individual V2 2026–2040 four-domain future-trajectory similarity.
- Pair-specific information did not enter decoy selection.
- Verified SWIEPH was required; fallback aborts.
- Both hard-match pools completed all 5,000 candidates.
- All six 1,000-decoy pair comparisons completed successfully.
- The runner generated `partner_hard_decoy_residual_results_v3.json` with SHA-256:

`4b577c87b9d01fb9fea2a67bb81268017dd9124f92b721ece8d104e96fcd7070`

The workflow's final `git push` was rejected only because `main` had advanced while the long benchmark was running. The numerical benchmark step itself concluded successfully. This summary preserves the output printed by that completed step.

## Frozen threshold

The preregistered threshold for a strong exploratory result was **joint percentile >=95 in both reciprocal directions**. A robust claim across Bee's unknown time required the result to survive all plausible time states.

No state approached that threshold.

## Joel → Bee versus 1,000 hard-matched partner decoys

| Bee state | Western pair-dynamic percentile | HD pair-dynamic percentile | Joint percentile | Joint rank / 1001 |
|---|---:|---:|---:|---:|
| early | 22.7 | 84.1 | **56.0** | 441 |
| mid | 18.7 | 84.0 | **50.2** | 499 |
| late | 24.2 | 83.0 | **57.0** | 431 |

### Early-state timing details

Western:

- peak 12-month window: 2031-07-15 through 2032-06-15;
- peak12 = 0.7985215266;
- peak 24-month window: 2031-10-15 through 2033-09-15;
- western dynamic score = 0.7796867880.

HD:

- peak 12-month window: 2030-05-15 through 2031-04-15;
- peak12 = 1.0;
- peak 24-month window: 2030-05-15 through 2032-04-15;
- HD dynamic score = 0.9666666667.

### Mid-state timing details

Western:

- peak 12-month window: 2031-04-15 through 2032-03-15;
- peak 24-month window: 2031-08-15 through 2033-07-15;
- western dynamic score = 0.7699251008.

HD:

- same 2030-05 through 2031-04 peak12 structure;
- HD dynamic score = 0.9666666667.

### Late-state timing details

Western:

- peak 12-month window: 2033-12-15 through 2034-11-15;
- peak 24-month window: 2033-04-15 through 2035-03-15;
- western dynamic score = 0.7908845795.

HD:

- same 2030-05 through 2031-04 peak12 structure;
- HD dynamic score = 0.9666666667.

## Bee → Joel versus 1,000 hard-matched partner decoys

| Bee state | Western pair-dynamic percentile | HD pair-dynamic percentile | Joint percentile | Joint rank / 1001 |
|---|---:|---:|---:|---:|
| early | 17.6 | 39.5 | **32.7** | 674 |
| mid | 12.9 | 44.0 | **31.6** | 685 |
| late | 14.7 | 61.6 | **38.2** | 619 |

### Early-state timing details

Western:

- peak 12-month window: 2031-07-15 through 2032-06-15;
- peak 24-month window: 2031-08-15 through 2033-07-15;
- western dynamic score = 0.8055193528.

HD:

- peak 12-month window: 2030-05-15 through 2031-04-15;
- HD dynamic score = 0.9666666667.

### Mid-state timing details

Western:

- peak 12-month window: 2031-03-15 through 2032-02-15;
- peak 24-month window: 2031-02-15 through 2033-01-15;
- western dynamic score = 0.7925152052.

HD:

- same 2030-05 through 2031-04 peak12 structure;
- HD dynamic score = 0.9666666667.

### Late-state timing details

Western:

- peak 12-month window: 2033-11-15 through 2034-10-15;
- peak 24-month window: 2032-11-15 through 2034-10-15;
- western dynamic score = 0.7938091448.

HD:

- same 2030-05 through 2031-04 peak12 structure;
- HD dynamic score = 0.9666666667.

## Interpretation

The V3 hard-decoy test does **not** support the hypothesis that Joel/Bee has unusually strong pair-specific future transition timing once decoys are deliberately chosen to have individual future trajectories resembling the real partner.

The strongest isolated feature is Joel→Bee HD timing at roughly the 83rd–84th percentile, which is only a modest signal under the frozen interpretation bands and does not survive reciprocal comparison. The Western pair-dynamic signal is below-average to low in every state. The equal-standardized joint score is ordinary in Joel→Bee and below-average in Bee→Joel.

Therefore:

> Under frozen V3, the previously noticed 2030–2032 relationship pattern is not evidence that Joel and Bee are uniquely likely to reunite relative to hard-matched alternatives.

This does not prove they will not reunite. It shows that this symbolic pair-specific residual model does not discriminate the pair strongly enough to justify that conclusion.

## Important distinction

V3 addresses **whether a specific relationship transition is astrologically/HD-distinctive**. It does not address whether the relationship would be loving, reciprocal, satisfying, safe, or good for both people. That is Track Q and must be trained/tested separately as specified in `docs/20_partner_transition_vs_quality.md`.

## Next research step

Do not tune V3 using Joel/Bee. Develop the empirical semi-Markov transition model on other couples, freeze it, and only then score Joel/Bee prospectively. Develop relationship-quality prediction as a separate empirical model.
