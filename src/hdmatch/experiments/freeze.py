"""Append-only prediction freezing bound to every scientific input artifact."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .canonical import load_json_bytes, sha256_file, write_new_canonical_json
from .manifest import (
    SHA256_PATTERN,
    RunManifest,
    capture_software_environment,
    git_revision,
    load_run_manifest,
)


class FreezeVerificationError(RuntimeError):
    """A freeze record is absent, malformed, unbound, or no longer matches its bytes."""


class ArtifactBindings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)


class FreezeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["prediction-freeze-v1"] = "prediction-freeze-v1"
    experiment_id: str = Field(min_length=1)
    prediction_file: str
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_size_bytes: int = Field(ge=0)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    run_manifest_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    software_commit: str
    software_dirty: bool
    software_versions: dict[str, str]
    created_at_utc: datetime
    answer_key_revealed: Literal[False] = False

    @field_validator("prediction_file")
    @classmethod
    def require_safe_relative_path(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or value in {"", "."}:
            raise ValueError("prediction_file must be a safe run-relative path")
        return path.as_posix()

    @field_validator("created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("freeze timestamp must be timezone-aware")
        return value.astimezone(UTC)


def _relative_artifact(run_dir: Path, artifact: Path) -> str:
    try:
        return artifact.resolve(strict=True).relative_to(run_dir.resolve(strict=True)).as_posix()
    except ValueError as exc:
        raise ValueError("prediction file must be inside the run directory") from exc


def _verify_run_manifest_binding(
    directory: Path,
    record: FreezeRecord,
    manifest_path: Path,
) -> RunManifest:
    if record.run_manifest_sha256 is None:
        raise FreezeVerificationError("prediction freeze lacks a run-manifest binding")
    try:
        manifest_path.resolve(strict=True).relative_to(directory.resolve(strict=True))
    except (FileNotFoundError, ValueError) as exc:
        raise FreezeVerificationError(
            "frozen run-manifest path escapes or is absent"
        ) from exc
    if sha256_file(manifest_path) != record.run_manifest_sha256:
        raise FreezeVerificationError("frozen run-manifest bytes changed")
    try:
        manifest = load_run_manifest(manifest_path)
    except ValueError as exc:
        raise FreezeVerificationError("frozen run manifest is invalid") from exc
    if manifest.experiment_id != record.experiment_id:
        raise FreezeVerificationError("run manifest experiment_id differs from prediction freeze")
    if manifest.input_hashes.get("blind_cases.json") != record.blind_input_sha256:
        raise FreezeVerificationError("run manifest does not bind the frozen blind input")
    if manifest.created_at_utc > record.created_at_utc:
        raise FreezeVerificationError("prediction freeze predates its run manifest")
    if (
        manifest.software_commit != record.software_commit
        or manifest.software_dirty != record.software_dirty
    ):
        raise FreezeVerificationError("prediction freeze software state differs from run manifest")
    expected_versions = manifest.software_environment.packages | {
        "python": manifest.software_environment.python_version
    }
    if record.software_versions != expected_versions:
        raise FreezeVerificationError(
            "prediction freeze software environment differs from run manifest"
        )
    return manifest


def freeze_predictions(
    run_dir: str | Path,
    *,
    experiment_id: str,
    bindings: ArtifactBindings,
    repository_root: str | Path,
    prediction_path: str | Path | None = None,
    run_manifest_path: str | Path | None = None,
    freeze_path: str | Path | None = None,
    created_at_utc: datetime | None = None,
) -> FreezeRecord:
    """Freeze the exact prediction bytes and their complete scientific bindings."""

    directory = Path(run_dir)
    directory.mkdir(parents=True, exist_ok=True)
    prediction = (
        Path(prediction_path) if prediction_path is not None else directory / "predictions.json"
    )
    relative_prediction = _relative_artifact(directory, prediction)
    # Imports stay local to keep the low-level hash module free of package import cycles.
    from hdmatch.evaluation.leakage import assert_no_prediction_leakage
    from hdmatch.synthetic.sealing import assert_no_plaintext_answer_keys

    assert_no_prediction_leakage(prediction)
    assert_no_plaintext_answer_keys(repository_root)
    commit, dirty = git_revision(repository_root)
    environment = capture_software_environment()
    manifest = Path(run_manifest_path) if run_manifest_path is not None else None
    manifest_hash = sha256_file(manifest) if manifest is not None else None
    record = FreezeRecord(
        experiment_id=experiment_id,
        prediction_file=relative_prediction,
        prediction_sha256=sha256_file(prediction),
        prediction_size_bytes=prediction.stat().st_size,
        **bindings.model_dump(),
        run_manifest_sha256=manifest_hash,
        software_commit=commit,
        software_dirty=dirty,
        software_versions=environment.packages | {"python": environment.python_version},
        created_at_utc=created_at_utc or datetime.now(UTC),
    )
    if manifest is not None:
        _verify_run_manifest_binding(directory, record, manifest)
    destination = (
        Path(freeze_path) if freeze_path is not None else directory / "prediction.freeze.json"
    )
    try:
        destination.resolve(strict=False).relative_to(directory.resolve(strict=True))
    except ValueError as exc:
        raise ValueError("freeze record must be inside the run directory") from exc
    write_new_canonical_json(destination, record)
    return record


def load_freeze_record(path: str | Path) -> FreezeRecord:
    try:
        value = load_json_bytes(path, require_canonical=True)
        return FreezeRecord.model_validate(value)
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise FreezeVerificationError(f"invalid or missing prediction freeze: {path}") from exc


def verify_frozen_predictions(
    run_dir: str | Path,
    *,
    freeze_path: str | Path | None = None,
    expected_bindings: ArtifactBindings | None = None,
    expected_experiment_id: str | None = None,
    run_manifest_path: str | Path | None = None,
    require_run_manifest: bool = False,
) -> FreezeRecord:
    """Verify frozen bytes and, in strict mode, the exact bound run-manifest bytes."""

    directory = Path(run_dir)
    freeze = Path(freeze_path) if freeze_path is not None else directory / "prediction.freeze.json"
    record = load_freeze_record(freeze)
    prediction = directory / record.prediction_file
    try:
        prediction.resolve(strict=True).relative_to(directory.resolve(strict=True))
    except (FileNotFoundError, ValueError) as exc:
        raise FreezeVerificationError("frozen prediction path escapes or is absent") from exc
    if prediction.stat().st_size != record.prediction_size_bytes:
        raise FreezeVerificationError("frozen prediction byte length changed")
    if sha256_file(prediction) != record.prediction_sha256:
        raise FreezeVerificationError("frozen prediction bytes changed")
    if require_run_manifest:
        manifest = (
            Path(run_manifest_path)
            if run_manifest_path is not None
            else directory / "run.manifest.json"
        )
        _verify_run_manifest_binding(directory, record, manifest)
    if expected_experiment_id is not None and record.experiment_id != expected_experiment_id:
        raise FreezeVerificationError("freeze experiment_id does not match reveal request")
    if expected_bindings is not None:
        actual = ArtifactBindings(
            blind_input_sha256=record.blind_input_sha256,
            model_sha256=record.model_sha256,
            question_bank_sha256=record.question_bank_sha256,
            mapping_sha256=record.mapping_sha256,
        )
        if actual != expected_bindings:
            raise FreezeVerificationError("freeze artifact bindings do not match expected inputs")
    if not re.fullmatch(SHA256_PATTERN, record.prediction_sha256):
        raise FreezeVerificationError("freeze prediction digest is malformed")
    return record
