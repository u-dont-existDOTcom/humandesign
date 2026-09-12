"""Validate and freeze a Life Patterns v2 human first pass from the private handoff.

The exact frozen human-handoff ZIP plus the auditor's three raw exports are sufficient. The
portable freeze does not require the earlier private preparation directory, call a model, or
expose target-model information. Private response and attestation bytes are preserved unchanged;
only a separate public-safe content-addressed receipt is suitable for Git.
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json, write_new_bytes

from .development_annotation_pipeline import (
    load_development_episode_responses_jsonl,
    normalize_development_episode_responses_jsonl,
)
from .development_blind_packets_v2 import BlindDevelopmentPacketArtifactV2
from .development_episode_evidence import development_episode_response_errors
from .development_human_attestation_v2 import (
    DevelopmentHumanAuditorAttestationReceiptArtifactV2,
    DevelopmentHumanAuditorAttestationV2,
    build_human_auditor_attestation_receipt_v2,
    load_and_validate_human_auditor_attestation_v2,
)
from .development_human_calibration_v2 import (
    DevelopmentHumanFirstPassArtifactV2,
    DevelopmentHumanFirstPassPayloadV2,
    load_development_series_responses_v2_jsonl,
    normalize_development_series_responses_v2_jsonl,
)
from .development_series_evidence import DevelopmentSeriesCodingTask
from .development_series_evidence_v2 import development_series_response_errors_v2
from .development_transfer_corpus import DevelopmentEpisodeCodingTask
from .neutral_measurement import OntologyReleaseArtifact
from .structured_annotation_v2 import StructuredCodingProcedureArtifactV2

HANDOFF_RECEIPT_NAME = "human_handoff_public_safe_receipt_v2.json"
EPISODE_BLANK_NAME = "episode_responses.blank.jsonl"
SERIES_BLANK_NAME = "series_responses.blank.jsonl"
EXPECTED_HANDOFF_SCHEMA = "life-patterns-private-human-handoff-receipt-v2"


class HumanFirstPassFreezeV2Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


@dataclass(frozen=True)
class VerifiedHumanHandoffForFirstPassV2:
    receipt_id: str
    receipt_sha256: str
    package_id: str
    package_sha256: str
    calibration_manifest_id: str
    calibration_manifest_sha256: str
    corpus_id: str
    corpus_sha256: str
    resolved_view_sha256: str
    coding_manual_sha256: str
    recurrence_policy_sha256: str
    human_prompt_sha256: str
    ontology: OntologyReleaseArtifact
    procedure: StructuredCodingProcedureArtifactV2
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...]
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...]
    episode_unit_count: int
    series_unit_count: int
    handoff_zip_sha256: str


class DevelopmentHumanFirstPassFreezeReceiptPayloadV2(HumanFirstPassFreezeV2Model):
    schema_version: Literal["life-patterns-human-first-pass-freeze-receipt-v2"] = (
        "life-patterns-human-first-pass-freeze-receipt-v2"
    )
    handoff_receipt_id: str = Field(pattern=r"^LPHB2-[0-9A-F]{20}$")
    handoff_receipt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    handoff_zip_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    package_id: str = Field(pattern=r"^LPKG2-[0-9A-F]{20}$")
    package_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    calibration_manifest_id: str = Field(pattern=r"^LPCA-[0-9A-F]{20}$")
    calibration_manifest_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    episode_first_pass_artifact_id: str = Field(pattern=r"^LPHF2-[0-9A-F]{20}$")
    episode_first_pass_artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    series_first_pass_artifact_id: str = Field(pattern=r"^LPHF2-[0-9A-F]{20}$")
    series_first_pass_artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    attestation_receipt_id: str = Field(pattern=r"^LPHA2-[0-9A-F]{20}$")
    attestation_receipt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    auditor_id_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    raw_episode_output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    raw_series_output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    raw_attestation_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    normalized_episode_output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    normalized_series_output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    episode_unit_count: int = Field(ge=1)
    series_unit_count: int = Field(ge=1)
    first_pass_completed_at_utc: datetime
    frozen_at_utc: datetime
    exact_raw_exports_preserved: Literal[True] = True
    complete_selected_unit_coverage: Literal[True] = True
    independent_theory_blind_human_attestation_validated: Literal[True] = True
    human_gate_satisfied: Literal[True] = True
    automated_coding_run_as_part_of_freeze: Literal[False] = False
    automated_consensus_available: Literal[False] = False
    target_model_information_used: Literal[False] = False
    target_model_scoring_run: Literal[False] = False
    contains_private_participant_text: Literal[False] = False
    contains_auditor_identity: Literal[False] = False
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @field_validator("first_pass_completed_at_utc", "frozen_at_utc")
    @classmethod
    def timestamps_are_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("human first-pass freeze v2 timestamps must be timezone-aware")
        return value.astimezone(UTC)


class DevelopmentHumanFirstPassFreezeReceiptArtifactV2(HumanFirstPassFreezeV2Model):
    schema_version: Literal["life-patterns-human-first-pass-freeze-receipt-artifact-v2"] = (
        "life-patterns-human-first-pass-freeze-receipt-artifact-v2"
    )
    receipt_id: str = Field(pattern=r"^LPHFR2-[0-9A-F]{20}$")
    receipt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    payload: DevelopmentHumanFirstPassFreezeReceiptPayloadV2


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_json_object(data: bytes, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must contain one JSON object")
    return cast(dict[str, Any], value)


def _load_jsonl_objects(data: bytes, *, label: str) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(data.splitlines(), start=1):
        if line.strip():
            rows.append(_load_json_object(line, label=f"{label} line {line_number}"))
    return tuple(rows)


def _verify_address(
    artifact: BaseModel,
    *,
    id_field: str,
    hash_field: str,
    prefix: str,
) -> str:
    payload = artifact.model_dump(mode="python")["payload"]
    digest = sha256_json(payload)
    if getattr(artifact, hash_field) != digest or getattr(artifact, id_field) != (
        f"{prefix}-{digest[:20].upper()}"
    ):
        raise ValueError(f"{prefix} artifact failed content-address verification")
    return digest


def _verify_receipted_members(
    files: dict[str, bytes],
    payload: dict[str, Any],
) -> None:
    declared_files = payload.get("files")
    if not isinstance(declared_files, dict) or not declared_files:
        raise ValueError("human handoff v2 receipt does not declare member hashes")
    expected_names = set(declared_files) | {HANDOFF_RECEIPT_NAME}
    if set(files) != expected_names:
        raise ValueError("human handoff v2 member set differs from its receipt")
    for name, expected_hash in declared_files.items():
        if not isinstance(name, str) or not isinstance(expected_hash, str):
            raise ValueError("human handoff v2 member receipt is malformed")
        if _sha256_bytes(files[name]) != expected_hash:
            raise ValueError(f"human handoff v2 member hash mismatch: {name}")


def _verify_handoff_flags(payload: dict[str, Any]) -> None:
    required_flags = {
        "selected_unit_coverage_verified": True,
        "calibration_selection_reused_without_resampling": True,
        "confirming_episodes_are_not_frequency_counts": True,
        "response_templates_are_annotations": False,
        "human_facing_ui_required_before_collection": True,
        "auditor_identity_verified": False,
        "human_blinding_attested": False,
        "development_only": True,
        "validation_use_forbidden": True,
    }
    for field, expected in required_flags.items():
        if payload.get(field) is not expected:
            raise ValueError(f"human handoff v2 has unexpected {field}")


def verify_human_handoff_for_first_pass_v2(
    handoff_zip: str | Path,
) -> VerifiedHumanHandoffForFirstPassV2:
    """Verify the exact private handoff and recover its frozen selected task universe."""

    source = Path(handoff_zip)
    raw_zip = source.read_bytes()
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("human handoff v2 contains duplicate ZIP member names")
        if any(name.endswith("/") for name in names):
            raise ValueError("human handoff v2 must contain files only")
        if HANDOFF_RECEIPT_NAME not in names:
            raise ValueError("human handoff v2 is missing its public-safe receipt")
        files = {name: archive.read(name) for name in names}

    receipt = _load_json_object(files[HANDOFF_RECEIPT_NAME], label=HANDOFF_RECEIPT_NAME)
    receipt_payload = receipt.get("payload")
    if not isinstance(receipt_payload, dict) or receipt_payload.get("schema_version") != (
        EXPECTED_HANDOFF_SCHEMA
    ):
        raise ValueError("human handoff v2 receipt has the wrong schema")
    receipt_digest = sha256_json(receipt_payload)
    if receipt.get("receipt_sha256") != receipt_digest or receipt.get("receipt_id") != (
        f"LPHB2-{receipt_digest[:20].upper()}"
    ):
        raise ValueError("human handoff v2 receipt failed content-address verification")
    _verify_receipted_members(files, receipt_payload)
    _verify_handoff_flags(receipt_payload)

    packet_names = sorted(
        name for name in files if name.startswith("packets/") and name.endswith(".json")
    )
    if len(packet_names) != receipt_payload.get("packet_count"):
        raise ValueError("human handoff v2 packet count disagrees with receipt")

    episode_tasks: list[DevelopmentEpisodeCodingTask] = []
    series_tasks: list[DevelopmentSeriesCodingTask] = []
    packet_hashes: set[str] = set()
    seen_task_ids: set[str] = set()
    ontology: OntologyReleaseArtifact | None = None
    procedure: StructuredCodingProcedureArtifactV2 | None = None
    resolved_view_sha256: str | None = None
    corpus_id: str | None = None
    corpus_sha256: str | None = None

    for name in packet_names:
        packet = BlindDevelopmentPacketArtifactV2.model_validate_json(files[name])
        packet_digest = sha256_json(packet.payload)
        if packet.packet_sha256 != packet_digest or packet.packet_id != (
            f"LPBP2-{packet_digest[:20].upper()}"
        ):
            raise ValueError(f"{name} failed LPBP2 content-address verification")
        if packet_digest in packet_hashes:
            raise ValueError("human handoff v2 repeats an LPBP2 content address")
        packet_hashes.add(packet_digest)
        packet_payload = packet.payload
        if packet_payload.coder_role != "human_calibration":
            raise ValueError(f"{name} is not a human-calibration packet")
        if any(
            (
                packet_payload.prior_automated_labels_available,
                packet_payload.automated_consensus_available,
                packet_payload.target_model_information_available,
                packet_payload.birth_or_chart_data_available,
                packet_payload.confirming_episodes_counted_as_frequency_evidence,
                packet_payload.calibration_selection_resampled_after_revision,
            )
        ):
            raise ValueError(f"{name} violates the blind first-pass chronology")
        if (
            packet_payload.package_id != receipt_payload.get("package_id")
            or packet_payload.package_sha256 != receipt_payload.get("package_sha256")
            or packet_payload.calibration_manifest_id
            != receipt_payload.get("calibration_manifest_id")
            or packet_payload.calibration_manifest_sha256
            != receipt_payload.get("calibration_manifest_sha256")
            or packet_payload.coding_manual_sha256
            != receipt_payload.get("coding_manual_sha256")
            or packet_payload.recurrence_policy_sha256
            != receipt_payload.get("recurrence_policy_sha256")
            or packet_payload.instruction_prompt_sha256
            != receipt_payload.get("human_prompt_sha256")
        ):
            raise ValueError(f"{name} does not bind the frozen human handoff")

        _verify_address(
            packet_payload.resolved_view,
            id_field="view_id",
            hash_field="view_sha256",
            prefix="LPRV",
        )
        _verify_address(
            packet_payload.ontology,
            id_field="artifact_id",
            hash_field="ontology_sha256",
            prefix="LPO",
        )
        _verify_address(
            packet_payload.procedure,
            id_field="procedure_id",
            hash_field="procedure_sha256",
            prefix="LPSP",
        )
        if ontology is None:
            ontology = packet_payload.ontology
            procedure = packet_payload.procedure
            resolved_view_sha256 = packet_payload.resolved_view.view_sha256
            corpus_id = packet_payload.corpus_id
            corpus_sha256 = packet_payload.corpus_sha256
        elif (
            packet_payload.ontology != ontology
            or packet_payload.procedure != procedure
            or packet_payload.resolved_view.view_sha256 != resolved_view_sha256
            or packet_payload.corpus_id != corpus_id
            or packet_payload.corpus_sha256 != corpus_sha256
        ):
            raise ValueError("human handoff v2 packets disagree on the frozen measurement stack")

        for task in packet_payload.tasks:
            if task.task_id in seen_task_ids:
                raise ValueError("human handoff v2 repeats a selected task identity")
            seen_task_ids.add(task.task_id)
            if packet_payload.evidence_kind == "episode":
                if not isinstance(task, DevelopmentEpisodeCodingTask):
                    raise ValueError("episode human packet contains the wrong task type")
                episode_tasks.append(task)
            else:
                if not isinstance(task, DevelopmentSeriesCodingTask):
                    raise ValueError("series human packet contains the wrong task type")
                series_tasks.append(task)

    expected_packet_hashes = receipt_payload.get("packet_sha256s")
    if not isinstance(expected_packet_hashes, list) or not all(
        isinstance(value, str) for value in expected_packet_hashes
    ):
        raise ValueError("human handoff v2 packet hash list is malformed")
    if packet_hashes != set(expected_packet_hashes):
        raise ValueError("human handoff v2 packet hashes differ from receipt")
    if ontology is None or procedure is None or resolved_view_sha256 is None:
        raise ValueError("human handoff v2 contains no usable measurement stack")
    if corpus_id is None or corpus_sha256 is None:
        raise ValueError("human handoff v2 contains no corpus binding")

    expected_episode_units = {
        (task.task_id, task.episode_id, observable_id)
        for task in episode_tasks
        for observable_id in task.observable_ids
    }
    expected_series_units = {
        (task.task_id, task.series_id, observable_id)
        for task in series_tasks
        for observable_id in task.observable_ids
    }
    blank_episode_rows = _load_jsonl_objects(
        files[EPISODE_BLANK_NAME],
        label=EPISODE_BLANK_NAME,
    )
    blank_series_rows = _load_jsonl_objects(
        files[SERIES_BLANK_NAME],
        label=SERIES_BLANK_NAME,
    )
    actual_blank_episode_units = {
        (row.get("task_id"), row.get("episode_id"), row.get("observable_id"))
        for row in blank_episode_rows
    }
    actual_blank_series_units = {
        (row.get("task_id"), row.get("series_id"), row.get("observable_id"))
        for row in blank_series_rows
    }
    if (
        actual_blank_episode_units != expected_episode_units
        or len(actual_blank_episode_units) != len(blank_episode_rows)
        or actual_blank_series_units != expected_series_units
        or len(actual_blank_series_units) != len(blank_series_rows)
    ):
        raise ValueError("human handoff v2 blank responses do not exactly cover packet units")
    if len(expected_episode_units) != receipt_payload.get("episode_unit_count"):
        raise ValueError("human handoff v2 episode unit count disagrees with receipt")
    if len(expected_series_units) != receipt_payload.get("series_unit_count"):
        raise ValueError("human handoff v2 series unit count disagrees with receipt")

    return VerifiedHumanHandoffForFirstPassV2(
        receipt_id=cast(str, receipt["receipt_id"]),
        receipt_sha256=cast(str, receipt["receipt_sha256"]),
        package_id=cast(str, receipt_payload["package_id"]),
        package_sha256=cast(str, receipt_payload["package_sha256"]),
        calibration_manifest_id=cast(str, receipt_payload["calibration_manifest_id"]),
        calibration_manifest_sha256=cast(str, receipt_payload["calibration_manifest_sha256"]),
        corpus_id=corpus_id,
        corpus_sha256=corpus_sha256,
        resolved_view_sha256=resolved_view_sha256,
        coding_manual_sha256=cast(str, receipt_payload["coding_manual_sha256"]),
        recurrence_policy_sha256=cast(str, receipt_payload["recurrence_policy_sha256"]),
        human_prompt_sha256=cast(str, receipt_payload["human_prompt_sha256"]),
        ontology=ontology,
        procedure=procedure,
        episode_tasks=tuple(episode_tasks),
        series_tasks=tuple(series_tasks),
        episode_unit_count=len(expected_episode_units),
        series_unit_count=len(expected_series_units),
        handoff_zip_sha256=_sha256_bytes(raw_zip),
    )


def _build_first_pass_artifact(
    *,
    evidence_kind: Literal["episode", "series"],
    auditor_id: str,
    handoff: VerifiedHumanHandoffForFirstPassV2,
    raw_output: bytes,
    normalized_output: bytes,
    selected_task_set_sha256: str,
    unit_count: int,
    frozen_at_utc: datetime,
) -> DevelopmentHumanFirstPassArtifactV2:
    payload = DevelopmentHumanFirstPassPayloadV2(
        evidence_kind=evidence_kind,
        auditor_id=auditor_id,
        package_id=handoff.package_id,
        package_sha256=handoff.package_sha256,
        calibration_manifest_id=handoff.calibration_manifest_id,
        calibration_manifest_sha256=handoff.calibration_manifest_sha256,
        corpus_id=handoff.corpus_id,
        corpus_sha256=handoff.corpus_sha256,
        codebook_sha256=handoff.resolved_view_sha256,
        coding_procedure_sha256=handoff.procedure.procedure_sha256,
        coding_manual_sha256=handoff.coding_manual_sha256,
        recurrence_policy_sha256=handoff.recurrence_policy_sha256,
        human_prompt_sha256=handoff.human_prompt_sha256,
        selected_task_set_sha256=selected_task_set_sha256,
        raw_output_sha256=_sha256_bytes(raw_output),
        normalized_output_sha256=_sha256_bytes(normalized_output),
        expected_unit_count=unit_count,
        validated_unit_count=unit_count,
        created_at_utc=frozen_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentHumanFirstPassArtifactV2(
        artifact_id=f"LPHF2-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def freeze_human_first_pass_from_handoff_v2(
    *,
    handoff_zip: str | Path,
    raw_episode_output: bytes,
    raw_series_output: bytes,
    raw_attestation: bytes,
    frozen_at_utc: datetime,
) -> tuple[
    DevelopmentHumanFirstPassArtifactV2,
    DevelopmentHumanFirstPassArtifactV2,
    DevelopmentHumanAuditorAttestationReceiptArtifactV2,
    DevelopmentHumanFirstPassFreezeReceiptArtifactV2,
    bytes,
    bytes,
]:
    """Validate complete raw exports and return private artifacts plus a public-safe receipt."""

    if frozen_at_utc.tzinfo is None or frozen_at_utc.utcoffset() is None:
        raise ValueError("human first-pass freeze timestamp must be timezone-aware")
    frozen_at = frozen_at_utc.astimezone(UTC)
    handoff = verify_human_handoff_for_first_pass_v2(handoff_zip)
    attestation: DevelopmentHumanAuditorAttestationV2 = (
        load_and_validate_human_auditor_attestation_v2(raw_attestation)
    )
    if attestation.first_pass_completed_at_utc > frozen_at:
        raise ValueError("human first-pass freeze cannot precede attested completion time")

    normalized_episode = normalize_development_episode_responses_jsonl(raw_episode_output)
    episode_responses = load_development_episode_responses_jsonl(normalized_episode)
    expected_episode_units = {
        (task.task_id, task.episode_id, observable_id)
        for task in handoff.episode_tasks
        for observable_id in task.observable_ids
    }
    actual_episode_units = {
        (episode_response.task_id, episode_response.episode_id, episode_response.observable_id)
        for episode_response in episode_responses
    }
    if len(episode_responses) != len(actual_episode_units) or actual_episode_units != (
        expected_episode_units
    ):
        raise ValueError("human episode first pass does not exactly cover frozen selected units")
    episode_task_by_id = {task.task_id: task for task in handoff.episode_tasks}
    for episode_response in episode_responses:
        errors = development_episode_response_errors(
            episode_response,
            task=episode_task_by_id[episode_response.task_id],
            ontology=handoff.ontology,
            procedure=handoff.procedure,
        )
        if errors:
            raise ValueError(
                "invalid human episode response "
                f"{episode_response.task_id}/{episode_response.observable_id}: "
                + "; ".join(errors)
            )

    normalized_series = normalize_development_series_responses_v2_jsonl(raw_series_output)
    series_responses = load_development_series_responses_v2_jsonl(normalized_series)
    expected_series_units = {
        (task.task_id, task.series_id, observable_id)
        for task in handoff.series_tasks
        for observable_id in task.observable_ids
    }
    actual_series_units = {
        (series_response.task_id, series_response.series_id, series_response.observable_id)
        for series_response in series_responses
    }
    if len(series_responses) != len(actual_series_units) or actual_series_units != (
        expected_series_units
    ):
        raise ValueError("human series first pass does not exactly cover frozen selected units")
    series_task_by_id = {task.task_id: task for task in handoff.series_tasks}
    for series_response in series_responses:
        errors = development_series_response_errors_v2(
            series_response,
            task=series_task_by_id[series_response.task_id],
            ontology=handoff.ontology,
            procedure=handoff.procedure,
        )
        if errors:
            raise ValueError(
                "invalid human series response "
                f"{series_response.task_id}/{series_response.observable_id}: "
                + "; ".join(errors)
            )

    episode_artifact = _build_first_pass_artifact(
        evidence_kind="episode",
        auditor_id=attestation.auditor_id,
        handoff=handoff,
        raw_output=raw_episode_output,
        normalized_output=normalized_episode,
        selected_task_set_sha256=sha256_json(handoff.episode_tasks),
        unit_count=len(expected_episode_units),
        frozen_at_utc=frozen_at,
    )
    series_artifact = _build_first_pass_artifact(
        evidence_kind="series",
        auditor_id=attestation.auditor_id,
        handoff=handoff,
        raw_output=raw_series_output,
        normalized_output=normalized_series,
        selected_task_set_sha256=sha256_json(handoff.series_tasks),
        unit_count=len(expected_series_units),
        frozen_at_utc=frozen_at,
    )
    attestation_receipt = build_human_auditor_attestation_receipt_v2(raw_attestation)
    receipt_payload = DevelopmentHumanFirstPassFreezeReceiptPayloadV2(
        handoff_receipt_id=handoff.receipt_id,
        handoff_receipt_sha256=handoff.receipt_sha256,
        handoff_zip_sha256=handoff.handoff_zip_sha256,
        package_id=handoff.package_id,
        package_sha256=handoff.package_sha256,
        calibration_manifest_id=handoff.calibration_manifest_id,
        calibration_manifest_sha256=handoff.calibration_manifest_sha256,
        episode_first_pass_artifact_id=episode_artifact.artifact_id,
        episode_first_pass_artifact_sha256=episode_artifact.artifact_sha256,
        series_first_pass_artifact_id=series_artifact.artifact_id,
        series_first_pass_artifact_sha256=series_artifact.artifact_sha256,
        attestation_receipt_id=attestation_receipt.receipt_id,
        attestation_receipt_sha256=attestation_receipt.receipt_sha256,
        auditor_id_sha256=_sha256_bytes(attestation.auditor_id.encode("utf-8")),
        raw_episode_output_sha256=_sha256_bytes(raw_episode_output),
        raw_series_output_sha256=_sha256_bytes(raw_series_output),
        raw_attestation_sha256=_sha256_bytes(raw_attestation),
        normalized_episode_output_sha256=_sha256_bytes(normalized_episode),
        normalized_series_output_sha256=_sha256_bytes(normalized_series),
        episode_unit_count=len(expected_episode_units),
        series_unit_count=len(expected_series_units),
        first_pass_completed_at_utc=attestation.first_pass_completed_at_utc,
        frozen_at_utc=frozen_at,
    )
    receipt_digest = sha256_json(receipt_payload)
    freeze_receipt = DevelopmentHumanFirstPassFreezeReceiptArtifactV2(
        receipt_id=f"LPHFR2-{receipt_digest[:20].upper()}",
        receipt_sha256=receipt_digest,
        payload=receipt_payload,
    )
    return (
        episode_artifact,
        series_artifact,
        attestation_receipt,
        freeze_receipt,
        normalized_episode,
        normalized_series,
    )


def write_human_first_pass_freeze_v2(
    *,
    output_dir: str | Path,
    handoff_zip: str | Path,
    raw_episode_output: bytes,
    raw_series_output: bytes,
    raw_attestation: bytes,
    frozen_at_utc: datetime,
) -> DevelopmentHumanFirstPassFreezeReceiptArtifactV2:
    """Create an immutable private freeze directory and return its public-safe receipt."""

    output = Path(output_dir)
    if output.exists() or output.is_symlink():
        raise FileExistsError("human first-pass freeze output already exists")
    (
        episode_artifact,
        series_artifact,
        attestation_receipt,
        freeze_receipt,
        normalized_episode,
        normalized_series,
    ) = freeze_human_first_pass_from_handoff_v2(
        handoff_zip=handoff_zip,
        raw_episode_output=raw_episode_output,
        raw_series_output=raw_series_output,
        raw_attestation=raw_attestation,
        frozen_at_utc=frozen_at_utc,
    )

    output.mkdir(mode=0o700, parents=True)
    private_files = {
        "episode_responses.raw.jsonl": raw_episode_output,
        "series_responses.raw.jsonl": raw_series_output,
        "auditor_attestation.raw.json": raw_attestation,
        "episode_responses.normalized.jsonl": normalized_episode,
        "series_responses.normalized.jsonl": normalized_series,
        "episode_first_pass_artifact.json": canonical_json_bytes(episode_artifact),
        "series_first_pass_artifact.json": canonical_json_bytes(series_artifact),
    }
    for name, raw in private_files.items():
        write_new_bytes(output / name, raw, mode=0o400)
    write_new_bytes(
        output / "auditor_attestation_public_safe_receipt.json",
        canonical_json_bytes(attestation_receipt),
        mode=0o400,
    )
    write_new_bytes(
        output / "human_first_pass_public_safe_receipt.json",
        canonical_json_bytes(freeze_receipt),
        mode=0o400,
    )
    return freeze_receipt


def human_first_pass_freeze_receipt_v2_integrity_errors(
    receipt: DevelopmentHumanFirstPassFreezeReceiptArtifactV2,
) -> tuple[str, ...]:
    digest = sha256_json(receipt.payload)
    if receipt.receipt_sha256 != digest or receipt.receipt_id != (
        f"LPHFR2-{digest[:20].upper()}"
    ):
        return ("human first-pass freeze receipt v2 failed content-address verification",)
    return ()
