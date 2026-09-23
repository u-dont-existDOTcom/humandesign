# G10 follow-up admission repair — 2026-09-23

Status: **REPAIRED / OWNER FEEDBACK INCORPORATED**

## Failure observed

A target-blind gap planner proposed this follow-up for `D10.stable_direction`:

> If the group’s fixed hours fit your availability, would anything else about how you want to work affect whether you join, or would that be enough?

It was surfaced without a separate final admission check on the exact rendered wording. Owner feedback immediately exposed two defects:

1. the nonadjacent antecedent was not re-established clearly enough (`the group` was ambiguous after many intervening turns);
2. asking whether “anything else” would affect joining a group is too broad and nearly forced, because joining can depend on many unspecified factors beyond schedule.

A fresh target-theory-blind admission audit independently confirmed failure of context binding, premise sufficiency, and construct discrimination.

## Causal mechanism

The interview protocol already required premise sufficiency, discrimination, context binding, and nonredundancy, but the live calibration orchestration treated a planner-selected/generated question as if route selection itself constituted admission. There was no hard post-planner check on the exact user-facing wording.

## Repair

The protocol now states explicitly that planner/selector output is proposal-only. Before any question is rendered, the exact wording must pass:

- context binding;
- premise sufficiency;
- construct discrimination;
- nonredundancy;
- construct alignment;
- single-response-task.

If any check fails, the question is repaired once using only neutral context; if the repair still fails, the route is suppressed and the facet remains unresolved.

The interviewer-bank planning metadata now carries the same proposal-only requirement, and `verify_v7.py` mechanically checks that this final-admission contract remains present.

## G10 repair attempts

- original generated follow-up: **REJECTED**; broad join decision and ambiguous nonadjacent context;
- repair 1: **REJECTED**; mixed retained priority with willingness to raise the issue socially;
- repair 2: **REJECTED**; alternatives overlapped because someone can accept fixed hours and still value choice;
- repair 3: **ADMITTED** after an independent target-blind audit passed all six final-admission checks.

Admitted wording:

> For that group whose work interests you, suppose its fixed hours fit your availability and you agree to follow them. How important, if at all, would it still be to you to have a say in choosing your working times for that group?

The owner’s process objection is not counted as a survey answer. The private measurement remains at 78 answers until the repaired question is answered or skipped.
