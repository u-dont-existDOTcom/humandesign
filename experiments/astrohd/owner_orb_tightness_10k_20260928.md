# Owner orb-tightness benchmark — 10,000 century charts

Date: 2026-09-28

## Question

How unusual is the recorded owner chart (1985-01-29 05:25 EST Philadelphia / 10:25 UTC) in its density of tight major aspects and its angularity, relative to ordinary birth moments in the same 100-year search universe?

## Method

- 10,000 UTC instants sampled uniformly at random from 1926-08-24 10:42 UTC through 2026-08-24 10:42 UTC.
- Fixed RNG seed: 20260928.
- Swiss Ephemeris files, tropical geocentric longitudes.
- Ten bodies: Sun through Pluto.
- 45 unordered planet pairs; nearest of the five major aspects 0/60/90/120/180 degrees.
- Tightness counts at <=0.5, <=1, <=2 and <=3 degrees.
- Angles calculated for Philadelphia (39.9526 N, 75.1652 W), using ASC/MC/DSC/IC.
- A descriptive 3-degree exactness index sums max(0, 3° - orb) over all 45 pairs. It is geometry only, not a validated astrological weight.

## Owner chart

At 10:25 UTC:
- <=0.5° aspects: 2
- <=1° aspects: 4
- <=2° aspects: 9
- <=3° aspects: 11
- 3° exactness index: 18.90985
- Pluto-MC distance: 2.86272°
- nearest planet-angle distance: 2.86272° (Pluto-MC)

At the V3.6 local score optimum, 10:36 UTC:
- the planetary tightness counts are unchanged;
- Pluto-MC distance is 0.0005759° (about 2.1 arcseconds).

## Empirical prevalence in 10,000 sampled charts

| Criterion | Sample at least as extreme | Fraction |
|---|---:|---:|
| >=4 aspects within 1° | 1,368 | 13.68% |
| >=9 aspects within 2° | 247 | 2.47% |
| >=11 aspects within 3° | 386 | 3.86% |
| 3° exactness index >= owner | 230 | 2.30% |
| all three count thresholds (1°/2°/3°) | 148 | 1.48% |
| Pluto-MC <=2.86272° | 162 | 1.62% |
| all three tight-count thresholds AND Pluto-MC <= owner | 1 | 0.01% |
| Pluto-MC <= 10:36 optimum (0.0005759°) | 0 | 0%; Wilson 95% upper bound 0.0384% |

The sample median has 2 aspects within 1°, 4 within 2°, and 6 within 3°. The owner has 4, 9, and 11 respectively.

## Interpretation

The owner chart is not unusual merely because *some* planet is angular: 48.64% of sampled charts had a planet at least as close to any of the four angles as the owner's 2.86° nearest-angle distance.

What is unusual is the conjunction of two specific geometric facts:
1. a dense set of tight major planetary aspects (roughly upper 1.5–4% depending on the frozen metric); and
2. Pluto specifically lying within 2.86° of the MC at the recorded time (1.62% in this sample).

Only 1 of 10,000 sampled moments met both the three tight-count thresholds and a Pluto-MC distance at least as small as the recorded chart. This 0.01% figure is **post-hoc descriptive**, not a valid p-value: these criteria were selected after inspecting the owner chart and after knowing that the V3.6 model contains a Pluto-MC feature.

The 10:36 local optimum is mechanically informative but not independent evidence. The V3.6 score rewards Pluto-MC, so optimizing birth time can naturally drive the score toward the minute when the MC reaches Pluto.

## Recoverability heterogeneity implication

Yes, the geometry makes heterogeneous recoverability plausible under a symbolic reverse-matching model.

Some birth moments have:
- rare combinations of multiple scored planetary features, which can narrow the date;
- rapidly moving angle contacts, which can make the score surface sharp in time;
- feature combinations that are highly discriminative under the frozen rubric.

Other birth moments can have common feature combinations and broad score plateaus, producing many ties or near-ties.

But geometric rarity is not enough. A rare chart becomes behaviorally recoverable only if the behavioral measurements reliably correspond to the rare chart features. Therefore the hypothesis must be tested prospectively across people.

The correct validation outcome is a per-person recoverability distribution, not only an overall hit rate. Predeclare chart-only candidate moderators (tight-aspect density, angular exactness, model information content, score-margin sharpness) and test whether they predict concealed-date rank on untouched participants. Do not define "high-signal people" after seeing who was successfully recovered.

This is consistent with the project's existing responder-heterogeneity and Survey-v2 recoverability safeguards in docs/14_responder_heterogeneity.md and docs/23_survey_v2_recoverability.md.

## Files

- Script: scripts/benchmark_owner_orb_tightness_10k.py
- Full machine-readable result: experiments/astrohd/owner_orb_tightness_10k_20260928.json