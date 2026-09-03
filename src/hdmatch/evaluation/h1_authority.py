"""Verification-only H1 human-content authority binding for Life Patterns.

This module does not adjudicate Human Design/astrology exposure and does not create
substantive measurement content. It accepts receipts that a separately authorized H1
process has already validated and binds those receipts to the exact content hash used by
the neutral-measurement ontology.

The underlying exposure policy is reused from the separately frozen Survey-v2 H1
adjudication contract. No model calls, exposure classification, or semantic repair occur
here.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import ConfigDict, BaseModel, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

from .neutral_measurement import HumanContentAuthorityReceipt

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
_ID_SUFFIX = r"[A-Za-z0-9_-]{16,}"

SURVEY_V2_H1_CONTRACT_VERSION = "survey-v2-h1-exposure-adjudication-contract-v1.0.0"
SURVEY_V2_H1_CONTRACT_SHA256 = "b26e8ca398eb805125ed4ea475243e1d0cb5134bee4c509dd29223355ff1b070"
SURVEY_V2_H1_REQUEST_SCHEMA_SHA256 = "1c7f55040d473fd8f4b47107b0edd296a448d9a5121845e907c6fd5eaf412240"
SURVEY_V2_H1_PROMPT_SHA256 = "236c3cfe5fbfc9ee3e03abfa49a3b7c5030276226a953778bb1dc0bef95f8100"
SURVEY_V2_H1_OUTPUT_SCHEMA_SHA256 = "9ec56a40cac3c6d31650ae5983083e74985b9ccca56bf2b616cba5787fb9c46c"
SURVEY_V2_H1_FREEZE_MANIFEST_SHA256 = "e920ac03ae51c811c2ed4fd54a7e7c28076c8769833c193ff40ea33d57337a80"
SURVEY_V2_H1_REQUIRED_MODEL_FAMILY = "gpt-5.6-sol"

ExposureClass = Literal[
    "shallow_or_incidental",
    "substantial_semantic_or_technical",
    "identity_defining_or_comprehensive",
    "intentionally_hd_derived",
    "ambiguous_or_insufficient",
]
H1Decision = Literal["eligible", "ineligible", "ambiguous_or_insufficient"]
EvidenceSufficiency = Literal["sufficient", "insufficient", "conflicting"]
RelevantWindowAssessment = Literal[
    "before_or_during_h1_authorship",
    "after_exact_h1_freeze_only",
    "no_exposure_in_relevant_window",
    "unknown",
]
SemanticOverlapAssessment = Literal[
    "none_affirmatively_established",
    "disjoint_technical_only",
    "material_or_foreseeable_overlap",
    "intentional_derivation",
    "unknown",
]
ReviewOutcome = Literal[
    "approved_for_validation",
    "approved_for_development_only",
    "needs_revision",
    "rejected",
]
ReviewerInfluence = Literal["method_only", "content_influencing"]


class AuthorityModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class SurveyV2H1SpecificationBinding(AuthorityModel):
    """Exact lock to the frozen H1 specification reused by Life Patterns."""

    contract_version: Literal[
        "survey-v2-h1-exposure-adjudication-contract-v1.0.0"
    ] = SURVEY_V2_H1_CONTRACT_VERSION
    contract_sha256: Literal[
        "b26e8ca398eb805125ed4ea475243e1d0cb5134bee4c509dd29223355ff1b070"
    ] = SURVEY_V2_H1_CONTRACT_SHA256
    request_schema_sha256: Literal[
        "1c7f55040d473fd8f4b47107b0edd296a448d9a5121845e907c6fd5eaf412240"
    ] = SURVEY_V2_H1_REQUEST_SCHEMA_SHA256
    prompt_sha256: Literal[
        "236c3cfe5fbfc9ee3e03abfa49a3b7c5030276226a953778bb1dc0bef95f8100"
    ] = SURVEY_V2_H1_PROMPT_SHA256
    output_schema_sha256: Literal[
        "9ec56a40cac3c6d31650ae5983083e74985b9ccca56bf2b616cba5787fb9c46c"
    ] = SURVEY_V2_H1_OUTPUT_SCHEMA_SHA256
    freeze_manifest_sha256: Literal[
        "e920ac03ae51c811c2ed4fd54a7e7c28076c8769833c193ff40ea33d57337a80"
    ] = SURVEY_V2_H1_FREEZE_MANIFEST_SHA256
    required_model_family: Literal["gpt-5.6-sol"] = SURVEY_V2_H1_REQUIRED_MODEL_FAMILY


class ValidatedH1AdjudicationPayload(AuthorityModel):
    """Receipt from an external validator of the frozen Survey-v2 H1 process.

    This object records a validation result. Constructing it does not itself prove the
    underlying human facts; downstream authority requires an eligible result plus all
    frozen validation attestations.
    """

    schema_version: Literal["life-patterns-h1-validated-adjudication-v1"] = (
        "life-patterns-h1-validated-adjudication-v1"
    )
    specification: SurveyV2H1SpecificationBinding
    h1_artifact_id: str = Field(pattern=rf"^H1A-{_ID_SUFFIX}$")
    h1_content_freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    request_id: str = Field(pattern=rf"^H1R-{_ID_SUFFIX}$")
    request_sha256: str = Field(pattern=_SHA256_PATTERN)
    evidence_packet_sha256: str = Field(pattern=_SHA256_PATTERN)
    raw_response_sha256: str = Field(pattern=_SHA256_PATTERN)
    parsed_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    subject_kind: Literal["human_author"] = "human_author"
    subject_role: Literal["construct_author"] = "construct_author"
    top_level_status: Literal["completed", "forbidden_input"]
    exposure_class: ExposureClass | None
    decision: H1Decision | None
    relevant_window_assessment: RelevantWindowAssessment | None
    semantic_overlap_assessment: SemanticOverlapAssessment | None
    evidence_sufficiency: EvidenceSufficiency | None
    missing_fact_codes: tuple[str, ...] = ()
    forced_decision: Literal[False] = False
    identity_blind_attestation: Literal[True] = True
    chart_blind_attestation: Literal[True] = True
    candidate_blind_attestation: Literal[True] = True
    h1_content_blind_attestation: Literal[True] = True
    no_external_tools_attestation: Literal[True] = True
    model_training_exposure_assessment: Literal["not_applicable"] = "not_applicable"
    request_schema_validated: Literal[True] = True
    output_schema_validated: Literal[True] = True
    semantic_contract_validated: Literal[True] = True
    evidence_custody_validated: Literal[True] = True
    transport_receipts_validated: Literal[True] = True
    model_family_validated: Literal[True] = True
    exact_content_binding_validated: Literal[True] = True
    validator_id: str = Field(min_length=1)
    validator_version: str = Field(min_length=1)
    validator_sha256: str = Field(pattern=_SHA256_PATTERN)
    validated_at_utc: datetime

    @field_validator("validated_at_utc")
    @classmethod
    def validation_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("H1 validation timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def completed_and_forbidden_states_are_coherent(self) -> ValidatedH1AdjudicationPayload:
        adjudication_fields = (
            self.exposure_class,
            self.decision,
            self.relevant_window_assessment,
            self.semantic_overlap_assessment,
            self.evidence_sufficiency,
        )
        if self.top_level_status == "forbidden_input":
            if any(value is not None for value in adjudication_fields) or self.missing_fact_codes:
                raise ValueError("forbidden-input H1 receipts cannot contain an adjudication decision")
        elif any(value is None for value in adjudication_fields):
            raise ValueError("completed H1 receipts require a complete adjudication result")
        return self


class ValidatedH1AdjudicationArtifact(AuthorityModel):
    schema_version: Literal["life-patterns-h1-validated-adjudication-artifact-v1"] = (
        "life-patterns-h1-validated-adjudication-artifact-v1"
    )
    validation_receipt_id: str = Field(pattern=r"^H1V-[0-9A-F]{20}$")
    validation_receipt_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: ValidatedH1AdjudicationPayload


class EligibleH1AuthorReference(AuthorityModel):
    validation_receipt_id: str = Field(pattern=r"^H1V-[0-9A-F]{20}$")
    validation_receipt_sha256: str = Field(pattern=_SHA256_PATTERN)
    request_id: str = Field(pattern=rf"^H1R-{_ID_SUFFIX}$")


class HumanAuthorshipProcessReceipt(AuthorityModel):
    schema_version: Literal["life-patterns-human-authorship-process-v1"] = (
        "life-patterns-human-authorship-process-v1"
    )
    h1_artifact_id: str = Field(pattern=rf"^H1A-{_ID_SUFFIX}$")
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    eligible_author_references: tuple[EligibleH1AuthorReference, ...] = Field(min_length=1)
    authorship_started_at_utc: datetime
    content_frozen_at_utc: datetime
    participant_evidence_available_to_authors: Literal[False] = False
    target_model_outputs_available_to_authors: Literal[False] = False
    content_authored_or_substantively_revised_only_by_listed_authors: Literal[True] = True
    post_freeze_change_requires_new_authorship_and_h1_receipts: Literal[True] = True

    @field_validator("authorship_started_at_utc", "content_frozen_at_utc")
    @classmethod
    def authorship_times_are_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("authorship timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def authorship_window_is_ordered(self) -> HumanAuthorshipProcessReceipt:
        if self.content_frozen_at_utc < self.authorship_started_at_utc:
            raise ValueError("content freeze cannot precede authorship start")
        ids = [row.validation_receipt_id for row in self.eligible_author_references]
        if len(ids) != len(set(ids)):
            raise ValueError("authorship receipt contains duplicate H1 validation receipts")
        return self


class HumanContentReviewReceipt(AuthorityModel):
    schema_version: Literal["life-patterns-human-content-review-v1"] = (
        "life-patterns-human-content-review-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    review_protocol_sha256: str = Field(pattern=_SHA256_PATTERN)
    review_outcome: ReviewOutcome
    reviewer_influence: ReviewerInfluence
    content_changed_during_review: bool
    content_influencing_reviewer_references: tuple[EligibleH1AuthorReference, ...] = ()
    reviewed_at_utc: datetime
    reliability_requirements_declared: Literal[True] = True
    construct_validity_not_established: Literal[True] = True

    @field_validator("reviewed_at_utc")
    @classmethod
    def review_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("content-review timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def review_state_is_coherent(self) -> HumanContentReviewReceipt:
        if self.review_outcome == "approved_for_validation" and self.content_changed_during_review:
            raise ValueError("changed content requires a new content hash and new review receipt")
        if self.reviewer_influence == "content_influencing":
            if not self.content_influencing_reviewer_references:
                raise ValueError("content-influencing reviewers require eligible H1 receipt references")
        elif self.content_influencing_reviewer_references:
            raise ValueError("method-only review cannot carry content-influencing H1 references")
        return self


class HumanContentAuthorityBundlePayload(AuthorityModel):
    schema_version: Literal["life-patterns-human-content-authority-bundle-v1"] = (
        "life-patterns-human-content-authority-bundle-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    adjudications: tuple[ValidatedH1AdjudicationArtifact, ...] = Field(min_length=1)
    authorship: HumanAuthorshipProcessReceipt
    content_review: HumanContentReviewReceipt
    authorized_at_utc: datetime
    does_not_establish_construct_validity_or_reliability: Literal[True] = True

    @field_validator("authorized_at_utc")
    @classmethod
    def authorization_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("content-authority timestamp must be timezone-aware")
        return value.astimezone(UTC)


class HumanContentAuthorityBundleArtifact(AuthorityModel):
    schema_version: Literal["life-patterns-human-content-authority-bundle-artifact-v1"] = (
        "life-patterns-human-content-authority-bundle-artifact-v1"
    )
    authority_bundle_id: str = Field(pattern=r"^LPH1-[0-9A-F]{20}$")
    authority_bundle_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: HumanContentAuthorityBundlePayload


def build_validated_h1_adjudication(
    payload: ValidatedH1AdjudicationPayload,
) -> ValidatedH1AdjudicationArtifact:
    digest = sha256_json(payload)
    return ValidatedH1AdjudicationArtifact(
        validation_receipt_id=f"H1V-{digest[:20].upper()}",
        validation_receipt_sha256=digest,
        payload=payload,
    )


def validated_h1_adjudication_integrity_errors(
    artifact: ValidatedH1AdjudicationArtifact,
) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(artifact.payload)
    if (
        artifact.validation_receipt_sha256 != digest
        or artifact.validation_receipt_id != f"H1V-{digest[:20].upper()}"
    ):
        errors.append("H1 validation receipt failed content-address verification")
    return tuple(errors)


def h1_eligibility_errors(artifact: ValidatedH1AdjudicationArtifact) -> tuple[str, ...]:
    errors = list(validated_h1_adjudication_integrity_errors(artifact))
    row = artifact.payload
    if row.top_level_status != "completed":
        errors.append("H1 adjudication did not complete")
    if row.decision != "eligible":
        errors.append("H1 adjudication did not return eligible")
    if row.evidence_sufficiency != "sufficient":
        errors.append("H1 adjudication lacks sufficient evidence")
    if row.missing_fact_codes:
        errors.append("H1 adjudication still has missing facts")
    if row.exposure_class == "shallow_or_incidental":
        if row.semantic_overlap_assessment != "none_affirmatively_established":
            errors.append("shallow/incidental eligibility lacks the frozen no-overlap assessment")
        if row.relevant_window_assessment not in {
            "before_or_during_h1_authorship",
            "no_exposure_in_relevant_window",
        }:
            errors.append("shallow/incidental eligibility has an invalid relevant-window result")
    elif row.exposure_class == "substantial_semantic_or_technical":
        if row.semantic_overlap_assessment != "disjoint_technical_only":
            errors.append("substantial exposure is eligible only under disjoint technical quarantine")
        if row.relevant_window_assessment != "before_or_during_h1_authorship":
            errors.append("eligible substantial exposure must use the frozen relevant-window branch")
    else:
        errors.append("H1 exposure class is not eligible under the frozen contract")
    return tuple(dict.fromkeys(errors))


def _reference_for(artifact: ValidatedH1AdjudicationArtifact) -> EligibleH1AuthorReference:
    return EligibleH1AuthorReference(
        validation_receipt_id=artifact.validation_receipt_id,
        validation_receipt_sha256=artifact.validation_receipt_sha256,
        request_id=artifact.payload.request_id,
    )


def authority_bundle_errors(payload: HumanContentAuthorityBundlePayload) -> tuple[str, ...]:
    errors: list[str] = []
    if payload.authorship.content_sha256 != payload.content_sha256:
        errors.append("authorship receipt does not bind authority content hash")
    if payload.content_review.content_sha256 != payload.content_sha256:
        errors.append("content-review receipt does not bind authority content hash")
    if payload.content_review.review_outcome != "approved_for_validation":
        errors.append("content review is not approved for validation")
    if payload.content_review.content_changed_during_review:
        errors.append("content changed during review and requires a new authority cycle")

    by_id = {row.validation_receipt_id: row for row in payload.adjudications}
    if len(by_id) != len(payload.adjudications):
        errors.append("authority bundle contains duplicate H1 validation receipts")

    for row in payload.adjudications:
        errors.extend(h1_eligibility_errors(row))
        if row.payload.h1_content_freeze_sha256 != payload.content_sha256:
            errors.append(
                f"H1 receipt {row.validation_receipt_id} does not bind authority content hash"
            )
        if row.payload.h1_artifact_id != payload.authorship.h1_artifact_id:
            errors.append(
                f"H1 receipt {row.validation_receipt_id} does not bind the authorship artifact"
            )

    required_refs = {
        row.validation_receipt_id: row
        for row in (
            *payload.authorship.eligible_author_references,
            *payload.content_review.content_influencing_reviewer_references,
        )
    }
    for ref_id, ref in required_refs.items():
        artifact = by_id.get(ref_id)
        if artifact is None:
            errors.append(f"authority bundle is missing referenced H1 receipt {ref_id}")
            continue
        if ref != _reference_for(artifact):
            errors.append(f"authority bundle H1 reference {ref_id} does not match its receipt")

    authorship_ids = {row.validation_receipt_id for row in payload.authorship.eligible_author_references}
    if not authorship_ids:
        errors.append("authority bundle has no eligible construct author")
    if not authorship_ids.issubset(by_id):
        errors.append("authorship references H1 receipts absent from the authority bundle")

    review_ids = {
        row.validation_receipt_id
        for row in payload.content_review.content_influencing_reviewer_references
    }
    if not review_ids.issubset(by_id):
        errors.append("content review references H1 receipts absent from the authority bundle")

    latest_validation = max(row.payload.validated_at_utc for row in payload.adjudications)
    if payload.authorship.content_frozen_at_utc < payload.authorship.authorship_started_at_utc:
        errors.append("authorship window is invalid")
    if payload.authorized_at_utc < latest_validation:
        errors.append("authority predates an H1 validation receipt")
    if payload.authorized_at_utc < payload.authorship.content_frozen_at_utc:
        errors.append("authority predates the content freeze")
    if payload.authorized_at_utc < payload.content_review.reviewed_at_utc:
        errors.append("authority predates content review")
    return tuple(dict.fromkeys(errors))


def build_human_content_authority_bundle(
    payload: HumanContentAuthorityBundlePayload,
) -> HumanContentAuthorityBundleArtifact:
    errors = authority_bundle_errors(payload)
    if errors:
        raise ValueError("invalid H1 authority bundle: " + "; ".join(errors))
    digest = sha256_json(payload)
    return HumanContentAuthorityBundleArtifact(
        authority_bundle_id=f"LPH1-{digest[:20].upper()}",
        authority_bundle_sha256=digest,
        payload=payload,
    )


def authority_bundle_integrity_errors(
    artifact: HumanContentAuthorityBundleArtifact,
) -> tuple[str, ...]:
    errors = list(authority_bundle_errors(artifact.payload))
    digest = sha256_json(artifact.payload)
    if (
        artifact.authority_bundle_sha256 != digest
        or artifact.authority_bundle_id != f"LPH1-{digest[:20].upper()}"
    ):
        errors.append("H1 authority bundle failed content-address verification")
    return tuple(dict.fromkeys(errors))


def human_content_authority_receipt_from_bundle(
    artifact: HumanContentAuthorityBundleArtifact,
) -> HumanContentAuthorityReceipt:
    errors = authority_bundle_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid H1 authority bundle: " + "; ".join(errors))
    adjudication_digest = sha256_json(artifact.payload.adjudications)
    return HumanContentAuthorityReceipt(
        content_sha256=artifact.payload.content_sha256,
        human_authorship_receipt_sha256=sha256_json(artifact.payload.authorship),
        exposure_adjudication_receipt_sha256=adjudication_digest,
        content_review_receipt_sha256=sha256_json(artifact.payload.content_review),
        authorized_at_utc=artifact.payload.authorized_at_utc,
    )


def write_h1_authority_bundle(
    path: str | Path,
    artifact: HumanContentAuthorityBundleArtifact,
) -> Path:
    errors = authority_bundle_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid H1 authority bundle: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_h1_authority_bundle(path: str | Path) -> HumanContentAuthorityBundleArtifact:
    raw = load_json_bytes(path, require_canonical=True)
    artifact = HumanContentAuthorityBundleArtifact.model_validate(raw)
    errors = authority_bundle_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid H1 authority bundle: " + "; ".join(errors))
    return artifact
