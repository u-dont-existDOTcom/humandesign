# Life Patterns Neutral Measurement Bridge — Research Specification

Status: development specification. No target-model execution, validation promotion, participant/coder contact, spending, merge, or deployment is authorized by this document.

## Purpose

Convert participant-approved Life Patterns behavioral evidence into a theory-neutral, auditable measurement layer suitable for later empirical comparison without allowing Human Design, AstroHD, astrology, birth data, or model-fit information to shape the behavioral target.

## Scientific chronology

1. chart-blind participant interview;
2. participant review/correction;
3. immutable participant-reviewed behavioral freeze;
4. theory-blind neutral measurement development;
5. independent theory-blind replication/reconciliation where required;
6. theory-blind development coding with external calibration;
7. theory-blind post-pilot revision/review;
8. select/freeze a validation measurement route before target-model results;
9. frozen validation-candidate measurement release;
10. blind validation coding;
11. separately authorized/preregistered model comparison;
12. locked execution/reveal only after blockers are satisfied.

Birth/model information must not feed backward into interview, participant review, behavioral freeze, neutral construct development, neutral coding, calibration, or revision.

## Current substantive candidate

Canonical development artifact:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

It contains 22 primary episode-level observables. Recurrence, context variability, temporal change, and several state-linked comparisons are derived from primary episode codes rather than treated as separate independent observations.

The candidate is theory-blindly reconciled and development-ready, but **not yet a validation candidate**.

## Theory-blind content authority

Binding policy:

`docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`

Substantive measurement content may be authored by humans or AI/model contexts when target-theory steering information is absent and exact provenance is preserved.

A detailed theory-exposed seed prompt is development-eligible only after the documented independent minimally seeded replication/reconciliation safeguards are satisfied.

## LLM-primary development coding

Default development protocol:

`docs/research/LIFE_PATTERNS_LLM_PRIMARY_CODING_PROTOCOL.md`

Rationale: a detailed multi-observable coding system imposes substantial attention burden on full-corpus human coding, while exact human-human agreement is neither realistic nor the scientific target. A high-capability theory-blind LLM can be used as the primary production coder if its stochastic/model stability and external human calibration are explicitly measured rather than assumed.

Development requirements:

- exact codebook/procedure/prompt frozen;
- repeated isolated automated coding passes, at least three when feasible;
- exact raw outputs retained;
- unresolved pass disagreement preserved;
- one theory-blind human auditor independently codes a sampled subset without seeing LLM labels first;
- human-versus-model disagreement is inspected against source evidence and operational definitions;
- theory-exposed owner coding, if used, is a separate post-freeze sensitivity analysis only.

The conventional full human-human benchmark remains available at:

`docs/research/LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md`

but is no longer the required default development route.

## Measurement objects

### Ontology release

`ObservableDefinition`, `OntologyReleasePayload`, and `OntologyReleaseArtifact` provide:

- stable observable IDs;
- definitions and exact allowed values;
- inclusion/exclusion/evidence requirements;
- explicit insufficient/not-applicable semantics;
- origin, validity, and reliability status;
- immutable/content-addressed release artifacts;
- semantic-fingerprint checks preventing silent meaning changes under the same stable ID.

A validation-frozen ontology must carry exactly one content-authority path:

- legacy stricter `HumanContentAuthorityReceipt`; or
- generic `TheoryBlindContentAuthorityReceipt`.

The two authority paths cannot be asserted simultaneously.

### Behavioral-freeze evidence binding

`freeze_evidence_index_from_artifact` verifies:

- outer freeze content address;
- approved episode hashes;
- source-turn identities/hashes;
- episode-to-source-turn provenance;
- input modality;
- participant-revision provenance.

Coding cannot cite evidence outside the frozen episode provenance.

### Episode coding

`CodedEpisodeRecord` supports:

- observed;
- contradicted;
- mixed;
- insufficient;
- not applicable.

Informative values require explicit source-turn evidence and must be valid under the exact observable codebook.

Episode coding cannot directly assign non-episode derived observables.

### Annotation exchange

`annotation_exchange.py` supplies canonical tool-neutral JSONL tasks/responses for use with external annotation tools without coupling the scientific format to one UI.

### Aggregation

`aggregate_person_observables` remains descriptive/distribution-preserving and does not force a trait midpoint or personality type.

### Reliability reports

`ReliabilityReportArtifact` records raw agreement, class distribution, confusion matrices, optional chance-corrected coefficients, abstention/adjudication, and error categories. Reliability does not establish construct validity.

### LLM-primary calibration receipts

`automated_annotation_calibration.py` records:

- each isolated automated coding pass;
- exact corpus/codebook/procedure/prompt hashes;
- model identity/version when available;
- whether prior pass outputs were unavailable;
- ensemble unanimous/majority/unresolved counts;
- blind human calibration-audit provenance;
- automated-human comparison artifact;
- explicit statements that model self-consistency does not establish correctness and calibration does not establish construct validity.

### Human-pilot receipts

`pilot_reliability.py` remains available for human-coded calibration/benchmark subsets, preserving corpus manifests, pre-adjudication first-pass freezes, and post-freeze adjudication.

## Validation authority routes

Before confirmatory target-model scoring, the project must freeze exactly one measurement-validation route without seeing target-model results:

1. `human_human_benchmark` — conventional independent human benchmark;
2. `statistically_justified_llm_substitution` — frozen statistical substitution decision using independent human calibration data; or
3. `automated_measurement_instrument` — preregistered automated instrument with stability/human-audit evidence and an explicit no-human-gold-standard-equivalence claim.

`TheoryBlindContentAuthorityPayload` enforces exactly one route for validation-candidate authority. Development-candidate authority must not carry a validation route.

For a detailed theory-exposed seed prompt, validation authority still requires the independent minimally seeded replication and reconciliation already preserved by this project.

Route choice cannot depend on which route favors the target model.

## Scoreability gate

`neutral_measurement.py` now implements the generic authority path as well as the legacy H1-compatible path.

For scoreable validation coding:

- ontology must be `frozen_for_validation`;
- exactly one valid content-authority path must be present;
- a generic theory-blind receipt must itself be `validation_candidate`;
- used observables must be `validation_candidate`;
- used observables must have completed readiness status (`human_baseline_evaluated` or `automation_evaluated`);
- coding run must be a validation run;
- automated coders must carry a frozen calibration/validation receipt;
- ordinary integrity/provenance checks must pass.

LLM self-consistency alone cannot create a scoreable artifact.

## Tournament boundary

Neutral coding remains upstream of the model tournament. Actual scoreable coding inputs should be bound later by a tournament execution-input receipt after the validation measurement route, ontology, coding procedure, and frozen coding artifact are all locked.

Do not rewrite preregistration artifacts post hoc to contain observed target outcomes.

## Current blocker

The former software-only H1/human-human mismatch is resolved. The remaining blocker is **empirical rather than structural**:

- the current 22-observable codebook is still a development candidate;
- no real repeated automated development-coding ensemble has yet been frozen against the exact codebook/corpus/prompt;
- no independent human calibration subset has yet been completed/frozen;
- no Route A/B/C validation decision has yet been frozen;
- therefore no validation-candidate ontology or target-model scoreable coding artifact exists.

The next legitimate step is to pin the exact automated coding prompt/model/corpus and human calibration selection rule, then run the theory-blind development calibration sequence under separate authorization. No target-model adapter or tournament execution should be used to bypass this chronology.
