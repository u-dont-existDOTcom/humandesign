# Longitudinal event discrimination policy

Date: 2026-10-01
Status: required development policy for astrology timing experiments.

## Why this exists

A timing model is not useful merely because known events receive high scores. It must also keep **non-events** low.

The 2026-10-01 owner development case exposed the failure directly:
- the relationship-danger model ranked a 2012 period above the actual 2013-2014 dangerous relationship, even though no dangerous relationship existed in 2012;
- the child-birth model ranked January 2011 above the actual 2014-01-12 birth, even though no fatherhood/birth event occurred in 2011.

Those are false positives, not near-hits. A model that rewards true-event coincidences while ignoring stronger false-event peaks is mis-specified.

## Core invariant

For every longitudinal timing model:

> optimize discrimination between target-event windows and verified non-event windows, not score at target events in isolation.

A new indicator is admitted only if it improves discrimination, not merely because it can narrate an observed event.

## 1. Define one endpoint at a time

Each model must predict exactly one declared endpoint, for example:
- relationship formation/onset;
- chronic relationship pressure;
- acute danger/escalation;
- pregnancy/family-state activation;
- exact child-birth timing;
- career transition.

Do not pool endpoints to rescue performance.

## 2. Build the full labeled timeline

Use a fixed time grid appropriate to the endpoint (for example month, week, or day).

Each interval must be one of:
- POSITIVE: target event/state is reliably present;
- NEGATIVE: target event/state is reliably absent;
- UNKNOWN: history is too uncertain to classify.

UNKNOWN intervals are excluded from supervised discrimination metrics. Never silently treat missing memory as a negative.

For the owner development case, currently revealed hard negatives include:
- relationship-danger: 2012 is NEGATIVE because the owner reports no dangerous relationship before Ann;
- child-birth/fatherhood exact-event model: January 2011 is NEGATIVE for the requested son's birth because the son was born 2014-01-12.

## 3. False-positive burden is first-class

Every evaluation must report at least:
- event recall / sensitivity;
- precision / positive predictive value;
- false-positive rate over labeled negative windows;
- false alarms per person-year (or per declared time unit);
- PR-AUC when a continuous score is available;
- Matthews correlation coefficient (MCC) at the frozen operating threshold when binary decisions are made;
- true-event rank/percentile among all eligible windows;
- number of negative windows scoring >= each true-event window ("false peaks above truth").

ROC-AUC may be supplemental, not primary, because sparse-event timelines are highly imbalanced.

## 4. Hard-negative regression gate

The highest-scoring known non-event windows are **hard negatives**.

When a model is changed because of a false positive:
1. rerun the changed model on the motivating true event AND the hard negative;
2. require the true-event discrimination margin to improve;
3. require that the false-positive burden does not worsen elsewhere on the labeled development timeline;
4. a development pass is non-validating and must then be tested on held-out people/events.

A candidate that still ranks a motivating hard negative above the relevant true event is rejected for that endpoint.

## 5. Discrimination margin

For a single positive event window, define:

```
margin = score(true_event_window) - max(score(verified_negative_windows))
```

Interpretation:
- margin > 0: the true event outranks every verified negative window;
- margin = 0: tied with at least one false peak;
- margin < 0: at least one false period outranks the true event.

For multiple positive windows, report each margin and a summary such as median margin; never hide the worst event behind an average.

This margin is a development diagnostic, not a calibrated probability.

## 6. Preconditions and state transitions

Some endpoints have real-world prerequisites. Encode them explicitly rather than allowing impossible false alarms.

Examples:
- acute relationship danger requires a relationship-active state;
- exact biological child-birth timing requires an eligible pregnancy/family precursor state.

However, for a blind historical inference the model may not use the revealed real-world state as an answer key. It must either:
- predict the prerequisite state with a separately frozen upstream model, or
- declare the prerequisite as externally supplied input before scanning.

Thus a danger model should be hierarchical:

```
relationship-active support
    -> chronic-pressure support
        -> acute-trigger support
```

