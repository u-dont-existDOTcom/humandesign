# Life Patterns v2 implementation repair 001

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Objective

Repair only `LP-PAN-v2-IMPL-001` from:

`state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-v2-IMPLEMENTATION-SUPERVISOR-REVIEW-2026-09-13.md`

Do not redesign the accepted v2 semantics.

## Required code change

In `src/hdmatch/evaluation/participant_adjudicated_v2.py`, strengthen `validate_adapter_operation_v2` so a declared `episode_fact` output cannot hide a cross-episode derivation.

Resolve the requested projected episode facts. For `aggregate`, `count`, `cluster`, `score`, or `summarize`, reject the operation if its requested episode facts span more than one `episode_id`.

Keep these cases valid:

- `inspect` across multiple episodes;
- a non-inspect combination whose episode facts all belong to one episode;
- a person-level operation based only on accepted resolved patterns under the existing rules.

## Required test change

Extend T006 in `tests/unit/test_participant_adjudicated_v2.py` with a regression case that:

1. builds a projection containing facts from at least two episodes;
2. creates an `AdapterOperationV2` using a non-inspect operation such as `aggregate`, with `output_semantic_level="episode_fact"`, over facts from both episodes;
3. verifies `validate_adapter_operation_v2` rejects it for crossing episode boundaries.

Preserve the existing test that directly rejects episode facts in a declared person-level operation.

## Validation

Start test-efficiency telemetry for this repair if the existing task telemetry cannot be continued cleanly.

Run:

1. focused `tests/unit/test_participant_adjudicated_v2.py`;
2. affected Life Patterns evaluation tests needed for the changed validator;
3. `python scripts/task_preflight.py`;
4. changed-file lint/typecheck or the project-native equivalent;
5. one checkpoint unit suite if the focused/affected results are green.

If the repository-wide checkpoint fails only on an unrelated pre-existing gate, report the exact test and whether this repair changed its source.

## Stop boundary

Commit and push the bounded repair to the same branch, then stop and return:

- start/end SHAs;
- files changed;
- focused/affected/checkpoint results;
- preflight result;
- lint/typecheck result;
- any remaining blocker.

Do not mutate the frozen v2 semantic candidate or independent semantic review artifacts. Follow `tasks/ACTIVE-TASK.json` for all standing authorization boundaries.
