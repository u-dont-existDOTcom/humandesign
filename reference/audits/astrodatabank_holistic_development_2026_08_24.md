# Astro-Databank holistic whole-profile DEVELOPMENT audit

**PHASE: DEVELOPMENT**

Date: 2026-08-24

## Purpose

This audit tests whether the apparent specificity seen in rich individual Human Design case analyses is better represented by whole-person / whole-chart matching than by isolated one-feature / one-trait correlations.

The Astro-Databank (ADB) C-sample used here is explicitly DEVELOPMENT data. Every model representation, dependency rule, matching stratum, ablation, and carrier subset inspected below may influence later hypotheses, but no result in this audit is independent confirmation.

## Epistemic checksum

1. May ADB data influence the hypothesis/model? **YES.**
2. May these same ADB results establish that the selected model generalizes? **NO.**

Cross-fitting below is therefore a model-selection/stability tool, not validation.

## Source and eligibility

Input was the user-supplied Astro-Databank `c_sample.zip`, containing `c_sample.xml`, export timestamp 2026-07-28.

The conservative analysis filter retained:

- Rodden rating `A` or `AA`;
- data type `Public Figure`;
- usable `jd_ut` timed birth;
- no alternative birth datum requiring favorable selection;
- non-deleted records.

This yielded **4,750** timed records.

## Positive-unlabeled outcome model

The ADB taxonomy is sparse and non-exhaustive. In the earlier pilot, only 166 of 4,975 less-conservatively filtered A/AA timed records had any `Traits : Personality` annotation, and 118 of those had only one personality tag. Therefore absence of an ADB category cannot generally be interpreted as evidence that the person lacks the behavior.

The holistic model treats:

- recorded category = positive evidence;
- unrecorded category = unknown;
- explicit contradiction only when the source actually supplies a negative observation.

For the broader whole-profile pass, positive labels were drawn from these top-level taxonomy branches:

- `Vocation`;
- `Lifestyle`;
- `Family`;
- `Traits`;
- `Notable`.

The development ontology excluded body/appearance-only material and other categories not suitable as behavioral/profile evidence, including `Traits : Body`, `Notable : Book Collection`, and the explicit `Same sex` category.

Only labels with at least 30 positives were retained in the development vocabulary. This yielded **123 labels**; **4,354 / 4,750** people carried at least one retained observed label.

### Outcome dependency control

Closely related taxonomy labels are not independent observations. Each label was assigned to a dependency cluster using its first two taxonomy levels. If a person had multiple observed labels in the same cluster, those labels shared one total evidence unit rather than each contributing a full unit.

This prevents, for example, multiple closely related entertainment-vocation tags from overwhelming unrelated parts of the person's profile.

## Person-level cross-fitting

All development performance used deterministic person-level 5-fold cross-fitting for the refined analyses:

1. fit the positive-evidence chart enrichment model on four folds;
2. score only people in the held-out fifth fold;
3. repeat until every reported person was scored by a model that did not train on that person.

The same ADB DEVELOPMENT people may appear in other folds' training sets. This controls in-sample memorization during model selection but does not make ADB an independent validation cohort.

## Candidate-chart ranking

For each held-out person:

1. keep their observed positive profile fixed;
2. score that profile against their true chart;
3. score it against matched alternative charts;
4. report the true chart percentile among those candidates.

A mean true-chart percentile of 50% is the exchangeability/null reference point.

Matched-decoy sensitivity analyses held increasingly strict conventional variables fixed, including sex, birth era/year, season/month, and pooled country.

## Astronomy and engineering scope

This DEVELOPMENT computation used the existing Moshier parity path because the local analysis environment did not contain the repository's verified Swiss `.se1` files. The calculation was mechanically checked against the repository's verified 1985 reference case and reproduced Projector, Splenic Authority, profile 2/5, and the verified four channels.

No result here is canonical V4.3. Any frozen external validation must be recomputed using the repository's verified Swiss Ephemeris path and provenance checks.

## Representation 1: structural whole chart

The first refined whole-chart representation used:

- Type;
- Authority;
- Profile;
- Definition;
- 9 Center states;
- 36 Channel states;
- 64 active-Gate states.

With positive-only outcome scoring, outcome dependency normalization, chart-feature dependency clustering, 5-fold person-level cross-fitting, and sex + birth-decade + birth-month matched decoys, the result was approximately:

