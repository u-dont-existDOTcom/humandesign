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
- Semantic boundary-resolution implementation head: `a4262667f190ec5fa18d3748c7f010d8e0d900c6`
- Hypothesis-reasoning final code/test head: `b1a54ef62194c28d7e531aeabc3f7e552ebf5064`
- Hosted hypothesis-reasoning CI: `34879139088` — `success`
- Railway hypothesis-reasoning deployment: `72dd705c-d544-4e13-ace2-29bba7ce2497` — `success`
- Active task: `life-patterns-v2-owner-multi-pattern-continuation` — OWNER REAL-DATA BROWSER JUDGMENT REQUIRED

## Direct owner product evidence

The surfaced fact-review/paraphrase strategy is **FAILED / REPLACED**.

The hidden-ledger, pattern-first interview later completed a bounded real owner thread successfully and was judged **GOOD / PASS / PRELIMINARY POSITIVE**.

Repeated-thread testing exposed two liveness defects, both repaired: uncertainty was incorrectly terminalized, and later a wrong tentative synthesis followed by `No` terminalized the whole inquiry instead of only rejecting the current synthesis.

The owner then identified the deeper issue: **fixing liveness was not enough because the tentative synthesis itself contained an obvious unsupported inference**. Participants should not have to supply basic reasoning repair after the product has overinterpreted their evidence.

No private owner interview narrative is stored in repository state.

## Current participant-facing method

The participant starts with a self-noticed pattern. Concrete situations, contrasts, life-phase material, exceptions, and boundary cases are used as evidence anchors in a hidden v2 ledger. A synthesis is tentative and remains subject to participant authority.

The panel distinguishes `Yes — keep that`, `Close, but change it`, `No — keep investigating`, `Keep trying to pin it down`, `Leave it unresolved for now`, and `Reject and stop this thread`.

## Hypothesis-reasoning failure mechanism

The observed reasoning error was structurally enabled by the controller:

1. The legacy conversation state treated any reply to a pending boundary/counterexample question as `boundary_answered=true`, even when the reply merely introduced another factor instead of supplying the requested discriminating case.
2. With that boolean gate open, the planner was encouraged to surface a nontrivial synthesis with explanatory compression.
3. The planner contract did not explicitly forbid turning an additional factor into a relative-weight claim, projecting a factor from one context into another, merging distinct reported outcomes, using a circular umbrella abstraction, or strengthening scope/quantifiers beyond the evidence.

Thus a new factor could be misread as evidence that an earlier factor mattered less, even though no comparison had been supplied. This was a reasoning-contract and state-gating defect, not merely an unfortunate wording choice.

## Reasoning-layer repair

Repair receipt: `state/LIFE-PATTERNS-v2-OWNER-HYPOTHESIS-REASONING-REPAIR-2026-09-14.md`.

### Semantic boundary resolution

The deployed reasoning session now classifies whether the participant's answer actually resolves the pending boundary/counterexample before the synthesis gate can open. `resolved=true` requires discriminating evidence responsive to the question. A reply that merely adds another factor, shifts variables, restates the pattern, gives general uncertainty, or lacks a concrete counterexample remains unresolved. Missing recall does not establish real-world absence.

The reasoning session clears the legacy pending flag and sets `boundary_answered` from this semantic result before delegating, so the old reply-arrival proxy cannot reopen the synthesis gate on the deployed owner path.

### Evidence-direction discipline

The interviewer is explicitly constrained so that:

- additive factors remain additive unless comparative evidence exists;
- relative-weight language requires direct support;
- context-specific factors remain context-specific unless linked;
- distinct reported outcomes remain distinct unless the participant links them;
- umbrella abstractions cannot merely rename the phenomenon;
- unresolved contrasts trigger the useful missing question rather than premature synthesis;
- participant disagreement triggers model-led diagnosis of the weakest unsupported inference, not a generic request that the participant explain the obvious mistake.

### Hidden pre-surface support audit

Every proposed surface hypothesis receives a hidden second-pass support audit before display. The audit blocks unsupported comparison, unsupported causal weighting, cross-context projection, construct conflation, circular abstraction, unresolved boundary/counterexample, quantifier/scope strengthening, or another unsupported inference.

If the audit fails, the synthesis is not shown; the participant receives one targeted discriminating question. Supported syntheses pass unchanged.

## Scientific and privacy invariants

The repair does not change accepted v2 evidence semantics. Preproposal/post-proposal timing, append-only provenance, participant person-level authority, target-theory blindness, and the episode-fact/person-pattern firewall remain unchanged.

No astrology or target-model hints are exposed. No automatic transcript persistence, Railway volume, or request-body logging was added. No target-model scoring or external participant activity is authorized.

## Verification / deployment

- final code/test head: `b1a54ef62194c28d7e531aeabc3f7e552ebf5064`;
- GitHub Actions run `34879139088`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed;
- owner-only Railway deployment: `72dd705c-d544-4e13-ace2-29bba7ce2497` from application source `a4262667f190ec5fa18d3748c7f010d8e0d900c6`: **SUCCESS**;
- application startup complete and Railway `/healthz`: HTTP `200`;
- health contract includes `semantic_boundary_resolution=true`, `hypothesis_support_audit=true`, and `rejection_reasoning_recovery=true`.

The test-only head is outside the Railway watch surface, so deployed application bytes correctly remain the semantic-boundary implementation head.

## Current gate

One-pattern strategy evidence: **GOOD / PASS / PRELIMINARY POSITIVE**.

Observed reasoning defect: **CAUSALLY DIAGNOSED / ROOT CONTROLLER + SYNTHESIS REPAIR IMPLEMENTED / VERIFIED / DEPLOYED**.

Next gate: **OWNER REAL-DATA REASONING JUDGMENT REQUIRED**.

1. Run a natural fresh thread and judge whether a reply only counts as resolving a boundary when it actually answers the requested discriminator.
2. Judge whether the interviewer refuses unsupported comparative weighting and cross-context compression.
3. Where evidence remains ambiguous, judge whether it asks the missing discriminating question instead of surfacing an elegant but unsupported synthesis.
4. If a synthesis is still wrong, use `No — keep investigating` and judge whether the interviewer diagnoses the likely unsupported inference itself rather than requiring an obvious explanation from the owner.
5. Then use `Finish for now` and judge whether the session summary is useful enough to justify durable persistence / a real Life Patterns Map.

Optional copy/export remains owner-triggered. Automatic transcript logging remains out of scope.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
