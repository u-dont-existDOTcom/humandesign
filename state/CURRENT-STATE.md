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

The repaired pattern-first + hidden-ledger strategy therefore has **PRELIMINARY POSITIVE** direct product evidence at the one-pattern level.

Receipts:

- `state/LIFE-PATTERNS-v2-OWNER-PATTERN-FIRST-PRELIMINARY-POSITIVE-2026-09-14.md`
- `state/LIFE-PATTERNS-v2-OWNER-PATTERN-FIRST-BOUNDED-SESSION-PASS-2026-09-14.md`

## Multi-pattern continuation frontier

The post-pattern dead end was repaired without changing accepted v2 semantics.

Continuation implementation head: `da3c5f58101d8cc10421e480d44b5162bd12ec78`.

Owner-facing behavior provides:

- `Explore another pattern`;
- `Finish for now`;
- a fresh backend conversation session for each new pattern thread;
- browser-page-local accumulation of completed pattern results and visible interview text;
- a compact finish-for-now summary with no completeness claim;
- owner-triggered client-side copy/export.

The server still keeps narrative/session state in process memory. The continuation adds no Git persistence, Railway volume persistence, private transcript logging, or automatic supervisor transcript ingestion.

Verification:

- focused task command covered `16` tests across the owner conversation and pattern-first suites;
- hosted GitHub Actions run `34864954177`: **SUCCESS**;
- the `verify` job passed unit/integration tests, Ruff, and strict mypy.

Existing owner-only Railway service reused; no new service was created and access was not broadened. Deployment `4ed43b5a-7249-4cc3-ad2e-1e1401ea0788` from source head `da3c5f58101d8cc10421e480d44b5162bd12ec78` succeeded and `/healthz` returned HTTP `200`.

## Repeated-thread unresolved-continuation finding and repair

Direct owner testing of a second fresh pattern thread produced **mixed but still positive** product evidence. The conversation was still generating useful discriminating information after the first tentative synthesis, but the UI converted uncertainty into a terminal `unresolved` adjudication rather than allowing the owner to continue working on the same pattern.

This is classified as a **workflow-liveness / adjudication-frontier defect**, not a failure of the pattern-first interaction strategy.

Repair receipt:

`state/LIFE-PATTERNS-v2-OWNER-UNRESOLVED-CONTINUATION-REPAIR-2026-09-14.md`

The repaired owner surface now distinguishes:

- `Keep trying to pin it down` — continue the same backend pattern session with another discriminating question;
- `Leave it unresolved for now` — explicitly end the thread unresolved;
- existing accept / revise / reject participant-authoritative judgments.

Post-proposal answers may add episode facts in the same thread, but they remain post-proposal evidence. The continuation path does not silently write an unresolved adjudication and does not automatically manufacture a replacement person-level proposal from post-proposal material. If the final wording changes, the existing explicit participant revision/adjudication route remains authoritative.

The participant-facing consequence copy is deliberately target-neutral: an unresolved thread contributes no settled person-level pattern to later analysis. Predictive-power or astrological-fit language is not exposed before behavioral lock because target-theory blindness remains binding and predictive performance has not been established.

Exact final verified code/test head:

`21d6a4addfd5549ef2d81ce694e8e127bd3eecce`

Hosted GitHub Actions run `34872101510`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

The first hosted run of the new regression had failed during test collection because Starlette `TestClient` required an uninstalled `httpx2` dependency. No product assertion ran. The unnecessary test dependency was removed rather than changing project dependencies; the registered FastAPI endpoint/session boundary is now exercised directly.

Current owner-only Railway deployment:

- service: `life-patterns-owner`;
- deployment ID: `a1aa5bdf-82f9-4e71-b7c9-9268eecea894`;
- application source head: `0d2aac5d65076f3ccc03e330c6696807ad5a7661`;
- status: **SUCCESS**;
- application startup complete;
- Railway healthcheck and runtime `/healthz`: HTTP `200`;
- deployed code declares `unresolved_thread_continuation=true` in the health response;
- later test/state-only commits are outside the Railway application watch surface.

Privacy boundary is unchanged: no automatic transcript persistence or request-body logging was added.

## Current outcome / next gate

Outcome advancement: **PRELIMINARY POSITIVE WITH A REPEATED-THREAD LIVENESS DEFECT FOUND AND REPAIRED**.

Strategy efficacy: **VIABLE; OWNER RETEST REQUIRED**.

Next gate: **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

1. On a pattern that remains uncertain after a first synthesis, choose `Keep trying to pin it down` and judge whether the interviewer actually continues the same thought with useful discriminating questions rather than forcing closure or starting over.
2. Then explicitly accept/revise/reject/leave unresolved.
3. Use `Finish for now` and judge whether the session-level summary is useful enough to justify durable persistence and development of a real Life Patterns Map.

Owner-triggered copy/export remains available if the owner chooses to share browser-local output. Automatic transcript logging remains out of scope.

Authorized: bounded owner-only testing of the deployed probe and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

Focused completion command: `python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_pattern_first.py tests/unit/test_life_patterns_v2_owner_refinement.py -q`

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
