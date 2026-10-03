# Independent review latency redesign — 2026-10-03

## Owner correction

The end-of-interview workflow should not trade scientific intelligence for a shorter UX by imposing an arbitrary one-clarification cap. The owner also proposed shifting work earlier: append answers to Railway during collection so candidate clarification gaps can be prepared incrementally and reconciled quickly at the end.

## Privacy-safe measured runtime evidence

No participant text is recorded here. The existing encrypted owner-pilot review receipts expose only stage/token/time metadata.

Successful initial clarification-selection pass:
- Plan: 390.001 s, 26,377 prompt tokens, 15,950 completion tokens, xhigh.
- Admission: 98.154 s, 26,752 prompt tokens, 3,800 completion tokens, xhigh.
- Total semantic wall time: ~488 s (~8m08s).

Later clarification passes on the same review:
- round 1: 40.911 + 25.149 + 41.008 + 24.116 = ~131 s (~2m11s), including one rejected/repair pair.
- round 2: 40.506 + 21.071 = ~61.6 s (~1m02s).

The former 15-minute participant check-back interval was therefore conservative UX, not an intrinsic requirement. It especially overstates post-clarification latency.

Privacy-safe plan-shape telemetry also showed that the successful initial planner emitted 14 evidence items and 16 addressed-route mappings before selecting one clarification question; earlier rejected plans emitted 22–24 evidence items and 17–18 addressed-route mappings. That deliverable-building work is coupled to clarification selection even though it is not required to decide the question.

## Independent Claude review

Claude Sonnet (high) and Claude Opus (xhigh) were asked to inspect the repository read-only and challenge the architecture. Neither saw participant text. Both independently converged on the same findings:

1. The expensive bulk Plan combines distinct jobs: full evidence coding, dispositions, route-address mapping, source-completeness attestation and next-question selection.
2. Full evidence coding is not intrinsically required to decide whether a clarification is needed. It belongs after the clarification set is settled or off the participant-facing critical path.
3. The one-round clarification cap is not justified by the frozen information-based stopping rule and can reduce quality. The relevant scarce resource is remote round trips/participant burden, not an arbitrary question count.
4. A rejected plan currently causes too much regeneration. Approved or reusable work should survive targeted repair.
5. Phase-blind waiting guidance is wrong: initial full-source work and later delta work have very different measured runtimes.
6. Incremental/background coding is architecturally sound if provisional analysis never feeds back into ordinary collection before saturation and final global reconciliation remains authoritative.

Opus additionally noted that the current worker creates a JSON schema file for Codex structured output but does not appear to pass it via --output-schema; this is a separate reliability candidate to verify before changing.

## Corrected immediate policy

Until the pipeline is redesigned:
- restore the frozen protocol's information-based stopping rule;
- no hard one-clarification cap;
- another clarification is allowed only when independently admitted as admissible, nonredundant and materially useful;
- coverage alone never justifies another question;
- use phase-aware check-back guidance: about 10 minutes for the initial current pipeline and about 3 minutes after a clarification unless the service returns a better interval.

This is a rollback of an assistant-added requirement, not a new scientific rule.

## Target architecture

Separate the endgame into three concerns.

### A. Clarification triage — participant-facing critical path

A dedicated Gap/Triage model call reads the complete exact source plus eligible route authority, but outputs only:
- review-ready vs clarification-needed;
- a small ranked set of materially useful unresolved questions;
- route ID, exact wording, antecedents and minimal support/nonredundancy references;
- defect flags such as contradiction, missing condition or unanswerable context.

It does **not** emit the full evidence ledger, all unassessed dispositions or a bank-wide addressed-route map.

A separate adversarial GapAdmission call verifies only the candidate questions against the exact source and frozen admission gates. Prefer refutation: already answered, unsupported premise, wrong antecedent, non-discriminating or low information gain.

The current real timing provides a useful feasibility signal: later xhigh Plan calls with ~23k input but only ~1.3k output completed in ~41 s, versus ~390 s when the initial Plan emitted ~16k output tokens. Therefore cutting the output contract, not merely compressing the input, is the highest-value latency experiment.

### B. Evidence synthesis — off the clarification critical path

Evidence coding can run after triage, in parallel with participant response time, or incrementally:
- extract exact-quote evidence candidates in bounded windows;
- deterministic exact-quote validation;
- independent item-level semantic admission;
- preserve corrections/conditions and invalidate affected provisional items;
- never require this full ledger to exist before the triage question is returned.

At finalization, perform a global reconciliation that outputs only amendments/conflicts/merges rather than regenerating all evidence.

### C. Information-based clarification stopping

Do not use a question-count cap as the scientific stopping rule.

A clarification is eligible only if its answer could materially change a currently unresolved evidence conclusion, route interpretation or contradiction and the question independently passes nonredundancy/context/admission checks.

