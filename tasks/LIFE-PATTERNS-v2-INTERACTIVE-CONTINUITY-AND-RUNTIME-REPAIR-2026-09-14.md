# Life Patterns v2 — interactive continuity + runtime repair — 2026-09-14

Status: **BOUNDED REPAIR REQUIRED BEFORE OWNER JUDGMENT**.

Repository: `u-dont-existDOTcom/humandesign`  
Branch: `codex/discover-life-patterns-mvp`  
PR: #24 — keep draft/open/unmerged.

Read first:

1. `tasks/ACTIVE-TASK.json`
2. `state/CURRENT-STATE.md`
3. `state/LIFE-PATTERNS-INTERACTIVE-INTERVIEW-CONTINUITY-FINDING-2026-09-14.md`
4. `state/LIFE-PATTERNS-v2-OWNER-REAL-DATA-PRODUCT-JUDGMENT-2026-09-14.md`
5. `state/LIFE-PATTERNS-PATTERN-FIRST-v8-DESIGN-RECEIPT-2026-09-05.md`
6. `state/LIFE-PATTERNS-PATTERN-FIRST-LONGITUDINAL-INTERVIEW-PROMPT-v8-2026-09-05.txt`
7. accepted v2 semantic architecture/contract and implementation disposition named by canonical state.

## Goal

Restore a usable owner-only conversational probe without repeating the product-layer mistake of making evidence coding the participant experience.

The intended synthesis is:

`pattern-first adaptive conversation -> minimal concrete anchors / contrasts / life-phase evidence -> hidden v2 evidence ledger -> informative synthesis / boundary check -> participant authority -> immutable freeze`

This is not a semantic redesign of v2 and does not authorize downstream target-model activity.

## Repair A — structured-output normalization

The live model returned a non-`surface_hypothesis` move carrying hypothesis fields, causing Pydantic failure:

`non-hypothesis moves cannot carry hypothesis fields`

Repair at the model-output boundary, before `ConversationMove.model_validate`:

- for `follow_up`, `request_contrast`, or `boundary_question`, normalize `hypothesis_proposition` to `None` and `evidence_fact_ids` to empty;
- retain the strict `ConversationMove` invariant after normalization;
- do not silently downgrade an invalid `surface_hypothesis`; it must still require a nonempty proposition and evidence IDs;
- add a regression test using a model payload that reproduces the owner-visible failure.

Prefer a small explicit normalization helper in the conversational module over deployment-only monkeypatching.

## Repair B — atomic turn behavior

Current `turn()` appends the participant message and applies extracted hidden evidence before planning the interviewer move. If planning/validation then fails, the in-memory session may be partially mutated.

Make one participant turn transactional for in-memory session state:

- if extraction, planning, move validation, or move post-processing fails, restore the pre-turn conversation and v2 record/session flags;
- a failed HTTP turn must not leave duplicate-able hidden facts, source provenance, episode state, boundary state, or conversation turns behind;
- add a regression test showing a failed planner call leaves state identical to pre-turn state.

Do not weaken append-only semantics for successful turns.

## Repair C — restore the earlier pattern-first participant-facing strategy

The original roadmap and v8 interview already established that the participant-facing product is an adaptive interview, not a coding form. V8 specifically corrected episode-first elicitation.

Change the opening and bounded probe so the first user-facing move invites a recurring, changing, puzzling, or context-dependent pattern in the participant's own words rather than requiring an arbitrary specific episode first.

Then use concrete situations as evidence anchors and falsification/contrast material:

- one main question per turn;
- ask for context boundaries or life-phase change when informative;
- ask for only enough concrete evidence to anchor/challenge the reported pattern;
- seek a meaningful contrast or exception rather than exhaustive detail;
- surface a synthesis only when it adds information beyond paraphrase and satisfies v2 grounding requirements.

Do **not** restore v8's fixed domain order as a closed ontology. Historical domains may be optional coverage scaffolding only. Preserve open-world residual patterns.

A general self-description supplied before any bounded episode may remain conversational context; do not manufacture an `EpisodeV2` or episode fact from a non-episode statement solely to satisfy the ledger. Ground any eventual person-level proposal in valid preproposal episode evidence under the accepted v2 contract.

## Scope invariants

Preserve:

- target-theory blindness;
- participant authority over person-level pattern claims;
- append-only corrections/provenance on successful turns;
- genuine-absence gating;
- immutable first-proposal evidence timing;
- no automatic person-level recurrence reconstruction from episode facts;
- no historical `/map` or automatic Life Patterns Map as person-level authority;
- no birth/chart/model access in the interview/evidence layer.

No external participant collection, automated participant coding, target-model scoring/reveal, recruitment/contact, merge/release, new public deployment, or unapproved spending.

## Verification

At minimum run:

`python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_app.py tests/unit/test_participant_adjudicated_v2.py -q`

Run touched Ruff and strict mypy. Run `python scripts/task_preflight.py` and require `PREFLIGHT_OK`.

If code changes are committed, hosted CI on the exact candidate head must be green before redeployment.

## Deployment boundary

The existing owner-only authenticated Railway service may be updated after the repair is verified because owner-only prototype deployment is already authorized in canonical state. Do not create a new service or broaden access.

After a successful redeploy, verify `/healthz` and one synthetic/nonprivate turn that exercises a normalized non-hypothesis move before asking the owner to resume natural testing.

## Stop condition

Stop after a verified owner-only repaired deployment and return the exact head, CI status, deployment ID/status, and owner test URL. Product-value judgment remains the owner's next action; do not infer success from technical verification.
