# Relationship Timing V3 — empirical contrastive freeze

Date: 2026-10-01
Status: development model; future empirical scan not yet inspected at this freeze.
Model family: positive-vs-background regularized classifier.
Scientific validity: not established.

## Why V3 changed

The hand-weighted V3 state-gate candidate repaired the old 2004 and 2010/11 false peaks but still generated too many high historical windows. It is retained as a failed development candidate and does not supersede V2.

V3 therefore changes the optimization target from "large astrology score" to **contrast between known major relationship windows and the entire historical background**, while separately tracking false peaks.

## Endpoint

Major relationship / romance activation.

Development positive windows:
- 2005-06 through 2005-09;
- 2013-03 through 2013-08;
- 2018-04 through 2018-07;
- 2025-12 through 2026-02.

These windows encode approximate event uncertainty and are development labels, not independent validation.

All other 2000-01 through 2026-09 months are used as **background**, not asserted to be verified negatives. Explicitly rejected historical peaks remain hard-negative diagnostics.

## Feature families

All features are derived from the already frozen relationship targets:
- natal Venus;
- natal Moon / 7th ruler;
- ASC/DSC axis.

Three-month centered window.

Slow transit features:
- Jupiter, Saturn, Uranus, Neptune, Pluto;
- conjunction/sextile/square/trine/opposition <=1°;
- exactness-weighted contact strength to Axis, Venus, Moon;
- body-specific contact indicators.

State features:
- annual profection relevance;
- secondary-progression relationship contact;
- personal solar-arc relationship contact;
- solar-arc angle contact.

Fast-trigger features:
- transiting Venus and Mars major aspects <=1° to Axis, Venus, Moon;
- exactness-weighted strengths.

Dependency rules from the progressed-chart policy remain active.

## Gated interaction

State evidence and trigger evidence are not treated as independent additive coincidences.

Define:
- `state_count` = number of active state families;
- multiply slow/fast target-strength features by `state_count`.

The empirical feature vector is:

- state_count
- state_count × slow Axis strength
- state_count × slow Venus strength
- state_count × slow Moon strength
- state_count × fast Axis strength
- state_count × fast Venus strength
- state_count × fast Moon strength
- Jupiter contact count
- Saturn contact count
- Uranus contact count
- Neptune contact count
- Pluto contact count

## Estimator

- standardize features from development data;
- logistic regression used only as a discriminant, not as a calibrated probability;
- L2 regularization;
- C = 1.0;
- class_weight = balanced;
- liblinear solver.

C=1.0 was selected on development-only blocked leave-one-event-era-out comparison after dependency correction. It tied the best worst-case held-out event rank (~90.5th percentile) and gave the best mean event-era average precision among the tied candidates.

## Development cross-check

Five-year-ish event-era holdouts:

- 2005 era: best held-out positive month outranked ~92.9% of background months in its test era; 4 background months scored higher.
- 2013 era: held-out event outranked 100% of background months in its test era.
- 2018 era: held-out event outranked 100% of background months in its test era.
- 2026 era: held-out event outranked ~90.5% of background months in its test era; 4 background months scored higher.

Mean event-era average precision was ~0.48 versus a much lower event prevalence baseline.

Interpretation: V3 is materially more discriminative than raw hit-counting, but **not clean enough to claim that every major relationship event will be uniquely identifiable**.

## Precision tiers

Because zero false alarms would miss multiple true development events, V3 does not use a single binary "astrology says event" cutoff.

After final fitting on all development data, define future tiers by the distribution of **background discriminant scores**:

- Tier A: >=99th percentile of development background.
- Tier B: >=95th and <99th percentile.
- Tier C: >=90th and <95th percentile.
- Below Tier C: do not surface as a major peak.

These are empirical rarity tiers, not event probabilities.

## Future-alert rule

For the retrospective astrology reminder:
- Tier A and Tier B future peaks are eligible for post-peak reminders;
- Tier C may be retained in the research artifact but does not trigger a reminder by default;
- reminder occurs only after the predicted window has passed;
- later model versions may supersede future windows only if frozen before those windows begin.

## Supersession

V3 supersedes V2 for future relationship-peak monitoring only after the V3 future scan artifact is written from this exact frozen specification.

V2 remains preserved as historical provenance.


## Pre-scan dependency correction

Before the empirical future scan, the implementation check found that `state_count` could accidentally count the solar-arc family twice when both `sa_personal_any` and `sa_any_axis` were true.

Correct rule:
```
state_count =
    profection_active
    + progression_family_active
    + solar_arc_family_active
```

Each timing family contributes at most one unit. Solar-arc subfeatures remain available for defining whether that family is active but cannot increase the family count beyond one.

The blocked development comparison was rerun after this correction. No future empirical scores had been generated yet. The corrected comparison selected C=1.0 as stated above.