For UX, reduce round trips rather than intelligence:
- triage can return multiple **independent** clarification candidates in one remote pass;
- candidates that depend on another clarification answer must wait for that answer;
- batch answer submission can reduce approval cards;
- if a safety/UX ceiling is ever introduced, reaching it must be recorded as an unresolved/budget-truncated state rather than natural saturation.

## Owner's incremental-streaming idea

### Semantic architecture: yes

Append-only per-turn analysis is a good fit:
- exact turn is immutable source;
- provisional evidence/gap candidates are keyed to source-turn IDs/hashes;
- later corrections invalidate affected candidates;
- later answers can resolve earlier provisional gaps;
- final global reconciliation over the complete exact source remains authoritative;
- provisional reviewer outputs are hidden from the live collector until saturation, preserving independence.

### Current Custom GPT: transport makes per-answer streaming unattractive

Each external Action may show an Allow card. Per-answer writes would turn a long interview into dozens of approval prompts and add new failure/replay surfaces.

Near-term options, in preferred order:
1. first split fast gap triage from full evidence coding — no extra participant approvals;
2. only if end latency remains too high, test one mid-interview append-only checkpoint at a natural break;
3. do not silently relabel research-data writes nonconsequential merely to suppress approval UX.

### Plugin: design for incremental ingestion

Build the backend now around transport-agnostic append-only turns so the future plugin can use the same semantics. In a private plugin prototype, measure whether installed-app permissions make batched/per-turn writes tolerable.

If they do:
- batch roughly several turns rather than requiring one network write per answer;
- background-code provisional evidence/gaps while the participant continues talking;
- expose a persistent review-status surface;
- reconcile globally at saturation;
- keep final source snapshot/hash authoritative.

If plugin approval UX remains intrusive, the same backend still supports periodic batches or end-only triage.

## Staged implementation

0. **Measure first.** Add visible-output/reasoning/cache/queue telemetry where available and retain privacy-safe per-stage timing.
1. **Restore protocol fidelity.** Remove the one-clarification cap and use phase-aware check-back intervals.
2. **Remove low-value output from the current Plan.** Stop emitting implicit unassessed dispositions and bank-wide addressed-route bookkeeping when not needed for the chosen action.
3. **Targeted repair.** Preserve admitted items; on question rejection repair/re-rank the question instead of regenerating the whole evidence ledger.
4. **Shadow Gap/Triage pipeline.** Run the new tiny-output clarification selector alongside the legacy pipeline without controlling participant behavior. Compare selected route/question and latency.
5. **Promote triage if non-inferior.** Require no rise in redundant/unsupported questions and large latency reduction.
6. **Move evidence synthesis off critical path.**
7. **Prototype incremental plugin ingestion.**

## Acceptance targets for the shadow redesign

Before promotion, on synthetic/development replay records:
- median time to clarification decision <= 3 minutes for 81-turn-class inputs; target <= 2 minutes if observed;
- p90 <= 5 minutes;
- clarification route/wording quality non-inferior to legacy under blind adjudication;
- zero admitted questions already answered in the complete source;
- 100% deterministic source-quote exactness for evidence;
- no loss of corrections, conditions or counterexamples;
- rejected clarification candidates do not force regeneration of already admitted evidence;
- no participant data in timing/diagnostic logs.

The purpose is to reduce unnecessary work and latency, not reasoning quality.

## Shadow implementation receipt — 2026-10-03

Stage 4 now has a development-only implementation in `participant/shadow_triage.py` and `scripts/benchmark_shadow_triage.py`. Gap/Triage reads the complete exact behavioral source plus eligible frozen route authority and emits at most three ranked question candidates. A fresh GapAdmission call receives the complete source, the selected route controls, and only the candidate fields needed for refutation; it does not receive the producer's verdict, defect labels, or claimed material effect. Deterministic validation enforces source references, route authority, candidate ordering/dependencies, exact admission gate/failure-code agreement, and triage-ranked selection.

The benchmark persists only ordinal case IDs, counts, route IDs, bounded rejection codes, token counts, and timing. It excludes participant text, source-turn IDs, paths, prompts, raw model output, exception text, and content-derived hashes, and writes mode 0600. It supports a no-model dry run and optional strict privacy-safe legacy comparison. The experiment is not imported by the participant engine, HTTP API, queued review worker, deployment entry point, or Custom GPT bundle, so it does not control live behavior.

Local verification: 14 focused tests pass; affected Ruff checks pass; 127 participant tests pass. One additional participant assertion has a proven parent-baseline failure because the committed `getLifePatternsReview` OpenAPI description is 314 characters against its existing 300-character test cap; neither file is changed here. Two earlier prototype shadow runs are preserved in `GAP-TRIAGE-SHADOW-RESULTS-20261003.md`; the hardened final CLI was not rerun semantically. The latency/non-inferiority promotion targets above therefore remain unevaluated for the final contract.
