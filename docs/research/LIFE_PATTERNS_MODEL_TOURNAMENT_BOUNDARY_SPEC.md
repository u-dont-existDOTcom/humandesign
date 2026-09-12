# Life Patterns Post-Freeze Model Tournament Boundary — v1

Status: development specification only. No model execution, birth-data collection, participant analysis, reveal, merge, or deployment authorization.

Independent conception snapshot: `state/LIFE-PATTERNS-MODEL-TOURNAMENT-INDEPENDENT-CONCEPTION-2026-09-03.md`.

## Existing-work scan

The next boundary substantially overlaps established methodology, so v1 composes existing work rather than inventing a new evaluation doctrine.

### Reuse / adapt

1. **Preregistration / Registered Reports** — predeclare confirmatory hypotheses, model roster, outcomes/metrics, exclusions, and analysis rules before inspecting the target result. Deviations remain visible and exploratory rather than silently replacing the plan.
   - Nosek et al. (2018), *The preregistration revolution*.
   - Chambers & Tzavella (2022), *The past, present and future of Registered Reports*.
2. **Model-selection bias / nested validation** — model selection is part of fitting. Any tuning among model variants, mappings, hyperparameters, representation choices, or scoring rules must occur inside the development loop; untouched evaluation cannot be reused to pick the winner and then reported as unbiased validation.
   - Cawley & Talbot (2010), *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*.
   - Varma & Simon (2006), *Bias in error estimation when using cross-validation for model selection*.
3. **Adaptive holdout / reusable-holdout literature** — repeated detailed feedback from an untouched validation set can itself overfit the holdout. Strong validation therefore limits adaptive inspection and preserves a genuinely untouched cohort for final claims.
   - Dwork et al. (2015), *The reusable holdout: Preserving validity in adaptive data analysis*.
4. **Proper scoring rules** — when models emit calibrated probabilities, use predeclared strictly proper scoring rules rather than a metric that rewards overconfident or strategically distorted probabilities.
   - Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*.
5. **Model Cards / versioned model documentation** — every executable model entry needs an explicit identity, intended role, implementation provenance, evaluation status, limitations, and version.
   - Mitchell et al. (2019), *Model Cards for Model Reporting*.
6. **Dynamic-consent principles** — a participant's behavioral-profile freeze is not consent for a secondary birth-model analysis. Analysis authorization is a distinct, active, scoped event.
7. **Repository-native canonical artifacts** — reuse `hdmatch.experiments.canonical` for canonical JSON, hashes, and immutable-create semantics. Reuse existing immutable Pydantic record style, candidate-universe identities, tie-aware rank metrics, confirmatory/reveal phase semantics, and model receipts where compatible.
8. **Specification-curve / multiverse analysis** — useful only as an explicitly exploratory robustness layer when many defensible specifications exist. It does not retroactively make a data-driven choice confirmatory.

## Explicit build decision

- confirmatory/exploratory semantics: **reuse/adapt preregistration and Registered Reports**
- development/validation separation: **reuse nested-validation/model-selection literature**
- untouched-cohort protection: **reuse adaptive-holdout principles**
- probabilistic evaluation: **reuse proper scoring rules**
- model documentation/versioning: **adapt Model Cards + existing repo receipts**
- rank/tie handling: **reuse `hdmatch.evaluation.metrics`**
- canonical identity/immutable artifacts: **reuse `hdmatch.experiments.canonical`**
- participant secondary-analysis permission: **adapt dynamic-consent principles**
- specification robustness: **optional exploratory experiment**
- project-specific freeze/manifest/model triple binding: **bespoke composition**

## Why the old AstroHD participant flow is not directly reused

The repository already has strong primitives in `hdmatch.participant`: immutable prediction freezes, candidate-universe hashes, confirmatory locks, ranking receipts, and reveal/post-hoc separation.

However, that older harness creates an AstroHD prediction freeze **before** participant answers because it was designed as a model-specific blind interview. The Life Patterns architecture intentionally reverses this chronology:

