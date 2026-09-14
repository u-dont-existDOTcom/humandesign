# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-hidden-ledger-conversational-insight-probe` — **OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED**.

Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`.

Independent semantic review: **PASS** — zero blockers, `semantic_change_required=false`.

Bounded v2 core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`.

## Product-layer history

The first real-data owner browser exposed the internal evidence ledger as fact/paraphrase review. Direct owner testing established that this was low-value as a product experience: correct comprehension was being demonstrated rather than useful self-understanding being produced.

That surfaced coding/paraphrase method is **FAILED / REPLACED**. The accepted v2 evidence semantics remain authoritative and internal.

The subsequent hidden-ledger conversational probe correctly hid routine coding work, but owner testing exposed two additional defects before product-value judgment could proceed:

1. the live model could return a non-hypothesis move carrying hypothesis-only fields, causing strict `ConversationMove` validation to fail;
2. the opening had regressed from the earlier pattern-first interview design back to arbitrary episode-first elicitation.

The old failed turn path could also mutate hidden session state before planner failure.

Continuity finding: `state/LIFE-PATTERNS-INTERACTIVE-INTERVIEW-CONTINUITY-FINDING-2026-09-14.md`.

## Current repaired architecture

The current owner-facing method combines the earlier pattern-first interaction strategy with the accepted v2 hidden evidence substrate:

`participant-reported pattern -> minimal concrete anchor(s) / contrasts / life-phase evidence -> hidden v2 evidence ledger -> discriminating follow-up / boundary check -> informative synthesis -> participant authority -> immutable freeze`

The participant begins from a recurring, changing, context-dependent, or puzzling pattern in their own words. The initial general pattern statement is conversational context only; it does **not** fabricate an episode, fact, or provenance record. A later real situation can become the first episode anchor.

Concrete situations are evidence anchors and falsification/contrast material, not the product objective. Historical v8 domains may remain optional coverage scaffolding; they are not restored as a closed taxonomy. The accepted v2 open-world architecture remains authoritative.

Pattern-first runtime repair implementation receipt:

`state/LIFE-PATTERNS-v2-PATTERN-FIRST-RUNTIME-REPAIR-IMPLEMENTATION-2026-09-14.md`

Exact verified/deployed repair source head:

`67b038b27d62b941b6beb224c6e89efd0d165bb4`

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_pattern_first.py`
- hidden-ledger base: `src/hdmatch/api/life_patterns_v2_owner_conversation.py`
- owner UI: `src/hdmatch/api/life_patterns_v2_owner_conversation_ui.py`
- authenticated entrypoint: `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- regressions: `tests/unit/test_life_patterns_v2_owner_pattern_first.py`

The provider boundary normalizes hypothesis-only fields away from non-hypothesis moves before strict validation, while true `surface_hypothesis` moves remain strict. Model-driven turns are transactional: extraction/planning/validation/post-processing failure restores pre-turn conversation, hidden record, flags, and proposal state.

## Verification and deployment

GitHub Actions run `34854800932` on exact source head `67b038b27d62b941b6beb224c6e89efd0d165bb4`: **SUCCESS**.

- unit/integration tests: passed;
- Ruff: passed;
- strict mypy: passed.

Owner-only Railway deployment:

- domain: `life-patterns-owner-production.up.railway.app`
- service: `life-patterns-owner`
- deployment ID: `842b13f2-66b2-435e-a918-dbc81cde00e7`
- source head: `67b038b27d62b941b6beb224c6e89efd0d165bb4`
- status: **SUCCESS**
- runtime: application startup complete;
- Railway health request: `GET /healthz` -> HTTP `200`.

Existing Basic authentication and runtime credential references remain unchanged. No new Railway service was created.

## Current outcome / next gate

Direct owner-facing information-gain evidence for the repaired pattern-first surface: **NOT YET MEASURED**.

Next gate: start a **fresh owner-only browser session** and judge the conversation naturally. Success requires useful information beyond paraphrase: a meaningful context distinction, life-phase change, counterexample, boundary, contrast, or synthesis that the participant did not simply state verbatim.

If the repaired experience remains essentially an elaborate parrot, classify the interaction strategy as failed rather than cosmetically polishing it.

Authorized: bounded owner-only testing of the deployed probe and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
