# 21 — Holistic positive-evidence chart identification

## Status

This is a DEVELOPMENT methodology. It was added after sparse archival tests showed that one-feature/one-trait correlations are a poor analogue of rich person-level case matching.

The central question is:

> Given the behavioral/life-pattern evidence actually observed for a person, does that person's complete birth-derived chart rank above appropriately matched decoy charts?

The primary unit is the **whole person ↔ whole chart** match. Marginal feature/trait tests remain useful diagnostics and later mechanism/minimization tools; they are not assumed to be the only way a real signal could appear.

## Missing evidence is unknown

Sparse archives are positive-unlabeled data.

- A recorded behavior/category is positive evidence.
- Absence of a label is not automatically a behavioral negative.
- Absence of an entire ontology branch is not evidence that the construct was assessed.

This rule applies at both evaluation and training time.

For each label, define an **observation opportunity**. Example archival opportunities include `Traits : Personality`, `Family : Relationship`, or the broad `Vocation` branch. A label's background prevalence and nearest-neighbor comparison are estimated only among people who have at least one annotation in that same opportunity branch.

People with no annotation in that branch must not enter the denominator and must not occupy that label's nearest-neighbor slots. Otherwise the model can learn who was richly annotated instead of learning the behavior itself.

## Dual dependency control

Dependency occurs on two sides.

### Behavioral evidence

Closely related recorded labels may all be retained for specificity, but their combined possible weight is capped within a dependency cluster. Ten occupational sublabels do not count as ten independent observations.

### Chart representation

Redundant representations of the same chart state must likewise be clustered or ablated. Type, centers, channels, gates, and planetary carriers are mechanically dependent. Added encodings must earn held-out information rather than multiply one state into artificial evidence.

## Nonlinear whole-chart models

An additive marginal model can miss conjunctions. The empirical track therefore permits whole-chart neighborhood models on DEVELOPMENT data.

A candidate chart may be represented by a frozen set of carrier-specific gate/line states or other declared chart features. Its score for an observed positive label compares the label's prevalence among structurally similar DEVELOPMENT charts with its prevalence among all DEVELOPMENT people who had that label's opportunity observed.

Neighbor count, feature representation, target scope, and smoothing may be optimized on DEVELOPMENT data. Once a candidate is carried to VALIDATION, those choices are frozen.

## Person-level cross-fitting

All development performance used for model selection should be person-level cross-fitted when feasible:

1. assign people deterministically to folds;
2. fit only on the other folds;
3. score the held-out person's observed positives against their true chart and matched decoys;
4. aggregate true-chart percentile/rank;
5. repeat for every fold.

Cross-fitting is a DEVELOPMENT model-selection tool, not independent confirmation.

## Candidate controls

Decoys must be matched closely enough that ordinary cohort structure cannot masquerade as astronomy. At minimum audit:

- sex where materially associated with the archive outcomes;
- exact birth year when the archive spans historical cohorts;
- country/geography where labels or source collection differ;
- source/collector/site when archive provenance differs.

A result that disappears under a justified tighter conventional control is not rescued by the looser result.

## Training-source leakage

Candidate matching alone is insufficient.

A model trained across heterogeneous archive sources can use a candidate chart's similarity to other source corpora as a proxy for source membership even when the target and every decoy share the same source label. Therefore source/site controls must be able to block the **TRAINING neighborhood/model fit itself**, not only the candidate set.

When `source_group` is a training block, all neighbors and background opportunity rates for a candidate are drawn only from that source group. Source-block fields must also be candidate-match fields so candidate scores are on the same source-specific baseline.

## Transport is mandatory for generalization

A pooled archive effect is not enough when the archive is heterogeneous.

Always report materially large source/site/country strata separately. Before treating a holistic archive signal as evidence of a general human effect, require reasonably consistent direction across independent sources or carry a frozen model to a genuinely independent cohort.

Strong effect in one collector/country + null/opposite effects elsewhere is evidence of nontransportability or source confounding until independently resolved.

## Canonical Astro-Databank lesson, 2026-08-25

The exploratory nonlinear Astro-Databank development path initially produced apparently strong carrier-pattern identification. Those positive-looking results did **not** survive the fully corrected model.

The canonical opportunity-conditioned Swiss-Ephemeris run used:

- the exact official C-sample bytes;
- A/AA timed public figures without alternative birth tuples;
- verified SWIEPH calculations only;
- fast-body Personality + Design gate/line carrier patterns;
- K=200;
- five-fold person cross-fitting;
- dependency-normalized positive labels;
- training and neighbor membership conditioned on observation opportunity;
- decoys matched by sex + exact birth year + normalized nation.

It produced a mean true-chart percentile of about **50.79%** over 3,328 evaluable people, with candidate-exchange `p≈0.095`.

Country-specific results were also null-like: France about 49.29%, the United States about 50.79%, and Italy about 50.28%.

A stricter collector-blocked run, which constrained both TRAINING neighborhoods and candidates by collector, produced about **49.28%** over 1,655 evaluable people (`p≈0.833`).

Therefore the current Astro-Databank endpoint is **null for this archive formulation**. The earlier 55–67% exploratory effects were artifacts of incomplete training-time missingness semantics, cohort/geography controls, and archive-source structure. See `reference/audits/astrodatabank_holistic_canonical_interpretation_2026_08_25.md`.

This negative result should not be generalized to the richer questionnaire phenomenon. Astro-Databank contains sparse, selectively coded biography tags rather than a systematic behavioral instrument.

## Rich `HumanCase` questionnaire path

The repository now converts rich DEVELOPMENT `HumanCase` records directly into the holistic representation through `src/hdmatch/human/holistic_humancase.py`.

For each answered questionnaire item:

- the categorical observation is encoded as `question_id → answer`;
- the **observation opportunity is the question itself** because an answer proves that item was assessed;
- `BehavioralResponse.cluster_id` supplies the dependency cluster;
- behavioral confidence × measurement reliability supplies the base weight;
- cluster normalization prevents several correlated questions from multiplying evidence;
- an `Other` answer remains valid evidence by default;
- context-dependent/unknown answers are omitted only when the analysis explicitly declares that exact answer unscored;
- raw free-text nuance is not turned into a unique statistical category. It should be coded blind to chart state into reusable constructs before empirical use.

Legacy flat `HumanCase.responses` remain supported: each question becomes its own dependency cluster and uses the case's reliability weight.

The adapter is DEVELOPMENT-only because `HumanCase` includes the person's actual chart features. Validation must use the existing blind protocol/candidate boundary rather than passing a true-chart-bearing development packet into the scorer.

CLI workflow:

```text
python -m hdmatch.holistic_cli convert-human-cases ...
python -m hdmatch.holistic_cli crossfit-opportunity ...
```

The first command creates an auditable positive-evidence packet with true development charts, observation opportunities, dependency clusters, and skipped/no-scorable-evidence IDs. The second runs person-level opportunity-conditioned cross-fitting and matched-decoy chart identification.

## Relationship to minimization / MPOD

Only after a whole-profile model shows reproducible, transportable held-out identification should minimization ask what can be deleted:

1. full chart representation;
2. remove architecture families by cross-fitted ablation;
3. remove carrier/body families;
4. replace symbolic HD encodings with simpler raw astronomical objects;
5. retain the smallest object that preserves nearly all independently replicating information.

A compact formula selected from one archive or one DEVELOPMENT cohort is a hypothesis. Its scientific weight comes from frozen external replication, not from how spectacularly it can be optimized on the discovery data.
