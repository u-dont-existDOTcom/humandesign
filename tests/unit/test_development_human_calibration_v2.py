from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.development_calibration_sampling import (
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from hdmatch.evaluation.development_episode_evidence import DevelopmentEpisodeAnnotationResponse
from hdmatch.evaluation.development_human_calibration_v2 import (
    build_development_human_episode_first_pass_v2,
    build_development_human_series_first_pass_v2,
    development_human_first_pass_v2_integrity_errors,
    normalize_development_series_responses_v2_jsonl,
)
from hdmatch.evaluation.development_private_preparation_v2 import (
    prepare_v8_private_development_package_v2,
)
from hdmatch.evaluation.development_series_evidence_v2 import DevelopmentSeriesAnnotationResponseV2
from hdmatch.experiments.canonical import canonical_json_bytes

HISTORICAL_TIME = datetime(2026, 9, 6, 21, 30, tzinfo=UTC)
V2_TIME = datetime(2026, 9, 8, 20, 0, tzinfo=UTC)
FIRST_PASS_TIME = datetime(2026, 9, 8, 21, 0, tzinfo=UTC)


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


def _preparation():
    return prepare_v8_private_development_package_v2(
        original=_original(),
        supplement=_supplement(),
        repo_root=Path("."),
        historical_source_commit="abcdef0123456789",
        historical_created_at_utc=HISTORICAL_TIME,
        v2_source_commit="fedcba9876543210",
        v2_created_at_utc=V2_TIME,
        episode_calibration_units=1,
        series_calibration_units=1,
        episode_per_observable_floor=0,
        series_per_observable_floor=0,
    )


def _safe_nominal_value(preparation, observable_id: str) -> str:
    definition = next(
        row for row in preparation.stack.ontology.payload.observables if row.observable_id == observable_id
    )
    extension = next(
        row
        for row in preparation.stack.procedure.payload.observable_extensions
        if row.observable_id == observable_id
    )
    assert definition.value_type in {"nominal", "ordinal"}
    for value in definition.allowed_values:
        if value not in extension.non_action_values and value != extension.other_specified_value:
            return value
    raise AssertionError(f"no ordinary synthetic-safe value for {observable_id}")


def _episode_response(preparation) -> DevelopmentEpisodeAnnotationResponse:
    task = human_episode_calibration_tasks(
        preparation.episode_tasks,
        preparation.calibration,
    )[0]
    observable_id = task.observable_ids[0]
    return DevelopmentEpisodeAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id=observable_id,
        state="observed",
        coded_values=(_safe_nominal_value(preparation, observable_id),),
        value_relation="single",
        supporting_source_segment_ids=(task.exact_source_segments[0].segment_id,),
        theory_exposure=task.participant_theory_exposure,
    )


def _series_response(preparation) -> DevelopmentSeriesAnnotationResponseV2:
    task = human_series_calibration_tasks(
        preparation.episode_tasks,
        preparation.series_report.tasks,
        preparation.calibration,
    )[0]
    observable_id = task.observable_ids[0]
    return DevelopmentSeriesAnnotationResponseV2(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id=observable_id,
        state="observed",
        coded_values=(_safe_nominal_value(preparation, observable_id),),
        value_relation="single",
        reported_recurrence_strength="universal_language",
        exception_status="exceptions_reported",
        exception_frequency="context_dependent",
        frequency_evidence_basis="generalized_self_report",
        minimum_reported_occurrences=None,
        recurrence_scope_description="synthetic repeated opportunities",
        supporting_source_segment_ids=(task.exact_source_segments[0].segment_id,),
        theory_exposure=task.participant_theory_exposure,
    )


def test_episode_first_pass_v2_binds_package_policy_and_exact_selection() -> None:
    preparation = _preparation()
    response = _episode_response(preparation)
    raw = canonical_json_bytes(response) + b"\n"
    artifact = build_development_human_episode_first_pass_v2(
        auditor_id="private-auditor-001",
        raw_output=raw,
        normalized_output=raw,
        package=preparation.package,
        calibration=preparation.calibration,
        episode_tasks=preparation.episode_tasks,
        series_tasks=preparation.series_report.tasks,
        ontology=preparation.stack.ontology,
        procedure=preparation.stack.procedure,
        created_at_utc=FIRST_PASS_TIME,
    )

    assert artifact.artifact_id.startswith("LPHF2-")
    assert artifact.payload.package_id == preparation.package.package_id
    assert artifact.payload.recurrence_policy_sha256 == preparation.stack.recurrence_policy_sha256
    assert artifact.payload.expected_unit_count == 1
    assert artifact.payload.human_facing_offline_ui_used is True
    assert artifact.payload.confirming_episodes_counted_as_frequency_evidence is False
    assert development_human_first_pass_v2_integrity_errors(artifact) == ()


def test_series_first_pass_v2_accepts_generalized_recurrence_without_fake_count() -> None:
    preparation = _preparation()
    response = _series_response(preparation)
    raw = canonical_json_bytes(response) + b"\n"
    assert normalize_development_series_responses_v2_jsonl(raw) == raw

    artifact = build_development_human_series_first_pass_v2(
        auditor_id="private-auditor-001",
        raw_output=raw,
        normalized_output=raw,
        package=preparation.package,
        calibration=preparation.calibration,
        episode_tasks=preparation.episode_tasks,
        series_tasks=preparation.series_report.tasks,
        ontology=preparation.stack.ontology,
        procedure=preparation.stack.procedure,
        created_at_utc=FIRST_PASS_TIME,
    )

    assert response.minimum_reported_occurrences is None
    assert response.frequency_evidence_basis == "generalized_self_report"
    assert artifact.payload.expected_unit_count == 1
    assert artifact.payload.recurrence_policy_sha256 == preparation.package.payload.recurrence_policy_sha256
    assert development_human_first_pass_v2_integrity_errors(artifact) == ()


def test_first_pass_v2_fails_closed_on_incomplete_selected_coverage() -> None:
    preparation = _preparation()
    with pytest.raises(ValueError, match="exactly cover selected units"):
        build_development_human_series_first_pass_v2(
            auditor_id="private-auditor-001",
            raw_output=b"",
            normalized_output=b"",
            package=preparation.package,
            calibration=preparation.calibration,
            episode_tasks=preparation.episode_tasks,
            series_tasks=preparation.series_report.tasks,
            ontology=preparation.stack.ontology,
            procedure=preparation.stack.procedure,
            created_at_utc=FIRST_PASS_TIME,
        )
