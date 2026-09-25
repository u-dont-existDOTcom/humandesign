# Life Patterns v2 owner-development prototype — 2026-09-13

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
PR: `#24` (remain draft/open/unmerged)

## Objective

Build the smallest owner-usable development prototype that exercises the accepted v2 flow end to end:

`episode -> episode facts -> participant fact review/correction -> candidate pattern question -> participant adjudication/revision -> accepted/rejected/unresolved pattern`

This is a product/interaction probe, not a new semantic-design phase or production campaign.

## Read first

1. `tasks/ACTIVE-TASK.json`
2. `state/CURRENT-STATE.md`
3. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-12.md`
4. `state/LIFE-PATTERNS-v2-OWNER-PROTOTYPE-METHOD-FORK-2026-09-13.md`
5. `state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-SUBSTRATE-v2-CANDIDATE-2026-09-12.md`
6. `state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-CONTRACT-v2-CANDIDATE-2026-09-12.json`
7. `src/hdmatch/evaluation/participant_adjudicated_v2.py`
8. current task-relevant UDA guidance activated by root `AGENTS.md`.

Historical fixed-codebook and automatic map-generation behavior is development history, not authority for this task.

## Hard boundaries

- Do not change the accepted v2 semantics/contract.
- Episode facts stay open-world and source-grounded.
- Real-world nonoccurrence uses the four-gate absence route only.
- Fact corrections are append-only.
- Candidate patterns are questions/hypotheses, never automatically accepted person-level claims.
- Participant decisions are `accept | revise | reject | unresolved`.
- A revised proposal must preserve participant-approved wording as required by v2.
- Post-first-proposal examples are scope/boundary evidence, not unbiased recurrence-frequency evidence.
- No episode-count threshold overrides participant rejection.
- No birth/chart/target-model information enters the prototype.
- No adapter may recreate person-level recurrence from episode facts.

## Required owner-visible slice

1. Load or enter one bounded development episode.
2. Show proposed episode facts in ordinary language.
3. Allow fact accept, correction, or not-supported handling; corrections must create new v2 revisions rather than mutate prior history.
4. Present a plain-language candidate pattern question only after usable preproposal evidence exists.
5. Allow pattern accept, revise, reject, or unresolved.
6. If revised, support one recursive refinement turn.
7. Show resolved status, accepted wording when applicable, scope/exception notes, and evidence provenance.
8. Produce and validate the corresponding v2 record through `participant_adjudicated_v2.py`.

**Owner-visible means the owner personally makes these choices at runtime. A scripted demonstration with preselected correction/revision/acceptance does not satisfy this requirement or reach OWNER PRODUCT JUDGMENT.**

Use synthetic fixtures and/or already-existing owner development material at runtime. Do not commit narrative-bearing development inputs to Git.

## Non-goals

Do not add production auth/recovery, voice, deployment, public hosting, external recruitment/collection, spending, target-model scoring, a comprehensive taxonomy, automatic Life Patterns Map generation from episode facts, broad refactors, or merge/release work.

Prefer a small new v2-specific development harness over retrofitting the full historical app. A minimal local FastAPI/HTML surface is acceptable. Do not add infrastructure merely because it may be useful later.

## Focused tests

Prove at minimum:

- fact correction creates a new revision;
- unsupported proposed facts do not become operative facts;
- pattern proposal remains provisional until adjudication;
- revise creates the next proposal with participant wording;
- reject cannot become an accepted resolved pattern;
- postproposal evidence cannot become preproposal evidence;
- absence routing remains gated;
- resulting record passes the frozen v2 validator;
- historical auto-map generation is not used to create accepted patterns;
- runtime owner inputs, not hard-coded demo choices, determine the interactive result.

Run the focused prototype tests plus `tests/unit/test_participant_adjudicated_v2.py`.

## Authorization

Authorized: bounded owner-only development/stress testing of this prototype.

Still unauthorized: external participant collection, recruitment/contact, target-model activity, public deployment, spending, merge/release.

## Stop boundary

Stop after a small genuinely owner-usable prototype and focused green tests. The next gate is **owner product judgment**. Do not scale the architecture before that judgment.
