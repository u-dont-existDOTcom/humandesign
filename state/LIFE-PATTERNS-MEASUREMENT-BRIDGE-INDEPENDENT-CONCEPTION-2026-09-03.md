# Life Patterns Neutral Measurement Bridge — Independent Conception Snapshot

Status: pre-existing-work-scan conception snapshot. This records the independent design before consulting external literature/standards for the next scientific milestone.

Date: 2026-09-03
Parent branch state before this snapshot: `cded29982f482f0bf1fde6370df9070226167669` on `codex/discover-life-patterns-mvp` / PR #24.

## Problem

The Life Patterns research path now has a theory-blind interview, participant-approved episodes, participant-reviewed neutral pattern claims, and immutable behavioral freezes. The post-freeze tournament manifest correctly requires a pinned measurement bridge for every executable model.

The unresolved scientific problem is how to convert rich, contextual, participant-authored evidence into structured observables that models can score without letting the model being tested determine how the evidence is interpreted.

A model-specific free-form LLM reading of each participant's narrative after birth/chart predictions exist would create severe researcher/model degrees of freedom. The bridge must therefore be frozen, theory-blind, auditable, and shared wherever possible across competing model families.

## Candidate architecture

Use a two-stage measurement layer rather than one flexible bridge per model.

### Stage A — shared neutral evidence coding

`immutable behavioral freeze -> versioned neutral ontology -> coded observable evidence`

The shared coder receives only:

- the immutable behavioral freeze;
- a frozen neutral ontology/codebook;
- a frozen coding procedure;
- no birth data, chart, candidate state, model prediction, rank, or model fit.

It emits structured neutral observables with provenance to exact frozen source material.

Candidate observable record:

- stable neutral `observable_id`;
- coded value or distribution over allowed values;
- explicit `observed | absent | contradictory | insufficient | not_applicable` state;
- confidence/uncertainty that reflects coding evidence, not model confidence;
- supporting episode IDs and source-turn IDs;
- counterexample episode IDs;
- context/domain qualifiers;
- time/life-phase qualifiers;
- participant-edited-vs-original-synthesis provenance;
- theory-language/exposure warning where source wording may have been influenced by known frameworks;
- coder/procedure/version/hash receipt;
- no model-family label in the coding decision.

### Stage B — declarative model mapping

`neutral observables -> model-specific score inputs`

Each model family gets a small, pinned declarative adapter that says which neutral observables it consumes and how their states map into that model's predeclared scoring contract.

The adapter may not reread raw participant narrative or ask an LLM to reinterpret evidence in light of the model. If a model needs a construct not represented in the neutral ontology, the ontology must be expanded prospectively and validated before that model can use it confirmatorily.

This makes the shared ontology/coder the main measurement instrument and model adapters comparatively thin.

## Neutral ontology design principles

The ontology should represent participant-observable phenomena rather than Human Design, astrology, or other theory labels.

Examples of neutral construct families may include:

- initiation vs response to external opportunity/request;
- decision latency and reversibility;
- explicit reasoning/information gathering;
- bodily sensations and salience;
- emotional trajectory before commitment;
- speaking/listening/advice effects;
- permission/coordination/social-role constraints;
- persistence/will/effort expenditure;
- environmental/context effects;
- stress/conflict response;
- learning/adaptation style;
- developmental change;
- context dependence and counterexamples.

These are candidate domains, not a frozen ontology. Existing-work review should determine whether established behavioral-science ontologies or coding frameworks can be reused.

## Preserve episode-level evidence

Do not code only the synthesized Life Patterns Map. The map is useful participant-facing synthesis but can collapse variation.

The bridge should retain episode-level coding and then derive any person-level summary according to a frozen aggregation rule. This permits:

- context-specific effects;
- counterexamples;
- within-person variability;
- life-phase change;
- uncertainty/missingness;
- future multilevel analysis.

## Missingness is data, not a negative answer

Never convert absence of evidence into evidence of absence.

At minimum distinguish:

- construct observed positively;
- construct observed negatively/contradicted;
- mixed/heterogeneous evidence;
- not elicited / insufficient evidence;
- not applicable to the episode/context.

A model cannot receive credit because the interview simply failed to elicit a construct.

## Candidate coding procedure

Prefer the least flexible procedure that preserves validity.

Possible hierarchy:

