from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.evaluation.development_blind_packets_v2 import (
    build_blind_development_packets_v2,
    packet_public_safe_receipt_v2,
    write_private_blind_packet_v2,
    write_public_safe_packet_receipt_v2,
)
from hdmatch.evaluation.development_human_handoff_v2 import (
    export_development_human_calibration_bundle_v2,
)
from hdmatch.evaluation.development_private_preparation import prepare_v8_private_development_package
from hdmatch.evaluation.development_private_preparation_v2 import (
    prepare_v8_private_development_package_v2,
    private_preparation_v2_safe_summary,
    write_private_development_preparation_v2,
)

HISTORICAL_TIME = datetime(2026, 9, 6, 21, 30, tzinfo=UTC)
V2_TIME = datetime(2026, 9, 8, 20, 0, tzinfo=UTC)


def _original() -> dict[str, object]:
    return {
        "schema_version": "life-patterns-pattern-first-longitudinal-interview-v8",
        "corpus_role": "development_pattern_first_longitudinal_stress_test",
        "prompt_version": "v8",
        "record_status": "complete_after_pattern_review",
        "stop_reason": "synthetic fixture",
        "domains_attempted": [{"domain_id": "P01", "status": "completed"}],
        "pattern_claims": [
            {
                "pattern_id": "PAT-001",
                "domain_id": "P01",
                "participant_claim_text": "Synthetic pattern.",
                "scope_context_qualifiers": "Synthetic scope.",
                "life_phase_claims": "Synthetic history.",
                "approximate_age_ranges": ["adult"],
                "support_state": "anchored_series",
                "supporting_episode_ids": ["EP-001"],
                "supporting_series_report_ids": ["SER-001"],
                "counterexample_episode_ids": [],
                "uncertainty": "none",
                "source_turn_ids": ["T01", "T02"],
            }
        ],
        "series_reports": [
            {
                "series_id": "SER-001",
                "domain_id": "P01",
                "bounded_period_context": "Synthetic repeated period.",
                "approximate_age_life_phase": "adult",
                "participant_recurrence_language": "always",
                "rough_opportunity_count": None,
                "behavior_reportedly_recurred": "Synthetic repeated action.",
                "explicit_exceptions": "rare exception",
                "memory_source_uncertainty": "direct repeated memory",
                "source_turn_ids": ["T02"],
            }
        ],
        "episodes": [
            {
                "episode_id": "EP-001",
                "domain_id": "P01",
                "approximate_age_age_range": "adult",
                "age_estimation_basis": "life phase",
                "memory_source": "direct memory",
                "bounded_situation": "Synthetic optional invitation.",
                "contemporaneous_knowledge_when_relevant": "Invitation was known.",
                "relevant_opportunities_options_constraints": "Could accept or decline.",
                "actions_in_temporal_order": ["Accepted."],
                "outcome_when_known": "Participated.",
                "participant_stated_explanation_if_supplied": None,
                "memory_uncertainty": "none stated",
                "linked_pattern_ids": ["PAT-001"],
                "source_turn_ids": ["T01"],
                "exact_participant_source_segments": ["PRIVATE-SYNTHETIC-EPISODE-TEXT"],
            }
        ],
        "transcript_source_provenance": {
            "interview_source": "synthetic",
            "external_sources_used": False,
            "source_turn_id_convention": "synthetic",
            "source_turn_index": {"T01": "Synthetic episode.", "T02": "Synthetic series."},
        },
        "limitations": ["synthetic"],
    }


def _supplement() -> dict[str, object]:
    return {
        "schema_version": "life-patterns-v8-repair-supplement-v8.1",
        "original_schema_version": "life-patterns-pattern-first-longitudinal-interview-v8",
        "original_record_status": "complete_after_pattern_review",
        "supplement_status": "repair_pass_complete_with_documented_outstanding_issues",
        "source_recovery_status": "partial synthetic recovery",
        "question_log": [],
        "repair_responses": [
            {"response_id": "RR-001", "role": "participant", "exact_text": "PRIVATE-REPAIR"},
            {"response_id": "RR-005", "role": "participant", "exact_text": "yes"},
        ],
        "recovered_transcript_turns": [
            {
                "recovered_turn_id": "RCV-001",
                "original_local_id": "T02",
                "role": "participant_original_elicitation",
                "exact_text": "Whenever this happened I always did X, except under Y.",
                "relevance": "SER-001",
            }
        ],
        "proposed_metadata_corrections": [],
        "participant_confirmed_account_changes": [],
        "post_review_added_evidence": [
            {
                "added_evidence_id": "ADD-EV-001",
                "target_pattern_id": "PAT-001",
                "evidence_type": "concrete_episode",
                "collection_phase": "v8.1 post-interview/post-review repair",
                "approximate_age_life_phase": "adult",
                "memory_source": "direct participant report",
                "bounded_situation": "Synthetic repair event.",
                "actions_in_temporal_order": ["Corrected something."],
                "outcome_when_known": "Done.",
                "participant_stated_explanation": "Synthetic reason.",
                "source_reference": "RR-001",
                "support_implication": "Synthetic support.",
            }
        ],
        "review_record": {
            "review_id": "REVIEW-001",
            "material_shown": ["synthetic repair"],
            "participant_response_reference": "RR-005",
            "participant_response": "yes",
            "interpretation": "synthetic approval",
        },
        "outstanding_issues": [],
        "review_status": (
            "participant_approved_changed_account; "
            "technical_audit_findings_logged_without_overwriting_original"
        ),
        "export_status": "exported_as_separate_v8_1_json; original_v8_json_not_overwritten",
        "limitations": ["synthetic"],
    }


