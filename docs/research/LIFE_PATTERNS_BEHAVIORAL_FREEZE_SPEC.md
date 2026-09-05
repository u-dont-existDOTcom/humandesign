# Participant-Reviewed Behavioral Freeze — v1

Status: implementation specification for PR #24 development branch. No merge/deployment/participant-use authorization.

Independent pre-scan conception: `state/LIFE-PATTERNS-BEHAVIORAL-FREEZE-INDEPENDENT-CONCEPTION-2026-09-03.md`.

## Existing-work scan and build decision

The underlying problems already have strong established components. v1 therefore composes them rather than inventing a new general provenance/validation system.

### Reuse / adapt

1. **W3C PROV** — reuse the entity/activity/derivation/revision conceptual model for provenance. Runtime JSON remains intentionally lightweight rather than becoming a full RDF/JSON-LD PROV implementation.
   - https://www.w3.org/TR/prov-dm/
2. **OSF Registrations** — adapt the distinction between an immutable frozen registration and a still-editable live project. The Life Patterns research freeze is a separate immutable artifact; the participant-owned live profile can continue evolving.
   - https://help.osf.io/article/330-welcome-to-registrations
3. **ICH E6(R3) / mature electronic-research audit trails** — adapt the requirements that original entries remain visible, corrections are attributable/traceable, workflow actions are retained, timestamps are unambiguous, and datasets are finalized before analysis. This project is not claiming regulated-trial compliance; these are data-integrity design baselines.
   - https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106_ErrorCorrections_2025_1024.pdf
4. **Qualitative member checking / participant validation** — adapt synthesized member checking: return interpreted material to participants for correction/refinement. Critically, participant feedback may generate new data rather than merely certify the researcher interpretation, so original synthesis and participant revision must both remain visible.
   - Birt et al. 2016, DOI 10.1177/1049732316654870
   - Koelsch 2013, DOI 10.1177/160940691301200105
   - Motulsky, *Is Member Checking the Gold Standard of Quality in Qualitative Research?*, DOI 10.1037/qup0000215
5. **Dynamic Consent** — reuse the principle of active, granular participant decisions, but do not build a general dynamic-consent platform in this milestone. Freezing is an explicit participant action; later birth-model analysis requires its own authorization boundary.
   - Budin-Ljøsne et al. 2017, DOI 10.1186/s12910-016-0162-9
   - CTRL / Australian Genomics, DOI 10.1038/s41431-020-00782-w
6. **RO-Crate / DataLad** — reuse their reproducible packaging/content-identity ideas conceptually. Do not add either dependency to the runtime MVP. A future export/archive layer can emit RO-Crate or DataLad-compatible research objects if needed.
   - https://www.researchobject.org/ro-crate/specification.html
   - https://www.datalad.org/

### Novel remainder: adapt + compose

No reviewed standard directly solves this project-specific boundary:

`theory-blind participant evidence -> participant-reviewed synthesis -> immutable behavioral hash -> later independent birth-model scoring`

We therefore implement a small domain-specific composition on top of the established patterns above.

### Explicit choice

- provenance semantics: **reuse/adapt W3C PROV**
- immutable-vs-live split: **adapt OSF registration model**
- correction/audit behavior: **adapt ICH/REDCap-style audit trail principles**
- participant review: **adapt synthesized member checking**
- consent: **reuse current explicit consent + add active freeze attestation; defer separate model-analysis authorization**
- artifact packaging: **simple canonical private JSON now; experiment with RO-Crate/DataLad only if interoperability need emerges**
- model-binding freeze protocol: **bespoke composition, benchmarked against the above baselines**

## Scientific architecture

The existing pre-lock boundary remains:

1. chart-blind interview;
2. participant-approved episodes;
3. neutral chart-blind Life Patterns Map;
4. participant review of map claims;
5. immutable behavioral freeze;
6. only later: separately authorized model tournament.

The freeze itself must not receive birth data, chart state, Human Design, astrology, candidate classification, hidden prediction, rank, or model fit.

## Two distinct objects

### Mutable personal profile

The ordinary Life Patterns interview/map is participant-owned and may continue changing as the participant learns more, adds episodes, uses coaching, or corrects old understandings.

### Immutable research freeze

A freeze is a new private artifact. Once created through the application it is never edited in place. Later corrections create append-only amendment events and/or a later separately identified freeze; they never rewrite the earlier scored artifact.

This distinction is non-negotiable.

## Freeze candidate

A candidate is deterministically identified from the exact current behavioral evidence state.

Candidate source material:

- participant-approved episodes only;
- participant source turns referenced by those episodes;
- current Life Patterns Map only if its recorded approved-episode set exactly equals the current approved-episode set;
- map provider receipt;
- descriptive evidence coverage snapshot;
- neutral map pattern claims;
- map important-unknowns field.

Exclude from the research candidate:

- strengths labels;
- friction-point labels;
- Pattern Transfer suggestions;
- reversible experiments;
- coaching messages;
- InnerSignal material;
- birth/model outputs.

Those fields are useful product/coaching outputs, not neutral research claims.

