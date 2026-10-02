# Action approval + review-handle incident — 2026-10-02

## Owner-observed UX
After importing the recovered 81-turn source and answering current setup/consent, ChatGPT displayed an external Action approval card for `startLifePatternsReview` without enough plain-language advance explanation. The owner reports several separate Allow prompts in the run. This is likely alarming to ordinary participants unless the workflow explains the Railway domain and why multiple per-step approvals can appear.

## Review-handle failure
The start-review POST returned HTTP 200. Privacy-safe Railway HTTP logs then show the local review worker claimed the queued job and later posted a successful worker result. The client later reported that the private `review_id` was unavailable and therefore could not call the status endpoint. The participant record/review was not lost; the transport handle was.

The exact private review ID recovered during diagnosis is intentionally not committed.

## Root cause
The server already provides idempotency by `request_id`: replaying the same `request_id` with the same candidate returns the existing review. But the shipped recovery artifact preserved only the candidate, not the outer request envelope/request ID. The client therefore had no durable key from which to recover the private review handle.

## Repair
- Explain external Railway permission cards before the first Action, including that several cards can appear across separate steps and that `Allow once` authorizes only that step.
- Preserve the exact candidate backup **and** an exact `life-patterns-review-handoff.json` request envelope before the first review call.
- Preserve a transport-only review receipt after success when possible.
- If `review_id` is lost, replay the same saved request envelope. Do not mint a new request ID and do not start a duplicate job.
- Add regression coverage for request-envelope preservation and instruction presence.

This changes transport/recovery UX only. It does not alter frozen question wording, admitted behavioral evidence, review semantics, or CF-003 ordering.
