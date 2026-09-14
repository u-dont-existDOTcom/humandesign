# Life Patterns current state — 2026-09-14

V2 independent semantic review: **PASS**.

- Candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
- Blocking semantic findings: `0`
- Semantic change required: `false`
- Adapter-firewall repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`
- Bounded v2 core implementation verified: `true`
- Pattern-first runtime repair head: `67b038b27d62b941b6beb224c6e89efd0d165bb4`
- Multi-pattern continuation head: `da3c5f58101d8cc10421e480d44b5162bd12ec78`
- Rejected-synthesis continuation repair head: `3536bf88f422551abfb9ff41f63e5690ecdb77e4`
- Hypothesis-reasoning final code/test head: `6a836b68b929f4e11eabcf8602bc2f6b23386b62`
- Hosted hypothesis-reasoning CI: `34878158579` — `success`
- Railway hypothesis-reasoning deployment: `bfab11be-16c6-4c78-8931-70ba9ae502d7` — `success`
- Active task: `life-patterns-v2-owner-multi-pattern-continuation` — OWNER REAL-DATA BROWSER JUDGMENT REQUIRED

## Direct owner product evidence

The surfaced fact-review/paraphrase strategy is **FAILED / REPLACED**.

The hidden-ledger, pattern-first interview later completed a bounded real owner thread successfully and was judged **GOOD / PASS / PRELIMINARY POSITIVE**.

Repeated-thread testing then exposed two liveness defects, both repaired: uncertainty was incorrectly terminalized, and later a wrong tentative synthesis followed by `No` terminalized the whole inquiry instead of only rejecting the current synthesis.

The owner then identified the deeper issue: **fixing liveness was not enough because the tentative synthesis itself contained an obvious unsupported inference**. Participants should not have to supply basic reasoning repair after the product has overinterpreted their evidence.

No private owner interview narrative is stored in repository state.

## Current participant-facing method

The participant starts with a self-noticed pattern. Concrete situations, contrasts, life-phase material, exceptions, and boundary cases are used as evidence anchors in a hidden v2 ledger. A synthesis is tentative and remains subject to participant authority.

The current panel distinguishes:

- `Yes — keep that`;
- `Close, but change it`;
- `No — keep investigating`;
- `Keep trying to pin it down`;
- `Leave it unresolved for now`;
- `Reject and stop this thread`.

`No — keep investigating` rejects the synthesis without terminating the pattern inquiry. `Reject and stop this thread` is the explicit terminal rejection.

## Hypothesis-reasoning failure mechanism

The observed reasoning error was structurally enabled by the controller:

1. Any reply to a pending boundary/counterexample question automatically set `boundary_answered=true`, even when the reply merely introduced another factor rather than supplying the requested discriminating case.
2. With that boolean gate open, the planner was encouraged to surface a nontrivial synthesis with explanatory compression.
3. The planner contract did not explicitly forbid turning an additional factor into a relative-weight claim, projecting a factor from one context into another, merging distinct reported outcomes, using a circular umbrella abstraction, or strengthening scope/quantifiers beyond the evidence.

Thus a new factor could be misread as evidence that an earlier factor mattered less, even though no comparison had been supplied. This was a reasoning-contract defect, not merely an unfortunate wording choice.

## Reasoning-layer repair

Repair receipt: `state/LIFE-PATTERNS-v2-OWNER-HYPOTHESIS-REASONING-REPAIR-2026-09-14.md`.

The primary interviewer is now explicitly constrained to preserve evidence direction:

- additive factors remain additive unless comparative evidence exists;
- relative-weight language requires direct support;
- context-specific factors remain context-specific unless linked;
- distinct reported outcomes remain distinct unless the participant links them;
- umbrella abstractions cannot merely rename the phenomenon;
- a reply does not count as resolving a requested boundary merely because a reply occurred;
- participant disagreement should trigger model-led diagnosis of the weakest unsupported inference, not a generic request that the participant explain the obvious mistake.

In addition, **every proposed surface hypothesis now receives a hidden second-pass support audit before display**. The audit blocks unsupported comparison, unsupported causal weighting, cross-context projection, construct conflation, circular abstraction, unresolved boundary/counterexample, quantifier/scope strengthening, or another unsupported inference.

If the audit fails, the synthesis is not shown. The participant instead gets one targeted discriminating question. Supported syntheses pass through unchanged.

## Scientific and privacy invariants

The repair does not change accepted v2 evidence semantics. Preproposal/post-proposal timing, append-only provenance, participant person-level authority, target-theory blindness, and the episode-fact/person-pattern firewall remain unchanged.

No astrology or target-model hints are exposed. No automatic transcript persistence, Railway volume, or request-body logging was added. No target-model scoring or external participant activity is authorized.

## Verification / deployment

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`;
- the secured owner deployment wrapper now uses the reasoning-guarded app;
- `tests/unit/test_life_patterns_v2_owner_reasoning.py` contains focused regressions for unsupported-comparison interception, supported-synthesis pass-through, and model-led rejection recovery.

Exact final code/test head `6a836b68b929f4e11eabcf8602bc2f6b23386b62` passed GitHub Actions run `34878158579`: unit/integration tests, Ruff, and strict mypy all succeeded.

The existing authenticated owner-only service was reused. Deployment `bfab11be-16c6-4c78-8931-70ba9ae502d7` from application source head `b8bc552d0c02370ace4f942db95f1616bb2d4234` is **SUCCESS**. Runtime startup completed and Railway `/healthz` returned HTTP `200`. The deployed health contract includes `hypothesis_support_audit=true` and `rejection_reasoning_recovery=true`.

## Current gate

One-pattern strategy evidence: **GOOD / PASS / PRELIMINARY POSITIVE**.

Observed reasoning defect: **CAUSALLY DIAGNOSED / IMPLEMENTED REPAIR / VERIFIED / DEPLOYED**.

Next gate: **OWNER REAL-DATA REASONING JUDGMENT REQUIRED**.

1. Run a natural fresh thread and judge whether the interviewer now refuses unsupported comparative weighting and cross-context compression.
2. Where evidence is still ambiguous, judge whether it asks the missing discriminating question instead of surfacing an elegant but unsupported synthesis.
3. If a synthesis is still wrong, use `No — keep investigating` and judge whether the interviewer diagnoses the likely unsupported inference itself rather than requiring an obvious explanation from the owner.
4. Then use `Finish for now` and judge whether the session summary is useful enough to justify durable persistence / a real Life Patterns Map.

Optional copy/export remains owner-triggered. Automatic transcript logging remains out of scope.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
