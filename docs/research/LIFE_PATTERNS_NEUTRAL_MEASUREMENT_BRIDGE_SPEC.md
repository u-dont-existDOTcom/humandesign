# Life Patterns Neutral Measurement Bridge — Design Specification

Status: **content-neutral framework implemented and CI-gated; substantive ontology content, human reliability evidence, and confirmatory execution remain blocked**. This document defines the neutral observational layer required before any birth-derived model can be scored against the Life Patterns behavioral freeze. It does not define substantive construct content and does not authorize model execution.

Date: 2026-09-03

## Purpose

The behavioral freeze preserves what the participant reported and approved. A later model tournament needs a shared target representation that does not silently encode Human Design, AstroHD, astrology, or another candidate model. This bridge converts frozen participant evidence into explicit, versioned observational codes while preserving source provenance, missingness, context, counterevidence, participant revisions, and coder identity.

The bridge is not a personality diagnosis and is not a participant-facing interpretation layer. It exists so different model families can be evaluated against the same behavioral evidence rather than each receiving its own bespoke target representation.

## Independent conception preserved before existing-work scan

The independent conception is recorded in:

- `state/LIFE-PATTERNS-MEASUREMENT-BRIDGE-INDEPENDENT-CONCEPTION-2026-09-03.md`

The initial mechanism was:

1. freeze participant-reviewed episodes and exact source evidence;
2. define a theory-blind observable vocabulary with explicit code states;
3. code episodes before model outputs are available to the coder;
4. preserve contradictory/context-specific evidence instead of collapsing it into a single personality label;
5. aggregate descriptively and deterministically;
6. require reliability evidence before automation or confirmatory scoring;
7. keep later model adapters thin and declarative.

The subsequent scan changed implementation details but not that core chronology.

## Existing-work scan and reuse decision

### Reuse / adapt

The project should compose established ideas rather than invent a bespoke measurement science:

- **AERA / APA / NCME Standards for Educational and Psychological Testing** and Messick-style validity reasoning: validity is evidence supporting interpretations/uses, not a property conferred by software passing tests.
- **Human Behaviour Ontology / Behaviour Change Intervention Ontology**: reuse stable external behavior concepts where they genuinely fit rather than renaming ordinary behavioral constructs into project-specific terminology.
- **OBO Foundry principles**: stable identifiers, documented definitions, versioning, provenance, reuse before duplication, and explicit deprecation/supersession.
- **Cognitive Atlas / PhenX Toolkit**: use established construct/measurement catalogs as discovery inputs where applicable, without assuming their instruments map directly to Life Patterns narratives.
- **directed/team qualitative content analysis**: frozen codebooks, inclusion/exclusion criteria, examples/near misses, explicit adjudication, and version-controlled changes.
- **within-person / ecological momentary assessment literature**: preserve context and repeated episode information instead of treating one response as a timeless latent trait.
- **Krippendorff-style reliability and chance-corrected agreement**: evaluate the actual coding procedure rather than assuming coder consistency.
- **Gwet agreement coefficients**: useful alongside raw agreement/Krippendorff when class prevalence makes kappa-like coefficients unstable.
- **measurement invariance / differential item functioning concepts**: later test whether language, modality, culture, and other observed collection conditions alter code behavior before pooling indiscriminately.
- **selective classification / reject-option systems**: abstention is a legitimate output; automation must not force a code when evidence is insufficient.
- **Argilla / doccano / Label Studio class of annotation tooling**: use a tool-neutral exchange format rather than building a second bespoke coder UI.

### LLM annotation disposition

LLM annotation is **experiment-only**, not the benchmark. The evidence base is heterogeneous: language models can perform well on some clearly specified annotation tasks, while contextual/sensitive coding can show criterion confusion, systematic bias, and task-dependent failures. Therefore:

- trained-human coding is the initial benchmark;
- any automated coder is version-pinned;
- automation is compared against a frozen human-coded reference set;
- error classes and abstention are reported, not just one average agreement number;
- automation cannot become scoreable merely because it is cheaper or internally consistent.

### Build/adapt/reuse decision

Decision: **composition/adaptation**.

The reusable parts are provenance, versioning, annotation exchange, codebook discipline, reliability reporting, abstention, and catalog/ontology reuse. The project-specific remainder is narrow: bind participant-approved episodic narratives to a neutral observational representation suitable for later multi-model scoring while preserving the chronology and H1 content-authorship boundary.

## H1 substantive-content boundary

The current reasoning chat, Codex/Work executors, and any model already exposed to Human Design/AstroHD repository content are not eligible to author or revise substantive neutral construct content. The binding boundary is documented in:

- `docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_H1_BOUNDARY.md`

Implementation in this PR is therefore limited to schemas, provenance checks, versioning, annotation exchange, reliability-report contracts, deterministic aggregation, synthetic fixtures, and receipt verification/import infrastructure.

Real definitions, inclusion/exclusion rules, theory-sensitive examples, substantive revisions, and any coding instructions that change construct meaning must come from the separately screened H1 human-only content process.

## Artifact chronology

