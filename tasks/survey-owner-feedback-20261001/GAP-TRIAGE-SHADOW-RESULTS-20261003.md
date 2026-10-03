# Gap-triage shadow experiment — 2026-10-03

## Goal

Test whether clarification selection can be separated from the expensive full evidence-synthesis pass without lowering reasoning effort. This branch is shadow-only: it does not control participant behavior or mutate Railway review state.

## Privacy boundary

The owner-authorized recovered 81-turn source file was used locally on the owner machine. No participant wording is committed here. Results below contain only source-turn counts, route IDs and aggregate model-call telemetry.

## Legacy production reference

A successful initial full review pass on the same 81-turn class previously required:

- Plan: 390.001 s, 25,788–26,377 prompt-token range in nearby runs, 15,950 completion tokens on the successful pass.
- Admission: 98.154 s, 26,752 prompt tokens, 3,800 completion tokens.
- Successful semantic total: ~488 s (~8m08s).

The legacy planner also emitted 14 evidence items plus 16 addressed-route mappings before returning one clarification candidate. Those deliverable-building outputs are not intrinsically required for the clarification decision.

## Shadow contract

The experimental `GapTriage` stage receives the complete exact behavioral source and eligible route cards but is prohibited from producing:

- an evidence ledger;
- per-turn dispositions;
- a bank-wide addressed-route map;
- a personality summary.

It returns only `review_ready` or up to three materially useful nonredundant clarification candidates. A separate `GapAdmission` stage adversarially checks those candidates against the complete source and can flag one clearly missed material gap.

Both calls used the same `gpt-5.6-sol` / `xhigh` configuration as the legacy review.

## Results

### Run 1

- Source turns: 81
- Triage context: 81,455 chars
- Admission context: 85,118 chars
- Triage: `clarification_needed`
- Proposed route IDs: `M05`, `M11`
- Approved route IDs: `M05`, `M11`
- Independent admission flagged one additional material missed route: `M09`
- GapTriage: 50.175 s, 25,788 prompt tokens, 1,847 completion tokens
- GapAdmission: 20.169 s, 26,551 prompt tokens, 999 completion tokens
- Total semantic wall time: ~70.3 s

### Run 2

- Source turns: 81
- Triage context: 81,455 chars
- Admission context: 85,154 chars
- Triage: `clarification_needed`
- Proposed route IDs: `M05`, `M11`
- Approved route IDs: `M05`, `M11`
- Independent admission again flagged `M09`
- GapTriage: 64.257 s, 25,787 prompt tokens, 2,383 completion tokens
- GapAdmission: 57.162 s, 26,570 prompt tokens, 2,179 completion tokens
- Total semantic wall time: ~121.4 s

## First conclusion

Two independent shadow runs produced the same candidate set and the same independently identified missed route while reducing the clarification-decision semantic wall time from ~488 s to ~70–121 s: about 4.0× to 6.9× faster on this case without lowering model or reasoning effort.

The main latency reduction came from output-contract reduction, not source truncation: prompt size stayed near the legacy range, while completion output fell sharply.

This does **not** yet establish non-inferior clarification quality. Route/wording quality must be compared blind against the legacy reviewer on a replay set before promotion. The experiment currently supports the architectural claim that full evidence synthesis need not sit on the clarification-decision critical path.

These measurements came from the initial prototype committed as `d725c26`. The final branch supersedes that prototype runner/schema with the more strictly independent, privacy-allowlisted implementation in `participant/shadow_triage.py` and `scripts/benchmark_shadow_triage.py`; it does not represent these prototype timings as measurements of the hardened final contract. The final CLI dry-run is tested, but a real semantic replay of the hardened contract remains future work.

## Prior-work map

A bounded research-before-reinvention scan found directly relevant established ideas:

- computerized adaptive testing selects questions adaptively and uses information/precision-based stopping rules rather than arbitrary question counts;
- predicted standard-error reduction is an example of stopping when expected information gain from another item is small;
- adaptive public-opinion and just-in-time assessment work explicitly targets fewer questions while retaining measurement precision;
- incremental information extraction literature reuses prior extraction state and recomputes only material changes rather than reprocessing the full corpus.

Disposition: **compose/adapt**, not invent from scratch. Use information-gain stopping concepts for clarification eligibility and incremental recomputation/provenance concepts for future background evidence coding. The project-specific remainder is preserving exact interview-source provenance and independent semantic admission under ChatGPT action/plugin transport constraints.

## Next experiment

1. Build a replay set from synthetic/development records with planted answered gaps, real unresolved gaps, contradictions and conditions.
2. Compare legacy vs shadow route/question decisions under blinded adjudication.
3. Verify zero accepted redundant questions against full source.
4. Only then test moving evidence coding off the critical path in shadow mode.
5. Keep incremental per-turn/batched ingestion as a plugin-oriented transport experiment; do not add dozens of Custom GPT Action approvals.
