# Life Patterns v2 owner real-data browser — Work runner — 2026-09-13

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
PR: `#24` (remain draft/open/unmerged)

## Purpose

Remove setup burden from the owner while preserving direct browser interaction. Work is execution-only: it prepares the runtime and launches the browser app, but the owner interacts with the web UI directly rather than through Work as a prompt courier.

## Read first

1. Fetch the live PR #24 head.
2. Read `tasks/ACTIVE-TASK.json`.
3. Read `tasks/LIFE-PATTERNS-v2-OWNER-REAL-DATA-BROWSER-PROTOTYPE-2026-09-13.md`.
4. Read `src/hdmatch/api/life_patterns_v2_owner_app.py` and `src/hdmatch/api/life_patterns_v2_owner_ui.py`.

## Execution

1. Obtain/update a clean checkout at the live `codex/discover-life-patterns-mvp` head.
2. Create/use Python >=3.11 virtualenv and install `requirements-dev.lock` plus editable package if needed.
3. Run `python scripts/task_preflight.py`; require `PREFLIGHT_OK`.
4. Ensure an owner-authorized runtime API key is available as `HDMATCH_LLM_API_KEY` or `OPENAI_API_KEY`. Do not ask the owner to paste a secret into chat. If no key is available in the runtime environment, stop and report that single blocker.
5. Launch the owner app locally with:
   `python -m uvicorn hdmatch.api.life_patterns_v2_owner_app:app --host 127.0.0.1 --port 8765`
6. Open `http://127.0.0.1:8765/` in Work's browser/computer and present the browser surface directly. Do not relay individual form prompts into chat.
7. Keep the process alive while the owner completes 2–3 real episodes and gives product feedback.

## Privacy

- Do not commit or publish runtime narratives.
- Do not expose the local server publicly.
- Do not log or echo secrets.
- Do not deploy, recruit/contact anyone, merge, or invoke target-model/chart logic.

## Return receipt

Return only environment/setup status, exact repo head, `PREFLIGHT_OK`, whether the browser app opened successfully, and any implementation error. Do not summarize or commit the owner's narrative content.