1. deterministic extraction where source structure permits it;
2. rule/codebook classification;
3. blinded human annotation for difficult constructs;
4. frozen LLM annotation only where it demonstrably matches reliable human coding and improves scalability.

If an LLM is used:

- exact model, prompt, schema, temperature/determinism settings, examples, and allowed outputs are frozen;
- no birth/model data enter the request;
- no adaptive prompting for one participant;
- output must cite source evidence IDs;
- unsupported inference must map to insufficient/missing;
- reliability is measured against a human-coded reference set that is separate from final validation participants;
- disagreements/low-confidence cases follow a frozen adjudication rule;
- the LLM's natural-language rationale is not itself research evidence.

## Reliability and validity

The bridge is a measurement instrument, not merely data plumbing. It needs its own validation independent of model success.

Candidate validation layers:

- codebook content/construct validity;
- blinded human inter-rater agreement on a development corpus;
- test-retest/recoding stability where appropriate;
- human-vs-automated coder agreement;
- prevalence and missingness diagnostics;
- modality/language/context sensitivity;
- explicit error analysis rather than one aggregate agreement score;
- discriminant validity between neighboring constructs;
- convergence with direct participant review where a construct can be expressed intelligibly;
- no tuning based on whether Human Design/astrology prediction accuracy improves.

## Theory contamination boundary

A participant may spontaneously use theory language or may have prior exposure. The bridge should not silently treat theory labels as ground-truth behavioral evidence.

Candidate policy:

- code the underlying described episode/behavior when present;
- tag theory-language exposure separately;
- a bare label such as "I am a Projector" or "I have emotional authority" without behavioral evidence does not directly instantiate the neutral observable;
- interviewer-introduced framework language remains excluded before freeze under the existing interview boundary;
- any contamination/exposure sensitivity analysis stays separate from primary behavioral coding.

## Shared ontology vs model-specific requirements

Model families may declare neutral observable requirements prospectively, but they do not control participant-specific coding.

Flow:

`model-family requirements -> union neutral ontology/codebook -> theory-blind shared coding -> immutable coded evidence -> model-specific declarative adapters -> scoring`

Maintain an open residual category for important recurring participant patterns not anticipated by candidate models. This protects the behavioral product/research record from becoming merely a disguised questionnaire for current models.

## Content identity

Every coding run should bind:

- behavioral `freeze_sha256`;
- ontology/codebook SHA-256;
- coding-procedure SHA-256;
- coder implementation/model SHA-256;
- adjudication-policy SHA-256;
- output artifact SHA-256.

Every model adapter then binds:

- coded-evidence SHA-256;
- model-adapter SHA-256;
- scoring-contract SHA-256.

## Constraints

- no birth/chart/model information in Stage A;
- no model-specific rereading of raw participant narrative in Stage B;
- no per-participant tuning;
- no success-driven recoding after seeing model results;
- participant-edited review data remain explicitly distinguished from pre-review synthesis;
- rejected/uncertain behavioral claims remain non-admissible unless the coding protocol explicitly uses episode-level source evidence independently of the rejected synthesis;
- source provenance remains exact;
- missingness never becomes an implicit zero/negative;
- ontology/codebook revisions create new versions rather than silently changing old coded artifacts;
- owner and bridge-development cases remain development data;
- no merge/deployment/model execution authorized by this snapshot.

## Candidate insight

The most important anti-leakage design is **one shared theory-blind measurement layer, then thin declarative model adapters**.

If every model gets its own flexible natural-language bridge, model comparison can become comparison of post-hoc interpretation strategies rather than comparison of models. The common measurement layer makes competing models answer against the same observed behavioral substrate.

## Existing-work questions to scan

Search the underlying measurement problem rather than project terminology:

- construct validity and measurement-model design;
- qualitative content analysis/codebook development;
- behavioral/event coding systems and ontology design;
- inter-rater reliability/agreement statistics and their limitations;
- missing-data semantics and partial observability;
- multilevel/within-person behavioral measurement;
- measurement invariance across modality, language, culture, or context;
- human vs LLM annotation reliability and bias;
- uncertainty-aware classification/selective prediction/abstention;
- provenance standards for coded/derived research data;
- existing psychology/behavior ontologies that may supply reusable neutral constructs.

After the scan, choose reuse, adaptation, composition, invention, or experiment explicitly for each component and benchmark any bespoke bridge against the strongest established coding baseline.