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
    decrypt_answer_key_envelope_bytes,
    verify_envelope_bindings,
)

from .answer_key_commitments import (
    answer_key_case_mapping,
    generation_seed_commitment,
    revealed_local_date_set_hash,
    revealed_target_set_hash,
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

    schema_version: Literal["answer-key-reveal-v2", "answer-key-reveal-v3"] = "answer-key-reveal-v2"
    experiment_id: str
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    run_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    freeze_record_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_file: str
    answer_key_payload_sha256: str = Field(pattern=SHA256_PATTERN)
    revealed_target_set_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    revealed_local_date_set_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    generation_seed_commitment_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    paired_prediction_freeze_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    paired_plan_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    paired_arm_id: str | None = None
    revealed_at_utc: datetime
    answer_key_revealed: Literal[True] = True

    @field_validator("encrypted_answer_key_file")
    @classmethod
    def require_safe_relative_path(cls, value: str) -> str:
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
    def require_v3_commitments(self) -> RevealRecord:
        commitments = (
            self.revealed_target_set_sha256,
            self.revealed_local_date_set_sha256,
            self.generation_seed_commitment_sha256,
        )
        paired = (
            self.paired_prediction_freeze_sha256,
            self.paired_plan_sha256,
            self.paired_arm_id,
        )
        if self.schema_version == "answer-key-reveal-v3":
            if not all(value is not None for value in commitments):
                raise ValueError("answer-key reveal v3 requires complete target/seed commitments")
        elif any(value is not None for value in commitments):
            raise ValueError("answer-key reveal v2 cannot claim v3 target/seed commitments")
        if any(value is not None for value in paired) and not all(
            value is not None for value in paired
        ):
            raise ValueError("paired reveal provenance must be complete or absent")
        if self.schema_version == "answer-key-reveal-v2" and any(
            value is not None for value in paired
        ):
            raise ValueError("answer-key reveal v2 cannot claim paired provenance")
        return self


_REVEAL_RESULT_CAPABILITY = object()


class RevealResult:
    """Non-serializable capability minted only by authenticated in-memory reveal."""

    __slots__ = ("__answer_key", "__capability", "freeze", "record")

    def __init__(
        self,
        *,
        answer_key: Any,
        record: RevealRecord,
        freeze: FreezeRecord,
        _capability: object | None = None,
    ) -> None:
        if _capability is not _REVEAL_RESULT_CAPABILITY:
            raise TypeError("RevealResult can only be created by authenticated answer-key reveal")
        self.__answer_key = answer_key
        self.__capability = _capability
        self.record = record
        self.freeze = freeze

    @property
    def answer_key(self) -> Any:
        self.require_claim_grade()
        return self.__answer_key

    def require_claim_grade(self) -> None:
        if self.__capability is not _REVEAL_RESULT_CAPABILITY:
            raise TypeError("invalid in-memory answer-key reveal capability")

    def model_dump(self) -> dict[str, object]:
        """Expose public receipt metadata while deliberately omitting plaintext truth."""

        self.require_claim_grade()
        return {"record": self.record.model_dump(), "freeze": self.freeze.model_dump()}

    def __repr__(self) -> str:
        return f"RevealResult(record={self.record!r}, freeze={self.freeze!r})"


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
    direct_bindings = {
        "blind_input_sha256": freeze.blind_input_sha256,
        "model_sha256": freeze.model_sha256,
        "question_bank_sha256": freeze.question_bank_sha256,
        "mapping_sha256": freeze.mapping_sha256,
        "run_manifest_sha256": freeze.run_manifest_sha256,
    }
    for field, expected in direct_bindings.items():
        if expected is None or getattr(record, field) != expected:
            raise FreezeVerificationError(f"reveal {field} does not match prediction freeze")
    if record.revealed_at_utc < freeze.created_at_utc:
        raise FreezeVerificationError("answer-key reveal predates the prediction freeze")
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
        return (
            encrypted_path.resolve(strict=True)
            .relative_to(directory.resolve(strict=True))
            .as_posix()
        )
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
    paired_prediction_freeze_path: str | Path | None = None,
    paired_plan_path: str | Path | None = None,
    paired_arm_id: str | None = None,
    expected_generation_seed_commitment_sha256: str | None = None,
    reveal_not_before_utc: datetime | None = None,
) -> RevealResult:
    """Verify frozen bytes, authenticate bindings, then reveal the key only in memory."""

    directory = Path(run_dir)
    resolved_freeze = (
        Path(freeze_path) if freeze_path is not None else directory / "prediction.freeze.json"
    )
    freeze = verify_frozen_predictions(
        directory,
        freeze_path=resolved_freeze,
        require_run_manifest=True,
    )
    metadata = SealingMetadata(
        experiment_id=freeze.experiment_id,
        blind_input_sha256=freeze.blind_input_sha256,
        model_sha256=freeze.model_sha256,
        question_bank_sha256=freeze.question_bank_sha256,
        mapping_sha256=freeze.mapping_sha256,
    )
    encrypted_path = Path(encrypted_answer_key_path)
    relative_envelope = _relative_envelope_path(directory, encrypted_path)
    try:
        encrypted_bytes = encrypted_path.read_bytes()
    except OSError as exc:
        raise AnswerKeySealingError("invalid encrypted answer-key envelope") from exc
    plaintext = decrypt_answer_key_envelope_bytes(
        encrypted_bytes,
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
    keyed_cases = answer_key_case_mapping(answer_key)
    target_set_sha256 = revealed_target_set_hash(keyed_cases)
    seed = answer_key.get("generation_seed")
    seed_commitment_sha256 = (
        generation_seed_commitment(seed)
        if isinstance(seed, int) and not isinstance(seed, bool)
        else None
    )
    complete_commitments = target_set_sha256 is not None and seed_commitment_sha256 is not None
    paired_values = (
        paired_prediction_freeze_path,
        paired_plan_path,
        paired_arm_id,
    )
    if any(value is not None for value in paired_values) and not all(
        value is not None for value in paired_values
    ):
        raise ValueError("paired reveal requires freeze, plan, and arm ID together")
    if paired_prediction_freeze_path is not None and not complete_commitments:
        raise ValueError("paired reveal requires complete authenticated target/seed commitments")
    if (
        expected_generation_seed_commitment_sha256 is not None
        and seed_commitment_sha256 != expected_generation_seed_commitment_sha256
    ):
        raise ValueError("revealed generation seed does not match the paired plan")
    reveal_time = revealed_at_utc or datetime.now(UTC)
    if reveal_time < freeze.created_at_utc:
        raise ValueError("answer-key reveal timestamp cannot predate prediction freeze")
    if reveal_not_before_utc is not None and reveal_time < reveal_not_before_utc:
        raise ValueError("answer-key reveal timestamp cannot predate paired freeze")
    manifest_sha256 = freeze.run_manifest_sha256
    if manifest_sha256 is None:
        raise FreezeVerificationError("prediction freeze lacks a run-manifest binding")
    record = RevealRecord(
        schema_version=("answer-key-reveal-v3" if complete_commitments else "answer-key-reveal-v2"),
        experiment_id=freeze.experiment_id,
        blind_input_sha256=freeze.blind_input_sha256,
        model_sha256=freeze.model_sha256,
        question_bank_sha256=freeze.question_bank_sha256,
        mapping_sha256=freeze.mapping_sha256,
        run_manifest_sha256=manifest_sha256,
        prediction_sha256=freeze.prediction_sha256,
        freeze_record_sha256=sha256_file(resolved_freeze),
        encrypted_answer_key_sha256=sha256_bytes(encrypted_bytes),
        encrypted_answer_key_file=relative_envelope,
        answer_key_payload_sha256=sha256_bytes(plaintext),
        revealed_target_set_sha256=(target_set_sha256 if complete_commitments else None),
        revealed_local_date_set_sha256=(
            revealed_local_date_set_hash(keyed_cases) if complete_commitments else None
        ),
        generation_seed_commitment_sha256=(
            seed_commitment_sha256 if complete_commitments else None
        ),
        paired_prediction_freeze_sha256=(
            sha256_file(paired_prediction_freeze_path)
            if paired_prediction_freeze_path is not None
            else None
        ),
        paired_plan_sha256=(
            sha256_file(paired_plan_path) if paired_plan_path is not None else None
        ),
        paired_arm_id=paired_arm_id,
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
    return RevealResult(
        answer_key=answer_key,
        record=record,
        freeze=freeze,
        _capability=_REVEAL_RESULT_CAPABILITY,
    )
