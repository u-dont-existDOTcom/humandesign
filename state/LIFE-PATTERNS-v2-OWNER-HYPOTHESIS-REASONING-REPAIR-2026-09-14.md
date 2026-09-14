# Life Patterns v2 owner hypothesis-reasoning repair — 2026-09-14

Status: **IMPLEMENTED / VERIFIED / DEPLOYED — OWNER RETEST REQUIRED**.

## Direct owner finding

A live owner pattern thread produced a plausible-sounding tentative synthesis that materially overreached the evidence. The owner correctly identified that repairing the terminal `No` behavior was insufficient: participants should not have to diagnose and explain an obvious reasoning error after the product has already surfaced it.

No private interview narrative is persisted in this receipt.

## Causal mechanism

The failure was produced by two coupled conditions in the interviewer controller:

1. A reply to a pending boundary/counterexample question automatically set `boundary_answered=true`, regardless of whether the reply actually supplied the requested counterexample or discriminating contrast.
2. Once that flag was true, the planner was explicitly encouraged to produce a nontrivial synthesis with explanatory compression, but the synthesis contract did not explicitly prohibit unsupported comparative weighting, cross-context projection, construct conflation, circular abstractions, or strengthened scope/quantifiers.

That combination allowed an answer that merely introduced another possible contributing factor to unlock a synthesis that ranked factors against one another without comparative evidence. It also allowed a factor observed in one context to be compressed across another context without direct support.

The rejected-synthesis continuation then still placed unnecessary diagnostic burden on the participant by asking them to explain what the synthesis got wrong, even when the unsupported leap was visible from the record.

## Repair

The owner-only product now inserts a reasoning guard before any tentative synthesis reaches the participant.

### Primary interviewer discipline

The planner is explicitly instructed that:

- an additional reported factor is additive unless evidence actually compares its importance with another factor;
- `more`, `less`, `mainly`, `primarily`, or `rather than` claims require direct discriminating support;
- a factor from one context may not be projected into another context without support;
- distinct reported outcomes remain distinct unless the participant links them;
- umbrella labels may not merely rename the phenomenon being explained;
- a reply that merely introduces another factor does not automatically resolve a requested boundary/counterexample;
- after participant disagreement, the model should identify the weakest unsupported inference itself and ask the narrowest useful question instead of defaulting to `what did I get wrong?`.

### Hidden pre-surface hypothesis audit

Every proposed `surface_hypothesis` now receives a second target-theory-blind support audit before display. The audit can reject the candidate for:

- unsupported comparison;
- unsupported causal weighting;
- cross-context projection;
- construct conflation;
- circular abstraction;
- unresolved boundary/counterexample;
- quantifier/scope strengthening;
- another unsupported inference.

A failed audit suppresses the synthesis and converts the move into one targeted discriminating follow-up question. A supported synthesis passes through unchanged.

### Rejected-synthesis reasoning recovery

`No — keep investigating` now invokes the reasoning planner on the existing evidence/conversation instead of returning a canned request for the participant to diagnose the failure. The same pattern inquiry remains live.

## Scientific / privacy boundary

This is a product-reasoning repair, not a change to the accepted v2 evidence semantics. Preproposal versus post-proposal provenance, participant authority, target-theory blindness, and the episode-fact/person-pattern firewall remain unchanged. No astrology/target hints, broader access, transcript persistence, or request-body logging were added.

## Verification / deployment

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`;
- `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py` now routes the authenticated owner surface through the reasoning-guarded app;
- `tests/unit/test_life_patterns_v2_owner_reasoning.py` contains focused regressions for unsupported-comparison interception, supported-synthesis pass-through, and model-led recovery after participant disagreement.

Exact final code/test head: `6a836b68b929f4e11eabcf8602bc2f6b23386b62`.

GitHub Actions run `34878158579`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

Existing owner-only Railway service reused; no new service and no access broadening.

- service: `life-patterns-owner`;
- deployment: `bfab11be-16c6-4c78-8931-70ba9ae502d7`;
- application source head: `b8bc552d0c02370ace4f942db95f1616bb2d4234`;
- status: **SUCCESS**;
- application startup complete;
- Railway `/healthz`: HTTP `200`;
- health contract includes `hypothesis_support_audit=true` and `rejection_reasoning_recovery=true`.

Later test/state-only commits are outside the Railway application watch surface.

## Next decision-changing evidence

Owner retest should now focus on reasoning quality rather than merely liveness:

1. Does the interviewer refrain from turning an additional factor into an unsupported relative-weight claim?
2. Does it avoid transferring factors across contexts or merging distinct outcomes without evidence?
3. When the evidence does not yet discriminate the possibilities, does it ask the useful missing question rather than manufacture a clever synthesis?
4. If the owner still rejects a synthesis, does the interviewer diagnose the likely unsupported inference itself rather than making the owner restate the obvious problem?
5. After a satisfactory thread, is `Finish for now` useful enough to justify durable persistence / a real Life Patterns Map?

**There was never a completion policy.**
