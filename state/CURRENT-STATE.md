# Current state — Life Patterns — 2026-09-18

The latest owner natural-use attempt failed immediately again. This second failure is not the prior unknown-historical-source bug. A fresh synthetic session failed the same way, proving the problem is global to the configured model-provider boundary rather than specific to the owner's recovered interview.

Privacy-safe provider diagnostics now identify the exact response: HTTP 429, error type insufficient_quota, error code credit_balance_exhausted, retryable=false. Model API credit is therefore the current external blocker.

Application code head: 9558017606d408beead3ddfa59b25fa828b3862f. Railway deployment 8ac6820b-8090-4b4c-b167-ba8db5b6c473, build survey-sol-xhigh-2026-09-18.6, health HTTP 200. Hosted CI run 35404982329: SUCCESS. GPT-5.6 Sol/xhigh remains the only configured semantic model and there is no weaker fallback.

## Independent repairs completed before stopping

The provider boundary now classifies failures without logging provider body text. Retryable 429/rate-limit, network, and transient 5xx failures receive bounded automatic retries. insufficient_quota / credit_balance_exhausted is deliberately not retried because repeated calls cannot restore account credit.

The UI now receives an actionable error: the model API credit balance is exhausted, the participant response is preserved, and API credit must be added before retrying. The actual browser suite verifies that this message is visible and that the draft remains intact.

The model-planning context was also compacted. Legacy recovered patterns no longer resend their full embedded 23-domain coverage reports to every semantic call. Their wording/status remains available, while historical coverage planning is already carried separately. Current source-backed items retain exact source text for fidelity. The participant-facing pattern view and research archive remain unchanged. This removes a major avoidable token/cost multiplier without changing Sol/xhigh, participant authority, or evidence semantics.

## Evidence and limits

A fresh synthetic live session on the hardened deployment still returns 503 in under one second, now with the correct safe detail that the API credit balance is exhausted. This establishes the external account boundary. It does not establish the cost or semantic quality of a successful post-compaction turn because the provider will not execute one until credit exists.

Focused and affected tests passed; the browser consumer suite passed 21 scenarios with zero page errors; Ruff under the repository CI rule and strict mypy passed; hosted CI passed. Test-efficiency telemetry recorded 14.32 seconds of tests over 857.87 seconds of task wall time with no forced redundant-green reruns.

## Next action and authority

The owner outcome remains OPEN but execution is BLOCKED_EXTERNAL at model inference. The only same-provider path is to replenish the configured API credit balance. Spending is not authorized in the task and the connected tooling cannot add payment credit on the owner's behalf. A provider switch would also be a material provider/cost boundary and is not inferred from the existing Sol/xhigh authorization.

After credit is added, refresh the existing browser tab and use Retry saved operation. The failed answer is preserved; do not re-enter earlier answers. Natural-use quality evaluation resumes from that changed candidate.

No external recruitment, chart-aware questioning, scientific-validation claim, HumanDesign merge, or public release occurred. The development pull request remains draft/open/unmerged.

**There was never a completion policy.** Preserve state/OWNER-CORRECTION-2026-09-02.md.
## 2026-09-19 owner credit-replenishment recheck

The owner reported that API credit was added. The supervisor immediately re-ran a fresh synthetic owner-session turn, then repeated the check after several minutes. Both calls still returned the hardened provider detail: HTTP 429 / insufficient_quota / credit_balance_exhausted in under two seconds.

Railway read-only diagnostics confirm the running service selects HDMATCH_LLM_API_KEY, calls api.openai.com, and HDMATCH_LLM_API_KEY resolves to the same key value as OPENAI_API_KEY. The application is therefore not accidentally using a different Railway key variable from the one already configured as OPENAI_API_KEY.

