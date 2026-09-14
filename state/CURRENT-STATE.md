# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-owner-multi-pattern-continuation` — **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`.

Independent semantic review: **PASS** — zero blockers, `semantic_change_required=false`.

Bounded v2 core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`.

## Product-layer history

The first real-data owner browser exposed the internal evidence ledger as fact/paraphrase review. Direct owner testing established that this was low-value as a product experience. That surfaced coding/paraphrase method is **FAILED / REPLACED**; the accepted v2 evidence semantics remain authoritative and internal.

The first hidden-ledger conversational probe then exposed a strict structured-output failure and an interaction regression back to arbitrary episode-first elicitation. Those were repaired by restoring the earlier pattern-first interaction strategy while keeping the v2 ledger hidden and making model-driven turns transactional.

The current owner-facing architecture is:

`participant-reported pattern -> minimal concrete anchor(s) / contrasts / life-phase evidence -> hidden v2 evidence ledger -> discriminating follow-up / boundary check -> informative synthesis -> participant authority -> immutable freeze`

Pattern-first repair receipt:

`state/LIFE-PATTERNS-v2-PATTERN-FIRST-RUNTIME-REPAIR-IMPLEMENTATION-2026-09-14.md`

## Provider 520 incident and repair

The first natural model-backed anchor turn on the repaired app exposed a separate upstream provider HTTP 520 failure. Railway showed the initial pattern turn returning HTTP 200 and the first concrete-anchor turn returning application HTTP 422 after the inner provider 520. This was a provider transport/gateway failure, not invalid participant input.

The transactional session wrapper restored pre-turn state on the exception, so the failed turn was not admitted as hidden evidence.

Provider repair receipt:

`state/LIFE-PATTERNS-v2-PROVIDER-520-REPAIR-2026-09-14.md`

Runtime repair head:

`8d74d4b89bff1e78922af524dcb5b95f271d9b97`

Regression-test head:

`b52be2a67e458c5d1334d058d7b73e938c04d1ef`

The owner-only service uses a direct provider Responses path with the existing Railway credential reference. It performs up to three bounded attempts for transient server/network failures and preserves transactional rollback.

GitHub Actions run `34857710301` on regression head `b52be2a67e458c5d1334d058d7b73e938c04d1ef`: **SUCCESS**.

## Direct owner outcome evidence after repair

The owner then ran a fresh live session after the provider repair and completed the full bounded pattern-first thread through a nontrivial synthesis and explicit adjudication.

Result:

- the live model-backed interview succeeded;
- the interviewer tested the initial generalization with contrast/counterexample material and narrowed the synthesis conditionally rather than merely parroting the owner;
- direct owner judgment of the bounded strategy: **GOOD / PASS**.

The repaired pattern-first + hidden-ledger strategy therefore has **PRELIMINARY POSITIVE** direct product evidence at the one-pattern level. This does not yet establish that repeated pattern threads remain useful or that a session-level summary deserves durable persistence.

Receipts:

- `state/LIFE-PATTERNS-v2-OWNER-PATTERN-FIRST-PRELIMINARY-POSITIVE-2026-09-14.md`
- `state/LIFE-PATTERNS-v2-OWNER-PATTERN-FIRST-BOUNDED-SESSION-PASS-2026-09-14.md`

## Multi-pattern continuation frontier

The post-pattern dead end is repaired without changing accepted v2 semantics.

Continuation implementation head: `da3c5f58101d8cc10421e480d44b5162bd12ec78`.

Owner-facing behavior now provides:

- `Explore another pattern`;
- `Finish for now`;
- a fresh backend conversation session for each new pattern thread;
- browser-page-local accumulation of completed pattern results and visible interview text;
- a compact finish-for-now summary with no completeness claim;
- owner-triggered client-side copy/export.

The server still keeps narrative/session state in process memory. The continuation adds no Git persistence, Railway volume persistence, private transcript logging, or automatic supervisor transcript ingestion. Railway deploy/HTTP logs inspected for the active deployment contain startup/health/request metadata, not private request bodies.

Verification:

- focused task command covers `16` tests across `tests/unit/test_life_patterns_v2_owner_conversation.py` and `tests/unit/test_life_patterns_v2_owner_pattern_first.py`;
- hosted GitHub Actions run `34864954177` on branch head `713582a7e3a1c9dd3f1bdd00c32e3075a3665feb`: **SUCCESS**;
- the `verify` job passed unit/integration tests, Ruff, and strict mypy.

Existing owner-only Railway service reused; no new service was created and access was not broadened.

Current Railway deployment:

- service: `life-patterns-owner`;
- deployment ID: `4ed43b5a-7249-4cc3-ad2e-1e1401ea0788`;
- runtime source head: `da3c5f58101d8cc10421e480d44b5162bd12ec78`;
- status: **SUCCESS**;
- Railway `/healthz` request: HTTP `200`;
- owner-facing routes remain HTTP-Basic protected;
- runtime model credentials remain Railway variable references rather than repository secrets.

The later state-only commit `713582a7e3a1c9dd3f1bdd00c32e3075a3665feb` was correctly skipped by Railway because the service watch patterns do not include state/task files; deployed application bytes therefore remain the verified continuation code head above.

## Current outcome / next gate

Outcome advancement: **PRELIMINARY POSITIVE** at the bounded one-pattern strategy level.

Strategy efficacy: **VIABLE, PENDING MULTI-PATTERN OWNER JUDGMENT**.

Next gate: **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**. In the deployed owner-only service, complete at least another pattern thread and use `Finish for now`. The decision-changing questions are:

1. Do repeated fresh pattern threads remain useful rather than becoming repetitive/paraphrastic?
2. Is the session-level summary useful enough to justify durable persistence and development of a real Life Patterns Map?

Owner-triggered copy/export is available if the owner chooses to share the browser-local session with the supervisor. Automatic transcript logging remains out of scope.

Authorized: bounded owner-only testing of the deployed probe and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

Focused completion command: `python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_pattern_first.py -q`

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
