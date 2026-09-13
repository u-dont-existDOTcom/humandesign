# Life Patterns v2 owner prototype interaction repair 001 — 2026-09-13

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
PR: `#24` (remain draft/open/unmerged)

## Objective

Repair `LP-PAN-v2-PROT-001` only: make the existing bounded v2 owner-development prototype genuinely owner-controlled at runtime so the project can reach **OWNER PRODUCT JUDGMENT**.

This is an implementation/usability repair. Do **not** change the accepted v2 semantics or contract.

## Read first

1. `tasks/ACTIVE-TASK.json`
2. `state/CURRENT-STATE.md`
3. `state/LIFE-PATTERNS-v2-OWNER-PROTOTYPE-INTERACTION-DEFECT-001-2026-09-13.md`
4. `tasks/LIFE-PATTERNS-v2-OWNER-DEVELOPMENT-PROTOTYPE-2026-09-13.md`
5. `src/hdmatch/evaluation/participant_adjudicated_v2_prototype.py`
6. `src/hdmatch/evaluation/participant_adjudicated_v2.py`
7. `tests/unit/test_participant_adjudicated_v2_prototype.py`
8. current task-relevant UDA guidance activated by root `AGENTS.md`.

## Exact defect

The executable path is scripted: `run_synthetic_owner_demo()` preselects fact correction, pattern revision, and final acceptance. The owner cannot make those choices while running the advertised command. Tests prove plumbing, not owner interaction.

There is a second implementation detail inside the same defect: the current prototype-only semantic grounding callback recognizes only two hard-coded pattern wordings (`I prepare before complex work.` and `I plan before complex work.`). A naive interactive repair that accepts arbitrary participant revision text would therefore fail validation for wording outside that whitelist. Do not solve this by weakening the production v2 contract.

## Required repair

Implement the smallest terminal interaction over the existing prototype session. Prefer injected I/O so it is deterministic under tests.

Required runtime behavior:

- display the bounded synthetic episode and proposed fact;
- ask the owner to `accept`, `correct`, or mark the fact `not-supported`;
- for `correct`, collect the replacement wording and create an append-only v2 revision;
- if no usable fact remains, terminate cleanly with no person-level pattern claim;
- show the candidate pattern question;
- ask `accept | revise | reject | unresolved`;
- for `revise`, collect participant wording, create exactly one revised proposal, show the revised question, then ask for a final adjudication;
- display the final status and accepted wording when applicable;
- validate/freeze/project through the existing v2 core before reporting success;
- do not hard-code the owner's substantive choices in the interactive path.

For owner-entered revised wording, keep any flexibility strictly inside the **development harness**. The production v2 semantic contract must remain unchanged. The prototype may use a development-only, target-theory-blind grounding mechanism bound to the owner interaction (for example an explicit owner confirmation that the episode evidence supports the revised wording, or another equally narrow provenance-marked test double). It must not silently treat every arbitrary proposition as grounded, and it must not modify `participant_adjudicated_v2.py` merely to make the prototype pass.

A CLI is sufficient. Do not add web UI, auth, email recovery, voice, deployment, paid inference, target-model logic, comprehensive taxonomies, or historical automatic map generation.

## Tests

Add direct regression coverage showing that injected owner inputs determine at least these paths:

1. accept fact -> accept pattern;
2. correct fact -> revise pattern wording -> accept revised pattern;
3. not-supported fact -> no pattern proposal;
4. reject pattern -> rejected result;
5. unresolved pattern -> unresolved result;
6. owner-entered revised wording outside the old two-string whitelist can complete only through the explicit development-only grounding path, without changing production v2 semantics.

Preserve all existing prototype and v2 core tests.

Focused completion command:

```sh
.venv/bin/python -m pytest tests/unit/test_participant_adjudicated_v2_prototype.py tests/unit/test_participant_adjudicated_v2.py -q
```

Also run focused lint/type checks for touched code and `python scripts/task_preflight.py` after canonical state includes the completion command.

## Stop boundary

Stop after:

- interactive owner-controlled command exists;
- focused tests/lint/typecheck are green;
- task preflight passes;
- canonical state returns to **OWNER PRODUCT JUDGMENT REQUIRED** with the exact command the owner should run.

Do not decide whether the product interaction is good. That judgment belongs to the owner after using it.
