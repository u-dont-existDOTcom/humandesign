from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.evaluation.development_private_preparation import (
    deterministic_calibration_seed,
    prepare_v8_private_development_package,
    private_preparation_safe_summary,
)


NOW = datetime(2026, 9, 6, 21, 30, tzinfo=UTC)


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
                "participant_recurrence_language": "many times",
                "rough_opportunity_count": "at least 3",
                "behavior_reportedly_recurred": "Synthetic repeated action.",
                "explicit_exceptions": None,
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
            "source_turn_index": {
                "T01": "Synthetic episode.",
                "T02": "Synthetic series.",
            },
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
            {
                "response_id": "RR-001",
                "role": "participant",
                "exact_text": "PRIVATE-SYNTHETIC-REPAIR-TEXT",
            },
            {
                "response_id": "RR-005",
                "role": "participant",
                "exact_text": "yes",
            },
        ],
        "recovered_transcript_turns": [
            {
                "recovered_turn_id": "RCV-001",
                "original_local_id": "T02",
                "role": "participant_original_elicitation",
                "exact_text": "PRIVATE-SYNTHETIC-SERIES-TEXT",
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


def test_private_preparation_builds_bound_package_without_running_coder() -> None:
    prep = prepare_v8_private_development_package(
        original=_original(),
        supplement=_supplement(),
        repo_root=Path("."),
        source_commit="abcdef0123456789",
        created_at_utc=NOW,
        episode_calibration_units=2,
        series_calibration_units=1,
        episode_per_observable_floor=0,
        series_per_observable_floor=0,
    )
    assert len(prep.episode_tasks) == 2
    assert prep.episode_manifest.payload.episode_task_count == 2
    assert prep.episode_manifest.payload.observable_count == 22
    assert prep.episode_manifest.payload.expected_episode_observable_unit_count == 44
    assert prep.series_report.eligible_series_count == 1
    assert prep.series_report.blocked_series_count == 0
    assert prep.series_manifest is not None
    assert prep.series_manifest.payload.expected_series_observable_unit_count == 22
    assert len(prep.calibration.payload.representative_episode_units) == 2
    assert len(prep.calibration.payload.representative_series_units) == 1
    assert prep.package.payload.required_isolated_automated_passes == 3
    assert prep.package.payload.validation_use_forbidden is True
    assert prep.package.payload.target_model_scoring_authorized is False
    assert prep.package.payload.contains_private_participant_text is False


def test_calibration_seed_depends_only_on_source_hashes_and_fixed_policy() -> None:
    first = deterministic_calibration_seed(
        source_record_sha256="1" * 64,
        supplement_sha256="2" * 64,
    )
    second = deterministic_calibration_seed(
        source_record_sha256="1" * 64,
        supplement_sha256="2" * 64,
    )
    changed = deterministic_calibration_seed(
        source_record_sha256="1" * 64,
        supplement_sha256="3" * 64,
    )
    assert first == second
    assert first != changed
    assert len(first) == 64


def test_public_safe_summary_contains_no_private_text() -> None:
    prep = prepare_v8_private_development_package(
        original=_original(),
        supplement=_supplement(),
        repo_root=Path("."),
        source_commit="abcdef0123456789",
        created_at_utc=NOW,
        episode_calibration_units=2,
        series_calibration_units=1,
        episode_per_observable_floor=0,
        series_per_observable_floor=0,
    )
    rendered = json.dumps(private_preparation_safe_summary(prep), sort_keys=True)
    assert "PRIVATE-SYNTHETIC" not in rendered
    assert '"contains_private_participant_text": false' in rendered
    assert '"validation_use_forbidden": true' in rendered
