# Owner orb-tightness benchmark — 10,000 century charts

Date: 2026-09-28

## Question

How unusual is the recorded owner chart (1985-01-29 05:25 EST Philadelphia / 10:25 UTC) in its density of tight major aspects and angularity, and how does that relate to the **current V1.4d six-rule method**?

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

The sample median has 2 aspects within 1°, 4 within 2°, and 6 within 3°. The owner has 4, 9, and 11 respectively.

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

The 0.01% combined figure is **post-hoc descriptive**, not a valid p-value: the conjunction of criteria was chosen after inspecting the owner chart.

A supplementary same-seed pass checked the two specific sub-1° geometries that activate the current six-rule model at the owner moment. Venus–Mars conjunction within 1° occurred in 108/10,000 charts (1.08%); Saturn–Venus trine within 1° occurred in 103/10,000 (1.03%); **none of the 10,000 had both simultaneously** (0/10,000; Wilson 95% upper bound ~0.0384%). This pairwise combination was inspected after the owner rules were known, so again it is descriptive rather than an independent significance test.

## Relation to the CURRENT six-rule method

The current project authority is V1.4d, not the older V3.6 merged model. V1.4d's exact minute-grid search evaluates 52,596,001 minutes across the century and leaves nine maximum-score minutes, all on 1985-01-29 from 10:18 through 10:26 UTC. The cold continuous plateau is approximately 10:17:52–10:26:12 UTC. It does **not** select the older V3.6 10:36 local optimum.

Orb tightness is directly relevant to **two of the six current rules** because the Lilly implementation defines the selected benefic aspect conditions as partile, operationalized with a <=1° orb:

1. `lilly/planet:saturn/benefic_trine` — at the owner moment, Saturn trines Venus by about **0.66°**, so this rule is active.
2. `lilly/lord:10/benefic_conjunction` — the Regiomontanus 10th cusp is in Scorpio, making Mars the traditional 10th lord; Mars is conjunct Venus by about **0.45°**, so this rule is active.

The other four selected rules are house/directional-strength conditions rather than generic aspect-orb rules:
- `lilly/lord:3/house_1_10`
- `lilly/planet:venus/house_2_5`
- `phaladeepika/planet:venus/directional`
- `lilly/lord:7/house_4_7_11`

Therefore the owner's dense tight-aspect geometry is not merely visually interesting: **two of the six Boolean votes in the current fitted model depend on sub-1° aspect geometry.** However, the model was target-aware fitted to this known owner case, so this cannot be treated as independent evidence that tight aspects predict personality.

Pluto-MC angularity is **not one of the six V1.4d rules**. The earlier observation that the legacy V3.6 score peaked near 10:36 when Pluto reached the MC remains a valid explanation of that older model's score surface, but it should not be used to explain the current six-rule recovery.

## Recoverability heterogeneity implication

The geometry makes heterogeneous recoverability plausible under a symbolic reverse-matching model.

Some birth moments can have:
- rare combinations of multiple scored features, narrowing the date;
- partile aspect conditions that turn on only in relatively narrow date windows;
- house/angle boundaries that create narrow time intervals;
- feature combinations with high information content under the frozen rubric.

Other birth moments can have common feature combinations and broad score plateaus, producing many ties or near-ties.

But geometric rarity is not enough. A rare chart becomes behaviorally recoverable only if the behavioral measurements reliably correspond to the rare chart features. The current six-rule result is a known-case development fit and does not establish how often this will happen in new people.

The correct next validation is a **per-person recoverability distribution**. Before revealing outcomes, compute chart-only candidate moderators such as:
- number/density of partile aspects used by the frozen rule library;
- rarity of the person's full rule signature in the century universe;
- size/duration of the maximum-score plateau;
- number of tied dates/minutes;
- score margin to the nearest competing dates.

Then test prospectively whether those frozen moderators predict concealed-date recovery on untouched participants. Do not define "easy people" as the people who happened to recover successfully.

This is consistent with the project's existing responder-heterogeneity and Survey-v2 recoverability safeguards in `docs/14_responder_heterogeneity.md` and `docs/23_survey_v2_recoverability.md`.

## Legacy V3.6 diagnostic retained separately

For historical comparison only: at the older V3.6 local score optimum (10:36 UTC), Pluto-MC is almost exact (~0.000576°). Zero of the 10,000 random charts had Pluto-MC that close (Wilson 95% upper bound ~0.0384%). This is not part of the current six-rule model and was selected by an older score that explicitly rewarded Pluto-MC.

## Files

- Script: `scripts/benchmark_owner_orb_tightness_10k.py`
- Full machine-readable result: `experiments/astrohd/owner_orb_tightness_10k_20260928.json`
- Current six-rule authority: `tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V14-SIX-RULE-MODEL-20260925.json`
- Exact century result: `experiments/astrohd/v14_exact_century_20260925/result.json`
