# Lilly horary retrospective pilot — method freeze — 2026-09-24

Status: **FROZEN BEFORE OUTCOME RETRIEVAL / EXPLORATORY RETROSPECTIVE PILOT / NOT VALIDATION**.

## Owner outcome
Run a blinded retrospective precursor to a prospective William-Lilly-style horary test, using archived questions asked before their outcomes and freezing predictions before outcome reveal.

## Evidence boundary
This pilot tests one finite operationalization of Lilly 1647 horary, not astrology in general and not the prior natal birth-recovery scorer. Forum cases are self-selected and outcomes are author-reported, so even a strong result remains exploratory.
Cases whose outcomes or decisive result-bearing replies were exposed during corpus discovery before prediction freeze are contaminated and excluded from the blind score.

## Existing-work disposition
Reuse/adapt the open-source Moira 6.2.0 Lilly 1647 Horary evidence/perfection engine for geometry and six source-defined perfection mechanisms. Moira deliberately provides evidence rather than a yes/no judgement; the only bespoke layer is the frozen binary composition below.
Primary historical authority remains William Lilly, *Christian Astrology* (1647), Books I-II.

## Inclusion rule
Include only public archived forum cases for which the opening post, before outcome reveal, supplies:
1. one concrete binary outcome question;
2. exact question date and clock time;
3. location or coordinates sufficient for the chart;
4. a straightforward radical topic house under the frozen map below;
5. a later outcome report that can be coded YES/NO without interpretive repair.

Exclude compound questions, timing-only questions, “should/why/how” questions, medical/pregnancy, legal or financial-advice questions, cases requiring topic-specific significator exceptions, cases with unresolved time/location, and any case already outcome-exposed to the scorer during discovery.

Frozen topic-house map:
- relationship / reconciliation with another person -> radical 7;
- job offer / hiring / getting the job -> radical 10;
- journey / travel occurring -> radical 9;
- lost personal movable possession recovered -> radical 2.
No other topic is admitted in v0.

## Chart and doctrine
- tropical zodiac; traditional seven planets;
- exact Regiomontanus houses;
- querent = ruler of Ascendant; co-significator = Moon;
- quesited = classical ruler of the frozen radical topic-house cusp;
- Moira profile `lilly_1647_perfection_v1`;
- exact question instant and source location;
- maximum perfection trace = 31 days, Moira's admitted v1 bound;
- considerations/hour agreement are recorded but do not flip the v0 verdict.

## Frozen verdict law
For the principal querent/quesited pair, inspect Moira's source-defined perfection witnesses.
- **YES** if at least one of DIRECT, TRANSLATION, or COLLECTION is PRESENT.
- **DEFER** if none of those is PRESENT and at least one is INDETERMINATE, or if the principal pair/evidence profile is not evaluable.
- **NO** otherwise.

PROHIBITION, REFRANATION, and FRUSTRATION are not separately reweighted: Moira already incorporates admitted interruptions into the relevant perfection classifications. Reception, dignity, planetary-hour agreement, and considerations are retained as diagnostics only and may not rescue or reverse the primary verdict.
No rule, house assignment, time window, or inclusion criterion may change after the first outcome is opened. Any revision becomes v1 on a new untouched sample.

## Freeze/reveal sequence
1. Save the eligible input corpus with source URLs and only opening-post metadata.
2. Hash the corpus.
3. Run the frozen engine and save a prediction record for every case.
4. Hash the predictions.
5. Only then retrieve later outcome posts.
6. Code outcomes independently of the predictions and save their provenance.
7. Join by case id and score.

Primary metric: exact accuracy among non-DEFER predictions. Also report coverage, exact binomial 95% CI, two-sided binomial p-value versus 0.5, class balance, sensitivity/specificity when defined, and accuracy of the majority-outcome baseline. Do not treat p<0.05 in this exploratory selected corpus as validation.

Stop condition: score the pre-frozen corpus once. Do not add favorable cases after reveal to improve the result.
