# Life Patterns temporary ChatGPT-subscription bridge

Status: OWNER-AUTHORIZED EXPERIMENTAL WORKAROUND
Date: 2026-09-19
Assurance lane: iteration
Base: `codex/discover-life-patterns-mvp` at `7837d7379b4349c120296d25d0c226373d217b72`

## Owner outcome

Restore the owner-only Life Patterns prototype without requiring additional OpenAI API credit by using the owner's authenticated ChatGPT/Codex entitlement through a Railway Cloud Agent. This is a temporary development workaround, not the intended public inference architecture.

## Live route

```text
life-patterns-owner
  -> HDMATCH_LLM_API_URL
  -> authenticated HTTPS bridge on Railway Cloud Agent port 8080
  -> Codex CLI with isolated ChatGPT auth
  -> GPT-5.6 Sol
```

The running Cloud Agent is `codex-human-46r`. Its public HTTPS endpoint is the current `HDMATCH_LLM_API_URL` for the owner service. No credential value is stored in Git.

The bridge accepts the existing Bearer credential already used by the owner app. It never logs request bodies or authorization headers.

## Provider isolation

The bridge does not use Railway Agent for semantic inference. Each inference runs Codex non-interactively with:

- an isolated `CODEX_HOME` containing only the copied ChatGPT auth file;
- `AI_AGENT_KEY`, `AI_AGENT_GLOBAL_SOCKET`, and `OPENAI_API_KEY` removed from the child environment;
- `--ignore-user-config`, `--ignore-rules`, `--ephemeral`, and `--skip-git-repo-check`;
- read-only sandbox mode;
- no MCP configuration and no web-search flag;
- the exact JSON Schema supplied by the existing OpenAI-compatible caller via `--output-schema`;
- model `gpt-5.6-sol`;
- the caller's requested reasoning effort, including `xhigh`.

A discriminating smoke on the Cloud Agent showed `provider: openai`, model `gpt-5.6-sol`, ChatGPT authentication, and successful schema-constrained output after the Railway-managed `railway_chatgpt` provider variables were removed from the isolated invocation.

Exact subscription/billing-accounting metadata is not exposed by the runtime, so this evidence establishes ChatGPT authentication rather than an independent billing attestation.

## Live evidence

- Cloud Agent public health check: HTTP 200.
- Direct authenticated bridge schema smoke: HTTP 200.
- The owner service redeployed successfully as deployment `e2afc5c3-574f-4715-9eb0-52cf24e775de`.
- A fresh end-to-end owner-session answer operation returned HTTP 200.
- The session revision advanced from 0 to 1 and returned to `awaiting_answer`.
- The bridge completed two real `xhigh` Codex calls for that operation.
- Railway application logs contained no `insufficient_quota`, `credit_balance_exhausted`, or provider 429 for the successful operation.

This is product-development evidence only. It is not scientific-validation evidence.

## Operational limits

- Owner-only development use. Do not open this path to external participants.
- The Cloud Agent must remain awake; Railway bills Cloud Agent compute while it is awake.
- Sleeping the agent stops the bridge process. Files persist. The installed lifecycle helper wakes the agent and restarts the bridge before use.
- Prompt payloads now traverse the Cloud Agent/Codex path rather than the prior direct OpenAI API path. Do not treat this as a reviewed production privacy architecture.
- The bridge is intentionally serialized to one inference at a time.
- No public release, recruitment, scientific claim, or merge to the main research line is authorized by this workaround.

## Installed lifecycle helper

The owner laptop now has a tested command at `~/.local/bin/life-patterns-agent` plus convenience wrappers `life-patterns-on` and `life-patterns-off`.

- `life-patterns-on` wakes the Cloud Agent, waits for `running`, starts the bridge if needed, verifies its public health endpoint, and opens the Life Patterns web app.
- `life-patterns-on --no-open` performs the same wake/start check without opening a browser.
- `life-patterns-off` sleeps the Cloud Agent and waits until it no longer reports `running`, stopping Cloud Agent compute billing.
- `life-patterns-agent status` reports the Cloud Agent state and only probes bridge health when the VM is running.

Two Zorin application-menu launchers were also installed locally: **Life Patterns ON** and **Life Patterns OFF**. The source for the lifecycle helper is preserved next to this integration record as `life-patterns-agent`; the desktop files themselves contain no secrets and remain local-only convenience UI.

The lifecycle was verified end-to-end: running -> sleep -> sleeping, then sleeping -> wake -> bridge restart -> public health ready -> direct authenticated schema inference HTTP 200, then sleep again. The final observed state after verification was `Cloud Agent: sleeping` and `Bridge: stopped`.

## Rollback

Restore:

```text
HDMATCH_LLM_API_URL=https://api.openai.com/v1/responses
```

and redeploy `life-patterns-owner`. The existing API credential was not replaced by this workaround, so rollback does not require reconstructing a secret.

## Next product action

Resume the owner's natural-use Life Patterns interview and evaluate actual question quality, recovery behavior, latency, and usefulness. Do not spend more time hardening this transport unless natural use establishes that the workaround is worth retaining.
