# Independent review context-budget incident — 2026-10-02

## Observed result
The recovered 81-turn owner candidate queued successfully under the previously recovered review handle. Railway later returned `resource_limited` with `model_context_budget_exceeded`. No clarification or review summary was admitted; source-review status remains pending.

## Failure classification
This is an execution/context-boundary failure, not semantic or scientific evidence. The existing review identity and exact unfrozen source remain authoritative. Do not freeze, ask CF-003, or create a replacement review.

## Diagnosis
The imported-source planner already uses a 110,000-character guard and passes the complete imported source to both semantic passes. The second independent-admission payload can grow substantially because it reattaches every source turn plus the planner proposal and full route-control cards for every route the planner marks addressed. That duplicated route-control material is not needed at full fidelity for addressed-only routes.

The owner source was used only for privacy-safe sizing on the owner machine; no participant text is committed here. A reconstructed source-preserving candidate produced a planner context below the existing 110,000-character guard, making the later admission-composition boundary the supported repair target.

## Recurrence after first repair — 2026-10-03
The same review was retried after the first admission-context compaction and again returned `resource_limited / model_context_budget_exceeded`. Privacy-safe inspection of the encrypted saved review showed the real sequence: the first planner and admission model calls both completed successfully; independent admission then rejected the proposal, and the engine attempted its protocol-authorized repair pass. The repair pass appended the entire rejected planner object to the already-large 81-turn planner context, pushing that next planner request over the 110,000-character guard before the second planner call could run.

This explains why the first repair reduced the admission payload substantially but did not change the final status. The recurring failure was at the **repair-composition boundary**, not the initial planner or independent-admission model call.

## Second repair
- Preserve all exact source turns in both semantic passes.
- Preserve the full proposed next-question route controls.
- For addressed-only routes in the admission pass, use the same compact route card the planner saw rather than duplicating full interpretation/context-binding/live-guard prose.
- Omit only planner-emitted `unassessed` disposition objects that carry no conditions/process-feedback; under `source_review_complete`, omitted imported turns deterministically become unassessed already.
- Preserve all emitted evidence and addressed-route source bindings.
- On a rejected semantic proposal, do **not** append the entire rejected plan to the next planner request. Reattach the complete source/routes/guide and pass only a bounded rejected-plan identity summary plus the bounded repair instruction.
- Record a privacy-safe repair-projection telemetry marker so another recurrence can be located without exposing participant text or model output.
- Permit `retry` on the **same review ID** after a resource-limit repair, resetting only the worker execution phase from `resource_limited` to `ready`; do not create a new review.

## Live validation after second repair — 2026-10-03
The same existing review was retried after the repair-pass bound was deployed. It crossed the previous failure boundary: planner 1 completed, admission 1 completed, the bounded repair projection remained below the context guard, planner 2 completed, and admission 2 completed. The resulting status changed from `resource_limited / model_context_budget_exceeded` to `error / question_or_evidence_admission_not_resolved`.

That is evidence that the context-budget defect is repaired. The remaining blocker is now a genuine semantic-admission disagreement after both protocol-authorized proposals, not another transport/context overflow.

A privacy-safe diagnostics follow-up records only proposal shape and admission booleans/error classes—never participant text, model prose, source quotes, or the private review handle—so the semantic rejection can be located without exposing the review content.

## Acceptance
Synthetic large-import regression must show every exact source turn retained, all addressed route IDs retained, semantic evidence unchanged, and the compact admission payload under the configured guard where the prior composition exceeded it. A separate reject-once regression must force independent admission to reject the first large bulk proposal, then prove the second planner call remains under the 110,000-character guard and can complete the same review. Existing ordinary review/clarification/submission tests must remain green.

## Retry-budget recurrence — 2026-10-03

After the repair-context fix was deployed, the same review successfully crossed the formerly failing repair boundary: two planner calls and two independent-admission calls all ran, and both repair-context projections stayed below the 110,000-character guard. The remaining outcome was semantic admission unresolved after the protocol-authorized repair, not another context overflow.

A subsequent diagnostic retry then stopped immediately as `resource_limited / study_model_call_limit_reached`. This was a separate state-machine defect: the explicit operator retry preserved historical Plan/Admission telemetry (correct for audit) but the call guard counted those old attempts against the new repaired execution epoch. The retry therefore had no usable call budget.

Repair: retain the complete historical call ledger, but when `controlLifePatternsReview(action=retry)` is explicitly invoked after a repaired `error` or `resource_limited` state, store the current semantic-call count as `model_call_budget_baseline`. The Engine counts only calls after that baseline against the existing per-epoch maximum. This does not increase the automatic retry count: another epoch still requires the existing explicit retry control after the underlying error is repaired.

## Semantic-admission recurrence — 2026-10-03

After the context and retry-budget defects were removed, privacy-safe saved-state telemetry showed the remaining rejection shape without exposing participant text or model prose. Both proposals selected the same next route, and the reviewer independently marked the next question context-supported and nonredundant and confirmed the complete imported-source review. The whole plan still failed because the planner proposed a large evidence set plus many addressed-route mappings and the reviewer judged some extensions unsupported and some route-address mappings insufficiently supported. The repair proposal reduced the counts but reproduced the same global failure.

This identified a composition defect: optional evidence coding and route-address bookkeeping were coupled to the admission of an otherwise acceptable next action. One overbroad optional item could invalidate the whole source review.

Repair:
- Extend the independent admission result with explicit approved evidence IDs and approved addressed-route IDs.
- Treat evidence items and route-address mappings as independently admissible: retain only IDs the reviewer approves; never convert a rejected optional item into evidence or addressed-route state.
- Keep the action/question gates strict. `approved`, context support, nonredundancy, and unsupported-extension checks now judge the next action after unapproved optional items are dropped.
- Require at least one independently admitted source-grounded evidence item before a complete recovered import can leave the bulk-review phase.
- Keep the complete recovered import in later planner and reviewer contexts for nonredundancy checks, so correctness no longer depends on every historical route being preclassified as addressed during one large pass. Old imported turns remain ineligible as *new* evidence on later turns; they are reattached only as authoritative context.
- On each explicit retry after an operator-side repair, preserve the full historical call ledger but move the call-budget baseline to the current ledger length and increment the bounded execution epoch.

Acceptance adds partial-admission tests: a plan containing one supported and one unsupported evidence/address item must continue with only the supported subset, and post-import clarification planning/review must reattach the complete recovered import while staying under the large-source context guard.

## Live validation after item-level admission repair — 2026-10-03

The same existing owner review was retried after the item-level admission repair was merged and deployed to both Railway and the local independent-review worker. No replacement review was created and the candidate remained unchanged.

The review advanced to `clarification_needed` with no error. The independent source-review status remains pending until that admitted clarification is answered. The returned clarification is canonical route `M11`; the private clarification handle and private review handle are intentionally not committed.

This live result crosses all three previously observed blockers on the same saved review: context budget overflow, repaired-retry budget exhaustion, and whole-plan semantic admission deadlock. It does not by itself complete independent review; completion still requires the participant's exact answer to the admitted clarification and the subsequent review round.
