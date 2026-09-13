# Current state

## Life Patterns — 2026-09-13

Active task: `life-patterns-v2-owner-real-data-browser-prototype` — OWNER REAL-DATA BROWSER JUDGMENT REQUIRED.

Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`.

Independent semantic review: **PASS** — zero blockers, `semantic_change_required=false`.

Bounded v2 core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`.

Synthetic HTML owner probe head: `894fc8c237221b51106f81c0e7c276dd27a878fb`.

Real-data owner browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`; hosted repository CI is green on that implementation head.

Core implementation disposition remains **PASS**. The accepted v2 semantics remain unchanged.

### What the owner judgment established

The direct HTML/card/chat surface is the correct interaction direction. The prior terminal/Work relay is not the owner-facing product surface. The owner also identified that two questions must stay separate in ordinary language:

1. whether a revised pattern feels true of the person;
2. whether the particular examples on screen actually support that revised wording.

A revision known from other situations must not be treated as established by the current examples.

### Active bounded experiment

The current task is defined in `tasks/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-PROTOTYPE-2026-09-13.md`.

The new owner-only browser app lives at:

- `src/hdmatch/api/life_patterns_v2_owner_app.py`
- `src/hdmatch/api/life_patterns_v2_owner_ui.py`

It uses the owner's own real episodes, not the synthetic checklist toy. Runtime narratives stay in memory only. A target-theory-blind model extracts literal/minimally normalized facts. The owner reviews those facts. After two reviewed episodes in this bounded product probe, the model may propose at most one cross-episode pattern hypothesis backed by reviewed facts from at least two episodes. The owner alone accepts, revises, rejects, or leaves the pattern unresolved.

The two-reviewed-episode wait is a development-probe design choice, not a universal scientific sufficiency threshold.

The browser app does not import or invoke the historical `OpenAILifePatternsMapper` or `/map` person-level generator. Accepted/rejected/unresolved results pass through the frozen v2 validation/freeze/projection path.

### Current gate

Run the owner-only browser app with **2–3 real episodes** and judge whether the interaction actually feels intelligent and natural. Do not scale the interview architecture before that owner judgment.

Still closed: external participant collection, automated participant coding, target-model activity, public deployment, recruitment/contact, merge/release, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
