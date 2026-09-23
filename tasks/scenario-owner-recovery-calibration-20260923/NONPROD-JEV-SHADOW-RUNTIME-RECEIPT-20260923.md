# Non-production Mission Control Jev-shadow runtime receipt — 2026-09-23

`NON_UNIVERSAL / EXAMPLE_OWNER_DEPLOYMENT`

Status: **ACTIVE / VERIFIED**. Production was not touched. No credential value is stored in Git.

## Requested runtime change

The existing non-production central Mission Control runtime was restarted with the existing owner OpenRouter credential and:

- `MISSION_CONTROL_JEV_SHADOW_ENABLED=1`
- `MISSION_CONTROL_JEV_SHADOW_MODEL=typesafe/jev-1.13`
- `MISSION_CONTROL_JEV_SHADOW_TIMEOUT_MS=1500`
- `OPENROUTER_API_KEY` present server-side from the existing private owner credential

The deployed source already contained `lib/jev-shadow.ts`, `open_blocker_present`, and the corrected ordered `next_action` policy before activation.

## Runtime preservation

- live logical container: `mission-control-issue90-live`
- image unchanged: `codex-mission-control:55769b-rdc-recovery`
- host networking preserved
- durable volume preserved: `codex-mission-control-issue90-live-v2` mounted at `/data` read/write
- source release bind preserved read-only
- capability-publisher socket bind preserved read-only
- stopped rollback preserved: `mission-control-issue90-live-pre-jev-shadow-20260923T161804Z`
- temporary credential staging files removed after restart

## Verification

Credential preflight: OpenRouter `/api/v1/models` returned HTTP **200** without exposing the credential.

Runtime after restart:

- Docker health: **healthy**
- daemon `/live`: HTTP 200, `status=ok`, `kind=liveness`
- daemon `/health`: HTTP 200, `status=ok`, `kind=readiness`
- event chain: `valid=true`
- submission-authority ledger: `valid=true`
- submission-authority scheduler: `ACTIVE_LEASE`
- BFF `/api/live`: HTTP 200, `status=ok`, `kind=liveness`

Real Jev observations after restart:

- `status=OK`
- `authoritative=false`
- `model=typesafe/jev-1.13`
- provider reported as `TypeSafe`
- deterministic trigger remained `HEALTHY_ADVANCING`
- repeated shadow `next_action` result: `no_action_healthy`

This verifies that Jev is running as a shadow/evaluation observer rather than an authority path.

## Non-blocking observation

One startup GitHub-supervision reconciliation attempt timed out after about 32 seconds. The daemon then remained healthy, readiness/event-chain/submission-authority checks were valid, and multiple successful Jev shadow observations followed. No Jev activation failure was observed.
