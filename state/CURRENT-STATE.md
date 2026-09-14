# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-owner-multi-pattern-continuation` — **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`.

Independent semantic review: **PASS** — zero blockers, `semantic_change_required=false`.

Bounded v2 core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`.

The accepted v2 substrate remains authoritative: open-world episode facts plus participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

## Product strategy history

The surfaced fact-review/paraphrase workflow failed direct owner product judgment and is **FAILED / REPLACED**.

The replacement hidden-ledger interview was restored to **pattern-first** elicitation. A full bounded real owner session later produced useful non-parroting information gain and was judged **GOOD / PASS / PRELIMINARY POSITIVE**.

Repeated-thread owner testing then exposed two liveness defects:

1. uncertainty after a tentative synthesis was terminalized instead of allowing same-thread continuation;
2. a wrong tentative synthesis followed by `No` was treated as terminal rejection of the whole inquiry.

Both were repaired. `Keep trying to pin it down` preserves an uncertain thread, while `No — keep investigating` rejects the current synthesis but keeps the inquiry live; `Reject and stop this thread` is the explicit terminal rejection.

Receipts:

- `state/LIFE-PATTERNS-v2-OWNER-UNRESOLVED-CONTINUATION-REPAIR-2026-09-14.md`
- `state/LIFE-PATTERNS-v2-OWNER-REJECTED-SYNTHESIS-CONTINUATION-REPAIR-2026-09-14.md`

## Hypothesis reasoning failure — causal diagnosis

The owner then correctly rejected a liveness-only interpretation of the latest failure. The larger defect occurred **before** adjudication: the interviewer produced a plausible-sounding synthesis that materially overreached the supplied evidence, creating unnecessary burden for the participant to correct an obvious inference error.

Code/prompt trace established two coupled causes:

1. `ConversationalOwnerSession.turn()` treated the arrival of any reply to a pending boundary/counterexample question as sufficient to set `boundary_answered=true`. The controller did not distinguish an actual counterexample/discriminating answer from a reply that merely introduced another possible factor.
2. Once that boolean gate was open, the planner was explicitly encouraged to surface a nontrivial synthesis with `explanatory compression`, but its contract lacked explicit evidence-direction checks against unsupported factor ranking, causal weighting, cross-context projection, construct conflation, circular umbrella abstractions, and strengthened scope/quantifiers.

The resulting failure class is therefore not random model error. The controller made premature synthesis structurally easy: **reply-arrival was used as a proxy for boundary resolution, then compression was rewarded before the evidence relationship had been audited**.

In particular, introducing an additional factor does not establish that an earlier factor matters less, more, mainly, primarily, or `rather than` the new factor. A context-specific factor also cannot be projected into a different context merely because both episodes concern the same broad pattern.

## Reasoning-layer repair

Repair receipt:

`state/LIFE-PATTERNS-v2-OWNER-HYPOTHESIS-REASONING-REPAIR-2026-09-14.md`

The owner-only interview now adds two reasoning controls without changing accepted v2 semantics.

### 1. Stronger primary interviewer discipline

The planner is explicitly instructed to:

- treat additional reported factors as additive unless direct evidence compares their importance;
- require discriminating support before using `more`, `less`, `mainly`, `primarily`, or `rather than`;
- avoid transferring a factor from one episode/context into another without support;
- preserve distinctions among reported outcomes unless the participant links them;
- reject explanatory abstractions that merely rename the phenomenon;
- treat a reply that merely adds another factor as **not necessarily resolving** the requested boundary/counterexample;
- after participant disagreement, identify the likely unsupported leap itself rather than defaulting to `what did I get wrong?`.

### 2. Hidden pre-surface hypothesis support audit

Every proposed `surface_hypothesis` now receives a second target-theory-blind support audit before it can be shown. The audit can block unsupported comparison, unsupported causal weighting, cross-context projection, construct conflation, circular abstraction, unresolved boundary/counterexample, quantifier/scope strengthening, or another unsupported inference.

If the audit fails, the candidate synthesis is suppressed and replaced with one targeted discriminating follow-up question. A supported synthesis passes through unchanged.

`No — keep investigating` now also invokes model-led reasoning on the existing evidence/conversation rather than returning a canned request that the participant diagnose the failure.

## Scientific / privacy boundary

This repair changes product reasoning only. Preproposal versus post-proposal provenance, participant authority, target-theory blindness, and the episode-fact/person-pattern firewall are unchanged. No target-model scoring, astrology hints, broader access, automatic transcript persistence, Railway volume, or request-body logging was added.

Private owner interview narrative was not committed; only the abstract product finding and generic regressions were preserved.

## Verification / deployment

Reasoning implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`;
- secured owner wrapper now routes through the reasoning-guarded app;
- `tests/unit/test_life_patterns_v2_owner_reasoning.py` covers unsupported-comparison interception, supported-synthesis pass-through, and model-led rejection recovery.

Exact code/test head: `6a836b68b929f4e11eabcf8602bc2f6b23386b62`.

GitHub Actions run `34878158579`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy all passed.

Existing authenticated Railway owner service reused. Deployment `bfab11be-16c6-4c78-8931-70ba9ae502d7` from application source head `b8bc552d0c02370ace4f942db95f1616bb2d4234` is **SUCCESS**. Application startup completed and Railway `/healthz` returned HTTP `200`. The deployed health contract includes `hypothesis_support_audit=true` and `rejection_reasoning_recovery=true`.

No new service was created and access was not broadened.

## Current outcome / next gate

Outcome advancement: **PRELIMINARY POSITIVE WITH THE OBSERVED SYNTHESIS-REASONING DEFECT REPAIRED**.

Strategy efficacy: **VIABLE; REASONING-GUARD OWNER RETEST REQUIRED**.

Next gate: **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

1. Refresh the deployed owner-only browser and run a natural pattern thread.
2. Judge whether additional factors remain additive unless comparative evidence exists, context-specific factors stay context-specific, and unresolved contrasts produce a useful follow-up instead of a premature synthesis.
3. If a synthesis is still wrong, choose `No — keep investigating` and judge whether the interviewer identifies the likely unsupported inference itself rather than requiring the owner to explain an obvious mistake.
4. After a satisfactory thread, use `Finish for now` and judge whether the session-level summary is useful enough to justify durable persistence / a real Life Patterns Map.

Owner-triggered copy/export remains available. Automatic transcript logging remains out of scope.

Authorized: bounded owner-only testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

Focused completion command: `python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_pattern_first.py tests/unit/test_life_patterns_v2_owner_refinement.py tests/unit/test_life_patterns_v2_owner_reasoning.py -q`

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
