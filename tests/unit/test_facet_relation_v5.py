import pytest

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
    observable_response_v5_errors,
)

CONTRACT = {
    "schema_version": V5_CONTRACT_SCHEMA_VERSION,
    "hybrid_value_components": {"R05-O2": {"affirmative": "x", "absence": "y"}},
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
        "NBM-R05": {
            "facets": {
                "alternative_search_disposition": {
                    "cardinality": "zero_or_one",
                    "cardinality_scope": {"scope_type": "event_stage"},
                    "value_ids": ["R05-O2"],
                },
                "choice_resolution": {
                    "cardinality": "zero_one_or_multiple",
                    "cardinality_scope": {"scope_type": "event_stage"},
                    "value_ids": ["R05-R4"],
                },
            }
        }
    },
}


def valid_r05_response() -> ObservableResponseV5:
    return ObservableResponseV5(
        response_id="resp-1",
        observable_id="NBM-R05",
        response_scope_id="EP-1",
        state="observed",
        facet_groups=(
            FacetGroupV5(
                facet_group_id="fg-search",
                facet_id="alternative_search_disposition",
                state="observed",
                cardinality="zero_or_one",
                cardinality_scope=EventStageScope(event_stage_id="stage-1"),
                allowed_value_ids=("R05-O2",),
                assertion_ids=("assert-o2",),
            ),
            FacetGroupV5(
                facet_group_id="fg-resolution",
                facet_id="choice_resolution",
                state="observed",
                cardinality="zero_one_or_multiple",
                cardinality_scope=EventStageScope(event_stage_id="stage-1"),
                allowed_value_ids=("R05-R4",),
                assertion_ids=("assert-r4",),
            ),
        ),
        value_assertions=(
            ValueAssertionV5(
                assertion_id="assert-o2",
                value_id="R05-O2",
                facet_id="alternative_search_disposition",
                facet_group_id="fg-search",
                event_stage_id="stage-1",
                evidence_unit_id="eu-1",
                component_assertion_ids=("comp-accept", "comp-no-search"),
                source_provenance_ids=("prov-1",),
                specificity_disposition="cross_facet_copresence",
            ),
            ValueAssertionV5(
                assertion_id="assert-r4",
                value_id="R05-R4",
                facet_id="choice_resolution",
                facet_group_id="fg-resolution",
                event_stage_id="stage-1",
                evidence_unit_id="eu-1",
                component_assertion_ids=(),
                source_provenance_ids=("prov-1",),
            ),
        ),
        component_assertions=(
            ComponentAssertionV5(
                component_assertion_id="comp-accept",
                parent_value_id="R05-O2",
                facet_id="alternative_search_disposition",
                facet_group_id="fg-search",
                event_stage_id="stage-1",
                evidence_unit_id="eu-1",
                component_role="affirmative",
                state="observed",
                proposition="accepted the designated default",
                source_provenance_ids=("prov-1",),
                absence_condition_id=None,
            ),
            ComponentAssertionV5(
                component_assertion_id="comp-no-search",
                parent_value_id="R05-O2",
                facet_id="alternative_search_disposition",
                facet_group_id="fg-search",
                event_stage_id="stage-1",
                evidence_unit_id="eu-1",
                component_role="absence",
                state="observed",
                proposition="no additional alternative search",
                source_provenance_ids=("prov-1",),
                absence_condition_id="absence-1",
            ),
        ),
        absence_conditions=(
            AbsenceConditionV5(
                absence_condition_id="absence-1",
                qualified_assertion_id="assert-o2",
                qualified_component_id="comp-no-search",
                absent_actor="narrator",
                absent_proposition_id="absence_of_additional_alternative_search",
                absent_proposition="no additional alternative search",
                window_id="window-1",
                awareness="established",
                opportunity="established",
                feasibility="established",
                established_nonoccurrence="established",
                source_provenance_ids=("prov-1",),
            ),
        ),
        source_provenance_records=(
            SourceProvenanceV5(
                source_provenance_id="prov-1",
                source_record_id="SEG-1",
                locator="exact source segment",
                exact_text_available=True,
            ),
        ),
        measurement_windows=(
            MeasurementWindowV5(
                window_id="window-1",
                window_kind="preselection_search_opportunity",
                event_stage_ids=("stage-1",),
                source_provenance_ids=("prov-1",),
            ),
        ),
        event_stages=(
            EventStageV5(
                event_stage_id="stage-1",
                state="observed",
                evidence_unit_id="eu-1",
                assertion_ids=("assert-o2", "assert-r4"),
                component_assertion_ids=("comp-accept", "comp-no-search"),
                source_provenance_ids=("prov-1",),
            ),
        ),
        temporal_edges=(),
        evidence_units=(
            EvidenceUnitV5(
                evidence_unit_id="eu-1",
                response_scope_id="EP-1",
                event_stage_ids=("stage-1",),
                independence_class="single_bounded_behavioral_occurrence",
            ),
        ),
    )


def test_valid_hybrid_and_cross_facet_copresence_share_one_evidence_unit() -> None:
    response = valid_r05_response()
    assert observable_response_v5_errors(
        response,
        contract=CONTRACT,
        valid_source_record_ids={"SEG-1"},
    ) == ()


def test_dangling_stage_reference_fails_closed() -> None:
    response = valid_r05_response()
    changed = response.value_assertions[0].model_copy(update={"event_stage_id": "missing-stage"})
    response = response.model_copy(
        update={"value_assertions": (changed, response.value_assertions[1])}
    )
    errors = observable_response_v5_errors(response, contract=CONTRACT)
    assert any("unknown id missing-stage" in error for error in errors)


def test_component_cannot_move_to_different_evidence_unit_than_stage() -> None:
    response = valid_r05_response()
    changed = response.component_assertions[0].model_copy(
        update={"evidence_unit_id": "other-unit"}
    )
    response = response.model_copy(
        update={"component_assertions": (changed, response.component_assertions[1])}
    )
    errors = observable_response_v5_errors(response, contract=CONTRACT)
    assert any("unknown id other-unit" in error for error in errors)
    assert any("evidence unit disagrees with event stage" in error for error in errors)


def test_observed_absence_component_requires_all_four_gate_elements() -> None:
    response = valid_r05_response()
    changed = response.absence_conditions[0].model_copy(update={"feasibility": "unclear"})
    response = response.model_copy(update={"absence_conditions": (changed,)})
    errors = observable_response_v5_errors(response, contract=CONTRACT)
    assert any("lacks a fully established gate" in error for error in errors)


def test_task_provenance_must_come_from_supplied_source() -> None:
    response = valid_r05_response()
    errors = observable_response_v5_errors(
        response,
        contract=CONTRACT,
        valid_source_record_ids={"SOME-OTHER-SEGMENT"},
    )
    assert any("cites source outside supplied task" in error for error in errors)


def test_observed_facet_group_cannot_be_empty() -> None:
    with pytest.raises(ValueError, match="observed facet group requires"):
        FacetGroupV5(
            facet_group_id="fg",
            facet_id="choice_resolution",
            state="observed",
            cardinality="zero_or_one",
            cardinality_scope=EventStageScope(event_stage_id="stage"),
            allowed_value_ids=("R05-R4",),
            assertion_ids=(),
        )
