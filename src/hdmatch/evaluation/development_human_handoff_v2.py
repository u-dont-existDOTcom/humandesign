"""Export an unlabelled recurrence-corrected private human calibration bundle.

The exporter verifies the v2 package, reused pre-label calibration selection, v2 human packets,
manual/policy/prompt bindings, and exact task universe before writing anything. It creates no
annotations and calls no model. JSON/JSONL remains interchange format; the human-facing UI is a
separate required layer before actual first-pass collection.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel, TypeAdapter

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_json,
    write_new_bytes,
)

from .development_blind_packets_v2 import (
    BlindDevelopmentPacketArtifactV2,
    BlindDevelopmentPacketReceiptArtifactV2,
    packet_public_safe_receipt_v2,
)
from .development_calibration_sampling import (
    DevelopmentCalibrationSamplingArtifact,
    development_calibration_integrity_errors,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from .development_coding_package_v2 import (
    DevelopmentCodingPackageArtifactV2,
    development_coding_package_v2_integrity_errors,
)
from .development_episode_evidence import DevelopmentEpisodeAnnotationResponse
from .development_series_evidence import DevelopmentSeriesCodingTask
from .development_series_evidence_v2 import DevelopmentSeriesAnnotationResponseV2
from .development_transfer_corpus import DevelopmentEpisodeCodingTask

_Model = TypeVar("_Model", bound=BaseModel)
_PACKET_NAME = re.compile(r"packet-[0-9]{3}\.json")

_README = """# Independent behavioral calibration — recurrence-corrected v2

This is the private interchange bundle for the frozen human calibration selection. Keep it
private. Do not upload participant-bearing packets to a public repository.

IMPORTANT: the independent auditor should use the project-provided local/offline human-facing
annotation interface rather than hand-editing JSON. These schemas/templates exist for exact
validation/export. The UI must preserve them exactly and make no network requests.

The recurrence-corrected method distinguishes generalized behavioral recurrence self-report from
bounded episodes and from sampled/externally observed frequency. A statement such as “I always X”
can be direct evidence of REPORTED recurrence without a fabricated numeric count. A confirming
example selected because the pattern was already asserted is not independent frequency evidence.
Exception status, recurrence strength and evidence basis remain separate.

Do not consult automated coding, consensus, expected answers, external theory mappings,
birth/chart data, or target-model outputs. Do not use an automated coder for the independent human
first pass. Preserve the first-pass result unchanged before any automated-label exposure.