`theory-blind behavioral measurement -> participant-reviewed behavioral freeze -> separately authorized model analysis`

Calling the old prediction-freeze machinery during the Life Patterns interview would violate the newer scientific boundary. Its primitives may be reused only downstream, after the behavioral freeze.

## Core invariant: triple binding

Every executable model result must bind exactly:

`behavioral freeze SHA-256 + tournament manifest SHA-256 + model implementation SHA-256 -> immutable result`

No result is scientifically interpretable without all three identities.

## Separate analysis authorization

A behavioral freeze is useful independently of birth-model research. It therefore contains `model_comparison_authorized=false`.

A future analysis-authorization record must be a distinct participant action and bind at least:

- exact `session_id`;
- exact `freeze_id` and `freeze_sha256`;
- analysis purpose;
- whether exact birth data may be collected/used;
- model-family scope the participant permits;
- storage/reveal scope;
- authorization timestamp;
- authorization schema/version;
- explicit statement that declining does not alter the participant's Life Patterns profile.

Authorization is necessary but not sufficient for execution. A scientifically executable manifest is also required.

## Tournament manifest

The manifest is immutable and is frozen before the target result is inspected.

Required top-level fields:

- schema version;
- manifest ID + SHA-256;
- exact behavioral freeze hash;
- exact analysis-authorization hash;
- exact birth-input artifact hash and civil-time/location-resolution receipt, once birth intake exists;
- cohort role: `development`, `validation`, or `untouched_final_validation`;
- exact model roster;
- exact metric plan;
- exact missing/uncertain/rejected-claim policy;
- exact tie policy;
- exact exclusion policy;
- reveal policy;
- runtime/code identity;
- creation timestamp and preregistration status.

### Model entry

Every model entry must contain:

- stable `model_id`;
- human-readable label;
- family;
- scientific status: `confirmatory_predeclared`, `development_only`, or `exploratory_posthoc`;
- implementation version;
- implementation SHA-256 or exact code/artifact identity;
- adapter ID + SHA-256;
- **measurement-bridge ID + SHA-256** describing how the neutral behavioral freeze becomes that model's scoreable observables;
- prediction/scoring-contract SHA-256;
- candidate-universe identity when ranking dates/times;
- complexity/tuning metadata;
- declared output type;
- limitations.

A model cannot be marked confirmatory merely because its underlying tradition existed before the participant. The exact computational representation, behavioral bridge, and scoring rule must also be predeclared.

## The measurement bridge is a first-class scientific object

This is the largest unresolved remainder.

The Life Patterns freeze contains participant-reviewed neutral claims and their episode provenance. Existing AstroHD scoring consumes structured question/answer observables. A flexible after-the-fact LLM translation from free text into whatever each model expects would create a large researcher degree of freedom and could dominate the model comparison.

Therefore every executable model must bind an immutable **measurement bridge** that specifies, without access to the participant's birth/model output:

- which neutral frozen fields it can consume;
- deterministic or predeclared classification rules;
- treatment of participant-edited claims;
- treatment of rejected/uncertain claims;
- treatment of missing observables;
- confidence/reliability transformation, if any;
- evidence aggregation and dependency rules;
- version/hash and validation status.

A bridge may itself use an LLM only if its exact prompt/model/schema, blindness constraints, reliability evaluation, and adjudication policy are frozen before target scoring. Birth/model outputs must never enter bridge classification.

Until at least one baseline and two genuinely distinct model families have valid pinned bridges/adapters, the system must not call itself an executable model tournament.

## Baseline requirement

A tournament must include at least one meaningful non-birth baseline appropriate to the task.

Possible baselines, depending on the final task definition:

- population/prevalence prediction for each neutral observable;
- context-only/non-birth covariate model developed on training data;
- permutation/randomized birth assignment for reverse-match discrimination;
- simple complexity-matched empirical baseline.

The baseline must be predeclared and scored under the same evidence/metric contract as competing models wherever mathematically meaningful.

