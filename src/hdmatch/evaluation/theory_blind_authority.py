"""Theory-blind substantive-content authority contracts for Life Patterns.

This module generalizes the Life Patterns content-authority policy beyond the legacy
human-only H1 path. It does not author measurement constructs, run exposure adjudication,
contact humans, or establish construct validity. It records and validates provenance,
blindness, replication/reconciliation, calibration evidence, and review receipts.
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

AuthorKind = Literal["human", "ai", "mixed"]
PromptSeedLevel = Literal["minimally_seeded", "detailed_domain_seeded", "not_applicable"]
AuthorityStage = Literal["development_candidate", "validation_candidate"]
ValidationRoute = Literal[
    "human_human_benchmark",
    "statistically_justified_llm_substitution",
    "automated_measurement_instrument",
]
ContentReviewOutcome = Literal[
    "approved_development_only",
    "approved_validation_candidate",
    "needs_revision",
    "rejected",
]


class AuthorityModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class TheoryBlindDevelopmentProvenance(AuthorityModel):
    """Exact provenance for theory-blind substantive measurement development."""

    schema_version: Literal["life-patterns-theory-blind-development-provenance-v1"] = (
        "life-patterns-theory-blind-development-provenance-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    author_kind: AuthorKind
    authorship_context_sha256: str = Field(pattern=_SHA256_PATTERN)
    exact_prompt_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    exact_first_output_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    source_artifact_sha256: tuple[str, ...] = ()
    author_or_model_identity: str | None = None
    author_or_model_version: str | None = None
    fresh_session_or_workspace: bool | None = None
    prompt_author_theory_exposed: bool
    prompt_seed_level: PromptSeedLevel
    independent_replication_artifact_sha256: str | None = Field(
        default=None,
        pattern=_SHA256_PATTERN,
    )
    reconciliation_artifact_sha256: str | None = Field(
        default=None,
        pattern=_SHA256_PATTERN,
    )
    target_theory_material_available_in_authorship_context: Literal[False] = False
    target_model_outputs_available_in_authorship_context: Literal[False] = False
    birth_or_chart_data_available_in_authorship_context: Literal[False] = False
    pretraining_exposure_zero_not_claimed: Literal[True] = True
    generated_at_utc: datetime

    @field_validator("generated_at_utc")
    @classmethod
    def generated_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("development-provenance timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("source_artifact_sha256")
    @classmethod
    def source_hashes_are_valid(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("development provenance contains duplicate source artifacts")
        if any(len(row) != 64 or any(ch not in "0123456789abcdef" for ch in row) for row in value):
            raise ValueError("development source artifacts must be lowercase SHA-256 digests")
        return value

    @model_validator(mode="after")
    def authorship_fields_match_author_kind(self) -> TheoryBlindDevelopmentProvenance:
        if self.author_kind in {"ai", "mixed"} and (
            self.exact_prompt_sha256 is None or self.exact_first_output_sha256 is None
        ):
            raise ValueError("AI-influenced authorship requires exact prompt and first-output hashes")
        if self.author_kind == "human" and self.prompt_seed_level == "not_applicable":
            return self
        if self.prompt_seed_level == "not_applicable" and self.exact_prompt_sha256 is not None:
            raise ValueError("not_applicable prompt seed level cannot carry an exact prompt hash")
        return self

    @property
    def requires_independent_replication_for_validation(self) -> bool:
        return self.prompt_author_theory_exposed and self.prompt_seed_level == "detailed_domain_seeded"


class BlindHumanReliabilityReceipt(AuthorityModel):
    """Legacy-compatible conventional human-human development benchmark evidence."""

    schema_version: Literal["life-patterns-blind-human-reliability-receipt-v1"] = (
        "life-patterns-blind-human-reliability-receipt-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    ontology_artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    development_corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    reliability_report_sha256: str = Field(pattern=_SHA256_PATTERN)
    comparison_type: Literal["human_human"] = "human_human"
    pre_adjudication_outputs_frozen: Literal[True] = True
    birth_chart_model_blind: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    reliability_does_not_establish_construct_validity: Literal[True] = True
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def reliability_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("reliability-receipt timestamp must be timezone-aware")
        return value.astimezone(UTC)


class StatisticalLLMSubstitutionReceipt(AuthorityModel):
    """Evidence that an automated annotator may substitute for full human coding.

    The statistical analysis itself remains an external immutable artifact. This receipt
    records its exact specification, result, decision rule, and human-calibration provenance.
    """

    schema_version: Literal["life-patterns-statistical-llm-substitution-v1"] = (
        "life-patterns-statistical-llm-substitution-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    automated_human_calibration_artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    calibration_sample_manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    statistical_method_id: str = Field(min_length=1)
    statistical_test_spec_sha256: str = Field(pattern=_SHA256_PATTERN)
    statistical_test_result_sha256: str = Field(pattern=_SHA256_PATTERN)
    decision_rule_sha256: str = Field(pattern=_SHA256_PATTERN)
    substitution_decision: Literal["supported"] = "supported"
    human_auditor_count: int = Field(ge=1)
    human_first_pass_frozen_before_llm_exposure: Literal[True] = True
    route_frozen_before_target_model_scoring: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    substitution_does_not_establish_construct_validity: Literal[True] = True
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def substitution_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("LLM-substitution timestamp must be timezone-aware")
        return value.astimezone(UTC)


class AutomatedMeasurementInstrumentReceipt(AuthorityModel):
    """Preregistered automated-instrument route without a human-gold-standard claim."""

    schema_version: Literal["life-patterns-automated-measurement-instrument-v1"] = (
        "life-patterns-automated-measurement-instrument-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    instrument_spec_sha256: str = Field(pattern=_SHA256_PATTERN)
    automated_prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    model_or_ensemble_spec_sha256: str = Field(pattern=_SHA256_PATTERN)
    stability_report_sha256: str = Field(pattern=_SHA256_PATTERN)
    automated_human_calibration_artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    calibration_sample_manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    unresolved_units_policy_sha256: str = Field(pattern=_SHA256_PATTERN)
    sensitivity_analysis_spec_sha256: str = Field(pattern=_SHA256_PATTERN)
    automated_pass_count: int = Field(ge=3)
    human_auditor_count: int = Field(ge=1)
    human_first_pass_frozen_before_llm_exposure: Literal[True] = True
    route_frozen_before_target_model_scoring: Literal[True] = True
    explicit_no_human_gold_standard_equivalence_claim: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    instrument_validation_does_not_establish_construct_validity: Literal[True] = True
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def instrument_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("automated-instrument timestamp must be timezone-aware")
        return value.astimezone(UTC)


class TheoryBlindContentReviewReceipt(AuthorityModel):
    """Review of exact frozen content before development or validation promotion."""

    schema_version: Literal["life-patterns-theory-blind-content-review-v1"] = (
        "life-patterns-theory-blind-content-review-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    reviewer_kind: AuthorKind
    review_protocol_sha256: str = Field(pattern=_SHA256_PATTERN)
    review_notes_sha256: str = Field(pattern=_SHA256_PATTERN)
    review_outcome: ContentReviewOutcome
    content_changed_during_review: bool
    target_theory_blind: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    reviewed_at_utc: datetime
    review_does_not_establish_construct_validity: Literal[True] = True

    @field_validator("reviewed_at_utc")
    @classmethod
    def review_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("content-review timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validation_review_cannot_change_content(self) -> TheoryBlindContentReviewReceipt:
        if self.review_outcome == "approved_validation_candidate" and self.content_changed_during_review:
            raise ValueError("changed content requires a new content hash and new validation review")
        return self


class TheoryBlindContentAuthorityPayload(AuthorityModel):
    """Authority decision over one exact frozen content artifact."""

    schema_version: Literal["life-patterns-theory-blind-content-authority-v1"] = (
        "life-patterns-theory-blind-content-authority-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    authority_stage: AuthorityStage
    development_provenance: TheoryBlindDevelopmentProvenance
    human_reliability: BlindHumanReliabilityReceipt | None = None
    llm_substitution: StatisticalLLMSubstitutionReceipt | None = None
    automated_instrument: AutomatedMeasurementInstrumentReceipt | None = None
    content_review: TheoryBlindContentReviewReceipt
    authorized_at_utc: datetime
    exact_content_frozen: Literal[True] = True
    target_model_outputs_available_to_authority_process: Literal[False] = False
    does_not_establish_construct_validity_or_model_validity: Literal[True] = True

    @field_validator("authorized_at_utc")
    @classmethod
    def authority_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("content-authority timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @property
    def validation_route(self) -> ValidationRoute | None:
        if self.human_reliability is not None:
            return "human_human_benchmark"
        if self.llm_substitution is not None:
            return "statistically_justified_llm_substitution"
        if self.automated_instrument is not None:
            return "automated_measurement_instrument"
        return None

    @model_validator(mode="after")
    def authority_chronology_and_stage_are_coherent(self) -> TheoryBlindContentAuthorityPayload:
        if self.development_provenance.content_sha256 != self.content_sha256:
            raise ValueError("development provenance does not bind authority content")
        if self.content_review.content_sha256 != self.content_sha256:
            raise ValueError("content review does not bind authority content")
        if self.content_review.reviewed_at_utc < self.development_provenance.generated_at_utc:
            raise ValueError("content review cannot precede substantive content generation")
        latest_dependency = self.content_review.reviewed_at_utc
        evidence_count = sum(
            row is not None
            for row in (self.human_reliability, self.llm_substitution, self.automated_instrument)
        )

        if self.authority_stage == "development_candidate":
            if self.content_review.review_outcome != "approved_development_only":
                raise ValueError("development authority requires an approved-development-only review")
            if evidence_count:
                raise ValueError("development authority must not carry validation-route evidence")
        else:
            provenance = self.development_provenance
            if provenance.requires_independent_replication_for_validation and (
                provenance.independent_replication_artifact_sha256 is None
                or provenance.reconciliation_artifact_sha256 is None
            ):
                raise ValueError(
                    "validation authority requires independent replication and reconciliation for a detailed theory-exposed seed prompt"
                )
            if evidence_count != 1:
                raise ValueError("validation authority requires exactly one frozen validation-evidence route")
            if self.content_review.review_outcome != "approved_validation_candidate":
                raise ValueError("validation authority requires validation-candidate content review")

            if self.human_reliability is not None:
                if self.human_reliability.content_sha256 != self.content_sha256:
                    raise ValueError("human reliability receipt does not bind authority content")
                latest_dependency = max(latest_dependency, self.human_reliability.created_at_utc)
            elif self.llm_substitution is not None:
                if self.llm_substitution.content_sha256 != self.content_sha256:
                    raise ValueError("LLM-substitution receipt does not bind authority content")
                latest_dependency = max(latest_dependency, self.llm_substitution.created_at_utc)
            else:
                assert self.automated_instrument is not None
                if self.automated_instrument.content_sha256 != self.content_sha256:
                    raise ValueError("automated-instrument receipt does not bind authority content")
                latest_dependency = max(latest_dependency, self.automated_instrument.created_at_utc)

        if self.authorized_at_utc < latest_dependency:
            raise ValueError("content authority cannot precede its latest dependency")
        return self


class TheoryBlindContentAuthorityArtifact(AuthorityModel):
    schema_version: Literal["life-patterns-theory-blind-content-authority-artifact-v1"] = (
        "life-patterns-theory-blind-content-authority-artifact-v1"
    )
    authority_id: str = Field(pattern=r"^LPTB-[0-9A-F]{20}$")
    authority_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: TheoryBlindContentAuthorityPayload


class TheoryBlindContentAuthorityReceipt(AuthorityModel):
    """Compact exact-content receipt for later neutral-ontology integration."""

    schema_version: Literal["life-patterns-theory-blind-content-authority-receipt-v1"] = (
        "life-patterns-theory-blind-content-authority-receipt-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    authority_id: str = Field(pattern=r"^LPTB-[0-9A-F]{20}$")
    authority_sha256: str = Field(pattern=_SHA256_PATTERN)
    authority_stage: AuthorityStage
    validation_route: ValidationRoute | None = None
    authorized_at_utc: datetime

    @field_validator("authorized_at_utc")
    @classmethod
    def receipt_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("content-authority receipt timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def route_matches_stage(self) -> TheoryBlindContentAuthorityReceipt:
        if self.authority_stage == "development_candidate" and self.validation_route is not None:
            raise ValueError("development content-authority receipt cannot claim a validation route")
        if self.authority_stage == "validation_candidate" and self.validation_route is None:
            raise ValueError("validation content-authority receipt requires a validation route")
        return self


def build_theory_blind_content_authority(
    payload: TheoryBlindContentAuthorityPayload,
) -> TheoryBlindContentAuthorityArtifact:
    digest = sha256_json(payload)
    return TheoryBlindContentAuthorityArtifact(
        authority_id=f"LPTB-{digest[:20].upper()}",
        authority_sha256=digest,
        payload=payload,
    )


def theory_blind_content_authority_integrity_errors(
    artifact: TheoryBlindContentAuthorityArtifact,
) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(artifact.payload)
    if artifact.authority_sha256 != digest or artifact.authority_id != f"LPTB-{digest[:20].upper()}":
        errors.append("theory-blind content authority failed content-address verification")
    return tuple(errors)


def compact_theory_blind_content_authority_receipt(
    artifact: TheoryBlindContentAuthorityArtifact,
) -> TheoryBlindContentAuthorityReceipt:
    errors = theory_blind_content_authority_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid theory-blind content authority: " + "; ".join(errors))
    return TheoryBlindContentAuthorityReceipt(
        content_sha256=artifact.payload.content_sha256,
        authority_id=artifact.authority_id,
        authority_sha256=artifact.authority_sha256,
        authority_stage=artifact.payload.authority_stage,
        validation_route=artifact.payload.validation_route,
        authorized_at_utc=artifact.payload.authorized_at_utc,
    )


def write_theory_blind_content_authority(
    path: str | Path,
    artifact: TheoryBlindContentAuthorityArtifact,
) -> Path:
    errors = theory_blind_content_authority_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid theory-blind content authority: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_theory_blind_content_authority(path: str | Path) -> TheoryBlindContentAuthorityArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = TheoryBlindContentAuthorityArtifact.model_validate(cast(dict[str, Any], raw))
    errors = theory_blind_content_authority_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid theory-blind content authority: " + "; ".join(errors))
    return artifact
