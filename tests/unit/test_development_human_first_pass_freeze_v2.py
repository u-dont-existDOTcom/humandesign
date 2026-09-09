from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.development_blind_packets_v2 import (
    BlindDevelopmentPacketArtifactV2,
    BlindDevelopmentPacketPayloadV2,
)
from hdmatch.evaluation.development_episode_evidence import DevelopmentEpisodeAnnotationResponse
from hdmatch.evaluation.development_human_first_pass_freeze_v2 import (
    freeze_human_first_pass_from_handoff_v2,
    human_first_pass_freeze_receipt_v2_integrity_errors,
    verify_human_handoff_for_first_pass_v2,
    write_human_first_pass_freeze_v2,
)
from hdmatch.evaluation.development_series_evidence import DevelopmentSeriesCodingTask
from hdmatch.evaluation.development_series_evidence_v2 import DevelopmentSeriesAnnotationResponseV2
from hdmatch.evaluation.development_transfer_corpus import (
    DevelopmentEpisodeCodingTask,
    DevelopmentSourceSegment,
)
from hdmatch.evaluation.resolved_development_stack_v2 import (
    build_repository_resolved_development_stack_v2,
)
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

ROOT = Path(__file__).resolve().parents[2]
NOW = datetime(2026, 9, 9, 12, 0, tzinfo=UTC)
CORPUS_ID = "LPDC-" + "A" * 20
CORPUS_SHA = "a" * 64
PACKAGE_ID = "LPKG2-" + "B" * 20
PACKAGE_SHA = "b" * 64
CALIBRATION_ID = "LPCA-" + "C" * 20
CALIBRATION_SHA = "c" * 64
PROMPT_TEXT = "Synthetic independent human calibration prompt."
PROMPT_SHA = hashlib.sha256(PROMPT_TEXT.encode()).hexdigest()


def _stack():
    return build_repository_resolved_development_stack_v2(
        ROOT,
        source_commit="abcdef0123456789",
        released_at_utc=NOW,
    )


def _tasks() -> tuple[DevelopmentEpisodeCodingTask, DevelopmentSeriesCodingTask]:
    episode_segment = DevelopmentSourceSegment(
        segment_id="E-S1",
        exact_text="Synthetic private episode source.",
        provenance_refs=("T01",),
    )
    series_segment = DevelopmentSourceSegment(
        segment_id="S-S1",
        exact_text="Synthetic private recurrence source.",
        provenance_refs=("T02",),
    )
    episode = DevelopmentEpisodeCodingTask(
        task_id="LPDT-" + "D" * 20,
        corpus_id=CORPUS_ID,
        corpus_sha256=CORPUS_SHA,
        episode_id="EP-001",
        approximate_age_life_phase="adult",
        episode_narrative="Synthetic bounded event.",
        exact_source_segments=(episode_segment,),
        source_completeness="partial_exact_segments_plus_transfer_summary",
        observable_ids=("NBM-R01",),
        participant_theory_exposure="unknown",
    )
    series = DevelopmentSeriesCodingTask(
        task_id="LPST-" + "E" * 20,
        corpus_id=CORPUS_ID,
        corpus_sha256=CORPUS_SHA,
        series_id="SER-001",
        bounded_period_context="Synthetic repeated opportunities.",
        approximate_age_life_phase="adult",
        recurrence_language="always",
        behavior_reportedly_recurred="Synthetic repeated action.",
        explicit_exceptions_or_limits="except under a synthetic boundary",
        exact_source_segments=(series_segment,),
        observable_ids=("NBM-R01",),
        participant_theory_exposure="unknown",
    )
    return episode, series


