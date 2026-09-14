# Life Patterns v2 pattern-first runtime repair — implementation receipt — 2026-09-14

Status: **IMPLEMENTED, VERIFIED, AND DEPLOYED OWNER-ONLY; OWNER PRODUCT JUDGMENT PENDING**.

## Owner outcome restored

The participant-facing interaction is again pattern-first rather than coding-first or arbitrary-episode-first. The owner begins with a recurring, changing, context-dependent, or puzzling pattern in their own words. Concrete situations are then requested as evidence anchors and falsification/contrast material while the accepted v2 evidence ledger stays hidden.

The coding/measurement layer remains infrastructure, not the participant product.

## Exact implementation

Exact verified code head:

`67b038b27d62b941b6beb224c6e89efd0d165bb4`

New repair layer:

`src/hdmatch/api/life_patterns_v2_owner_pattern_first.py`

Deployment wrapper:

`src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`

Regression tests:

`tests/unit/test_life_patterns_v2_owner_pattern_first.py`

The existing accepted hidden-ledger conversation and v2 core remain underneath this layer.

## Repairs

### 1. Structured-output normalization

The owner-visible failure was caused by a provider response that selected a non-hypothesis move while also populating hypothesis-only fields. The new provider boundary explicitly normalizes `hypothesis_proposition` to `null` and `evidence_fact_ids` to an empty list for `follow_up`, `request_contrast`, and `boundary_question` before strict `ConversationMove` validation.

The strict invariant is retained: a real `surface_hypothesis` still requires a nonempty proposition and evidence IDs. Invalid surface hypotheses are not silently downgraded.

### 2. Transactional participant turns

The pattern-first session snapshots conversation, v2 record, episode/boundary flags, proposal support, pending episode state, and active proposal state before a model-driven turn. If extraction, planning, validation, or post-processing raises, pre-turn state is restored.

A failed turn therefore no longer leaves duplicate-able hidden facts, provenance, episode state, or conversation messages behind.

### 3. Pattern-first opening without evidence laundering

The first participant pattern statement is retained only as conversational context. It does **not** create an `EpisodeV2`, episode fact, or source-provenance record merely to satisfy the ledger.

The interviewer then asks for one representative real situation. That subsequent concrete situation can become the first episode anchor under the existing v2 evidence rules.

This preserves the earlier v8 interaction insight without restoring v8 as a closed fixed taxonomy. The accepted v2 open-world architecture remains authoritative.

## Verification

GitHub Actions run `34854800932` on exact head `67b038b27d62b941b6beb224c6e89efd0d165bb4`: **SUCCESS**.

The verify job passed:

- full unit/integration suite;
- Ruff;
- strict mypy.

The immediately preceding candidate also demonstrated that the full suite passed `715 passed, 7 skipped`; its only failure was one unused import, subsequently removed at the exact green head above.

The added regressions cover:

- the exact non-hypothesis/hypothesis-field overpopulation failure shape;
- preservation of strict `surface_hypothesis` validation;
- no fabricated episode/fact/provenance for the initial pattern claim;
- second turn becoming the first concrete anchor;
- rollback after a planner failure that occurs after extraction.

## Owner-only Railway deployment

Existing service only; no new service was created and access was not broadened.

- service: `life-patterns-owner`
- domain: `life-patterns-owner-production.up.railway.app`
- deployment: `842b13f2-66b2-435e-a918-dbc81cde00e7`
- source head: `67b038b27d62b941b6beb224c6e89efd0d165bb4`
- status: **SUCCESS**
- runtime log: application startup complete
- Railway health request: `GET /healthz` -> HTTP `200`

Authentication and existing runtime credential references were not changed.

The live authenticated interview turn has **not** been replayed by Chat after deployment because doing so would require owner credentials. The exact prior failure shape is covered at the provider/validator seam by the new regression test, and Railway confirms the repaired source is running and healthy. Owner natural use is therefore still the next live consumer-seam/product check.

## Scientific / product boundary

`semantic_change_required=false`.

Preserved:

- target-theory blindness;
- accepted v2 open-world episode facts;
- append-only successful corrections/provenance;
- genuine-absence gating;
- immutable first-proposal evidence timing;
- participant authority over person-level pattern claims;
- no automatic reconstruction of person-level recurrence from episode facts;
- no historical `/map` authority.

Still unauthorized:

- external participant collection;
- automated participant coding;
- target-model scoring/reveal or downstream target-model activity;
- recruitment/contact;
- merge/release;
- broader public deployment;
- unapproved spending.

## Next gate

**OWNER CONVERSATIONAL INSIGHT JUDGMENT.** Start a fresh owner-only browser session and use the repaired pattern-first interview naturally. The success criterion is not technical correctness or fluent paraphrase. It is whether the interviewer produces at least one useful distinction, context boundary, developmental change, counterexample, contrast, or synthesis that adds information beyond what the owner simply handed it.

If it still behaves mainly as an elaborate parrot, classify the interaction strategy as failed rather than polishing the surface.
