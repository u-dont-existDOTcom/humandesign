"""Validate and freeze the private auditor declaration for Life Patterns v2 calibration.

This module validates the auditor's own declaration and produces a public-safe hash receipt. It
cannot independently prove the declaration or real-world chronology; controlled handoff records
and preservation of the first-pass artifacts remain separate evidence.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json


class HumanAuditorAttestationV2Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentHumanAuditorAttestationV2(HumanAuditorAttestationV2Model):
    schema_version: Literal["life-patterns-human-auditor-attestation-v2"] = (
        "life-patterns-human-auditor-attestation-v2"
    )
    auditor_id: str = Field(min_length=1)
    independent_of_participant: Literal[True]
    participant_or_theory_exposed_owner: Literal[False]
    target_theory_blind: Literal[True]
    llm_outputs_available_before_first_pass: Literal[False]
    automated_consensus_available_before_first_pass: Literal[False]
    target_model_outputs_available: Literal[False]
    birth_or_chart_data_available: Literal[False]
    automated_coder_used_for_first_pass: Literal[False]
    human_facing_offline_ui_used: Literal[True]
    first_pass_completed_at_utc: datetime
    auditor_notes: str | None = None

    @field_validator("first_pass_completed_at_utc")
    @classmethod
    def completion_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("auditor completion timestamp must be timezone-aware")
        return value.astimezone(UTC)


class DevelopmentHumanAuditorAttestationReceiptPayloadV2(HumanAuditorAttestationV2Model):
    schema_version: Literal["life-patterns-human-auditor-attestation-receipt-v2"] = (
        "life-patterns-human-auditor-attestation-receipt-v2"
    )
    attestation_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    auditor_id_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    first_pass_completed_at_utc: datetime
    independent_of_participant_declared: Literal[True] = True
    participant_or_theory_exposed_owner_declared: Literal[False] = False
    target_theory_blind_declared: Literal[True] = True
    no_llm_outputs_before_first_pass_declared: Literal[True] = True
    no_automated_consensus_before_first_pass_declared: Literal[True] = True
    no_target_model_outputs_declared: Literal[True] = True
    no_birth_or_chart_data_declared: Literal[True] = True
    no_automated_coder_for_first_pass_declared: Literal[True] = True
    human_facing_offline_ui_used_declared: Literal[True] = True
    declaration_is_not_independent_proof: Literal[True] = True
    contains_auditor_identity: Literal[False] = False
    contains_auditor_notes: Literal[False] = False
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @field_validator("first_pass_completed_at_utc")
    @classmethod
    def receipt_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("attestation receipt timestamp must be timezone-aware")
        return value.astimezone(UTC)


class DevelopmentHumanAuditorAttestationReceiptArtifactV2(HumanAuditorAttestationV2Model):
    schema_version: Literal["life-patterns-human-auditor-attestation-receipt-artifact-v2"] = (
        "life-patterns-human-auditor-attestation-receipt-artifact-v2"
    )
    receipt_id: str = Field(pattern=r"^LPHA2-[0-9A-F]{20}$")
    receipt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    payload: DevelopmentHumanAuditorAttestationReceiptPayloadV2


def load_and_validate_human_auditor_attestation_v2(
    raw_attestation: bytes,
) -> DevelopmentHumanAuditorAttestationV2:
    """Parse the exact private declaration and fail closed on any ineligible state."""

    return DevelopmentHumanAuditorAttestationV2.model_validate_json(raw_attestation)


def build_human_auditor_attestation_receipt_v2(
    raw_attestation: bytes,
) -> DevelopmentHumanAuditorAttestationReceiptArtifactV2:
    attestation = load_and_validate_human_auditor_attestation_v2(raw_attestation)
    exact_attestation_sha256 = hashlib.sha256(raw_attestation).hexdigest()
    auditor_id_sha256 = hashlib.sha256(attestation.auditor_id.encode("utf-8")).hexdigest()
    payload = DevelopmentHumanAuditorAttestationReceiptPayloadV2(
        attestation_sha256=exact_attestation_sha256,
        auditor_id_sha256=auditor_id_sha256,
        first_pass_completed_at_utc=attestation.first_pass_completed_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentHumanAuditorAttestationReceiptArtifactV2(
        receipt_id=f"LPHA2-{digest[:20].upper()}",
        receipt_sha256=digest,
        payload=payload,
    )


def canonical_human_auditor_attestation_v2_bytes(
    attestation: DevelopmentHumanAuditorAttestationV2,
) -> bytes:
    """Canonical serialization helper for UI/export tests; raw submitted bytes remain preserved."""

    return canonical_json_bytes(attestation)


def human_auditor_attestation_receipt_v2_integrity_errors(
    receipt: DevelopmentHumanAuditorAttestationReceiptArtifactV2,
) -> tuple[str, ...]:
    digest = sha256_json(receipt.payload)
    if receipt.receipt_sha256 != digest or receipt.receipt_id != f"LPHA2-{digest[:20].upper()}":
        return ("human auditor attestation receipt v2 failed content-address verification",)
    return ()
