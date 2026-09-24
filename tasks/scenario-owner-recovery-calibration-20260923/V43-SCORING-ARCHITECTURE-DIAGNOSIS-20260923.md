# V4.3 scoring architecture diagnosis and vNext decision — 2026-09-23

Status: **DECISION-SUFFICIENT DEVELOPMENT DIAGNOSIS**.

This analysis is post-result development work. It does not alter the frozen GPT-v1 or Opus-v2 calibration receipts and may not be described as independent validation.

## Direct finding

Under the frozen Opus-v2 translation, the 2013 rank-1 interval and the best interval intersecting the recorded 1985 local birth date have the **same 14 supported participant-observable values**.

The verified structural century cache shows the same observable fingerprint for both candidates. The fingerprint is shared by **46 exact structural intervals**.

Therefore any scorer whose input is only the participant-observable evidence actually established by this survey must treat these two candidate neighborhoods as observationally equivalent. A preference between them requires information outside the established observable vector.

## Where V4.3 gets the 2013 advantage

V4.3 does not stop at the participant observable. It scores the strongest matched structural pathway inside each dependency cluster using:

`behavioral confidence × structural salience × mapping directness × flexibility × -log2(structural prevalence)`.

For three observables, 2013 matches the full-Channel pathway while 1985 matches a hanging-Gate alternative for the **same reported behavior**.
The exact score decomposition is:

| Observable | 2013 pathway | 1985 pathway | 2013 hidden-pathway bonus |
| --- | --- | --- | ---: |
| CONSEQUENTIAL_CORRECTION | Channel 18-58 | Gate 58 alternative | 0.559619 |
| PURPOSE_STRUGGLE | Channel 28-38 | Gate 28 alternative | 0.777665 |
| RETREAT_PRIVACY | Channel 13-33 | Gate 33 alternative | 0.327353 |
| **Total** | | | **1.6646366** |

That total is the entire Opus-v2 NetInformation gap between the 2013 winner and the best 1985-date interval.

The survey did not measure whether the participant's correction, purpose, or retreat behavior came from a Channel rather than its Gate alternative. Those mechanism identities are latent theory-side explanations, not participant evidence.

**Primary diagnosis:** V4.3 is rewarding hidden pathway rarity/strength that the measurement never observed.

This is not merely a bad weight choice. Setting different channel/gate weights would still use unmeasured mechanism identity. The correct fix is an architecture boundary: collapse alternative structural mechanisms to the participant observable **before** behavioral scoring unless the mechanisms make separately measured behavioral predictions.

## Observable-only baseline result

Using Opus-supported observables only:

- 2013 and best-1985 have identical 14-observable vectors;
- both match 9 of 14 supported positive observables;
- both have confidence-weighted positive-match score 3.5;
- the exact recorded 1985 moment also has positive-match score 3.5, although it trades `PROFILE_24` for `PROFILE_LINE5_PROJECTION`.
This simple baseline does **not** recover the date. It exposes the correct information state: the present measurement is insufficient to distinguish these candidate neighborhoods without using hidden mechanism information.

Across all 19 clean historical observables, 2013 and best-1985 differ only on:

- `ORGANIZED_DETAIL`: 2013=1, 1985=0;
- `RHYTHM_ROUTINE`: 2013=0, 1985=1.

Both were left unestablished by the frozen scenario measurement.

Within the 46-state tie group:

- ORGANIZED_DETAIL alone provides 0.9877 bits of partition entropy;
- RHYTHM_ROUTINE provides 0.9321 bits;
- the pair provides 1.7544 bits and creates four cells;
- the five currently unestablished observables together create 12 cells, 3.4248 bits, largest cell 7;
- the MASTERY_REPETITION contradiction adds zero information inside this tie group.

These are useful **post-result design diagnostics only**. Asking the owner those items now to rescue the current calibration would be candidate-exposed/post-selection development evidence.

## Secondary V4.3 architecture problems

### 1. Marginal structural rarity is not behavioral evidence likelihood

V4.3 rewards `-log2(P(structural anchor))`. A rare chart structure is not, by itself, stronger evidence that the reported behavior came from that structure. For candidate discrimination the relevant empirical quantity would be a response likelihood or likelihood ratio such as `P(answer | candidate prediction)`, with alternatives compared under the same observation model.
### 2. Positive-support asymmetry

Missing support is neutral unless a bespoke contradiction was predeclared. This loses ordinary negative/counterevidence.

Example: the frozen neutral profile describes free-day timing as flexible and state/need-dependent. That does not positively establish `RHYTHM_ROUTINE`, but V4.3 also does not encode it as evidence against a stable-routine prediction. A coherent measurement model needs positive / negative / mixed / unknown-abstain states rather than only “positive support or nothing.”

### 3. Conditional-prevalence parent leakage

`duration_prevalence()` computes mapping rarity inside frozen parent conditions such as Projector + Splenic, but `score_one()` checks the mapping predicate without requiring the scored candidate to satisfy those parents.

