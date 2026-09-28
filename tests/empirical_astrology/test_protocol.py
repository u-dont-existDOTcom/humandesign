from __future__ import annotations

import hashlib
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.empirical_astrology import (
    CohortEntities,
    FreezeManifestError,
    ensure_disjoint_cohorts,
    holm_family,
    require_exact_diagnostic_family,
    validate_bound_freeze_manifest,
    validate_freeze_manifest,
)
from hdmatch.empirical_astrology.protocol import FREEZE_MANIFEST_REQUIRED_FIELDS, HASH_FIELDS

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
REVIEWED_EVIDENCE = "e7f82ab4a1b08705bf4429958a0d577b2758c407"


def _manifest() -> dict[str, object]:
    opening = datetime(2027, 1, 1, tzinfo=UTC)
    manifest: dict[str, object] = {
        field: "0" * 64 if field.endswith("sha256") else "frozen"
        for field in FREEZE_MANIFEST_REQUIRED_FIELDS
    }
    manifest["reviewed_evidence_commit"] = "1" * 40
    manifest["software_commit"] = "2" * 40
    manifest["freeze_timestamp_utc"] = (opening - timedelta(days=1)).isoformat()
    manifest["cohort_opening_utc"] = opening.isoformat()
    manifest["cohort_closing_utc"] = (opening + timedelta(days=30)).isoformat()
    return manifest


def test_freeze_manifest_requires_every_field_and_exact_window() -> None:
    validate_freeze_manifest(_manifest())
    missing = _manifest()
    del missing["pair_registry_sha256"]
    with pytest.raises(FreezeManifestError, match="missing"):
        validate_freeze_manifest(missing)
    wrong_window = _manifest()
    wrong_window["cohort_closing_utc"] = (
        datetime.fromisoformat(str(wrong_window["cohort_opening_utc"])) + timedelta(days=29)
    ).isoformat()
    with pytest.raises(FreezeManifestError, match="30"):
        validate_freeze_manifest(wrong_window)


def test_freeze_manifest_resolves_real_git_checkpoints_and_ancestry() -> None:
    manifest = _manifest()
    manifest["reviewed_evidence_commit"] = REVIEWED_EVIDENCE
    manifest["software_commit"] = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    validate_freeze_manifest(manifest, repository_root=REPOSITORY_ROOT)

    malformed = dict(manifest)
    malformed["software_commit"] = "a" * 64
    with pytest.raises(FreezeManifestError, match="40-character"):
        validate_freeze_manifest(malformed, repository_root=REPOSITORY_ROOT)

    missing = dict(manifest)
    missing["software_commit"] = "0" * 40
    with pytest.raises(FreezeManifestError, match="does not resolve"):
        validate_freeze_manifest(missing, repository_root=REPOSITORY_ROOT)


def test_bound_freeze_manifest_hashes_every_declared_artifact(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "fixture@example.invalid"], cwd=tmp_path, check=True
    )
    subprocess.run(["git", "config", "user.name", "Fixture"], cwd=tmp_path, check=True)
    seed = tmp_path / "seed.txt"
    seed.write_text("seed\n")
    subprocess.run(["git", "add", "seed.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=tmp_path, check=True)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    manifest = _manifest()
    manifest["reviewed_evidence_commit"] = head
    manifest["software_commit"] = head
    bindings: dict[str, Path] = {}
    for index, field in enumerate(sorted(HASH_FIELDS)):
        path = tmp_path / "artifacts" / f"{index}.bin"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(field.encode())
        bindings[field] = path.relative_to(tmp_path)
        manifest[field] = hashlib.sha256(path.read_bytes()).hexdigest()
    validate_bound_freeze_manifest(
        manifest,
        repository_root=tmp_path,
        artifact_paths=bindings,
        expected_protocol_version="frozen",
    )
    (tmp_path / bindings["pair_registry_sha256"]).write_bytes(b"changed")
    with pytest.raises(FreezeManifestError, match="pair_registry_sha256"):
        validate_bound_freeze_manifest(
            manifest,
            repository_root=tmp_path,
            artifact_paths=bindings,
            expected_protocol_version="frozen",
        )


def test_cross_cohort_overlap_fails_for_each_entity_type() -> None:
    empty = frozenset()
    base = CohortEntities(
        frozenset({"P1"}), frozenset({"F1"}), frozenset({"H1"}), frozenset({"N1"})
    )
    disjoint = CohortEntities(
        frozenset({"P2"}), frozenset({"F2"}), frozenset({"H2"}), frozenset({"N2"})
    )
    ensure_disjoint_cohorts(base, disjoint)
    for candidate in (
        CohortEntities(frozenset({"P1"}), empty, empty, empty),
        CohortEntities(empty, frozenset({"F1"}), empty, empty),
        CohortEntities(empty, empty, frozenset({"H1"}), empty),
        CohortEntities(empty, empty, empty, frozenset({"N1"})),
    ):
        with pytest.raises(ValueError, match="overlap"):
            ensure_disjoint_cohorts(base, candidate)


def test_holm_family_preserves_order_and_exact_21_test_gate() -> None:
    results = holm_family([0.001, 0.03, 0.2])
    assert [result.original_index for result in results] == [0, 1, 2]
    assert results[0].rejected is True
    assert results[2].rejected is False
    assert len(require_exact_diagnostic_family([1.0] * 21)) == 21
    with pytest.raises(ValueError, match="21"):
        require_exact_diagnostic_family([1.0] * 20)
