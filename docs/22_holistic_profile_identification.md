# 22 — Holistic Whole-Profile Identification and Minimization

## Phase boundary

This module supports both DEVELOPMENT and frozen VALIDATION, but the operations are not interchangeable.

### DEVELOPMENT

Development people may be used repeatedly to:
- fit whole-profile likelihoods;
- inspect failures;
- define or revise feature groups;
- search declared interactions;
- choose matching strata;
- run ablations;
- minimize chart representations;
- tune regularization, neighborhood size, and complexity.

Cross-validation or matched-decoy performance inside DEVELOPMENT is a search/model-selection instrument, not independent confirmation.

Development evaluation used for model selection should be person-level cross-fitted whenever practical: each reported person's score is produced by a model fitted without that person. Reusing the same DEVELOPMENT population across folds is allowed; it improves development hygiene but does not create an untouched validation set.

### VALIDATION

Validation people may be scored only with a previously frozen model, evidence-tokenization rule, feature schema, matching policy, decoy policy, missingness/opportunity rule, dependency ontology, and analysis. Validation outcomes must not select a new chart representation.

## Why this exists

Sparse archival datasets and rich questionnaire cases pose a different question from one-feature/one-trait correlation tests.

The holistic model asks:

> Given the behavioral/life-pattern evidence actually observed for this person, does their true chart explain that observed set better than appropriately matched alternative charts?

The primary scientific unit is the **whole person ↔ whole chart** match. Marginal feature/trait tests remain useful diagnostics, falsifications, and later mechanism/minimization tools; they are not assumed to be equivalent to the whole-profile question.

## Missing evidence is unknown

Unrecorded behavior is unknown. It is not contradiction.

Sparse archives are especially positive-unlabeled:
- a recorded label is positive evidence;
- absence of that label is not automatically a negative;
- absence of an entire ontology branch is not evidence that the construct was assessed.

This rule applies at both **evaluation and training** time.

### Observation opportunities

For each observed label, define an **observation opportunity**: the smallest unit proving that this construct/category family was actually assessed.

Examples:
- Astro-Databank `Traits : Personality`;
- `Family : Relationship`;
- the broad `Vocation` branch;
- in a systematic questionnaire, the answered `question_id` itself.

A label's background rate may be estimated only among people with that opportunity observed.

Critically, people without that opportunity must also be excluded from that label's nearest-neighbor pool. Merely fixing the denominator is insufficient: non-assessed people occupying K nearest-neighbor slots can still distort the local rate.

## Positive-evidence score

For each observed label `y`, candidate chart `c`, and its declared observation opportunity:

1. identify the relevant DEVELOPMENT people for whom that opportunity was observed;
2. find the K structurally nearest charts within the permitted training/source block;
3. estimate the smoothed local rate of `y` in those neighbors;
4. compare it with the corresponding opportunity-conditioned background rate;
5. add the reliability/dependency-weighted log enrichment.

No term is added for an unrecorded label.

This is deliberately different from a standard multi-label classifier that scores both presences and absences.

## Dependency control

Dependency control is required on **both sides** of the comparison.

### Chart-feature dependencies

Chart features are assigned to declared families/clusters or ablated as groups. Type, Authority, Profile, center states, channels, gates, and carrier placements are mechanically related and must not manufacture evidence merely by expanding one state into many flags.

Examples of chart families:
- Type / Authority / Profile core architecture;
- center states;
- channel states;
- gate states;
- planetary carrier gate/line states;
- declared interaction/substructure families;
- deterministic astronomical families such as Sun/Earth and North/South Node oppositions.

Added encodings must earn held-out information.

### Observed-behavior dependencies

Observed labels may also be correlated. Multiple labels/questions describing the same behavioral construct must not be counted as independent confirmation merely because the questionnaire or source taxonomy contains several names for related material.

`cluster_normalized_evidence_weights()` keeps the labels available for specificity while capping their combined contribution within a declared dependency cluster. Reliability may reduce a label's weight but may not turn correlated observations into multiple full evidence units.