The candidate stores a canonical SHA-256 over its immutable source payload. Re-requesting the same exact candidate returns the existing candidate rather than silently manufacturing a new interpretation.

## Claim review

Each map pattern is one review unit.

Participant actions:

- `approve` — accept the original synthesized claim;
- `edit` — supply corrected participant wording, optionally correcting the neutral pattern status;
- `reject` — state that the synthesized pattern should not be treated as a participant-endorsed profile claim;
- `uncertain` — preserve the synthesis as unresolved/not confidently representative.

Review rules:

- every review is appended as a new event with UTC timestamp and event ID;
- previous review events are never overwritten;
- latest event determines the pre-freeze effective decision;
- original AI synthesis always remains present;
- an `edit` is explicitly flagged `new_data_during_review=true`; it is not misrepresented as merely validation of the original synthesis;
- review cannot change evidence episode IDs or invent new source provenance;
- if the participant wants to add a new factual episode, it should be elicited through the ordinary interview flow rather than smuggled into claim metadata;
- all claims must have an explicit latest review decision before finalization.

## Final participant attestation

Finalization requires an active request containing:

- `attest_profile_reviewed=true`;
- explicit acknowledgment that the snapshot will no longer change after freezing.

This is an attestation to the behavioral snapshot only. It does **not** authorize later birth-model analysis; that remains a separate future boundary.

## Frozen payload

The canonical frozen payload contains:

- schema version;
- session ID;
- candidate ID + candidate hash;
- freeze timestamp in UTC;
- exact approved episode objects;
- exact referenced participant source turns;
- SHA-256 for every included episode and source turn;
- source map SHA-256 and provider receipt;
- evidence-coverage snapshot with explicit `not_completion_denominator` semantics;
- every original pattern synthesis;
- every latest participant review decision;
- final participant wording for approved/edited claims;
- rejected and uncertain claims retained in audit form;
- `admissible_claim_ids` containing only `approve` and `edit` claims;
- important unknowns;
- theory-blindness boundary declaration;
- provenance mapping identifying source entities, synthesis activity, participant-review activity, and freeze-finalization activity;
- explicit future model-comparison boundary.

The canonical payload is serialized as UTF-8 JSON with sorted keys and compact separators. `freeze_sha256 = SHA256(canonical_payload)`.

The wrapper artifact contains:

- `freeze_id = BPF-<hash prefix>`;
- full `freeze_sha256`;
- canonical payload.

## Storage

Write final artifacts under a private `freezes/` directory beneath `HDMATCH_LIFE_PATTERNS_STORE`.

Application behavior:

- create with restrictive permissions;
- never overwrite an existing freeze file;
- if an identical freeze path exists, verify identical bytes and return it idempotently;
- if bytes differ under the same hash-derived ID, fail closed;
- session record stores only a receipt/pointer to the immutable artifact plus append-only review/candidate metadata.

This is application-level immutability plus tamper evidence, not a claim of hardware WORM storage.

## Post-freeze behavior

The participant may continue interviewing and regenerate their mutable map. Nothing should lock the product merely because a research snapshot exists.

A later correction does not alter the old freeze. Future work may implement:

- append-only correction/amendment note tied to a freeze;
- new behavioral freeze from the later evidence state;
- explicit supersession relation for future analyses.

Any model result must bind to the exact `freeze_sha256` it consumed.

## UX

After a current map exists, expose **Review & freeze for research**.

The review panel should:

- explain that the ordinary profile can still change later;
- show one map claim at a time or in a compact list;
- show the original claim and status;
- offer Approve / Edit / Reject / Uncertain;
- preserve participant corrections visibly;
- refuse finalization until every claim has an explicit decision;
- show the final freeze ID/hash receipt;
- state that no birth-model comparison has been run or authorized merely by freezing.

The UI burden of claim-by-claim review is an **experiment**. Pilot data should determine whether bundling low-risk claims or alternative review ergonomics improves completion without sacrificing review quality.

## Acceptance criteria

1. Candidate creation fails without a current map or when the map is stale relative to approved episodes.
2. Candidate contains only participant-approved episodes and research-neutral pattern material.
3. Original synthesis is never overwritten by participant review.
4. Review events are append-only; later pre-freeze review supersedes by event order rather than mutation.
5. Participant edits are marked as new review-phase data.
6. Finalization fails until every claim has a review and the participant attestation is explicit.
7. Final freeze hash recomputes exactly from canonical payload.
8. Final freeze is written as a separate non-overwritten private artifact.
9. Later interview/map changes do not alter prior freeze bytes or hash.
10. Rejected/uncertain claims remain in the audit payload but are absent from `admissible_claim_ids`.
11. Product/coaching suggestion fields are excluded from the research freeze.
12. No birth/chart/model information is introduced into the freeze path.
13. CI, Ruff and strict mypy remain green.

## Out of scope for this milestone

- running any Human Design/astrology/AstroHD/raw-astronomy model;
- birth-data linking;
- consent for a later model tournament;
- public participant recruitment;
- deployment;
- full RO-Crate/DataLad export;
- hardware/managed WORM storage;
- changing PR #23.