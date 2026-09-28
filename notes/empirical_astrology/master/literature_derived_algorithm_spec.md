# Literature-Derived Algorithm Development Specification

Date: 2026-09-28

Status: development specification only; not a validated model

## 1. Decision boundary

The literature does not justify shipping a general astrology scoring model. It justifies a constrained prospective research algorithm with explicit negative controls, a very small candidate set, and a frozen evaluation protocol.

The current protocol decision is binding:

- the primary same-hospital / near-time-birth personality test remains theory-neutral;
- aspect/orb tightness and angularity are preregistered secondary moderators;
- every specific aspect-to-trait mapping is frozen before outcomes are inspected;
- held-out replication is required;
- historical literature is development evidence and cannot be counted as untouched validation.

No coefficient below is a production weight. Where the literature does not supply a replicated transportable effect, initialize the coefficient to zero and learn it only inside the development split under the stated regularization and multiplicity plan.

## 2. Reproducible astronomical layer

### 2.1 Input contract

For every participant store:

- birth timestamp as reported, source, timezone, daylight-saving interpretation and UTC conversion;
- uncertainty interval in minutes, not merely a quality letter;
- latitude/longitude and hospital/site identifier;
- calendar date and local clock time;
- source record type (civil/hospital, parental report, self-report, rectified, unknown);
- outcome collection time and whether astrology knowledge or prior readings were measured.

Records whose time uncertainty is wider than a feature's sensitivity are interval-propagated or excluded for that feature. Rectified times are never mixed with recorded times in a confirmatory analysis.

### 2.2 Calculation contract

Pin the ephemeris package, ephemeris files, Earth-orientation assumptions, zodiac frame, node definition and coordinate convention in the preregistration and output them with every feature row. Convert local timestamps to UTC before calculation. For the primary experiment compute both the raw time/hospital controls and the chart-derived secondary features; the primary endpoint must not depend on choosing an astrological house system.

For two ecliptic longitudes \(\lambda_i,\lambda_j\) in degrees define the unsigned separation:

\[
d(i,j)=\min(|\lambda_i-\lambda_j|, 360-|\lambda_i-\lambda_j|),\quad 0\le d\le180.
\]

For an exact aspect angle \(a\in\{0,60,90,120,180\}\), define distance to exactness:

\[
o(i,j,a)=|d(i,j)-a|.
\]

Do not choose an orb after seeing outcomes. A binary aspect indicator is \(I[o\le O_{ij,a}]\), where every \(O_{ij,a}\) is frozen in the feature manifest. Prefer continuous splines of \(o\) in the exploratory development model so arbitrary cutpoints can be ablated.

Applying/separating status is defined from ephemeris motion, not a text label. Evaluate the signed change in distance to exactness at the birth instant using relative longitudinal velocities (or a small preregistered forward step): applying if \(o(t+\epsilon)<o(t)\), separating if \(o(t+\epsilon)>o(t)\). Stationary/ambiguous cases are a separate category. The Tarvainen 2022 abstract motivates, but does not validate, a single interaction in which the maximum applying orb may be 1° or 2° wider than the separating orb; both values must be declared before outcomes.

For angularity, calculate the minimum angular distance from a body's ecliptic longitude to ASC, MC, DSC and IC under the pinned astronomical convention. Use a continuous preregistered distance function first. Any sector/bin version must be an ablation, and the primary analysis must not select a house system by fit.

## 3. Primary prospective experiment

### 3.1 Scientific question

Do people born at nearly the same clock time in the same hospital/site show greater measured personality similarity than locally comparable births farther apart in time?

This is theory-neutral. It does not assume signs, houses, aspects, planetary sectors or a complete astrological system.

### 3.2 Sampling

Use recorded hospital/civil times. Construct same-site birth pairs or sets within preregistered windows, for example 0–5, 5–15, 15–30, 30–60 and 60–180 minutes. Exact windows must be frozen after a feasibility-only inspection of timestamp density and before personality outcomes are opened. Keep one individual from contributing uncontrolled numbers of dependent pairs; use a graph/cluster-aware estimator or predefine one matched comparison per target.

Match or condition on hospital, date, local clock time, year/cohort, sex where justified, and relevant recruitment variables. Preserve season and secular trends. Do not shuffle birthdays globally.

### 3.3 Outcome

Use a prespecified validated personality instrument with item-level scoring rules frozen before chart features are generated. Define one primary similarity metric and direction. Candidate choices include standardized Euclidean distance or profile correlation, but only one is primary; the rest are sensitivity analyses.

Measure astrology belief, sign knowledge, prior readings and recruitment source. They are confound/heterogeneity variables, not success endpoints.

### 3.4 Primary model

The primary predictor is birth-time distance within site, represented by a prespecified continuous function or ordered windows. Estimate the association with personality distance using site/date clusters or mixed effects. Report the effect with confidence/credible interval and calibration against site-preserving permutations.

