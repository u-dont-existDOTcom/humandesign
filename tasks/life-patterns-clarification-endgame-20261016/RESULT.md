# Clarification progress and Railway finish — result (2026-10-16)

## What failed

The existing Life Patterns Custom GPT presented "1 of 1 remaining" on each independent-review batch. The server sends **up to three currently admitted questions**, but the independent reviewer can generate another batch after those answers are processed. A single-question batch never established one question remaining in the **entire** review.

Existing instructions mentioned future batches being unknown but did not force a clear distinction in every participant-facing footer. An early source completed as a main interview can still be undergoing multiple independent reviewer rounds and later full evidence synthesis. Earlier question counts are not an accurate lifetime progress denominator.

## Implemented, current source

1. Additive read-only progress in `review_timing.py` and all GPT review status responses, with source-bound **total clarifications already answered/skipped**, size of **current batch only**, an explicit unknown total remaining until status `ready`, and true finite post-`ready` steps: participant source-evidence confirmation, 3 CF-003 items, encrypted final submission.
2. Correct `wait_guidance` to state unequivocally that any batch count is local, that another batch could arrive after reviewer reconciliation, and that no total remaining number is presently known.
3. Patch the existing Action OpenAPI response schema **1.6.1** additively, preserving the same six operations and authentication requirements; no raw review details or personal information are published as part of the new progress fields.
4. Harden the participant-facing GPT Knowledge guide and cumulative Custom GPT instructions. **Never show "1 of 1 remaining" unqualified**. Instead label "Question 1 of 1 IN THIS BATCH; overall future questions UNKNOWN," with actual completed clarifications and next stage. Retain material-information/nonredundancy gates; do **not** impose an arbitrary lifetime question cap.
5. Versioned deterministic cumulative ZIP under `reference/custom_gpt/releases/Life-Patterns-GPT-honest-review-progress-2026-10-16.zip`, maintaining the old 8 Knowledge files and Oct15 source-recovery rules, no participant content or credentials, with strict instruction count **7,957** (<8,000).
6. Owner-ready ZIP and full files installed directly to `~/Téléchargements/Life-Patterns-Progress-Fix-2026-10-16/`. `HUMAN-QUICK-CORRECTION.md` provides an immediately usable instruction in the **same active participant conversation** that requires no GPT editor update or participant restart.
7. Investigated the optional Railway final handoff. Railway already stores and independently reviews GPT answers, but its public participant survey is disabled, and the GPT Action uses service-level authorization. A safe finishing page needs a short-lived review-scoped participant authorization and protected consent/confirmation, separate CF-003, and transactional submission. Blueprint retained in `RAILWAY-FINISH-HANDOFF-DESIGN.md`.

## Outcome and boundary

The immediate **source-code and GPT release package repair is tested and delivered**, but **the production Railway code and private GPT configuration have not been updated by these local changes**. Existing production Railway environment has four unrelated staged changes and an active ongoing participant reviewer; do not accept the entire patch or restart review just to ship these fields. Participant may send the quick corrective message **now** in their existing GPT chat. Only the owner can apply the editor files to the same GPT (after preserving the live recovery state).

The suggested browser-finishing screen is a **design only**, not a live app or offered continuation link. Do not expose the shared Action Bearer credential or internal review IDs to the browser. The participant's source, unanswered routes, review ID, birth data, person identity and consent records were not accessed or committed in this task.

## Verification

- Full repo: `1092 passed, 3 skipped` (three unrelated official Swiss chart smoke fixtures).
- Relevant fast-review API/worker and new progress tests: `18 passed`.
- Authored Python Ruff check/format passed.
- Deterministic GPT ZIP check and owner-local file/manifest readback passed.
- Old Action operation set and old science/interview Knowledge files preserved.
- No new model inference, no new third-party participant-data access, no Railway deployment.