The dependency ontology is DEVELOPMENT-tunable and must be frozen before VALIDATION.

## Nonlinear whole-chart models

An additive marginal model can miss conjunctions. The empirical track therefore permits whole-chart neighborhood models on DEVELOPMENT data.

A candidate chart may be represented by a frozen set of carrier-specific gate/line states, channels/gates, or another declared chart representation. Whole-chart similarity can detect interactions even when no single feature has a strong marginal association.

Neighbor count, representation, target scope, matching policy, and smoothing may be optimized on DEVELOPMENT data. Once carried to VALIDATION, those choices are frozen.

## Person-level cross-fitting

For DEVELOPMENT model selection:

1. assign people deterministically to folds;
2. fit only on the other folds;
3. score the held-out person's observed positives against their true chart and matched decoys;
4. aggregate true-chart percentile/rank;
5. repeat until every person is scored out of fold.

Cross-fitting reduces direct in-sample optimism. Repeatedly consulting cross-fitted results while changing the model still makes those people DEVELOPMENT.

## Person-to-chart identification

For each person:

1. keep their observed behavioral profile fixed;
2. score that profile against the person's true chart;
3. score it against matched alternative charts;
4. report the true chart percentile/rank among those candidates.

Primary group summaries include:
- mean true-chart percentile;
- median percentile;
- reciprocal rank where meaningful;
- randomization/permutation result;
- distribution by materially distinct source/site/country strata.

## Candidate controls

Decoys must be matched tightly enough that ordinary calendar/environment/source variables cannot masquerade as astronomy.

Depending on the dataset, audit:
- sex;
- exact birth year rather than only decade for long historical archives;
- country/geography;
- recruitment site;
- source/collector/biographer;
- other conventional variables materially linked to both annotation/outcome and birth-state distribution.

A result that disappears under a justified tighter control is not rescued by the looser result.

## Training-source leakage

Candidate matching alone is insufficient.

A model trained across heterogeneous source corpora can use a candidate chart's similarity to other source corpora as a proxy for provenance even when the target and all decoys share the same source label.

Therefore source/site controls must be able to block the **TRAINING neighborhood/model fit itself**, not only the candidate set.

When `collector`, `site`, or another source field is a training block:
- background opportunity rates are source-blocked;
- nearest-neighbor pools are source-blocked;
- the same field must also be a candidate-match field.

Small source strata that cannot support the frozen K are unevaluable. Do not lower K after seeing their outcomes merely to recover them.

## Randomization

The full candidate-score vector is retained for each person.

Under the chart-identity null, the designated true chart is exchangeable with another matched candidate. Randomization repeatedly designates a candidate from each frozen score vector and compares the null mean percentile with the observed true-chart mean.

When DEVELOPMENT search selects among representations, feature groups, carrier subsets, matching rules, interaction structures, K values, thresholds, or other model variants, the relevant null must account for that selection procedure. A p-value for only the final chosen object does not pay for the search that selected it.

## Transport is mandatory for generalization

A pooled archive result is not enough when source populations differ.

Always report materially large source/site/country strata separately. Before treating a holistic signal as evidence of a general human effect, require reasonably consistent direction across independent sources or carry a frozen model to a genuinely independent cohort.

Strong effect in one source + null/opposite effects elsewhere is evidence of nontransportability or source confounding until independently resolved.

## Canonical Astro-Databank development result, 2026-08-25

The Astro-Databank development path was intentionally adversarial. Early nonlinear experiments produced apparently strong carrier-pattern identification, including very large French results. Those effects did **not** survive the fully corrected missingness/opportunity and provenance controls.

The final canonical Swiss-Ephemeris run used:
- exact official C-sample bytes;
- A/AA timed public figures without alternative birth tuples;
- verified SWIEPH calculations only;
- Personality + Design Sun/Moon/Mercury/Venus/Mars gate+line carrier states;
- K=200;
- five-fold person cross-fitting;
- dependency-normalized positive labels;
- observation-opportunity conditioning during both background estimation and nearest-neighbor selection;
- decoys matched by sex + exact birth year + normalized nation.

