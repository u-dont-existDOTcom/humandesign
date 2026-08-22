# 20 — Forward-Blind Prospective Human Design Validation

Date: 2026-08-22

## Decision

Add a **forward-blind human validation track** as the easiest primary test of whether a birth-derived Human Design chart contains out-of-sample behavioral information.

This track is distinct from reverse matching. The participant supplies their actual birth data up front, but the system never reveals the resulting HD chart or its expected behavioral interpretation until after the prediction and response records are frozen.

The research question is:

> Given independently supplied DOB, exact birth time, and birthplace/timezone, does the resulting concealed HD chart predict the participant's blinded questionnaire responses better than matched alternative charts and non-HD baselines?

A positive result here is much easier to interpret than a 100-year reverse search and should become the preferred first prospective human validation route once the V4.3/V3.6 mapping/scoring implementation is frozen.

## Why this track exists

Reverse matching asks a very difficult identification question:

```text
behavior -> search a large birth-state universe -> recover true birth state
```

Forward-blind validation asks the simpler causal/predictive question first:

```text
known birth state -> concealed HD chart -> frozen behavioral predictions
                                 |
                                 v
                         blinded questionnaire
                                 |
                                 v
                       prospective evaluation
```

If forward-blind prediction is at chance, broad reverse matching should not be treated as evidentially persuasive merely because a complicated search can find a high-scoring state. If forward-blind prediction succeeds on untouched participants, reverse matching becomes a stronger secondary test.

## Scientific claim boundary

A successful forward-blind test would support only the claim that the frozen chart-derived model contains predictive information about the measured responses beyond the declared controls.

It would not by itself establish:

- the metaphysical explanations of Human Design;
- the practical superiority of Strategy/Authority;
- Color/Tone/Base validity unless those layers were separately enabled and tested;
- relationship mechanics;
- past-life or reincarnation claims.

Those remain separate hypotheses.

## Participant flow

### 1. Intake

Collect before any chart interpretation is shown:

- date of birth;
- exact local birth time;
- birthplace;
- resolved historical IANA timezone;
- birth-time source quality: certificate/hospital record, family record, memory, rectified, unknown;
- stated uncertainty if known, e.g. `±2 minutes`;
- prior Human Design familiarity;
- whether the participant already knows their Type/Profile/Authority or deeper chart details;
- optional predeclared demographic/control variables needed for nuisance matching.

Do not display the calculated chart during intake.

### 2. Calculate the true chart privately

Use only the verified production chart engine:

- pinned Swiss `.se1` files;
- requested/returned mode must both be SWIEPH;
- exact 88-degree Design root;
- frozen true/mean Node convention;
- frozen Rave Mandala constants;
- complete required feature registry for the model version being tested.

Create a `true_chart_feature_hash` from the canonical feature vector.

### 3. Freeze the prediction package before answers

The participant must not answer the scored questionnaire until all scored expectations are immutable.

Freeze and hash at minimum:

- normalized birth-input hash;
- chart-feature hash;
- ephemeris provenance hash;
- model/mapping-library hash;
- scoring-policy hash;
- questionnaire-bank hash;
- selected-question-set hash;
- predicted response distribution or option-support map for every scored question;
- dependency-cluster assignments;
- reliability policy;
- decoy/control-panel specification and seed/hash;
- software commit;
- timestamp.

The freeze must occur before response collection.

### 4. Administer a participant-blind questionnaire

Do not show:

- Type;
- Strategy;
- Authority;
- Profile;
- Centers;
- Gates/Channels;
- Variable/PHS labels;
- the option direction favored by the real chart;
- live score or rank.

Questions must be behavior-first and concealed-direction.

Bad:

> Do you wait for invitations?

Better:

> Think of several opportunities that became important. Which entry pattern most often occurred?

Bad:

> Are you emotionally defined?

Better:

> For major decisions, how does certainty usually change between the first moment and later hours/days?

Question option ordering should be randomized from a frozen per-participant seed when feasible. `Unknown`, `mixed`, or `not enough evidence` must remain legitimate responses and must not be coerced into chart support.

### 5. Freeze responses

Before any chart reveal or model change, store and hash:

- raw responses;
- coded responses;
- optional concrete examples/counterexamples;
- response timestamps;
- skipped/unknown items;
- response-record hash.

### 6. Evaluate

Evaluate the true chart against preregistered null/control comparisons. Do not alter mappings after inspecting the participant.

### 7. Reveal

Only after the prediction package, response record, and evaluation output are frozen may the participant see their chart and the scoring explanation.

The reveal should make the temporal order obvious:

```text
prediction sealed -> questionnaire answered -> score frozen -> chart revealed
```

## Primary evaluation modes