def _historical():
    return prepare_v8_private_development_package(
        original=_original(),
        supplement=_supplement(),
        repo_root=Path("."),
        source_commit="abcdef0123456789",
        created_at_utc=HISTORICAL_TIME,
        episode_calibration_units=2,
        series_calibration_units=1,
        episode_per_observable_floor=0,
        series_per_observable_floor=0,
    )


def _v2():
    return prepare_v8_private_development_package_v2(
        original=_original(),
        supplement=_supplement(),
        repo_root=Path("."),
        historical_source_commit="abcdef0123456789",
        historical_created_at_utc=HISTORICAL_TIME,
        v2_source_commit="fedcba9876543210",
        v2_created_at_utc=V2_TIME,
        episode_calibration_units=2,
        series_calibration_units=1,
        episode_per_observable_floor=0,
        series_per_observable_floor=0,
    )


def _write_human_packet_groups(prepared: Path, preparation) -> None:
    root = prepared / "blind_packets_v2"
    for kind in ("episode", "series"):
        packets = build_blind_development_packets_v2(
            preparation,
            repo_root=Path("."),
            coder_role="human_calibration",
            evidence_kind=kind,
            max_tasks_per_packet=3,
        )
        group = root / f"human_calibration_{kind}"
        group.mkdir(parents=True, exist_ok=True)
        for packet in packets:
            stem = f"packet-{packet.payload.batch_index:03d}"
            write_private_blind_packet_v2(group / f"{stem}.json", packet)
            write_public_safe_packet_receipt_v2(
                group / f"{stem}.receipt.json",
                packet_public_safe_receipt_v2(packet),
            )


def test_v2_reuses_exact_prelabel_selection_without_resampling() -> None:
    historical = _historical()
    v2 = _v2()
    assert v2.corpus == historical.corpus
    assert v2.episode_tasks == historical.episode_tasks
    assert v2.series_report.tasks == historical.series_report.tasks
    assert v2.calibration == historical.calibration
    assert v2.package.payload.calibration_manifest_id == historical.calibration.manifest_id
    assert v2.package.payload.calibration_selection_reused_without_resampling is True
    assert v2.package.payload.calibration_resampled_after_method_revision is False


def test_v2_package_binds_new_semantics_without_target_information() -> None:
    v2 = _v2()
    payload = v2.package.payload
    assert v2.package.package_id.startswith("LPKG2-")
    assert payload.series_response_schema_version == (
        "life-patterns-development-series-annotation-response-v2"
    )
    assert payload.confirming_episodes_are_not_frequency_counts is True
    assert payload.target_model_information_used_for_revision is False
    assert payload.target_model_scoring_authorized is False
    assert payload.validation_use_forbidden is True
    assert v2.stack.recurrence_policy_sha256 == payload.recurrence_policy_sha256


def test_v2_public_safe_summary_contains_no_private_text() -> None:
    rendered = json.dumps(private_preparation_v2_safe_summary(_v2()), sort_keys=True)
    assert "PRIVATE-" not in rendered
    assert '"contains_private_participant_text": false' in rendered
    assert '"calibration_selection_reused_without_resampling": true' in rendered
    assert '"confirming_episodes_are_not_frequency_counts": true' in rendered


def test_v2_human_packets_bind_manual_policy_and_reused_selection() -> None:
    preparation = _v2()
    series_packets = build_blind_development_packets_v2(
        preparation,
        repo_root=Path("."),
        coder_role="human_calibration",
        evidence_kind="series",
    )
    assert len(series_packets) == 1
    packet = series_packets[0]
    assert packet.payload.package_id == preparation.package.package_id
    assert packet.payload.recurrence_policy_sha256 == preparation.stack.recurrence_policy_sha256
    assert packet.payload.calibration_manifest_id == preparation.calibration.manifest_id
    assert packet.payload.confirming_episodes_counted_as_frequency_evidence is False
    assert packet.payload.series_response_schema_version.endswith("response-v2")
    assert packet.payload.target_model_information_available is False


def test_v2_human_handoff_exports_v2_series_schema_without_annotations(tmp_path: Path) -> None:
    preparation = _v2()
    prepared = tmp_path / "prepared"
    output = tmp_path / "handoff"
    write_private_development_preparation_v2(prepared, preparation)
    _write_human_packet_groups(prepared, preparation)

    receipt = export_development_human_calibration_bundle_v2(prepared, output)
    payload = receipt["payload"]
    assert receipt["receipt_id"].startswith("LPHB2-")
    assert payload["package_id"] == preparation.package.package_id
    assert payload["series_response_schema_version"] == (
        "life-patterns-development-series-annotation-response-v2"
    )
    assert payload["calibration_selection_reused_without_resampling"] is True
    assert payload["confirming_episodes_are_not_frequency_counts"] is True
    assert payload["human_facing_ui_required_before_collection"] is True
    assert payload["response_templates_are_annotations"] is False
    assert payload["readiness"] == "awaiting_human_ui"

    series_rows = [
        json.loads(line)
        for line in (output / "series_responses.blank.jsonl").read_text().splitlines()
    ]
    assert len(series_rows) == 1
    assert series_rows[0]["schema_version"] == (
        "life-patterns-development-series-annotation-response-v2"
    )
    assert series_rows[0]["reported_recurrence_strength"] is None
    assert series_rows[0]["minimum_reported_occurrences"] is None
    assert series_rows[0]["confirming_episode_counted_as_independent_frequency_evidence"] is False