def _packet(kind: str, task, batch_index: int) -> BlindDevelopmentPacketArtifactV2:
    stack = _stack()
    payload = BlindDevelopmentPacketPayloadV2(
        coder_role="human_calibration",
        evidence_kind=kind,
        batch_index=batch_index,
        package_id=PACKAGE_ID,
        package_sha256=PACKAGE_SHA,
        corpus_id=CORPUS_ID,
        corpus_sha256=CORPUS_SHA,
        reconciled_source=stack.source,
        ambiguity_resolution=stack.resolution,
        resolved_view=stack.resolved,
        ontology=stack.ontology,
        procedure=stack.procedure,
        coding_manual_sha256=stack.coding_manual_sha256,
        coding_manual_text=(ROOT / "state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md").read_text(),
        recurrence_policy_sha256=stack.recurrence_policy_sha256,
        recurrence_policy_text=(
            ROOT / "docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md"
        ).read_text(),
        instruction_prompt_sha256=PROMPT_SHA,
        instruction_prompt_text=PROMPT_TEXT,
        tasks=(task,),
        assigned_unit_count=1,
        calibration_manifest_id=CALIBRATION_ID,
        calibration_manifest_sha256=CALIBRATION_SHA,
    )
    digest = sha256_json(payload)
    return BlindDevelopmentPacketArtifactV2(
        packet_id=f"LPBP2-{digest[:20].upper()}",
        packet_sha256=digest,
        payload=payload,
    )


def _blank_episode_row(task: DevelopmentEpisodeCodingTask) -> dict[str, object]:
    return {
        "schema_version": "life-patterns-development-episode-annotation-response-v1",
        "task_id": task.task_id,
        "corpus_id": task.corpus_id,
        "corpus_sha256": task.corpus_sha256,
        "episode_id": task.episode_id,
        "observable_id": "NBM-R01",
        "state": None,
    }


def _blank_series_row(task: DevelopmentSeriesCodingTask) -> dict[str, object]:
    return {
        "schema_version": "life-patterns-development-series-annotation-response-v2",
        "task_id": task.task_id,
        "corpus_id": task.corpus_id,
        "corpus_sha256": task.corpus_sha256,
        "series_id": task.series_id,
        "observable_id": "NBM-R01",
        "state": None,
    }


def _write_handoff_zip(path: Path) -> tuple[DevelopmentEpisodeCodingTask, DevelopmentSeriesCodingTask]:
    episode_task, series_task = _tasks()
    episode_packet = _packet("episode", episode_task, 1)
    series_packet = _packet("series", series_task, 1)
    files: dict[str, bytes] = {
        "packets/episode/packet-001.json": canonical_json_bytes(episode_packet),
        "packets/series/packet-001.json": canonical_json_bytes(series_packet),
        "episode_responses.blank.jsonl": canonical_json_bytes(_blank_episode_row(episode_task)) + b"\n",
        "series_responses.blank.jsonl": canonical_json_bytes(_blank_series_row(series_task)) + b"\n",
    }
    stack = _stack()
    receipt_payload = {
        "schema_version": "life-patterns-private-human-handoff-receipt-v2",
        "package_id": PACKAGE_ID,
        "package_sha256": PACKAGE_SHA,
        "calibration_manifest_id": CALIBRATION_ID,
        "calibration_manifest_sha256": CALIBRATION_SHA,
        "packet_sha256s": [episode_packet.packet_sha256, series_packet.packet_sha256],
        "human_prompt_sha256": PROMPT_SHA,
        "recurrence_policy_sha256": stack.recurrence_policy_sha256,
        "coding_manual_sha256": stack.coding_manual_sha256,
        "packet_count": 2,
        "episode_unit_count": 1,
        "series_unit_count": 1,
        "files": {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(files.items())},
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
    }
    receipt_digest = sha256_json(receipt_payload)
    receipt = {
        "receipt_id": f"LPHB2-{receipt_digest[:20].upper()}",
        "receipt_sha256": receipt_digest,
        "payload": receipt_payload,
    }
    files["human_handoff_public_safe_receipt_v2.json"] = canonical_json_bytes(receipt)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in files.items():
            archive.writestr(name, raw)
    return episode_task, series_task


def _episode_output(task: DevelopmentEpisodeCodingTask) -> bytes:
    row = DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R01",
        state="insufficient",
        theory_exposure="unknown",
    )
    return canonical_json_bytes(row) + b"\n"


def _series_output(task: DevelopmentSeriesCodingTask) -> bytes:
    row = DevelopmentSeriesAnnotationResponseV2(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id="NBM-R01",
        state="insufficient",
        theory_exposure="unknown",
    )
    return canonical_json_bytes(row) + b"\n"


