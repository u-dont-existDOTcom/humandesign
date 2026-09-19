# Owner retest: paraphrase presented as inference, then no next question

Date: 2026-09-18 (UTC).
Status: OWNER RETEST FAILED on the reported direct-report and continuation boundary. Diagnosis completed; no runtime fix deployed in this pass.

## Evidence boundary

The owner supplied a browser recovery checkpoint and reported that a supposed connection merely restated their answer, after which the interview gave them no next move. The original upload was inspected locally without modification. Its internal recovery checksum verifies. No private transcript, source-derived hash, participant/session/turn identifier, or private quotation is included here.

Current development head inspected: `163d426158ae7a537b0d16a7b0f01d33f22227c2`. The application source recorded at that head is `78543a9f876b1105c4d62757b8b5f5119cc7b5e5`. The uploaded checkpoint records semantic policy version 3 and Sol/xhigh request/response metadata. It does not independently bind itself to a producing application commit. The observed transitions agree with the inspected source. No provider inference call, owner-session access, deployment, or source-code mutation was made for this diagnosis.

## F1 — Direct semantic content falls through to inference presentation

Observed: the latest formulation review returns `decision=direct` with empty `inference_added` and `inference_quote`. The formulation summarizes information already supplied across the participant's answers. It is not a contiguous quotation from one source message. Nevertheless, the operation presents it as a possible connection requiring participant judgment.

Causal path in `src/hdmatch/api/life_patterns_v2_owner_workflow.py`:

1. `_create_pattern` recognizes the review as direct and sets `_direct_context_safe`.
2. `_direct_report_source` additionally requires exact contiguous wording in one user message and all cited facts linked to that same source.
3. This summary cannot satisfy those exact-source conditions, so the method returns `None`.
4. `NaturalFlowRecoverabilitySession._create_pattern` in `life_patterns_v2_owner_natural_flow.py` treats that result as permission to fall through to an inferred draft.
5. `_emit_move` displays the generic connection-approval request despite no positive inference decision and no added inference.

The provenance restriction has a valid purpose. The invalid implication is: not an exact single-source quote therefore a new inference. A faithful paraphrase or an assembly of already stated claims is a third case. Failure to auto-record under an exact-source rule must not manufacture a new relationship or a redundant approval burden. This is separate from the extractor-label veto corrected in the preceding deployment.

## F2 — Resolved objection leaves an answer-waiting state with no question

Observed final state: no draft, `phase=awaiting_answer`, `repair_pending=true`, client not paused, no pending operation, and the last assistant response is only a withdrawal acknowledgement. It contains no question. The latest coverage assessment has three sufficient, four partial, and sixteen unassessed areas. These are current-archive assessment states, not a claim that all legacy work was never covered.

Causal path:

1. `_handle_answer` routes the owner's objection as repair and retires the draft.
2. The same generic repair branch always sets `repair_pending=true` and, without a draft, `phase=awaiting_answer`.
3. `_apply` immediately returns for `process_only`, without selecting another interviewer action.
4. The browser's `nextStep()` in `life_patterns_v2_owner_client.py` automatically advances only from `phase=advancing` (apart from restored-draft review).

The interface is waiting for a participant answer to an absent question. This is not a completed interview, an explicit pause, an active provider request, or an observed decision that no useful question remains. The original source facts survive; withdrawing the draft did not retract the participant's reports. No new accepted pattern was created for that area.

## Corrective direction under existing authority

Restore the already-required distinction between evidence capture and discovery presentation. A no-added-inference paraphrase must not become an inferred draft when exact-source recording fails. Retain original statements and qualifications with their actual provenance; use faithful summaries only as labeled summaries. Do not silently attribute model wording to the participant, loosen source safeguards, or treat a rejection of the discovery label as rejection of the underlying self-report. Genuine new inferred relationships still require participant judgment.

Repair handling must distinguish a clarified question that awaits an answer from a resolved objection that leaves no participant action outstanding. After the latter, select the next useful interviewer action on the appropriate focus, or explicitly defer that focus and continue the interview. Do not advance blindly after every clarification, fabricate a user Continue event, or make the owner invent an answer just to restart the workflow.

The next bounded implementation test should use a synthetic multi-turn paraphrase plus a resolved withdrawal, through the real operation/browser composition. It should fail when a direct review still reaches inference approval, and when a resolved repair leaves no useful next action. Preserve explicit pause, genuine clarification, unjudged inference, source integrity, and idempotent recovery as affected negative cases. No new reviewer, model change, episode quota, broad benchmark, or research-acceptance requirement is introduced.

## Progress and limitations

Parent outcome remains OPEN. The owner natural-use verdict is now observed and FAILED on these two boundaries, superseding the earlier not-yet-observed status. Earlier CI and bounded model checks remain historical evidence for their tested scopes; they did not establish these product properties. This pass is EVIDENCE_ACQUISITION and STRATEGY_LEARNING, not an implemented product improvement. The current strategy must change at the semantic-decision-to-runtime-action boundary, not receive another wording-only patch or model upgrade.

This is a source-and-checkpoint causal diagnosis, not a new runtime replay, general accuracy estimate, independent evaluation, or scientific validity judgment. No new test-suite run was required for this documentation-only diagnosis. The narrow checksum/structural checks were performed locally.

## Active obligation application

Activation route: current owner bootstrap and project AGENTS, then the live UDA root (blob `94404a13885f169ae8d43f088e32f9ef7d491bb3`), lesson index, and applicable source-provenance, task-time activation, iteration-lane, executable-frontier, outcome-progress, and write-isolation guidance.

Applied: source versus inference remains distinct; owner failure is not converted into a pass by old test counts; the missing next action is traced to actual server/client transitions; no private narrative or source-derived identifiers/hashes enter Git; only an isolated documentation delta is integrated; no model spending or deployment occurs. Research-before-reinvention is not applicable to this narrow diagnosis; no new bespoke method is implemented. Added mandatory owner requirements: none. The existing no-redundant-confirmation and automatic-continuation requirements determine the corrective target.

**There was never a completion policy.** Preserve the accepted evidence contract and existing owner authority; this diagnosis does not redefine scientific completion.
