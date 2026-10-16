# Life Patterns: honest review progress

This cumulative release updates the existing GPT. Read the bundled instructions before applying it.

The misleading "1 of 1 remaining" means exactly one question in the **current clarification batch**. Additional review rounds may follow, so the total future question count is not known until Railway returns independent review status "ready".

## Apply to existing GPT

1. Replace its Instructions with INSTRUCTIONS-life-patterns-voice-interviewer-v2.md.
2. Replace Knowledge/ACTION-HANDOFF-GUIDE-v1.md with the new copy; keep the other seven Knowledge files.
3. Import ACTION-life-patterns-submission-openapi.yaml into the existing Action, without creating a second Action or changing existing private authentication.
4. Click Update and resume the SAME saved conversation.

The package is cumulative over October 15 and contains no participant records.

## Accurate progress footer

"Current stage: independent clarifications. Answers already submitted/skipped: [actual count]. Current batch: question i of n. Overall new questions still required: unknown. Next: reconciliation; another admitted batch OR final evidence review; participant confirmation; the three CF-003 questions; final secure submission."

Never say "one more question" or "100% complete" from the current batch count. Only independent review status "ready" closes the clarification stage. Participants can pause/stop; this is not falsely recorded as a completed review.

## Railway finishing screen versus current workflow

Railway already handles independent review and encrypted storage for the GPT. Its separate participant survey is currently disabled; it is NOT a continuation page for an existing GPT review. A safe optional Railway finishing screen would need a review-scoped expiring participant session and full final-review, confirmation and CF-003 support. That cannot be replaced by simply sending the existing reviewer ID in a browser URL.

The current Railway production environment has unrelated pending changes. The new server-side read-only progress extension has been source-tested, but must not be claimed deployed merely because this release ZIP is installed. Existing GPT instructions can report batch-local progress honestly even before a new server deployment.

For immediate correction in the current saved participant chat, see HUMAN-QUICK-CORRECTION.md.
