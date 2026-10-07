# Owner pilot closeout repair — 2026-10-07

## Parent owner outcome

Status: OPEN.

Repair the existing Life Patterns participant flow exposed by the completed owner pilot, while preserving the same review and exact participant source. The repaired flow must:

1. forecast the remaining external Action/Allow sequence at each phase and issue the exact per-call Allow instruction before every consequential call;
2. present final-review evidence with an understandable neutral construct/distinction label, preserve conditions/quotes, and avoid combining unrelated constructs into one apparent trait;
3. remove the obsolete/misleading ChatGPT Memory-enabled question for Custom GPT interviews and explain the actual blinding/visible-context rule at the beginning;
4. make final submission reliably expose and transport both exact frozen records through the Action interface, without weakening server validation;
5. use the private owner pilot as development evidence to improve low-information, obvious, redundant, under-specified, or forced-answer handling without publishing private source text or claiming validation.

## Constraints

- Same GPT, same saved conversation, same Railway review; no replacement review or reconstructed answers.
- Frozen v7 historical wording remains unchanged.
- No birth/chart/astrology/Human Design targets are exposed to participants or used in behavioral coding.
- Private participant text and private review identifiers do not enter public Git.
- Existing object-field submission remains backward-compatible; the Custom GPT Action receives a transport form it can actually expose.
- Purpose/construct labels are neutral measurement explanations, not diagnoses or validated personality verdicts.
- Approval count over an adaptive interview is not falsely promised; phase-local known calls are stated exactly and later conditional calls are described as conditional.

## Implementation lanes

### A. Approval-sequence UX
- Add phase-local forecasts to the handoff guide and active instructions.
- Clarification answer phase: state that one Allow sends the answer batch and a later status retrieval may be a second permission card; do not imply the first Allow completes review.
- Final submission phase: state one final storage Action/Allow is expected.
- Put the instruction in the operation descriptions as another enforcement surface.
- Regression-test the exact wording and absence of silent consequential calls.

### B. Final-review measurement labels and coherence
- Enrich public review entries with neutral measured-distinction labels derived from exact source route lineage.
- Preserve source-quote-to-construct binding so multi-construct evidence can be displayed separately.
- Tighten semantic prompts: one evidence item = one coherent construct; participant process objections are not trait evidence; ordinary/tautological responses are not promoted merely for coverage.
- Update GPT rendering instructions and tests.

### C. Blinding metadata correction
- Remove the Memory-enabled post-freeze question from the CF-003 module.
- At onboarding, say the interview uses only visible/authorized source in the current conversation and excludes visible chart/birth/HD information.
- Keep prior chart-familiarity metadata post-freeze; record actual visible target exposure rather than a generic product setting.

### D. Final-submission transport
- Add JSON-string transport fields for both exact records in the Action-facing request schema.
- Server parses strictly and then runs the same existing validation/hash/linkage/storage path.
- Preserve legacy object-field support outside the Action-facing schema.
- Add successful, malformed, missing-field, non-storage, idempotency, and exact-record tests.

### E. Owner-pilot design audit
- Analyze the exact private 79-answer development record locally.
- Commit only aggregate/public-safe defect classes, route IDs where safe, and design consequences.
- Add low-information/obvious/redundant/under-specified admission rules and regression fixtures.

## Verification and release

- Focused tests after each lane.
- Participant application suite and relevant repository tests.
- Scoped lint/typecheck/diff check.
- Deploy exact tested backend and local reviewer only where runtime code changed.
- Live schema/readback and a synthetic final submission using nonprivate fixtures.
- Build and deliver a superseding same-GPT update packet.
- Preserve the current real review; retry its final submission only if the exact frozen primary and CF-003 records are recovered without reconstruction.
