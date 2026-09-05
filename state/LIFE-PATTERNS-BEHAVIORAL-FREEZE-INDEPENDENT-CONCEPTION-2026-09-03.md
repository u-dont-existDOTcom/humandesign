# Life Patterns Behavioral Freeze — Independent Conception Snapshot

Status: pre-existing-work-scan conception snapshot. This records the design before consulting external standards/literature so later adaptation does not overwrite the independent idea.

Date: 2026-09-03
Parent branch state before this snapshot: `e7cee21b880016ca97ef7f1520c193d6d7518fc5` on `codex/discover-life-patterns-mvp` / PR #24.

## Problem

The Life Patterns interview already collects participant-authored turns, AI-extracted provisional episodes, participant approve/edit/reject decisions, descriptive evidence progress, and an evidence-linked Life Patterns Map. Birth-derived models remain blinded from this process. The missing scientific boundary is a participant-reviewed immutable behavioral-profile freeze that can later be scored by independent HD/astrology/AstroHD/raw-astronomy models without allowing post-reveal edits to contaminate the confirmatory record.

The freeze must preserve participant agency without allowing later corrections to rewrite history. It must also preserve provenance from every frozen behavioral claim back to participant-approved episodes and source turns.

## Candidate mechanism

Treat the research freeze as a new immutable snapshot artifact, not as a mutable status bit on the live personal profile.

A freeze candidate contains:

1. exact ordered IDs and hashes of all participant-approved episodes admitted to the snapshot;
2. exact reviewed synthesis/profile claims derived from those episodes;
3. provenance from each claim to supporting and counterexample episode IDs;
4. the neutral coding/synthesis schema version and provider/runtime receipts used to produce the candidate;
5. participant review decisions over every claim or coherent review unit: approve, edit, reject, or explicitly mark uncertain/not-representative;
6. unresolved important unknowns retained explicitly rather than silently omitted;
7. an exact canonical serialization whose SHA-256 becomes the freeze identity;
8. freeze timestamp and session identifier;
9. explicit statement that no birth/chart/model prediction was available to the interview/synthesis/review path;
10. post-freeze corrections recorded as append-only amendments/superseding profile versions, never mutations of the frozen artifact.

## Participant review flow

- Generate a freeze candidate only from participant-approved episodes.
- Show the participant the candidate in plain language with supporting/counterexample episode references.
- Require active review; no implicit acceptance by inactivity.
- Allow participant edits before freeze. Any edit must remain participant-authored/approved and retain provenance to the original candidate plus the evidence episodes.
- Reject claims the participant considers wrong or overgeneralized; rejected material stays in the audit trail but does not enter the frozen behavioral profile.
- Preserve uncertainty and context-dependence rather than forcing categorical closure.
- Final freeze action creates a new immutable snapshot and returns its content hash/receipt.

## Separation after freeze

The frozen artifact is the only behavioral input admissible to the confirmatory model tournament for that analysis cycle. Later interview turns, coaching interactions, InnerSignal sessions, model reveals, and participant amendments are outside that frozen evidence set.

A later correction can create a new personal-profile state and, if scientifically appropriate, a new separately identified research freeze for a future analysis cycle. It must never retroactively alter the prior scored artifact.

## Constraints

- no birth data, chart, candidate class, prediction rank, model fit, or theory-language reinforcement before freeze;
- only participant-approved evidence can enter the candidate;
- no hidden LLM-only claims without participant review;
- exact reproducibility of the frozen payload from its recorded inputs/versions;
- tamper evidence via canonical serialization + hash;
- append-only provenance for candidate creation, participant review, freeze, and later amendment;
- preserve raw participant turns and approved episodes as separate source evidence rather than replacing them with the synthesis;
- the mutable coaching/personal profile can evolve independently after freeze;
- no requirement that all evidence areas be `strong`; uncertainty can be frozen explicitly;
- no fixed question-count completion rule;
- no merge/deployment/participant recruitment authorized by this snapshot.

## Candidate insight

The main architectural distinction is **immutable research snapshot vs mutable participant-owned personal model**. Scientific reproducibility requires the former; participant correction and ongoing usefulness require the latter. Conflating them would either block legitimate future learning or allow post-reveal contamination. Therefore every model score should bind to a specific behavioral-freeze hash, while later personal-profile versions remain useful but scientifically separate.

## Questions for existing-work scan

Search the underlying problems, not the project terminology:

- provenance standards for derived research data and transformations;
- immutable/versioned research records and append-only audit trails;
- participant/member validation of qualitative summaries;
- consent and participant-controlled correction/versioning;
- reproducible dataset snapshots/content-addressed research objects;
- preregistration/lock mechanisms separating measurement from downstream model evaluation.

After the scan, choose explicitly among reuse, adaptation, composition, invention, or experiment for each component.