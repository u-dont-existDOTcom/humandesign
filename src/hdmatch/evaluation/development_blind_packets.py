"""Render private theory-blind coder packets from the frozen development preparation.

Packets contain private participant evidence and therefore belong in gitignored/private storage.
A separate receipt contains only hashes, task identities, counts, and blind-state assertions and is
safe to commit. Automated and human-calibration packets are rendered from the same frozen
measurement stack, but human packets are restricted to the preselected calibration units and
never contain automated labels.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json, write_new_bytes

from .development_calibration_sampling import (
    development_calibration_integrity_errors,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from .development_private_preparation import (
    EPISODE_TRANSPORT_PROMPT_REL,
    SERIES_TRANSPORT_PROMPT_REL,
    PrivateDevelopmentPreparation,
)
from .development_series_evidence import DevelopmentSeriesCodingTask
from .development_transfer_corpus import DevelopmentEpisodeCodingTask
from .neutral_measurement import OntologyReleaseArtifact
from .non_action_resolution import (
    NonActionAmbiguityResolutionArtifact,
    ResolvedCodebookViewArtifactV2,
)
from .reconciled_codebook_source import ReconciledCodebookSourceArtifact
from .resolved_development_stack import CODING_MANUAL_REL, file_sha256
from .structured_annotation_v2 import StructuredCodingProcedureArtifactV2

BlindCoderRole = Literal["automated", "human_calibration"]
BlindEvidenceKind = Literal["episode", "series"]
BlindTask = DevelopmentEpisodeCodingTask | DevelopmentSeriesCodingTask

HUMAN_CALIBRATION_PROMPT_REL = Path(
    "state/LIFE-PATTERNS-DEVELOPMENT-HUMAN-CALIBRATION-PROMPT-v1-2026-09-06.txt"
)


class BlindPacketModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class BlindDevelopmentPacketPayload(BlindPacketModel):
    schema_version: Literal["life-patterns-blind-development-coder-packet-v1"] = (
        "life-patterns-blind-development-coder-packet-v1"
    )
    coder_role: BlindCoderRole
    evidence_kind: BlindEvidenceKind
    batch_index: int = Field(ge=1)
    package_id: str = Field(pattern=r"^LPKG-[0-9A-F]{20}$")
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
    instruction_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    instruction_prompt_text: str = Field(min_length=1)

    tasks: tuple[BlindTask, ...] = Field(min_length=1, max_length=5)
    assigned_unit_count: int = Field(ge=1)
    calibration_manifest_id: str | None = None
    calibration_manifest_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")

    prior_automated_labels_available: Literal[False] = False
    automated_consensus_available: Literal[False] = False
    target_model_information_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    participant_pattern_claims_supplied_as_coding_targets: Literal[False] = False
    packet_contains_private_participant_text: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @model_validator(mode="after")
    def packet_contract_is_coherent(self) -> BlindDevelopmentPacketPayload:
        if self.assigned_unit_count != sum(len(task.observable_ids) for task in self.tasks):
            raise ValueError("blind packet assigned unit count disagrees with task observables")
        if self.evidence_kind == "episode" and any(
            not isinstance(task, DevelopmentEpisodeCodingTask) for task in self.tasks
        ):
            raise ValueError("episode blind packet contains non-episode task")
        if self.evidence_kind == "series" and any(
            not isinstance(task, DevelopmentSeriesCodingTask) for task in self.tasks
        ):
            raise ValueError("series blind packet contains non-series task")
        if self.coder_role == "human_calibration":
            if self.calibration_manifest_id is None or self.calibration_manifest_sha256 is None:
                raise ValueError("human calibration packet requires frozen calibration manifest")
        elif self.calibration_manifest_id is not None or self.calibration_manifest_sha256 is not None:
            raise ValueError("automated blind packet cannot masquerade as calibration packet")
        return self


class BlindDevelopmentPacketArtifact(BlindPacketModel):
    schema_version: Literal["life-patterns-blind-development-coder-packet-artifact-v1"] = (
        "life-patterns-blind-development-coder-packet-artifact-v1"
    )
    packet_id: str = Field(pattern=r"^LPBP-[0-9A-F]{20}$")
    packet_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    payload: BlindDevelopmentPacketPayload


class BlindDevelopmentPacketReceiptPayload(BlindPacketModel):
    schema_version: Literal["life-patterns-blind-development-packet-receipt-v1"] = (
        "life-patterns-blind-development-packet-receipt-v1"
    )
    packet_id: str = Field(pattern=r"^LPBP-[0-9A-F]{20}$")
    packet_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coder_role: BlindCoderRole
    evidence_kind: BlindEvidenceKind
    batch_index: int = Field(ge=1)
    package_id: str = Field(pattern=r"^LPKG-[0-9A-F]{20}$")
    package_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    instruction_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coding_manual_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    task_ids: tuple[
        Annotated[str, Field(pattern=r"^LP(?:DT|ST)-[0-9A-F]{20}$")], ...
    ] = Field(min_length=1, max_length=5)
    assigned_unit_count: int = Field(ge=1)
    calibration_manifest_id: str | None = None
    calibration_manifest_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    prior_automated_labels_available: Literal[False] = False
    target_model_information_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    receipt_contains_private_participant_text: Literal[False] = False
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True


class BlindDevelopmentPacketReceiptArtifact(BlindPacketModel):
    schema_version: Literal["life-patterns-blind-development-packet-receipt-artifact-v1"] = (
        "life-patterns-blind-development-packet-receipt-artifact-v1"
    )
    receipt_id: str = Field(pattern=r"^LPBR-[0-9A-F]{20}$")
    receipt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    payload: BlindDevelopmentPacketReceiptPayload


def _text_and_hash(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise ValueError(f"blind packet input file is missing: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"blind packet input file is empty: {path}")
    return text, file_sha256(path)


def _task_view(
    preparation: PrivateDevelopmentPreparation,
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
        raise ValueError("invalid development calibration manifest: " + "; ".join(errors))
    if evidence_kind == "episode":
        return cast(
            tuple[BlindTask, ...],
            human_episode_calibration_tasks(
                preparation.episode_tasks,
                preparation.calibration,
            ),
        )
    return cast(
        tuple[BlindTask, ...],
        human_series_calibration_tasks(
            preparation.episode_tasks,
            preparation.series_report.tasks,
            preparation.calibration,
        ),
    )


def build_blind_development_packets(
    preparation: PrivateDevelopmentPreparation,
    *,
    repo_root: str | Path,
    coder_role: BlindCoderRole,
    evidence_kind: BlindEvidenceKind,
    max_tasks_per_packet: int = 3,
) -> tuple[BlindDevelopmentPacketArtifact, ...]:
    if not 1 <= max_tasks_per_packet <= 5:
        raise ValueError("blind development packet batch size must be between 1 and 5")
    root = Path(repo_root)
    manual_text, manual_sha256 = _text_and_hash(root / CODING_MANUAL_REL)
    if manual_sha256 != preparation.package.payload.coding_manual_sha256:
        raise ValueError("blind packet coding manual does not bind frozen development package")

    if coder_role == "human_calibration":
        prompt_text, prompt_sha256 = _text_and_hash(root / HUMAN_CALIBRATION_PROMPT_REL)
    elif evidence_kind == "episode":
        prompt_text, prompt_sha256 = _text_and_hash(root / EPISODE_TRANSPORT_PROMPT_REL)
        if prompt_sha256 != preparation.package.payload.episode_transport_prompt_sha256:
            raise ValueError("episode transport prompt does not bind frozen development package")
    else:
        prompt_text, prompt_sha256 = _text_and_hash(root / SERIES_TRANSPORT_PROMPT_REL)
        if prompt_sha256 != preparation.package.payload.series_transport_prompt_sha256:
            raise ValueError("series transport prompt does not bind frozen development package")

    tasks = _task_view(
        preparation,
        coder_role=coder_role,
        evidence_kind=evidence_kind,
    )
    if not tasks:
        raise ValueError(f"no {coder_role} {evidence_kind} tasks are available for packet rendering")

    packets: list[BlindDevelopmentPacketArtifact] = []
    calibration_id = preparation.calibration.manifest_id if coder_role == "human_calibration" else None
    calibration_sha = (
        preparation.calibration.manifest_sha256 if coder_role == "human_calibration" else None
    )
    for start in range(0, len(tasks), max_tasks_per_packet):
        batch = tasks[start : start + max_tasks_per_packet]
        payload = BlindDevelopmentPacketPayload(
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
            instruction_prompt_sha256=prompt_sha256,
            instruction_prompt_text=prompt_text,
            tasks=batch,
            assigned_unit_count=sum(len(task.observable_ids) for task in batch),
            calibration_manifest_id=calibration_id,
            calibration_manifest_sha256=calibration_sha,
        )
        digest = sha256_json(payload)
        packets.append(
            BlindDevelopmentPacketArtifact(
                packet_id=f"LPBP-{digest[:20].upper()}",
                packet_sha256=digest,
                payload=payload,
            )
        )
    return tuple(packets)


def packet_public_safe_receipt(
    packet: BlindDevelopmentPacketArtifact,
) -> BlindDevelopmentPacketReceiptArtifact:
    payload = BlindDevelopmentPacketReceiptPayload(
        packet_id=packet.packet_id,
        packet_sha256=packet.packet_sha256,
        coder_role=packet.payload.coder_role,
        evidence_kind=packet.payload.evidence_kind,
        batch_index=packet.payload.batch_index,
        package_id=packet.payload.package_id,
        package_sha256=packet.payload.package_sha256,
        instruction_prompt_sha256=packet.payload.instruction_prompt_sha256,
        coding_manual_sha256=packet.payload.coding_manual_sha256,
        task_ids=tuple(task.task_id for task in packet.payload.tasks),
        assigned_unit_count=packet.payload.assigned_unit_count,
        calibration_manifest_id=packet.payload.calibration_manifest_id,
        calibration_manifest_sha256=packet.payload.calibration_manifest_sha256,
    )
    digest = sha256_json(payload)
    return BlindDevelopmentPacketReceiptArtifact(
        receipt_id=f"LPBR-{digest[:20].upper()}",
        receipt_sha256=digest,
        payload=payload,
    )


def write_private_blind_packet(
    path: str | Path,
    packet: BlindDevelopmentPacketArtifact,
) -> Path:
    return write_new_bytes(path, canonical_json_bytes(packet), mode=0o400)


def write_public_safe_packet_receipt(
    path: str | Path,
    receipt: BlindDevelopmentPacketReceiptArtifact,
) -> Path:
    return write_new_bytes(path, canonical_json_bytes(receipt), mode=0o400)
