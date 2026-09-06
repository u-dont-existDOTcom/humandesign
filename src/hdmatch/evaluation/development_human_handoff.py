"""Export an unlabelled private human bundle from already-frozen development packets.

No source reconstruction, sampling, packet rendering, annotation, or model execution occurs.
Only human packets are copied, byte for byte, after package and selection verification.
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

from .development_blind_packets import (
    BlindDevelopmentPacketArtifact,
    BlindDevelopmentPacketReceiptArtifact,
    BlindTask,
    packet_public_safe_receipt,
)
from .development_calibration_sampling import (
    DevelopmentCalibrationSamplingArtifact,
    development_calibration_integrity_errors,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from .development_coding_package import (
    DevelopmentCodingPackageArtifact,
    development_coding_package_integrity_errors,
)
from .development_episode_evidence import DevelopmentEpisodeAnnotationResponse
from .development_series_evidence import (
    DevelopmentSeriesAnnotationResponse,
    DevelopmentSeriesCodingTask,
)
from .development_transfer_corpus import DevelopmentEpisodeCodingTask

_Model = TypeVar("_Model", bound=BaseModel)
_PACKET_NAME = re.compile(r"packet-[0-9]{3}\.json")
_README = """# Independent behavioral calibration

This private bundle contains the frozen human calibration packets, response schemas, and
unfilled response templates. Keep it private. Do not upload it to a public repository.

Read the instruction prompt and coding manual embedded in each packet. Apply their exact
measurement definitions to only the observable IDs assigned in that packet. The supplied
packets are unchanged. Episode evidence and repeated-series evidence remain separate.

Create a working copy of the blank JSONL templates and complete one object per assigned unit.
The templates deliberately have state=null and no selected behavioral values: they are not
annotations and will fail response validation until completed. The JSON schemas describe
field types and permitted values; their defaults are software defaults, not suggested labels.
Replace every null placeholder as required by the schema and manual, including empty arrays
or false where appropriate. Preserve the populated identities and fixed schema constants.
Copy theory_exposure from the assigned task's participant_theory_exposure provenance.
Use only exact source segments from the assigned task for supporting citations.

Do not consult automated coding, consensus, expected answers, external theory mappings,
birth/chart data, or target-model outputs. If any have already been seen, disclose that in
the separate attestation form before beginning; the coordinator must assess eligibility.
Do not use an automated coder to complete this independent human first pass.

The attestation form is deliberately unfilled. Only the human auditor can report their
identity, independence, exposure, and completion time. Exporting this bundle attests to none
of those facts. Preserve the first-pass output unchanged and give it to the coordinator for
validation and freezing before receiving any automated labels or consensus.