The project should support both direct predictive scoring and chart identification. They answer related but different questions.

### A. Direct prospective response prediction

If calibrated `P(answer | chart features)` values exist, use proper scoring rules such as:

- multiclass log loss;
- Brier score;
- per-question calibration;
- aggregate held-out likelihood.

Compare the true HD model against:

- response-frequency-only null;
- demographic/control model where collected;
- shuffled chart assignment;
- reduced HD models M0/M1/M2;
- empirical/hybrid models only when trained entirely outside the test participant.

If probabilities are not calibrated, do not pretend symbolic support values are probabilities. Use the frozen NetInformation/rank framework and label it accordingly.

### B. Participant-chart identification matrix

For a cohort of `N` untouched participants:

1. calculate all `N` concealed charts independently;
2. score each participant's response vector against all `N` charts using the same frozen model;
3. form an `N x N` response-to-chart score matrix;
4. rank the participant's own chart among the other participants' charts.

This is especially clean because the decoys are real participant charts rather than cherry-picked synthetic alternatives.

Report:

- median true-chart percentile;
- Top-1 / Top-3 / Top-5 identification;
- mean reciprocal rank;
- true-vs-off-diagonal score margin;
- exact/permutation significance for the diagonal advantage;
- optional assignment-level accuracy using a frozen one-to-one matching rule.

The participant-chart identity labels must not be used to tune the questionnaire or model on the untouched cohort.

## Matched decoy panels

The cohort matrix should be primary when sample size allows. For single-participant or small-cohort experiments, use a frozen decoy panel.

Do not use only one arbitrary decoy distribution. Preserve at least two panels:

### Panel 1 — nuisance-matched local-time controls

Sample alternative birth instants while holding major nuisance variables as tightly as practical, for example:

- same birthplace/timezone;
- same birth year;
- preferably same month for the most conservative age/season control;
- exact timestamps sampled independently from a frozen seed.

This asks whether the true chart beats nearby calendar alternatives that share age/cohort and much seasonal structure.

### Panel 2 — broad chart controls

Sample from the verified broad chart universe/cache using a frozen seed and declared weighting rule.

This asks whether the participant resembles their own chart more than a wide range of HD architectures.

Report both. A result that appears only in the broad panel but disappears against matched nearby dates may reflect season/cohort/calendar structure rather than HD-specific information.

## Permutation/null procedure

At cohort level, the preferred null is chart-label permutation:

```text
responses fixed
charts fixed
randomly permute chart <-> participant identity
repeat many times
```

Predeclare the number of permutations, e.g. 10,000 where computationally feasible.

Primary group statistic candidates include:

- sum/mean diagonal-minus-off-diagonal score;
- mean true-chart percentile;
- Top-k count;
- total held-out log score.

Choose the primary statistic before looking at final validation outcomes.

## Cohort policy

Maintain three human groups:

### DEVELOPMENT

Known outcomes may be inspected. Use this group to improve:

- question wording;
- construct definitions;
- mapping directions;
- reliability estimates;
- empirical probabilities;
- option randomization UX;
- decoy sampling policy;
- model regularization.

Development performance is not final evidence.

### VALIDATION

Freeze the complete model before opening outcomes. Use once for model selection/confirmation.

If validation motivates changes, create a new version and obtain new untouched participants.

### FINAL UNTOUCHED TEST

No question selection, mapping fitting, probability fitting, threshold choice, or model simplification may use this cohort before the final freeze.

## Prior HD knowledge

HD familiarity is a major contamination risk because a participant who already knows they are a Projector/2/4/etc. may consciously or unconsciously answer toward the expected theory.

Therefore:

- record familiarity before testing;
- preregister a primary `HD-naive` analysis where feasible;
- analyze knowledgeable participants separately or as a secondary cohort;
- do not mix prior chart knowledge into the primary untouched claim without reporting it.

The best recruitment target for the strongest initial test is people with documented birth times who do **not** already know their detailed Human Design chart.

## Birth-time uncertainty

Forward-blind testing does not require pretending an uncertain time is exact.

If documented uncertainty crosses chart boundaries:

1. enumerate every exact chart state inside the input uncertainty interval;
2. report predictions that are invariant across the interval separately from time-dependent predictions;
3. do not score a time-sensitive item as though one unverified substate were known;
4. for Color/Tone/Base, require stability across the uncertainty interval or mark that substructure unresolved.

## Layer-wise validation

Never make the full HD stack one indivisible claim. Report nested models:

```text
F0  Type + Strategy + Authority + Centers + Profile
F1  F0 + Definition + Channels
F2  F1 + Gates + Lines + planetary carriers + Nodes/Cross
F3  F2 + line fixing where validated
F4  F3 + Color/Tone/Base + Variable/PHS/Rave Psychology, only after Base-level engine parity
```

