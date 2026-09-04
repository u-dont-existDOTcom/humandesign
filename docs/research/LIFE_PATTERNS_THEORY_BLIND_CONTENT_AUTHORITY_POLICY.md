# Life Patterns — Theory-Blind Content Authority Policy

Status: **binding owner-approved Life Patterns policy, superseding the prior human-only substantive-content requirement for this project only**.

Date: 2026-09-04

## Purpose

The neutral behavioral measurement layer must not be designed to make Human Design, AstroHD, astrology, or any other candidate birth-derived model look good. The relevant scientific safeguard is therefore **theory-blind construct development and theory-blind measurement**, not the unrealistic requirement that an author or coder—human or AI—has literally never encountered astrology-related ideas in their life or pretraining corpus.

This policy changes the Life Patterns content-authority rule from `human-only H1 authorship` to `documented theory-blind authorship/coding with provenance and contamination controls`.

It does **not** alter the separately frozen Survey-v2 H1 exposure-adjudication contract or authorize execution under that contract. It applies to the Life Patterns neutral measurement bridge only.

## Eligible substantive authors

Substantive neutral construct content may be authored by either:

1. a human working under a documented target-theory blind;
2. an AI/model session working under a documented target-theory blind.

An author is not automatically disqualified merely because they or the model may have generic prior familiarity with astrology, personality systems, or behavioral science.

The decisive question is whether target-theory information capable of steering the content was available in the relevant authorship context.

## Required blind

During substantive construct generation, revision, or neutral coding, the relevant context must not contain:

- Human Design or AstroHD names, terminology, mappings, or predictions;
- astrology target constructs, chart features, or model-specific prediction logic;
- participant birth data or chart outputs;
- candidate-model identities when those identities would reveal the intended mapping problem;
- model-fit results, scores, rankings, residuals, error patterns, or any indication of which constructs discriminate candidate models;
- repository question-bank mappings or other target-theory-derived construct lists;
- instructions to add, remove, split, combine, redefine, or recode constructs because of their relationship to a target model.

The author/coder may receive ordinary behavioral narratives, generic measurement requirements, coding constraints, and theory-neutral methodological requirements.

## AI authorship/coding provenance

When an AI/model authors substantive content or performs primary coding, preserve as much of the following as available:

- exact input prompt/procedure;
- exact first-pass output;
- model/product identity and version when known;
- date/time of generation;
- whether the session/chat/workspace was isolated/fresh;
- explicit attestation that target-theory material was absent from the relevant context;
- any later prompts or revisions, in order;
- for repeated coding, pass identity and whether prior pass outputs were unavailable.

A fresh account/chat is useful because it reduces conversation-history contamination, but it does not prove that the model had no relevant pretraining exposure. Pretraining exposure is a residual risk, not automatic disqualification.

## Prompt-author contamination

A theory-blind generator can still be steered by a theory-exposed prompt author. Therefore prompt provenance matters separately from generator provenance.

### Minimally seeded neutral prompts

A theory-exposed project member or model may supply a **minimal generic measurement prompt** that specifies only broad methodological constraints such as:

- code concrete reported behavior rather than personality labels;
- preserve context, counterexamples, missingness, and source evidence;
- avoid diagnoses, moral judgments, and hidden-cause inference;
- choose substantive behavioral domains independently where domain generation is the task;
- do not infer or ask for an external theory or target hypothesis.

Such a prompt should avoid enumerating target-sensitive behavioral domains or candidate distinctions.

### Detailed domain-seeding prompts

If a theory-exposed source supplies a prompt that enumerates substantive behavioral domains or distinctions, the resulting artifact may still be retained as a **development candidate**, but it is not sufficient by itself for confirmatory validation-candidate status.

Before promotion, obtain at least one independent minimally seeded theory-blind replication and reconcile the frameworks without target-model performance information.

## Theory-exposed audits after freeze

A theory-exposed reviewer may audit an already frozen draft or coding pipeline for obvious leakage, provenance failures, redundancy, codability, causal overreach, missingness problems, or software/schema incompatibility.

Such a reviewer must not silently rewrite the frozen artifact or blind coding outputs.

If a theory-exposed audit identifies a needed substantive change, the repair must be performed in a theory-blind authoring context using theory-neutral instructions. The original artifact and audit remain preserved.

## Development versus validation authority

### Development candidate

A substantive artifact may be marked development-candidate when:

- the exact artifact is frozen and content-addressable;
- target-model outputs were unavailable to the authoring context;
- provenance is documented;
- obvious direct target-theory leakage has not been identified, or any concern is explicitly recorded;
- unresolved contamination/reliability issues are documented rather than hidden.

### Validation candidate

A substantive artifact may be promoted to validation-candidate only after all applicable requirements are satisfied:

1. exact content and generation/revision provenance are frozen;
2. no target-model fit/results were available during substantive development or revision;
3. if a theory-exposed source materially seeded substantive domain selection, an independent minimally seeded theory-blind replication exists;
4. reconciliation/revision occurred without target-model results;
5. external calibration/reliability evidence exists for the coding procedure under a frozen validation route;
6. unreliable, redundant, or ambiguous distinctions were handled using blind development evidence rather than target-model performance;
7. the final validation-candidate artifact and coding pipeline are frozen before confirmatory model mapping/scoring;
8. later changes create a new version and cannot be retroactively inserted into the frozen validation artifact.

