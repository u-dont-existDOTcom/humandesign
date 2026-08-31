"""Immutable participant-session records for the AstroHD interview harness."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from hdmatch.schemas import BehavioralResponse, ChartFeatures, ScoredState


class ParticipantModel(BaseModel):
    """Strict immutable base for participant-session records."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class SessionMode(StrEnum):
    SCIENTIFIC_BLIND = "scientific_blind"
    SELF_DISCOVERY = "self_discovery"


class SessionPhase(StrEnum):
    CONFIRMATORY_BLIND = "confirmatory_blind"
    CONFIRMATORY_LOCKED = "confirmatory_locked"
    REVEALED = "revealed"
    POSTHOC_EXPLORATORY = "posthoc_exploratory"
    FINALIZED = "finalized"


class RankScope(StrEnum):
    KNOWN_BIRTH_MONTH = "known_birth_month"
    CENTURY_GLOBAL = "century_global"


class EvidenceDomain(StrEnum):
    TRAIT = "trait"
    BEHAVIOR = "behavior"
    OUTCOME = "outcome"
    TIMING = "timing"
    ENVIRONMENT = "environment"
    CONVENTIONAL_COVARIATE = "conventional_covariate"

    @property
    def natal_ranking_eligible(self) -> bool:
        """Only latent traits/behaviors may enter the natal fingerprint score."""

        return self in {EvidenceDomain.TRAIT, EvidenceDomain.BEHAVIOR}


class ResearchLayer(StrEnum):
    NATAL_BEHAVIORAL_FINGERPRINT = "natal_behavioral_fingerprint"
    BEHAVIOR_TO_OUTCOME = "behavior_plus_environment_to_outcome"
    DIRECT_OUTCOME_INCREMENT = "chart_to_outcome_increment"
    TIMING_INCREMENT = "progression_or_transit_timing_increment"
    RESIDUAL_INCREMENT = "chart_residual_after_conventional_covariates"


class BirthIntake(ParticipantModel):
    """Civil birth tuple accepted only by the trusted intake/backend."""

    local_datetime: datetime
    birthplace: str = Field(min_length=1)
    iana_timezone: str = Field(min_length=1)
    fold: int | None = Field(default=None, ge=0, le=1)
    mode: SessionMode = SessionMode.SCIENTIFIC_BLIND
    ranking_scope: RankScope = RankScope.KNOWN_BIRTH_MONTH

    @field_validator("local_datetime")
    @classmethod
    def require_naive_wall_clock(cls, value: datetime) -> datetime:
        if value.tzinfo is not None and value.utcoffset() is not None:
            raise ValueError("local_datetime must be a naive civil wall-clock tuple")
        return value


