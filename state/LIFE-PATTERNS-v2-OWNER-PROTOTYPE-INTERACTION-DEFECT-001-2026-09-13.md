# Life Patterns v2 owner prototype interaction defect 001 — 2026-09-13

Status: **REPAIR REQUIRED**

Finding ID: `LP-PAN-v2-PROT-001`

Semantic change required: **false**.

## Finding

The bounded v2 owner-development prototype is technically green but has not reached the required **OWNER PRODUCT JUDGMENT** boundary.

The task requires an owner-usable interaction in which the owner can personally:

- review proposed episode facts;
- accept, correct, or mark them unsupported;
- see a candidate pattern question;
- accept, revise, reject, or leave it unresolved;
- perform one recursive refinement when revising;
- inspect the resulting participant-adjudicated v2 result.

The current module `src/hdmatch/evaluation/participant_adjudicated_v2_prototype.py` exposes programmatic methods for those operations, but its executable `run_synthetic_owner_demo()` hard-codes the correction, revision, and acceptance. Running:

```sh
.venv/bin/python -m hdmatch.evaluation.participant_adjudicated_v2_prototype
```

therefore demonstrates a scripted path rather than allowing the owner to exercise the product interaction. The focused tests verify the scripted transcript and method behavior; they do not prove an owner-controlled interaction exists.

## Disposition

- accepted v2 semantics/contract: unchanged;
- bounded v2 core implementation: unchanged;
- prototype plumbing: reusable;
- owner product judgment: **NOT YET REACHED**;
- product scaling: blocked;
- external participant collection / target-model work / merge-deploy / spending: remain unauthorized.

## Required repair

Add the smallest local interactive surface over the existing `OwnerPrototypeSessionV2` behavior. A terminal interaction is sufficient; do not build web/auth/voice/deployment infrastructure.

The owner must be able to provide choices and wording at runtime. The executable path must not preselect the outcome. It should support at minimum:

1. display the synthetic bounded episode and proposed fact;
2. prompt owner for `accept | correct | not-supported`;
3. if correction, accept owner wording and create the append-only fact revision;
4. if no usable fact remains, end without a pattern claim;
5. display the candidate pattern question;
6. prompt `accept | revise | reject | unresolved`;
7. if revise, accept owner wording, create one revised proposal, show the revised question, and prompt again;
8. show final status/wording/provenance and validate through the frozen v2 core.

The interaction must make it easy to test negative paths as well as the happy path.

## Focused regression

Add a testable input/output driver (for example injected `input_fn` / `output_fn`) so tests can prove that runtime owner choices, rather than hard-coded decisions, determine the result. Preserve the existing semantic/core tests.

## State defect discovered concurrently

`tasks/ACTIVE-TASK.json` omitted `completionCommand`, causing `python scripts/task_preflight.py` to fail closed. The prototype repair task should restore a concrete completion command covering the interactive prototype tests plus the v2 core tests.
