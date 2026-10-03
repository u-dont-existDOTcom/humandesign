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

## Planted nonredundancy replay

Three additional **private local** replay variants appended one synthetic noncanonical Q&A that clearly answered one baseline candidate's neutral distinction. The synthetic wording and the owner's source were not committed; only route-level outcomes are recorded.

- **M05 answered in source** → triage proposed `M11`, `M09`; admission approved both; `M05` was not proposed. Total semantic wall time ~97.4 s.
- **M11 answered in source** → triage proposed `M05`, `M09`; admission approved both; `M11` was not proposed. Total semantic wall time ~118.5 s.
- **M09 answered in source** → triage proposed `M05`, `M11`; admission approved both; `M09` was not proposed. Total semantic wall time ~149.8 s.

This is a useful first adversarial check: each planted equivalent answer suppressed exactly the route it was designed to make redundant even though the appended turn had **no canonical route ID**, so the exclusion came from semantic full-source review rather than the deterministic presented-route filter.

Across five shadow runs so far (two baseline repeats + three planted-answer variants), the clarification decision remained well below the ~488 s legacy successful initial pass, with no reduction in model or reasoning effort.

Still missing before promotion: planted unsupported-premise/context cases, conditional/correction cases, review-ready cases, and blinded quality adjudication against the legacy question choice.

## Hardened lean-contract replay — 2026-10-03

The earlier hardened shadow contract was re-run semantically on the same private 81-turn owner source, then simplified to remove producer-side source citations/defect labels and to give compact route cards to triage while reserving full route controls for independent admission.

Privacy-safe result:

- complete behavioral source turns: 81
- eligible routes: 69
- triage context: 77,702 chars
- admission context: 39,294 chars
- triage proposed: `M11`, `M09`, `M05`
- independent admission retained: `M11`, `M05`
- `M09` was rejected under `already_answered` / `low_information_gain`
- GapTriage: 72.012 s, 25,269 prompt tokens, 3,895 completion tokens
- GapAdmission: 40.011 s, 17,121 prompt tokens, 1,317 completion tokens
- total semantic wall time: 112.023 s (~1m52s)

For comparison, the successful legacy initial Plan+Admission on this owner review took ~488.155 s (~8m08s), so the lean shadow decision was about 4.36x faster without lowering model or reasoning effort.

A privacy-safe read of the actual legacy review history shows that its **first canonical clarification route was also `M11`**. That is one real-case route-choice agreement between the lean shadow and legacy pipeline. The later legacy history used an `M11` missing-piece follow-up and then another route, which is consistent with the owner's complaint that the sequential endgame can create avoidable wait cycles.

This is useful but still not sufficient for promotion. One owner case cannot establish non-inferiority. The next quality gate remains a synthetic/development replay set with planted redundant, unsupported-premise, conditional/correction, dependent-follow-up and review-ready cases under blinded adjudication.

### Output-contract finding

The same xhigh model/source class now has three useful points:

- legacy full Plan+Admission: ~488 s, initial planner ~15,950 completion tokens;
- hardened verbose shadow: ~222 s, triage ~7,113 completion tokens;
- hardened lean shadow: ~112 s, triage ~3,895 completion tokens.

The direction is consistent: preserving complete source and xhigh reasoning while shrinking the **required output contract** materially reduces participant-facing latency. The remaining optimization target is question-selection quality, not weaker reasoning.

## Hardened final-contract semantic replication — later 2026-10-03

The final privacy-hardened benchmark CLI was then run semantically on the same private 81-turn owner source. This closes the earlier provenance gap where only the prototype/lean variants had semantic timing.

Privacy-safe result:

- complete behavioral source turns: 81
- eligible routes: 69
- triage context: 105,479 chars
- admission context: 39,982 chars
- triage proposed routes: `G15`, `M11`, `M09`
- independent admission retained only: `M11`
- triage rejection counts across the candidate review: 2 `already_answered`, 2 `low_information_gain`
- GapTriage: 177.302 s, 30,904 prompt tokens, 7,113 completion tokens
- GapAdmission: 45.012 s, 17,278 prompt tokens, 1,605 completion tokens
- total semantic wall time: 222.314 s (~3m42s)

This final hardened contract is slower than the lean prototype but still ~2.20x faster than the ~488 s legacy initial Plan+Admission, with the same `gpt-5.6-sol` / `xhigh` reasoning configuration and complete source retained.

A privacy-safe read of the actual legacy review establishes that its first clarification was canonical route `M11`; the hardened final shadow also selected `M11`. The live review then used an `M11` missing-piece follow-up and later a different canonical route, which is evidence against an arbitrary one-question cap: later clarification can be semantically distinct even when tied to the same route family.

The benchmark therefore now supports two separate claims:

1. clarification triage can be materially faster than full evidence synthesis without truncating source or lowering reasoning effort;
2. output/schema hardening itself has latency cost, so the next experiment should optimize the hardened contract rather than rely on the fastest prototype number.

It still does not establish general non-inferiority; the replay/adjudication gate remains required before any live replacement.

## Synthetic quality replay — later 2026-10-03

Five synthetic/development cases exercised distinct failure and eligibility classes without using or committing participant wording:

- **True unresolved M11** → triage proposed `M11`; independent admission retained `M11`; ~27.0 s total.
- **Semantically answered M11** → `review_ready`; no admission call needed; ~8.0 s.
- **Dependent PREFER-EXCHANGE with valid M11 antecedent** → triage proposed and admission retained `PREFER-EXCHANGE`; ~29.0 s.
- **PREFER-EXCHANGE without its required M11 antecedent** → route was deterministically ineligible and triage returned `review_ready`; ~8.0 s.
- **Correction case where later source superseded the apparent negotiation preference** → triage returned `review_ready`; ~6.0 s.

