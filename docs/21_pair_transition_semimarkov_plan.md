# 21 — Pair-Specific Semi-Markov Relationship Transition Test

## Goal

Test whether frozen Western-astrology and Human-Design pair features improve prediction of **actual relationship transitions** beyond ordinary demographic/exposure information and beyond each individual's own relationship timing.

This is Track T from `docs/20_partner_transition_vs_quality.md`. It does not claim that a relationship is loving, healthy, or good for either person.

## Primary estimand

For a currently separated pair A/B, a target example is:

```text
P(A and B reunite within 12 / 24 / 60 months
  | current state, duration separated, baseline covariates,
    A individual timing, B individual timing, pair-specific features)
```

For initially unpartnered people, analogous targets include first romantic formation and transition to committed/shared life.

The research question is not whether astrology can narrate the event after it occurs. It is whether pair-specific chart information improves held-out transition probabilities.

## Multi-state structure

Start conservatively with states that can be labeled reproducibly:

```text
S0  not together / no active romantic pair
S1  romantic pair / dating / lover
S2  committed or shared-life pair / cohabiting / married
S3  separated
S4  reunited
S5  final dissolution / divorce where documented
S6  death or observation-end competing/censoring state
```

The exact state taxonomy must be adapted to source reliability. Sparse historical data should use fewer states rather than pretending to know fine-grained relationship phases.

## Why semi-Markov

The hazard of a transition is plausibly duration-dependent. A couple separated for two weeks and the same couple separated for ten years should not receive the same baseline reunion hazard.

Use a **clock-reset / time-since-state-entry** formulation for the primary semi-Markov analysis.

For each allowed transition `r -> s` estimate a transition-specific intensity/hazard:

```text
h_rs(u, t | X)
```

where:

- `u` = time since entry into the current relationship state;
- `t` = calendar/age time if needed;
- `X` = frozen covariates.

An intensity-based implementation is preferred initially because transition-specific likelihoods can be fit as simpler survival submodels and compared hierarchically.

## Nested model sequence

Every empirical test compares nested models. Astrology/HD only matters if it improves untouched data.

### M0 — non-astrological baseline

Examples:

- ages and age difference;
- calendar period;
- current relationship state;
- time in current state;
- prior number of breakups/reunions when known;
- geographic/exposure constraints where known;
- marriage/cohabitation status;
- observation/data-quality variables.

### M1 — individual timing only

Add each person's independently calculated future timing, without any cross-person aspects:

- secondary progressions;
- transits to natal chart;
- natal-house/angle activations where birth time is reliable;
- HD life-cycle/individual transit state under frozen rules.

M1 answers whether both people happen to be relationship-active at the same time.

### M2 — static pair structure

Add pair-specific but time-invariant features:

- preregistered synastry features;
- composite/Davison natal features where supported;
- HD static connection fingerprint.

### M3 — dynamic Western pair features

Add only pair-specific time-varying features:

- progressed A → natal B;
- progressed B → natal A;
- progressed A → progressed B;
- progressed composite;
- transits → natal composite;
- transits → progressed composite;
- later Davison layers only if they add held-out value.

### M4 — dynamic Human Design pair features

Add:

- transiting split bridges;
- changing composite Definition topology;
- Center-count changes;
- time-varying pair mechanics frozen from source rules.

### Decision rule

Retain a layer only if it improves out-of-sample prediction against the immediately simpler model. Narrative fit on development couples does not qualify.

## Hard risk sets / decoys

Random strangers are an easy null. The preferred event-level risk set contains people who were genuinely plausible alternatives.

In decreasing order of quality:

1. documented acquaintances/peers in the focal person's social environment at that date;
2. people in the same place/network/industry and plausible age range;
3. birth-data subjects matched on age, geography, calendar time, and relationship availability;
4. synthetic age-matched birth moments as an engineering/development fallback.

For every observed A-B formation/reunion event, ask whether B's pair hazard with A outranks the available decoys at that same time.

