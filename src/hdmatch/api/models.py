"""Strict request and response schemas for the public HTTP boundary."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.model.symbolic_score import SymbolicScore
from hdmatch.schemas import BehavioralResponse, CandidateState, RankedDate, ScoredState
from hdmatch.search import AggregationMode


class ApiModel(BaseModel):
    """Immutable, extra-forbidding base for API records."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class ErrorIssue(ApiModel):
    location: tuple[str | int, ...] = ()
    message: str
    type: str


class ErrorDetail(ApiModel):
    code: str
    message: str
    issues: tuple[ErrorIssue, ...] = ()


class ErrorResponse(ApiModel):
    error: ErrorDetail


class ComponentHealth(ApiModel):
    status: Literal["ready", "unconfigured", "unresolved"]
    detail: str


class HealthResponse(ApiModel):
    status: Literal["ok"] = "ok"
    service: Literal["hdmatch-api"] = "hdmatch-api"
    api_version: str
    chart_engine: ComponentHealth
    symbolic_model: ComponentHealth
    answer_key_access: Literal["prohibited"] = "prohibited"


class EphemerisFileMetadata(ApiModel):
    name: str
    sha256: str
    size_bytes: int


class EphemerisMetadataResponse(ApiModel):
    provider: str
    library_version: str
    files: tuple[EphemerisFileMetadata, ...]
    calculation_flags: tuple[str, ...]
    coordinate_frame: str
    node_convention: str


class ChartEngineMetadataResponse(ApiModel):
    chart_engine_version: str
    ephemeris: EphemerisMetadataResponse
    mandala_constants_sha256: str
    bodygraph_constants_sha256: str
    design_target_arc_degrees: float
    design_time_tolerance_seconds: float
    design_arc_tolerance_degrees: float
    advanced_substructure_status: Literal["unavailable_unvalidated"]
    cross_engine_status: Literal["unverified"] = "unverified"


class ChartComponentMetadata(ApiModel):
    status: Literal["ready", "unconfigured"]
    chart_engine_version: str
    timezone_database_version: str
    ephemeris: EphemerisMetadataResponse | None = None
    cross_engine_status: Literal["unverified"] = "unverified"
    advanced_substructure_status: Literal["unavailable_unvalidated"] = (
        "unavailable_unvalidated"
    )


class SymbolicModelMetadata(ApiModel):
    status: Literal["ready", "unconfigured"]
    model_version: str | None = None
    mapping_library_sha256: str | None = None
    question_bank_version: str | None = None
    frozen_mapping_count: int = 0
    unresolved_mapping_count: int = 0


class ModelMetadataResponse(ApiModel):
    schema_version: Literal["api-model-metadata-v1"] = "api-model-metadata-v1"
    api_version: str
    code_commit: str
    chart: ChartComponentMetadata
    symbolic: SymbolicModelMetadata
    answer_key_access: Literal["prohibited"] = "prohibited"
    unavailable_capabilities: tuple[str, ...]


class ChartRequest(ApiModel):
    birth_utc: AwareDatetime
    design_time_tolerance_seconds: float = Field(default=0.01, gt=0.0, le=1.0)
    design_arc_tolerance_degrees: float = Field(default=1e-8, gt=0.0, le=1e-4)

    @field_validator("birth_utc")
    @classmethod
    def normalize_birth_utc(cls, value: datetime) -> datetime:
        return value.astimezone(UTC)


class ActivationResponse(ApiModel):
    body: CelestialBody
    side: Literal["personality", "design"]
    longitude: float = Field(ge=0.0, lt=360.0)
    gate: int = Field(ge=1, le=64)
    line: int = Field(ge=1, le=6)
    color: None = None
    tone: None = None
    base: None = None
    advanced_substructure_status: Literal["unavailable_unvalidated"] = (
        "unavailable_unvalidated"
    )


class ChartRecord(ApiModel):
    schema_version: Literal["chart-record-v1"] = "chart-record-v1"
    personality_utc: datetime
    design_utc: datetime
    complete_feature_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    personality_activations: dict[str, ActivationResponse]
    design_activations: dict[str, ActivationResponse]
    type: str
    strategy: str
    authority: str
    profile: str
    definition: str
    defined_centers: tuple[str, ...]
    channels: tuple[str, ...]
    engine_metadata: ChartEngineMetadataResponse


class BoundaryEventResponse(ApiModel):
    at_utc: datetime
    ephemeris_utc: datetime
    side: Literal["personality", "design"]
    body: CelestialBody
    resolution: Literal["gate", "line"]
    boundary_longitude: float
    before_gate: int
    before_line: int
    after_gate: int
    after_line: int
    root_tolerance_seconds: float


class ChartStateInterval(ApiModel):
    schema_version: Literal["chart-state-interval-v1"] = "chart-state-interval-v1"
    state_id: str = Field(pattern=r"^STATE-[a-f0-9]{24}$")
    start_utc: datetime
    end_utc: datetime
    representative_utc: datetime
    complete_feature_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    personality_activations: dict[str, ActivationResponse]
    design_utc: datetime
    design_activations: dict[str, ActivationResponse]
    type: str
    strategy: str
    authority: str
    profile: str
    definition: str
    defined_centers: tuple[str, ...]
    channels: tuple[str, ...]
    boundary_events: tuple[BoundaryEventResponse, ...]
    cross_engine_status: Literal["unverified"] = "unverified"


