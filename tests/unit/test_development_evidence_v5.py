from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.development_evidence_v5 import (
    DevelopmentEpisodeAnnotationResponseV5,
    DevelopmentSeriesAnnotationResponseV5,
    development_episode_response_errors_v5,
    development_series_response_errors_v5,
    series_supports_opportunity_level_frequency_inference_v5,
)
from hdmatch.evaluation.development_series_evidence import DevelopmentSeriesCodingTask
from hdmatch.evaluation.development_transfer_corpus import (
    DevelopmentEpisodeCodingTask,
    DevelopmentSourceSegment,
)
from hdmatch.evaluation.facet_relation_v5 import (
    AbsenceConditionV5,
    ComponentAssertionV5,
    EventStageScope,
    EventStageV5,
    EvidenceUnitV5,
    FacetGroupV5,
    MeasurementWindowV5,
    ObservableResponseV5,
    SourceProvenanceV5,
    ValueAssertionV5,
    V5_CONTRACT_SCHEMA_VERSION,
)
from hdmatch.evaluation.neutral_measurement import (
    ObservableDefinition,
    OntologyReleaseArtifact,
    OntologyReleasePayload,
)
from hdmatch.experiments.canonical import sha256_json

NOW = datetime(2026, 9, 11, 16, 0, tzinfo=UTC)
ZERO = "0" * 64
CONTRACT: dict[str, object] = {
    "schema_version": V5_CONTRACT_SCHEMA_VERSION,
    "hybrid_value_components": {},
    "default_observable_profile": {
        "facets": {
            "substantive_response": {
                "cardinality": "zero_one_or_multiple",
                "cardinality_scope": {"scope_type": "event_stage"},
                "value_ids_source": "bound codebook",
            }
        }
    },
    "observable_facet_profiles": {
        "NBM-R14": {
            "facets": {
                "error_response_sequence": {
                    "cardinality": "zero_one_or_multiple",
                    "cardinality_scope": {"scope_type": "event_stage"},
                    "value_ids": ["R14-a", "R14-i"],
                }
            }
        }
    },
}


def _source(segment_id: str) -> DevelopmentSourceSegment:
    return DevelopmentSourceSegment(
        segment_id=segment_id,
        exact_text="Synthetic exact participant text.",
        provenance_refs=("T01",),
    )


def _episode_task() -> DevelopmentEpisodeCodingTask:
    return DevelopmentEpisodeCodingTask(
        task_id="LPDT-00000000000000000001",
        corpus_id="LPDC-00000000000000000001",
        corpus_sha256="1" * 64,
        episode_id="EP-001",
        approximate_age_life_phase="adult",
        episode_narrative="Synthetic transfer summary.",
        exact_source_segments=(_source("EP-001-SEG-01"),),
        source_completeness="partial_exact_segments_plus_transfer_summary",
        observable_ids=("NBM-R14",),
        participant_theory_exposure="prior_exposure_possible",
    )


def _series_task() -> DevelopmentSeriesCodingTask:
    return DevelopmentSeriesCodingTask(
        task_id="LPST-00000000000000000001",
        corpus_id="LPDC-00000000000000000001",
        corpus_sha256="1" * 64,
        series_id="SER-001",
        bounded_period_context="Synthetic repeated opportunities.",
        approximate_age_life_phase="adult",
        recurrence_language="usually",
        behavior_reportedly_recurred="Synthetic verification behavior.",
        exact_source_segments=(_source("SER-001-SEG-01"),),
        observable_ids=("NBM-R14",),
        participant_theory_exposure="prior_exposure_possible",
    )


