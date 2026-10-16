# Optional Railway finishing page — assessed design, not a live feature

**Requested experience:** A participant who did the interview in ChatGPT should not have to endure repeated tool approvals and uncertain clarification rounds at the end. Once the independent review reports `ready`, they should be able to finish in one secure Railway page, confirm the evidence, answer the three fixed secondary items and submit. The **entire** earlier source, corrections, conditions, omissions, and exact frozen distinction must survive this handoff.

## Current topology, confirmed October 16

- The existing Custom GPT is already a thin client to the Railway `life-patterns-participant` GPT Action API. That service performs encrypted review storage, fast clarification queuing and final submission.
- GPT still presents the reviewed evidence, obtains participant confirmation, asks CF-003 secondary questions and calls final storage.
- The Railway `PARTICIPANT_LIVE_ENABLED` browser questionnaire is **off** and the Venice inference provider isn't configured in that public service; turning it back on would recreate the old ingestion/provider bottleneck.
- Railway's current review GET requires the same service-level GPT submission authorization used by the Action. Merely sharing the review ID in a public URL would not establish that the browser user is the authorized participant. Never embed the shared GPT bearer credential in a link.
- Production has an unrelated four-change staged environment patch, and the participant is currently using an active review. Do not execute a global accept-deploy or restart mid-review to ship an unrelated front-end experiment.

## Proposed architecture (reuse incumbent Railway, no new host)

1. Only after `GET review.status=ready`, the GPT may offer an optional "Finish privately on Railway" path **at the participant's request**. Ordinary in-GPT completion remains supported.
2. GPT calls a new authenticated Action, e.g. `POST /api/gpt/reviews/{review_id}/issue-finish-link`. The server validates ready state, creates a random one-time 256-bit token, stores only its digest with expiry (e.g. 20 minutes), binds it to one review and an intended permitted action set, and returns a short opaque URL. No raw source, DOB, chart input, bearer secret or stable review ID in the URL.
3. Railway serves a dedicated finishing page. On redeeming the token, it exchanges it once for an HttpOnly, Secure, SameSite session cookie, removes the token from browser history (303 redirect to clean path), and enforces origin/CSRF, rate limits, expiry, and zero analytics of participant answers. Lost link is reissued from the original GPT Action rather than relaxed.
4. On the finishing page, show the **source-exact reviewer-admitted evidence**, conditions and missingness, not chart interpretations or hidden model labels. Participant approves or appends a correction; a material correction restarts independent review under the same source lineage, not a fake finalization.
5. After a clean confirmation, ask the existing three CF-003 questions in their required fixed order. Preserve their separate record, dates, and privacy boundary; no opportunistic extra questions.
6. Submit the unchanged reviewed primary + CF-003 through the same transactional, review-bound encrypted backend path already used for GPT final submission, with idempotent operation identity and explicit receipt. The page confirms completion **only after actual storage receipt**. Multiple submit attempts return the same receipt.
7. Cancel/expiry leaves current source/review unchanged, without creating new review or losing the ability to finish in the GPT.

## Scientific/UX properties and acceptance

- No re-interview, questionnaire restart, duplicate private source, target/chart leakage or required new model calls.
- Does not force a lifetime clarification cap. The Railway finish option is offered only when the independent reviewer actually reaches `ready`. Clarification progress before that stays honestly uncertain.
- The participant knows the exact **remaining finite steps at ready**: evidence confirmation, three secondary answers, storage. This eliminates the prior "1 of 1" presentation error and multiple GPT permission cards *after ready*, without guessing how many earlier reviewer batches may occur.
- Test unauthorized token, reuse, expiry, identity switch, network replay, source-correction rollback, separately stored CF003, successful happy path, and no review-id/Bearer exfiltration before launching.
- Treat Hâle's older edited questionnaire as a development/provenance-limited source; a new finishing page cannot make the earlier source prospectively blind.

## Disposition

**Recommended future step:** Reuse the existing Railway backend to build this narrowly scoped finalization page, rather than re-enabling the whole Venice-powered questionnaire. **Not deployed or live today.** The immediate implemented correction is batch-local progress with accurate overall-unknown status plus a source-preserving in-chat instruction. This minimizes disruption to the active participant review.