and an exact birth model may be hierarchical:

```
family/pregnancy-state support
    -> eligible biological interval
        -> exact-event trigger
```

A downstream score cannot create an event where the prerequisite state is absent.

## 7. Positive and negative optimization must be symmetric

During model development:
- adding a feature because it raises a true-event score is insufficient;
- removing/downweighting a feature because it creates false peaks is equally legitimate;
- model selection uses the joint discrimination objective;
- a change that improves hits while increasing false alarms can be accepted only under a predeclared cost tradeoff, never by narrative preference.

## 8. Sparse-event evaluation and imbalance

Rare life events create severe class imbalance. Use metrics designed to expose false alarms:
- precision-recall behavior / PR-AUC for score ranking;
- MCC for thresholded balanced discrimination;
- false alarms per person-year for operational interpretability;
- event/window recall so a model cannot become "accurate" by predicting nothing.

Do not maximize ordinary accuracy; a model that predicts "no event" almost everywhere can look excellent under class imbalance while being useless.

## 9. Cross-person validation

Owner history is development data once revealed.

After tuning on owner positives and hard negatives:
- do not claim validation from improved owner retrodiction;
- freeze the model;
- test on untouched people with both positive-event dates and explicit negative/control periods;
- split by PERSON before threshold/weight selection;
- compare against simple calendar/base-rate baselines and randomized/permuted timing baselines.

## 10. Versioning and future predictions

Existing frozen forecasts remain frozen. A discrimination-policy update does not silently rewrite them.

A future forecast is superseded only when:
1. a new model version is fully specified;
2. the full future timeline is rescored;
3. the new prediction artifact explicitly declares supersession before the relevant future peak begins.

Retrospective edits after a peak do not count as prospective predictions.

## Prior-work disposition

Research-before-reinvention: required.
Disposition: adapt + compose.

Established components reused:
- precision/recall and PR-AUC for imbalanced rare-event discrimination;
- MCC for thresholded balanced performance;
- explicit false-alarm rates;
- event-centric time-series evaluation;
- hard-negative regression as a development discipline.

Novel/project-specific remainder:
- applying these controls to astrological timing windows and hierarchical prerequisite states.

External baseline:
- a simple base-rate/calendar model with the same event prevalence and time resolution.


## 11. Event occurrence versus event morphology and impact

A timing model must keep these distinct:

- **event occurrence** — what objectively happened and when;
- **event morphology** — sudden vs prolonged, violent vs nonviolent, acute vs chronic, externally imposed vs gradual;
- **subjective/life-course impact** — how shocking, consequential, disruptive, or transformative the event was for the person.

Do not assume that a model component which improves one revealed case identifies the causal reason it worked.

Example from owner development:
- the father's death was sudden, accidental, shocking, and life-changing;
- a V4 development repair added a Uranian rupture gate and strongly improved the father's exact-date ranking;
- this does **not** establish that suddenness, tragedy, Uranus, or subjective impact caused the improvement.

Required control:
1. mark morphology-specific components as hypotheses;
2. compare a morphology-neutral model with morphology-specific ablations on future/held-out cases;
3. do not transfer a sudden-shock modifier to a prolonged/non-shocking event merely because the endpoint is also death;
4. separately score event detection and morphology/impact classification when data allow;
5. a morphology-specific repair that fits one revealed case remains development-only until cross-person evidence shows incremental discrimination.

## 12. Post-reveal repair must improve contrasts, not explanations

After a revealed miss, a plausible narrative mechanism is not enough.

A repair is useful only if it:
- raises the true event relative to the motivating false peak;
- does not create an equal or larger false-positive burden elsewhere;
- survives dependency and causal-window checks;
- is frozen before being evaluated on new cases.

When the repair depends on a revealed qualifier such as suddenness, prolonged illness, violence, travel, pregnancy, or relationship-active state, preserve that qualifier as the exact scope of the hypothesis. Do not generalize it to the broader event class until an ablation or held-out comparison earns that transfer.
