"""Core immutable records crossing chart, model, search, and experiment boundaries."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FrozenModel(BaseModel):
    """Strict immutable base for hash-stable records."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class Activation(FrozenModel):
    body: str
    side: Literal["personality", "design"]
    longitude: float = Field(ge=0.0, lt=360.0)
    gate: int = Field(ge=1, le=64)
    line: int = Field(ge=1, le=6)
    color: int | None = Field(default=None, ge=1, le=6)
    tone: int | None = Field(default=None, ge=1, le=6)
    base: int | None = Field(default=None, ge=1, le=5)


class ChartFeatures(FrozenModel):
    schema_version: Literal["chart-features-v1"] = "chart-features-v1"
    personality_utc: datetime
    design_utc: datetime
    type: str
    strategy: str
    authority: str
    profile: str
    definition: str
    defined_centers: tuple[str, ...] = ()
    channels: tuple[str, ...] = ()
    activations: dict[str, Activation]
    engine_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("personality_utc", "design_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("chart timestamps must be timezone-aware")
        return value.astimezone(UTC)


class LocalDateOverlap(FrozenModel):
    date: date
    seconds: float = Field(gt=0.0)


class CandidateState(FrozenModel):
    schema_version: Literal["candidate-state-v1"] = "candidate-state-v1"
    state_id: str
    start_utc: datetime
    end_utc: datetime
    chart_features_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    chart_features: ChartFeatures
    local_date_overlaps: tuple[LocalDateOverlap, ...]
    boundary_events: tuple[str, ...] = ()
    cross_engine_status: Literal["verified", "unverified", "disagreement"] = "unverified"

    @model_validator(mode="after")
    def validate_interval(self) -> CandidateState:
        if self.end_utc <= self.start_utc:
            raise ValueError("candidate-state interval must have positive duration")
        duration = (self.end_utc - self.start_utc).total_seconds()
        overlap = sum(item.seconds for item in self.local_date_overlaps)
        if abs(duration - overlap) > 1e-3:
            raise ValueError("local-date overlaps must cover the entire interval")
        return self


class BehavioralResponse(FrozenModel):
    question_id: str
    cluster_id: str
    answer: str
    behavioral_confidence: float = Field(ge=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)
    example_text: str | None = None
    counterexample_text: str | None = None

    @property
    def effective_confidence(self) -> float:
        return self.behavioral_confidence * self.measurement_reliability


class BlindCase(FrozenModel):
    schema_version: Literal["blind-case-v1"] = "blind-case-v1"
    case_id: str
    known_birth_year: int
    known_birth_month: int = Field(ge=1, le=12)
    birthplace: str
    iana_timezone: str
    responses: tuple[BehavioralResponse, ...]
    candidate_universe: Literal["known_month", "known_date"] = "known_month"
    known_birth_day: int | None = Field(default=None, ge=1, le=31)


class ScoredState(FrozenModel):
    state_id: str
    net_rubric_bits: float
    evidence_rubric_bits: float
    contradiction_rubric_bits: float
    detailed_support: float = Field(ge=0.0, le=100.0)
    core_fit: float = Field(ge=0.0, le=100.0)
    meaningful_contradictions: int = Field(ge=0)


class RankedDate(FrozenModel):
    local_date: date
    date_score: float
    date_rank: float = Field(ge=1.0)
    best_state: ScoredState
    duration_weighted_support: float
    tied: bool = False
