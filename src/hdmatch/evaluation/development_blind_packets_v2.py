"""Render recurrence-corrected private theory-blind development coder packets.

V2 packet rendering is additive. It binds the recurrence policy and coding manual v2 while
reusing the exact pre-label calibration unit selection. Private participant text remains in
private packets; public receipts remain hash/identity/count only.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json, write_new_bytes

from .development_blind_packets import BlindCoderRole, BlindEvidenceKind, BlindTask
from .development_calibration_sampling import (
    development_calibration_integrity_errors,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from .development_private_preparation import EPISODE_TRANSPORT_PROMPT_REL
from .development_private_preparation_v2 import (
    HUMAN_CALIBRATION_PROMPT_V2_REL,
    SERIES_TRANSPORT_PROMPT_V2_REL,
    PrivateDevelopmentPreparationV2,
)
from .neutral_measurement import OntologyReleaseArtifact
from .non_action_resolution import (
    NonActionAmbiguityResolutionArtifact,
    ResolvedCodebookViewArtifactV2,
)
from .reconciled_codebook_source import ReconciledCodebookSourceArtifact
from .resolved_development_stack import file_sha256
from .resolved_development_stack_v2 import CODING_MANUAL_V2_REL, RECURRENCE_POLICY_V2_REL
from .structured_annotation_v2 import StructuredCodingProcedureArtifactV2


class BlindDevelopmentPacketV2Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class BlindDevelopmentPacketPayloadV2(BlindDevelopmentPacketV2Model):
    schema_version: Literal["life-patterns-blind-development-coder-packet-v2"] = (
        "life-patterns-blind-development-coder-packet-v2"
    )
    coder_role: BlindCoderRole
    evidence_kind: BlindEvidenceKind
    batch_index: int = Field(ge=1)
    package_id: str = Field(pattern=r"^LPKG2-[0-9A-F]{20}$")
    package_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    reconciled_source: ReconciledCodebookSourceArtifact
    ambiguity_resolution: NonActionAmbiguityResolutionArtifact
    resolved_view: ResolvedCodebookViewArtifactV2
    ontology: OntologyReleaseArtifact
    procedure: StructuredCodingProcedureArtifactV2
    coding_manual_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coding_manual_text: str = Field(min_length=1)
    recurrence_policy_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    recurrence_policy_text: str = Field(min_length=1)
    instruction_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    instruction_prompt_text: str = Field(min_length=1)

    tasks: tuple[BlindTask, ...] = Field(min_length=1, max_length=5)
    assigned_unit_count: int = Field(ge=1)
    calibration_manifest_id: str | None = None
    calibration_manifest_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")

    episode_response_schema_version: Literal[
        "life-patterns-development-episode-annotation-response-v1"
    ] = "life-patterns-development-episode-annotation-response-v1"
    series_response_schema_version: Literal[
        "life-patterns-development-series-annotation-response-v2"
    ] = "life-patterns-development-series-annotation-response-v2"

    prior_automated_labels_available: Literal[False] = False
    automated_consensus_available: Literal[False] = False
    target_model_information_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    participant_pattern_claims_supplied_as_coding_targets: Literal[False] = False
    confirming_episodes_counted_as_frequency_evidence: Literal[False] = False
    calibration_selection_resampled_after_revision: Literal[False] = False
    packet_contains_private_participant_text: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @model_validator(mode="after")
    def packet_contract_is_coherent(self) -> BlindDevelopmentPacketPayloadV2:
        if self.assigned_unit_count != sum(len(task.observable_ids) for task in self.tasks):
            raise ValueError("blind packet v2 assigned unit count disagrees with task observables")
        expected_type = "DevelopmentEpisodeCodingTask" if self.evidence_kind == "episode" else (
            "DevelopmentSeriesCodingTask"
        )
        if any(type(task).__name__ != expected_type for task in self.tasks):
            raise ValueError(f"{self.evidence_kind} blind packet v2 contains wrong task kind")
        if self.coder_role == "human_calibration":
            if self.calibration_manifest_id is None or self.calibration_manifest_sha256 is None:
                raise ValueError("human calibration packet v2 requires frozen calibration manifest")
        elif self.calibration_manifest_id is not None or self.calibration_manifest_sha256 is not None:
            raise ValueError("automated blind packet v2 cannot carry human calibration identity")
        return self


class BlindDevelopmentPacketArtifactV2(BlindDevelopmentPacketV2Model):
    schema_version: Literal["life-patterns-blind-development-coder-packet-artifact-v2"] = (
        "life-patterns-blind-development-coder-packet-artifact-v2"
    )
    packet_id: str = Field(pattern=r"^LPBP2-[0-9A-F]{20}$")
    packet_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    payload: BlindDevelopmentPacketPayloadV2


class BlindDevelopmentPacketReceiptPayloadV2(BlindDevelopmentPacketV2Model):
    schema_version: Literal["life-patterns-blind-development-packet-receipt-v2"] = (
        "life-patterns-blind-development-packet-receipt-v2"
    )
    packet_id: str = Field(pattern=r"^LPBP2-[0-9A-F]{20}$")
    packet_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coder_role: BlindCoderRole
    evidence_kind: BlindEvidenceKind
    batch_index: int = Field(ge=1)
    package_id: str = Field(pattern=r"^LPKG2-[0-9A-F]{20}$")
    package_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    instruction_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coding_manual_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    recurrence_policy_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    task_ids: tuple[
        Annotated[str, Field(pattern=r"^LP(?:DT|ST)-[0-9A-F]{20}$")], ...
    ] = Field(min_length=1, max_length=5)
    assigned_unit_count: int = Field(ge=1)
    calibration_manifest_id: str | None = None
    calibration_manifest_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    prior_automated_labels_available: Literal[False] = False
    target_model_information_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    confirming_episodes_counted_as_frequency_evidence: Literal[False] = False
    receipt_contains_private_participant_text: Literal[False] = False
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True


class BlindDevelopmentPacketReceiptArtifactV2(BlindDevelopmentPacketV2Model):
    schema_version: Literal["life-patterns-blind-development-packet-receipt-artifact-v2"] = (
        "life-patterns-blind-development-packet-receipt-artifact-v2"
    )
    receipt_id: str = Field(pattern=r"^LPBR2-[0-9A-F]{20}$")
    receipt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    payload: BlindDevelopmentPacketReceiptPayloadV2


def _text_and_hash(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise ValueError(f"blind packet v2 input is missing: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"blind packet v2 input is empty: {path}")
    return text, file_sha256(path)


def _task_view(
    preparation: PrivateDevelopmentPreparationV2,
    *,
    coder_role: BlindCoderRole,
    evidence_kind: BlindEvidenceKind,
) -> tuple[BlindTask, ...]:
    if coder_role == "automated":
        if evidence_kind == "episode":
            return cast(tuple[BlindTask, ...], preparation.episode_tasks)
        return cast(tuple[BlindTask, ...], preparation.series_report.tasks)

    errors = development_calibration_integrity_errors(
        preparation.calibration,
        episode_tasks=preparation.episode_tasks,
        series_tasks=preparation.series_report.tasks,
    )
    if errors:
        raise ValueError("invalid reused v2 calibration selection: " + "; ".join(errors))
    if evidence_kind == "episode":
        return cast(
            tuple[BlindTask, ...],
            human_episode_calibration_tasks(preparation.episode_tasks, preparation.calibration),
        )
    return cast(
        tuple[BlindTask, ...],
        human_series_calibration_tasks(
            preparation.episode_tasks,
            preparation.series_report.tasks,
            preparation.calibration,
        ),
    )


def build_blind_development_packets_v2(
    preparation: PrivateDevelopmentPreparationV2,
    *,
    repo_root: str | Path,
    coder_role: BlindCoderRole,
    evidence_kind: BlindEvidenceKind,
    max_tasks_per_packet: int = 3,
) -> tuple[BlindDevelopmentPacketArtifactV2, ...]:
    if not 1 <= max_tasks_per_packet <= 5:
        raise ValueError("blind development packet v2 batch size must be between 1 and 5")
    root = Path(repo_root)
    manual_text, manual_sha256 = _text_and_hash(root / CODING_MANUAL_V2_REL)
    policy_text, policy_sha256 = _text_and_hash(root / RECURRENCE_POLICY_V2_REL)
    package = preparation.package.payload
    if manual_sha256 != package.coding_manual_sha256:
        raise ValueError("blind packet v2 manual does not bind development package v2")
    if policy_sha256 != package.recurrence_policy_sha256:
        raise ValueError("blind packet v2 recurrence policy does not bind package v2")

    if coder_role == "human_calibration":
        prompt_text, prompt_sha256 = _text_and_hash(root / HUMAN_CALIBRATION_PROMPT_V2_REL)
        if prompt_sha256 != package.human_calibration_prompt_sha256:
            raise ValueError("human calibration prompt v2 does not bind package v2")
    elif evidence_kind == "episode":
        prompt_text, prompt_sha256 = _text_and_hash(root / EPISODE_TRANSPORT_PROMPT_REL)
        if prompt_sha256 != package.episode_transport_prompt_sha256:
            raise ValueError("episode transport prompt does not bind package v2")
    else:
        prompt_text, prompt_sha256 = _text_and_hash(root / SERIES_TRANSPORT_PROMPT_V2_REL)
        if prompt_sha256 != package.series_transport_prompt_sha256:
            raise ValueError("series transport prompt v2 does not bind package v2")

    tasks = _task_view(
        preparation,
        coder_role=coder_role,
        evidence_kind=evidence_kind,
    )
    if not tasks:
        raise ValueError(f"no {coder_role} {evidence_kind} tasks are available for packet v2")

    calibration_id = preparation.calibration.manifest_id if coder_role == "human_calibration" else None
    calibration_sha = (
        preparation.calibration.manifest_sha256 if coder_role == "human_calibration" else None
    )
    packets: list[BlindDevelopmentPacketArtifactV2] = []
    for start in range(0, len(tasks), max_tasks_per_packet):
        batch = tasks[start : start + max_tasks_per_packet]
        payload = BlindDevelopmentPacketPayloadV2(
            coder_role=coder_role,
            evidence_kind=evidence_kind,
            batch_index=len(packets) + 1,
            package_id=preparation.package.package_id,
            package_sha256=preparation.package.package_sha256,
            corpus_id=preparation.corpus.corpus_id,
            corpus_sha256=preparation.corpus.corpus_sha256,
            reconciled_source=preparation.stack.source,
            ambiguity_resolution=preparation.stack.resolution,
            resolved_view=preparation.stack.resolved,
            ontology=preparation.stack.ontology,
            procedure=preparation.stack.procedure,
            coding_manual_sha256=manual_sha256,
            coding_manual_text=manual_text,
            recurrence_policy_sha256=policy_sha256,
            recurrence_policy_text=policy_text,
            instruction_prompt_sha256=prompt_sha256,
            instruction_prompt_text=prompt_text,
            tasks=batch,
            assigned_unit_count=sum(len(task.observable_ids) for task in batch),
            calibration_manifest_id=calibration_id,
            calibration_manifest_sha256=calibration_sha,
        )
        digest = sha256_json(payload)
        packets.append(
            BlindDevelopmentPacketArtifactV2(
                packet_id=f"LPBP2-{digest[:20].upper()}",
                packet_sha256=digest,
                payload=payload,
            )
        )
    return tuple(packets)


def packet_public_safe_receipt_v2(
    packet: BlindDevelopmentPacketArtifactV2,
) -> BlindDevelopmentPacketReceiptArtifactV2:
    payload = BlindDevelopmentPacketReceiptPayloadV2(
        packet_id=packet.packet_id,
        packet_sha256=packet.packet_sha256,
        coder_role=packet.payload.coder_role,
        evidence_kind=packet.payload.evidence_kind,
        batch_index=packet.payload.batch_index,
        package_id=packet.payload.package_id,
        package_sha256=packet.payload.package_sha256,
        instruction_prompt_sha256=packet.payload.instruction_prompt_sha256,
        coding_manual_sha256=packet.payload.coding_manual_sha256,
        recurrence_policy_sha256=packet.payload.recurrence_policy_sha256,
        task_ids=tuple(task.task_id for task in packet.payload.tasks),
        assigned_unit_count=packet.payload.assigned_unit_count,
        calibration_manifest_id=packet.payload.calibration_manifest_id,
        calibration_manifest_sha256=packet.payload.calibration_manifest_sha256,
    )
    digest = sha256_json(payload)
    return BlindDevelopmentPacketReceiptArtifactV2(
        receipt_id=f"LPBR2-{digest[:20].upper()}",
        receipt_sha256=digest,
        payload=payload,
    )


def write_private_blind_packet_v2(
    path: str | Path,
    packet: BlindDevelopmentPacketArtifactV2,
) -> Path:
    return write_new_bytes(path, canonical_json_bytes(packet), mode=0o400)


def write_public_safe_packet_receipt_v2(
    path: str | Path,
    receipt: BlindDevelopmentPacketReceiptArtifactV2,
) -> Path:
    return write_new_bytes(path, canonical_json_bytes(receipt), mode=0o400)
