# Life Patterns v2 provider 520 repair — 2026-09-14

Status: **TECHNICAL REPAIR DEPLOYED; OWNER LIVE TURN STILL REQUIRED**.

## Observed failure

During the repaired pattern-first owner interview, the first participant pattern turn completed normally and the app requested a concrete anchor. The next owner turn failed in the browser with:

`Owner Life Patterns model HTTP 520: error code: 520`

Railway request evidence on deployment `842b13f2-66b2-435e-a918-dbc81cde00e7`:

- session creation: HTTP 200;
- initial pattern turn: HTTP 200;
- first concrete-anchor turn: HTTP 422 after about 11 seconds.

The 422 was the application wrapper translating a runtime exception. The runtime exception itself records an upstream model HTTP 520 response. This is therefore a model-provider transport/gateway failure, not the earlier `ConversationMove` structured-output validation defect and not evidence that the participant input was invalid.

The pattern-first session transaction wrapper already snapshots the conversation, hidden v2 record, flags, and proposal state before model-driven turns and restores that snapshot on exceptions. The failed turn therefore does not become admitted hidden evidence.

No owner narrative from the failed turn is committed in this receipt.

## Repair

### Provider path

The owner-only Railway service is now pinned to the official OpenAI Responses endpoint:

`https://api.openai.com/v1/responses`

Runtime model:

`gpt-5.6-luna`

The service continues to use the existing Railway `OPENAI_API_KEY` reference. No API secret was copied into Git or exposed. `HDMATCH_LLM_API_KEY` is left empty so the existing runtime precedence falls through to `OPENAI_API_KEY`.

This removes the inherited/custom model endpoint from the owner probe's critical path.

### Bounded transient retry

`PatternFirstOpenAIConversationModel` now retries a narrow class of transport/server failures up to three total attempts:

- HTTP 408;
- HTTP 500, 502, 503, 504;
- HTTP 520–524;
- model network errors.

It does not retry ordinary validation/auth/client failures.

If the bounded retry budget is exhausted, the runtime raises `TemporaryModelProviderError`. The HTTP layer maps that to `503 Service Unavailable` with a participant-facing message stating that the model service is temporarily unavailable and that nothing from the failed turn was saved. The existing session transaction rollback remains authoritative.

## Verification

Runtime repair code head:

`8d74d4b89bff1e78922af524dcb5b95f271d9b97`

Regression-test head:

`b52be2a67e458c5d1334d058d7b73e938c04d1ef`

GitHub Actions run `34857710301` on the regression-test head: **SUCCESS**.

The added tests cover:

- an HTTP 520 provider failure twice followed by success on the third bounded attempt;
- exhaustion of all three 520 attempts becoming the retryable temporary-provider error;
- existing strict surface-hypothesis validation and pattern-first/rollback behavior remain covered.

The first test revision attempted to use FastAPI/Starlette `TestClient`, but the repository does not install the new `httpx2` dependency required by the current Starlette test client. That test-only dependency was removed rather than expanding production/dev dependencies for this bounded repair. The final regression remains dependency-free.

Test-efficiency telemetry is `not_applicable` for this repair: Chat did not run repeated local suites; one failed hosted CI run identified the test-only dependency issue, one materially changed candidate was submitted, and the succeeding hosted CI run established the checkpoint.

## Deployment

Existing owner-only Railway service: `life-patterns-owner`.

Deployment `feba6ba2-9677-4f94-b0b8-1cf0e6d530fe` from runtime repair head `8d74d4b89bff1e78922af524dcb5b95f271d9b97`: **SUCCESS**.

Deployment log shows application startup complete and Railway healthcheck `/healthz` returned HTTP 200.

The subsequent regression-test-only commits do not change runtime code and are excluded by Railway watch patterns.

## Current boundary

The technical provider-path repair is complete. Chat cannot replay the authenticated owner interview turn without the owner's Basic-auth credential, and no unauthenticated paid model-call diagnostic route was added merely to bypass that boundary.

Next decision-changing evidence: the owner opens a fresh authenticated session and sends a normal concrete anchor. If that turn succeeds, continue product judgment. If it still fails, inspect the new exact status/body before changing method again.

Still closed: external participant collection, automated participant coding, target-model activity, recruitment/contact, merge/release, broader public deployment, and unapproved spending.
