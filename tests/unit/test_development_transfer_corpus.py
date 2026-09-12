from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.development_transfer_corpus import (
    DevelopmentTransferCorpusArtifact,
    build_development_episode_tasks,
    build_development_task_manifest,
    build_v8_v8_1_development_corpus,
    development_transfer_corpus_integrity_errors,
)


NOW = datetime(2026, 9, 6, 19, 30, tzinfo=UTC)


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
                "participant_claim_text": "Synthetic recurring pattern.",
                "scope_context_qualifiers": "Synthetic scope.",
                "life_phase_claims": "Synthetic life history.",
                "approximate_age_ranges": ["childhood", "adult"],
                "support_state": "anchored_series",
                "supporting_episode_ids": ["EP-001"],
                "supporting_series_report_ids": ["SER-001"],
                "counterexample_episode_ids": ["EP-002"],
                "uncertainty": "Synthetic uncertainty.",
                "source_turn_ids": ["T01", "T02", "T03"],
            }
        ],
        "series_reports": [
            {
                "series_id": "SER-001",
                "domain_id": "P01",
                "bounded_period_context": "A synthetic repeated period.",
                "approximate_age_life_phase": "adult",
                "participant_recurrence_language": "many times",
                "rough_opportunity_count": "at least 3",
                "behavior_reportedly_recurred": "Repeated synthetic action.",
                "explicit_exceptions": "One exception.",
                "memory_source_uncertainty": "direct repeated memory",
                "source_turn_ids": ["T02"],
            }
        ],
        "episodes": [
            {
                "episode_id": "EP-001",
                "domain_id": "P01",
                "approximate_age_age_range": "~10",
                "age_estimation_basis": "explicit approximate age",
                "memory_source": "direct memory",
                "bounded_situation": "A synthetic opportunity occurred.",
                "contemporaneous_knowledge_when_relevant": "The opportunity was noticed.",
                "relevant_opportunities_options_constraints": "Participation was optional.",
                "actions_in_temporal_order": ["Considered it.", "Accepted it."],
                "outcome_when_known": "Synthetic outcome.",
                "participant_stated_explanation_if_supplied": "Synthetic explanation.",
                "memory_uncertainty": "age approximate",
                "linked_pattern_ids": ["PAT-001"],
                "source_turn_ids": ["T01"],
                "exact_participant_source_segments": ["synthetic exact participant fragment one"],
            },
            {
                "episode_id": "EP-002",
                "domain_id": "P01",
                "approximate_age_age_range": "adult",
                "age_estimation_basis": "life phase",
                "memory_source": "direct memory",
                "bounded_situation": "A comparable synthetic opportunity occurred.",
                "contemporaneous_knowledge_when_relevant": "The opportunity was noticed.",
                "relevant_opportunities_options_constraints": "Participation was optional.",
                "actions_in_temporal_order": ["Declined it."],
                "outcome_when_known": "No participation.",
                "participant_stated_explanation_if_supplied": None,
                "memory_uncertainty": "none stated",
                "linked_pattern_ids": ["PAT-001"],
                "source_turn_ids": ["T03"],
                "exact_participant_source_segments": ["synthetic exact participant fragment two"],
            },
        ],
        "transcript_source_provenance": {
            "interview_source": "synthetic",
            "external_sources_used": False,
            "source_turn_id_convention": "synthetic local IDs",
            "source_turn_index": {
                "T01": "Synthetic episode one.",
                "T02": "Synthetic repeated series.",
                "T03": "Synthetic episode two.",
            },
        },
        "limitations": ["synthetic fixture"],
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
                "exact_text": "synthetic exact repair episode response",
            },
            {
                "response_id": "RR-002",
                "role": "participant",
                "exact_text": "synthetic exact series repair response",
            },
            {
                "response_id": "RR-003",
                "role": "participant",
                "exact_text": "synthetic current example",
            },
            {
                "response_id": "RR-005",
                "role": "participant",
                "exact_text": "yes",
                "meaning_in_context": "approved synthetic changes",
            },
        ],
        "recovered_transcript_turns": [
            {
                "recovered_turn_id": "RCV-001",
                "original_local_id": "T02",
                "role": "participant_original_elicitation",
                "exact_text": "synthetic exact repeated-series text",
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
                "approximate_age_life_phase": "~26",
                "memory_source": "direct participant report",
                "bounded_situation": "A synthetic repair situation.",
                "actions_in_temporal_order": ["Recognized an error.", "Apologized."],
                "outcome_when_known": "Outcome unknown.",
                "participant_stated_explanation": "Believed the action was wrong.",
                "source_reference": "RR-001",
                "support_implication": "Synthetic support.",
            },
            {
                "added_evidence_id": "ADD-EV-002",
                "target_pattern_id": "PAT-001",
                "evidence_type": "repeated_series_report",
                "collection_phase": "v8.1 post-interview/post-review repair",
                "bounded_period_context": "synthetic adolescence",
                "approximate_age_life_phase": "adolescence",
                "participant_recurrence_language": "sometimes",
                "rough_opportunity_count": None,
                "behavior_reportedly_recurred": "Repeated synthetic behavior.",
                "explicit_exceptions_or_limits": "Not common.",
                "memory_source_uncertainty": "direct but frequency uncertain",
                "source_reference": "RR-002",
                "support_implication": "Synthetic series support.",
            },
            {
                "added_evidence_id": "ADD-EV-003",
                "target_pattern_id": "PAT-001",
                "evidence_type": "current_behavioral_example",
                "collection_phase": "v8.1 post-interview/post-review repair",
                "approximate_age_life_phase": "current/adult",
                "situation": "Synthetic current behavior.",
                "participant_judgment": "Seems valid.",
                "reported_behavior": "Follows it.",
                "recurrence_or_frequency": "not quantified",
                "source_reference": "RR-003",
                "support_implication": "Synthetic auxiliary support.",
            },
        ],
        "review_record": {
            "review_id": "REVIEW-001",
            "material_shown": ["synthetic changes"],
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
        "limitations": ["synthetic fixture"],
    }