def _attestation(**overrides: object) -> bytes:
    values: dict[str, object] = {
        "schema_version": "life-patterns-human-auditor-attestation-v2",
        "auditor_id": "private-auditor-001",
        "independent_of_participant": True,
        "participant_or_theory_exposed_owner": False,
        "target_theory_blind": True,
        "llm_outputs_available_before_first_pass": False,
        "automated_consensus_available_before_first_pass": False,
        "target_model_outputs_available": False,
        "birth_or_chart_data_available": False,
        "automated_coder_used_for_first_pass": False,
        "human_facing_offline_ui_used": True,
        "first_pass_completed_at_utc": NOW.isoformat(),
        "auditor_notes": "synthetic private note",
    }
    values.update(overrides)
    return json.dumps(values, sort_keys=True).encode()


def test_portable_freeze_validates_handoff_and_preserves_raw_exports(tmp_path: Path) -> None:
    handoff_zip = tmp_path / "handoff.zip"
    episode_task, series_task = _write_handoff_zip(handoff_zip)
    raw_episode = _episode_output(episode_task)
    raw_series = _series_output(series_task)
    raw_attestation = _attestation()

    verified = verify_human_handoff_for_first_pass_v2(handoff_zip)
    assert verified.episode_unit_count == 1
    assert verified.series_unit_count == 1

    output = tmp_path / "freeze"
    receipt = write_human_first_pass_freeze_v2(
        output_dir=output,
        handoff_zip=handoff_zip,
        raw_episode_output=raw_episode,
        raw_series_output=raw_series,
        raw_attestation=raw_attestation,
        frozen_at_utc=NOW + timedelta(minutes=1),
    )

    assert receipt.receipt_id.startswith("LPHFR2-")
    assert receipt.payload.human_gate_satisfied is True
    assert receipt.payload.episode_unit_count == 1
    assert receipt.payload.series_unit_count == 1
    assert receipt.payload.automated_coding_run_as_part_of_freeze is False
    assert human_first_pass_freeze_receipt_v2_integrity_errors(receipt) == ()
    assert (output / "episode_responses.raw.jsonl").read_bytes() == raw_episode
    assert (output / "series_responses.raw.jsonl").read_bytes() == raw_series
    assert (output / "auditor_attestation.raw.json").read_bytes() == raw_attestation

    public_text = (output / "human_first_pass_public_safe_receipt.json").read_text()
    assert "private-auditor-001" not in public_text
    assert "Synthetic private" not in public_text


def test_portable_freeze_fails_closed_on_incomplete_selected_coverage(tmp_path: Path) -> None:
    handoff_zip = tmp_path / "handoff.zip"
    episode_task, _ = _write_handoff_zip(handoff_zip)
    with pytest.raises(ValueError, match="series first pass does not exactly cover"):
        freeze_human_first_pass_from_handoff_v2(
            handoff_zip=handoff_zip,
            raw_episode_output=_episode_output(episode_task),
            raw_series_output=b"",
            raw_attestation=_attestation(),
            frozen_at_utc=NOW + timedelta(minutes=1),
        )


def test_portable_freeze_fails_closed_on_contaminated_attestation(tmp_path: Path) -> None:
    handoff_zip = tmp_path / "handoff.zip"
    episode_task, series_task = _write_handoff_zip(handoff_zip)
    with pytest.raises(ValidationError):
        freeze_human_first_pass_from_handoff_v2(
            handoff_zip=handoff_zip,
            raw_episode_output=_episode_output(episode_task),
            raw_series_output=_series_output(series_task),
            raw_attestation=_attestation(automated_coder_used_for_first_pass=True),
            frozen_at_utc=NOW + timedelta(minutes=1),
        )


def test_portable_freeze_rejects_tampered_handoff_member(tmp_path: Path) -> None:
    handoff_zip = tmp_path / "handoff.zip"
    _write_handoff_zip(handoff_zip)
    tampered = tmp_path / "tampered.zip"
    with zipfile.ZipFile(handoff_zip) as source, zipfile.ZipFile(tampered, "w") as target:
        for name in source.namelist():
            raw = source.read(name)
            if name == "episode_responses.blank.jsonl":
                raw += b" "
            target.writestr(name, raw)
    with pytest.raises(ValueError, match="member hash mismatch"):
        verify_human_handoff_for_first_pass_v2(tampered)
