# Life Patterns Neutral Measurement — H1 Human-Only Content Boundary

> **Status update (2026-09-03): superseded for Life Patterns substantive measurement content.** The owner approved a broader theory-blind authorship policy allowing either humans or AI/model sessions to author substantive neutral content when the target theory is absent from the relevant authorship context and provenance/contamination controls are satisfied. See `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`. The separately frozen Survey-v2 H1 specification remains unchanged, and the current Life Patterns software still contains legacy human-only authority receipt types that must be generalized before AI-authored content can pass software authority gates.

Status: historical record of the previously binding execution boundary for the neutral measurement-bridge milestone. This document records the former H1 measurement-content policy; it no longer defines the current Life Patterns substantive-content authority rule.

Date: 2026-09-03

## Boundary

The current reasoning chat, Codex/Work executors, and any model that has been exposed to AstroHD, Human Design, repository mappings, prediction logic, or prior theory-linked project discussions are **not eligible to author or revise substantive neutral construct content** for the confirmatory measurement instrument.

That includes:

- observable definitions;
- inclusion/exclusion criteria that determine substantive construct meaning;
- theory-sensitive positive/negative examples;
- substantive codebook revisions;
- prompts whose examples or wording implicitly encode target-model distinctions;
- adjudication rules that change substantive construct boundaries.

Substantive construct-content authorship/revision requires the separately screened human-only H1 process already established by the project. Exposure is adjudicated under that process; content authority cannot be rescued after the fact by removing explicit Human Design vocabulary.

## What this branch may implement now

The current PR #24 branch may implement only **content-neutral measurement infrastructure**, including:

- immutable ontology/codebook artifact schemas;
- stable/versioned identifiers;
- external-source/reuse registry fields;
- generic code-state and missingness semantics;
- provenance/hash validation;
- generic annotation exchange formats;
- generic human/automated reliability-report schemas;
- generic deterministic aggregation interfaces;
- synthetic fixtures using obviously non-substantive placeholders such as `OBSERVABLE_ALPHA`;
- validators that block substantive execution until an eligible human-authored content artifact is supplied and separately approved/frozen;
- verification/import adapters that bind externally validated H1 receipts to exact content hashes without performing H1 adjudication.

## Synthetic fixture rule

Synthetic fixtures MUST be visibly non-authoritative and must not encode real HD/AstroHD constructs under neutral aliases.

Allowed examples:

- `OBSERVABLE_ALPHA`;
- `VALUE_ONE`, `VALUE_TWO`;
- `CONTEXT_ALPHA`;
- synthetic source/evidence IDs.

Disallowed examples:

- realistic neutralized constructs chosen because they correspond to known Human Design/astrology mappings;
- paraphrases of repository question-bank dimensions;
- examples selected to exercise a known chart rule or mapping.

## Downstream execution gate

A measurement ontology/codebook cannot be marked `frozen_for_validation` or used by an executable tournament merely because it passes software validation.

A future substantive release must carry an external human-content authority receipt establishing at minimum:

- eligible H1 human authorship/revision;
- exact content artifact/hash reviewed;
- exposure-screen/adjudication receipt required by the H1 protocol;
- content-review status;
- reliability/validation status required by the measurement-bridge specification.

The Life Patterns H1 adapter is **verification/import only**. It reuses the exact frozen Survey-v2 H1 contract and may verify already validated receipts, but it does not run adjudication, call an adjudication model, contact authors, or create eligibility. The existing Survey-v2 H1 freeze manifest is specification-only and does not itself authorize adjudication execution or H1 authorship.

Software tests in this PR can verify that receipts are structurally required and internally bound. They cannot manufacture or satisfy the human scientific authority.

## No validity inference

This branch may establish only deterministic engineering/governance properties of the measurement framework. It does not establish:

- construct validity;
- coding reliability;
- Human Design/AstroHD validity;
- participant benefit;
- birth-time recovery accuracy;
- empirical model discrimination.

Those require subsequent eligible human content development, reliability work, and independent model testing.
