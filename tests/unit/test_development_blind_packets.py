from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.development_blind_packets import (
    build_blind_development_packets,
    packet_public_safe_receipt,
)
from hdmatch.evaluation.development_calibration_sampling import build_development_calibration_sample
from hdmatch.evaluation.development_coding_package import build_development_coding_package
from hdmatch.evaluation.development_private_preparation import (
    EPISODE_TRANSPORT_PROMPT_REL,
    SERIES_TRANSPORT_PROMPT_REL,
    PrivateDevelopmentPreparation,
    deterministic_calibration_seed,
)
from hdmatch.evaluation.development_series_evidence import (
    build_development_series_manifest,
    build_development_series_tasks,
)
from hdmatch.evaluation.development_transfer_corpus import (
    DevelopmentSourceSegment,
    DevelopmentTransferCorpusArtifact,
    DevelopmentTransferCorpusPayload,
    DevelopmentTransferEpisode,
    DevelopmentTransferSeriesReport,
    build_development_episode_tasks,
    build_development_task_manifest,
)
from hdmatch.evaluation.resolved_development_stack import (
    build_repository_resolved_development_stack,
    file_sha256,
)
from hdmatch.experiments.canonical import sha256_json


NOW = datetime(2026, 9, 6, 23, 0, tzinfo=UTC)
PRIVATE_MARKER = "PRIVATE-SYNTHETIC-PARTICIPANT-TEXT"


def _preparation() -> PrivateDevelopmentPreparation:
    stack = build_repository_resolved_development_stack(
        Path("."),
        source_commit="abcdef0123456789",
        released_at_utc=NOW,
    )
    segment = DevelopmentSourceSegment(
        segment_id="EP-001-SEG-01",
        exact_text=PRIVATE_MARKER,
        provenance_refs=("T01",),
    )
    episode = DevelopmentTransferEpisode(
        episode_id="EP-001",
        origin_id="EP-001",
        collection_phase="v8_original",
        domain_id="P01",
        approximate_age_life_phase="adult",
        source_review_scope="pattern_reviewed_transfer_summary",
        source_completeness="partial_exact_segments_plus_transfer_summary",
        bounded_situation="Private synthetic bounded situation.",
        actions_in_temporal_order=("Accepted.",),
        exact_source_segments=(segment,),
        transfer_summary="Private synthetic transfer summary.",
    )
    series = DevelopmentTransferSeriesReport(
        series_id="SER-001",
        origin_id="SER-001",
        collection_phase="v8_original",
        domain_id="P01",
        bounded_period_context="Private synthetic repeated period.",
        approximate_age_life_phase="adult",
        recurrence_language="many times",
        rough_opportunity_count="at least 3",
        behavior_reportedly_recurred="Private synthetic repeated behavior.",
        exact_source_segments=(
            DevelopmentSourceSegment(
                segment_id="SER-001-SEG-01",
                exact_text=PRIVATE_MARKER + "-SERIES",
                provenance_refs=("T02",),
            ),
        ),
        source_completeness="partial_exact_recovered_turns",
    )
    payload = DevelopmentTransferCorpusPayload(
        source_record_schema_version="life-patterns-pattern-first-longitudinal-interview-v8",
        source_record_sha256="1" * 64,
        supplement_schema_version="life-patterns-v8-repair-supplement-v8.1",
        supplement_sha256="2" * 64,
        participant_theory_exposure="prior_exposure_possible",
        source_record_status="complete_after_pattern_review",
        supplement_status="repair_pass_complete_with_documented_outstanding_issues",
        episodes=(episode,),
        series_reports=(series,),
        pattern_claims=(),
        auxiliary_post_review_evidence=(),
        created_at_utc=NOW,
    )
    corpus_sha = sha256_json(payload)
    corpus = DevelopmentTransferCorpusArtifact(
        corpus_id=f"LPDC-{corpus_sha[:20].upper()}",
        corpus_sha256=corpus_sha,
        payload=payload,
    )
    episode_tasks = build_development_episode_tasks(corpus, observable_ids=stack.observable_ids)
    episode_manifest = build_development_task_manifest(corpus, tasks=episode_tasks, created_at_utc=NOW)
    series_report = build_development_series_tasks(corpus, observable_ids=stack.observable_ids)
    series_manifest = build_development_series_manifest(series_report, created_at_utc=NOW)
    seed = deterministic_calibration_seed(
        source_record_sha256=payload.source_record_sha256,
        supplement_sha256=payload.supplement_sha256,
    )
    calibration = build_development_calibration_sample(
        episode_tasks=episode_tasks,
        series_tasks=series_report.tasks,
        episode_sample_size=2,
        series_sample_size=1,
        episode_per_observable_floor=0,
        series_per_observable_floor=0,
        seed_sha256=seed,
        created_at_utc=NOW,
    )
    episode_prompt_sha = file_sha256(EPISODE_TRANSPORT_PROMPT_REL)
    series_prompt_sha = file_sha256(SERIES_TRANSPORT_PROMPT_REL)
    package = build_development_coding_package(
        corpus=corpus,
        stack=stack,
        episode_tasks=episode_tasks,
        episode_manifest=episode_manifest,
        episode_transport_prompt_sha256=episode_prompt_sha,
        series_tasks=series_report.tasks,
        series_manifest=series_manifest,
        series_transport_prompt_sha256=series_prompt_sha,
        blocked_summary_only_series_ids=series_report.blocked_summary_only_series_ids,
        calibration=calibration,
        created_at_utc=NOW,
    )
    return PrivateDevelopmentPreparation(
        stack=stack,
        corpus=corpus,
        episode_tasks=episode_tasks,
        episode_manifest=episode_manifest,
        series_report=series_report,
        series_manifest=series_manifest,
        calibration=calibration,
        package=package,
        calibration_seed_sha256=seed,
        episode_transport_prompt_sha256=episode_prompt_sha,
        series_transport_prompt_sha256=series_prompt_sha,
    )