The primary test succeeds only if the held-out prospective cohort shows the preregistered direction after its declared correction. An exploratory development effect is not success.

## 4. Candidate feature modules

### 4.1 Aspect tightness and angularity moderators

**Evidence:** Startup 1984 (`SRC-11C6F771BA7D21`) is broadly null; Tarvainen 2022 (`SRC-POST-TARVAINEN2022`) is abstract-only and suggests applying/separating asymmetry rather than generic tightness.

**Feature:** for each predeclared planet pair/aspect mapping, include continuous distance-to-exactness \(o\), applying/separating category, angularity distance for both bodies, and no more than the following interactions:

- mapped aspect × distance-to-exactness;
- mapped aspect × applying status;
- mapped aspect × minimum angularity distance;
- a single three-way interaction only if separately powered and preregistered.

**Outcome domain:** the exact personality dimension named in the frozen mapping.

**Independence:** one verified Startup cohort plus an unverified recent multi-dataset abstract; not replicated.

**Weight:** must be learned with shrinkage in development data; prior mean zero. No sign/direction is imported from literature.

**Ablation:** remove the mapped aspect, then tightness, applying status and angularity one at a time; compare held-out loss, not within-sample p-value.

**Held-out test:** required in an untouched recruitment wave with the same calculation manifest.

### 4.2 Oshop–Foss AtmaKaraka–PutraKaraka kendra rule

**Evidence:** Oshop and Foss 2015 (`SRC-33C6ABEB7839AE`), one selected N=84 dataset; 60/84 versus 3025/5460 permuted, one-sided Fisher p=.00205.

**Exact calculation:** use sidereal longitudes with the Lahiri ayanāṃśa and mean lunar nodes. Rank the seven relevant classical planets by their degree within their current sign, using the paper's tie rule. AtmaKaraka is the greatest within-sign degree; PutraKaraka is the sixth-greatest. Calculate each planet's sign in D1 and its navāṃśa sign in D9 under a pinned implementation. The binary feature equals one when the two karakas are 1, 4, 7 or 10 signs apart in D1 or D9.

**Outcome domain:** public prominence/follower rank. It has no verified personality meaning.

**Independence:** one dataset; no independent replication.

**Weight:** zero in the primary personality model. In a separately justified prominence study, learn a binary coefficient only after exact reproduction of the original counts.

**Dependencies:** timed birth coverage, celebrity/public-figure ascertainment, ayanāṃśa, node and navāṃśa implementation.

**Ablations:** D1 only, D9 only, both; alternative karaka ranks only as separately corrected exploratory variants.

**Held-out test:** a preregistered population frame defined before birth-data availability is checked, with coverage weighting and a second untouched cohort.

### 4.3 Adjusted planetary-dominance biography matching

**Evidence:** Godbout–Coron 2023 (`SRC-POST-GODBOUTCORON2023`) abstract reports independent N=61, p=3.2e-05, r=.51. The full method was not available.

**Exact calculation:** not implementable from verified evidence. No placeholder or inferred definition is permitted. The full paper, scoring dictionary, biography labels, semantic model/version and match procedure must be recovered before code is written.

**Outcome domain:** chart-to-biography/profile matching only.

**Weight:** none; feature blocked by definition uncertainty.

**Required audit:** label creation blinded to charts, fixed vocabulary, no biography text leakage into chart keywords, all candidate models counted, and permutation at the complete-pipeline level.

### 4.4 Southern Hemisphere inversion

**Evidence:** Godbout–Brun 2026 (`SRC-POST-GODBOUTBRUN2026`) abstract reports N=141, but full methods/results were unavailable.

**Provisional mathematical transform:** for Southern Hemisphere births replace tropical longitude \(\lambda\) with \((\lambda+180)\bmod360\) before sign categorization; Northern Hemisphere remains unchanged. Do not apply this transform to houses or aspects unless the original method explicitly did so.

**Outcome domain:** automated public-figure trait/profile matching.

**Independence:** one claimed dataset.

**Weight:** none until the Mastro Expert/Semantic Proximity pipeline and roughly 150-trait coding scheme are reproduced.

**Ablation:** original versus inverted zodiac, hemisphere × transform interaction, latitude-matched north/south controls.

**Held-out test:** independent people and an analysis team blinded to hemisphere labels during trait coding.

### 4.5 Gauquelin key-sector module

**Evidence:** historically reported effects, failed/disputed replications, extensive reuse and the Ertel–Irving reanalysis (`SRC-POST-ERTELIRVING1997`).

**Exact calculation:** deliberately unspecified here. “Key sector” is not one stable feature across the chain. The sector geometry, planet set, civil-time correction, eminence rule and admission criteria must be selected from a named primary protocol before implementation.