- evaluable people: **3,845**;
- mean true-chart percentile: **50.34%**.

Fold means were approximately 52.61%, 48.88%, 51.73%, 48.85%, and 49.55%.

**Conclusion:** the structural whole chart alone was essentially chance under this formulation. The earlier ~51.8% one-off pilot did not survive the stricter cross-fitted/dependency-controlled version.

## Representation 2: detailed planetary carriers

The next development representation added the actual gate/line carried by each Personality and Design celestial-body activation, rather than collapsing all activations to a set of anonymous active Gates.

The standard carrier families were:

- Sun;
- Earth;
- Moon;
- North Node;
- South Node;
- Mercury;
- Venus;
- Mars;
- Jupiter;
- Saturn;
- Uranus;
- Neptune;
- Pluto;

on both Personality and Design sides.

### Carrier dependency granularity

Several dependency encodings were inspected on DEVELOPMENT data.

Approximate mean true-chart percentile on the same broad matched set:

| representation | mean percentile |
|---|---:|
| structural chart only | 50.34% |
| carriers collapsed into one dependency cluster | 50.29% |
| carriers separated only by Personality vs Design | 50.79% |
| carriers grouped by celestial body | 52.02% |
| each carrier treated separately | 51.99% |
| carrier-only, grouped by body | 52.11% |

The result therefore depended on retaining **which celestial body carries which gate/line**. Merely knowing the set of active Gates was insufficient.

### Deterministic redundancy correction

Earth is mechanically opposite the Sun and South Node is mechanically opposite North Node. They are therefore not independent carrier families.

The refined carrier representation used 11 dependency axes:

- `solar_axis` = Sun + Earth;
- `node_axis` = North Node + South Node;
- Moon;
- Mercury;
- Venus;
- Mars;
- Jupiter;
- Saturn;
- Uranus;
- Neptune;
- Pluto.

On the broad sex + decade + month matched development set, this corrected carrier-axis representation reached approximately **52.60%** mean true-chart percentile. This increase was observed after inspecting alternative dependency encodings and is therefore development evidence only.

## Conventional matching sensitivity

The carrier-axis representation was tested with increasingly strict matching. Approximate results were:

| matched variables | N | mean true-chart percentile |
|---|---:|---:|
| sex + decade + month | 4,000 | 51.71% |
| sex + 5-year bin + month | 3,602 | 51.97% |
| sex + exact year + quarter | 3,065 | 52.34% |
| sex + exact year + half-year | 3,754 | 52.30% |
| sex + exact year | 3,884 | 52.01% |
| sex + exact year + pooled country | 2,576 | 51.47% |
| sex + exact year + half-year + pooled country | 2,346 | 51.46% |
| sex + decade + month + pooled country | 2,344 | 51.78% |

Adding geography/source-composition control weakened the apparent signal. This is evidence that at least part of the unconstrained improvement may be associated with geography, source composition, or variables correlated with them.

## Fixed full-carrier full-pipeline null

For the strict development comparison using sex + exact birth year + half-year + pooled-country strata:

- evaluable people: **2,346**;
- observed full 11-axis carrier mean percentile: **51.461%**.

The complete fitting/ranking procedure was then rerun after permuting chart assignments **within the same strict matching strata**.

Among 24 full-pipeline permutations, one null run exceeded the observed full-carrier result. Using `(ge + 1)/(N + 1)` gives a conservative development empirical rate of approximately:

`(1 + 1) / (24 + 1) = 0.08`.

This is a small development hint, not strong evidence of an anomaly.

## Marginal carrier behavior

Under the strict country/year/season matching, no single carrier axis was strong. Approximate single-axis mean percentiles were:

- Neptune: 50.73%;
- Moon: 50.38%;
- Mercury: 50.26%;
- Saturn: 50.25%;
- Pluto: 50.15%;
- Jupiter: 50.11%;
- Venus: 50.03%;
- Node axis: 49.74%;
- Uranus: 49.19%;
- Mars: 49.13%;
- Solar axis: 48.80%.

Despite weak marginal results, removing some weak individual axes from the combined representation harmed joint performance. This is consistent with complementary/contextual information, but complementarity by itself does not establish a real signal because the same pattern can arise during high-dimensional search.

