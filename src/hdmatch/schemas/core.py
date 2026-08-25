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
    """One behavioral construct with current, longitudinal, and contextual evidence.

    ``answer`` remains the backwards-compatible summary/current categorical answer
    used by existing scorers. ``period_answers`` and ``context_answers`` preserve
    structured variation instead of flattening childhood/current or context-specific
    differences into one token. Raw nuance remains provenance until coded blind to
    chart state into reusable categories.
    """

    question_id: str
    cluster_id: str
    answer: str
    behavioral_confidence: float = Field(ge=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)
    example_text: str | None = None
    counterexample_text: str | None = None
    period_answers: dict[str, str] = Field(default_factory=dict)
    context_answers: dict[str, str] = Field(default_factory=dict)
    pattern_changed: bool | None = None
    change_period: str | None = None
    nuance_text: str | None = None

    @field_validator("period_answers", "context_answers")
    @classmethod
    def require_nonblank_structured_answers(
        cls,
        value: dict[str, str],
    ) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for key, answer in value.items():
            period_or_context = str(key).strip()
            categorical_answer = str(answer).strip()
            if not period_or_context or not categorical_answer:
                raise ValueError("structured behavioral answer keys/values cannot be blank")
            if period_or_context in normalized:
                raise ValueError("structured behavioral answer keys must be unique")
            normalized[period_or_context] = categorical_answer
        return normalized

    @field_validator("change_period", "nuance_text")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

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