In the Opus-v2 top 20, **6 intervals are not Projector/Splenic**, yet they can receive gate/channel evidence whose rarity was estimated inside the Projector/Splenic stratum. This does not explain the specific 2013-vs-1985 gap because both are Projector/Splenic, but it makes the broader century ordering internally inconsistent as a conditional evidence calculation.

### 4. Cross-observable dependence remains heuristic

Dependency control prevents Channel+Gate alternatives inside a named cluster from being summed, but the total still adds many behavior clusters as rubric bits. Correlated behaviors and correlated chart structures are not modeled jointly. The score is therefore not a posterior or calibrated likelihood.

### 5. Profile observable/cluster mismatch

The holistic information audit treats `PROFILE_24`, `PROFILE_LINE5_PROJECTION`, and `PROFILE_LINE6_PHASES` as different participant observables. V4.3 scoring puts all three in one `PROFILE_STRUCTURE` cluster and retains only one winning pathway. The measurement model and scoring model therefore disagree about the unit of evidence.
## Strongest replacement baseline already in the repository

Survey-v2 already implements the more appropriate boundary:

1. **Candidate normalization at the observable level.** Any frozen structural predicate intended as an alternative explanation for one observable produces the same candidate observable value.
2. **Symmetric measurement states.** Classified positive/negative, mixed, insufficient, other and unclassifiable outcomes are explicit; abstention does not become absence.
3. **Dependency-cluster weighting.** Each eligible dependency cluster contributes at most one denominator unit, with macro-averaging inside a cluster.
4. **Adaptive follow-up.** Candidate-blind entropy selection asks the remaining observable that best splits the current tie.
5. **Noise testing.** Full-century synthetic audits measure how wrong/ambiguous/uncertain answers affect rank.

The Survey-v2 synthetic results prove mechanical recoverability of that architecture under its own generated/noisy answer model; they do **not** establish that Human Design predicts real human behavior.

## Recommended vNext architecture

Do **not** modify V4.3 in place. Preserve it as the historical descriptive scorer.

Create a separately versioned **observable-evidence scorer** for scenario-v7:

### Layer A — measurement

For each observable retain:
- evidence state: positive / negative / mixed / unknown-abstain / not-measured;
- behavioral confidence;
- measurement reliability;
- conditions and source evidence IDs.

A positive historical claim that is merely “not established” is not automatically negative. Negative evidence must be explicitly supported by the participant record.
### Layer B — candidate prediction

For each candidate and observable:
- predict the participant-observable value by collapsing all frozen structural alternatives intended to express that observable;
- Channel vs component Gate may explain *why* the chart predicts the observable but cannot add evidence weight unless separate observable predictions were measured;
- fail closed on missing candidate values.

### Layer C — development baseline score

Before empirical response likelihoods exist:
- use Survey-v2-style exact/mixed observable matching;
- macro-average within declared dependency clusters;
- apply participant confidence/reliability to measured evidence;
- omit abstentions from the denominator;
- include explicit negative evidence symmetrically;
- do not use structural rarity as evidence strength.

This simple score should be treated as a development classifier, not a probability.

### Layer D — adaptive measurement

When candidate ties remain, select the next **unmeasured observable** by candidate-blind expected information gain among the tied/high-posterior candidate set.

For the current owner case, the post-result diagnostic says ORGANIZED_DETAIL and RHYTHM_ROUTINE are highly informative, but that fact must be used only to improve a future survey version and then tested on fresh participants—not to repair this already-exposed owner calibration.

### Layer E — empirical likelihood upgrade

After enough independent blinded participant cases exist, replace heuristic match weights with learned response likelihoods:
- estimate `P(response category | candidate-predicted observable)`;
- regularize heavily and cross-validate;
- model correlated observables with an explicit dependency model (e.g. hierarchical logistic / Bayesian network / TAN-like structure) rather than assuming independent additive evidence;
- compare log loss, calibration and top-k recovery against the simple observable baseline.
## Decision

**Retire V4.3 pathway-rarity scoring as the primary scorer for scenario-v7 behavior-only recovery.**

Keep:
- frozen chart predicates;
- observable grouping;
- exact interval engine;
- verified century cache;
- candidate-blind chronology and privacy rules;
- dependency metadata where semantically justified.

Replace:
- pathway-level rarity bonuses;
- positive-support-only semantics;
- unvalidated additive rubric-bit interpretation;
- conditional-prevalence use that is not enforced on scored candidates.

Adopt:
- Survey-v2 observable normalization and abstention/negative semantics as the immediate baseline;
- dependency-family normalization;
- adaptive information-gain follow-up;
- empirical response likelihoods later, only from independent data.

## Owner-case interpretation

The scoring-architecture correction does **not** make 1985 win. It removes an unjustified 2013 preference and reveals that the current established observable evidence cannot distinguish 2013 from the best 1985-date neighborhood.

That is a more useful failure mode: it says the next bottleneck is **measurement of genuinely discriminating observables and empirical response modeling**, not further tuning of structural rarity weights.
