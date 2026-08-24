# NCDS VITALITY 5-15 validation eligibility result

**PHASE: VALIDATION — ELIGIBILITY CHECK ONLY**

Date: 2026-08-24

Frozen protocol: `reference/validation/ncds_vitality_5_15_freeze_v1.json`

## Result

**INELIGIBLE under the ordinary longitudinal NCDS release. No individual age-50 or age-62 outcome values were accessed.**

The frozen protocol required verification that the recorded delivery time/date from Question 7 of the 1958 Perinatal Mortality Survey was available in a dataset that can be linked to later NCDS outcomes.

The check failed:

1. The annotated 1958 Perinatal Mortality Survey visibly includes Question 7, `Time and date of delivery`.
2. In that annotated questionnaire, variables carried into the longitudinal NCDS data are shown with blue variable identifiers beside the corresponding questionnaire items. Question 7 has **no linked variable identifier**.
3. The NCDS Perinatal Mortality Survey additional-variables guide states that the ordinary longitudinal childhood file SN 5565 contains only 62 selected variables from the birth questionnaire and explicitly notes that not every birth question was keyed.
4. The additional 2014 PMS deposit contributes 51 more longitudinally linkable variables, but its published inventory covers other obstetric/birth fields and does not add Question 7 delivery time/date.
5. The older PMS SN 2137 contains more detailed birth data but uses a different identifier and the UK Data Service documentation explicitly states that it cannot be linked longitudinally to NCDS outcomes.

Therefore the standard NCDS data route cannot evaluate a birth-time-dependent predictor against the age-50 SF-36 Energy/Fatigue outcome.

## Epistemic consequence

This is **not a failed 5-15 replication**. It is a failed dataset-eligibility check before outcome access. The frozen predictor remains unchanged and may be carried to another independent cohort.

The NCDS cohort could become eligible only if an authorized special linkage/research extract supplies the original Question 7 delivery time/date tied to `ncdsid` (or another verified longitudinal identifier) without exposing outcomes during predictor construction. Such access would use the already-frozen formula and analysis rather than retune it.

## Public evidence inspected

- CLS annotated 1958 Perinatal Mortality Survey, page containing Question 7.
- UK Data Service/CLS `NCDS Perinatal Mortality Survey User Guide: Additional Variables`, especially sections 5-8 and its variable inventory.
- UK Data Service description of SN 2137 noting the absence of a linking variable to NCDS.
