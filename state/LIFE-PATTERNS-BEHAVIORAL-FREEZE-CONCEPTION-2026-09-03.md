# Life Patterns Behavioral Freeze — Independent Conception Snapshot

Date: 2026-09-03  
Repository: `u-dont-existDOTcom/humandesign`  
Branch: `codex/discover-life-patterns-mvp`  
Conception baseline: `e7cee21b880016ca97ef7f1520c193d6d7518fc5`  
Scope: participant-reviewed immutable behavioral-profile freeze only

## Why this record exists

This file preserves the project's independent conception of the next Life Patterns
milestone before consulting external work on provenance, participant correction,
immutable research records, or model-evaluation separation. It is intentionally a
design snapshot, not evidence that the design is novel and not authorization to merge
or deploy.

The implementation should begin only after this design is compared with established
work and any adaptations are recorded separately. GitHub remains canonical.

## Scientific purpose

The freeze creates the boundary between:

1. chart-blind behavioral elicitation and participant review; and
2. later, independently versioned evaluation by Human Design, astrology, AstroHD,
   raw-astronomy, empirical birth-derived, or non-birth baselines.

A downstream evaluator must receive a specific frozen artifact and its digest. It must
not read the mutable interview session, silently regenerate a map, select different
episodes, or write interpretations back into the research record.

The freeze is a record of what the participant reviewed and authorized at a particular
time. It is not a claim that the profile is complete, objectively true, or a fixed trait
description.

## Participant-facing contract

The participant initiates the freeze. The product must explain that:

- only participant-approved episodes count as behavioral evidence;
- AI-generated map language remains an interpretation of that evidence;
- the participant can approve the profile as shown or attach an explicit correction;
- freezing makes this version read-only for reproducible research comparison;
- coaching may continue to read the profile but may not change the frozen research
  record; and
- a later correction must create a new, explicitly superseding version rather than
  rewriting this one.

The request must contain an affirmative immutable-freeze consent, not an inferred
consent from earlier storage or AI-processing consent.

## Eligibility and fail-closed behavior

Freeze is allowed only when all of the following hold:

- the authenticated session is still `in_progress`;
- no episode remains `pending`;
- at least two episodes are participant-approved;
- a schema-valid Life Patterns Map exists;
- the map was built from exactly the current ordered set of approved episode IDs;
- every supporting and counterexample episode reference in the map resolves to an
  approved episode;
- every approved episode's source-turn IDs resolve to stored participant turns when
  source turns are declared;
- the participant chooses either `approve` or `approve_with_correction`;
- `approve_with_correction` includes nonblank participant-authored correction text;
  and
- explicit consent to create an immutable research freeze is true.

Any mismatch fails closed without creating an artifact or changing session status.
Repeated freeze requests fail rather than replace the prior artifact.

## Correction and review provenance

An AI extraction begins as a provisional record. Participant review must append an
attributable review event containing the action and UTC timestamp. An edit must preserve
both:

- the original provisional extraction; and
- the participant-corrected episode that becomes eligible evidence.

The participant's profile-level correction is an addendum to the reviewed map. It does
not silently mutate or replace the AI map. The frozen record must make the participant
correction primary context for any downstream interpretation.

For records created before this milestone, absence of an older provisional copy must be
represented honestly as legacy provenance; the implementation must not invent an
original value.

## Frozen artifact

Write one separate canonical JSON file with exclusive-create semantics. The artifact
contains:

- schema version and freeze ID;
- pseudonymous session ID and UTC creation time;
- participant review action, explicit freeze consent, and optional correction addendum;
- the exact participant-approved episode snapshots, including source-turn links,
  provisional extraction where available, and review events;
- the exact Life Patterns Map the participant reviewed;
- the exact map-provider receipt already stored by the chart-blind mapper;
- ordered approved-episode IDs;
- canonical digests for source conversation turns, approved episodes, and map;
- session and interview schema versions;
- evidence, interpretation, correction, and evaluation-boundary policy identifiers;
- an explicit list of excluded pre-freeze inputs (birth data, chart features, Human
  Design, astrology, candidate states, predictions, ranks, and model fit); and
- a rule that downstream evaluation must bind to the artifact's canonical SHA-256 and
  must remain read-only with respect to the frozen record.

The artifact digest is computed over the exact canonical bytes. The mutable session may
retain only a reference to the new artifact, its digest, freeze ID, and timestamp. That
pointer is useful for retrieval but is not the source of scientific truth.

## Storage and immutability

The store writes the freeze to a dedicated session-derived path using atomic,
exclusive creation and read-only file permissions. Existing freeze bytes are never
overwritten. Loading a freeze requires canonical JSON and digest verification against
the session reference when one exists.

After a successful freeze, these operations fail closed:

- new interview turns;
- episode approve/edit/reject actions; and
- map generation or regeneration.

Read-only retrieval, portable export, and evidence-grounded coaching remain available.
Exports after freeze must identify the freeze digest so consumers can bind to the same
version.

Filesystem read-only permissions are defense in depth, not the scientific guarantee.
The guarantee is write-once application behavior plus canonical byte hashing and
verification.

## API surface

Add participant-authenticated endpoints equivalent to:

- `POST /api/life-patterns/interview/sessions/{session_id}/freeze`
- `GET /api/life-patterns/interview/sessions/{session_id}/freeze`

The POST accepts:

- resume token;
- review action: `approve` or `approve_with_correction`;
- optional correction text, required only for the latter; and
- explicit immutable-research-freeze consent.

The response returns the freeze, its SHA-256 receipt, and the participant-safe meaning
of the lock. The GET verifies and returns the exact frozen bytes represented as JSON and
the same receipt.

## UI surface

When a current map exists, show a distinct final-review card that:

- summarizes what will be frozen;
- offers approve-as-shown or approve-with-correction;
- provides a correction textarea for the second action;
- requires a dedicated consent checkbox;
- warns that this version becomes read-only; and
- displays the freeze receipt after success without implying the participant must save
  it as an access credential.

The ordinary interview composer and map-regeneration controls become disabled once the
profile is frozen. Coaching remains visibly separate and read-only.

## Reproducible downstream boundary

This milestone creates no HD/astrology scorer. It defines the input contract such a
scorer must later use:

`behavioral_profile_freeze_sha256 -> separately versioned evaluation run`

A later evaluation record must bind at minimum to the freeze digest, evaluator/model
version, mapping version, code commit, declared candidate/baseline set, random seed when
used, and output digest. Evaluation artifacts live outside the participant's immutable
behavioral profile and cannot feed back into it.

## Verification requirements

Tests must prove:

- explicit consent and review-action validation;
- pending/stale/invalid evidence prevents freezing;
- participant edits preserve the provisional extraction and append a review event;
- canonical digest stability;
- exclusive creation and refusal to overwrite;
- tamper detection on load;
- all interview/map mutation routes are blocked after freeze;
- exports bind to the freeze receipt;
- coaching does not mutate either session state or freeze bytes;
- freeze inputs and the stored artifact contain no birth/chart/model-evaluation data;
  and
- the full existing suite, lint, and strict type checks remain green.

## Explicit exclusions

This milestone does not:

- decide interview stopping or evidence completeness;
- claim the current two-episode map threshold is scientifically sufficient;
- calculate, reveal, score, rank, or compare any birth-derived model;
- create a post-freeze correction/supersession workflow;
- merge PR #24;
- deploy the product; or
- contact participants.