class StateIntervalsRequest(ApiModel):
    range_start_utc: AwareDatetime
    range_end_utc: AwareDatetime
    feature_layers: tuple[Literal["architecture", "gate_line"], ...] = (
        "architecture",
        "gate_line",
    )
    boundary_tolerance_seconds: float = Field(default=0.01, ge=0.001, le=1.0)

    @field_validator("range_start_utc", "range_end_utc")
    @classmethod
    def normalize_range_utc(cls, value: datetime) -> datetime:
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def valid_range_and_layers(self) -> StateIntervalsRequest:
        if self.range_end_utc <= self.range_start_utc:
            raise ValueError("range_end_utc must be after range_start_utc")
        if len(self.feature_layers) != 2 or set(self.feature_layers) != {
            "architecture",
            "gate_line",
        }:
            raise ValueError(
                "state intervals require the complete architecture and gate_line feature layers"
            )
        return self


class StateIntervalsResponse(ApiModel):
    schema_version: Literal["chart-state-intervals-v1"] = "chart-state-intervals-v1"
    range_start_utc: datetime
    range_end_utc: datetime
    intervals: tuple[ChartStateInterval, ...]
    engine_metadata: ChartEngineMetadataResponse


class SymbolicChartFeatures(ApiModel):
    type: str
    strategy: str
    authority: str
    profile: str
    defined_centers: tuple[str, ...] = ()


class SymbolicScoreRequest(ApiModel):
    chart_features: SymbolicChartFeatures
    responses: tuple[BehavioralResponse, ...]
    prevalence_by_anchor: dict[str, float]

    @field_validator("prevalence_by_anchor")
    @classmethod
    def valid_prevalence(cls, value: dict[str, float]) -> dict[str, float]:
        invalid = sorted(key for key, probability in value.items() if not 0.0 < probability <= 1.0)
        if invalid:
            raise ValueError(f"prevalence values must be in (0, 1]: {invalid}")
        return value


class SymbolicScoreResponse(ApiModel):
    schema_version: Literal["symbolic-score-response-v1"] = "symbolic-score-response-v1"
    model_version: str
    mapping_library_sha256: str
    score: SymbolicScore


class DateAggregationRequest(ApiModel):
    states: tuple[CandidateState, ...] = Field(min_length=1)
    scores: dict[str, ScoredState]
    mode: AggregationMode = AggregationMode.DURATION_WEIGHTED_EVIDENCE
    threshold_rubric_bits: float = 0.0

    @model_validator(mode="after")
    def one_exact_score_per_state(self) -> DateAggregationRequest:
        state_ids = [state.state_id for state in self.states]
        if len(state_ids) != len(set(state_ids)):
            raise ValueError("candidate state IDs must be unique")
        if set(self.scores) != set(state_ids):
            raise ValueError("scores must contain exactly one entry for every candidate state")
        return self


class DateAggregationResponse(ApiModel):
    schema_version: Literal["date-aggregation-response-v1"] = "date-aggregation-response-v1"
    results: tuple[RankedDate, ...]


class NextQuestionRequest(ApiModel):
    candidate_weights: tuple[float, ...] = Field(min_length=1)
    likelihoods_by_question: dict[str, tuple[dict[str, float], ...]] = Field(min_length=1)
    expected_reliability: dict[str, float] = Field(default_factory=dict)
    burden: dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def valid_likelihood_table(self) -> NextQuestionRequest:
        if any(weight < 0.0 for weight in self.candidate_weights):
            raise ValueError("candidate weights must be non-negative")
        if sum(self.candidate_weights) <= 0.0:
            raise ValueError("candidate weights must contain positive mass")
        for question_id, rows in self.likelihoods_by_question.items():
            if len(rows) != len(self.candidate_weights):
                raise ValueError(
                    f"question {question_id} must have one likelihood row per candidate"
                )
            for row in rows:
                if not row or any(probability < 0.0 for probability in row.values()):
                    raise ValueError(f"question {question_id} has an invalid likelihood row")
                if abs(sum(row.values()) - 1.0) > 1e-9:
                    raise ValueError(
                        f"question {question_id} likelihood rows must sum to one"
                    )
        if any(not 0.0 <= value <= 1.0 for value in self.expected_reliability.values()):
            raise ValueError("expected reliability must be within [0, 1]")
        if any(value < 0.0 for value in self.burden.values()):
            raise ValueError("question burden must be non-negative")
        return self


class QuestionUtilityResponse(ApiModel):
    question_id: str
    expected_information_gain: float
    adjusted_utility: float
    expected_reliability: float
    burden: float


class NextQuestionResponse(ApiModel):
    schema_version: Literal["next-question-response-v1"] = "next-question-response-v1"
    selection: QuestionUtilityResponse | None


def jsonable_error(response: ErrorResponse) -> dict[str, Any]:
    """Return a JSON-safe representation for exception handlers."""

    return response.model_dump(mode="json")