For each held-out cohort ask whether the deeper layer improves predictive performance beyond the shallower layer.

A deeper layer earns validation status only if it improves untouched/prospective results. Retrospective richness is insufficient.

## Color/Tone/Base integration rule

Color/Tone/Base is **off by default** in forward-blind validation until `docs/19_base_level_substructure_validation.md` passes its engineering activation gates.

Once engineering parity is established, behavioral validation remains separate:

1. source/freeze the exact CTB -> Variable/PHS/Rave Psychology mappings;
2. build concealed questions for downstream claims that are concrete enough to observe;
3. freeze them on DEVELOPMENT participants;
4. test `F4` against `F3` on untouched participants;
5. require positive incremental out-of-sample value before declaring CTB behaviorally useful.

Do not validate Base merely by showing that the Base calculation is reproducible. Calculation parity and behavioral prediction are different claims.

## Recommended CTB behavioral endpoints

Prefer concrete downstream constructs over free-form raw-Base storytelling.

Examples, only after source verification and preregistration:

- dietary/determination response patterns;
- sensory/cognition discriminators;
- environment preference/functional performance under contrasting environments;
- perspective/view contrasts;
- motivation/transference contrasts;
- Left/Right orientation contrasts where canonically derived.

Each construct should have a neutral multi-option question or behavioral task with concealed direction. Avoid asking participants to endorse Human Design jargon.

Raw Base-level archetypal descriptions should remain exploratory until they demonstrate independent prospective discrimination.

## Prospective CTB interventions

Some CTB/PHS claims are more naturally tested as repeated within-person experiments than as personality survey items.

Where safe and low-stakes, predeclare an A/B or randomized crossover procedure:

```text
condition predicted to fit the participant
vs
matched alternative condition
```

Measure concrete outcomes such as comfort, task performance, adherence, sensory clarity, or reproducible preference. Keep these separate from medical or nutritional treatment claims; no high-stakes health recommendation may be made from HD.

A repeated-measures design can be more powerful than a one-time trait questionnaire because each participant acts as their own control.

## Data leakage prohibitions

During untouched forward-blind runs:

- no chart reveal before response freeze;
- no use of participant identity/history outside the declared intake fields;
- no model edits after seeing answers;
- no hand-written interpretation tailored to the participant;
- no candidate-specific follow-up question unless the selection algorithm and answer mapping were already frozen;
- no discarding failures because the participant is said to be `not-self`;
- no defining `good responders` from their observed match score and then using that same definition as proof.

## Output contract

Each forward-blind run should leave an auditable package containing:

```text
participant_id_pseudonym
intake_hash
birth_time_source_quality
birth_time_uncertainty
hd_familiarity_level
true_chart_feature_hash
engine_provenance_hash
model_hash
question_bank_hash
selected_question_set_hash
prediction_package_hash
response_record_hash
decoy_panel_hash / cohort_chart_set_hash
software_commit
score_method
true_chart_rank
true_chart_percentile
null/permutation result
layer-wise results
reveal_timestamp
```

Never commit personally identifying participant data or secret pre-reveal answer keys to the public repository.

## CLI/API target

After the current V4.3 migration is integrated, implement a first-class module rather than a one-off script.

Suggested package:

```text
src/hdmatch/forward_blind/
    intake.py
    prediction.py
    questionnaire.py
    controls.py
    evaluate.py
    reveal.py
```

Suggested CLI:

```bash
hdmatch forward-prepare --intake participant.json --model frozen_model/ --out run/
hdmatch forward-questionnaire --run run/
hdmatch forward-freeze-responses --run run/ --responses responses.json
hdmatch forward-evaluate --run run/ --decoys matched --n-decoys 999
hdmatch forward-reveal --run run/
hdmatch forward-cohort-evaluate --runs runs/validation_cohort/
```

The implementation should reuse, not duplicate:

- chart engine;
- V4.3 mapping/scoring library;
- freeze/hash primitives;
- questionnaire bank;
- reliability/dependency controls;
- verified century cache where broad decoys are requested;
- permutation/evaluation utilities.

## Priority relative to reverse matching

Once the V4.3 model is frozen and the engineering prerequisites pass, the recommended human-validation order is:

```text
1. forward-blind known-birth prediction
2. known-date hidden-time rectification
3. month/year concealed-date recovery
4. broader reverse matching
5. relationship prospective validation
```

Forward-blind validation is computationally cheaper and tests the core predictive premise more directly. Broad reverse matching remains valuable as a stronger information-recovery demonstration if the simpler prospective prediction survives untouched testing.