**Outcome domain:** narrowly specified profession/eminence only.

**Weight:** none.

**Required design:** independent civil records, fixed profession and eminence rubric, complete inclusion log, local demographic/time controls, and one untouched country/cohort replication. Every reanalysis of the discovery cohort shares one evidence unit.

### 4.6 Excluded high-stakes candidates

Bhandary clinical judgment (`SRC-83F9732686E74F`) and the Daigno violence-aspect abstract (`SRC-POST-DAIGNO2026`) are not algorithm modules. They may be studied only as aggregate methodological claims under appropriate ethics review. They must never produce a diagnosis, violence score, mortality score, hiring decision or person-level warning.

## 5. Features that must not enter the next version

The following receive no model column, no fallback heuristic and no narrative “tie-breaker”:

- Sun-sign personality main effects;
- Sun-sign relationship compatibility;
- client preference for a reading;
- human astrologer confidence or intuition weights;
- generic hard/soft aspect weights;
- generic aspect/no-aspect personality weights;
- the 108th-harmonic personality claim;
- uncorrected high-dimensional p<.05 selections;
- broad near-time whole-chart similarity scores;
- the 21-rule/68-parameter Vedic celebrity aggregate;
- clinical, violence, mortality, fatality or hiring scores;
- synthetic/preprint demonstrations as evidence;
- any feature defined only by an abstract or review paraphrase.

## 6. Learning and validation protocol

### 6.1 Split before analysis

Partition by person, family, hospital/site and temporal block as necessary to prevent leakage. Reserve an untouched prospective replication cohort before inspecting astrology-feature associations. If a site appears in both development and replication, keep nonoverlapping future time blocks and test site drift.

### 6.2 Feature manifest

Before outcomes are opened, hash and archive:

- ephemeris and calculation versions;
- planet/body list;
- zodiac/reference frame;
- every aspect angle and orb;
- applying/separating rule;
- angularity definition;
- every aspect-to-trait mapping;
- all exclusions and birth-time thresholds;
- primary/secondary outcomes;
- interaction family;
- control generator;
- multiplicity and model-selection procedure.

### 6.3 Estimation

Use a low-capacity baseline first. Compare:

1. conventional covariates only;
2. birth-time-distance primary model;
3. primary plus frozen aspect mappings;
4. primary plus secondary tightness/angularity interactions.

Use regularization nested entirely inside development data. Standardize continuous predictors using development statistics. Never use the replication cohort for feature selection, stopping, orb choice, missing-data tuning or calibration.

### 6.4 Controls

Run complete-pipeline permutations that preserve hospital, date/cohort, local clock time, geography and birth-time quality. For astronomical-frequency tests, shuffle in a way that preserves real ephemeris/base-rate structure. Report negative controls such as maternal variables or impossible/future labels when scientifically suitable.

### 6.5 Multiplicity

Define one primary hypothesis. Secondary aspects, orbs, angularity and candidate modules form named families with Holm, FDR or a preregistered hierarchical model. Model selection is part of multiplicity: permutations must repeat the full selection process.

### 6.6 Success criteria

Success requires all of the following:

- preregistered direction and metric;
- held-out improvement over conventional controls and a site-preserving null;
- confidence/credible interval excluding the minimum effect of no practical interest in the favorable direction;
- acceptable calibration and no dependence on a single site, reader, orb or outlier subgroup;
- replication in a second untouched cohort;
- effect remains after measuring belief/prior knowledge where the outcome can be self-attributed.

Statistical significance alone is not success.

## 7. Required ablations and failure reports

For every surviving model report:

- no-astrology baseline;
- time-distance only;
- chart features without interactions;
- tightness removed;
- applying/separating removed;
- angularity removed;
- uncertain birth times removed;
- astrology-aware participants removed or stratified;
- each hospital/site left out;
- all feature selection repeated under null permutations.

Publish null and opposite results with the same prominence as positive results. If the held-out result fails, the feature returns to zero weight; it is not retuned on the replication set.

## 8. Provenance contract

Each model feature must link to a `candidate_feature_id`, exact source IDs, dataset IDs, extraction IDs, calculation code hash, preregistration hash and outcome-freeze timestamp. If a source is abstract-only or definition-uncertain, its feature is blocked in code. Dataset lineage is checked before any evidence aggregation so repeated publications cannot multiply a prior.

## 9. Next implementable version

The next version should implement only:

1. the theory-neutral same-hospital/near-time primary predictor and conventional controls;
2. a minimal, fully frozen secondary aspect-to-trait mapping supplied before outcome access;
3. continuous orb distance, applying/separating and angularity as secondary moderators;
4. complete control-generation, multiplicity, ablation and provenance machinery.

No literature-derived feature has earned a nonzero production weight. The purpose of this version is to discriminate hypotheses efficiently, not to maximize a retrospective astrology score.