def _ontology() -> OntologyReleaseArtifact:
    observable = ObservableDefinition(
        observable_id="NBM-R14",
        label="Synthetic error response",
        definition="Synthetic development observable.",
        unit_of_analysis="episode",
        value_type="nominal",
        allowed_values=("R14-a", "R14-i", "OS"),
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
        ontology_id="synthetic-v5-development-test",
        ontology_version="v1.0",
        release_status="development",
        scope_statement="Synthetic V5 development response test ontology.",
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


def _direct_graph(scope_id: str, source_id: str) -> ObservableResponseV5:
    return ObservableResponseV5(
        response_id=f"resp-{scope_id}",
        observable_id="NBM-R14",
        response_scope_id=scope_id,
        state="observed",
        facet_groups=(
            FacetGroupV5(
                facet_group_id="fg-r14",
                facet_id="error_response_sequence",
                state="observed",
                cardinality="zero_one_or_multiple",
                cardinality_scope=EventStageScope(event_stage_id="stage-r14"),
                allowed_value_ids=("R14-a", "R14-i"),
                assertion_ids=("assert-r14-a",),
            ),
        ),
        value_assertions=(
            ValueAssertionV5(
                assertion_id="assert-r14-a",
                value_id="R14-a",
                facet_id="error_response_sequence",
                facet_group_id="fg-r14",
                event_stage_id="stage-r14",
                evidence_unit_id="eu-r14",
                source_provenance_ids=("prov-r14",),
            ),
        ),
        source_provenance_records=(
            SourceProvenanceV5(
                source_provenance_id="prov-r14",
                source_record_id=source_id,
                locator="exact source segment",
                exact_text_available=True,
            ),
        ),
        event_stages=(
            EventStageV5(
                event_stage_id="stage-r14",
                state="observed",
                evidence_unit_id="eu-r14",
                assertion_ids=("assert-r14-a",),
                source_provenance_ids=("prov-r14",),
            ),
        ),
        evidence_units=(
            EvidenceUnitV5(
                evidence_unit_id="eu-r14",
                response_scope_id=scope_id,
                event_stage_ids=("stage-r14",),
                independence_class="single_bounded_behavioral_occurrence",
            ),
        ),
    )


def _pure_absence_graph(scope_id: str, source_id: str) -> ObservableResponseV5:
    return ObservableResponseV5(
        response_id=f"resp-absence-{scope_id}",
        observable_id="NBM-R14",
        response_scope_id=scope_id,
        state="observed",
        facet_groups=(
            FacetGroupV5(
                facet_group_id="fg-r14",
                facet_id="error_response_sequence",
                state="observed",
                cardinality="zero_one_or_multiple",
                cardinality_scope=EventStageScope(event_stage_id="stage-r14"),
                allowed_value_ids=("R14-a", "R14-i"),
                assertion_ids=("assert-r14-i",),
            ),
        ),
        value_assertions=(
            ValueAssertionV5(
                assertion_id="assert-r14-i",
                value_id="R14-i",
                facet_id="error_response_sequence",
                facet_group_id="fg-r14",
                event_stage_id="stage-r14",
                evidence_unit_id="eu-r14",
                component_assertion_ids=("comp-r14-i",),
                source_provenance_ids=("prov-r14",),
            ),
        ),
        component_assertions=(
            ComponentAssertionV5(
                component_assertion_id="comp-r14-i",
                parent_value_id="R14-i",
                facet_id="error_response_sequence",
                facet_group_id="fg-r14",
                event_stage_id="stage-r14",
                evidence_unit_id="eu-r14",
                component_role="absence",
                state="observed",
                proposition="no remedial response in the defined feasible window",
                source_provenance_ids=("prov-r14",),
                absence_condition_id="absence-r14",
            ),
        ),
        absence_conditions=(
            AbsenceConditionV5(
                absence_condition_id="absence-r14",
                qualified_assertion_id="assert-r14-i",
                qualified_component_id="comp-r14-i",
                absent_actor="narrator",
                absent_proposition_id="no_remedial_error_response_during_the_defined_feasible_window",
                absent_proposition="no remedial response in the defined feasible window",
                window_id="window-r14",
                awareness="established",
                opportunity="established",
                feasibility="established",
                established_nonoccurrence="established",
                source_provenance_ids=("prov-r14",),
            ),
        ),
        source_provenance_records=(
            SourceProvenanceV5(
                source_provenance_id="prov-r14",
                source_record_id=source_id,
                locator="exact source segment",
                exact_text_available=True,
            ),
        ),
        measurement_windows=(
            MeasurementWindowV5(
                window_id="window-r14",
                window_kind="remedial_response_window",
                event_stage_ids=("stage-r14",),
                source_provenance_ids=("prov-r14",),
            ),
        ),
        event_stages=(
            EventStageV5(
                event_stage_id="stage-r14",
                state="observed",
                evidence_unit_id="eu-r14",
                assertion_ids=("assert-r14-i",),
                component_assertion_ids=("comp-r14-i",),
                source_provenance_ids=("prov-r14",),
            ),
        ),
        evidence_units=(
            EvidenceUnitV5(
                evidence_unit_id="eu-r14",
                response_scope_id=scope_id,
                event_stage_ids=("stage-r14",),
                independence_class="single_bounded_behavioral_occurrence",
            ),
        ),
    )


def test_episode_v5_binds_task_source_ontology_and_contract() -> None:
    task = _episode_task()
    response = DevelopmentEpisodeAnnotationResponseV5(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R14",
        response_graph=_direct_graph(task.episode_id, "EP-001-SEG-01"),
    )
    assert development_episode_response_errors_v5(
        response,
        task=task,
        ontology=_ontology(),
        contract=CONTRACT,
    ) == ()
    assert response.accepted_contract_review_commit == "ce04642146c41a7d5d94f85360572c78de887682"
    assert response.validation_use_forbidden is True


def test_episode_v5_accepts_gated_pure_absence_graph() -> None:
    task = _episode_task()
    response = DevelopmentEpisodeAnnotationResponseV5(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R14",
        response_graph=_pure_absence_graph(task.episode_id, "EP-001-SEG-01"),
    )
    assert development_episode_response_errors_v5(
        response,
        task=task,
        ontology=_ontology(),
        contract=CONTRACT,
    ) == ()


def test_episode_v5_source_provenance_outside_task_fails_closed() -> None:
    task = _episode_task()
    response = DevelopmentEpisodeAnnotationResponseV5(
        task_id=task.task_id,
        corpus_id=task.corpus_id,
        corpus_sha256=task.corpus_sha256,
        episode_id=task.episode_id,
        observable_id="NBM-R14",
        response_graph=_direct_graph(task.episode_id, "NOT-IN-TASK"),
    )
    errors = development_episode_response_errors_v5(
        response,
        task=task,
        ontology=_ontology(),
        contract=CONTRACT,
    )
    assert any("cites source outside supplied task" in error for error in errors)


def _series_response(**overrides: object) -> DevelopmentSeriesAnnotationResponseV5:
    task = _series_task()
    values: dict[str, object] = {
        "task_id": task.task_id,
        "corpus_id": task.corpus_id,
        "corpus_sha256": task.corpus_sha256,
        "series_id": task.series_id,
        "observable_id": "NBM-R14",
        "response_graph": _direct_graph(task.series_id, "SER-001-SEG-01"),
        "reported_recurrence_strength": "usually",
        "exception_status": "exceptions_not_probed_or_unknown",
        "exception_frequency": "unknown",
        "frequency_evidence_basis": "generalized_self_report",
    }
    values.update(overrides)
    return DevelopmentSeriesAnnotationResponseV5.model_validate(values)


def test_series_v5_preserves_generalized_recurrence_without_fake_frequency() -> None:
    task = _series_task()
    response = _series_response()
    assert development_series_response_errors_v5(
        response,
        task=task,
        ontology=_ontology(),
        contract=CONTRACT,
    ) == ()
    assert response.minimum_reported_occurrences is None
    assert response.confirming_episode_counted_as_independent_frequency_evidence is False
    assert series_supports_opportunity_level_frequency_inference_v5(response) is False


def test_series_v5_frequency_inference_requires_sampled_or_external_basis() -> None:
    sampled = _series_response(
        reported_recurrence_strength="bounded_rate_or_count",
        frequency_evidence_basis="sampled_opportunities",
        minimum_reported_occurrences=4,
        bounded_rate_or_count_description="four sampled opportunities",
    )
    assert series_supports_opportunity_level_frequency_inference_v5(sampled) is True


def test_series_v5_nonobserved_graph_cannot_assert_recurrence_fields() -> None:
    empty_graph = ObservableResponseV5(
        response_id="resp-insufficient",
        observable_id="NBM-R14",
        response_scope_id="SER-001",
        state="insufficient",
    )
    with pytest.raises(ValidationError, match="cannot assert recurrence fields"):
        _series_response(response_graph=empty_graph)