Result:
- 3,328 evaluable people;
- mean true-chart percentile **50.794%**;
- median 50%;
- candidate-exchange `p≈0.095`.

Country transport was likewise null-like:
- France ≈49.293%;
- United States ≈50.786%;
- Italy ≈50.284%.

A stricter collector-blocked run constrained TRAINING neighborhoods and candidates by collector and produced:
- 1,655 evaluable people;
- mean true-chart percentile **49.279%**;
- `p≈0.833`.

Therefore the current Astro-Databank endpoint is **null for this archive formulation**. The earlier ~55–67% exploratory effects were artifacts exposed by the development process, not evidence to preserve by retuning.

The complete superseding interpretation is `reference/audits/astrodatabank_holistic_canonical_interpretation_2026_08_25.md`.

This null should not be generalized to rich questionnaire cases: Astro-Databank contains sparse, selectively coded biographical tags rather than a systematic behavioral instrument.

## Rich `HumanCase` questionnaire path

`src/hdmatch/human/holistic_humancase.py` converts the repository's rich DEVELOPMENT `HumanCase` records directly into the holistic representation.

For each answered item:
- the categorical observation is encoded collision-safely as `question_id + answer`;
- the observation opportunity is the `question_id` itself;
- `BehavioralResponse.cluster_id` supplies the dependency cluster;
- behavioral confidence × measurement reliability supplies the base evidence weight;
- cluster normalization prevents correlated questions from multiplying support;
- an `Other` answer remains valid evidence by default;
- unknown/context-dependent answers are omitted only when the analysis explicitly declares that exact answer unscored;
- raw free-text nuance is preserved for blind coding/provenance but is not automatically converted into a unique statistical category.

Legacy flat `HumanCase.responses` are supported: each question becomes its own dependency cluster and uses the case's reliability weight.

The adapter is DEVELOPMENT-only because `HumanCase` contains the actual chart features. Validation must use the blind candidate/answer-key boundary instead of passing true-chart-bearing development packets to the scorer.

CLI workflow:

```text
python -m hdmatch.holistic_cli convert-human-cases ...
python -m hdmatch.holistic_cli crossfit-opportunity ...
```

The conversion packet records:
- positive-evidence person records;
- true DEVELOPMENT charts;
- label observation opportunities;
- dependency clusters;
- explicitly skipped/no-scorable-evidence people;
- input hashes and a DEVELOPMENT claim boundary.

The crossfit command then runs opportunity-conditioned person-level chart identification against matched decoys.

## Minimization / MPOD

Only after a whole-profile model shows reproducible, transportable held-out identification should minimization ask what can be deleted.

Recommended progression:

```text
whole chart
→ whole-profile positive-evidence identification
→ person-level cross-fitting
→ dependency-controlled ablation / subset frontier
→ full-selection permutation null
→ compact HD representation
→ raw astronomical compression
→ frozen external validation
```

Minimization should report the full complexity/performance frontier, including:
1. indispensable core;
2. substitutable representations;
3. redundant symbolic expansion;
4. candidate raw/minimal mathematical object.

Do not use VALIDATION people to choose the minimized representation.

## Synthetic acceptance tests

The implementation must demonstrate that:
- an injected whole-profile law ranks true charts above decoys;
- unrecorded labels contribute zero evidence;
- people without a label's observation opportunity cannot enter that label's denominator or neighborhood;
- duplicate chart features in one dependency cluster cannot multiply support;
- correlated observed labels share capped dependency evidence;
- matched-decoy strata are enforced;
- training-source blocks constrain both model fitting/neighborhoods and candidate matching;
- cross-fitted development scoring does not train on the person it reports;
- cached scoring is identical to the slow reference semantics;
- rich `HumanCase` conversion preserves `Other`, confidence/reliability, and question dependency clusters;
- validation `HumanCase` records are rejected by the true-chart-bearing development adapter;
- minimization removes known noninformative groups while preserving injected signal.
