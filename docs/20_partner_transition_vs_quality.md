# 20 — Partner Transition Prediction vs Relationship Quality

## Purpose

Separate two questions that ordinary compatibility/synastry readings often collapse:

1. **Pair-transition question:** will two specific people enter, re-enter, remain in, or leave a romantic relationship?
2. **Relationship-quality question:** conditional on being together, is the relationship mutually loving, reciprocal, safe, satisfying, stable, and beneficial to both people?

These are different outcomes and require different models.

A pair can have a high probability of forming/reforming while having poor relationship quality. Conversely, a pair could have high potential quality if they formed but a low probability of actually meeting or choosing one another.

## Track T — Pair-transition model

The transition model predicts movement among observed relationship states such as:

```text
not together
→ opening/dating
→ committed/shared life
→ separated
→ reunited
→ final separation
```

The preferred empirical formulation is a competing-risk multi-state survival / semi-Markov model. Transition hazards may depend on:

- current state;
- time already spent in that state;
- age/life stage;
- each person's independent relationship-activation state;
- static pair features;
- pair-specific dynamic features;
- prior relationship history where known.

The astrology/HD contribution of interest is the **incremental pair-specific hazard after individual timing has already been modeled**.

Do not interpret a high transition score as evidence that the relationship is healthy or desirable.

## Track Q — Relationship-quality model

Quality must be trained and tested against outcomes that measure the relationship itself rather than mere persistence.

Candidate outcome dimensions:

- mutual affection/love;
- sexual/romantic fulfillment;
- reciprocity and perceived fairness;
- emotional safety;
- trust/honesty;
- conflict frequency and repair quality;
- autonomy versus coercion/control;
- mutual support;
- satisfaction for partner A;
- satisfaction for partner B;
- stability without chronic rupture;
- whether each partner reports that the relationship improves or worsens their life.

A quality model should preserve **both partners' reports separately** before forming a dyadic summary. A relationship that is excellent for one person and damaging for the other must not receive a misleadingly high average score.

Preferred outputs include:

```text
quality_A
quality_B
mutuality = min(quality_A, quality_B)
conflict/instability burden
separation hazard conditional on quality
```

No symbolic quality scalar should be called validated until trained on development couples and tested on untouched couples.

## Why persistence is not quality

Observed duration can be caused by love and compatibility, but also by:

- financial dependence;
- children/family obligations;
- social pressure;
- fear;
- repeated rupture/reunion;
- limited alternatives;
- habit;
- coercive dynamics.

Therefore the Track T semi-Markov model and Track Q quality model must remain distinct even if they later share some predictors.

## Pair-specific residual principle

Before asking whether a pair has unusual dynamic timing, first control for what each individual would experience with many possible partners.

For a focal pair A/B:

1. calculate A's individual future-state timeline;
2. calculate B's individual future-state timeline;
3. select hard decoys whose individual timelines closely resemble B (when testing A→B) or A (when testing B→A);
4. compare only pair-specific dynamics after hard matching;
5. run the reciprocal direction;
6. preserve negative results.

This prevents `both happen to have strong relationship years` from masquerading as evidence for the specific pair.

## Pair-specific dynamic Western layers

Predeclared candidate layers for Track T include:

- secondary progressed A → natal B;
- secondary progressed B → natal A;
- progressed A → progressed B;
- progressed composite;
- transits to natal composite;
- transits to progressed composite;
- Davison/transit layers as a separately tested extension.

These layers should be added hierarchically and retained only if they improve out-of-sample transition prediction.

## Pair-specific Human Design layers

Use separately from Western astrology:

- static connection fingerprint;
- transiting split bridges;
- changing composite Center count;
- changing Definition topology;
- temporary electromagnetic/compromise/dominance mechanics where mechanically defined;
- life-cycle chart interactions only under a frozen rule.

Do not convert Ra's relationship keynotes into a probability of love or health without empirical calibration.

## Hard-decoy benchmark

The first development benchmark is specified in:

`reference/research/partner_hard_decoy_residual_freeze_v3.md`

It tests whether Joel/Bee pair-specific dynamic timing is unusual after matching decoys on individual 2026–2040 future trajectories.

## Best eventual empirical design

Use relationship datasets with birth data and dated transitions. Build on development couples, freeze the model, then evaluate on untouched couples.

For each transition event, use a risk set of realistic alternatives rather than arbitrary strangers whenever possible. Ideal decoys are people the focal person plausibly could have partnered with, or at minimum people matched on age, location/exposure, and individual relationship timing.

The strongest claim is not `this pair has interesting synastry`; it is:

> Conditional on ordinary demographic/exposure factors and both individuals' independent relationship timing, the frozen pair-specific model assigns unusually high hazard to the transition that actually occurs, and it does so out of sample.

Track Q should then independently test whether the same or different chart features predict mutual relationship quality.