## Metrics

### Reverse-match / identification tasks

Reuse repository tie-aware rank semantics rather than inventing new tie handling:

- best/worst rank interval;
- fractional-credit midrank;
- top-k fractional credit;
- reciprocal rank;
- percentile;
- tie rate;
- margin where meaningful.

Candidate universe and date/state aggregation semantics must be hashed in the manifest.

### Probabilistic observable prediction

If a model emits probabilities, predeclare at least one strictly proper score such as log score or Brier score and report calibration separately where feasible.

### Coverage

Report behavioral coverage separately from accuracy: a model that makes predictions for only a small subset of meaningful frozen evidence should not be treated as equivalent to a model covering the full behavioral target.

### Complexity

Do not create an arbitrary one-number complexity penalty without empirical justification. Record model degrees of freedom/tuning/search budget and use nested/held-out evaluation to account for development flexibility. Any later information-criterion or Bayesian-complexity comparison requires a separately justified statistical model.

## Cohort and adaptation policy

### Development

Cases that influence prompt wording, ontology, bridge rules, model representation, mapping, metric choice, or bug-driven scientific decisions are development cases.

The owner's case is development/stress-test data and cannot become untouched validation merely because the final code is later frozen.

### Validation

A validation cohort can evaluate a frozen development product, but if its detailed outcomes are repeatedly inspected to alter the system it becomes development data for subsequent iterations.

### Untouched final validation

Strong claims require a cohort whose detailed model-comparison outcomes have not been used adaptively during development.

## Reveal / post-hoc boundary

Model execution and result storage precede participant-facing reveal when a blind protocol requires it.

After reveal:

- mismatch exploration is `exploratory_posthoc`;
- new behavioral episodes do not enter the old score;
- participant corrections do not rewrite the old freeze;
- model variants inspired by the mismatch are development/exploratory models until tested on new untouched data;
- the original manifest/result artifacts remain unchanged.

## Executability validator

The next code milestone should implement a pure, server-owned validator/builder for authorization and tournament manifests. It should **not execute models**.

A manifest is `execution_ready=true` only when all of these hold:

1. exact behavioral freeze identity is present;
2. separate valid analysis authorization binds the same freeze;
3. exact birth-input identity is present when any roster entry requires birth data;
4. roster includes a valid baseline;
5. roster contains the required number of genuinely distinct implemented model families for the declared comparison;
6. every executable entry has pinned implementation, adapter, measurement bridge, and scoring-contract identities;
7. confirmatory entries have no unresolved placeholder hashes or `development_only` dependencies;
8. metric/tie/missing-data/exclusion policies are explicit;
9. cohort role and reveal policy are explicit;
10. canonical manifest hash recomputes exactly;
11. no target result has already been supplied to the builder.

For the current repository state, the expected behavior is **fail closed / not execution-ready**, because the Life Patterns neutral-to-model measurement bridges and true multi-family adapter roster do not yet exist.

## Immediate implementation boundary

Implement now:

- strict immutable Pydantic models for analysis authorization, model entries, metric policy, and tournament manifest;
- canonical hashes using `hdmatch.experiments.canonical`;
- validator that explains every execution blocker;
- immutable artifact writer/reader for manifests;
- synthetic tests proving fail-closed behavior, baseline requirement, bridge requirement, status separation, exact hash identity, and immutability;
- no participant birth intake and no UI yet;
- no execution endpoint;
- no result/reveal endpoint.

## Next research work after the boundary exists

1. Design/freeze the neutral measurement ontology and bridge contract against the Life Patterns freeze.
2. Audit which existing AstroHD/HD mappings can be represented without theory leakage.
3. Implement a non-birth baseline under the identical measurement contract.
4. Define at least one genuinely distinct comparison family rather than relabeling nearby AstroHD variants.
5. Validate bridge reliability blind to birth/model information.
6. Only then add separately consented birth intake, executable manifest creation, model execution, and reveal.
