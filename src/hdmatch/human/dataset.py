"""Versioned human-case import without exposing final-test labels to fitting code."""

from __future__ import annotations

import csv
import json
import math
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from hdmatch.chart.timezone import LocalTimeStatus, resolve_local_datetime
from hdmatch.schemas import BehavioralResponse
from hdmatch.util import sha256_file, sha256_json


class BirthRecordProvenance(BaseModel):
    """Caller-declared source and verification method without invented source categories."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    source_kind: str = Field(min_length=1)
    verification_method: str = Field(min_length=1)
    notes: str | None = None

    @field_validator("source_kind", "verification_method")
    @classmethod
    def reject_blank_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("birth-record provenance fields cannot be blank")
        return normalized


class VerifiedBirthRecord(BaseModel):
    """Verified civil tuple and its exact historical-IANA UTC resolution."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["verified-birth-record-v1"] = "verified-birth-record-v1"
    local_datetime: datetime
    birthplace: str = Field(min_length=1)
    iana_timezone: str = Field(min_length=1)
    resolved_utc: datetime
    timezone_fold: Literal[0, 1] | None = None
    precision_minutes: int = Field(
        ge=0,
        description="Symmetric UTC uncertainty radius; zero denotes an exact recorded instant.",
    )
    provenance: BirthRecordProvenance

    @field_validator("local_datetime")
    @classmethod
    def require_naive_local_datetime(cls, value: datetime) -> datetime:
        if value.tzinfo is not None:
            raise ValueError("birth local_datetime must be a naive civil tuple")
        return value

    @field_serializer("local_datetime")
    def serialize_local_datetime(self, value: datetime) -> str:
        return value.isoformat()

    @field_validator("resolved_utc")
    @classmethod
    def require_utc_instant(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("birth resolved_utc must be timezone-aware UTC")
        if value.utcoffset() != timedelta(0):
            raise ValueError("birth resolved_utc must use a zero UTC offset")
        return value.astimezone(UTC)

    @field_validator("birthplace", "iana_timezone")
    @classmethod
    def reject_blank_location_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("birthplace and IANA timezone cannot be blank")
        return normalized

    @model_validator(mode="after")
    def verify_timezone_resolution(self) -> VerifiedBirthRecord:
        resolution = resolve_local_datetime(self.local_datetime, self.iana_timezone)
        if resolution.status is LocalTimeStatus.NONEXISTENT:
            raise ValueError("birth local_datetime does not exist in the declared timezone")
        if resolution.status is LocalTimeStatus.AMBIGUOUS:
            if self.timezone_fold is None:
                raise ValueError("ambiguous birth local_datetime requires timezone_fold")
            candidates = tuple(
                item for item in resolution.candidates if item.fold == self.timezone_fold
            )
            if len(candidates) != 1:
                raise ValueError("timezone_fold does not resolve the birth local_datetime")
            expected_utc = candidates[0].utc
        else:
            if self.timezone_fold is not None:
                raise ValueError("timezone_fold is forbidden for an unambiguous local_datetime")
            expected_utc = resolution.candidates[0].utc
        if self.resolved_utc != expected_utc:
            raise ValueError("birth resolved_utc disagrees with historical IANA resolution")
        return self


def flatten_response_records(
    records: tuple[BehavioralResponse, ...],
) -> tuple[dict[str, str], dict[str, float]]:
    identifiers = [record.question_id for record in records]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("behavioral response question_id values must be unique per person")
    return (
        {record.question_id: record.answer for record in records},
        {record.question_id: record.measurement_reliability for record in records},
    )


class HumanCase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str = Field(min_length=1)
    cohort: Literal["development", "validation", "final_test", "unassigned"]
    responses: dict[str, str]
    response_reliability: dict[str, float] = Field(default_factory=dict)
    response_records: tuple[BehavioralResponse, ...] = ()
    chart_features: dict[str, Any]
    verified_birth_record: VerifiedBirthRecord | None = None
    birth_year: int | None = None
    birth_month: int | None = Field(default=None, ge=1, le=12)
    birth_day: int | None = Field(default=None, ge=1, le=31)
    documented_time_precision_minutes: int | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("participant_id")
    @classmethod
    def reject_blank_participant_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("participant_id cannot be blank")
        return normalized

    @model_validator(mode="before")
    @classmethod
    def populate_flattened_response_views(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        data = dict(value)
        raw_responses = data.get("responses")
        raw_records = data.get("response_records")
        if isinstance(raw_responses, (list, tuple)):
            if raw_records not in (None, (), []):
                raise ValueError("supply rich responses once, not in two fields")
            raw_records = raw_responses
            data["response_records"] = raw_records
            data["responses"] = {}
        if raw_records not in (None, (), []):
            assert raw_records is not None
            records = tuple(BehavioralResponse.model_validate(item) for item in raw_records)
            responses, reliability = flatten_response_records(records)
            supplied_responses = data.get("responses")
            if supplied_responses not in (None, {}) and supplied_responses != responses:
                raise ValueError("flattened responses disagree with typed response records")
            supplied_reliability = data.get("response_reliability")
            if supplied_reliability not in (None, {}) and supplied_reliability != reliability:
                raise ValueError(
                    "flattened response reliability disagrees with typed response records"
                )
            data["responses"] = responses
            data["response_reliability"] = reliability
        raw_birth = data.get("verified_birth_record")
        if raw_birth not in (None, {}):
            birth = VerifiedBirthRecord.model_validate(raw_birth)
            expected_birth_fields = {
                "birth_year": birth.local_datetime.year,
                "birth_month": birth.local_datetime.month,
                "birth_day": birth.local_datetime.day,
                "documented_time_precision_minutes": birth.precision_minutes,
            }
            for field, expected in expected_birth_fields.items():
                supplied = data.get(field)
                if supplied is not None and supplied != expected:
                    raise ValueError(f"{field} disagrees with verified birth record")
                data[field] = expected
        return data

    @model_validator(mode="after")
    def valid_response_reliability(self) -> HumanCase:
        unknown = set(self.response_reliability) - set(self.responses)
        if unknown:
            raise ValueError(f"reliability supplied for unanswered questions: {sorted(unknown)}")
        invalid = sorted(
            question
            for question, value in self.response_reliability.items()
            if not math.isfinite(value) or not 0.0 <= value <= 1.0
        )
        if invalid:
            raise ValueError(f"response reliability must be within [0, 1]: {invalid}")
        if self.response_records:
            responses, reliability = flatten_response_records(self.response_records)
            if responses != self.responses or reliability != self.response_reliability:
                raise ValueError("typed response records disagree with flattened response views")
        if self.verified_birth_record is not None:
            local = self.verified_birth_record.local_datetime
            legacy = (self.birth_year, self.birth_month, self.birth_day)
            if any(item is not None for item in legacy) and legacy != (
                local.year,
                local.month,
                local.day,
            ):
                raise ValueError("legacy birth date disagrees with verified birth record")
            if (
                self.documented_time_precision_minutes is not None
                and self.documented_time_precision_minutes
                != self.verified_birth_record.precision_minutes
            ):
                raise ValueError("legacy birth precision disagrees with verified birth record")
        return self

    @property
    def evidence_weights(self) -> dict[str, float]:
        """Return legacy reliability or rich confidence×reliability weights."""

        if not self.response_records:
            return self.response_reliability
        return {
            response.question_id: response.effective_confidence
            for response in self.response_records
        }


class HumanDataset(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-dataset-v1", "human-dataset-v2"] = "human-dataset-v1"
    questionnaire_version: str
    cases: tuple[HumanCase, ...]
    source_sha256: str | None = None
    partition: Literal["development", "validation", "final_test"] | None = None
    split_manifest_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    full_dataset_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def unique_people(self) -> HumanDataset:
        identifiers = [case.participant_id for case in self.cases]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError(
                "participant_id must be unique; merge a person's answers before import"
            )
        if self.schema_version == "human-dataset-v2":
            missing_responses = sorted(
                case.participant_id
                for case in self.cases
                if case.responses and not case.response_records
            )
            if missing_responses:
                raise ValueError(
                    "v2 human dataset requires typed response records: "
                    f"{missing_responses}"
                )
            missing_birth = sorted(
                case.participant_id
                for case in self.cases
                if case.verified_birth_record is None
            )
            if missing_birth:
                raise ValueError(
                    "v2 human dataset requires verified birth records: " f"{missing_birth}"
                )
        elif any(case.response_records or case.verified_birth_record for case in self.cases):
            raise ValueError("rich human records require schema_version human-dataset-v2")
        bindings = (
            self.partition,
            self.split_manifest_sha256,
            self.full_dataset_sha256,
        )
        if any(value is not None for value in bindings) and not all(
            value is not None for value in bindings
        ):
            raise ValueError("human partition bindings must be supplied together")
        if self.partition is not None and any(
            case.cohort != self.partition for case in self.cases
        ):
            raise ValueError("human partition cases must match its declared cohort")
        return self


def human_dataset_sha256(dataset: HumanDataset) -> str:
    """Hash v1 datasets with their pre-rich-schema shape and v2 datasets exactly."""

    payload = dataset.model_dump(mode="json")
    if dataset.schema_version == "human-dataset-v1":
        payload.pop("partition", None)
        payload.pop("split_manifest_sha256", None)
        payload.pop("full_dataset_sha256", None)
        for case in payload["cases"]:
            case.pop("response_records", None)
            case.pop("verified_birth_record", None)
    return sha256_json(payload)


def _from_rows(rows: Iterable[dict[str, Any]], questionnaire_version: str) -> HumanDataset:
    cases = tuple(HumanCase.model_validate(row) for row in rows)
    return HumanDataset(
        schema_version=(
            "human-dataset-v2"
            if any(case.response_records or case.verified_birth_record for case in cases)
            else "human-dataset-v1"
        ),
        questionnaire_version=questionnaire_version,
        cases=cases,
    )


def load_human_dataset(path: str | Path, questionnaire_version: str) -> HumanDataset:
    """Load JSON, JSONL, CSV, or Parquet records into the strict person-level schema."""

    source = Path(path)
    suffix = source.suffix.lower()
    if suffix == ".json":
        raw = json.loads(source.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and "cases" in raw:
            dataset = HumanDataset.model_validate(raw)
        elif isinstance(raw, list):
            dataset = _from_rows(raw, questionnaire_version)
        else:
            raise ValueError("JSON human dataset must be a list or HumanDataset object")
    elif suffix == ".jsonl":
        rows = [
            json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line
        ]
        dataset = _from_rows(rows, questionnaire_version)
    elif suffix == ".csv":
        with source.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        decoded: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            for field in ("responses", "response_reliability", "chart_features", "metadata"):
                item[field] = json.loads(item[field]) if item.get(field) else {}
            item["response_records"] = (
                json.loads(item["response_records"]) if item.get("response_records") else []
            )
            item["verified_birth_record"] = (
                json.loads(item["verified_birth_record"])
                if item.get("verified_birth_record")
                else None
            )
            integer_fields = (
                "birth_year",
                "birth_month",
                "birth_day",
                "documented_time_precision_minutes",
            )
            for field in integer_fields:
                item[field] = int(item[field]) if item.get(field) else None
            decoded.append(item)
        dataset = _from_rows(decoded, questionnaire_version)
    elif suffix in {".parquet", ".pq"}:
        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError as exc:  # pragma: no cover - optional dependency boundary
            raise RuntimeError("Parquet import requires the empirical extra") from exc
        rows = pd.read_parquet(source).to_dict(orient="records")
        dataset = _from_rows(rows, questionnaire_version)
    else:
        raise ValueError(f"unsupported human dataset format: {suffix}")
    if dataset.questionnaire_version != questionnaire_version:
        raise ValueError("human dataset questionnaire version does not match the import request")
    return dataset.model_copy(update={"source_sha256": sha256_file(source)})
