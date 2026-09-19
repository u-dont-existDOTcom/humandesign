# Life Patterns provider-credit boundary — 2026-09-18

Status: RUNTIME HARDENED; OWNER OUTCOME BLOCKED BY EXTERNAL API CREDIT.

## Observed failure

The owner reported a second immediate failure after the prior input-routing repair. Railway HTTP evidence showed the new operation returning 503 in under one second. A newly created synthetic session then reproduced the same immediate 503, ruling out the recovered owner session as the necessary cause.

A privacy-safe provider adapter was deployed and the synthetic check was repeated. It recorded:

- HTTP status: 429
- provider error type: insufficient_quota
- provider error code: credit_balance_exhausted
- retryable: false

No private prompt, participant text, or raw provider body is logged by this diagnostic.

## Changes

1. Provider HTTP/network failures are converted to allowlisted metadata rather than carrying raw provider response bodies.
2. Genuine transient failures, including ordinary rate limiting, receive bounded automatic retry with bounded Retry-After handling.
3. Credit exhaustion is not retried and is surfaced to the participant as an actionable saved-state error.
4. The browser continues preserving the draft and revision-bound saved operation.
5. Legacy recovered pattern memory sent to Sol is compacted: full historical coverage blocks are not duplicated into every semantic call. The separate planning coverage memory remains, and the participant/research views are unchanged.

## Verification

- provider retry/unit tests: PASS;
- quota non-retry test: PASS;
- workflow/API actionable-error test: PASS;
- browser consumer suite: 21 PASS, zero page errors;
- browser specifically proves credit-exhaustion detail is visible and draft is preserved;
- Ruff with repository CI settings: PASS;
- strict mypy: PASS, 208 source files;
- hosted CI 35404982329: SUCCESS;
- Railway deployment 8ac6820b-8090-4b4c-b167-ba8db5b6c473: SUCCESS;
- live /healthz: build survey-sol-xhigh-2026-09-18.6, commit 9558017606d408beead3ddfa59b25fa828b3862f, GPT-5.6 Sol/xhigh, no automatic model fallback;
- live synthetic answer: expected 503 with exact safe credit-balance-exhausted guidance.

The last live check is a failure-boundary verification, not a successful semantic-turn test. A successful post-compaction Sol turn cannot be measured until provider credit is restored.

## Stopping boundary

All independent in-scope repairs are complete. Continuing the same provider/model requires an account payment/credit action. That is an explicit spending boundary and cannot be performed autonomously. Switching provider would materially change provider/cost semantics and likewise requires owner authority.

After credit restoration, retry the preserved saved operation; no earlier interview answers need re-entry.