## Exhaustive carrier-axis minimization

Because the 11 carrier-axis contributions are additive after fitting, every nonempty carrier-axis subset could be evaluated exactly:

- total subsets: **2,047**.

The best observed DEVELOPMENT subset contained 9 axes: all nonredundant carrier axes except the Solar axis and Uranus.

Observed best mean percentile:

**52.0296%**.

The complexity frontier was:

| axes retained | best mean percentile |
|---:|---:|
| 1 | 50.729% |
| 2 | 50.739% |
| 3 | 51.022% |
| 4 | 51.609% |
| 5 | 51.743% |
| 6 | 51.663% |
| 7 | 52.001% |
| 8 | 51.995% |
| 9 | **52.030%** |
| 10 | 51.819% |
| 11 | 51.461% |

A four-axis subset (`node_axis + Moon + Venus + Saturn`) reached about 51.61%; a seven-axis subset was already almost tied with the nine-axis development winner.

This is a useful compression frontier, but choosing the best subset is itself a large model-selection operation.

## Full 2,047-subset selection null

The decisive development falsification reran the **entire 2,047-subset search** after permuting charts within the same strict conventional strata.

The first 12 complete null searches had best-of-2,047 mean percentiles approximately:

1. 52.445%;
2. 50.338%;
3. 50.554%;
4. 52.368%;
5. 50.962%;
6. 51.996%;
7. 51.332%;
8. 52.675%;
9. 50.719%;
10. 51.546%;
11. 51.016%;
12. 51.367%.

Three of the 12 null searches exceeded the observed optimized result of 52.030%.

Conservative selection-aware empirical rate:

`(3 + 1) / (12 + 1) = 0.3077`.

**Therefore the optimized carrier subset is null-like once the 2,047-subset search is counted.** It must not be promoted as evidence merely because its raw development percentile is above 52%.

## Interpretation

This development exercise answers the user's holistic-analysis question more precisely:

1. **Missing-as-unknown matters.** Sparse biographical archives are badly represented by models that treat every unrecorded behavior as false.
2. **Anonymous structural chart features were insufficient.** Type/Authority/Profile/Centers/Channels/active-Gates produced essentially chance whole-person identification after cross-fitting and dependency control.
3. **Detailed planetary carrier assignments contained a small development hint.** Which body carries which gate/line mattered more than anonymous active Gates.
4. **Conventional matching, especially geography, weakened the hint.** Some apparent information is plausibly source/geography composition.
5. **No individual carrier explained the pattern.** The joint result was genuinely multivariate in the additive model.
6. **But optimizing the carrier subset did not survive the full selection null.** Random chart assignments can produce equal or better optimized carrier subsets often enough that the observed 52.03% winner is not unusual.

Thus the correct current conclusion is **not** that holistic analysis validates HD, and not that holistic interactions are ruled out. It is that the first rigorous positive-unlabeled holistic implementation finds where a weak signal-like pattern appears, but the pattern is not statistically unusual after the actual development search process is reproduced under the null.

## What this dataset cannot test well

ADB is still a poor analogue of the rich individual case profiles that motivated the question:

- taxonomy annotation is sparse and non-exhaustive;
- annotations are heterogeneous in depth;
- many labels describe vocation or public biography rather than stable behavioral phenomenology;
- contextual conditions and developmental trajectories are mostly absent;
- negative/counterexample behavior is rarely encoded;
- biography/source practices can correlate with geography, era, profession, and fame.

A strong test of the original phenomenon requires richer people-level profiles with explicit stable patterns, contexts, counterexamples, and developmental changes.

## Next development hypothesis

The current holistic enrichment model is still additive across declared chart-feature dependency clusters. It cannot learn interactions such as:

`carrier A matters only when carrier B or center state C is present`.

A legitimate next DEVELOPMENT model is therefore an interaction-capable positive-unlabeled density-ratio teacher trained with person-level cross-fitting. It should:

- predict observed positive behavior labels from complete chart representations without treating background people as proven behavioral negatives;
- use shallow/regularized interaction models;
- retain conventional controls and matched-decoy chart identification;
- rerun the **entire interaction-model selection pipeline** under chart permutations;
- distill any surviving teacher into a compact student/minimal object before external validation.

Any resulting object remains a DEVELOPMENT hypothesis until frozen and tested on an independent cohort.