This is development calibration only. It does not establish objective frequency accuracy,
construct validity, predictive validity, or truth of any external theory.
"""


def _read_model(path: Path, model: type[_Model]) -> _Model:
    return model.model_validate_json(path.read_bytes())


def _verify_address(artifact: BaseModel, *, id_field: str, hash_field: str, prefix: str) -> str:
    digest = sha256_json(artifact.model_dump(mode="python")["payload"])
    if getattr(artifact, hash_field) != digest or getattr(artifact, id_field) != (
        f"{prefix}-{digest[:20].upper()}"
    ):
        raise ValueError("human handoff v2 input failed content-address verification")
    return digest


def _verify_packet_bindings(
    packet: BlindDevelopmentPacketArtifactV2,
    package: DevelopmentCodingPackageArtifactV2,
    calibration: DevelopmentCalibrationSamplingArtifact,
) -> None:
    _verify_address(packet, id_field="packet_id", hash_field="packet_sha256", prefix="LPBP2")
    payload = packet.payload
    bound = package.payload
    if payload.coder_role != "human_calibration":
        raise ValueError("human handoff v2 refuses automated packets")
    if (
        payload.package_id != package.package_id
        or payload.package_sha256 != package.package_sha256
        or payload.corpus_id != bound.corpus_id
        or payload.corpus_sha256 != bound.corpus_sha256
        or payload.calibration_manifest_id != calibration.manifest_id
        or payload.calibration_manifest_sha256 != calibration.manifest_sha256
    ):
        raise ValueError("human packet v2 does not bind frozen package and calibration")

    for artifact, id_field, hash_field, prefix, expected_id, expected_hash in (
        (
            payload.reconciled_source,
            "artifact_id",
            "artifact_sha256",
            "LPCB",
            bound.reconciled_source_artifact_id,
            bound.reconciled_source_sha256,
        ),
        (
            payload.ambiguity_resolution,
            "resolution_id",
            "resolution_sha256",
            "LPAR",
            bound.ambiguity_resolution_id,
            bound.ambiguity_resolution_sha256,
        ),
        (
            payload.resolved_view,
            "view_id",
            "view_sha256",
            "LPRV",
            bound.resolved_view_id,
            bound.resolved_view_sha256,
        ),
        (
            payload.ontology,
            "artifact_id",
            "ontology_sha256",
            "LPO",
            bound.ontology_artifact_id,
            bound.ontology_sha256,
        ),
        (
            payload.procedure,
            "procedure_id",
            "procedure_sha256",
            "LPSP",
            bound.procedure_id,
            bound.procedure_sha256,
        ),
    ):
        digest = _verify_address(artifact, id_field=id_field, hash_field=hash_field, prefix=prefix)
        if digest != expected_hash or getattr(artifact, id_field) != expected_id:
            raise ValueError("human packet v2 measurement stack differs from frozen package")

    if (
        payload.coding_manual_sha256 != bound.coding_manual_sha256
        or sha256_bytes(payload.coding_manual_text.encode()) != payload.coding_manual_sha256
        or payload.recurrence_policy_sha256 != bound.recurrence_policy_sha256
        or sha256_bytes(payload.recurrence_policy_text.encode()) != payload.recurrence_policy_sha256
        or payload.instruction_prompt_sha256 != bound.human_calibration_prompt_sha256
        or sha256_bytes(payload.instruction_prompt_text.encode())
        != payload.instruction_prompt_sha256
    ):
        raise ValueError("human packet v2 manual/policy/prompt fails package binding")
    if payload.confirming_episodes_counted_as_frequency_evidence is not False:
        raise ValueError("human packet v2 violates confirming-episode frequency firewall")


def _blank_episode_row(task: DevelopmentEpisodeCodingTask, observable_id: str) -> dict[str, Any]:
    properties = DevelopmentEpisodeAnnotationResponse.model_json_schema()["properties"]
    row: dict[str, Any] = {name: definition.get("const") for name, definition in properties.items()}
    row.update(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id=observable_id,
    )
    return row


def _blank_series_row(task: DevelopmentSeriesCodingTask, observable_id: str) -> dict[str, Any]:
    properties = DevelopmentSeriesAnnotationResponseV2.model_json_schema()["properties"]
    row: dict[str, Any] = {name: definition.get("const") for name, definition in properties.items()}
    row.update(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id=observable_id,
    )
    return row


def export_development_human_calibration_bundle_v2(
    prepared_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    """Validate all frozen v2 inputs first, then create one private unlabelled handoff."""

    prepared = Path(prepared_dir)
    output = Path(output_dir)
    if output.exists() or output.is_symlink():
        raise FileExistsError("human handoff v2 output already exists")

    package = _read_model(
        prepared / "development_coding_package_v2_public_safe.json",
        DevelopmentCodingPackageArtifactV2,
    )
    if development_coding_package_v2_integrity_errors(package):
        raise ValueError("invalid frozen development package v2 content address")
    calibration = _read_model(
        prepared / "development_calibration_manifest.json",
        DevelopmentCalibrationSamplingArtifact,
    )
    episode_tasks = TypeAdapter(tuple[DevelopmentEpisodeCodingTask, ...]).validate_json(
        (prepared / "development_episode_tasks.json").read_bytes()
    )
    series_tasks = TypeAdapter(tuple[DevelopmentSeriesCodingTask, ...]).validate_json(
        (prepared / "development_series_tasks.json").read_bytes()
    )
    if development_calibration_integrity_errors(
        calibration,
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
    ):
        raise ValueError("invalid reused human calibration selection v2")

    bound = package.payload
    if (
        calibration.manifest_id != bound.calibration_manifest_id
        or calibration.manifest_sha256 != bound.calibration_manifest_sha256
        or calibration.payload.corpus_id != bound.corpus_id
        or calibration.payload.corpus_sha256 != bound.corpus_sha256
        or sha256_json(episode_tasks) != bound.episode_task_set_sha256
        or (sha256_json(series_tasks) if series_tasks else None) != bound.series_task_set_sha256
        or len(episode_tasks) != bound.episode_task_count
        or len(series_tasks) != bound.series_task_count
    ):
        raise ValueError("package v2 does not bind supplied task universe/calibration")

    selected_episode = human_episode_calibration_tasks(episode_tasks, calibration)
    selected_series = human_series_calibration_tasks(episode_tasks, series_tasks, calibration)
    selected_by_kind: dict[str, tuple[DevelopmentEpisodeCodingTask | DevelopmentSeriesCodingTask, ...]] = {
        "episode": selected_episode,
        "series": selected_series,
    }
    files: dict[str, bytes] = {"README.md": _README.encode()}
    packet_hashes: list[str] = []
    prompt_hashes: set[str] = set()
    unit_counts: dict[str, int] = {}

    for kind, expected_tasks in selected_by_kind.items():
        group = prepared / "blind_packets_v2" / f"human_calibration_{kind}"
        paths = sorted(
            path for path in group.glob("*.json") if not path.name.endswith(".receipt.json")
        )
        expected_by_id = {task.task_id: task for task in expected_tasks}
        if len(expected_by_id) != len(expected_tasks):
            raise ValueError("selected v2 human tasks repeat an identity")
        seen: set[str] = set()
        batch_indices: list[int] = []
        rows: list[dict[str, Any]] = []
        for path in paths:
            if not _PACKET_NAME.fullmatch(path.name):
                raise ValueError("unexpected file in frozen v2 human packet group")
            raw = path.read_bytes()
            packet = BlindDevelopmentPacketArtifactV2.model_validate_json(raw)
            _verify_packet_bindings(packet, package, calibration)
            if packet.payload.evidence_kind != kind:
                raise ValueError("human packet v2 mixes evidence strata")
            receipt = _read_model(
                path.with_suffix(".receipt.json"),
                BlindDevelopmentPacketReceiptArtifactV2,
            )
            if receipt != packet_public_safe_receipt_v2(packet):
                raise ValueError("frozen packet v2 receipt does not bind exact packet")
            batch_indices.append(packet.payload.batch_index)
            if path.name != f"packet-{packet.payload.batch_index:03d}.json":
                raise ValueError("human packet v2 filename disagrees with batch index")
            for task in packet.payload.tasks:
                if task.task_id in seen or task != expected_by_id.get(task.task_id):
                    raise ValueError("human packets v2 contain duplicate, extra, or changed tasks")
                seen.add(task.task_id)
                for observable_id in task.observable_ids:
                    if kind == "episode":
                        if not isinstance(task, DevelopmentEpisodeCodingTask):
                            raise ValueError("episode packet v2 contains series task")
                        rows.append(_blank_episode_row(task, observable_id))
                    else:
                        if not isinstance(task, DevelopmentSeriesCodingTask):
                            raise ValueError("series packet v2 contains episode task")
                        rows.append(_blank_series_row(task, observable_id))
            prompt_hashes.add(packet.payload.instruction_prompt_sha256)
            packet_hashes.append(packet.packet_sha256)
            files[f"packets/{kind}/{path.name}"] = raw
        if seen != set(expected_by_id):
            raise ValueError("human packets v2 are missing frozen selected tasks")
        if batch_indices != list(range(1, len(paths) + 1)):
            raise ValueError("human packet v2 batches are incomplete or nonsequential")
        unit_counts[kind] = len(rows)
        files[f"{kind}_responses.blank.jsonl"] = b"".join(
            canonical_json_bytes(row) + b"\n" for row in rows
        )

    if len(prompt_hashes) != 1 or next(iter(prompt_hashes)) != bound.human_calibration_prompt_sha256:
        raise ValueError("human packet v2 groups do not share the bound human prompt")
    if (
        unit_counts["episode"] != bound.calibration_episode_unit_count
        or unit_counts["series"] != bound.calibration_series_unit_count
    ):
        raise ValueError("human packet v2 unit counts disagree with frozen package")

    files["episode_response.schema.json"] = canonical_json_bytes(
        DevelopmentEpisodeAnnotationResponse.model_json_schema()
    )
    files["series_response.schema.json"] = canonical_json_bytes(
        DevelopmentSeriesAnnotationResponseV2.model_json_schema()
    )
    files["auditor_attestation.blank.json"] = canonical_json_bytes(
        {
            "schema_version": "life-patterns-human-auditor-unfilled-attestation-v2",
            "auditor_id": None,
            "independent_of_participant": None,
            "participant_or_theory_exposed_owner": None,
            "target_theory_blind": None,
            "llm_outputs_available_before_first_pass": None,
            "automated_consensus_available_before_first_pass": None,
            "target_model_outputs_available": None,
            "birth_or_chart_data_available": None,
            "automated_coder_used_for_first_pass": None,
            "human_facing_offline_ui_used": None,
            "first_pass_completed_at_utc": None,
            "auditor_notes": None,
        }
    )

    payload = {
        "schema_version": "life-patterns-private-human-handoff-receipt-v2",
        "package_id": package.package_id,
        "package_sha256": package.package_sha256,
        "calibration_manifest_id": calibration.manifest_id,
        "calibration_manifest_sha256": calibration.manifest_sha256,
        "packet_sha256s": packet_hashes,
        "human_prompt_sha256": next(iter(prompt_hashes)),
        "recurrence_policy_sha256": bound.recurrence_policy_sha256,
        "coding_manual_sha256": bound.coding_manual_sha256,
        "packet_count": len(packet_hashes),
        "episode_unit_count": unit_counts["episode"],
        "series_unit_count": unit_counts["series"],
        "episode_response_schema_version": bound.episode_response_schema_version,
        "series_response_schema_version": bound.series_response_schema_version,
        "files": {name: sha256_bytes(raw) for name, raw in sorted(files.items())},
        "readiness": "awaiting_human_ui",
        "selected_unit_coverage_verified": True,
        "calibration_selection_reused_without_resampling": True,
        "confirming_episodes_are_not_frequency_counts": True,
        "response_templates_are_annotations": False,
        "human_facing_ui_required_before_collection": True,
        "auditor_identity_verified": False,
        "human_blinding_attested": False,
        "development_only": True,
        "validation_use_forbidden": True,
        "receipt_contains_private_participant_text": False,
    }
    digest = sha256_json(payload)
    receipt_data = {
        "receipt_id": f"LPHB2-{digest[:20].upper()}",
        "receipt_sha256": digest,
        "payload": payload,
    }
    files["human_handoff_public_safe_receipt_v2.json"] = canonical_json_bytes(receipt_data)

    output.mkdir(mode=0o700)
    for relative_name, raw in files.items():
        destination = output / relative_name
        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        write_new_bytes(destination, raw, mode=0o400)
    return receipt_data
