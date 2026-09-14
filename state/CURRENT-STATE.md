# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-owner-real-data-browser-prototype` — OWNER REAL-DATA BROWSER JUDGMENT REQUIRED.

Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`.

Independent semantic review: **PASS** — zero blockers, `semantic_change_required=false`.

Bounded v2 core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`.

Synthetic HTML owner probe head: `894fc8c237221b51106f81c0e7c276dd27a878fb`.

Real-data owner browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`; hosted repository CI is green on that implementation head.

Authenticated deployment wrapper final source head: `bca426b8ab873d02fe5038d271d13b1b814fc813`; hosted repository CI is green on that head.

Core implementation disposition remains **PASS**. The accepted v2 semantics remain unchanged.

### What the owner judgment established

The direct HTML/card/chat surface is the correct interaction direction. The prior terminal/Work relay is not the owner-facing product surface. The owner also identified that two questions must stay separate in ordinary language:

1. whether a revised pattern feels true of the person;
2. whether the particular examples on screen actually support that revised wording.

A revision known from other situations must not be treated as established by the current examples.

### Active bounded experiment

The current task is defined in `tasks/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-PROTOTYPE-2026-09-13.md`.

The owner-only browser app lives at:

- `src/hdmatch/api/life_patterns_v2_owner_app.py`
- `src/hdmatch/api/life_patterns_v2_owner_ui.py`
- deployed access wrapper: `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`

The app uses the owner's own real episodes. Runtime narratives stay in memory only. A target-theory-blind model extracts literal/minimally normalized facts. The owner reviews those facts. After two reviewed episodes in this bounded product probe, the model may propose at most one cross-episode pattern hypothesis backed by reviewed facts from at least two episodes. The owner alone accepts, revises, rejects, or leaves the pattern unresolved.

The two-reviewed-episode wait is a development-probe design choice, not a universal scientific sufficiency threshold.

The browser app does not import or invoke the historical `OpenAILifePatternsMapper` or `/map` person-level generator. Accepted/rejected/unresolved results pass through the frozen v2 validation/freeze/projection path.

Focused completion command:

`python -m pytest tests/unit/test_life_patterns_v2_owner_app.py tests/unit/test_participant_adjudicated_v2.py -q`

### Owner-authorized Railway deployment

The owner explicitly authorized this bounded owner-only deployment on 2026-09-14.

Deployment receipt: `state/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-RAILWAY-DEPLOYMENT-2026-09-14.md`.

- Railway service: `life-patterns-owner`
- Service domain: `life-patterns-owner-production.up.railway.app`
- First authenticated-wrapper deployment `b932cfb5-cf50-4778-b974-c5c783a83336`: **SUCCESS**
- `/healthz`: HTTP `200`
- unauthenticated `/`: HTTP `401`
- all owner-facing paths are protected by HTTP Basic authentication
- model credential is supplied by a Railway reference to the existing configured service credential; no secret value is committed to Git
- the existing `relationship-web` application source/start/domain/running deployment were not repurposed

Subsequent state-only branch commits may trigger routine Railway redeploys but do not change the implemented browser semantics or authorization boundary.

This one owner-only authenticated deployment is authorized and executed. It does **not** authorize external/public participant deployment or broader production rollout.

### Current gate

Use the authenticated owner browser app with **2–3 real episodes** and judge whether the interaction actually feels intelligent and natural. Do not scale the interview architecture before that owner judgment.

Still closed: external participant collection, automated participant coding, target-model activity, external/public participant deployment, recruitment/contact, merge/release, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
