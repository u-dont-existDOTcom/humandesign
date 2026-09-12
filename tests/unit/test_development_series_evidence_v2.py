from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.development_series_evidence import build_development_series_tasks
from hdmatch.evaluation.development_series_evidence_v2 import (
    DevelopmentSeriesAnnotationResponseV2,
    development_series_response_errors_v2,
    series_supports_opportunity_level_frequency_inference_v2,
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
    ObservableProcedureExtensionV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_coding_procedure_v2,
)
from hdmatch.experiments.canonical import sha256_json

NOW = datetime(2026, 9, 8, 18, 0, tzinfo=UTC)
ZERO = "0" * 64


def _source(segment_id: str, text: str) -> DevelopmentSourceSegment:
    return DevelopmentSourceSegment(
        segment_id=segment_id,
        exact_text=text,
        provenance_refs=("T01",),
    )


def _task():
    episode = DevelopmentTransferEpisode(
        episode_id="EP-001",
        origin_id="EP-001",
        collection_phase="v8_original",
        approximate_age_life_phase="adult",
        source_review_scope="pattern_reviewed_transfer_summary",
        source_completeness="partial_exact_segments_plus_transfer_summary",
        bounded_situation="Synthetic opportunity.",
        actions_in_temporal_order=("Accepted.",),
        exact_source_segments=(_source("EP-001-SEG-01", "I accepted once."),),
        transfer_summary="Synthetic.",
    )
    series = DevelopmentTransferSeriesReport(
        series_id="SER-001",
        origin_id="SER-001",
        collection_phase="v8_original",
        bounded_period_context="Repeated invitations.",
        approximate_age_life_phase="adult",
        recurrence_language="always",
        behavior_reportedly_recurred="Accepted invitations.",
        exact_source_segments=(
            _source(
                "SER-001-SEG-01",
                "Whenever that happened I always accepted; I cannot remember an exception.",
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
    digest = sha256_json(payload)
    corpus = DevelopmentTransferCorpusArtifact(
        corpus_id=f"LPDC-{digest[:20].upper()}",
        corpus_sha256=digest,
        payload=payload,
    )
    return build_development_series_tasks(corpus, observable_ids=("NBM-R01",)).tasks[0]


def _ontology() -> OntologyReleaseArtifact:
    observable = ObservableDefinition(
        observable_id="NBM-R01",
        label="Synthetic optional response",
        definition="Synthetic development observable.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("R01-a", "OS"),
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
        ontology_id="synthetic-series-v2-test",
        ontology_version="v1.0",
        release_status="development",
        scope_statement="Synthetic series v2 test ontology.",
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
                non_action_values=(),
                other_specified_value="OS",
            ),
        ),
        created_at_utc=NOW,
    )
    return build_structured_coding_procedure_v2(payload, ontology)


def _base(**overrides):
    task = _task()
    values = dict(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        series_id=task.series_id,
        observable_id="NBM-R01",
        state="observed",
        coded_values=("R01-a",),
        value_relation="single",
        reported_recurrence_strength="universal_language",
        exception_status="exceptions_not_probed_or_unknown",
        exception_frequency="unknown",
        frequency_evidence_basis="generalized_self_report",
        supporting_source_segment_ids=("SER-001-SEG-01",),
        theory_exposure="prior_exposure_possible",
    )
    values.update(overrides)
    return task, values


def test_generalized_recurrence_is_observed_without_fake_occurrence_floor() -> None:
    task, values = _base()
    response = DevelopmentSeriesAnnotationResponseV2(**values)
    assert response.minimum_reported_occurrences is None
    assert response.reported_recurrence_strength == "universal_language"
    assert response.confirming_episode_counted_as_independent_frequency_evidence is False
    ontology = _ontology()
    assert development_series_response_errors_v2(
        response,
        task=task,
        ontology=ontology,
        procedure=_procedure(ontology),
    ) == ()


def test_always_does_not_imply_exceptions_were_explicitly_denied() -> None:
    _, values = _base()
    response = DevelopmentSeriesAnnotationResponseV2(**values)
    assert response.exception_status == "exceptions_not_probed_or_unknown"
    assert response.exception_frequency == "unknown"


def test_minimum_occurrence_count_cannot_be_invented_for_generalized_self_report() -> None:
    _, values = _base(minimum_reported_occurrences=2)
    with pytest.raises(ValidationError, match="bounded/sampled/external/mixed"):
        DevelopmentSeriesAnnotationResponseV2(**values)


def test_explicit_denial_of_exceptions_requires_none_reported_frequency() -> None:
    _, values = _base(
        exception_status="exceptions_explicitly_denied",
        exception_frequency="sometimes",
    )
    with pytest.raises(ValidationError, match="none_reported"):
        DevelopmentSeriesAnnotationResponseV2(**values)


def test_bounded_rate_or_count_needs_bounded_evidence() -> None:
    _, values = _base(
        reported_recurrence_strength="bounded_rate_or_count",
        frequency_evidence_basis="bounded_rate_or_count_self_report",
        minimum_reported_occurrences=3,
        bounded_rate_or_count_description="at least three relevant opportunities",
    )
    response = DevelopmentSeriesAnnotationResponseV2(**values)
    assert response.minimum_reported_occurrences == 3


def test_opportunity_level_frequency_inference_requires_sampling_or_external_basis() -> None:
    _, generalized = _base()
    generalized_response = DevelopmentSeriesAnnotationResponseV2(**generalized)
    assert series_supports_opportunity_level_frequency_inference_v2(generalized_response) is False

    _, sampled = _base(
        reported_recurrence_strength="bounded_rate_or_count",
        frequency_evidence_basis="sampled_opportunities",
        minimum_reported_occurrences=4,
        bounded_rate_or_count_description="four sampled opportunities",
    )
    sampled_response = DevelopmentSeriesAnnotationResponseV2(**sampled)
    assert series_supports_opportunity_level_frequency_inference_v2(sampled_response) is True


def test_v2_source_citations_still_fail_closed() -> None:
    task, values = _base(supporting_source_segment_ids=("NOT-IN-TASK",))
    response = DevelopmentSeriesAnnotationResponseV2(**values)
    ontology = _ontology()
    errors = development_series_response_errors_v2(
        response,
        task=task,
        ontology=ontology,
        procedure=_procedure(ontology),
    )
    assert "series v2 response cites supporting source outside supplied task" in errors
