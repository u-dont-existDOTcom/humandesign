from __future__ import annotations

import subprocess
from pathlib import Path

from scripts.check_private_artifacts import (
    REQUIRED_DOCKERIGNORE_LINES,
    REQUIRED_GITIGNORE_LINES,
    audit_ignore_contract,
    audit_path_list,
    audit_tracked_files,
    is_private_path,
)

PROJECT_ROOT = Path(__file__).parents[2]


def test_repository_ignore_and_docker_contract_is_complete() -> None:
    assert not audit_ignore_contract(PROJECT_ROOT)
    assert REQUIRED_GITIGNORE_LINES
    assert REQUIRED_DOCKERIGNORE_LINES


def test_private_classes_are_forbidden_but_public_synthetic_fixture_is_allowed() -> None:
    private_paths = (
        "data/relationship_sessions/session.json",
        "data/natal_time_private/intake.json",
        "contact_exports/contacts.csv",
        "consent_exports/consents.json",
        "raw_response_exports/raw.jsonl",
        "free_text_exports/narratives.txt",
        "private_birth_inputs/birth.json",
        "private_classifier_transcripts/case.txt",
        "private_learning_cases/case.json",
        "private_backups/backup.private.tar.gz",
        "participant.sqlite-wal",
        "participant.recovery-token",
    )
    assert all(is_private_path(path) for path in private_paths)
    assert not is_private_path("tests/fixtures/synthetic_natal_time/public_example.json")


def test_staged_private_file_fails_the_index_gate(tmp_path: Path) -> None:
    subprocess.run(("git", "init", "-q"), cwd=tmp_path, check=True)
    private = tmp_path / "private_participant_store" / "record.json"
    private.parent.mkdir(parents=True)
    private.write_text('{"synthetic_canary":"must-not-publish"}', encoding="utf-8")
    subprocess.run(("git", "add", "-f", private.relative_to(tmp_path)), cwd=tmp_path, check=True)

    findings = audit_tracked_files(tmp_path)

    assert findings
    assert "private_participant_store/record.json" in findings[0].detail


def test_branch_path_gate_rejects_generated_private_suffix() -> None:
    findings = audit_path_list(
        ("reports/public.json", "exports/pair_001.private.json"), surface="unit-test"
    )

    assert [finding.detail for finding in findings] == [
        "forbidden private path: exports/pair_001.private.json"
    ]
