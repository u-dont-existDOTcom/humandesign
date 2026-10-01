**VERDICT: AGREES.** Deploy the bounded pilot.

All ten findings are resolved in substance. I'm taking your reported bwrap probe and live run as given. Nothing left can expose out-of-task data, bill an API, or break blinding or consent, and claim and answer binding hold. What remains are recovery and usability gaps that fail closed, plus one rare path (R1) that can mislabel a record.

**Weakest remaining step:** recovering from a review error (R1).

## Original findings

| # | Status |
|---|---|
| 1 Reachable files / return paths | **Resolved.** bwrap exposes only the task dir, a copied `auth.json`, read-only `/usr` and resolver/cert files. `HOME` is empty and `CODEX_HOME` holds only `auth.json`. Project docs, memories and tools are off, and `--json` tool events are rejected. With nothing outside the task reachable, the free-text return paths can only carry that participant's own data. |
| 2 Paid API / provenance | **Resolved.** `login status`, `auth_mode` check, `forced_login_method`, scrubbed env, CLI model mapping, and `returned_model: null` labelled as requested only. |
| 3 Claim binding | **Resolved.** Claim ID plus lease check, a heartbeat that kills Codex when the claim is lost, idempotent replays, encrypted outbox, single-instance lock, and 409/422 handling. |
| 4 Answer binding | **Resolved.** Each question gets a `clarification_id`, and replays with the same `operation_id` are idempotent. |
| 5 Skip / stop / withdraw | **Resolved** on server and worker. Withdrawal clears the job and stops work already running. How the GPT records a skip: R2. |
| 6 Authority | **Resolved.** The instrument ships with the job. The pin hash, the prior state's version and the receipt's version are all checked. |
| 7 Clarification-turn shape | **Resolved for answered turns.** Skipped turns: R2. |
| 8 One submission per review | **Resolved.** `gpt_review_finalizations`, with `ready` re-checked inside the transaction. |
| 9 Linkage | **Resolved.** Receipts, state hash and admitted evidence are stored with the submission. |
| 10 Hardening | Token lengths **resolved**. The retry instruction is still missing: R1. |

## Residuals (none blocking; each is a line or two)

**R1 — Error retries no longer reliably resume from the last good `worker_state`.** My earlier review listed this under "What holds"; it no longer does. `complete_gpt_review` stores whatever state the worker posts.
- **The 422 repair wipes the state.** The repair in `process_one` sends `worker_state=None`. After `retry`, `prepare_state` rebuilds from the bare candidate while `clarification_history` stays.
  - If the re-plan asks a question again, the round after that fails permanently with `review_history_state_mismatch`.
  - If it goes straight to review, the job becomes `ready` without the earlier answers. The submission still matches, because `expected_review_behavioral` includes the history, and is stored as `independent_review_completed: true`.
  - This needs a server-rejected result followed by a retry, so it's rare.
- **Engine errors may be stored as-is.** If the Engine turns a Codex failure into `phase: "error"`, that state is stored. `retry` then helps only if `Engine.advance` can restart from `error`, which I couldn't see.
- **The GPT isn't told about retry.** `retry` is now the only way to re-queue, since resending the start body returns the same job.
- **Fix:**
  - In `complete_gpt_review`, assign `worker_state` only when it is non-null and its `phase` isn't `"error"`.
  - Add one GPT line: on `error`, if the participant asks to try again, call `controlLifePatternsReview` with `retry`.

**R2 — The instructions don't say how to record a skipped clarification in the frozen primary.** `expected_review_behavioral` expects that turn with `answer_text: null`. The GPT text only covers "after the participant answers, append…", so a skipped turn is easily left out or written as `""`. That causes a generic 422 at final submission, so the records go by manual delivery and the ready review is never linked to them.
- **Fix:**
  - Add one line: "A skipped clarification is still appended: exact question, `route_id` as `canonical_question_id`, `answer_text: null`, empty arrays."
  - Optionally, name the first mismatching index and field in that 422.

**R3 — Some permanent rejections stall the only worker.** The outbox re-raises any status outside {401, 409, 422}, for example a 413 when a result exceeds `BodyLimit`. `main` then retries the same POST forever and never claims another job. This is unlikely with candidates small enough to pass through the Action.
- **Fix:** treat every 4xx other than 401/408/409/429 like 422.

**Minor:**
- `process_one` swallows the exception, so failures leave no local trace. Log the `review_id` and the exception type.
- The receipt's `semantic_calls` don't include `cli_model`.

## Couldn't verify
`engine.py` and `domain.py` weren't in the pasted material, and the working directory returned nothing.
- **Unchanged from before:**
  - whether `import_record(..., "prior_json")` passes GPT-authored `conditions` into Admission;
  - whether `maximum_calls=12` counts saved calls from earlier rounds. If it does, long clarification chains end `resource_limited`.
- **New, and quick to check:** whether two `engine.advance` calls always end at a question or a review for a full-length transcript. If imports are processed in batches, `run_review` posts `error` with code `ready`. A small synthetic run wouldn't show this.