A confirmatory path is:

1. participant interview and approved episodes;
2. participant-reviewed immutable behavioral freeze (`BPF-*`);
3. H1-authored neutral ontology/codebook content frozen independently of participant evidence and target-model output;
4. eligible-author/exposure/content-review authority receipts bound to that exact content hash;
5. human development coding on a development corpus;
6. reliability/validity-development review and codebook revision under version control;
7. a validation-candidate ontology version frozen before validation coding;
8. blind validation coding of behavioral freezes;
9. only coding artifacts passing the scoreability gate may feed later tournament execution;
10. target-model prediction/scoring occurs downstream under the separately frozen tournament contract.

The model tournament preregistration may pin the measurement-bridge/codebook contract before the final coded evidence exists. The eventual tournament execution layer must bind the actual scoreable coding artifact; the preregistration manifest itself should not be rewritten post hoc to include observed target results.

## Neutral ontology release

Implemented in `src/hdmatch/evaluation/neutral_measurement.py`.

Each release has:

- `ontology_id`;
- `ontology_version`;
- release status: `development`, `candidate`, or `frozen_for_validation`;
- scope statement;
- one or more observable definitions;
- exact coding-procedure ID/hash;
- exact aggregation-policy ID/hash;
- exact theory-contamination-policy ID/hash;
- source commit;
- release timestamp;
- `synthetic_fixture_only` flag;
- optional H1 human-content authority receipt;
- a permanent statement that software validation does not establish construct validity.

The full payload is canonicalized and content-addressed as `LPO-*` with SHA-256. Immutable writes reuse the repository-wide canonical artifact primitives.

### Stable IDs and semantic revision

An observable may retain an ID only when its core meaning remains stable. The semantic fingerprint includes at minimum:

- definition;
- unit of analysis;
- value type / allowed values or numeric bounds;
- `insufficient` semantics;
- `not_applicable` semantics.

Changing core meaning under the same stable ID is rejected by the successor check. A genuine semantic revision gets a new ID and may declare `supersedes_observable_id`.

## Observable definition contract

Each observable records:

- stable ID and label;
- definition;
- unit of analysis;
- value type;
- categorical values or numeric bounds;
- explicit `insufficient` and `not_applicable` semantics;
- inclusion criteria;
- exclusion criteria;
- evidence requirements;
- positive examples, near misses, and ambiguity examples where supplied by eligible content authors;
- participant-review policy;
- theory-contamination policy;
- external concept references;
- origin status: reused / adapted / project-specific / synthetic placeholder;
- validity-development status;
- reliability status;
- supersession metadata;
- release notes.

A construct marked as exact reuse requires an external source reference. External references identify the source, external ID, relation, version where available, citation, and optional URL.

## Coding state model

Episode coding distinguishes:

- `observed`: evidence supports one code value;
- `contradicted`: relevant evidence contradicts the coded proposition and no affirmative value is asserted;
- `mixed`: the same frozen episode supports multiple mutually relevant values;
- `insufficient`: evidence is not sufficient to decide;
- `not_applicable`: the observable does not apply to the episode.

`insufficient` is not zero evidence, and `not_applicable` is not a negative observation. Neither may carry artificial classifier confidence.

Informative codes require explicit source-turn provenance. Values must conform exactly to the frozen observable codebook.

## Frozen evidence binding

The bridge verifies the behavioral-freeze content address before coding. It independently checks:

- exact approved episode hashes;
- exact frozen participant source-turn hashes;
- unique source-turn identities;
- exact key-set correspondence between source turns and their hash index;
- episode-to-source-turn provenance;
- frozen input modality;
- participant-revision provenance.

A coded record cannot cite a source turn outside its frozen episode. A forged outer freeze hash does not rescue stale inner episode/source-turn hashes.

## Coder identity and blindness

Every coding run identifies the coder and version.

Human coders require a training receipt. Automated coders require a pinned implementation hash. Coding runs affirm that birth data and chart/model outputs were unavailable to the coder.

An automated coder may not become tournament-scoreable without a separate human-benchmark automation-validation receipt.

This is an engineering gate, not a claim that the automation is valid; the actual human comparison artifact must exist.

## Annotation exchange

Implemented in `src/hdmatch/evaluation/annotation_exchange.py`.

The exchange format is canonical JSONL and intentionally tool-neutral. Annotation tasks include:

- behavioral freeze ID/hash;
- ontology ID/hash;
- episode ID/title/narrative;
- exact frozen source turns associated with the episode;
- eligible observable IDs;
- coding-guidelines hash;
- explicit birth/chart-model blindness.

Responses bind back to the exact task, freeze, episode, ontology, and observable and cannot cite turns outside the task.

This permits future use of mature annotation tools without making those tools part of the scientific record format.

## Aggregation policy

The current generic aggregation is descriptive and distribution-preserving. It does **not** infer one timeless trait value.

For each observable it reports:

- number of episode records;
- applicable episodes;
- informative episodes;
- insufficient episodes;
- not-applicable episodes;
- coverage fraction among applicable episodes;
- state counts;
- value counts, preserving values seen in `mixed` records;
- number of distinct observed values;
- context coverage.

