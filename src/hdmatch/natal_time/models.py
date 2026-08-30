"""Strict immutable records for natal-time evidence and state transitions."""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.util import sha256_json

SHA256_PATTERN = r"^[a-f0-9]{64}$"
EVIDENCE_ID_PATTERN = r"^NTE-[A-F0-9]{24}$"
LINEAGE_ID_PATTERN = r"^NTL-[A-F0-9]{24}$"


class NatalTimeModel(BaseModel):
    """Extra-forbidding immutable base for every scientific object."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class EvidenceSource(StrEnum):
    DOCUMENTARY = "documentary"
    MEMORY = "memory"
    EXPLICIT_CANDIDATE_DATE_SET = "explicit_candidate_date_set"


class DocumentaryVerification(StrEnum):
    NOT_APPLICABLE = "not_applicable"
    PARTICIPANT_REPORTED = "participant_reported"
    INDEPENDENTLY_VERIFIED = "independently_verified"


class Weekday(StrEnum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @classmethod
    def from_date(cls, value: date) -> Weekday:
        return tuple(cls)[value.weekday()]


class WeekdayAnswerStatus(StrEnum):
    REMEMBERED = "remembered"
    NOT_REMEMBERED = "not_remembered"
    UNKNOWN = "unknown"


class WeekdayRelation(StrEnum):
    UNAVAILABLE = "unavailable"
    CONCORDANT = "concordant"
    CONFLICT = "conflict"
    MIXED = "mixed"


class EvidenceState(StrEnum):
    DOCUMENTARY_WEEKDAY_UNAVAILABLE = "documentary_weekday_unavailable"
    DOCUMENTARY_CONCORDANT = "documentary_concordant"
    DOCUMENTARY_WEEKDAY_CONFLICT = "documentary_weekday_conflict"
    MEMORY_DATE_UNVERIFIED = "memory_date_unverified"
    MEMORY_CONCORDANT = "memory_concordant"
    BIRTH_DATE_UNCERTAIN = "birth_date_uncertain"
    UNRESOLVED_DOCUMENTARY_CONFLICT = "unresolved_documentary_conflict"
    CANDIDATE_DATE_SET_CONFIRMED = "candidate_date_set_confirmed"


class DateEvidence(NatalTimeModel):
    schema_version: Literal["natal-date-evidence-v1"] = "natal-date-evidence-v1"
    evidence_id: str = Field(pattern=EVIDENCE_ID_PATTERN)
    asserted_date: date
    source: EvidenceSource
    documentary_verification: DocumentaryVerification
    entered_at_utc: datetime
    entered_how: str = Field(min_length=1, max_length=120)
    supplements_evidence_id: str | None = Field(default=None, pattern=EVIDENCE_ID_PATTERN)
    supersedes_evidence_id: str | None = Field(default=None, pattern=EVIDENCE_ID_PATTERN)

    @field_validator("entered_at_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("evidence timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def valid_source_and_verification(self) -> DateEvidence:
        if self.source is EvidenceSource.EXPLICIT_CANDIDATE_DATE_SET:
            raise ValueError("candidate-date sets use CandidateDateSetEvidence")
        if self.source is EvidenceSource.DOCUMENTARY:
            if self.documentary_verification is DocumentaryVerification.NOT_APPLICABLE:
                raise ValueError("documentary evidence must declare its verification status")
        elif self.documentary_verification is not DocumentaryVerification.NOT_APPLICABLE:
            raise ValueError("memory evidence cannot claim documentary verification")
        return self


class WeekdayEvidence(NatalTimeModel):
    schema_version: Literal["natal-weekday-evidence-v1"] = "natal-weekday-evidence-v1"
    evidence_id: str = Field(pattern=EVIDENCE_ID_PATTERN)
    source: Literal[EvidenceSource.MEMORY] = EvidenceSource.MEMORY
    answer_status: WeekdayAnswerStatus
    asserted_weekday: Weekday | None = None
    entered_at_utc: datetime
    entered_how: str = Field(min_length=1, max_length=120)
    locked_at_utc: datetime
    server_lock_sequence: int = Field(ge=1)
    implied_weekday_revealed_before_lock: Literal[False] = False
    supplements_evidence_id: str | None = Field(default=None, pattern=EVIDENCE_ID_PATTERN)
    supersedes_evidence_id: str | None = Field(default=None, pattern=EVIDENCE_ID_PATTERN)

    @field_validator("entered_at_utc", "locked_at_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("weekday timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def valid_answer(self) -> WeekdayEvidence:
        if self.answer_status is WeekdayAnswerStatus.REMEMBERED:
            if self.asserted_weekday is None:
                raise ValueError("a remembered weekday requires an asserted value")
        elif self.asserted_weekday is not None:
            raise ValueError("an unavailable weekday answer cannot assert a weekday")
        if self.locked_at_utc < self.entered_at_utc:
            raise ValueError("weekday lock cannot predate entry")
        return self


class CandidateDateSetEvidence(NatalTimeModel):
    schema_version: Literal["natal-candidate-date-set-v1"] = "natal-candidate-date-set-v1"
    evidence_id: str = Field(pattern=EVIDENCE_ID_PATTERN)
    source: Literal[EvidenceSource.EXPLICIT_CANDIDATE_DATE_SET] = (
        EvidenceSource.EXPLICIT_CANDIDATE_DATE_SET
    )
    candidate_dates: tuple[date, ...] = Field(min_length=1)
    candidate_ordering: Literal["none"] = "none"
    declared_date_evidence_ids: tuple[str, ...] = Field(min_length=1)
    confirmed_at_utc: datetime
    confirmed_how: str = Field(min_length=1, max_length=120)
    weekday_conflict_disclosed_before_confirmation: Literal[True] = True
    supersedes_evidence_id: str | None = Field(default=None, pattern=EVIDENCE_ID_PATTERN)

    @field_validator("candidate_dates")
    @classmethod
    def unique_canonical_dates(cls, value: tuple[date, ...]) -> tuple[date, ...]:
        if len(set(value)) != len(value):
            raise ValueError("candidate dates must be unique")
        return tuple(sorted(value))

    @field_validator("declared_date_evidence_ids")
    @classmethod
    def unique_evidence_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("declared date evidence IDs must be unique")
        for evidence_id in value:
            if not __import__("re").fullmatch(EVIDENCE_ID_PATTERN, evidence_id):
                raise ValueError("candidate set references a malformed evidence ID")
        return tuple(sorted(value))

    @field_validator("confirmed_at_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("candidate-set timestamp must be timezone-aware")
        return value.astimezone(UTC)


class EvidenceLineage(NatalTimeModel):
    schema_version: Literal["natal-evidence-lineage-v1"] = "natal-evidence-lineage-v1"
    lineage_id: str = Field(pattern=LINEAGE_ID_PATTERN)
    version: int = Field(ge=1)
    date_evidence: tuple[DateEvidence, ...] = Field(min_length=1)
    weekday_evidence: WeekdayEvidence
    candidate_date_set: CandidateDateSetEvidence | None = None
    supersedes_lineage_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def unique_evidence_ids(self) -> EvidenceLineage:
        ids = [item.evidence_id for item in self.date_evidence]
        ids.append(self.weekday_evidence.evidence_id)
        if self.candidate_date_set is not None:
            ids.append(self.candidate_date_set.evidence_id)
            unknown = set(self.candidate_date_set.declared_date_evidence_ids) - {
                item.evidence_id for item in self.date_evidence
            }
            if unknown:
                raise ValueError(
                    f"candidate set references unknown date evidence: {sorted(unknown)}"
                )
        if len(ids) != len(set(ids)):
            raise ValueError("evidence IDs must be unique within one lineage")
        if self.version == 1 and self.supersedes_lineage_sha256 is not None:
            raise ValueError("version 1 cannot supersede another lineage")
        if self.version > 1 and self.supersedes_lineage_sha256 is None:
            raise ValueError("later lineage versions must bind the superseded digest")
        return self

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


class DateWeekdayFact(NatalTimeModel):
    candidate_date: date
    implied_weekday: Weekday
    remembered_weekday_matches: bool | None


class EvidenceAssessment(NatalTimeModel):
    schema_version: Literal["natal-evidence-assessment-v1"] = "natal-evidence-assessment-v1"
    lineage_sha256: str = Field(pattern=SHA256_PATTERN)
    state: EvidenceState
    weekday_relation: WeekdayRelation
    operative_dates: tuple[date, ...]
    candidate_ordering: Literal["none"] = "none"
    date_weekday_facts: tuple[DateWeekdayFact, ...]
    enumeration_allowed: bool
    requires_candidate_date_set: bool
    original_declared_dates_preserved: Literal[True] = True
    agreement_adds_precision: Literal[False] = False
    date_was_auto_corrected: Literal[False] = False
