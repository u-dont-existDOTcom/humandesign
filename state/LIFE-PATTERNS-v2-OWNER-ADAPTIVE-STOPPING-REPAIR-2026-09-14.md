# Life Patterns v2 owner adaptive-stopping repair — 2026-09-14

Status: **IMPLEMENTED / VERIFIED / DEPLOYED — OWNER RETEST REQUIRED**.

## Direct owner finding

A fresh owner-only browser test with an intentionally ordinary recurring pattern exposed severe over-interrogation. The interviewer kept demanding extra contrasts and increasingly artificial distinctions after the basic pattern was already clear, reopened uncertainty after the participant said they did not know, and asked a distinction the participant could not directly observe.

The owner reported that the interview had not been this unintelligent earlier in development. Repository comparison supports that judgment. No private interview transcript or narrative detail is persisted here; only the abstract product finding is recorded.

## Causal diagnosis: requirement accretion / regression

The older Life Patterns interview conduct already had a strong adaptive burden rule:

- examples or clarification only when they add something important;
- main questions, probes, and follow-ups are choices, not a mandatory loop;
- before a follow-up, identify what different answers would materially change; if neither would change the retained interpretation, move on;
- do not ask for restatement of supplied information;
- do not demand hypothetical edge cases;
- unknown / declined may remain unresolved and should not be reopened without new information;
- do not hunt for contradiction;
- when a question is called obvious, redundant, confusing, or already answered, inspect the interviewer question first and drop it when it is not materially necessary.

The later v2 product layer accidentally converted evidence hygiene into participant-facing prerequisites that were not required by the accepted v2 semantic contract:

1. planner pressure to obtain at least two concrete episodes;
2. a boundary/counterexample question before synthesis;
3. a hard `boundary_answered` gate;
4. a two-episode requirement in proposal creation;
5. pressure for `explanatory compression` rather than allowing a simple supported formulation;
6. the subsequent semantic-boundary classifier and second pre-surface audit strengthened the same interrogative scaffold.

The accepted v2 record schema requires grounded evidence and participant adjudication but does **not** require two episodes, a mandatory counterexample, or explanatory novelty. Historical project state also explicitly said to request only enough concrete evidence to anchor or challenge a claim and to ask for a useful exception/counterexample without forcing one.

Therefore the latest failure is classified as **requirement accretion causing product regression**, not merely low model intelligence.

## Repair: restore the simpler adaptive interviewer

The deployed owner path now restores the earlier information-gain / burden discipline while retaining the accepted v2 hidden ledger and participant authority.

Current rules:

- no fixed episode quota;
- no mandatory counterexample or boundary gate;
- another question is admitted only when plausible answers can materially change the retained pattern's meaning, scope, context, timing, exception structure, or uncertainty;
- if another answer would not materially change the pattern, surface the narrow supported synthesis;
- ordinary/simple patterns are allowed to remain ordinary/simple; do not manufacture depth;
- unknown, not remembered, inapplicable, or declined may remain unresolved without repeated drilling;
- do not ask a participant to distinguish internal states they could not reasonably observe;
- do not restate or re-ask information already supplied;
- additive factors remain additive unless comparative evidence exists;
- context-specific factors are not projected into other contexts without support;
- explanatory novelty is not required;
- one grounded episode may be sufficient when paired with an explicit participant-reported recurring self-description;
- a single isolated occurrence still cannot be silently promoted into a person-level recurrence;
- after a rejected synthesis, model-led diagnosis remains available;
- post-proposal evidence timing, participant authority, target-theory blindness, append-only provenance, and the episode-fact/person-pattern firewall are unchanged.

The previous hidden second-pass hypothesis audit is disabled on this adaptive path because it reinforced the same over-interrogation scaffold. Evidence-direction constraints remain directly in the primary interviewer instructions.

## Verification

Implementation: `src/hdmatch/api/life_patterns_v2_owner_reasoning.py` (compatibility entry point retained; now serves the adaptive interviewer).

Focused regression coverage in `tests/unit/test_life_patterns_v2_owner_reasoning.py` verifies:

1. the adaptive planner contains the information-gain stopping rule and no mandatory episode/counterexample quota;
2. a grounded episode plus explicit recurring self-report can surface a person-level proposal;
3. one isolated event cannot silently become recurrence;
4. `I don't know` to a counterexample does not force continued interrogation when the narrow recurring pattern is already supported;
5. rejected-synthesis recovery remains model-led.

Exact verified code head: `26057ea84366bd56c59a0725fe7681c7544d3800`.

GitHub Actions run `34910994811`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy all passed. The immediately preceding run proved all 732 tests passed and failed only on one Ruff style suggestion; the lint-only repair then produced the fully green run.

Existing authenticated owner-only Railway service reused; no new service or access broadening.

- deployment: `f4a8e388-311f-4418-addf-f4291afc1836`;
- source head: `26057ea84366bd56c59a0725fe7681c7544d3800`;
- status: **SUCCESS**;
- application startup complete;
- Railway `/healthz`: HTTP `200`.

Health contract now declares `adaptive_information_gain_gate=true`, `fixed_episode_quota=false`, `mandatory_counterexample_gate=false`, and `hypothesis_support_audit=false`.

## Next decision-changing evidence

Owner retest should evaluate the restored interaction strategy, not another internal assurance layer:

1. Try one deliberately ordinary/simple pattern. The interviewer should stop once the narrow pattern is adequately grounded rather than inventing depth.
2. Try one genuinely nuanced/context-dependent pattern. It should still pursue a distinction when different answers would materially change the formulation.
3. Confirm that `I don't know` or an unobservable distinction is not repeatedly reopened.
4. If a synthesis is wrong, use `No — keep investigating` and judge whether it corrects intelligently without requiring obvious restatement.
5. Then judge `Finish for now` summary utility.

Durable persistence / a real Life Patterns Map remains contingent on owner product judgment. External participants, target-model activity, recruitment, merge/release, broader deployment, and spending remain unauthorized.

**There was never a completion policy.**
