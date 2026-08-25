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

## Astro-Databank development lesson, 2026-08-25

The first nonlinear Astro-Databank development pass produced apparently strong exact-year-controlled carrier-pattern identification when missing labels were treated as unknown. A deeper audit found that:

- unordered gate/channel effects largely disappeared under exact-year controls;
- carrier-specific fast-body gate/line representations retained more development signal;
- opportunity-conditioned training removed a large annotation-selection artifact;
- the remaining signal was highly nontransportable by country: France was strong, the United States was approximately null, and Italy ran opposite;
- French results depended materially on heterogeneous archive provenance/collector structure.

This is **not validation of Human Design**. It is the reason opportunity conditioning, source-blocked training, and transport reporting are now mandatory parts of the holistic archive workflow.

## Relationship to minimization / MPOD

Only after a whole-profile model shows reproducible, transportable held-out identification should minimization ask what can be deleted:

1. full chart representation;
2. remove architecture families by cross-fitted ablation;
3. remove carrier/body families;
4. replace symbolic HD encodings with simpler raw astronomical objects;
5. retain the smallest object that preserves nearly all independently replicating information.

A compact formula selected from one archive is a DEVELOPMENT hypothesis. Its scientific weight comes from frozen external replication, not from how spectacularly it can be optimized on the discovery archive.
