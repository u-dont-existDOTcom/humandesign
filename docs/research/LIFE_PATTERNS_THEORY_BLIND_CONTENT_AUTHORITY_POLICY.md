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

## Preserved development sequence

The project now preserves the substantive development chain as separate immutable artifacts:

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

## Blind pilot protocol

The required human reliability-development procedure is specified in:

`docs/research/LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md`

The protocol requires independent pre-adjudication human coding, explicit non-action prerequisites, separate reporting of segmentation/applicability/value/sequence/missingness/context reliability, preserved original coder outputs, and theory-blind post-pilot revision.

It does not authorize coder recruitment/contact or spending.

## Implemented theory-blind authority contracts

The generic machine-checkable authority contract is implemented in:

`src/hdmatch/evaluation/theory_blind_authority.py`

It supports human or AI theory-blind authorship and separately binds:

- exact content;
- authoring-context provenance;
- prompt and first-output hashes for AI-influenced authorship;
- prompt-author exposure / seed level;
- independent replication and reconciliation where required;
- blind human-human reliability evidence for validation promotion;
- exact-content theory-blind review;
- chronology and content-address integrity.

A detailed theory-exposed seed prompt can create a development-candidate authority artifact without pretending the contamination concern disappeared. It cannot create validation-candidate authority unless the required replication/reconciliation and blind human reliability evidence exist.

Blind reliability-pilot receipt contracts are implemented in:

`src/hdmatch/evaluation/pilot_reliability.py`

They provide immutable/content-addressed corpus-manifest, independent first-pass, and post-freeze adjudication receipts. Reliability must be computed from the frozen pre-adjudication outputs.

## Current Independent Draft v1 disposition

The artifact:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-DRAFT-v1-2026-09-03.md`

was generated by a separate target-theory-blind ChatGPT context and contains no obvious direct Human Design/astrology leakage in the subsequent theory-exposed audit.

However, its seed prompt was authored by the current theory-exposed project chat and enumerated several behavioral domains. Under this policy, v1 was therefore only a **development candidate** by itself.

That prompt-steering concern has since been addressed at the development stage by the separately preserved minimally seeded replication and theory-blind reconciliation. Validation promotion remains blocked on actual blind human reliability-development evidence.

## Relationship to the previous H1 human-only boundary

`docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_H1_BOUNDARY.md` records the previous, more conservative human-only rule. This policy supersedes that rule for Life Patterns substantive measurement content.

The old `HumanContentAuthorityReceipt` / H1 adapter remains in the repository as a legacy compatible path for content that actually used that stricter process. It must not be used to relabel AI-authored content as human-authored.

The generic theory-blind authority and pilot receipt contracts are now implemented, but `src/hdmatch/evaluation/neutral_measurement.py` still wires `frozen_for_validation` directly to the legacy human-only receipt field. Until that core integration is generalized, software validation may continue to block an otherwise policy-compliant theory-blind validation candidate. This is a remaining implementation mismatch, not a scientific requirement, and it must not be bypassed by fabricating a legacy human receipt.

## Non-negotiable chronology

The intended confirmatory chronology remains:

1. chart-blind participant interview;
2. participant review/correction;
3. immutable behavioral freeze;
4. theory-blind neutral measurement development;
5. independent theory-blind replication/reconciliation where required;
6. blind pilot coding and human reliability work;
7. theory-blind post-pilot revision/review;
8. frozen validation-candidate measurement release;
9. blind validation coding;
10. separately authorized/preregistered candidate-model comparison;
11. locked execution/reveal after all blockers are satisfied.

Birth/model information must not feed back into interview, participant review, behavioral freeze, neutral construct development, neutral coding, or pre-freeze revision decisions.
