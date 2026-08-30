"""Fail closed when private participant material can enter public artifacts."""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

PRIVATE_PATH_PREFIXES = (
    "data/relationship_sessions/",
    "data/natal_time_private/",
    "relationship_sessions/",
    "natal_time_private/",
    "private_participant_store/",
    "participant_records/",
    "contact_exports/",
    "consent_exports/",
    "raw_response_exports/",
    "free_text_exports/",
    "private_birth_inputs/",
    "private_classifier_transcripts/",
    "private_learning_cases/",
    "private_exports/",
    "private_backups/",
    "private_uploads/",
    "uploads/birth_records/",
    "tmp/private/",
    "state/private/",
)

PRIVATE_SUFFIXES = (
    ".sqlite",
    ".sqlite3",
    ".sqlite-journal",
    ".sqlite-wal",
    ".sqlite-shm",
    ".db",
    ".db-journal",
    ".private.json",
    ".private.jsonl",
    ".private.csv",
    ".private.tsv",
    ".private.zip",
    ".private.tar",
    ".private.tar.gz",
    ".session-token",
    ".recovery-token",
)

REQUIRED_GITIGNORE_LINES = frozenset(
    {
        *(f"/{prefix}" for prefix in PRIVATE_PATH_PREFIXES),
        *(f"*{suffix}" for suffix in PRIVATE_SUFFIXES),
        "*.log",
        ".env",
        ".env.*",
        "secrets/",
        "*.key",
        "*.pem",
    }
)

REQUIRED_DOCKERIGNORE_LINES = frozenset(
    {
        *(prefix.rstrip("/") for prefix in PRIVATE_PATH_PREFIXES),
        *(f"*{suffix}" for suffix in PRIVATE_SUFFIXES),
        "*.log",
        ".env",
        ".env.*",
        "secrets",
        "*.key",
        "*.pem",
    }
)

# Construct high-confidence token patterns in pieces so this source file does
# not contain a literal credential-shaped canary that would flag itself.
SECRET_PATTERNS = (
    re.compile("-" * 5 + r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    re.compile(r"\bsk" + r"-[A-Za-z0-9_-]{32,}\b"),
    re.compile(r"\bgh[pousr]" + r"_[A-Za-z0-9]{30,}\b"),
)

TEXT_SCAN_SUFFIXES = frozenset(
    {".py", ".md", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".txt", ".js", ".html"}
)


@dataclass(frozen=True, slots=True)
class PrivacyFinding:
    surface: str
    detail: str


def is_private_path(path: str) -> bool:
    normalized = PurePosixPath(path).as_posix().removeprefix("./")
    return normalized.startswith(PRIVATE_PATH_PREFIXES) or normalized.endswith(PRIVATE_SUFFIXES)


def audit_path_list(paths: tuple[str, ...], *, surface: str) -> tuple[PrivacyFinding, ...]:
    return tuple(
        PrivacyFinding(surface=surface, detail=f"forbidden private path: {path}")
        for path in paths
        if is_private_path(path)
    )


def audit_ignore_contract(root: Path) -> tuple[PrivacyFinding, ...]:
    findings: list[PrivacyFinding] = []
    for name, required in (
        (".gitignore", REQUIRED_GITIGNORE_LINES),
        (".dockerignore", REQUIRED_DOCKERIGNORE_LINES),
    ):
        path = root / name
        if not path.is_file():
            findings.append(PrivacyFinding(name, "required exclusion file is missing"))
            continue
        lines = {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        for missing in sorted(required - lines):
            findings.append(PrivacyFinding(name, f"required exclusion is missing: {missing}"))
    return tuple(findings)


def audit_tracked_files(root: Path) -> tuple[PrivacyFinding, ...]:
    tracked = _git_lines(root, "ls-files", "--cached")
    findings = list(audit_path_list(tracked, surface="git-index"))
    for relative in tracked:
        path = root / relative
        if relative == "scripts/check_private_artifacts.py":
            continue
        if path.suffix.lower() not in TEXT_SCAN_SUFFIXES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(
                    PrivacyFinding("git-index", f"credential-shaped content in {relative}")
                )
                break
    return tuple(findings)


def audit_branch_diff(root: Path, base: str | None) -> tuple[PrivacyFinding, ...]:
    if base is None:
        return ()
    changed = _git_lines(root, "diff", "--name-only", f"{base}...HEAD")
    return audit_path_list(changed, surface=f"diff:{base}...HEAD")


def audit_reachable_history_paths(root: Path) -> tuple[PrivacyFinding, ...]:
    objects = _git_lines(root, "rev-list", "--objects", "--all")
    paths = tuple(line.split(" ", 1)[1] for line in objects if " " in line)
    return audit_path_list(paths, surface="reachable-history")


def audit_reachable_history_secrets(root: Path) -> tuple[PrivacyFinding, ...]:
    """Search every reachable revision for high-confidence credential shapes."""

    pattern = re.compile(
        b"-" * 5
        + rb"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"
        + rb"|\bsk-[A-Za-z0-9_-]{32,}"
        + rb"|\bgh[pousr]_[A-Za-z0-9]{30,}"
    )
    objects: dict[str, str] = {}
    for line in _git_lines(root, "rev-list", "--objects", "--all"):
        object_id, _, path = line.partition(" ")
        objects.setdefault(object_id, path or "<unpathed-object>")

    process = subprocess.Popen(
        ("git", "cat-file", "--batch"),
        cwd=root,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stdin is None or process.stdout is None:
        raise RuntimeError("could not open Git history scanner pipes")
    try:
        for object_id, path in objects.items():
            process.stdin.write(object_id.encode("ascii") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii", errors="replace").strip()
            parts = header.split()
            if len(parts) != 3 or parts[1] == "missing":
                raise RuntimeError(f"invalid git cat-file response: {header}")
            size = int(parts[2])
            content = process.stdout.read(size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError("invalid git cat-file object terminator")
            if size <= 2 * 1024 * 1024 and pattern.search(content):
                return (
                    PrivacyFinding(
                        "reachable-history",
                        f"credential-shaped content in historical object {object_id} ({path})",
                    ),
                )
    finally:
        process.stdin.close()
        process.terminate()
        process.wait(timeout=5)
    return ()


def run_audit(root: Path, *, diff_base: str | None = None) -> tuple[PrivacyFinding, ...]:
    resolved = root.resolve(strict=True)
    findings = (
        *audit_ignore_contract(resolved),
        *audit_tracked_files(resolved),
        *audit_branch_diff(resolved, diff_base),
        *audit_reachable_history_paths(resolved),
        *audit_reachable_history_secrets(resolved),
    )
    return tuple(findings)


def _git_lines(root: Path, *args: str) -> tuple[str, ...]:
    result = subprocess.run(
        ("git", *args),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(line for line in result.stdout.splitlines() if line)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--diff-base")
    args = parser.parse_args()
    findings = run_audit(args.repository_root, diff_base=args.diff_base)
    if findings:
        for finding in findings:
            print(f"{finding.surface}: {finding.detail}")
        return 1
    print("private-artifact gate: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