These cases add evidence for nonredundancy, context/antecedent gating, dependent-follow-up eligibility and later-source correction handling. They remain development fixtures, not participant-validation evidence.

The remaining promotion gap is narrower: add an explicit unsupported-premise candidate/refutation case, a condition-preservation case where a clarification remains useful only under a stated condition, and an independent blind adjudication comparing legacy versus shadow choices across the replay set.

### Edge replay follow-up

- A deliberately malformed M11 follow-up inserted an unsupported premise that the respondent had said they would pressure the friend until agreement. Independent GapAdmission rejected it and emitted the expected bounded failure classes, including `unsupported_premise`, `wrong_antecedent`, `context_not_supported`, `low_information_gain` and `unsupported_extension`; ~17.0 s.
- A deliberately conditional `PREFER-EXCHANGE` source said continued negotiation would depend on why the friend objected, without naming the deciding conditions. GapTriage returned `review_ready`; ~16.0 s. This case is **not counted as a pass yet** because whether the missing condition is materially worth clarifying is a semantic judgment. It is reserved for blind adjudication rather than being relabeled after seeing the model output.

That leaves blind adjudication as the next quality discriminator rather than more ad-hoc prompt tuning.

## Synthetic semantic quality checks — 2026-10-03

A separate fully synthetic targeted benchmark isolated specific clarification behaviors by marking all irrelevant routes already addressed. No participant source was read for these cases.

Seven targeted outcomes were tested with `gpt-5.6-sol` / `xhigh`:

- unresolved `M11` value-exchange distinction → `M11` proposed and independently admitted; ~27 s;
- a noncanonical synthetic answer that already resolved `M11` → no admitted clarification; independent admission rejected the proposed repeat as already answered / low-information; ~77 s in the repeat run;
- an answered `M11` antecedent with genuinely unresolved preferred-use distinction → `PREFER-EXCHANGE` proposed and admitted; ~22 s on the refined rerun;
- `PREFER-EXCHANGE` without its required `M11` antecedent → no eligible route and `review_ready`; ~8 s;
- a synthetic answer followed by an explicit correction resolving the exchange preference → `review_ready`; ~8 s;
- `WORK-RECOVERY` with a `G15` antecedent explicitly reporting no tiredness/depletion → `review_ready`, correctly rejecting the probe's tiredness premise; ~7 s;
- two independent unresolved self-contained routes (`M05` + `M11`) → both proposed and independently admitted in one batch; ~43 s.

The first `PREFER-EXCHANGE` synthetic wording accidentally implied enough willingness to continue the negotiation that the model judged the probe already answered. The fixture was corrected to leave that preference genuinely unresolved, and the targeted rerun then selected/admitted `PREFER-EXCHANGE`. This is test-fixture repair rather than treating a sensible model decision as failure.

This is not yet a full blind non-inferiority study, but it adds direct semantic checks for true unresolved gaps, semantic redundancy without canonical IDs, antecedent gating, unsupported-premise rejection, correction handling, and multi-question batching. The synthetic benchmark is reproducible from `scripts/benchmark_shadow_synthetic_quality.py` and contains no private source.

## Legacy-vs-shadow synthetic comparison

The unchanged legacy Plan+Admission pipeline was then run on the same seven synthetic cases with the same `gpt-5.6-sol` / `xhigh` configuration. This gives a direct development comparison rather than judging the shadow only against hand-written expectations.

Privacy-safe outcome comparison:

- unresolved `M11`: both legacy and shadow selected `M11`;
- semantically redundant `M11`: **legacy still selected `M11`**, while the shadow's independent admission rejected the repeat as already answered / low-information;
- antecedent-supported `PREFER-EXCHANGE`: both selected `PREFER-EXCHANGE` after the refined synthetic answer;
- missing `PREFER-EXCHANGE` antecedent: both reached review-ready/no question;
- explicit correction resolving exchange preference: both reached review-ready/no question;
- unsupported `WORK-RECOVERY` tiredness premise: both reached review-ready/no question;
- two independent unresolved routes `M05` + `M11`: legacy selected only `M05` because its live contract is single-question, while shadow proposed and independently admitted **both** in one batch.

Legacy semantic wall times on these route-isolated synthetic cases were approximately 25–76 s per case. The key result here is qualitative rather than latency: the shadow did not lose the useful route choices the legacy made, rejected one redundant question the legacy still asked, and exposed the intended independent batching advantage. These fixtures remain development evidence rather than a substitute for broader blind replay/adjudication.

The legacy comparison is reproducible from `scripts/benchmark_legacy_synthetic_quality.py`; it reads only the committed synthetic fixtures and produces route/timing metadata.

## Dependent clarification sequence

A separate synthetic two-step replay verified the boundary that independent batching must not cross. With only `M11` and its dependent `PREFER-EXCHANGE` route left unresolved:

1. Before any `M11` answer existed, only `M11` was eligible and admitted; `PREFER-EXCHANGE` was not batched prematurely. Semantic time: ~27.0 s.
2. After appending a synthetic canonical `M11` answer that deliberately left preferred negotiation use unresolved, `PREFER-EXCHANGE` became eligible and was admitted on the next pass. Semantic time: ~24.0 s.

This matches the intended batching rule: independent gaps can be returned together, but a follow-up whose usefulness depends on a new answer waits for that answer. The sequence is reproducible from `scripts/benchmark_shadow_dependency_sequence.py` and contains no participant source.
