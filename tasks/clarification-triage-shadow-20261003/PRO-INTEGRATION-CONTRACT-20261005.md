# Integration contract after the owner-authorized Pro review

## Outcome and authority

Use the repaired fast clarification stage to reduce the participant's initial end-review wait without reducing configured reasoning effort, dropping material clarifications, or treating missing coverage as a reason to ask. The owner's Pro-instead-of-Claude instruction replaces that pending reviewer only; it is not evidence that a live integration or deployment occurred.

Reviewed code commit: `a39228f89c12a3a03742efd5b067a7477dffadc2`.
Branch: `pro/gap-triage-review-20261005`.
Canonical review: `tasks/clarification-triage-shadow-20261003/PRO-REVIEW-20261005.md`.

Do not revive the superseded Claude-quota wait or restart the long synthetic-version campaign. Preserve the old failures and the new executable regressions. Keep the original slow reviewer available during reversible pilot integration.

## Preparation

Fetch the published review branch, reconcile it against the actual current live integration branch, and use a new isolated worktree. Do not merge the entire experimental history into a deployment branch without checking its unrelated task/state changes. The useful production delta is the reviewed clarification implementation and its tests; experiment reports are supporting provenance.

Existing executable verification:

```sh
PYTHONPATH=apps/life-patterns-participant .venv/bin/python -m pytest apps/life-patterns-participant/tests -q
.venv/bin/python -m ruff check apps/life-patterns-participant/participant/shadow_triage.py apps/life-patterns-participant/scripts/replay_shadow_validation.py apps/life-patterns-participant/tests/test_shadow_triage.py apps/life-patterns-participant/tests/test_shadow_triage_pro_review.py
```

The current scripts are development harnesses, not deploy commands. Resolve the production branch, deployed worker configuration, service and current release requirements from the live repository/runtime before changing them.

## Required adapter behavior

1. Integrate at the existing review worker boundary, `apps/life-patterns-participant/scripts/gpt_review_worker.py::run_review`, preserving exact source preparation, consent, target-information exclusions, pause/withdraw/stop handling and existing source identity checks.
2. Consume only `final_questions` / `ready_question_route_ids` as deliverable questions. `admitted_route_ids` proves a gap was admitted, not that wording is ready. A render failure, admission disagreement or pending audit must never become `ready` or freeze eligibility.
3. Treat `final_review_completed: false` literally. Fast triage is not full evidence synthesis. Keep the complete final review/final submission gates until their actual required work is done.
4. Persist deferred omission work bound to the exact candidate/source version. Detection results are proposals: recovered questions still require complete-source independent admission. Reconcile after new answers; do not apply a stale audit or stale question batch to a changed record.
5. Preserve independently useful questions and dependencies. The current API supports one clarification, so do not silently call a shadow three-question batch a working one-Action answer flow. Any batch extension must version both server and GPT transport, retain exact answers/skips and order, and be idempotent across retries. New answers can invalidate a queued question; refresh or reconcile it rather than blindly asking stale wording.
6. Keep the interviewer separate from provisional review while the interview is underway. No per-answer Action calls or streaming checkpoints are introduced by this review.
7. Keep participant-data and control writes consequential. The read-only status permission experiment remains separate from fast-review correctness; no persistent-permission claim is established here.

## Release boundary

Before live enablement, exercise the actual adapter through start, usable clarification, answer/skip, resume/retry, stale result, cancellation/withdrawal, no-question completion and final synthesis. Run affected integration tests and applicable existing release/rollback checks against the exact deployment candidate. These verify the new adapter; they are not a requirement for another model-review tournament.

Only after the backend is deployed and read back should a replacement GPT package advertise that behavior. Keep the install version, Action schema, backend capability and wait guidance consistent. Do not tell the owner that updating the old GPT ZIP alone activates the fast stage.

## Current handoff status

Pro review and shadow repairs are complete. No live adapter, deployment, batch-answer API or new GPT ZIP has been claimed as completed. The next engineering task is this integration, not obtaining Claude approval. The parent product outcome remains open until the participant can use the deployed flow.
