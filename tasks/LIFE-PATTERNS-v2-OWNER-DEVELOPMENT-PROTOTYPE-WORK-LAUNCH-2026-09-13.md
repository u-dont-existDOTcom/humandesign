# Work launch — Life Patterns v2 owner-development prototype — 2026-09-13

Recommended Work reasoning level: **Medium**. Chat has already settled the architecture, semantic constraints, method fork, scope, and stop boundary. Work should execute, not redesign.

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Start here

1. Fetch the **live** PR #24 head. Do not rely on the head written in an older handoff.
2. Read `AGENTS.md`.
3. Read `tasks/ACTIVE-TASK.json` and confirm task id `life-patterns-v2-owner-development-prototype`.
4. Read `state/CURRENT-STATE.md` and the overlay it names.
5. Read `state/LIFE-PATTERNS-v2-OWNER-PROTOTYPE-METHOD-FORK-2026-09-13.md`.
6. Read and execute `tasks/LIFE-PATTERNS-v2-OWNER-DEVELOPMENT-PROTOTYPE-2026-09-13.md` exactly.
7. Read the accepted v2 architecture/contract and `src/hdmatch/evaluation/participant_adjudicated_v2.py` before writing code.

## Execution constraints

- Do not redesign the accepted semantics.
- Do not restore the historical automatic Life Patterns Map generator as person-level authority.
- Prefer a small new v2-specific harness over broad modification of the historical app.
- Do not add production auth/recovery, voice, deployment, target-model code, recruitment/contact, or other future infrastructure.
- Do not spend money or make paid model/API calls. A provider abstraction or deterministic/synthetic test double is acceptable; live paid inference is not authorized.
- Never commit private owner/participant narrative text, private runtime source data, browser state, credentials, or screenshots containing it.
- Keep PR #24 draft/open/unmerged.

## Product requirement

The owner must be able to exercise one understandable interaction slice rather than inspect raw JSON:

`episode -> proposed source-grounded facts -> fact accept/correct/not-supported -> candidate recurring-pattern question -> accept/revise/reject/unresolved -> optional one-step refinement -> human-readable result`

The persisted/validated state underneath that interaction must use the accepted v2 core. Candidate patterns remain provisional until participant adjudication.

For the owner-development prototype, it is acceptable for candidate facts/pattern text to enter through a development-only proposer/test-double boundary rather than a paid external model. Keep that boundary explicit so later LLM integration cannot bypass participant adjudication.

## Verification

Run the focused prototype tests required by the active task plus:

`.venv/bin/python -m pytest tests/unit/test_participant_adjudicated_v2.py -q`

Run only additional affected checks needed by the files actually changed. Do not turn this iteration task into a release campaign.

Before stopping, verify directly that:

- a correction creates an append-only fact revision;
- a rejected/not-supported fact is not operative;
- a pattern does not become accepted before participant adjudication;
- revise produces the next proposal using participant-approved wording;
- reject stays rejected;
- postproposal examples cannot become preproposal evidence;
- absence claims remain four-gate controlled;
- the historical automatic map generator is not used in the new acceptance path.

## Stop condition

Stop when a small owner-usable prototype exists, focused checks are green, and an owner-test handoff is ready. Update canonical state so the next gate is **OWNER PRODUCT JUDGMENT**.

Do not scale the implementation after that point. Do not merge or deploy.

Return a concise receipt containing:

- exact final commit/head;
- files changed and why;
- focused commands and results;
- how the owner can exercise the prototype;
- any limitations that materially affect product judgment;
- confirmation that no private narrative was committed and no paid inference/spending occurred.