def test_automated_episode_packet_contains_full_frozen_task_without_target_information() -> None:
    prep = _preparation()
    packets = build_blind_development_packets(
        prep,
        repo_root=Path("."),
        coder_role="automated",
        evidence_kind="episode",
        max_tasks_per_packet=1,
    )
    assert len(packets) == 1
    packet = packets[0]
    assert len(packet.payload.tasks) == 1
    assert len(packet.payload.tasks[0].observable_ids) == 22
    assert packet.payload.assigned_unit_count == 22
    assert packet.payload.instruction_prompt_sha256 == prep.package.payload.episode_transport_prompt_sha256
    assert packet.payload.target_model_information_available is False
    assert packet.payload.birth_or_chart_data_available is False
    assert packet.payload.prior_automated_labels_available is False
    assert packet.payload.validation_use_forbidden is True


def test_human_packet_contains_only_preselected_units_and_no_automated_labels() -> None:
    prep = _preparation()
    packets = build_blind_development_packets(
        prep,
        repo_root=Path("."),
        coder_role="human_calibration",
        evidence_kind="episode",
        max_tasks_per_packet=5,
    )
    assert len(packets) == 1
    packet = packets[0]
    assert packet.payload.assigned_unit_count == 2
    assert len(packet.payload.tasks[0].observable_ids) == 2
    assert packet.payload.calibration_manifest_id == prep.calibration.manifest_id
    assert packet.payload.calibration_manifest_sha256 == prep.calibration.manifest_sha256
    assert packet.payload.prior_automated_labels_available is False
    assert packet.payload.automated_consensus_available is False


def test_automated_series_packet_uses_separate_series_transport_prompt() -> None:
    prep = _preparation()
    packet = build_blind_development_packets(
        prep,
        repo_root=Path("."),
        coder_role="automated",
        evidence_kind="series",
        max_tasks_per_packet=1,
    )[0]
    assert packet.payload.evidence_kind == "series"
    assert packet.payload.assigned_unit_count == 22
    assert packet.payload.instruction_prompt_sha256 == prep.package.payload.series_transport_prompt_sha256


def test_public_safe_packet_receipt_does_not_repeat_private_text() -> None:
    packet = build_blind_development_packets(
        _preparation(),
        repo_root=Path("."),
        coder_role="automated",
        evidence_kind="episode",
    )[0]
    assert PRIVATE_MARKER in json.dumps(packet.model_dump(mode="json"), sort_keys=True)
    receipt = packet_public_safe_receipt(packet)
    rendered = json.dumps(receipt.model_dump(mode="json"), sort_keys=True)
    assert PRIVATE_MARKER not in rendered
    assert receipt.payload.receipt_contains_private_participant_text is False
    assert receipt.payload.target_model_information_available is False


def test_public_receipts_reject_narrative_in_identifier_fields() -> None:
    prep = _preparation()
    package_payload = prep.package.payload.model_dump(mode="json")
    package_payload["blocked_summary_only_series_ids"] = [PRIVATE_MARKER]
    with pytest.raises(ValueError, match="blocked_summary_only_series_ids"):
        type(prep.package.payload).model_validate(package_payload)
    package_payload["blocked_summary_only_series_ids"] = ["SER-002", "ADD-EV-002"]
    type(prep.package.payload).model_validate(package_payload)

    packet = build_blind_development_packets(
        prep, repo_root=Path("."), coder_role="automated", evidence_kind="episode"
    )[0]
    receipt = packet_public_safe_receipt(packet)
    receipt_payload = receipt.payload.model_dump(mode="json")
    receipt_payload["task_ids"] = [PRIVATE_MARKER]
    with pytest.raises(ValueError, match="task_ids"):
        type(receipt.payload).model_validate(receipt_payload)


def test_packet_batch_size_is_bounded_to_five_tasks() -> None:
    with pytest.raises(ValueError, match="between 1 and 5"):
        build_blind_development_packets(
            _preparation(),
            repo_root=Path("."),
            coder_role="automated",
            evidence_kind="episode",
            max_tasks_per_packet=6,
        )
