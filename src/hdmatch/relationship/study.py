"""Private-intake and pre-answer freeze contracts for relationship research.

This module deliberately separates participant contact/birth data from behavioral
answers. A confirmatory relationship session is not ready for Question 1 until every
required prediction layer reports ``computed`` and the resulting bundle is frozen.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, date, datetime, time
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StudyModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class BirthTimeSource(StrEnum):
    BIRTH_CERTIFICATE = "birth_certificate"
    HOSPITAL_RECORD = "hospital_record"
    PARENT_OR_FAMILY_MEMORY = "parent_or_family_memory"
    PERSONAL_MEMORY = "personal_memory"
    ESTIMATED = "estimated"
    UNKNOWN = "unknown"


class PredictionLayerStatus(StrEnum):
    COMPUTED = "computed"
    PENDING_ENGINE = "pending_engine"
    INSUFFICIENT_BIRTH_DATA = "insufficient_birth_data"
    UNAVAILABLE = "unavailable"


class NoisePolicyStatus(StrEnum):
    PENDING_AUTHORITATIVE_ARTIFACT = "pending_authoritative_artifact"
    ARTIFACT_BOUND = "artifact_bound"


class RelationshipBirthInput(StudyModel):
    """Private civil birth record for one member of a relationship pair."""

    birth_date: date
    local_time: time | None = None
    birthplace: str = Field(min_length=1, max_length=300)
    iana_timezone: str | None = Field(default=None, max_length=120)
    time_source: BirthTimeSource
    uncertainty_minutes: int | None = Field(default=None, ge=0, le=24 * 60)
    latitude: float | None = Field(default=None, ge=-90.0, le=90.0)
    longitude: float | None = Field(default=None, ge=-180.0, le=180.0)

    @model_validator(mode="after")
    def validate_time_uncertainty(self) -> RelationshipBirthInput:
        if self.local_time is None:
            if self.time_source is not BirthTimeSource.UNKNOWN:
                raise ValueError("missing local_time requires time_source='unknown'")
            if self.uncertainty_minutes is not None:
                raise ValueError("unknown birth time cannot have a numeric uncertainty window")
        elif self.time_source is BirthTimeSource.UNKNOWN:
            raise ValueError("time_source='unknown' requires local_time to be omitted")
        if self.uncertainty_minutes is not None and self.time_source is not BirthTimeSource.ESTIMATED:
            raise ValueError("uncertainty_minutes is only valid for estimated birth times")
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must be supplied together")
        return self


class RelationshipStudyIntake(StudyModel):
    """Private pre-behavior intake. Never serialize this record to the public repo."""

    contact_email: str | None = Field(default=None, max_length=320)
    respondent_birth: RelationshipBirthInput
    partner_birth: RelationshipBirthInput
    consent_to_store_private_research_data: Literal[True]
    consent_to_process_partner_birth_data: Literal[True]
    created_at_utc: datetime

    @field_validator("contact_email")
    @classmethod
    def validate_contact_email(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = normalize_email(value)
        local, sep, domain = normalized.rpartition("@")
        if not sep or not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise ValueError("contact_email must look like a valid email address")
        return normalized

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at_utc must be timezone-aware")
        return value.astimezone(UTC)

    @property
    def birth_input_sha256(self) -> str:
        return canonical_sha256(
            {
                "respondent_birth": self.respondent_birth.model_dump(mode="json"),
                "partner_birth": self.partner_birth.model_dump(mode="json"),
            }
        )

    @property
    def contact_email_lookup_sha256(self) -> str | None:
        if self.contact_email is None:
            return None
        return hashlib.sha256(self.contact_email.encode()).hexdigest()


class PredictionLayerFreeze(StudyModel):
    layer_id: str = Field(min_length=1)
    required_for_confirmatory: bool = True
    status: PredictionLayerStatus
    model_version: str = Field(min_length=1)
    model_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    payload: dict[str, Any] = Field(default_factory=dict)
    limitations: tuple[str, ...] = ()


class NoisePolicyBinding(StudyModel):
    status: NoisePolicyStatus
    source_path: str | None = None
    source_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    source_schema_version: str | None = None
    note: str


class RelationshipPredictionFreeze(StudyModel):
    schema_version: Literal["relationship-prediction-freeze-v1"] = (
        "relationship-prediction-freeze-v1"
    )
    session_id: str = Field(min_length=1)
    created_at_utc: datetime
    birth_input_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    layers: tuple[PredictionLayerFreeze, ...]
    noise_policy: NoisePolicyBinding
    questionnaire_version: str = Field(min_length=1)
    questionnaire_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    code_commit: str = Field(min_length=1)

    @field_validator("created_at_utc")
    @classmethod
    def normalize_freeze_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at_utc must be timezone-aware")
        return value.astimezone(UTC)

    @property
    def confirmatory_ready(self) -> bool:
        required = tuple(layer for layer in self.layers if layer.required_for_confirmatory)
        return bool(required) and all(
            layer.status is PredictionLayerStatus.COMPUTED for layer in required
        )

    @property
    def freeze_sha256(self) -> str:
        return canonical_sha256(self.model_dump(mode="json"))


class RelationshipStudyPreflight(StudyModel):
    """Participant-safe preflight summary: no raw email, birth tuple, chart, or prediction."""

    session_id: str
    contact_email_on_file: bool
    email_verification_status: Literal["not_configured", "pending", "verified"]
    birth_intake_complete: bool
    prediction_freeze_present: bool
    prediction_freeze_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    confirmatory_ready: bool
    prediction_layer_statuses: dict[str, PredictionLayerStatus]
    noise_policy_status: NoisePolicyStatus


def normalize_email(value: str) -> str:
    return value.strip().casefold()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bind_noise_policy(path: Path | None) -> NoisePolicyBinding:
    """Bind an authoritative noise artifact when supplied; never invent thresholds."""

    if path is None or not path.exists():
        return NoisePolicyBinding(
            status=NoisePolicyStatus.PENDING_AUTHORITATIVE_ARTIFACT,
            note=(
                "Final Survey-v2 noise policy is not bound yet; retry/corroboration/stopping "
                "thresholds must not be guessed."
            ),
        )
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    schema_version = None
    if isinstance(raw, dict):
        for key in ("schema_version", "version", "audit_version"):
            candidate = raw.get(key)
            if isinstance(candidate, str) and candidate:
                schema_version = candidate
                break
    return NoisePolicyBinding(
        status=NoisePolicyStatus.ARTIFACT_BOUND,
        source_path=str(path),
        source_sha256=file_sha256(path),
        source_schema_version=schema_version,
        note=(
            "Artifact identity is bound. Policy-threshold extraction belongs to a "
            "version-specific adapter once the final scoring schema is frozen."
        ),
    )


def public_preflight(
    *,
    session_id: str,
    intake: RelationshipStudyIntake | None,
    prediction_freeze: RelationshipPredictionFreeze | None,
    email_verification_status: Literal["not_configured", "pending", "verified"] = (
        "not_configured"
    ),
) -> RelationshipStudyPreflight:
    return RelationshipStudyPreflight(
        session_id=session_id,
        contact_email_on_file=bool(intake and intake.contact_email),
        email_verification_status=email_verification_status,
        birth_intake_complete=intake is not None,
        prediction_freeze_present=prediction_freeze is not None,
        prediction_freeze_sha256=(
            prediction_freeze.freeze_sha256 if prediction_freeze is not None else None
        ),
        confirmatory_ready=(
            prediction_freeze.confirmatory_ready if prediction_freeze is not None else False
        ),
        prediction_layer_statuses=(
            {layer.layer_id: layer.status for layer in prediction_freeze.layers}
            if prediction_freeze is not None
            else {}
        ),
        noise_policy_status=(
            prediction_freeze.noise_policy.status
            if prediction_freeze is not None
            else NoisePolicyStatus.PENDING_AUTHORITATIVE_ARTIFACT
        ),
    )
