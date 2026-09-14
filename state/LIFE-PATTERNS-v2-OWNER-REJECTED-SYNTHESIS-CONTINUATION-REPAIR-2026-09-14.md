# Life Patterns v2 owner rejected-synthesis continuation repair — 2026-09-14

Status: **IMPLEMENTED / CI-VERIFIED / DEPLOYED — OWNER RETEST REQUIRED**.

## Direct owner product evidence

The owner reported a fresh pattern thread in which the interviewer surfaced a tentative synthesis that did not fit. Choosing `No` then ended the entire thread as `rejected` even though the underlying pattern inquiry was still worth pursuing.

This is a **workflow-liveness / adjudication-frontier defect**. A participant rejecting one tentative synthesis is not equivalent to asking the product to abandon the underlying pattern inquiry.

No private interview narrative is persisted in this receipt.

## Causal mechanism

The prior unresolved-continuation repair added `Keep trying to pin it down`, but the existing `No` button remained wired directly to the terminal `reject` adjudication. The UI therefore conflated **proposal-level disagreement** with **inquiry-level termination**.

## Repair

The owner-facing synthesis panel now separates those actions:

- `No — keep investigating` records conversational disagreement with the current synthesis and keeps the same backend session/proposal inquiry live;
- the interviewer asks what the current synthesis gets wrong or misses, then continues collecting discriminating material in the same thread;
- `Reject and stop this thread` is the explicit terminal rejection action;
- `Keep trying to pin it down` remains available for uncertainty that is not an outright disagreement;
- accept, revise, and leave-unresolved remain participant-authoritative terminal/adjudication choices.

The nonterminal disagreement action does not write a terminal `ParticipantAdjudicationV2`, does not create a replacement person-level proposal automatically, and does not alter the accepted v2 evidence semantics. Any new material supplied after the first proposal remains post-proposal evidence and cannot be silently promoted to preproposal support.

Target-theory blindness and privacy boundaries are unchanged: no astrology/predictive-power language is exposed in the pre-freeze interview, and no automatic transcript persistence or private request-body logging was added.

## Verification and deployment

Application repair head: `3536bf88f422551abfb9ff41f63e5690ecdb77e4`.

GitHub Actions run `34876597710`: **SUCCESS**.

- unit/integration tests: passed;
- Ruff: passed;
- strict mypy: passed.

The exact new disagreement path was additionally inspected in the committed source: the `No — keep investigating` handler calls the nonterminal `/patterns/disagree` route, while `Reject and stop this thread` remains the only UI action wired to terminal `decision('reject')`.

A dedicated new reject-path regression file could not be committed because the GitHub write interface blocked the attempted test-file writes. That is recorded as targeted verification debt rather than hidden; the full hosted suite is green on the exact application repair head.

Existing owner-only Railway service reused; no new service and no access broadening.

- service: `life-patterns-owner`;
- deployment: `28e06edc-3266-435d-8830-8adceabfe281`;
- application source head: `3536bf88f422551abfb9ff41f63e5690ecdb77e4`;
- status: **SUCCESS**;
- application startup complete;
- Railway runtime health request: `/healthz` -> HTTP `200`;
- deployed health contract includes `rejected_synthesis_continuation=true`.

## Next decision-changing owner evidence

Refresh the owner-only browser and deliberately test a thread where the first synthesis is wrong. Choose `No — keep investigating`, explain what is wrong or missing, and judge whether the interviewer stays with the same inquiry and uses that correction to ask a useful discriminating next question rather than terminating or starting over.

When genuinely done with that inquiry, use `Reject and stop this thread`, accept, revise, or leave it unresolved. Then use `Finish for now` to judge whether the session summary is useful enough to justify durable persistence / a real Life Patterns Map.

**There was never a completion policy.**
