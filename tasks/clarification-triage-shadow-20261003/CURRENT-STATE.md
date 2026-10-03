# Shadow clarification triage experiment — current state

- Task: `experiment-gap-triage-shadow-20261003`
- Branch: `experiment-gap-triage-shadow-20261003`
- Parent baseline: `2053e58`
- Status: local implementation and verification complete; commit/push/ref verification pending
- Assurance lane: iteration, with privacy/no-live-change hard gates
- Authority: owner request plus `tasks/survey-owner-feedback-20261001/INDEPENDENT-REVIEW-LATENCY-REDESIGN-20261003.md`
- Preflight: `python3 scripts/task_preflight.py`
- Completion command: `PYTHONPATH=apps/life-patterns-participant python -m pytest apps/life-patterns-participant/tests -q`

## Required outcome

Add a development-only two-call clarification triage and adversarial admission path, plus a benchmark CLI whose persisted report and console receipt contain only privacy-safe aggregate/route metadata. Do not connect the experiment to the live participant engine, review worker, HTTP API, deployment, or Custom GPT bundle.

## Implemented

1. `participant/shadow_triage.py` contains strict small-output triage and adversarial admission schemas, complete exact behavioral-source contexts, frozen-route controls, deterministic validators, and a non-mutating two-call runner.
2. `scripts/benchmark_shadow_triage.py` supports private replay records, no-model dry runs, optional strict legacy comparisons, and mode-0600 privacy-safe reports/receipts without participant text, source IDs, input paths, prompts, raw output, exception text, or content-derived hashes.
3. `tests/test_shadow_triage.py` covers complete-source propagation, independent admission projection, no-mutation/shadow isolation, rank/dependency/gate validation, all-rejected and review-ready outcomes, 81-turn-class input, privacy-safe CLI output, strict legacy loading/comparison, and absence from live surfaces.
4. The README documents the shadow-only boundary and safe dry-run command. No live engine, API, review-worker, deployment, provider, or Custom GPT file changed.

## Verification

- Focused shadow suite: `14 passed`.
- Ruff check and format check on all three new Python files: pass.
- Complete participant suite: `127 passed, 1 failed`; the sole failure is a parent-baseline mismatch in `test_action_schema_privacy_and_description_limits` because the committed `getLifePatternsReview` OpenAPI description is 314 characters while the existing cap is 300. This experiment did not change the live schema or that test.
- Participant suite excluding that proven baseline-only assertion: `127 passed, 1 deselected`.
- Semantic replay: the concurrent prototype commit preserved two privacy-safe private-source shadow runs (about 70.3 s and 121.4 s) in `tasks/survey-owner-feedback-20261001/GAP-TRIAGE-SHADOW-RESULTS-20261003.md`. The hardened final CLI was not rerun semantically; its dry-run path was exercised by tests. No paid Venice/API inference was used.
- Remaining task work: commit, push `experiment-gap-triage-shadow-20261003`, and verify the remote ref. Do not merge.

## Suspended competing sources

The parent hybrid-voice task state, global research roadmap, unrelated worktrees, deployment, merge, paid inference, and participant activation do not select work in this experiment branch.