## Human calibration is required; full-corpus human coding is not

Allowing theory-blind AI authorship/coding does **not** make self-consistency equivalent to truth. A high-capability LLM can be consistently wrong.

The project therefore requires independent human calibration evidence before automated coding is treated as confirmatory measurement, but does **not** require two humans to code the entire corpus.

The default development route is now specified in:

`docs/research/LIFE_PATTERNS_LLM_PRIMARY_CODING_PROTOCOL.md`

It uses repeated isolated high-capability LLM coding across the development corpus plus a smaller theory-blind human audit/calibration subset.

At development stage, one blind human auditor may be sufficient to detect gross model/codebook failures and inform theory-blind revision. A second human is not a prerequisite to begin development coding.

Before confirmatory model scoring, one validation route must be selected and frozen without target-model results:

### Route A — conventional human benchmark

Use sufficient independent theory-blind human coding to establish external reliability.

### Route B — statistically justified automated-annotator substitution

Use a prespecified human calibration design large enough to statistically test whether the frozen automated annotator is an acceptable substitute for human annotators. This may require multiple humans and a larger calibration subset, but only on the calibration subset rather than the full corpus.

### Route C — explicit automated measurement instrument

Treat the frozen automated coding pipeline itself as the measurement instrument. Report replicated-model/test-retest stability plus independent human spot-audit evidence, and do not claim that its labels are a human gold standard. The methods justification and acceptance criteria must be frozen before confirmatory target-model scoring.

Route choice must not be made retrospectively based on which route improves target-model performance.

Regardless of route:

- reliability does not establish construct validity;
- raw agreement, prevalence, abstention, disagreement, and error patterns must be reported;
- unresolved automated disagreement is not silently forced into a label;
- automated production coding must be compared with independent human evidence on a frozen subset before confirmatory use.

## Preserved development sequence

The project preserves the substantive development chain as separate immutable artifacts:

- first independent theory-blind draft;
- theory-exposed leakage/codability audit;
- minimally seeded independent replication;
- replication crosswalk;
- exact reconciliation prompt;
- exact theory-blind reconciled candidate.

The current reconciled development candidate is:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

The exact reconciliation prompt is:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-RECONCILIATION-PROMPT-v1-2026-09-03.md`

The reconciliation reduces the substantive primary layer to episode-level observables while moving recurrence, context variability, temporal change, and state-linked comparisons to derived summaries or metadata where appropriate. This is still a **development candidate**, not a validation candidate.

## Pilot protocols

Default LLM-primary development route:

`docs/research/LIFE_PATTERNS_LLM_PRIMARY_CODING_PROTOCOL.md`

Stricter alternate all-human benchmark route:

`docs/research/LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md`

The latter remains methodologically usable but is no longer a prerequisite for current development.

Neither protocol authorizes coder recruitment/contact or spending by itself.

## Implemented theory-blind authority contracts

The generic machine-checkable authority contract is implemented in:

`src/hdmatch/evaluation/theory_blind_authority.py`

It currently encodes the earlier stricter human-human reliability requirement for validation promotion. That contract is now **more conservative than this policy** and must be generalized before a non-Route-A validation candidate can be represented in software.

This mismatch is safe in the short term because it fails closed; it must not be bypassed by fabricated human receipts.

Blind reliability-pilot receipt contracts are implemented in:

`src/hdmatch/evaluation/pilot_reliability.py`

They remain useful for any human-coded calibration or benchmark subset. Additional machine-checkable receipts for repeated LLM passes and LLM-human calibration should be added before automated development coding is treated as a frozen pipeline.

## Current codebook disposition

The initial independent draft used a detailed prompt authored by a theory-exposed context, so it was not sufficient alone. That prompt-steering concern has been addressed at the development stage by the separately preserved minimally seeded replication and theory-blind reconciliation.

The current reconciled artifact remains a **development candidate**. It is not promoted merely because several AI generations converged.

## Relationship to the previous H1 human-only boundary

`docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_H1_BOUNDARY.md` records the previous, more conservative human-only rule. This policy supersedes that rule for Life Patterns substantive measurement content.

The old `HumanContentAuthorityReceipt` / H1 adapter remains in the repository as a legacy compatible path for content that actually used that stricter process. It must not be used to relabel AI-authored content as human-authored.

`src/hdmatch/evaluation/neutral_measurement.py` also still wires `frozen_for_validation` directly to the legacy human-only receipt field. Until that core integration is generalized, software validation may continue to block an otherwise policy-compliant non-Route-A validation candidate. This is a remaining implementation mismatch, not a scientific requirement.

## Non-negotiable chronology

The intended chronology is:

1. chart-blind participant interview;
2. participant review/correction;
3. immutable behavioral freeze;
4. theory-blind neutral measurement development;
5. independent theory-blind replication/reconciliation where required;
6. repeated theory-blind automated development coding plus blind human calibration;
7. theory-blind post-pilot revision/review;
8. choose and freeze the validation measurement route without target-model results;
9. frozen validation-candidate measurement release;
10. blind validation coding;
11. separately authorized/preregistered candidate-model comparison;
12. locked execution/reveal after all blockers are satisfied.

Birth/model information must not feed back into interview, participant review, behavioral freeze, neutral construct development, neutral coding, calibration, or pre-freeze revision decisions.
