# Life Patterns current state — 2026-09-14

V2 independent semantic review: **PASS**.

- Candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
- Blocking semantic findings: `0`
- Semantic change required: `false`
- Adapter-firewall repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`
- Bounded v2 core implementation verified: `true`
- Synthetic HTML owner probe head: `894fc8c237221b51106f81c0e7c276dd27a878fb`
- Real-data owner browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`
- Authenticated deployment-wrapper source head: `bca426b8ab873d02fe5038d271d13b1b814fc813`
- Hosted CI on final deployed source head: `success`
- Active task: `life-patterns-v2-owner-real-data-browser-prototype` — OWNER REAL-DATA BROWSER JUDGMENT REQUIRED

The synthetic HTML probe established that the direct browser/card/chat direction is preferable to a terminal or Work prompt relay. It also exposed a wording/semantic UX requirement: keep separate whether a revised pattern feels true and whether the currently displayed examples actually establish the added wording.

Task: `tasks/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-PROTOTYPE-2026-09-13.md`.

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_app.py`
- `src/hdmatch/api/life_patterns_v2_owner_ui.py`
- `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- `tests/unit/test_life_patterns_v2_owner_app.py`

The owner-only app accepts real episode narratives, uses a target-theory-blind model for literal/minimally normalized fact extraction, requires owner fact review, and may propose one tentative cross-episode pattern only from reviewed operative facts. Owner adjudication remains authoritative. Revised wording attributed to other situations is not laundered into support from the current examples.

The two-reviewed-episode wait is a bounded product-probe choice, not a universal sufficiency threshold.

Historical automatic person-level map generation remains superseded and is not invoked by the new app. The accepted v2 semantic contract remains unchanged.

## Owner-authorized deployed surface

The owner explicitly authorized an owner-only Railway deployment on 2026-09-14.

Deployment receipt: `state/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-RAILWAY-DEPLOYMENT-2026-09-14.md`.

- Railway service: `life-patterns-owner`
- Domain: `life-patterns-owner-production.up.railway.app`
- Deployment ID: `b932cfb5-cf50-4778-b974-c5c783a83336`
- Deployment status: **SUCCESS**
- Public healthcheck `/healthz`: HTTP `200`
- Owner-facing `/` without credentials: HTTP `401`
- Owner-facing paths are HTTP-Basic protected; password is not committed to Git
- Model credential is supplied through Railway service-variable reference rather than copied into repository state

This authorization is limited to the owner-only authenticated development surface. External/public participant deployment remains closed.

Authorized: bounded owner-only real-data browser testing, owner-initiated runtime model use, and the already executed owner-only authenticated Railway deployment.

Still closed: external participant collection, automated participant coding, downstream target-model activity, external/public participant deployment, recruitment/contact, merge/release, and unapproved spending.

Next gate: **OWNER REAL-DATA BROWSER JUDGMENT** after 2–3 real episodes.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
