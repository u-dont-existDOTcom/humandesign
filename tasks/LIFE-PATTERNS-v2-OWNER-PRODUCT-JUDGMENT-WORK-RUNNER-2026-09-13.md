# Life Patterns v2 owner product judgment — Work runner — 2026-09-13

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
PR: `#24` (remain draft/open/unmerged)

## Purpose

Remove local setup burden from the owner while preserving the actual owner-controlled interaction test.

Work is execution-only here. Do not redesign semantics, choose owner answers, or decide whether the product interaction is good.

## Reasoning level

Use **Low** reasoning. The architecture and interaction semantics are already fixed for this bounded test.

## Read first

1. Fetch the live PR #24 head.
2. Read `tasks/ACTIVE-TASK.json`.
3. Read `state/CURRENT-STATE.md`.
4. Read `src/hdmatch/evaluation/participant_adjudicated_v2_prototype.py`.
5. Read `tasks/LIFE-PATTERNS-v2-OWNER-PROTOTYPE-INTERACTION-REPAIR-001-2026-09-13.md`.

## Execution

Use Work's own cloud terminal/computer. Do not require the owner to locate or configure a local checkout.

1. Obtain/update a clean checkout of this repository at the live `codex/discover-life-patterns-mvp` head.
2. Verify the exact branch/head before running anything.
3. Create a Python >=3.11 virtual environment if one is not already usable.
4. Install the minimum package requirements needed to run the prototype; `pip install -e '.[dev]'` is acceptable if simplest.
5. Run `python scripts/task_preflight.py`; it must return `PREFLIGHT_OK` before the interaction begins.
6. Run the actual executable interaction:
   `.venv/bin/python -m hdmatch.evaluation.participant_adjudicated_v2_prototype`
   or the equivalent interpreter from Work's environment.
7. Maintain the terminal process interactively. **Before requesting each owner answer, show the owner the complete owner-visible terminal output emitted since launch or since the previous owner input, followed by the current input prompt. Never send a bare CLI prompt by itself.** For example, the first relay must include the displayed episode, the proposed fact, and then `Fact review [accept/correct/not-supported]:` in one message.
8. Wait for the owner's answer. Enter exactly the owner's answer into the terminal. Do not select, normalize, reinterpret, improve, or substitute an answer.
9. After entering an answer, capture and relay all new owner-visible terminal output before asking for the next answer. Preserve enough context that the owner can understand what they are judging without consulting this task file or source code.
10. Continue until the executable produces the final result or terminates because no usable fact remains.

## Important interaction boundary

The owner, not Work, must make the substantive choices:

- fact `accept | correct | not-supported`;
- replacement fact wording if correction is chosen;
- pattern `accept | revise | reject | unresolved`;
- revised pattern wording if chosen;
- development-only grounding confirmation;
- final `accept | reject | unresolved` after a revision.

Work may explain a literal CLI error if one occurs, but must not coach the owner toward any answer.

A relay that contains only an input prompt and omits the immediately preceding episode/fact/question/result context is invalid. If that occurs, do not ask the owner to answer yet; re-display the missing owner-visible context first.

## Privacy and repository rules

- Do not commit the owner's interactive answers or any resulting narrative-bearing runtime data.
- Do not publish, deploy, recruit/contact anyone, spend money, invoke target-model/chart logic, or merge PR #24.
- Do not alter the accepted v2 contract or `participant_adjudicated_v2.py` as part of this run.
- If the executable itself fails before product judgment, report the exact implementation failure and stop; do not redesign around it.

## Return receipt

After the owner-controlled run ends, return only:

- exact repo branch/head used;
- `PREFLIGHT_OK` confirmation;
- whether the interactive executable completed successfully;
- the final status emitted by the executable (`accepted`, `rejected`, `unresolved`, or no-pattern because no usable fact remained);
- the exact owner-visible transcript from this bounded interaction, redacting only secrets if any unexpectedly appear;
- no product-quality verdict.

The next step after this receipt belongs in the supervising Chat, where the owner gives the actual product judgment.
