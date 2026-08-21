from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from hdmatch.model.mapping_library import load_mapping_library
from hdmatch.runtime.symbolic_adapter import FrozenSymbolicModel, candidate_prevalence
from hdmatch.schemas import Activation, CandidateState, ChartFeatures, LocalDateOverlap

ROOT = Path(__file__).resolve().parents[2]


def _chart(chart_type: str = "generator") -> ChartFeatures:
    return ChartFeatures(
        personality_utc=datetime(2000, 1, 1, tzinfo=UTC),
        design_utc=datetime(1999, 10, 1, tzinfo=UTC),
        type=chart_type,
        strategy="wait_to_respond",
        authority="sacral",
        profile="1/3",
        definition="single_definition",
        defined_centers=("sacral",),
        activations={
            "personality:sun": Activation(
                body="sun", side="personality", longitude=0.0, gate=41, line=1
            )
        },
    )


def _state(identifier: str, chart: ChartFeatures, hours: int) -> CandidateState:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    end = start + timedelta(hours=hours)
    return CandidateState(
        state_id=identifier,
        start_utc=start,
        end_utc=end,
        chart_features_hash="a" * 64,
        chart_features=chart,
        local_date_overlaps=(LocalDateOverlap(date=start.date(), seconds=hours * 3600),),
    )


def test_frozen_model_generates_only_declared_canonical_answers() -> None:
    model = FrozenSymbolicModel(ROOT / "mappings" / "mapping_library_v1.json")
    responses = model.oracle_responses(_chart())
    assert responses
    assert all(response.behavioral_confidence == 1.0 for response in responses)
    assert all(
        response.answer in model.answer_spaces()[response.question_id] for response in responses
    )


def test_candidate_prevalence_is_duration_weighted() -> None:
    library = load_mapping_library(ROOT / "mappings" / "mapping_library_v1.json")
    states = (_state("A", _chart("generator"), 6), _state("B", _chart("projector"), 18))
    prevalence = candidate_prevalence(states, library)
    generator_anchors = {
        mapping.anchor_id
        for mapping in library.frozen_mappings
        if mapping.chart_feature_predicate is not None
        and mapping.chart_feature_predicate.feature == "type"
        and mapping.chart_feature_predicate.matches(_chart("generator"))
    }
    assert generator_anchors
    assert all(prevalence[anchor] == 0.25 for anchor in generator_anchors)
