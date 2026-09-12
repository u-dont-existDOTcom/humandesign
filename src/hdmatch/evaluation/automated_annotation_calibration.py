"""Theory-blind automated-coding calibration receipts for Life Patterns.

These contracts support the LLM-primary development workflow. They preserve repeated
independent automated coding passes and a blind human calibration audit without claiming
that model self-consistency establishes correctness or construct validity.
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

_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class CalibrationModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class AutomatedCodingPassReceipt(CalibrationModel):
    schema_version: Literal["life-patterns-automated-coding-pass-v1"] = (
        "life-patterns-automated-coding-pass-v1"
    )
    pass_id: str = Field(min_length=1)
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    codebook_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    model_identity: str = Field(min_length=1)
    model_version: str | None = None
    output_sha256: str = Field(pattern=_SHA256_PATTERN)
    isolated_context: Literal[True] = True
    prior_pass_outputs_available: Literal[False] = False
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("automated coding pass timestamp must be timezone-aware")
        return value.astimezone(UTC)


class AutomatedCodingEnsembleReceipt(CalibrationModel):
    schema_version: Literal["life-patterns-automated-coding-ensemble-v1"] = (
        "life-patterns-automated-coding-ensemble-v1"
    )
    passes: tuple[AutomatedCodingPassReceipt, ...] = Field(min_length=3)
    consensus_rule_sha256: str = Field(pattern=_SHA256_PATTERN)
    consensus_report_sha256: str = Field(pattern=_SHA256_PATTERN)
    total_units: int = Field(ge=1)
    unanimous_units: int = Field(ge=0)
    majority_units: int = Field(ge=0)
    unresolved_units: int = Field(ge=0)
    self_consistency_does_not_establish_correctness: Literal[True] = True

    @model_validator(mode="after")
    def passes_bind_same_pipeline_and_counts_are_coherent(self) -> AutomatedCodingEnsembleReceipt:
        pass_ids = [row.pass_id for row in self.passes]
        if len(pass_ids) != len(set(pass_ids)):
            raise ValueError("automated coding ensemble contains duplicate pass IDs")
        first = self.passes[0]
        for row in self.passes[1:]:
            if row.corpus_sha256 != first.corpus_sha256:
                raise ValueError("automated coding passes must bind the same corpus")
            if row.codebook_sha256 != first.codebook_sha256:
                raise ValueError("automated coding passes must bind the same codebook")
            if row.coding_procedure_sha256 != first.coding_procedure_sha256:
                raise ValueError("automated coding passes must bind the same coding procedure")
            if row.prompt_sha256 != first.prompt_sha256:
                raise ValueError("automated coding passes must bind the same frozen prompt")
        if self.unanimous_units + self.majority_units + self.unresolved_units != self.total_units:
            raise ValueError("automated coding ensemble unit counts must sum to total_units")
        return self

    @property
    def corpus_sha256(self) -> str:
        return self.passes[0].corpus_sha256

    @property
    def codebook_sha256(self) -> str:
        return self.passes[0].codebook_sha256

    @property
    def coding_procedure_sha256(self) -> str:
        return self.passes[0].coding_procedure_sha256


class BlindHumanCalibrationAuditReceipt(CalibrationModel):
    schema_version: Literal["life-patterns-blind-human-calibration-audit-v1"] = (
        "life-patterns-blind-human-calibration-audit-v1"
    )
    auditor_id: str = Field(min_length=1)
    sample_manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    parent_corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    codebook_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    audit_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    llm_outputs_available_before_first_pass: Literal[False] = False
    target_theory_blind: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def audit_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("human calibration audit timestamp must be timezone-aware")
        return value.astimezone(UTC)


class AutomatedHumanCalibrationComparisonPayload(CalibrationModel):
    schema_version: Literal["life-patterns-automated-human-calibration-comparison-v1"] = (
        "life-patterns-automated-human-calibration-comparison-v1"
    )
    ensemble: AutomatedCodingEnsembleReceipt
    human_audit: BlindHumanCalibrationAuditReceipt
    comparison_report_sha256: str = Field(pattern=_SHA256_PATTERN)
    sampled_units: int = Field(ge=1)
    raw_applicability_agreement: float | None = Field(default=None, ge=0.0, le=1.0)
    raw_value_agreement: float | None = Field(default=None, ge=0.0, le=1.0)
    unresolved_sample_units: int = Field(ge=0)
    created_at_utc: datetime
    calibration_does_not_make_human_or_llm_infallible: Literal[True] = True
    does_not_establish_construct_validity: Literal[True] = True

    @field_validator("created_at_utc")
    @classmethod
    def comparison_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("calibration-comparison timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def audit_binds_ensemble_pipeline(self) -> AutomatedHumanCalibrationComparisonPayload:
        if self.human_audit.parent_corpus_sha256 != self.ensemble.corpus_sha256:
            raise ValueError("human calibration audit does not bind the ensemble corpus")
        if self.human_audit.codebook_sha256 != self.ensemble.codebook_sha256:
            raise ValueError("human calibration audit does not bind the ensemble codebook")
        if self.human_audit.coding_procedure_sha256 != self.ensemble.coding_procedure_sha256:
            raise ValueError("human calibration audit does not bind the ensemble coding procedure")
        if self.unresolved_sample_units > self.sampled_units:
            raise ValueError("unresolved calibration units cannot exceed sampled units")
        return self


class AutomatedHumanCalibrationComparisonArtifact(CalibrationModel):
    schema_version: Literal["life-patterns-automated-human-calibration-artifact-v1"] = (
        "life-patterns-automated-human-calibration-artifact-v1"
    )
    artifact_id: str = Field(pattern=r"^LPAC-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: AutomatedHumanCalibrationComparisonPayload


def build_automated_human_calibration_artifact(
    payload: AutomatedHumanCalibrationComparisonPayload,
) -> AutomatedHumanCalibrationComparisonArtifact:
    digest = sha256_json(payload)
    return AutomatedHumanCalibrationComparisonArtifact(
        artifact_id=f"LPAC-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def automated_human_calibration_integrity_errors(
    artifact: AutomatedHumanCalibrationComparisonArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPAC-{digest[:20].upper()}":
        return ("automated-human calibration artifact failed content-address verification",)
    return ()


def write_automated_human_calibration_artifact(
    path: str | Path,
    artifact: AutomatedHumanCalibrationComparisonArtifact,
) -> Path:
    errors = automated_human_calibration_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid automated-human calibration artifact: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_automated_human_calibration_artifact(
    path: str | Path,
) -> AutomatedHumanCalibrationComparisonArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = AutomatedHumanCalibrationComparisonArtifact.model_validate(cast(dict[str, Any], raw))
    errors = automated_human_calibration_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid automated-human calibration artifact: " + "; ".join(errors))
    return artifact
