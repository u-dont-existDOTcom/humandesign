# 33 — Automatic Relationship Learning Loop

Status: development architecture. This document defines how relationship cases may improve future model versions without allowing same-case post-hoc mutation of the active model.

## Goal

Automate the kind of learning that occurred manually during development cases:

- discover when one outcome axis actually contains two different constructs;
- detect recurrent directional asymmetries;
- detect context/state moderators such as distance, familiarity, cohabitation, attachment activation, or third-party threat;
- identify frozen symbolic predictors that repeatedly miss;
- identify important narrative patterns that the current rubric cannot classify;
- propose new questionnaire follow-ups or model feature families;
- evaluate proposed revisions on data not used to generate the proposal;
- promote only a new version after explicit evaluation and freeze.

The system must **learn from cases without silently rewriting itself while scoring those same cases**.

## Relationship analogue of the existing empirical-learning track

The natal empirical-learning track estimates quantities of the form:

```text
P(response | chart features)
```

The relationship analogue is:

```text
P(axis outcome, direction, trajectory, context | pair features, natal moderators, context)
```

where the pair feature set may contain separately identifiable layers:

- HD connection mechanics;
- Western directional synastry;
- composite/Davison shared-field features where birth times permit;
- natal person-level moderators;
- non-symbolic relationship-science baselines;
- ordinary context covariates.

Do not merge these layers before ablation testing.

## Case lifecycle

Every consenting development case should pass through these stages:

1. **Raw narrative freeze**
   - preserve verbatim questionnaire responses and context metadata;
   - hash/freeze before chart reveal when the study mode requires chart-blind capture.
2. **Blind phenotype classification**
   - map narrative to the frozen relationship outcome rubric;
   - preserve confidence, counterevidence, context, observability limits, `Other`, mixed, and unresolved states.
3. **Frozen prediction evaluation**
   - compare each model/version's pre-existing predictions with the frozen phenotype;
   - record hit/miss/partial/unresolved/not-predicted separately for every axis/direction/context.
4. **Error-ledger accumulation**
   - append the case to the development learning ledger;
   - aggregate errors only after the case's evaluation is immutable.
5. **Discovery/proposal generation**
   - identify repeated failure structures across development cases;
   - generate candidate V-next revisions, never edits to the currently frozen model.
6. **Development holdout evaluation**
   - generate proposals on one development subset and test them on other development cases not used to formulate the proposal;
   - use grouped/person-level splitting so multiple relationships from one respondent cannot leak across train/test when that would matter.
7. **Promotion gate**
   - a proposal becomes a new explicit model/questionnaire version only after it improves predeclared held-out metrics enough to justify added complexity;
   - after promotion, freeze it before any untouched validation cohort.

## Deterministic automatic signals

The first learning layer should not require an LLM. It should compute structured diagnostics from frozen case evaluations.

### Per axis/direction/model

Track:

- scored case count;
- hit count;
- miss count;
- partial/mixed count;
- unresolved/insufficient count;
- not-predicted count;
- classifier confidence distribution;
- answerability rate;
- trajectory frequencies;
- context-condition frequencies;
- observability-limitation frequencies;
- predicted ordinal versus observed ordinal error where both are available;
- calibration/proper score when the model emits actual probabilities.

### Recurrent failure triggers

Flag, but do not auto-fix:

- high miss rate concentrated in one context;
- opposite-direction errors (`A→B` works while `B→A` fails);
- apparent success only when directions are incorrectly pooled;
- repeated `mixed` or `Other` responses on one axis;
- repeated respondent distinctions not represented in the rubric;
- one question producing several systematically independent subpatterns;
- one symbolic feature predicting two outcomes that empirically dissociate;
- apparently useful feature only in training but not development holdouts;
- low answerability or low classifier reliability despite high theoretical information gain;
- a question whose noise cost exceeds its discrimination benefit.

## LLM-assisted discovery layer

A separate proposal agent may inspect only **development** cases and their frozen evaluations to suggest revisions.

It may propose:

