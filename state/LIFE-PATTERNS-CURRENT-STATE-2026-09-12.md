# Life Patterns current state — 2026-09-13

V2 independent semantic review: **PASS**.

- Candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
- Blocking semantic findings: `0`
- Semantic change required: `false`
- Adapter-firewall repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`
- Bounded v2 core implementation verified: `true`
- Synthetic HTML owner probe head: `894fc8c237221b51106f81c0e7c276dd27a878fb`
- Real-data owner browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`
- Hosted CI on real-data implementation head: `success`
- Active task: `life-patterns-v2-owner-real-data-browser-prototype` — OWNER REAL-DATA BROWSER JUDGMENT REQUIRED

The synthetic HTML probe established that the direct browser/card/chat direction is preferable to a terminal or Work prompt relay. It also exposed a wording/semantic UX requirement: keep separate whether a revised pattern feels true and whether the currently displayed examples actually establish the added wording.

Task: `tasks/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-PROTOTYPE-2026-09-13.md`.

Work launcher: `tasks/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-WORK-RUNNER-2026-09-13.md`. Work may prepare the environment and launch the local browser, but it must not act as a prompt courier; the owner interacts with the web UI directly.

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_app.py`
- `src/hdmatch/api/life_patterns_v2_owner_ui.py`
- `tests/unit/test_life_patterns_v2_owner_app.py`

The owner-only app accepts real episode narratives, uses a target-theory-blind model for literal/minimally normalized fact extraction, requires owner fact review, and may propose one tentative cross-episode pattern only from reviewed operative facts. Owner adjudication remains authoritative. Revised wording attributed to other situations is not laundered into support from the current examples.

The two-reviewed-episode wait is a bounded product-probe choice, not a universal sufficiency threshold.

Historical automatic person-level map generation remains superseded and is not invoked by the new app. The accepted v2 semantic contract remains unchanged.

Authorized: bounded owner-only real-data browser testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, downstream target-model activity, public deployment, recruitment/contact, merge/release, and unapproved spending.

Next gate: **OWNER REAL-DATA BROWSER JUDGMENT** after 2–3 real episodes.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
