"""Freeze-gated answer-key reveal with no plaintext project artifact."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from hdmatch.synthetic.sealing import SealingMetadata, decrypt_answer_key_json

from .canonical import load_json_bytes, sha256_file, write_new_canonical_json
from .freeze import FreezeRecord, FreezeVerificationError, verify_frozen_predictions
from .manifest import SHA256_PATTERN


class RevealRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["answer-key-reveal-v1"] = "answer-key-reveal-v1"
    experiment_id: str
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    freeze_record_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    revealed_at_utc: datetime
    answer_key_revealed: Literal[True] = True

    @field_validator("revealed_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("reveal timestamp must be timezone-aware")
        return value.astimezone(UTC)


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
    return record


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
    answer_key = decrypt_answer_key_json(
        encrypted_answer_key_path,
        key_path=key_path,
        decoder_root=decoder_root,
        expected_metadata=metadata,
    )
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
        encrypted_answer_key_sha256=sha256_file(encrypted_answer_key_path),
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
