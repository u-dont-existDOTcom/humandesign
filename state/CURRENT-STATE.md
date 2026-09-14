# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-owner-multi-pattern-continuation` — **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

V2 independent semantic review remains **PASS** with zero blockers and `semantic_change_required=false`.

The accepted substrate is unchanged: open-world episode facts plus participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall. The participant-facing interview may be changed without weakening these internal semantics.

## Product strategy history

The surfaced fact-review/paraphrase workflow is **FAILED / REPLACED**.

The hidden-ledger pattern-first replacement completed a bounded real owner session successfully and was judged **GOOD / PASS / PRELIMINARY POSITIVE**. Multi-pattern continuation was added. Two later liveness defects were repaired: uncertainty after a synthesis no longer forces terminal unresolved, and `No` no longer terminates the entire inquiry unless the owner explicitly chooses `Reject and stop this thread`.

A later reasoning repair addressed unsupported comparative/cross-context synthesis. Direct owner testing then exposed a more fundamental regression: the interviewer had become severely over-interrogative even on an intentionally ordinary recurring pattern, repeatedly seeking contrasts and distinctions after the useful pattern was already clear.

No private owner interview narrative is committed; only abstract product findings are preserved.

## Current causal diagnosis: requirement accretion

Repository comparison confirms the owner's judgment that the earlier interview conduct was better.

The historical interviewer explicitly required adaptive burden control:

- ask examples or clarification only when they add something important;
- main questions, probes, and follow-ups are choices, not a mandatory loop;
- before any follow-up, identify what different answers would materially change; if neither would change the retained interpretation, move on;
- do not request restatement of information already supplied;
- do not demand hypothetical edge cases;
- unknown / declined may remain unresolved without reopening;
- do not hunt for contradiction;
- when a question is called obvious, redundant, confusing, or already answered, inspect the interviewer question first and drop it when not materially necessary.

The later v2 product layer accidentally hardened assistant-inferred scaffolding that was **not required by the accepted v2 semantic contract**:

1. pressure for at least two concrete episodes;
2. a boundary/counterexample before synthesis;
3. a hard `boundary_answered` prerequisite;
4. a two-episode proposal-creation requirement;
5. pressure for explanatory compression/novelty;
6. a later semantic boundary classifier and second pre-surface audit that strengthened the same interrogative scaffold.

The v2 record schema requires grounded evidence and participant adjudication, but not two episodes, a mandatory counterexample, or explanatory novelty. The historical Life Patterns continuity finding likewise says to request only enough evidence to anchor/challenge a claim and to ask for an exception/counterexample **without forcing one**.

This is classified as **requirement accretion causing product regression**, not simply a low-intelligence model response.

## Current participant-facing strategy: adaptive stopping restored

Repair receipt:

`state/LIFE-PATTERNS-v2-OWNER-ADAPTIVE-STOPPING-REPAIR-2026-09-14.md`

The deployed owner interview now restores the earlier information-gain / burden rule while retaining the hidden v2 ledger and participant authority.

Current rules:

- **no fixed episode quota**;
- **no mandatory counterexample/boundary gate**;
- another question is admitted only when plausible answers can materially change the retained pattern's meaning, scope, context, timing, exceptions, or uncertainty;
- when another answer would not materially change the pattern, surface the narrow supported synthesis;
- simple/ordinary patterns are allowed to remain simple/ordinary; do not manufacture depth;
- unknown, not remembered, inapplicable, or declined may remain unresolved without repeated drilling;
- do not ask participants to distinguish internal states they could not reasonably observe;
- do not restate or re-ask supplied information;
- additive factors remain additive unless comparative evidence exists;
- context-specific factors are not projected across contexts without support;
- explanatory novelty is not required;
- one grounded episode may be sufficient when paired with an explicit participant-reported recurring self-description;
- one isolated occurrence still cannot be silently promoted to recurrence;
- rejected-synthesis recovery remains model-led;
- post-proposal evidence timing and all accepted v2 scientific/privacy invariants remain unchanged.

The previous hidden second-pass hypothesis audit is disabled on the adaptive path because direct owner evidence showed that the stricter scaffold was increasing participant burden rather than improving the product outcome.

## Verification / deployment

Adaptive implementation: `src/hdmatch/api/life_patterns_v2_owner_reasoning.py` (compatibility entry point retained; it now serves the adaptive interviewer).

Regression coverage verifies adaptive stopping, no mandatory episode/counterexample quota, one grounded episode + recurring self-report sufficiency, protection against single-event recurrence promotion, non-reopening after `I don't know`, and model-led rejection recovery.

Exact verified application head: `26057ea84366bd56c59a0725fe7681c7544d3800`.

GitHub Actions run `34910994811`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy all passed. The immediately preceding run showed **732 passed / 7 skipped** and failed only on one Ruff style suggestion; the lint-only repair produced the fully green final run.

Existing authenticated owner-only Railway service reused:

- deployment: `f4a8e388-311f-4418-addf-f4291afc1836`;
- source head: `26057ea84366bd56c59a0725fe7681c7544d3800`;
- status: **SUCCESS**;
- application startup complete;
- `/healthz` -> HTTP `200`;
- health contract declares `adaptive_information_gain_gate=true`, `fixed_episode_quota=false`, `mandatory_counterexample_gate=false`, `hypothesis_support_audit=false`.

No new service, broadened access, persistence layer, target-model activity, or private transcript logging was introduced.

## Current outcome / next gate

Outcome advancement: **PRELIMINARY POSITIVE, WITH A REQUIREMENT-ACCRETION REGRESSION IDENTIFIED AND THE PRIOR ADAPTIVE INTERVIEW STRATEGY RESTORED AS THE CURRENT CANDIDATE**.

Strategy efficacy: **ADAPTIVE RESTORATION VIABLE; OWNER RETEST REQUIRED**.

Next owner test:

1. Use one intentionally ordinary/simple recurring pattern. The interviewer should stop when another question would not materially change the formulation instead of trying to discover hidden complexity.
2. Use one genuinely nuanced/context-dependent pattern. It should still ask a discriminating question when different answers would materially change the synthesis.
3. Confirm that `I don't know` and unobservable distinctions are not repeatedly reopened.
4. If a synthesis is wrong, use `No — keep investigating` and judge whether it repairs intelligently without requiring obvious restatement.
5. Use `Finish for now` and judge whether the session summary is useful enough to justify durable persistence / a real Life Patterns Map.

Owner-triggered copy/export remains available. Automatic transcript logging remains out of scope.

Authorized: bounded owner-only testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
