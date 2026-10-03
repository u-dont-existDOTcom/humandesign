# Independent review context-budget incident — 2026-10-02

## Observed result
The recovered 81-turn owner candidate queued successfully under the previously recovered review handle. Railway later returned `resource_limited` with `model_context_budget_exceeded`. No clarification or review summary was admitted; source-review status remains pending.

## Failure classification
This is an execution/context-boundary failure, not semantic or scientific evidence. The existing review identity and exact unfrozen source remain authoritative. Do not freeze, ask CF-003, or create a replacement review.

## Diagnosis
The imported-source planner already uses a 110,000-character guard and passes the complete imported source to both semantic passes. The second independent-admission payload can grow substantially because it reattaches every source turn plus the planner proposal and full route-control cards for every route the planner marks addressed. That duplicated route-control material is not needed at full fidelity for addressed-only routes.

The owner source was used only for privacy-safe sizing on the owner machine; no participant text is committed here. A reconstructed source-preserving candidate produced a planner context below the existing 110,000-character guard, making the later admission-composition boundary the supported repair target.

## Repair
- Preserve all exact source turns in both semantic passes.
- Preserve the full proposed next-question route controls.
- For addressed-only routes in the admission pass, use the same compact route card the planner saw rather than duplicating full interpretation/context-binding/live-guard prose.
- Omit only planner-emitted `unassessed` disposition objects that carry no conditions/process-feedback; under `source_review_complete`, omitted imported turns deterministically become unassessed already.
- Preserve all emitted evidence and addressed-route source bindings.
- Permit `retry` on the **same review ID** after a resource-limit repair, resetting only the worker execution phase from `resource_limited` to `ready`; do not create a new review.

## Acceptance
Synthetic large-import regression must show every exact source turn retained, all addressed route IDs retained, semantic evidence unchanged, and the compact admission payload under the configured guard where the prior composition exceeded it. Existing ordinary review/clarification/submission tests must remain green.
