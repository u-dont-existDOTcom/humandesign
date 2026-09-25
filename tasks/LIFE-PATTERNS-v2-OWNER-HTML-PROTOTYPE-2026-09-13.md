# Life Patterns v2 owner HTML prototype — 2026-09-13

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
PR: `#24` (remain draft/open/unmerged)

## Objective

Replace the terminal/Work-relay owner-judgment surface with a small directly usable HTML prototype that preserves the accepted v2 semantics.

Reuse the visual language of `src/hdmatch/api/life_patterns_interview_ui.py` where useful. Do **not** restore the old person-level auto-map backend.

## Read first

1. `tasks/ACTIVE-TASK.json`
2. `state/CURRENT-STATE.md`
3. `state/LIFE-PATTERNS-v2-OWNER-UX-HTML-FEEDBACK-2026-09-13.md`
4. `state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-SUBSTRATE-v2-CANDIDATE-2026-09-12.md`
5. `src/hdmatch/evaluation/participant_adjudicated_v2.py`
6. `src/hdmatch/evaluation/participant_adjudicated_v2_prototype.py`
7. `src/hdmatch/api/life_patterns_interview_ui.py`

## Required owner experience

The owner should interact directly with a browser/HTML surface, not with a terminal transcript relayed through Work.

For the bounded synthetic episode, present:

1. the episode in ordinary language;
2. the proposed factual summary;
3. natural-language controls equivalent to fact `accept | correct | not-supported`;
4. correction text entry when needed;
5. a conversational candidate-pattern question;
6. natural-language controls equivalent to pattern `accept | revise | reject | unresolved`;
7. editable participant wording for revise;
8. one refinement/grounding check when relevant;
9. a plain-language final result showing accepted/rejected/unresolved/no-pattern status.

Internal research codes may exist behind the UI but should not be the primary participant-facing labels.

## Simplest acceptable implementation

Prefer a **single self-contained HTML file** for owner product judgment if that avoids setup and preserves the interaction accurately. It may use a deterministic synthetic state machine for the UI judgment because the Python v2 core and interaction plumbing are already separately green.

If a small local browser app is simpler, that is also acceptable, but it must not require the owner to install anything or operate a terminal. Work may set it up and return a directly usable browser surface/file.

Do not make production-grade web infrastructure a prerequisite for this test.

## Semantic boundaries

- Do not modify the accepted v2 semantic contract.
- Do not infer person-level recurrence from episode facts automatically.
- Candidate patterns remain hypotheses until participant adjudication.
- Fact corrections remain append-only in the authoritative implementation path.
- Postproposal evidence is not unbiased recurrence evidence.
- Genuine absence claims retain the four-gate route.
- No birth/chart/target-model information enters this prototype.
- Do not use the historical `/map` generator as person-level authority.

## Tests / checks

At minimum verify the HTML surface can exercise:

- fact accept;
- fact correction;
- fact not-supported -> no pattern;
- pattern accept;
- pattern revise -> revised wording -> final decision;
- pattern reject;
- pattern unresolved;
- no old map-generation endpoint or mapper is invoked by the prototype.

Preserve the existing v2 core tests. Run `python scripts/task_preflight.py` after canonical state is updated.

## Authorization

Authorized: bounded owner-only HTML/product-surface development and testing.

Still unauthorized: external participant collection, automated participant coding, target-model activity, public deployment, recruitment/contact, spending, merge/release.

## Stop boundary

Stop when the owner receives a directly usable HTML/browser prototype and can judge the interaction without terminal work or Work acting as a prompt courier.

The next gate after that is **OWNER PRODUCT JUDGMENT** in the supervising chat. Do not scale beyond this surface first.
