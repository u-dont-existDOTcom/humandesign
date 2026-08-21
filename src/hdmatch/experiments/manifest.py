"""Immutable run manifests and non-secret software provenance."""

from __future__ import annotations

import os
import platform
import re
import subprocess
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .canonical import load_json_bytes, sha256_json, write_new_canonical_json

SHA256_PATTERN = r"^[a-f0-9]{64}$"
_VERSION_PACKAGES = (
    "hdmatch",
    "cryptography",
    "pydantic",
    "tzdata",
    "pyswisseph",
    "numpy",
    "scikit-learn",
)
_ISOLATED_COMMIT_ENV = "HDMATCH_ISOLATED_SOURCE_COMMIT"
_ISOLATED_TREE_ENV = "HDMATCH_ISOLATED_SOURCE_TREE"
_ISOLATED_ROOT_ENV = "HDMATCH_ISOLATED_SOURCE_ROOT"
_GIT_OBJECT_PATTERN = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")


class SoftwareEnvironment(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    python_version: str
    python_implementation: str
    operating_system: str
    machine: str
    packages: dict[str, str]


class RunManifest(BaseModel):
    """The immutable declaration made when an experiment starts.

    Later freeze, reveal, and evaluation records are separate append-only artifacts;
    they never rewrite this initial statement.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["run-manifest-v1"] = "run-manifest-v1"
    experiment_id: str = Field(min_length=1)
    created_at_utc: datetime
    seed: int
    software_commit: str
    software_dirty: bool
    software_environment: SoftwareEnvironment
    candidate_universe: str
    aggregation_rule: str
    model_id: str
    input_hashes: dict[str, str] = Field(min_length=1)
    config_sha256: str = Field(pattern=SHA256_PATTERN)
    reveal_status: Literal["blind"] = "blind"
    declared_outputs: tuple[str, ...] = ()

    @field_validator("created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("manifest timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("input_hashes")
    @classmethod
    def require_sha256_inputs(cls, value: dict[str, str]) -> dict[str, str]:
        for name, digest in value.items():
            if not name or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError(f"invalid SHA-256 binding for {name!r}")
        return dict(sorted(value.items()))

    @property
    def manifest_sha256(self) -> str:
        return sha256_json(self)


def capture_software_environment() -> SoftwareEnvironment:
    versions: dict[str, str] = {}
    for package_name in _VERSION_PACKAGES:
        try:
            versions[package_name] = metadata.version(package_name)
        except metadata.PackageNotFoundError:
            continue
    return SoftwareEnvironment(
        python_version=platform.python_version(),
        python_implementation=platform.python_implementation(),
        operating_system=platform.system(),
        machine=platform.machine(),
        packages=versions,
    )


def git_revision(repository_root: str | Path) -> tuple[str, bool]:
    root = Path(repository_root)
    isolated_values = {
        "commit": os.environ.get(_ISOLATED_COMMIT_ENV),
        "tree": os.environ.get(_ISOLATED_TREE_ENV),
        "root": os.environ.get(_ISOLATED_ROOT_ENV),
    }
    if any(isolated_values.values()):
        if not all(isolated_values.values()):
            raise RuntimeError("isolated source provenance environment is incomplete")
        commit = str(isolated_values["commit"])
        tree = str(isolated_values["tree"])
        declared_root = Path(str(isolated_values["root"]))
        if _GIT_OBJECT_PATTERN.fullmatch(commit) is None:
            raise RuntimeError("isolated source commit is malformed")
        if _GIT_OBJECT_PATTERN.fullmatch(tree) is None:
            raise RuntimeError("isolated source tree is malformed")
        if root.resolve(strict=False) != declared_root.resolve(strict=False):
            raise RuntimeError("isolated source root does not match the mounted decoder root")
        # The claim-grade wrapper obtains both objects from one clean checkout, then
        # mounts only its tracked decoder files. The tree is repeated in the separate
        # isolation receipt; the existing manifest schema records the commit identity.
        return commit, False
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot determine Git revision for {root}") from exc
    return commit, bool(dirty_result.stdout.strip())


def create_run_manifest(
    *,
    experiment_id: str,
    seed: int,
    repository_root: str | Path,
    candidate_universe: str,
    aggregation_rule: str,
    model_id: str,
    input_hashes: dict[str, str],
    config: object,
    declared_outputs: tuple[str, ...] = (),
    created_at_utc: datetime | None = None,
) -> RunManifest:
    commit, dirty = git_revision(repository_root)
    return RunManifest(
        experiment_id=experiment_id,
        created_at_utc=created_at_utc or datetime.now(UTC),
        seed=seed,
        software_commit=commit,
        software_dirty=dirty,
        software_environment=capture_software_environment(),
        candidate_universe=candidate_universe,
        aggregation_rule=aggregation_rule,
        model_id=model_id,
        input_hashes=input_hashes,
        config_sha256=sha256_json(config),
        declared_outputs=declared_outputs,
    )


def write_run_manifest(manifest: RunManifest, path: str | Path) -> Path:
    return write_new_canonical_json(path, manifest)


def load_run_manifest(path: str | Path) -> RunManifest:
    try:
        return RunManifest.model_validate(load_json_bytes(path, require_canonical=True))
    except (OSError, ValueError) as exc:
        raise ValueError(f"invalid or non-canonical run manifest: {path}") from exc


def verify_run_manifest_resume(
    manifest: RunManifest,
    *,
    experiment_id: str,
    seed: int,
    candidate_universe: str,
    aggregation_rule: str,
    model_id: str,
    input_hashes: dict[str, str],
    config: object,
) -> RunManifest:
    """Require an existing manifest to equal the complete requested recovery contract."""

    expected_fields = {
        "experiment_id": experiment_id,
        "seed": seed,
        "candidate_universe": candidate_universe,
        "aggregation_rule": aggregation_rule,
        "model_id": model_id,
        "input_hashes": dict(sorted(input_hashes.items())),
        "config_sha256": sha256_json(config),
    }
    for field, expected in expected_fields.items():
        if getattr(manifest, field) != expected:
            raise ValueError(f"existing run manifest {field} does not match this recovery")
    return manifest
