# Life Patterns v2 owner hypothesis-reasoning repair — 2026-09-14

Status: **IMPLEMENTED / VERIFIED / DEPLOYED — OWNER RETEST REQUIRED**.

## Direct owner finding

A live owner pattern thread produced a plausible-sounding tentative synthesis that materially overreached the evidence. The owner correctly identified that repairing terminal `No` behavior was insufficient: participants should not have to diagnose and explain an obvious reasoning error after the product has already surfaced it.

No private interview narrative is persisted in this receipt.

## Causal mechanism

The failure was produced by two coupled controller conditions:

1. The legacy conversation controller treated the arrival of any reply to a pending boundary/counterexample question as sufficient to set `boundary_answered=true`. It did not distinguish a true counterexample/discriminating answer from a reply that merely introduced another possible factor.
2. Once that boolean gate was open, the planner was explicitly encouraged to produce a nontrivial synthesis with explanatory compression, while its contract lacked explicit evidence-direction guards against unsupported comparative weighting, causal weighting, cross-context projection, construct conflation, circular abstractions, or strengthened scope/quantifiers.

That combination allowed `factor A affects the outcome` plus `factor B also affects the outcome` to be compressed into `the outcome is less about A than B` without comparative evidence. It also allowed a factor observed in one context to be generalized into another context without direct support.

This was therefore not merely unfortunate wording or a random model miss. **Reply-arrival was used as a proxy for boundary resolution, then compression was rewarded before the evidence relationship had been verified.**

## Repair

The deployed owner-only reasoning path now fixes both levels of the defect.

### Semantic boundary-resolution gate

A pending counterexample/boundary reply no longer opens the synthesis gate merely because the participant replied. Before the inherited controller sees that turn, `life_patterns_boundary_resolution_v1` asks whether the latest answer actually supplies discriminating evidence responsive to the preceding question.

`resolved=true` requires something such as a concrete exception, a case that breaks or preserves the proposed contrast, or a direct comparison that separates live possibilities. Merely adding another factor, shifting to an adjacent variable, restating the pattern, expressing uncertainty, or failing to recall a counterexample leaves the boundary unresolved. Missing recall is never treated as real-world absence.

The reasoning session clears the legacy pending flag and sets `boundary_answered` from this semantic result before delegating, so the legacy reply-arrival proxy cannot reopen the gate on the deployed owner path.

### Primary interviewer discipline

The planner is explicitly instructed that:

- additional reported factors are additive unless evidence actually compares their importance;
- `more`, `less`, `mainly`, `primarily`, or `rather than` claims require direct discriminating support;
- a factor from one context may not be projected into another context without support;
- distinct reported outcomes remain distinct unless the participant links them;
- umbrella labels may not merely rename the phenomenon being explained;
- an unresolved counterexample should trigger the useful missing question rather than premature synthesis;
- after participant disagreement, the model should identify the weakest unsupported inference itself instead of defaulting to `what did I get wrong?`.

### Hidden pre-surface hypothesis audit

Every proposed `surface_hypothesis` receives a second target-theory-blind support audit before display. It can reject unsupported comparison, unsupported causal weighting, cross-context projection, construct conflation, circular abstraction, unresolved boundary/counterexample, quantifier/scope strengthening, or another unsupported inference.

A failed audit suppresses the synthesis and converts the move into one targeted discriminating question. A supported synthesis passes through unchanged.

### Rejected-synthesis recovery

`No — keep investigating` invokes the reasoning planner on the existing evidence/conversation instead of returning a canned request for the participant to diagnose the failure. The same pattern inquiry remains live.

## Scientific / privacy boundary

This is a product-reasoning repair, not a change to the accepted v2 evidence semantics. Preproposal versus post-proposal provenance, participant authority, target-theory blindness, append-only correction/provenance, and the episode-fact/person-pattern firewall remain unchanged. No astrology/target hints, broader access, transcript persistence, Railway volume, or request-body logging were added.

## Verification / deployment

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`;
- `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py` routes the authenticated owner surface through the reasoning-guarded app;
- `tests/unit/test_life_patterns_v2_owner_reasoning.py` covers unsupported-comparison interception, supported-synthesis pass-through, model-led recovery after disagreement, and the exact controller regression that a merely relevant reply must not open the synthesis gate when the boundary is not semantically resolved.

Exact final code/test head: `b1a54ef62194c28d7e531aeabc3f7e552ebf5064`.

GitHub Actions run `34879139088`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

Existing owner-only Railway service reused; no new service and no access broadening.

- service: `life-patterns-owner`;
- deployment: `72dd705c-d544-4e13-ace2-29bba7ce2497`;
- application source head: `a4262667f190ec5fa18d3748c7f010d8e0d900c6`;
- status: **SUCCESS**;
- application startup complete;
- Railway `/healthz`: HTTP `200`;
- deployed health contract includes `semantic_boundary_resolution=true`, `hypothesis_support_audit=true`, and `rejection_reasoning_recovery=true`.

The test-only commit is outside the Railway application watch surface, so deployed application bytes correctly remain the semantic-boundary implementation head above.

## Next decision-changing evidence

Owner retest should focus on reasoning quality rather than merely liveness:

1. Does a reply only count as resolving a counterexample when it actually answers the requested discriminator?
2. Does the interviewer refrain from turning an additional factor into unsupported relative weighting?
3. Does it avoid projecting factors across contexts or merging distinct outcomes without evidence?
4. When evidence does not yet discriminate possibilities, does it ask the useful missing question rather than manufacture an elegant synthesis?
5. If a synthesis is still rejected, does the interviewer diagnose the likely unsupported inference itself rather than making the owner restate the obvious problem?
6. After a satisfactory thread, is `Finish for now` useful enough to justify durable persistence / a real Life Patterns Map?

**There was never a completion policy.**