class ResolvedBirth(ParticipantModel):
    supplied_local: datetime
    birthplace: str
    iana_timezone: str
    fold: int
    birth_utc: datetime
    utc_offset_seconds: int
    tzdb_version: str
    pre_standard_time_uncertain: bool = False

    @field_validator("supplied_local")
    @classmethod
    def supplied_local_is_naive(cls, value: datetime) -> datetime:
        if value.tzinfo is not None and value.utcoffset() is not None:
            raise ValueError("supplied_local must remain a naive civil tuple")
        return value

    @field_serializer("supplied_local")
    def serialize_supplied_local(self, value: datetime) -> str:
        """Canonical JSON cannot contain a naive datetime object; preserve it as ISO text."""

        return value.isoformat()

    @field_validator("birth_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("birth_utc must be timezone-aware")
        return value.astimezone(UTC)


class PredictionDimension(ParticipantModel):
    """One pre-answer AstroHD prediction that can later be compared with evidence."""

    question_id: str
    cluster_id: str
    canonical_answer: str
    support_answers: tuple[str, ...]
    contradiction_answers: tuple[str, ...] = ()
    behavioral_statements: tuple[str, ...] = ()
    mapping_ids: tuple[str, ...] = ()


class PredictionFreeze(ParticipantModel):
    """Immutable predictions, search universe, and provenance frozen before answers."""

    schema_version: Literal["participant-prediction-freeze-v2"] = "participant-prediction-freeze-v2"
    session_id: str
    created_at_utc: datetime
    birth: ResolvedBirth
    chart: ChartFeatures
    dimensions: tuple[PredictionDimension, ...]
    code_commit: str
    engine_fingerprint: str
    model_version: str
    model_sha256: str
    mapping_sha256: str
    question_bank_version: str
    question_bank_sha256: str
    ranking_scope: RankScope
    candidate_universe_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    candidate_universe_state_count: int = Field(ge=1)
    candidate_universe_utc_start: datetime
    candidate_universe_utc_end_exclusive: datetime
    candidate_universe_timezone: str = Field(min_length=1)
    primary_research_layer: ResearchLayer = ResearchLayer.NATAL_BEHAVIORAL_FINGERPRINT

    @field_validator(
        "created_at_utc",
        "candidate_universe_utc_start",
        "candidate_universe_utc_end_exclusive",
    )
    @classmethod
    def freeze_timestamp_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("freeze timestamps must be timezone-aware")
        return value.astimezone(UTC)


class SessionRecord(ParticipantModel):
    schema_version: Literal["participant-session-v1"] = "participant-session-v1"
    session_id: str = Field(pattern=r"^HD-[A-F0-9]{32}$")
    mode: SessionMode
    ranking_scope: RankScope
    created_at_utc: datetime
    prediction_freeze_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    primary_research_layer: ResearchLayer = ResearchLayer.NATAL_BEHAVIORAL_FINGERPRINT
    secondary_research_layers: tuple[ResearchLayer, ...] = (
        ResearchLayer.BEHAVIOR_TO_OUTCOME,
        ResearchLayer.DIRECT_OUTCOME_INCREMENT,
        ResearchLayer.TIMING_INCREMENT,
        ResearchLayer.RESIDUAL_INCREMENT,
    )

    @field_validator("created_at_utc")
    @classmethod
    def session_timestamp_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at_utc must be timezone-aware")
        return value.astimezone(UTC)


class EvidenceInput(ParticipantModel):
    """One atomic observation extracted from participant narrative."""

    domain: EvidenceDomain
    question_id: str | None = None
    cluster_id: str | None = None
    answer: str | None = None
    behavioral_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    measurement_reliability: float = Field(default=0.75, ge=0.0, le=1.0)
    narrative: str = Field(min_length=1)
    childhood_pattern: str | None = None
    adult_pattern: str | None = None
    contexts: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()
    example_text: str | None = None
    counterexample_text: str | None = None
    supersedes_evidence_id: str | None = None

    def scoring_response(self) -> BehavioralResponse | None:
        """Return scoreable natal evidence or None for outcomes/covariates/free text."""

        if not self.domain.natal_ranking_eligible:
            return None
        if self.question_id is None or self.cluster_id is None or self.answer is None:
            return None
        return BehavioralResponse(
            question_id=self.question_id,
            cluster_id=self.cluster_id,
            answer=self.answer,
            behavioral_confidence=self.behavioral_confidence,
            measurement_reliability=self.measurement_reliability,
            example_text=self.example_text,
            counterexample_text=self.counterexample_text,
        )


class EvidenceRecord(ParticipantModel):
    schema_version: Literal["participant-evidence-v1"] = "participant-evidence-v1"
    evidence_id: str
    session_id: str
    phase: Literal["confirmatory_blind", "posthoc_exploratory"]
    created_at_utc: datetime
    evidence: EvidenceInput

    @field_validator("created_at_utc")
    @classmethod
    def evidence_timestamp_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at_utc must be timezone-aware")
        return value.astimezone(UTC)


class ConfirmatoryLock(ParticipantModel):
    schema_version: Literal["participant-confirmatory-lock-v1"] = "participant-confirmatory-lock-v1"
    session_id: str
    locked_at_utc: datetime
    evidence_ids: tuple[str, ...]
    scoring_responses: tuple[BehavioralResponse, ...]
    scoring_responses_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    excluded_non_natal_evidence_count: int = Field(ge=0)

    @field_validator("locked_at_utc")
    @classmethod
    def lock_timestamp_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("locked_at_utc must be timezone-aware")
        return value.astimezone(UTC)


class RankingSnapshot(ParticipantModel):
    schema_version: Literal["participant-ranking-v1"] = "participant-ranking-v1"
    session_id: str
    analysis_kind: Literal["pre_reveal", "posthoc_final_profile"]
    ranking_scope: RankScope
    created_at_utc: datetime
    candidate_state_count: int = Field(ge=1)
    candidate_date_count: int = Field(ge=1)
    true_state_rank: float = Field(ge=1.0)
    true_state_percentile: float = Field(ge=0.0, le=100.0)
    true_date_rank: float = Field(ge=1.0)
    true_date_percentile: float = Field(ge=0.0, le=100.0)
    top_state_tie_count: int = Field(ge=1)
    top_date_tie_count: int = Field(ge=1)
    top_margin_rubric_bits: float
    actual_state_score: ScoredState
    scientific_status: Literal[
        "confirmatory_blind",
        "precommitted_self_discovery",
        "posthoc_exploratory_not_independent",
    ]
    caveat: str

    @field_validator("created_at_utc")
    @classmethod
    def ranking_timestamp_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at_utc must be timezone-aware")
        return value.astimezone(UTC)


class PublicProgress(ParticipantModel):
    """Safe pre-reveal progress. It never contains the true birth rank."""

    schema_version: Literal["participant-progress-v1"] = "participant-progress-v1"
    session_id: str
    phase: SessionPhase
    confirmatory_observation_count: int = Field(ge=0)
    scoreable_observation_count: int = Field(ge=0)
    non_natal_observation_count: int = Field(ge=0)
    scoreable_question_count: int = Field(ge=0)
    scoreable_coverage: float = Field(ge=0.0, le=1.0)
    candidate_state_count: int | None = Field(default=None, ge=1)
    top_state_tie_count: int | None = Field(default=None, ge=1)
    top_margin_rubric_bits: float | None = None
    true_birth_rank_concealed: Literal[True] = True


class NextInterviewQuestion(ParticipantModel):
    schema_version: Literal["participant-next-question-v1"] = "participant-next-question-v1"
    session_id: str
    question_id: str | None
    prompt: str
    response_format: str
    followups: tuple[str, ...] = ()
    expected_information_gain: float | None = None
    adjusted_utility: float | None = None
    allow_other: Literal[True] = True
    guidance: str = (
        "If the listed options are imperfect, answer in your own words. "
        "Describe context, exceptions, and childhood-to-adult changes when relevant."
    )


class PredictionComparison(ParticipantModel):
    question_id: str
    cluster_id: str
    predicted_answer: str
    observed_answer: str | None
    classification: Literal[
        "supported", "partially_supported", "contradicted", "insufficient_evidence"
    ]
    behavioral_statements: tuple[str, ...] = ()
    evidence_id: str | None = None


class ParticipantModelReceipt(ParticipantModel):
    """Public-safe provenance for the exact model frozen before this interview."""

    prediction_freeze_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    code_commit: str
    engine_fingerprint: str
    model_version: str
    model_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    mapping_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    question_bank_version: str
    question_bank_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    ranking_scope: RankScope
    candidate_universe_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    candidate_universe_state_count: int = Field(ge=1)


class RevealReport(ParticipantModel):
    schema_version: Literal["participant-reveal-v2"] = "participant-reveal-v2"
    session_id: str
    revealed_at_utc: datetime
    birth: ResolvedBirth
    chart: ChartFeatures
    confirmatory_ranking: RankingSnapshot
    prediction_comparisons: tuple[PredictionComparison, ...]
    model_receipt: ParticipantModelReceipt
    primary_test_statement: str = (
        "The natal confirmatory test uses only persistent trait/behavior evidence. "
        "Outcomes, event timing, environment, and conventional covariates are retained "
        "for separate incremental tests and do not improve this natal ranking."
    )

    @field_validator("revealed_at_utc")
    @classmethod
    def reveal_timestamp_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("revealed_at_utc must be timezone-aware")
        return value.astimezone(UTC)


class ExploratoryRankingReport(ParticipantModel):
    schema_version: Literal["participant-exploratory-ranking-v1"] = (
        "participant-exploratory-ranking-v1"
    )
    session_id: str
    ranking: RankingSnapshot
    final_profile_responses: tuple[BehavioralResponse, ...]
    changed_question_ids: tuple[str, ...]
    disclaimer: str = (
        "This ranking uses post-reveal profile refinement. It is useful for "
        "self-exploration and hypothesis generation but is not independent "
        "confirmatory evidence for astrology."
    )


class FinalParticipantReport(ParticipantModel):
    schema_version: Literal["participant-final-report-v1"] = "participant-final-report-v1"
    session_id: str
    mode: SessionMode
    confirmatory: RevealReport
    exploratory: ExploratoryRankingReport
    retained_secondary_evidence: tuple[EvidenceRecord, ...]
    research_layers: tuple[ResearchLayer, ...] = (
        ResearchLayer.NATAL_BEHAVIORAL_FINGERPRINT,
        ResearchLayer.BEHAVIOR_TO_OUTCOME,
        ResearchLayer.DIRECT_OUTCOME_INCREMENT,
        ResearchLayer.TIMING_INCREMENT,
        ResearchLayer.RESIDUAL_INCREMENT,
    )
