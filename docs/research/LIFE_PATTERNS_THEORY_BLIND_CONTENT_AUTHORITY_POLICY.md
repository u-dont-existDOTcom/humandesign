# Life Patterns — Theory-Blind Content Authority Policy

Status: **binding owner-approved Life Patterns policy, superseding the prior human-only substantive-content requirement for this project only**.

Date: 2026-09-03

## Purpose

The neutral behavioral measurement layer must not be designed to make Human Design, AstroHD, astrology, or any other candidate birth-derived model look good. The relevant scientific safeguard is therefore **theory-blind construct development**, not the unrealistic requirement that an author—human or AI—has literally never encountered astrology-related ideas in their life or pretraining corpus.

This policy changes the Life Patterns content-authority rule from `human-only H1 authorship` to `documented theory-blind authorship with provenance and contamination controls`.

It does **not** alter the separately frozen Survey-v2 H1 exposure-adjudication contract or authorize execution under that contract. It applies to the Life Patterns neutral measurement bridge only.

## Eligible substantive authors

Substantive neutral construct content may be authored by either:

1. a human working under a documented target-theory blind;
2. an AI/model session working under a documented target-theory blind.

An author is not automatically disqualified merely because they or the model may have generic prior familiarity with astrology, personality systems, or behavioral science.

The decisive question is whether target-theory information capable of steering the content was available in the relevant authorship context.

## Required blind

During substantive construct generation or revision, the authoring context must not contain:

- Human Design or AstroHD names, terminology, mappings, or predictions;
- astrology target constructs, chart features, or model-specific prediction logic;
- participant birth data or chart outputs;
- candidate-model identities when those identities would reveal the intended mapping problem;
- model-fit results, scores, rankings, residuals, error patterns, or any indication of which constructs discriminate candidate models;
- repository question-bank mappings or other target-theory-derived construct lists;
- instructions to add, remove, split, combine, or redefine constructs because of their relationship to a target model.

The author may receive ordinary behavioral narratives, generic measurement requirements, coding constraints, and theory-neutral methodological requirements.

## AI authorship provenance

When an AI/model authors substantive content, preserve as much of the following as available:

- exact input prompt;
- exact first-pass output;
- model/product identity and version when known;
- date/time of generation;
- whether the session/chat/account was fresh;
- explicit attestation that target-theory material was absent from the session context;
- any later prompts or revisions, in order.

A fresh account/chat is useful because it reduces conversation-history contamination, but it does not prove that the model had no relevant pretraining exposure. Pretraining exposure is a residual risk, not automatic disqualification.

## Prompt-author contamination

A theory-blind generator can still be steered by a theory-exposed prompt author. Therefore prompt provenance matters separately from generator provenance.

### Minimally seeded neutral prompts

A theory-exposed project member or model may supply a **minimal generic measurement prompt** that specifies only broad methodological constraints such as:

- code concrete reported behavior rather than personality labels;
- preserve context, counterexamples, missingness, and source evidence;
- avoid diagnoses, moral judgments, and hidden-cause inference;
- choose the substantive behavioral domains independently;
- do not infer or ask for an external theory or target hypothesis.

Such a prompt should avoid enumerating target-sensitive behavioral domains or candidate distinctions.

### Detailed domain-seeding prompts

If a theory-exposed source supplies a prompt that enumerates substantive behavioral domains or distinctions, the resulting artifact may still be retained as a **development candidate**, but it is not sufficient by itself for confirmatory validation-candidate status.

Before promotion, obtain at least one independent minimally seeded theory-blind replication and reconcile the frameworks without target-model performance information.

## Theory-exposed audits after freeze

A theory-exposed reviewer may audit an already frozen draft for obvious leakage, provenance failures, redundancy, codability, causal overreach, missingness problems, or software/schema incompatibility.

Such a reviewer must not silently rewrite the frozen artifact.

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
5. human development/double-coding evidence exists for the coding procedure;
6. unreliable, redundant, or ambiguous distinctions were handled using blind development evidence rather than target-model performance;
7. the final validation-candidate artifact is frozen before confirmatory model mapping/scoring;
8. later changes create a new version and cannot be retroactively inserted into the frozen validation artifact.

## Human reliability benchmark remains required

Allowing theory-blind AI authorship does **not** make AI coding the benchmark.

The existing neutral-measurement rule remains:

- trained-human coding is the initial reliability benchmark;
- automated coding requires comparison against a frozen human-coded reference set before it can become tournament-scoreable;
- reliability does not establish construct validity;
- abstention, class prevalence, disagreement, and error patterns must be reported.

## Current Independent Draft v1 disposition

The artifact:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-DRAFT-v1-2026-09-03.md`

was generated by a separate target-theory-blind ChatGPT context and contains no obvious direct Human Design/astrology leakage in the subsequent theory-exposed audit.

However, its seed prompt was authored by the current theory-exposed project chat and enumerated several behavioral domains. Under this policy, v1 is therefore a **development candidate** and is not by itself sufficient for validation-candidate promotion.

The matching audit is:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-v1-LEAKAGE-AND-CODABILITY-AUDIT-2026-09-03.md`

## Relationship to the previous H1 human-only boundary

`docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_H1_BOUNDARY.md` records the previous, more conservative human-only rule. This policy supersedes that rule for Life Patterns substantive measurement content.

The existing software receipt types are still named and constrained around `HumanContentAuthorityReceipt` / H1 human-authorship artifacts. Until that implementation is generalized, software validation may continue to block AI-authored substantive content even when it satisfies this policy. That is an implementation mismatch to repair; it must not be misrepresented as a scientific requirement.

## Non-negotiable chronology

The intended confirmatory chronology remains:

1. chart-blind participant interview;
2. participant review/correction;
3. immutable behavioral freeze;
4. theory-blind neutral measurement development;
5. blind pilot coding and human reliability work;
6. frozen validation-candidate measurement release;
7. blind validation coding;
8. separately authorized/preregistered candidate-model comparison;
9. locked execution/reveal after all blockers are satisfied.

Birth/model information must not feed back into interview, participant review, behavioral freeze, neutral construct development, neutral coding, or pre-freeze revision decisions.