- split axis `X` into `X1` and `X2`;
- make an axis directional instead of dyadic;
- add a trajectory or context moderator;
- add an observability/constraint variable;
- retire or downweight a failed predictor family;
- add a new source-backed astrology/HD candidate feature;
- add, merge, rewrite, or retire a questionnaire prompt;
- change a follow-up applicability condition;
- propose a non-symbolic baseline interaction.

Every proposal must include:

- exact development cases/evaluation records that motivated it;
- whether it arose from hits, misses, `Other`, mixed, or context dependence;
- the proposed semantic change;
- the proposed feature/question change;
- a complexity cost;
- a falsifiable held-out prediction;
- a declaration that the motivating cases cannot count as validation of the proposal.

The proposal agent must not edit the live model directly.

## Example learning patterns from initial development

These examples motivated the current architecture and are **training history**, not validation:

- `compatibility` split into multiple axes because sex, love, intellect, emotional ease, and practical fit dissociated;
- attraction and sexual chemistry split because one actor can be highly attracted while dyadic sex is poor due to partner libido;
- libido and novelty/habituation split because a person can have high libido but lose desire for familiar partners;
- love and Eros split because deep mutual love can coexist with one-sided or absent `in love` state;
- intellectual compatibility and intellectual stimulation split because one partner may fit the actor's reasoning while another expands the actor's mind more;
- communication quality and communication abundance split because a pair can communicate well but have little common material;
- visible drama and serious conflict split because theatricality may be frequent while hostility remains rare;
- emotional ease became state-conditional because distance versus cohabitation/attachment threat can reverse the experience;
- sexual jealousy and romantic-priority jealousy split because sexual openness can coexist with strong romantic exclusivity.

Future cases should be able to produce comparable proposals automatically when genuinely new recurring distinctions appear.

## Noise-audit dependency

The active natal `SURVEY-V2-NOISE-AUDIT` is upstream of the final learning policy.

Authoritative completed checkpoints reported during development at commit `dd37aa4`:

- perfect answers: 100% top-1, 100% true-candidate survival;
- one wrong classification: 98.344% top-1, 99.595% true-candidate survival;
- 5% wrong classifications: 96.555% top-1, 99.104% true-candidate survival.

A 10% wrong-classification scenario had a preliminary earlier result around 92.24% top-1, but it was not yet authoritative at the time this document was written.

Consequences:

- preserve the existing answer-blind EIG architecture unless the completed audit overturns it;
- do not finalize relationship retry/backtracking/corroboration thresholds until all authoritative Survey-v2 scenarios are available;
- after that, run a relationship-specific noise simulation rather than assuming natal robustness transfers unchanged;
- learn per-question reliability empirically from development/test-retest data rather than treating current questionnaire reliability constants as calibrated probabilities.

## Promotion discipline

There are three distinct model states:

### `ACTIVE_FROZEN`

Used for current validation/scoring. Immutable for enrolled cases.

### `DEVELOPMENT_CANDIDATE`

Generated from development evidence. May change freely but its motivating cases are training data.

### `NEXT_FROZEN`

A selected development candidate that passed the development holdout gate and has been hashed/frozen for the next untouched cohort.

No individual participant response can directly transition `ACTIVE_FROZEN` to a modified version.

## Automatic learner outputs

A batch learning run should emit at minimum:

```text
learning_run_id
input_case_manifest_hash
active_model_hashes
axis_error_summary
question_answerability_summary
context_failure_clusters
directional_failure_clusters
other_mixed_unresolved_clusters
candidate_revision_proposals
holdout_evaluation_plan
promotion_status
```

If no stable new pattern is present, the correct result is `no_revision_recommended`.

## Participant consent

The public questionnaire should distinguish:

- consent to receive a personalized result;
- consent to retain de-identified questionnaire data for research;
- consent to use de-identified responses to improve future questionnaire/model versions;
- consent, where applicable, to use supplied birth data for Astro/HD research.

A participant may receive the result without being forced to consent to future model training if the product design permits that separation.

## Scientific objective

The learning system is not trying to maximize retrospective narrative fit.

Its target is:

> improve out-of-sample prediction/classification/discrimination on relationships or participants that were not used to invent the revision.

If training fit rises while development holdout/untouched performance does not, the revision is overfitting and must not be promoted.
