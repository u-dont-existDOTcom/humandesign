"""Immutable post-freeze model-tournament contracts for Life Patterns.

This module deliberately does not execute models. It records participant authorization,
freezes exact comparison manifests, and explains why a manifest is or is not scientifically
execution-ready. The target behavioral result is never supplied to the builder.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

ScientificStatus = Literal[
    "confirmatory_predeclared",
    "development_only",
    "exploratory_posthoc",
]
ImplementationStatus = Literal["implemented", "planned_only"]
CohortRole = Literal["development", "validation", "untouched_final_validation"]
PreregistrationStatus = Literal[
    "confirmatory_preregistered",
    "development_protocol",
    "exploratory_posthoc",
]
RevealPolicy = Literal[
    "research_only_no_participant_reveal",
    "participant_reveal_after_locked_execution",
]
AuthorizationPurpose = Literal[
    "research_comparison",
    "research_comparison_and_participant_reveal",
]
OutputType = Literal[
    "ranked_candidates",
    "categorical_observables",
    "probabilistic_observables",
    "hybrid",
]

_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class TournamentModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class AnalysisAuthorizationPayload(TournamentModel):
    schema_version: Literal["life-patterns-analysis-authorization-v1"] = (
        "life-patterns-analysis-authorization-v1"
    )
    session_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    purpose: AuthorizationPurpose
    model_family_scope: tuple[str, ...] = Field(min_length=1)
    exact_birth_data_use_authorized: bool
    result_storage_authorized: bool
    authorized_at_utc: datetime
    declining_would_not_change_life_patterns_profile: Literal[True] = True

    @field_validator("authorized_at_utc")
    @classmethod
    def authorization_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("authorization timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("model_family_scope")
    @classmethod
    def unique_nonempty_family_scope(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(item.strip() for item in value)
        if any(not item for item in normalized):
            raise ValueError("authorized model families must be nonempty")
        if len(set(normalized)) != len(normalized):
            raise ValueError("authorized model families must be unique")
        return normalized


class AnalysisAuthorizationArtifact(TournamentModel):
    schema_version: Literal["life-patterns-analysis-authorization-artifact-v1"] = (
        "life-patterns-analysis-authorization-artifact-v1"
    )
    authorization_id: str = Field(pattern=r"^LPA-[0-9A-F]{20}$")
    authorization_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: AnalysisAuthorizationPayload


class ModelManifestEntry(TournamentModel):
    model_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    family: str = Field(min_length=1)
    scientific_status: ScientificStatus
    implementation_status: ImplementationStatus
    implementation_version: str = Field(min_length=1)
    implementation_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    adapter_id: str = Field(min_length=1)
    adapter_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    measurement_bridge_id: str = Field(min_length=1)
    measurement_bridge_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    scoring_contract_id: str = Field(min_length=1)
    scoring_contract_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    requires_birth_data: bool
    is_baseline: bool
    output_type: OutputType
    candidate_universe_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    candidate_universe_state_count: int | None = Field(default=None, ge=1)
    tuning_or_search_budget: str = Field(min_length=1)
    limitations: tuple[str, ...] = ()

    @model_validator(mode="after")
    def candidate_universe_fields_move_together(self) -> ModelManifestEntry:
        if (self.candidate_universe_sha256 is None) != (self.candidate_universe_state_count is None):
            raise ValueError(
                "candidate universe hash and state count must either both be present or both be absent"
            )
        return self


class MetricPlan(TournamentModel):
    schema_version: Literal["life-patterns-tournament-metrics-v1"] = (
        "life-patterns-tournament-metrics-v1"
    )
    primary_metric_ids: tuple[str, ...] = Field(min_length=1)
    secondary_metric_ids: tuple[str, ...] = ()
    proper_scoring_rule_ids: tuple[str, ...] = ()
    tie_policy: str = Field(min_length=1)
    missing_claim_policy: str = Field(min_length=1)
    rejected_claim_policy: str = Field(min_length=1)
    uncertain_claim_policy: str = Field(min_length=1)
    exclusion_policy: str = Field(min_length=1)
    behavioral_coverage_reported_separately: Literal[True] = True

    @field_validator("primary_metric_ids", "secondary_metric_ids", "proper_scoring_rule_ids")
    @classmethod
    def metric_ids_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(item.strip() for item in value)
        if any(not item for item in normalized):
            raise ValueError("metric identifiers must be nonempty")
        if len(set(normalized)) != len(normalized):
            raise ValueError("metric identifiers must be unique within each metric list")
        return normalized


class TournamentManifestPayload(TournamentModel):
    schema_version: Literal["life-patterns-tournament-manifest-v1"] = (
        "life-patterns-tournament-manifest-v1"
    )
    session_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    authorization_id: str = Field(pattern=r"^LPA-[0-9A-F]{20}$")
    authorization_sha256: str = Field(pattern=_SHA256_PATTERN)
    birth_input_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    civil_time_resolution_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    cohort_role: CohortRole
    preregistration_status: PreregistrationStatus
    reveal_policy: RevealPolicy
    model_roster: tuple[ModelManifestEntry, ...] = Field(min_length=1)
    metric_plan: MetricPlan
    runtime_code_commit: str = Field(min_length=7)
    target_results_supplied_to_builder: Literal[False] = False
    minimum_distinct_nonbaseline_families: int = Field(default=2, ge=1)
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def manifest_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("manifest timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("model_roster")
    @classmethod
    def model_ids_are_unique(
        cls,
        value: tuple[ModelManifestEntry, ...],
    ) -> tuple[ModelManifestEntry, ...]:
        ids = [entry.model_id for entry in value]
        if len(ids) != len(set(ids)):
            raise ValueError("model roster IDs must be unique")
        return value

    @model_validator(mode="after")
    def birth_artifact_fields_move_together(self) -> TournamentManifestPayload:
        if (self.birth_input_sha256 is None) != (self.civil_time_resolution_sha256 is None):
            raise ValueError(
                "birth-input hash and civil-time resolution hash must both be present or both absent"
            )
        return self


class TournamentManifestArtifact(TournamentModel):
    schema_version: Literal["life-patterns-tournament-manifest-artifact-v1"] = (
        "life-patterns-tournament-manifest-artifact-v1"
    )
    manifest_id: str = Field(pattern=r"^LPT-[0-9A-F]{20}$")
    manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: TournamentManifestPayload
    execution_ready: bool
    execution_blockers: tuple[str, ...]


def build_analysis_authorization(
    payload: AnalysisAuthorizationPayload,
) -> AnalysisAuthorizationArtifact:
    digest = sha256_json(payload)
    return AnalysisAuthorizationArtifact(
        authorization_id=f"LPA-{digest[:20].upper()}",
        authorization_sha256=digest,
        payload=payload,
    )


def analysis_authorization_integrity_errors(
    artifact: AnalysisAuthorizationArtifact,
) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(artifact.payload)
    expected_id = f"LPA-{digest[:20].upper()}"
    if artifact.authorization_sha256 != digest or artifact.authorization_id != expected_id:
        errors.append("analysis authorization artifact failed content-address verification")
    return tuple(errors)


def _missing_or_placeholder_sha(value: str | None) -> bool:
    return value is None or value == "0" * 64


def tournament_execution_blockers(
    payload: TournamentManifestPayload,
    authorization: AnalysisAuthorizationArtifact,
) -> tuple[str, ...]:
    blockers = list(analysis_authorization_integrity_errors(authorization))
    auth = authorization.payload
    if not auth.result_storage_authorized:
        blockers.append("participant did not authorize storage of model-analysis results")
    if payload.session_id != auth.session_id:
        blockers.append("manifest session does not match analysis authorization")
    if payload.freeze_id != auth.freeze_id or payload.freeze_sha256 != auth.freeze_sha256:
        blockers.append("manifest behavioral freeze does not match analysis authorization")
    if (
        payload.authorization_id != authorization.authorization_id
        or payload.authorization_sha256 != authorization.authorization_sha256
    ):
        blockers.append("manifest does not bind the supplied analysis authorization artifact")

    authorized_families = set(auth.model_family_scope)
    for entry in payload.model_roster:
        if entry.family not in authorized_families:
            blockers.append(
                f"model {entry.model_id} family {entry.family!r} is outside participant authorization"
            )

    if not any(entry.is_baseline for entry in payload.model_roster):
        blockers.append("model roster has no declared non-birth/context baseline")

    nonbaseline_families = {
        entry.family for entry in payload.model_roster if not entry.is_baseline
    }
    if len(nonbaseline_families) < payload.minimum_distinct_nonbaseline_families:
        blockers.append(
            "model roster does not contain enough distinct non-baseline model families for the declared comparison"
        )

    if payload.preregistration_status == "confirmatory_preregistered" and not any(
        entry.scientific_status == "confirmatory_predeclared" and not entry.is_baseline
        for entry in payload.model_roster
    ):
        blockers.append("confirmatory manifest has no confirmatory predeclared non-baseline model")

    if (
        payload.preregistration_status == "confirmatory_preregistered"
        and payload.cohort_role == "development"
    ):
        blockers.append("development cohort cannot support confirmatory validation status")

    birth_required = any(entry.requires_birth_data for entry in payload.model_roster)
    if birth_required:
        if not auth.exact_birth_data_use_authorized:
            blockers.append("participant did not authorize exact birth-data use")
        if payload.birth_input_sha256 is None or payload.civil_time_resolution_sha256 is None:
            blockers.append(
                "birth-dependent roster lacks pinned birth-input and civil-time-resolution artifacts"
            )

    if payload.reveal_policy == "participant_reveal_after_locked_execution" and (
        auth.purpose != "research_comparison_and_participant_reveal"
    ):
        blockers.append("participant-facing reveal is outside the authorized purpose")

    has_probabilistic_output = any(
        entry.output_type in {"probabilistic_observables", "hybrid"}
        for entry in payload.model_roster
    )
    if has_probabilistic_output and not payload.metric_plan.proper_scoring_rule_ids:
        blockers.append("probabilistic model output lacks a predeclared proper scoring rule")

    for entry in payload.model_roster:
        if entry.implementation_status != "implemented":
            blockers.append(f"model {entry.model_id} is planned only, not implemented")
        if _missing_or_placeholder_sha(entry.implementation_sha256):
            blockers.append(f"model {entry.model_id} lacks a pinned implementation hash")
        if _missing_or_placeholder_sha(entry.adapter_sha256):
            blockers.append(f"model {entry.model_id} lacks a pinned adapter hash")
        if _missing_or_placeholder_sha(entry.measurement_bridge_sha256):
            blockers.append(f"model {entry.model_id} lacks a pinned measurement-bridge hash")
        if _missing_or_placeholder_sha(entry.scoring_contract_sha256):
            blockers.append(f"model {entry.model_id} lacks a pinned scoring-contract hash")
        if entry.output_type == "ranked_candidates" and entry.candidate_universe_sha256 is None:
            blockers.append(f"ranked model {entry.model_id} lacks a pinned candidate universe")

    # Keep blocker ordering deterministic while removing duplicates.
    return tuple(dict.fromkeys(blockers))


def build_tournament_manifest(
    payload: TournamentManifestPayload,
    authorization: AnalysisAuthorizationArtifact,
) -> TournamentManifestArtifact:
    blockers = tournament_execution_blockers(payload, authorization)
    digest = sha256_json(payload)
    return TournamentManifestArtifact(
        manifest_id=f"LPT-{digest[:20].upper()}",
        manifest_sha256=digest,
        payload=payload,
        execution_ready=not blockers,
        execution_blockers=blockers,
    )


def tournament_manifest_integrity_errors(
    artifact: TournamentManifestArtifact,
    authorization: AnalysisAuthorizationArtifact,
) -> tuple[str, ...]:
    errors = list(analysis_authorization_integrity_errors(authorization))
    digest = sha256_json(artifact.payload)
    expected_id = f"LPT-{digest[:20].upper()}"
    if artifact.manifest_sha256 != digest or artifact.manifest_id != expected_id:
        errors.append("tournament manifest failed content-address verification")
    recomputed_blockers = tournament_execution_blockers(artifact.payload, authorization)
    if artifact.execution_ready != (not recomputed_blockers):
        errors.append("stored execution-ready flag disagrees with recomputed blockers")
    if artifact.execution_blockers != recomputed_blockers:
        errors.append("stored execution blockers disagree with recomputed blockers")
    return tuple(dict.fromkeys(errors))


def write_tournament_manifest(
    path: str | Path,
    artifact: TournamentManifestArtifact,
    authorization: AnalysisAuthorizationArtifact,
) -> Path:
    errors = tournament_manifest_integrity_errors(artifact, authorization)
    if errors:
        raise ValueError("invalid tournament manifest: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_tournament_manifest(
    path: str | Path,
    authorization: AnalysisAuthorizationArtifact,
) -> TournamentManifestArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = TournamentManifestArtifact.model_validate(raw)
    errors = tournament_manifest_integrity_errors(artifact, authorization)
    if errors:
        raise ValueError("invalid tournament manifest: " + "; ".join(errors))
    return artifact


def write_analysis_authorization(
    path: str | Path,
    artifact: AnalysisAuthorizationArtifact,
) -> Path:
    errors = analysis_authorization_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid analysis authorization: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_analysis_authorization(path: str | Path) -> AnalysisAuthorizationArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = AnalysisAuthorizationArtifact.model_validate(cast(dict[str, Any], raw))
    errors = analysis_authorization_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid analysis authorization: " + "; ".join(errors))
    return artifact