def _build() -> DevelopmentTransferCorpusArtifact:
    return build_v8_v8_1_development_corpus(
        _original(),
        _supplement(),
        participant_theory_exposure="prior_exposure_possible",
        created_at_utc=NOW,
    )


def test_builds_content_addressed_development_only_corpus() -> None:
    artifact = _build()
    assert artifact.corpus_id.startswith("LPDC-")
    assert len(artifact.corpus_sha256) == 64
    assert development_transfer_corpus_integrity_errors(artifact) == ()
    assert artifact.payload.source_transcript_completeness == "partial_exact_segments_only"
    assert artifact.payload.canonical_behavioral_freeze_eligible is False
    assert artifact.payload.development_coding_eligible is True
    assert artifact.payload.validation_use_forbidden is True
    assert artifact.payload.participant_theory_exposure == "prior_exposure_possible"


def test_keeps_original_and_post_review_concrete_episodes_distinct() -> None:
    artifact = _build()
    assert [row.episode_id for row in artifact.payload.episodes] == [
        "EP-001",
        "EP-002",
        "ADD-EV-001",
    ]
    original = artifact.payload.episodes[0]
    repair = artifact.payload.episodes[-1]
    assert original.collection_phase == "v8_original"
    assert original.source_review_scope == "pattern_reviewed_transfer_summary"
    assert original.transfer_summary_is_not_primary_source is True
    assert repair.collection_phase == "v8.1_repair"
    assert repair.source_review_scope == "post_review_participant_approved"
    assert repair.exact_source_segments[0].exact_text == "synthetic exact repair episode response"


def test_series_reports_are_preserved_separately_not_promoted_to_episodes() -> None:
    artifact = _build()
    assert [row.series_id for row in artifact.payload.series_reports] == ["SER-001", "ADD-EV-002"]
    assert all(row.primary_episode_code_from_series_forbidden for row in artifact.payload.series_reports)
    assert artifact.payload.series_reports[0].source_completeness == "partial_exact_recovered_turns"
    assert artifact.payload.series_reports[0].exact_source_segments[0].exact_text == (
        "synthetic exact repeated-series text"
    )
    assert artifact.payload.series_reports[1].exact_source_segments[0].exact_text == (
        "synthetic exact series repair response"
    )