The explicit semantic label is:

`descriptive_distribution_preserving_no_trait_collapse`

Any future transformation from these distributions to a model-specific prediction target belongs in a separately frozen scoring/model-adapter contract, not in the neutral measurement layer.

## Reliability report contract

The framework provides immutable reliability-report artifacts with:

- exact ontology and coding-procedure hashes;
- exact development-corpus hash;
- comparison type: human–human, human–automated, or automated–automated;
- reference and comparison coder IDs;
- per-observable double-coded N;
- class distribution;
- raw agreement;
- optional Krippendorff alpha;
- optional Gwet AC;
- abstention rate;
- adjudication rate;
- confusion matrix;
- error-category counts;
- an explicit statement that reliability does not establish construct validity.

The schema records statistics; it does not fabricate them or set universal numeric thresholds. Thresholds must be preregistered for the actual coding context, justified by consequences and prevalence, and frozen before confirmatory use.

## Validation and reliability readiness

A substantive ontology can be structurally marked `frozen_for_validation` only with H1 human-content authority. That alone is not sufficient for scoring.

A coding artifact is blocked from `scoreable_for_model_tournament=True` when any of the following apply:

- it is synthetic;
- the ontology is not frozen for validation;
- H1 human-content authority is absent;
- the coding run is empty;
- the run is not a validation run;
- a used observable has not reached `validity_status == validation_candidate`;
- a used observable has not reached a declared human reliability baseline (`human_baseline_evaluated` or `automation_evaluated`);
- an automated coder lacks a human-benchmark automation-validation receipt;
- any provenance/integrity blocker is present.

This prevents software-valid artifacts and H1-authorized content from being mistaken for measurement-ready evidence.

## H1 authority-binding adapter

Implemented in `src/hdmatch/evaluation/h1_authority.py`.

The adapter is one-way verification/import infrastructure. It pins the existing Survey-v2 H1 exposure-adjudication specification and can:

- verify content-addressed externally validated H1 receipts;
- recheck the already-frozen eligible-branch semantics;
- bind author eligibility to the exact content freeze and H1 artifact;
- require content-review receipts;
- require H1 eligibility for any content-influencing reviewer;
- derive the compact human-content authority receipt used by the ontology layer.

It cannot:

- run H1 exposure adjudication;
- call an adjudication model;
- classify an author;
- repair an ambiguous/ineligible result;
- contact candidate authors;
- authorize H1 execution;
- create substantive constructs.

The current Survey-v2 H1 freeze manifest is specification-only and explicitly does not authorize H1 implementation/execution or human authorship. That external human dependency remains open.

## Synthetic fixture policy

Software tests may use only visibly non-authoritative placeholders such as:

- `OBSERVABLE_ALPHA`;
- `STRUCTURAL_READINESS_ALPHA`;
- `VALUE_ONE`, `VALUE_TWO`;
- `CONTEXT_ALPHA`;
- fake hashes and synthetic evidence IDs.

Synthetic ontology releases cannot be frozen for validation and cannot produce tournament-scoreable research evidence.

Structural tests may exercise the schema path with fake authority hashes only when they are unmistakably labeled as software fixtures. Such tests do not constitute scientific or H1 authority.

## Invariance and heterogeneity plan

Before broad pooling, development work should report code behavior across observed collection conditions where sample size permits, including at least:

- language;
- typed vs voice-derived transcript;
- participant-revised vs unedited episode summaries;
- context/life phase;
- coder identity/version.

Formal measurement-invariance or differential-functioning analyses should be added when a substantive ontology and sufficient sample sizes exist. The current framework preserves the metadata needed for those analyses but does not claim they have been performed.

## No post-hoc target repair

Once a validation ontology/codebook and coding run are frozen:

- target-model results cannot be used to alter the coded evidence;
- a construct definition change creates a successor ontology version;
- development revisions cannot be applied retroactively to a confirmatory validation run;
- participant corrections remain provenance-visible and cannot be rewritten as if they had been original unprompted evidence.

## Implementation receipt

The content-neutral framework milestone is recorded in:

- `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-BRIDGE-RECEIPT-2026-09-03.md`

The H1 authority-binding milestone is recorded in:

- `state/LIFE-PATTERNS-H1-CONTENT-AUTHORITY-BINDING-RECEIPT-2026-09-03.md`

The last implementation head verified before the H1 receipt/documentation-only commits was:

- `0a948cf32a72678f519bc37f9916a441bc04a85d`
- GitHub Actions run `33794321062`
- 412 passed / 6 expected environment or shallow-checkout skips;
- Ruff clean;
- mypy clean across 137 source files.

## Genuine next blocker

No theory-exposed AI should continue by inventing neutral construct content or target-model mappings under neutral aliases.

Substantive progression requires an eligible H1 human-authored ontology/codebook package, exact H1 authority receipts, an independent content review, and human reliability-development evidence. Until those exist, confirmatory measurement and real tournament execution remain fail-closed.
