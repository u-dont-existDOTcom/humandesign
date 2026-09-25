# Life Patterns v2 owner real-data browser — Railway deployment receipt — 2026-09-14

Status: **DEPLOYED / OWNER-ONLY PRODUCT JUDGMENT REQUIRED**.

## Owner authorization

The owner explicitly authorized deployment on 2026-09-14 with: `deploy it`.

This authorization applies to this bounded owner-only Life Patterns browser prototype. It does not authorize external participant collection, public recruitment, target-model activity, merge/release, or broader production rollout.

## Source

- Repository: `u-dont-existDOTcom/humandesign`
- Branch: `codex/discover-life-patterns-mvp`
- Real-data browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`
- Deployment-auth wrapper head: `7ef988e313c8ae8d25d2a7c1f40d78fd115e5c5b`
- Auth-wrapper typing fix / verified deployment source head: `bca426b8ab873d02fe5038d271d13b1b814fc813`
- Hosted repository CI on `bca426b8ab873d02fe5038d271d13b1b814fc813`: **success** (`702 passed, 7 expected skips`; Ruff pass; mypy pass)

## Railway deployment

- Project: `humandesign-relationship`
- Environment: `production`
- Service: `life-patterns-owner`
- Service ID: `df2bf91c-7515-4c2e-860f-43c61286a7ab`
- First successful authenticated-wrapper deployment ID: `b932cfb5-cf50-4778-b974-c5c783a83336`
- Deployment status: **SUCCESS**
- Public service domain: `life-patterns-owner-production.up.railway.app`
- Build path: repository `Dockerfile`
- Start app: `hdmatch.api.life_patterns_v2_owner_deployed_app:app`
- Healthcheck: `/healthz`

Deployment logs show application startup completed, Uvicorn bound to Railway's assigned port, and Railway healthcheck returned HTTP `200`.

Subsequent state-only commits on the bound source branch may cause routine Railway redeploys; they do not change the deployed application implementation or authorization boundary.

## Owner-only access control

The public Railway route is protected by HTTP Basic authentication for every path except `/healthz`.

External verification after deployment:

- unauthenticated HTTPS `GET /` -> HTTP `401`
- unauthenticated HTTPS `GET /healthz` -> HTTP `200`

The Basic-auth password is stored only as a Railway service variable and is intentionally not committed to Git. The owner receives the access credential out of band in the supervising chat.

## Model credential handling

`life-patterns-owner` receives `OPENAI_API_KEY` through a Railway service-variable reference to the already configured `relationship-web` credential. The secret value was not copied into Git or exposed in the deployment receipt.

The existing `relationship-web` application source, start command, domain, and running deployment were not repurposed for Life Patterns.

## Product/research boundary

The deployed app remains the bounded v2 owner-development probe:

- owner enters 2–3 real episodes;
- target-theory-blind extraction proposes literal/minimally normalized episode facts;
- owner keeps, edits, or rejects facts;
- tentative cross-episode pattern generation occurs only after two reviewed episodes in this product probe;
- owner adjudication remains authoritative;
- whether wording feels true remains separate from whether the displayed examples support it;
- revised wording known from other situations is not laundered into support from current examples;
- no birth/chart/target-model information enters the loop;
- historical automatic `/map` person-level authority remains unused;
- runtime narratives remain in memory only and are not committed.

The two-reviewed-episode wait is a development-probe choice, not a universal scientific sufficiency threshold.

## Next gate

**OWNER REAL-DATA BROWSER JUDGMENT REQUIRED.**

The owner should use the authenticated browser app with 2–3 real episodes and report whether the fact review, tentative pattern proposal, revision, evidence-source clarification, and final adjudication feel intelligent and natural. Do not scale before that judgment.

**There was never a completion policy.**
