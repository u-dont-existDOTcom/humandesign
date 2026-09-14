# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-hidden-ledger-conversational-insight-probe` — **OWNER CONVERSATIONAL INSIGHT JUDGMENT IN PROGRESS / PRELIMINARY POSITIVE**.

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

The owner-only service now uses a direct provider Responses path with the existing Railway credential reference. It performs up to three bounded attempts for transient server/network failures and preserves transactional rollback.

GitHub Actions run `34857710301` on regression head `b52be2a67e458c5d1334d058d7b73e938c04d1ef`: **SUCCESS**.

Owner-only Railway deployment:

- domain: `life-patterns-owner-production.up.railway.app`
- service: `life-patterns-owner`
- deployment ID: `feba6ba2-9677-4f94-b0b8-1cf0e6d530fe`
- runtime source head: `8d74d4b89bff1e78922af524dcb5b95f271d9b97`
- status: **SUCCESS**
- Railway health request: `GET /healthz` -> HTTP `200`.

## Direct owner outcome evidence after repair

The owner then ran a fresh live session after the provider repair.

Result:

- the live model-backed turn succeeded;
- direct owner judgment of that turn was positive: **good**.

This is the first direct positive owner-facing evidence for the repaired pattern-first + hidden-ledger strategy. The previous `not yet measured` status is therefore superseded by **PRELIMINARY POSITIVE**.

Receipt:

`state/LIFE-PATTERNS-v2-OWNER-PATTERN-FIRST-PRELIMINARY-POSITIVE-2026-09-14.md`

One good turn does not establish that the complete interview strategy is successful. The remaining product question is whether the session continues to produce information gain—useful context/scope distinctions, developmental change, counterexamples, contrasts, or synthesis—without collapsing back into paraphrase or exposing evidence bookkeeping.

## Current outcome / next gate

Continue the same bounded owner-only session naturally. The next decision-changing evidence is later-turn quality, especially the first deeper discriminating move and, if reached naturally, a cross-situation synthesis / boundary check.

If later turns remain good and produce genuine information gain, the interaction strategy can advance beyond this probe. If it degrades into paraphrase/confirmation, classify that failure rather than polishing around it.

Authorized: bounded owner-only testing of the deployed probe and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