This is development calibration. It does not establish predictive or construct validity.
"""


def _read_model(path: Path, model: type[_Model]) -> _Model:
    return model.model_validate_json(path.read_bytes())


def _verify_address(artifact: BaseModel, *, id_field: str, hash_field: str, prefix: str) -> str:
    digest = sha256_json(artifact.model_dump(mode="python")["payload"])
    if (
        getattr(artifact, hash_field) != digest
        or getattr(artifact, id_field) != f"{prefix}-{digest[:20].upper()}"
    ):
        raise ValueError("human handoff input failed content-address verification")
    return digest


def _verify_packet_bindings(
    packet: BlindDevelopmentPacketArtifact,
    package: DevelopmentCodingPackageArtifact,
    calibration: DevelopmentCalibrationSamplingArtifact,
) -> None:
    _verify_address(packet, id_field="packet_id", hash_field="packet_sha256", prefix="LPBP")
    payload, bound = packet.payload, package.payload
    if payload.coder_role != "human_calibration":
        raise ValueError("human handoff refuses automated packets")
    if (
        payload.package_id != package.package_id
        or payload.package_sha256 != package.package_sha256
        or payload.corpus_id != bound.corpus_id
        or payload.corpus_sha256 != bound.corpus_sha256
        or payload.calibration_manifest_id != calibration.manifest_id
        or payload.calibration_manifest_sha256 != calibration.manifest_sha256
    ):
        raise ValueError("human packet does not bind frozen package and calibration")
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
            raise ValueError("human packet measurement stack differs from frozen package")
    if (
        payload.coding_manual_sha256 != bound.coding_manual_sha256
        or sha256_bytes(payload.coding_manual_text.encode()) != payload.coding_manual_sha256
        or sha256_bytes(payload.instruction_prompt_text.encode())
        != payload.instruction_prompt_sha256
    ):
        raise ValueError("human packet manual or prompt text fails its hash binding")


def _blank_row(task: BlindTask, observable_id: str) -> dict[str, Any]:
    response_model: type[BaseModel]
    if isinstance(task, DevelopmentEpisodeCodingTask):
        response_model = DevelopmentEpisodeAnnotationResponse
        evidence_field, evidence_id = "episode_id", task.episode_id
    else:
        response_model = DevelopmentSeriesAnnotationResponse
        evidence_field, evidence_id = "series_id", task.series_id
    properties = response_model.model_json_schema()["properties"]
    row: dict[str, Any] = {name: definition.get("const") for name, definition in properties.items()}
    row.update(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        observable_id=observable_id,
    )
    row[evidence_field] = evidence_id
    return row


def export_development_human_calibration_bundle(
    prepared_dir: str | Path, output_dir: str | Path
) -> dict[str, Any]:
    """Verify frozen inputs, then create a new private bundle and safe hash receipt.

    The output's parent must already exist. All input validation completes before any
    output is created. The receipt describes preparation, never human identity or blinding.
    """

    prepared, output = Path(prepared_dir), Path(output_dir)
    if output.exists() or output.is_symlink():
        raise FileExistsError("human handoff output already exists")
    package = _read_model(
        prepared / "development_coding_package_public_safe.json", DevelopmentCodingPackageArtifact
    )
    if development_coding_package_integrity_errors(package):
        raise ValueError("invalid frozen development package content address")
    calibration = _read_model(
        prepared / "development_calibration_manifest.json", DevelopmentCalibrationSamplingArtifact
    )
    episode_tasks = TypeAdapter(tuple[DevelopmentEpisodeCodingTask, ...]).validate_json(
        (prepared / "development_episode_tasks.json").read_bytes()
    )
    series_tasks = TypeAdapter(tuple[DevelopmentSeriesCodingTask, ...]).validate_json(
        (prepared / "development_series_tasks.json").read_bytes()
    )
    if development_calibration_integrity_errors(
        calibration, episode_tasks=episode_tasks, series_tasks=series_tasks
    ):
        raise ValueError("invalid frozen human calibration or task-set binding")
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
        or sum(len(task.observable_ids) for task in episode_tasks)
        != bound.episode_observable_unit_count
        or sum(len(task.observable_ids) for task in series_tasks)
        != bound.series_observable_unit_count
    ):
        raise ValueError("frozen package does not bind supplied calibration and task universe")
    all_tasks: tuple[BlindTask, ...] = (*episode_tasks, *series_tasks)
    if any(
        task.corpus_id != bound.corpus_id or task.corpus_sha256 != bound.corpus_sha256
        for task in all_tasks
    ):
        raise ValueError("prepared tasks mix development corpora")
    selected: dict[str, tuple[BlindTask, ...]] = {
        "episode": human_episode_calibration_tasks(episode_tasks, calibration),
        "series": human_series_calibration_tasks(episode_tasks, series_tasks, calibration),
    }
    files: dict[str, bytes] = {"README.md": _README.encode()}
    packet_hashes: list[str] = []
    prompt_hashes: set[str] = set()
    unit_counts: dict[str, int] = {}
    for kind, expected_tasks in selected.items():
        group = prepared / "blind_packets" / f"human_calibration_{kind}"
        paths = sorted(
            path for path in group.glob("*.json") if not path.name.endswith(".receipt.json")
        )
        expected_by_id = {task.task_id: task for task in expected_tasks}
        if len(expected_by_id) != len(expected_tasks):
            raise ValueError("selected human tasks repeat an identity")
        seen: set[str] = set()
        batch_indices: list[int] = []
        rows: list[dict[str, Any]] = []
        for path in paths:
            if not _PACKET_NAME.fullmatch(path.name):
                raise ValueError("unexpected file in frozen human packet group")
            raw = path.read_bytes()
            packet = BlindDevelopmentPacketArtifact.model_validate_json(raw)
            _verify_packet_bindings(packet, package, calibration)
            if packet.payload.evidence_kind != kind:
                raise ValueError("human packet mixes evidence strata")
            receipt = _read_model(
                path.with_suffix(".receipt.json"), BlindDevelopmentPacketReceiptArtifact
            )
            if receipt != packet_public_safe_receipt(packet):
                raise ValueError("frozen packet receipt does not bind exact human packet")
            batch_indices.append(packet.payload.batch_index)
            if path.name != f"packet-{packet.payload.batch_index:03d}.json":
                raise ValueError("human packet filename disagrees with frozen batch index")
            for task in packet.payload.tasks:
                if task.task_id in seen or task != expected_by_id.get(task.task_id):
                    raise ValueError(
                        "human packets contain duplicate, extra, or changed selected units"
                    )
                seen.add(task.task_id)
                rows.extend(
                    _blank_row(task, observable_id) for observable_id in task.observable_ids
                )
            prompt_hashes.add(packet.payload.instruction_prompt_sha256)
            packet_hashes.append(packet.packet_sha256)
            files[f"packets/{kind}/{path.name}"] = raw
        if seen != set(expected_by_id):
            raise ValueError("human packets are missing frozen selected units")
        if batch_indices != list(range(1, len(paths) + 1)):
            raise ValueError("human packet batches are not complete and sequential")
        unit_counts[kind] = len(rows)
        files[f"{kind}_responses.blank.jsonl"] = b"".join(
            canonical_json_bytes(row) + b"\n" for row in rows
        )
    if len(prompt_hashes) != 1:
        raise ValueError("human packet groups must share one frozen human instruction prompt")
    if (
        unit_counts["episode"] != bound.calibration_episode_unit_count
        or unit_counts["series"] != bound.calibration_series_unit_count
    ):
        raise ValueError("human packet unit counts disagree with frozen package")
    files["episode_response.schema.json"] = canonical_json_bytes(
        DevelopmentEpisodeAnnotationResponse.model_json_schema()
    )
    files["series_response.schema.json"] = canonical_json_bytes(
        DevelopmentSeriesAnnotationResponse.model_json_schema()
    )
    files["auditor_attestation.blank.json"] = canonical_json_bytes(
        {
            "schema_version": "life-patterns-human-auditor-unfilled-attestation-v1",
            "auditor_id": None,
            "independent_of_participant": None,
            "participant_or_theory_exposed_owner": None,
            "target_theory_blind": None,
            "llm_outputs_available_before_first_pass": None,
            "automated_consensus_available_before_first_pass": None,
            "target_model_outputs_available": None,
            "birth_or_chart_data_available": None,
            "automated_coder_used_for_first_pass": None,
            "first_pass_completed_at_utc": None,
            "auditor_notes": None,
        }
    )
    payload = {
        "schema_version": "life-patterns-private-human-handoff-receipt-v1",
        "package_id": package.package_id,
        "package_sha256": package.package_sha256,
        "calibration_manifest_id": calibration.manifest_id,
        "calibration_manifest_sha256": calibration.manifest_sha256,
        "packet_sha256s": packet_hashes,
        "human_prompt_sha256": next(iter(prompt_hashes)),
        "packet_count": len(packet_hashes),
        "episode_unit_count": unit_counts["episode"],
        "series_unit_count": unit_counts["series"],
        "files": {name: sha256_bytes(raw) for name, raw in sorted(files.items())},
        "readiness": "awaiting_human",
        "packet_bytes_preserved": True,
        "selected_unit_coverage_verified": True,
        "response_templates_are_annotations": False,
        "auditor_identity_verified": False,
        "human_blinding_attested": False,
        "development_only": True,
        "validation_use_forbidden": True,
        "contains_private_participant_text": False,
    }
    digest = sha256_json(payload)
    receipt_data = {
        "receipt_id": f"LPHB-{digest[:20].upper()}",
        "receipt_sha256": digest,
        "payload": payload,
    }
    files["human_handoff_public_safe_receipt.json"] = canonical_json_bytes(receipt_data)
    output.mkdir(mode=0o700)
    for relative_name, raw in files.items():
        destination = output / relative_name
        if destination.parent != output:
            (output / "packets").mkdir(mode=0o700, exist_ok=True)
            destination.parent.mkdir(mode=0o700, exist_ok=True)
        write_new_bytes(destination, raw, mode=0o400)
    return receipt_data