OpenAI's current billing guidance states that a purchased prepaid balance can take a few minutes to appear and that any negative balance accumulated after prior credit exhaustion is deducted from the next purchase. Because repeated checks after that propagation window still report credit_balance_exhausted, the remaining action is account-side: verify the positive prepaid balance actually appears for the organization/project associated with this API key and was not fully consumed by a prior negative balance. No additional same-provider runtime repair can create provider credit.

## 2026-09-19 temporary ChatGPT-subscription bridge — live owner-only workaround

The earlier direct OpenAI API credit blocker remains historically accurate, but it is no longer the immediate owner-development blocker. The owner explicitly authorized a temporary subscription-backed workaround.

A Railway Cloud Agent now hosts an authenticated OpenAI-compatible bridge on its port 8080. The deployed `life-patterns-owner` service points `HDMATCH_LLM_API_URL` at that bridge. The bridge invokes Codex with an isolated `CODEX_HOME` carrying ChatGPT authentication, removes the Railway-managed agent-provider variables and `OPENAI_API_KEY` from the inference child environment, loads no MCP/user rules, uses read-only/ephemeral execution, enforces the caller-supplied JSON Schema mechanically, and selects `gpt-5.6-sol` with the caller-requested reasoning effort.

A discriminating Cloud Agent smoke showed direct Codex provider `openai`, model `gpt-5.6-sol`, ChatGPT authentication, and successful schema output. Exact subscription billing metadata is not exposed, so this is authentication evidence rather than an independent billing attestation.

Railway deployment `e2afc5c3-574f-4715-9eb0-52cf24e775de` completed successfully with the bridge URL. A fresh end-to-end owner-session answer operation returned HTTP 200, advanced the session revision from 0 to 1, and returned to `awaiting_answer`. The bridge completed the real xhigh semantic calls; the application logs contained no provider 429, `insufficient_quota`, or `credit_balance_exhausted` for that operation.

The workaround is owner-only and experimental. The Cloud Agent must stay awake for the bridge to run; sleeping stops the process while retaining its files. Do not open this transport to external participants or treat it as reviewed production privacy/inference architecture. Rollback is to restore `HDMATCH_LLM_API_URL=https://api.openai.com/v1/responses` and redeploy; the existing API credential was not replaced.

A tested lifecycle helper is now installed on the owner laptop: `life-patterns-on` wakes the Cloud Agent, starts and health-checks the bridge, and opens the web app; `life-patterns-off` sleeps the agent and stops Cloud Agent compute billing. Zorin application-menu launchers named **Life Patterns ON** and **Life Patterns OFF** are also installed. A full sleep -> wake -> bridge restart -> authenticated schema inference -> sleep cycle passed. Final observed state after verification: Cloud Agent sleeping, bridge stopped.

The owner outcome remains OPEN at product quality rather than provider availability. Next action: resume natural-use interviewing and evaluate actual question quality, recovery behavior, latency, and usefulness. Do not harden this transport further unless natural use demonstrates that it is worth retaining. Exact operational evidence and the non-secret bridge source are preserved under `tasks/life-patterns-subscription-bridge-20260919/`.

## 2026-09-19 owner reverted Life Patterns to direct OpenAI API

The owner found the Cloud-Agent/Codex subscription bridge too slow and explicitly requested a return to direct API inference.

Railway runtime configuration was restored to `HDMATCH_LLM_API_URL=https://api.openai.com/v1/responses`. Deployment `ed975981-30bf-44bc-804b-19b287baa57c` completed successfully. The Cloud Agent remains sleeping and the local ON/OFF launchers/helpers were removed so the obsolete bridge is not accidentally awakened.

A fresh synthetic end-to-end owner-session probe against the restored API route created a session successfully but the semantic operation returned HTTP 503. Railway logs bind the upstream failure to HTTP 429, `insufficient_quota`, `credit_balance_exhausted`, retryable=false. The direct API transport is therefore restored exactly as requested, but model inference remains externally blocked until the OpenAI API balance/key project is funded.

The subscription bridge is superseded as the live route. Its branch artifacts remain historical/recovery evidence only.