## Dataset strategy

### Astro-Databank development data

The ADB schema can supply:

- natal birth data and Rodden rating;
- explicit person-to-person relationship links;
- dated marriage/divorce and other events where available;
- coarse relationship-quality categories for the separate Track Q model.

During 2026 the full ADB export is temporarily unavailable, so use the public large C-sample for pipeline development and request/obtain the full research export when access resumes.

Filter by birth-data quality before using houses/angles. Preserve alternative birth times rather than silently choosing one.

### Other datasets

Seek additional datasets with:

- exact or well-rated birth date/time/place;
- dated relationship transitions;
- partner identity;
- ideally both partners' birth records;
- ideally repeated quality/satisfaction measures.

Do not treat celebrity/public-event data as the only validation population.

## Data splitting

Split by **people/couples**, never merely by event rows, to avoid the same natal chart leaking across train and test.

Recommended development sequence:

```text
60% development/training couples
20% validation/model-selection couples
20% untouched final test couples
```

If sample size is limited, use grouped cross-validation on development data, then reserve a final untouched set.

Freeze all feature rules and hyperparameters before final-test access.

## Time resolution and event uncertainty

Historical event dates are often coarse.

- exact day known: use day-level event interval;
- month known: interval-censor within month;
- year known: interval-censor within year;
- unknown date: usable for static quality/pair analyses but not precise timing calibration.

Do not invent exact wedding/breakup dates from astrological transits.

## Statistical model

Begin with transition-specific flexible survival models using clock-reset duration.

Candidate baseline hazards:

- Weibull/Gompertz for simple development;
- flexible spline/Royston-Parmar style hazards when sample supports them;
- penalized Cox-like transition models as a robustness comparison.

Use regularization/hierarchical shrinkage because the astrological feature space is large and correlated.

Do not start with thousands of gates/aspects/substructures. Add nested feature families only when validated.

## Primary evaluation

For untouched couples report:

- transition-specific log loss / likelihood;
- time-dependent concordance;
- integrated Brier score;
- calibration of 12/24/60-month transition probabilities;
- cumulative incidence / state-occupation calibration;
- partner rank inside the event-specific risk set;
- top-1, top-5, and percentile partner-identification rates;
- incremental performance M1-M0, M2-M1, M3-M2, M4-M3.

The key scientific result is the incremental gain from **M3/M4 pair-specific features** after M1 has already absorbed individual timing.

## Null and falsification tests

Run at least:

1. shuffle partner identities within age/geography strata;
2. shuffle birth times while preserving dates;
3. shift natal dates by random offsets while preserving event dates;
4. use sham pair-dynamic windows;
5. compare true dynamic features with time-shifted versions (e.g. ±1–5 years);
6. test whether apparent gains vanish when collective slow-planet features are removed.

A legitimate pair model should beat these controls on untouched data.

## Prospective test

After historical development, freeze a prospective version and enroll real participants/couples.

For currently separated pairs:

- record current relationship state and separation duration;
- calculate 12/24/60-month reunion hazards before outcomes occur;
- collect whether contact, dating, reunion, cohabitation, and dissolution actually occur;
- preserve misses.

For singles with known candidate partners/exposure sets, predict pair formation prospectively.

## Relationship quality remains separate

Track Q should be developed in parallel but not mixed into the transition likelihood.

A future report can therefore say things such as:

```text
transition model: high reunion hazard
quality model: low predicted mutuality / high conflict burden
```

or:

```text
transition model: low formation hazard
quality model: high conditional quality if relationship forms
```

This distinction directly prevents `likely to be together` from being confused with `good for each other`.

## Joel/Bee use

Do not train the semi-Markov model on Joel/Bee and then claim its Joel/Bee output is validation.

Use Joel/Bee only as:

- a development/debugging case before the empirical model is frozen; or
- a prospective untouched case after the model has been developed on other couples.

The hard-decoy V3 benchmark is an interim symbolic test, not the final semi-Markov model.
