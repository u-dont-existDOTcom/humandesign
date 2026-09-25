#!/usr/bin/env python3
"""Fail closed when active task, checkpoint, and current branch disagree."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def finding(code: str, detail: str) -> None:
    print(f"{code}: {detail}")


def main() -> int:
    task_path = ROOT / "tasks" / "ACTIVE-TASK.json"
    state_path = ROOT / "state" / "CURRENT-STATE.md"
    if not task_path.exists():
        finding("ACTIVE_TASK_MISSING", str(task_path))
        return 1
    task = json.loads(task_path.read_text(encoding="utf-8"))
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()
    errors = 0
    if task.get("exclusive") is not True:
        finding("ACTIVE_TASK_NOT_EXCLUSIVE", task.get("taskId", "unknown"))
        errors += 1
    if branch != task.get("requiredBranch"):
        finding(
            "ACTIVE_TASK_BRANCH_MISMATCH",
            f"expected={task.get('requiredBranch')} actual={branch}",
        )
        errors += 1
    state = state_path.read_text(encoding="utf-8") if state_path.exists() else ""
    task_id = task.get("taskId")
    if not isinstance(task_id, str) or not task_id.strip():
        finding("ACTIVE_TASK_ID_MISSING", "taskId must be a non-empty string")
        errors += 1
    elif task_id not in state:
        finding("CURRENT_STATE_TASK_MISMATCH", task_id)
        errors += 1
    completion_command = task.get("completionCommand")
    if not isinstance(completion_command, str) or not completion_command.strip():
        finding(
            "ACTIVE_TASK_COMPLETION_COMMAND_MISSING",
            "completionCommand must be a non-empty string",
        )
        errors += 1
    elif completion_command not in state:
        finding("CURRENT_STATE_ACCEPTANCE_MISSING", completion_command)
        errors += 1
    if not task.get("suspendedTaskSources"):
        finding("SUSPENDED_TASK_SOURCES_MISSING", "expected at least one source")
        errors += 1
    if errors:
        return 1
    print(f"PREFLIGHT_OK: task={task_id} branch={branch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
