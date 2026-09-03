# Life Patterns Neutral Measurement — H1 Human-Only Content Boundary

Status: binding execution boundary for the neutral measurement-bridge milestone. This reasserts the project's existing H1 measurement-content policy; it does not authorize new substantive construct content.

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
- validators that block substantive execution until an eligible human-authored content artifact is supplied and separately approved/frozen.

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

Software tests in this PR can verify that the receipt is structurally required. They cannot manufacture or satisfy that human scientific authority.

## No validity inference

This branch may establish only deterministic engineering/governance properties of the measurement framework. It does not establish:

- construct validity;
- coding reliability;
- Human Design/AstroHD validity;
- participant benefit;
- birth-time recovery accuracy;
- empirical model discrimination.

Those require subsequent eligible human content development, reliability work, and independent model testing.
