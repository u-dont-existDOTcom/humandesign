# Life Patterns v2 implementation supervisor review — 2026-09-13

implementation_reviewed: `122d906dc416948c36910b40d442d5a913928767`
semantic_candidate_head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
semantic_review: PASS
implementation_verdict: BLOCKED
semantic_change_required: false
implementation_blocking_findings: 1

## Scope

Reviewed only the bounded v2 implementation introduced by the implementation worker:

- `src/hdmatch/evaluation/participant_adjudicated_v2.py`
- `tests/unit/test_participant_adjudicated_v2.py`

The frozen v2 semantic candidate remains accepted. This review does not reopen or mutate the semantic contract.

## What is correctly implemented

The implementation materially enforces T001–T005 and most of T006:

- genuine factual nonoccurrence is routed through the four-gate absence path by a required theory-blind semantic callback;
- evidence acquisition phase cannot be reset for the same fact/thread across revisions;
- terminal proposal grounding is semantically revalidated against current admissible factual anchors;
- fact correction history is append-only, monotonic, nonbranching, provenance-bound, and only the current leaf projects;
- fact-specific qualification survives freeze and projection;
- rejected/unresolved patterns do not enter the accepted-pattern projection;
- person-level adapter operations cannot directly name episode facts;
- freezes are canonical/content-addressed and raw narrative/source-resolver capability is absent from the projection.

## Blocking finding

### LP-PAN-v2-IMPL-001 — cross-episode aggregation can bypass the person-level firewall by mislabeling its output

**Location**

`AdapterOperationV2` and `validate_adapter_operation_v2` in `src/hdmatch/evaluation/participant_adjudicated_v2.py`; T006 in `tests/unit/test_participant_adjudicated_v2.py`.

**Literal failure mode**

The Pydantic model rejects episode facts when `output_semantic_level == "person_level_pattern"`, but an adapter can instead submit an operation such as `aggregate`, `count`, `cluster`, `score`, or `summarize` over facts from multiple distinct episodes while declaring `output_semantic_level == "episode_fact"`. `validate_adapter_operation_v2` currently verifies only that referenced IDs exist, so this cross-episode operation is admitted.

The frozen v2 contract says episode facts remain episode-level evidence and prohibits deriving person-level recurrence/typicality/frequency/trait/pattern from episode facts by aggregation, counting, clustering, scoring, or summarizing. A structural output label therefore cannot be the sole firewall.

**Smallest implementation repair**

In `validate_adapter_operation_v2`, resolve the requested projected episode facts. For any non-`inspect` operation among `aggregate`, `count`, `cluster`, `score`, or `summarize`, reject the operation when the requested episode facts span more than one `episode_id`. Cross-episode inspection may remain allowed because it does not derive a summary. Same-episode combination may remain allowed because it stays episode-level.

Add a T006 regression case that constructs a cross-episode `aggregate` (or equivalent) with `output_semantic_level="episode_fact"` and verifies that `validate_adapter_operation_v2` rejects it. Keep the existing accepted-pattern operation test.

No semantic artifact change is required.

## Control-plane disposition

The implementation worker also exposed stale task/preflight state. Supervising Chat repaired this separately:

- active task advanced from the completed-review lock to implementation supervision;
- `state/CURRENT-STATE.md` and the dated overlay again carry the explicit owner correction that there is no inferred completion policy;
- `scripts/task_preflight.py` now fails closed with an explicit finding when `taskId` or `completionCommand` is missing instead of raising `TypeError`.

These control repairs do not alter v2 semantics.

## Required next action

Apply only `LP-PAN-v2-IMPL-001`, run the focused v2 tests plus the relevant checkpoint verification, and return the exact commit/test evidence to supervising Chat. Do not modify the frozen semantic candidate or review artifacts.
