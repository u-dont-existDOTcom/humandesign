# Life Patterns — Automated Coding Execution Specification

Status: pre-execution development specification. **No coding run, human contact, validation promotion, or target-model scoring is authorized by this document.**

Date: 2026-09-04

## Purpose

Freeze the operational details of the LLM-primary development pass before any automated labels or human-calibration labels are observed.

This specification implements `LIFE_PATTERNS_LLM_PRIMARY_CODING_PROTOCOL.md` and targets the high-fidelity V2 exchange in `structured_annotation_v2.py`.

## Automated coder

Preferred development coder: **GPT-5.6 Sol in a fresh ChatGPT Pro theory-blind context**, when that exact model identity is available/displayed at execution time.

The subscription/product label `Pro` is not treated as the scientific model identity. Every pass receipt must record the actual model/product identity and version information available at execution. If the product does not expose a precise version, record the displayed identity exactly and do not invent one.

A different high-capability model may be used only under a new execution manifest. Do not switch models mid-ensemble merely because another model produces more convenient labels.

## Frozen inputs

Before the first automated label is produced, freeze/hash:

1. reconciled codebook source artifact;
2. machine-readable ontology derived from that source;
3. structured V2 coding-procedure artifact, including the non-action-value registry;
4. exact automated-coder prompt;
5. behavioral development corpus manifest;
6. exact V2 annotation task set;
7. fixed batching manifest;
8. consensus rule;
9. human-calibration selection manifest/rule;
10. raw-output normalization implementation identity.

No target-model/birth/chart information may be present in these inputs.

## Episode boundaries

For participant-reviewed Life Patterns evidence, episode boundaries are already part of the frozen behavioral source. Automated coding therefore **must not split, merge, enlarge, or rewrite episodes**.

Episode-segmentation reliability is a separate research question for raw-transcript workflows and is not silently mixed into this coding pass.

## Automated pass structure

Use at least **three complete isolated passes** for development stability assessment.

An automated pass is complete only when every frozen annotation unit has a schema-valid response or an explicitly preserved unresolved/invalid status under the frozen failure policy.

### Isolation

- A pass cannot see outputs from another pass.
- A batch cannot receive labels from prior batches as examples.
- No disagreement summary is supplied until all raw passes are frozen.
- If using interactive ChatGPT rather than a stateless API, use a fresh theory-blind chat for each batch.

### Batching

Freeze the batch partition before coding. Prefer small batches that keep the full codebook/procedure available without encouraging cross-episode pattern inference.

Operational default: **1–5 frozen episodes per batch**, depending on context size.

The same batch manifest is reused for every repeated pass. Batch boundaries cannot be adjusted after seeing difficult cases unless the run is abandoned and restarted under a new manifest.

## V2 primary coding semantics

For each assigned episode–observable unit:

- primary episode state is only `observed`, `insufficient`, or `not_applicable`;
- person-level `contradicted` and `mixed` are not encoded as primary episode states;
- multiple substantive values are represented as `single`, `ordered_sequence`, or `unordered_multiple`;
- ordered sequences must preserve reported temporal order;
- multiple values must not be used merely to hedge uncertainty;
- a value registered as non-action is valid only when awareness, opportunity, feasibility, and established non-action are all `established`;
- if a candidate non-action fails that gate, the response must be `insufficient` rather than a substantive non-action value;
- narrator-explicit influence and mere temporal precedence are separate;
- all evidence references must be source-turn IDs inside the frozen task.

## Raw-output policy

Preserve the exact raw model output bytes/hash for every attempted batch.

A deterministic parser may normalize schema-valid raw JSON objects to canonical V2 JSONL using `structured_annotation_normalization.py`. Normalization may alter whitespace/key order only through parse-and-reserialize. It may not:

- repair substantive values;
- add missing evidence;
- change state;
- infer a non-action gate;
- rewrite a sequence;
- correct an observable ID.

Schema-invalid raw output is preserved as an invalid attempt. A retry must use the same frozen inputs in a fresh isolated context and receive a new attempt identity.

## Ensemble consensus

Consensus is calculated only after every constituent pass is frozen.

Define an annotation unit as `(episode_id, observable_id)`.

For each unit compare the full substantive tuple, not merely the top-level state:

- state;
- coded values;
- value relation;
- non-action flag/gate;
- influence relation;
- source evidence;
- context/missingness fields used by the frozen consensus rule.

Classify each unit as:

- **unanimous** — all valid passes agree under the frozen equality rule;
- **majority** — a prespecified majority agrees but at least one valid pass differs;
- **unresolved** — no allowed majority, incompatible evidence, or invalid-pass condition under the frozen rule.

Do not force unresolved units into a label.

## Human calibration design

The human auditor works independently and **must not see automated labels before the first-pass audit is frozen**.

The basic calibration unit is an **episode–observable pair**, not necessarily a whole episode coded against all 22 observables.

This is intended to make a serious blind human check feasible without requiring a person to reproduce the full automated workload.

### Two calibration strata

Freeze two strata before automated labels are revealed:

#### A. Representative stratum

Select episode–observable pairs using a deterministic/random rule from the full eligible unit universe without using model outputs.

Purpose: estimate ordinary automated-human agreement without conditioning on model disagreement.

#### B. Boundary/prerequisite stratum

Separately select units using theory-neutral predeclared criteria such as:

- non-action-value eligibility;
- known codebook confusion pairs;
- multi-step episode metadata;
- explicit uncertainty/missingness;
- rare prerequisite classes;
- modality/language/context diversity.

Purpose: stress-test difficult distinctions. Results are reported separately and are not treated as natural-prevalence agreement.

Selection may not use target-model information or automated labels.

### Initial burden target

For the first development calibration, target roughly **60–100 focused episode–observable judgments total** across the two strata, not 60–100 fully coded episodes.

This is an operational burden target, not a universal psychometric threshold. Expand the calibration sample if results are unstable, sparse, or a later Route-B statistical substitution test requires more data.

## Owner sensitivity pass

The theory-exposed owner may separately code a frozen subset only after automated and blind-human first-pass outputs are independently frozen and without seeing those labels first.

Owner results are a sensitivity analysis of theory exposure and do not constitute the blind human calibration benchmark.

## Route-B statistical substitution

If the project later considers `statistically_justified_llm_substitution`, freeze before target-model scoring:

- exact eligible calibration population;
- sampling design;
- statistical test/method;
- null/alternative or acceptance framework;
- decision rule;
- handling of abstentions/unresolved units;
- multiplicity policy if testing many observables/facets;
- minimum data conditions under which no substitution claim will be made.

A passing decision must be stored in `StatisticalLLMSubstitutionReceipt`. The project must not choose or tune the test after inspecting target-model performance.

## Route-C automated instrument

If the project instead treats the pipeline as an explicit automated measurement instrument, freeze:

- exact model/prompt/ensemble definition;
- stability acceptance criteria;
- human-audit criteria;
- unresolved-unit policy;
- sensitivity analyses;
- version-drift policy;
- explicit statement that automated labels are not claimed to equal a human gold standard.

## Failure/stop conditions

Pause theory-blind development and revise under a new version if, before target-model results:

- repeated passes show systematic unresolved coding on important distinctions;
- human calibration identifies systematic codebook/model errors;
- the non-action gate is frequently violated or cannot be applied reproducibly;
- sequence information is routinely lost;
- evidence provenance is frequently invalid;
- output-format failures make the frozen execution procedure impractical.

Do not relax these rules because stricter coding reduces apparent target-model fit.
