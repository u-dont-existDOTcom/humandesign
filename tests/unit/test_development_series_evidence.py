from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.development_series_evidence import (
    DevelopmentSeriesAnnotationResponse,
    build_development_series_manifest,
    build_development_series_tasks,
    development_series_response_errors,
    series_supports_additional_occurrence_for_anchor,
    series_supports_stronger_repeated_condition,
)
from hdmatch.evaluation.development_transfer_corpus import (
    DevelopmentSourceSegment,
    DevelopmentTransferCorpusArtifact,
    DevelopmentTransferCorpusPayload,
    DevelopmentTransferEpisode,
    DevelopmentTransferSeriesReport,
)
from hdmatch.evaluation.neutral_measurement import (
    ObservableDefinition,
    OntologyReleaseArtifact,
    OntologyReleasePayload,
)
from hdmatch.evaluation.structured_annotation_v2 import (
    NonActionGateAssessmentV2,
    ObservableProcedureExtensionV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_coding_procedure_v2,
)
from hdmatch.experiments.canonical import sha256_json


NOW = datetime(2026, 9, 6, 20, 0, tzinfo=UTC)
ZERO = "0" * 64


def _source(segment_id: str, text: str) -> DevelopmentSourceSegment:
    return DevelopmentSourceSegment(
        segment_id=segment_id,
        exact_text=text,
        provenance_refs=("T01",),
    )


def _corpus() -> DevelopmentTransferCorpusArtifact:
    episode = DevelopmentTransferEpisode(
        episode_id="EP-001",
        origin_id="EP-001",
        collection_phase="v8_original",
        domain_id="P01",
        approximate_age_life_phase="adult",
        source_review_scope="pattern_reviewed_transfer_summary",
        source_completeness="partial_exact_segments_plus_transfer_summary",
        bounded_situation="Synthetic detailed opportunity.",
        actions_in_temporal_order=("Accepted.",),
        exact_source_segments=(_source("EP-001-SEG-01", "I accepted the invitation."),),
        transfer_summary="Situation: synthetic\nActions in order: Accepted.",
    )
    exact_series = DevelopmentTransferSeriesReport(
        series_id="SER-EXACT",
        origin_id="SER-EXACT",
        collection_phase="v8_original",
        domain_id="P01",
        bounded_period_context="Repeated adult invitations.",
        approximate_age_life_phase="adult",
        recurrence_language="many times",
        rough_opportunity_count="at least 3",
        behavior_reportedly_recurred="Accepted invitations.",
        exact_source_segments=(
            _source("SER-EXACT-SEG-01", "that happened lots of times; i usually accepted"),
        ),
        source_completeness="partial_exact_recovered_turns",
    )
    summary_only_series = DevelopmentTransferSeriesReport(
        series_id="SER-SUMMARY",
        origin_id="SER-SUMMARY",
        collection_phase="v8_original",
        domain_id="P01",
        bounded_period_context="Repeated childhood invitations.",
        approximate_age_life_phase="childhood",
        recurrence_language="often",
        behavior_reportedly_recurred="Accepted invitations.",
        source_completeness="transfer_summary_only",
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
        series_reports=(exact_series, summary_only_series),
        pattern_claims=(),
        auxiliary_post_review_evidence=(),
        created_at_utc=NOW,
    )
    digest = sha256_json(payload)
    return DevelopmentTransferCorpusArtifact(
        corpus_id=f"LPDC-{digest[:20].upper()}",
        corpus_sha256=digest,
        payload=payload,
    )


def _ontology() -> OntologyReleaseArtifact:
    observable = ObservableDefinition(
        observable_id="NBM-R01",
        label="Synthetic optional response",
        definition="Synthetic development observable.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("R01-a", "R01-h", "OS"),
        insufficient_semantics="Missing required information.",
        not_applicable_semantics="Prerequisite absent.",
        inclusion_criteria=("Synthetic prerequisite.",),
        exclusion_criteria=("Synthetic exclusion.",),
        evidence_requirements=("Synthetic evidence requirement.",),
        participant_review_policy="Synthetic participant review.",
        theory_contamination_policy="No target-model information.",
        origin_status="synthetic_placeholder",
        release_notes="Synthetic test only.",
    )
    payload = OntologyReleasePayload(
        ontology_id="synthetic-series-test",
        ontology_version="v1.0",
        release_status="development",
        scope_statement="Synthetic series test ontology.",
        observables=(observable,),
        coding_procedure_id="synthetic-procedure",
        coding_procedure_sha256=ZERO,
        aggregation_policy_id="synthetic-aggregation",
        aggregation_policy_sha256=ZERO,
        theory_contamination_policy_id="synthetic-theory-policy",
        theory_contamination_policy_sha256=ZERO,
        source_commit="abcdef0",
        released_at_utc=NOW,
        synthetic_fixture_only=True,
    )
    digest = sha256_json(payload)
    return OntologyReleaseArtifact(
        artifact_id=f"LPO-{digest[:20].upper()}",
        ontology_sha256=digest,
        payload=payload,
    )


def _procedure(ontology: OntologyReleaseArtifact):
    payload = StructuredCodingProcedurePayloadV2(
        ontology_artifact_id=ontology.artifact_id,
        ontology_sha256=ontology.ontology_sha256,
        reconciled_codebook_sha256="3" * 64,
        coding_manual_sha256="4" * 64,
        observable_extensions=(
            ObservableProcedureExtensionV2(
                observable_id="NBM-R01",
                non_action_values=("R01-h",),
                other_specified_value="OS",
            ),
        ),
        created_at_utc=NOW,
    )
    return build_structured_coding_procedure_v2(payload, ontology)


