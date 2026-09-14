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

Repeated-thread owner testing then exposed two liveness defects, both repaired: uncertainty after a tentative synthesis was terminalized, and a wrong tentative synthesis followed by `No` was treated as terminal rejection of the whole inquiry. The current panel separates `Keep trying to pin it down`, `No — keep investigating`, `Leave it unresolved for now`, and `Reject and stop this thread`.

Receipts:

- `state/LIFE-PATTERNS-v2-OWNER-UNRESOLVED-CONTINUATION-REPAIR-2026-09-14.md`
- `state/LIFE-PATTERNS-v2-OWNER-REJECTED-SYNTHESIS-CONTINUATION-REPAIR-2026-09-14.md`

## Hypothesis reasoning failure — causal diagnosis

The owner explicitly rejected a liveness-only repair as insufficient. The larger defect occurred **before** adjudication: the interviewer produced a plausible-sounding synthesis that materially overreached the evidence, forcing the participant to correct an obvious inference error.

Code/prompt trace established two coupled causes:

1. The legacy conversation controller treated the arrival of any reply to a pending boundary/counterexample question as sufficient to set `boundary_answered=true`. It did not distinguish an actual discriminating answer from a reply that merely introduced another possible factor.
2. With that boolean gate open, the planner was encouraged to produce a nontrivial synthesis with `explanatory compression`, while its contract lacked explicit evidence-direction checks against unsupported factor ranking, causal weighting, cross-context projection, construct conflation, circular umbrella abstractions, and strengthened scope/quantifiers.

The resulting failure class is not random model error. **Reply-arrival was used as a proxy for boundary resolution, then compression was rewarded before the evidence relationship had been verified.** Introducing an additional factor does not establish that an earlier factor matters less, more, mainly, primarily, or `rather than` the new factor. A context-specific factor also cannot be projected into a different context merely because both episodes concern the same broad pattern.

## Reasoning-layer repair

Repair receipt:

`state/LIFE-PATTERNS-v2-OWNER-HYPOTHESIS-REASONING-REPAIR-2026-09-14.md`

The deployed owner reasoning path now repairs the controller signal itself, not only its downstream consequence.

### 1. Semantic boundary-resolution gate

When a boundary/counterexample question is pending, the reasoning session first asks a hidden target-theory-blind classifier whether the latest participant answer actually supplies discriminating evidence responsive to that question. A reply that merely adds another factor, shifts to an adjacent variable, restates the pattern, expresses uncertainty, or fails to recall a concrete counterexample does **not** resolve the boundary.

The reasoning session clears the legacy pending flag and sets `boundary_answered` from this semantic result before delegating. Therefore the deployed owner path no longer lets mere reply-arrival open the synthesis gate. Missing recall is not converted into real-world absence.

### 2. Stronger primary interviewer discipline

The planner is explicitly instructed to:

- treat additional reported factors as additive unless direct evidence compares their importance;
- require discriminating support before using `more`, `less`, `mainly`, `primarily`, or `rather than`;
- avoid transferring a factor from one episode/context into another without support;
- preserve distinctions among reported outcomes unless the participant links them;
- reject explanatory abstractions that merely rename the phenomenon;
- keep an unresolved counterexample unresolved and ask the useful missing question;
- after participant disagreement, identify the likely unsupported leap itself rather than defaulting to `what did I get wrong?`.

### 3. Hidden pre-surface hypothesis support audit

Every proposed `surface_hypothesis` receives a second target-theory-blind support audit before display. The audit can block unsupported comparison, unsupported causal weighting, cross-context projection, construct conflation, circular abstraction, unresolved boundary/counterexample, quantifier/scope strengthening, or another unsupported inference.

If the audit fails, the candidate synthesis is suppressed and replaced with one targeted discriminating follow-up question. A supported synthesis passes through unchanged.

`No — keep investigating` also invokes model-led reasoning on the existing evidence/conversation rather than returning a canned request that the participant diagnose the failure.

## Scientific / privacy boundary

This repair changes product reasoning only. Preproposal versus post-proposal provenance, participant authority, target-theory blindness, append-only correction/provenance, and the episode-fact/person-pattern firewall are unchanged. No target-model scoring, astrology hints, broader access, automatic transcript persistence, Railway volume, or request-body logging was added.

Private owner interview narrative was not committed; only the abstract product finding and generic regressions were preserved.

## Verification / deployment

Reasoning implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`;
- secured owner wrapper routes through the reasoning-guarded app;
- `tests/unit/test_life_patterns_v2_owner_reasoning.py` covers unsupported-comparison interception, supported-synthesis pass-through, model-led rejection recovery, and the exact state-machine regression that a merely relevant reply must not open the synthesis gate when the boundary is not semantically resolved.

Exact final code/test head: `b1a54ef62194c28d7e531aeabc3f7e552ebf5064`.

GitHub Actions run `34879139088`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy all passed.

Existing authenticated Railway owner service reused. Deployment `72dd705c-d544-4e13-ace2-29bba7ce2497` from application source head `a4262667f190ec5fa18d3748c7f010d8e0d900c6` is **SUCCESS**. Application startup completed and Railway `/healthz` returned HTTP `200`. The deployed health contract includes `semantic_boundary_resolution=true`, `hypothesis_support_audit=true`, and `rejection_reasoning_recovery=true`.

The test-only commit is outside the Railway application watch surface, so deployed application bytes correctly remain the semantic-boundary implementation head. No new service was created and access was not broadened.

## Current outcome / next gate

Outcome advancement: **PRELIMINARY POSITIVE WITH THE OBSERVED SYNTHESIS-REASONING DEFECT REPAIRED**.

Strategy efficacy: **VIABLE; REASONING-GUARD OWNER RETEST REQUIRED**.

Next gate: **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

1. Refresh the deployed owner-only browser and run a natural pattern thread.
2. Judge whether a reply only opens synthesis when it actually answers the requested discriminator.
3. Judge whether additional factors remain additive unless comparative evidence exists, context-specific factors stay context-specific, and unresolved contrasts produce a useful follow-up instead of a premature synthesis.
4. If a synthesis is still wrong, choose `No — keep investigating` and judge whether the interviewer identifies the likely unsupported inference itself rather than requiring the owner to explain an obvious mistake.
5. After a satisfactory thread, use `Finish for now` and judge whether the session-level summary is useful enough to justify durable persistence / a real Life Patterns Map.

Owner-triggered copy/export remains available. Automatic transcript logging remains out of scope.

Authorized: bounded owner-only testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

Focused completion command: `python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_pattern_first.py tests/unit/test_life_patterns_v2_owner_refinement.py tests/unit/test_life_patterns_v2_owner_reasoning.py -q`

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