def test_non_episode_post_review_evidence_remains_auxiliary() -> None:
    artifact = _build()
    auxiliary = artifact.payload.auxiliary_post_review_evidence
    assert {row.evidence_id for row in auxiliary} == {"ADD-EV-002", "ADD-EV-003"}
    current = next(row for row in auxiliary if row.evidence_id == "ADD-EV-003")
    assert current.evidence_type == "current_behavioral_example"
    assert current.primary_episode_code_from_auxiliary_evidence_forbidden is True


def test_episode_tasks_bind_exact_corpus_and_keep_source_warning() -> None:
    artifact = _build()
    tasks = build_development_episode_tasks(
        artifact,
        observable_ids=("NBM-R01", "NBM-R02"),
    )
    assert len(tasks) == 3
    assert all(task.corpus_id == artifact.corpus_id for task in tasks)
    assert all(task.corpus_sha256 == artifact.corpus_sha256 for task in tasks)
    assert all(task.development_only and task.validation_use_forbidden for task in tasks)
    assert all(task.transfer_summary_is_not_primary_source for task in tasks)
    assert all(task.observable_ids == ("NBM-R01", "NBM-R02") for task in tasks)
    assert tasks[0].exact_source_segments[0].exact_text == "synthetic exact participant fragment one"


def test_task_manifest_counts_episode_observable_units_and_series_separately() -> None:
    artifact = _build()
    tasks = build_development_episode_tasks(
        artifact,
        observable_ids=("NBM-R01", "NBM-R02", "NBM-R03"),
    )
    manifest = build_development_task_manifest(artifact, tasks=tasks, created_at_utc=NOW)
    assert manifest.payload.episode_task_count == 3
    assert manifest.payload.observable_count == 3
    assert manifest.payload.expected_episode_observable_unit_count == 9
    assert manifest.payload.series_report_count == 2
    assert manifest.payload.series_reports_are_not_pseudo_episodes is True
    assert manifest.payload.canonical_freeze_required_before_validation is True


def test_source_fragment_is_required_for_every_original_development_episode() -> None:
    original = _original()
    episodes = original["episodes"]
    assert isinstance(episodes, list)
    assert isinstance(episodes[0], dict)
    episodes[0]["exact_participant_source_segments"] = []
    with pytest.raises(ValueError, match="lacks exact participant source fragments"):
        build_v8_v8_1_development_corpus(
            original,
            _supplement(),
            participant_theory_exposure="prior_exposure_possible",
            created_at_utc=NOW,
        )


def test_invalid_post_review_source_reference_fails_closed() -> None:
    supplement = _supplement()
    additions = supplement["post_review_added_evidence"]
    assert isinstance(additions, list)
    assert isinstance(additions[0], dict)
    additions[0]["source_reference"] = "RR-MISSING"
    with pytest.raises(ValueError, match="source reference does not resolve"):
        build_v8_v8_1_development_corpus(
            _original(),
            supplement,
            participant_theory_exposure="prior_exposure_possible",
            created_at_utc=NOW,
        )


def test_invalid_review_approval_fails_closed() -> None:
    supplement = _supplement()
    responses = supplement["repair_responses"]
    assert isinstance(responses, list)
    assert isinstance(responses[-1], dict)
    responses[-1]["exact_text"] = "no"
    with pytest.raises(ValueError, match="affirmative participant approval"):
        build_v8_v8_1_development_corpus(
            _original(),
            supplement,
            participant_theory_exposure="prior_exposure_possible",
            created_at_utc=NOW,
        )


def test_duplicate_observable_ids_fail_task_build() -> None:
    with pytest.raises(ValueError, match="nonempty and unique"):
        build_development_episode_tasks(
            _build(),
            observable_ids=("NBM-R01", "NBM-R01"),
        )


def test_payload_cannot_validate_as_validation_eligible_state() -> None:
    artifact = _build()
    invalid = artifact.payload.model_dump(mode="python")
    invalid["canonical_behavioral_freeze_eligible"] = True
    with pytest.raises(ValidationError):
        type(artifact.payload).model_validate(invalid)