def test_only_exact_source_series_become_coding_tasks() -> None:
    report = build_development_series_tasks(_corpus(), observable_ids=("NBM-R01",))
    assert report.eligible_series_count == 1
    assert report.blocked_series_count == 1
    assert [task.series_id for task in report.tasks] == ["SER-EXACT"]
    assert report.blocked_summary_only_series_ids == ("SER-SUMMARY",)
    task = report.tasks[0]
    assert task.exact_source_segments[0].exact_text == (
        "that happened lots of times; i usually accepted"
    )
    assert task.summary_fields_are_secondary_to_exact_source_text is True
    assert task.validation_use_forbidden is True


def test_series_manifest_counts_units_without_counting_series_as_episodes() -> None:
    report = build_development_series_tasks(
        _corpus(),
        observable_ids=("NBM-R01", "NBM-R02", "NBM-R03"),
    )
    manifest = build_development_series_manifest(report, created_at_utc=NOW)
    assert manifest.payload.task_count == 1
    assert manifest.payload.expected_series_observable_unit_count == 3
    assert manifest.payload.series_reports_are_not_episode_counts is True
    assert manifest.payload.blocked_summary_only_series_ids == ("SER-SUMMARY",)


def test_observed_series_requires_plural_floor_and_exact_source_citation() -> None:
    task = build_development_series_tasks(_corpus(), observable_ids=("NBM-R01",)).tasks[0]
    with pytest.raises(ValidationError, match="reported recurrence floor"):
        DevelopmentSeriesAnnotationResponse(
            task_id=task.task_id,
            corpus_id=task.corpus_id,
            corpus_sha256=task.corpus_sha256,
            series_id=task.series_id,
            observable_id="NBM-R01",
            state="observed",
            coded_values=("R01-a",),
            value_relation="single",
            supporting_source_segment_ids=("SER-EXACT-SEG-01",),
        )


def test_response_validation_rejects_source_outside_task() -> None:
    corpus = _corpus()
    task = build_development_series_tasks(corpus, observable_ids=("NBM-R01",)).tasks[0]
    ontology = _ontology()
    procedure = _procedure(ontology)
    response = DevelopmentSeriesAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-a",),
        value_relation="single",
        minimum_reported_occurrences=3,
        supporting_source_segment_ids=("NOT-IN-TASK",),
        theory_exposure="prior_exposure_possible",
    )
    errors = development_series_response_errors(
        response,
        task=task,
        ontology=ontology,
        procedure=procedure,
    )
    assert "series response cites source segments outside supplied task" in errors


def test_response_validation_binds_non_action_to_frozen_registry_and_gate() -> None:
    corpus = _corpus()
    task = build_development_series_tasks(corpus, observable_ids=("NBM-R01",)).tasks[0]
    ontology = _ontology()
    procedure = _procedure(ontology)
    gate = NonActionGateAssessmentV2(
        awareness="established",
        opportunity="established",
        feasibility="established",
        established_non_action="established",
    )
    response = DevelopmentSeriesAnnotationResponse(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-h",),
        value_relation="single",
        minimum_reported_occurrences=3,
        asserts_non_action=True,
        non_action_gate=gate,
        supporting_source_segment_ids=("SER-EXACT-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )
    assert development_series_response_errors(
        response,
        task=task,
        ontology=ontology,
        procedure=procedure,
    ) == ()


def test_series_can_support_episode_plus_series_recurrence_only_with_explicit_anchor_relation() -> None:
    task = build_development_series_tasks(_corpus(), observable_ids=("NBM-R01",)).tasks[0]
    base = dict(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-a",),
        value_relation="single",
        minimum_reported_occurrences=2,
        supporting_source_segment_ids=("SER-EXACT-SEG-01",),
        anchor_episode_id="EP-001",
        theory_exposure="prior_exposure_possible",
    )
    unknown = DevelopmentSeriesAnnotationResponse(
        **base,
        anchor_relation="anchor_relation_unknown",
    )
    assert not series_supports_additional_occurrence_for_anchor(
        unknown,
        anchor_episode_id="EP-001",
        substantive_value="R01-a",
    )

    includes = DevelopmentSeriesAnnotationResponse(
        **base,
        anchor_relation="includes_anchor_episode",
    )
    assert series_supports_additional_occurrence_for_anchor(
        includes,
        anchor_episode_id="EP-001",
        substantive_value="R01-a",
    )
    assert not series_supports_additional_occurrence_for_anchor(
        includes,
        anchor_episode_id="EP-OTHER",
        substantive_value="R01-a",
    )


def test_stronger_repeated_condition_requires_at_least_three_reported_occurrences() -> None:
    task = build_development_series_tasks(_corpus(), observable_ids=("NBM-R01",)).tasks[0]
    base = dict(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-a",),
        value_relation="single",
        supporting_source_segment_ids=("SER-EXACT-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )
    two = DevelopmentSeriesAnnotationResponse(**base, minimum_reported_occurrences=2)
    three = DevelopmentSeriesAnnotationResponse(**base, minimum_reported_occurrences=3)
    assert series_supports_stronger_repeated_condition(two) is False
    assert series_supports_stronger_repeated_condition(three) is True
