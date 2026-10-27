"""Separate, source-preserving metadata for a selected shared research study.

This record is not an interview, prediction freeze, chart, or scoring input. The
birth tuple stays in its existing private record; only its exact-byte hash is
linked here. No value is inferred from a missing answer or from a target model.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, write_new_bytes

Identifier = Annotated[str, Field(strict=True, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$")]
Sha256 = Annotated[str, Field(strict=True, pattern=r"^[0-9a-f]{64}$")]
Seconds = Annotated[float, Field(strict=True, ge=0, allow_inf_nan=False)]
SignedSeconds = Annotated[float, Field(strict=True, allow_inf_nan=False)]
KnowledgeAnswer = Literal["yes", "no", "unsure", "prefer_not_to_say", "unknown", "not_asked"]
FamiliarityAnswer = Literal[
    "none", "heard_of_it", "basic", "intermediate", "advanced",
    "unsure", "prefer_not_to_say", "unknown", "not_asked",
]
CollectionStage = Literal["trusted_intake_before_interview", "separate_post_freeze"]


class MetadataModel(BaseModel):
    """Forbid hidden target fields and preserve an immutable validated record."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class ReportedUncertaintyInterval(MetadataModel):
    """Source-stated bounds relative to the linked private record's nominal time.

    Offsets are signed seconds, not birth dates or times. Never synthesize bounds
    from ``stated_uncertainty_seconds`` or infer that a reported interval is
    symmetric. This helper records a report; it performs no chart calculation.
    """

    lower_offset_seconds: SignedSeconds
    upper_offset_seconds: SignedSeconds
    source: Literal["participant_statement", "source_record"]

    @model_validator(mode="after")
    def ordered_bounds(self) -> ReportedUncertaintyInterval:
        if self.lower_offset_seconds > self.upper_offset_seconds:
            raise ValueError("reported uncertainty interval bounds must be ordered")
        return self


class BirthQualityMetadata(MetadataModel):
    """Existing intake meanings, with missing precision retained as unknown."""

    time_source: Literal[
        "certificate", "hospital_record", "family_record", "memory", "rectified", "unknown"
    ] = "unknown"
    stated_uncertainty_seconds: Seconds | None = None
    reported_uncertainty_interval: ReportedUncertaintyInterval | None = None


class SystemKnowledgeMetadata(MetadataModel):
    """Prior knowledge labels only; never store a placement or profile value."""

    system_id: Identifier
    familiarity: FamiliarityAnswer = "unknown"
    own_profile_known: KnowledgeAnswer = "unknown"
    prior_personal_interpretation: KnowledgeAnswer = "unknown"


class SharedStudyIntakeMetadata(MetadataModel):
    """A private, consented metadata record for one declared study selection."""

    schema_version: Literal["shared-study-intake-metadata-v1"] = "shared-study-intake-metadata-v1"
    participant_id_pseudonym: Identifier
    study_id: Identifier
    birth_input_sha256: Sha256
    collection_stage: CollectionStage
    recorded_at_utc: datetime
    source: Literal[
        "participant_self_report", "participant_supplied_record",
        "researcher_transcription", "existing_private_record", "unknown",
    ] = "unknown"
    source_record_sha256: Sha256 | None = None
    consent_to_pseudonymous_research_record: StrictBool
    primary_record_sha256: Sha256 | None = None
    selected_system_ids: tuple[Identifier, ...] = Field(min_length=1)
    birth_quality: BirthQualityMetadata = Field(default_factory=BirthQualityMetadata)
    system_knowledge: tuple[SystemKnowledgeMetadata, ...] = ()

    @field_validator("recorded_at_utc", mode="before")
    @classmethod
    def reject_numeric_timestamp(cls, value: object) -> object:
        if not isinstance(value, (str, datetime)):
            raise ValueError("recorded_at_utc must be an explicit datetime, not a numeric epoch")
        return value

    @field_validator("recorded_at_utc")
    @classmethod
    def require_explicit_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("recorded_at_utc must include an explicit timezone")
        return value.astimezone(UTC)

    @field_validator("consent_to_pseudonymous_research_record")
    @classmethod
    def require_actual_consent(cls, value: bool) -> bool:
        if not value:
            raise ValueError("actual consent to this research metadata record is required")
        return value

    @model_validator(mode="after")
    def check_study_scope_and_stage(self) -> SharedStudyIntakeMetadata:
        if len(set(self.selected_system_ids)) != len(self.selected_system_ids):
            raise ValueError("selected_system_ids must not contain duplicates")
        supplied_ids = tuple(item.system_id for item in self.system_knowledge)
        if len(set(supplied_ids)) != len(supplied_ids):
            raise ValueError("system_knowledge must not contain duplicate system IDs")
        if not set(supplied_ids).issubset(self.selected_system_ids):
            raise ValueError("system_knowledge contains a system outside this study selection")
        if self.collection_stage == "separate_post_freeze":
            if self.primary_record_sha256 is None:
                raise ValueError("post-freeze metadata must link the frozen primary record hash")
        elif self.primary_record_sha256 is not None:
            raise ValueError("before-interview metadata cannot claim a primary freeze link")
        by_id = {item.system_id: item for item in self.system_knowledge}
        # Omission means unknown, not an observed denial and not proof it was unasked.
        ordered = tuple(
            by_id.get(system_id, SystemKnowledgeMetadata(system_id=system_id))
            for system_id in self.selected_system_ids
        )
        object.__setattr__(self, "system_knowledge", ordered)
        return self


def _unique_json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _reject_json_constant(_: str) -> None:
    raise ValueError("non-finite JSON constants are forbidden")


def parse_shared_study_intake_metadata(raw: str | bytes) -> SharedStudyIntakeMetadata:
    """Validate exact JSON without silently accepting duplicate object keys."""

    value = json.loads(
        raw, object_pairs_hook=_unique_json_pairs, parse_constant=_reject_json_constant
    )
    if not isinstance(value, dict):
        raise ValueError("metadata JSON must contain one object")
    return SharedStudyIntakeMetadata.model_validate(value)


def canonical_shared_intake_bytes(record: SharedStudyIntakeMetadata) -> bytes:
    """Use the repository's canonical JSON format, including explicit unknowns."""

    return canonical_json_bytes(record)


def write_shared_intake_metadata(path: str | Path, record: SharedStudyIntakeMetadata) -> Path:
    """Create a separate private file atomically; never overwrite an existing file."""

    destination = Path(path)
    if not destination.parent.is_dir():
        raise ValueError("the private output directory must already exist")
    return write_new_bytes(destination, canonical_shared_intake_bytes(record), mode=0o600)
