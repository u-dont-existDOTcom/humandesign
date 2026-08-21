"""Freeze-gated answer-key reveal with no plaintext project artifact."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.synthetic.sealing import (
    AnswerKeySealingError,
    SealingMetadata,
    decrypt_answer_key_bytes,
    verify_envelope_bindings,
)

from .canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
    sha256_file,
    write_new_canonical_json,
)
from .freeze import FreezeRecord, FreezeVerificationError, verify_frozen_predictions
from .manifest import SHA256_PATTERN


class RevealRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["answer-key-reveal-v1"] = "answer-key-reveal-v1"
    experiment_id: str
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    freeze_record_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_file: str | None = None
    answer_key_payload_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    revealed_at_utc: datetime
    answer_key_revealed: Literal[True] = True

    @field_validator("encrypted_answer_key_file")
    @classmethod
    def require_safe_relative_path(cls, value: str | None) -> str | None:
        if value is None:
            return None
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or value in {"", "."}:
            raise ValueError("encrypted_answer_key_file must be a safe run-relative path")
        return path.as_posix()

    @field_validator("revealed_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("reveal timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_complete_binding_pair(self) -> RevealRecord:
        if (self.encrypted_answer_key_file is None) != (
            self.answer_key_payload_sha256 is None
        ):
            raise ValueError("complete reveal bindings must be declared together")
        return self


class RevealResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    answer_key: Any = Field(repr=False, exclude=True)
    record: RevealRecord
    freeze: FreezeRecord


def load_reveal_record(path: str | Path) -> RevealRecord:
    try:
        value = load_json_bytes(path, require_canonical=True)
        return RevealRecord.model_validate(value)
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise FreezeVerificationError(
            f"invalid or missing answer-key reveal record: {path}"
        ) from exc


def verify_reveal_record(
    run_dir: str | Path,
    *,
    freeze: FreezeRecord,
    freeze_path: str | Path,
    reveal_record_path: str | Path | None = None,
    require_complete_binding: bool = False,
) -> RevealRecord:
    directory = Path(run_dir)
    path = (
        Path(reveal_record_path)
        if reveal_record_path is not None
        else directory / "answer-key.reveal.json"
    )
    record = load_reveal_record(path)
    if record.experiment_id != freeze.experiment_id:
        raise FreezeVerificationError("reveal experiment_id does not match prediction freeze")
    if record.prediction_sha256 != freeze.prediction_sha256:
        raise FreezeVerificationError("reveal prediction hash does not match prediction freeze")
    if record.freeze_record_sha256 != sha256_file(freeze_path):
        raise FreezeVerificationError("reveal is not bound to the current freeze record bytes")
    if record.revealed_at_utc < freeze.created_at_utc:
        raise FreezeVerificationError("answer-key reveal predates the prediction freeze")
    if record.encrypted_answer_key_file is None:
        if require_complete_binding:
            raise FreezeVerificationError(
                "reveal record lacks complete envelope and answer-key payload bindings"
            )
        return record
    envelope_path = directory / record.encrypted_answer_key_file
    try:
        envelope_path.resolve(strict=True).relative_to(directory.resolve(strict=True))
    except (FileNotFoundError, ValueError) as exc:
        raise FreezeVerificationError("reveal envelope path escapes or is absent") from exc
    if sha256_file(envelope_path) != record.encrypted_answer_key_sha256:
        raise FreezeVerificationError("reveal envelope bytes changed")
    metadata = SealingMetadata(
        experiment_id=freeze.experiment_id,
        blind_input_sha256=freeze.blind_input_sha256,
        model_sha256=freeze.model_sha256,
        question_bank_sha256=freeze.question_bank_sha256,
        mapping_sha256=freeze.mapping_sha256,
    )
    try:
        verify_envelope_bindings(envelope_path, expected_metadata=metadata)
    except AnswerKeySealingError as exc:
        raise FreezeVerificationError("reveal envelope bindings are invalid") from exc
    return record


def _relative_envelope_path(directory: Path, encrypted_path: Path) -> str:
    try:
        return encrypted_path.resolve(strict=True).relative_to(
            directory.resolve(strict=True)
        ).as_posix()
    except (FileNotFoundError, ValueError) as exc:
        raise ValueError("encrypted answer-key envelope must be inside the run directory") from exc


def reveal_answer_key(
    run_dir: str | Path,
    *,
    encrypted_answer_key_path: str | Path,
    key_path: str | Path,
    decoder_root: str | Path,
    freeze_path: str | Path | None = None,
    reveal_record_path: str | Path | None = None,
    revealed_at_utc: datetime | None = None,
) -> RevealResult:
    """Verify frozen bytes, authenticate bindings, then reveal the key only in memory."""

    directory = Path(run_dir)
    resolved_freeze = (
        Path(freeze_path) if freeze_path is not None else directory / "prediction.freeze.json"
    )
    freeze = verify_frozen_predictions(directory, freeze_path=resolved_freeze)
    metadata = SealingMetadata(
        experiment_id=freeze.experiment_id,
        blind_input_sha256=freeze.blind_input_sha256,
        model_sha256=freeze.model_sha256,
        question_bank_sha256=freeze.question_bank_sha256,
        mapping_sha256=freeze.mapping_sha256,
    )
    encrypted_path = Path(encrypted_answer_key_path)
    relative_envelope = _relative_envelope_path(directory, encrypted_path)
    plaintext = decrypt_answer_key_bytes(
        encrypted_path,
        key_path=key_path,
        decoder_root=decoder_root,
        expected_metadata=metadata,
    )
    try:
        answer_key = json.loads(plaintext)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("decrypted answer key is not valid UTF-8 JSON") from exc
    if canonical_json_bytes(answer_key) != plaintext:
        raise ValueError("decrypted answer-key payload must use canonical JSON bytes")
    if not isinstance(answer_key, dict):
        raise ValueError("answer key must be a JSON object")
    if answer_key.get("schema_version") != "answer-key-v1":
        raise ValueError("unsupported answer-key schema")
    if answer_key.get("experiment_id") != freeze.experiment_id:
        raise ValueError("answer-key experiment_id does not match the prediction freeze")
    if answer_key.get("blind_input_sha256") != freeze.blind_input_sha256:
        raise ValueError("answer-key blind input hash does not match the prediction freeze")
    reveal_time = revealed_at_utc or datetime.now(UTC)
    if reveal_time < freeze.created_at_utc:
        raise ValueError("answer-key reveal timestamp cannot predate prediction freeze")
    record = RevealRecord(
        experiment_id=freeze.experiment_id,
        prediction_sha256=freeze.prediction_sha256,
        freeze_record_sha256=sha256_file(resolved_freeze),
        encrypted_answer_key_sha256=sha256_file(encrypted_path),
        encrypted_answer_key_file=relative_envelope,
        answer_key_payload_sha256=sha256_bytes(plaintext),
        revealed_at_utc=reveal_time,
    )
    destination = (
        Path(reveal_record_path)
        if reveal_record_path is not None
        else directory / "answer-key.reveal.json"
    )
    try:
        destination.resolve(strict=False).relative_to(directory.resolve(strict=True))
    except ValueError as exc:
        raise ValueError("reveal record must be inside the run directory") from exc
    write_new_canonical_json(destination, record)
    return RevealResult(answer_key=answer_key, record=record, freeze=freeze)
