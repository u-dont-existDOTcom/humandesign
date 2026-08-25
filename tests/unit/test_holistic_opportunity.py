from __future__ import annotations

import pytest

from hdmatch.human.holistic import CandidateChart, PositiveEvidenceRecord
from hdmatch.human.holistic_opportunity import (
    OpportunityConditionedNeighborModel,
    cross_fitted_opportunity_identification,
    taxonomy_opportunity,
)


def _record(
    participant_id: str,
    labels: tuple[str, ...],
    *,
    f1: str,
    f2: str = "0",
    source: str = "S",
) -> PositiveEvidenceRecord:
    return PositiveEvidenceRecord(
        participant_id=participant_id,
        cohort="development",
        observed_labels=labels,
        chart_features={"f1": f1, "f2": f2},
        match_strata={"source": source, "year": "2000"},
    )


def _chart(
    chart_id: str,
    owner: str,
    *,
    f1: str,
    f2: str = "0",
    source: str = "S",
) -> CandidateChart:
    return CandidateChart(
        chart_id=chart_id,
        owner_participant_id=owner,
        chart_features={"f1": f1, "f2": f2},
        match_strata={"source": source, "year": "2000"},
    )


def test_taxonomy_opportunity_keeps_vocation_as_one_observation_branch() -> None:
    assert taxonomy_opportunity("Vocation : Entertainer : Actor") == "Vocation"
    assert taxonomy_opportunity("Family : Relationship : Marriage") == (
        "Family : Relationship"
    )
    assert taxonomy_opportunity("Traits : Personality : Active") == (
        "Traits : Personality"
    )


def test_unobserved_ontology_branch_cannot_change_label_neighborhood() -> None:
    target = "Traits : Personality : Active"
    other = "Traits : Personality : Reserved"
    base = (
        _record("p1", (target,), f1="x"),
        _record("p2", (target,), f1="x"),
        _record("p3", (other,), f1="y"),
        _record("p4", (other,), f1="y"),
    )
    unrelated = tuple(
        _record(f"v{i}", ("Vocation : Science",), f1="x" if i % 2 else "y")
        for i in range(20)
    )
    kwargs = dict(
        model_id="m",
        feature_names=("f1",),
        neighbor_count=2,
        min_label_count=1,
        min_opportunity_count=2,
    )
    model_base = OpportunityConditionedNeighborModel.fit(base, **kwargs)
    model_extra = OpportunityConditionedNeighborModel.fit(base + unrelated, **kwargs)
    person = _record("held", (target,), f1="x")
    candidate = _chart("cx", "held", f1="x")
    assert model_base.score_candidate(person, candidate) == pytest.approx(
        model_extra.score_candidate(person, candidate)
    )


def test_source_blocking_removes_other_source_from_training_baseline() -> None:
    target = "Traits : Personality : Active"
    other = "Traits : Personality : Reserved"
    source_a = (
        _record("a1", (target,), f1="x", source="A"),
        _record("a2", (target,), f1="x", source="A"),
        _record("a3", (other,), f1="y", source="A"),
        _record("a4", (other,), f1="y", source="A"),
    )
    source_b = (
        _record("b1", (target,), f1="y", source="B"),
        _record("b2", (target,), f1="y", source="B"),
        _record("b3", (other,), f1="x", source="B"),
        _record("b4", (other,), f1="x", source="B"),
    )
    model = OpportunityConditionedNeighborModel.fit(
        source_a + source_b,
        model_id="blocked",
        feature_names=("f1",),
        training_block_fields=("source",),
        neighbor_count=2,
        min_label_count=1,
        min_opportunity_count=2,
    )
    person = _record("held", (target,), f1="x", source="A")
    score_x = model.score_candidate(person, _chart("x", "held", f1="x", source="A"))
    score_y = model.score_candidate(person, _chart("y", "held", f1="y", source="A"))
    assert score_x is not None and score_y is not None
    assert score_x > score_y


def test_whole_chart_neighborhood_recovers_conjunction_without_marginal_rule() -> None:
    target = "Traits : Personality : Target"
    other = "Traits : Personality : Other"
    records = []
    for f1, f2 in (("0", "0"), ("0", "1"), ("1", "0"), ("1", "1")):
        label = target if (f1, f2) == ("1", "1") else other
        for index in range(12):
            records.append(
                _record(f"{f1}{f2}-{index}", (label,), f1=f1, f2=f2)
            )
    model = OpportunityConditionedNeighborModel.fit(
        tuple(records),
        model_id="conjunction",
        feature_names=("f1", "f2"),
        neighbor_count=8,
        min_label_count=2,
        min_opportunity_count=8,
    )
    person = _record("held", (target,), f1="1", f2="1")
    true_score = model.score_candidate(person, _chart("true", "held", f1="1", f2="1"))
    decoy_score = model.score_candidate(person, _chart("decoy", "held", f1="1", f2="0"))
    assert true_score is not None and decoy_score is not None
    assert true_score > decoy_score


def test_training_source_block_must_also_be_candidate_match_field() -> None:
    records = tuple(
        _record(
            f"p{i}",
            ("Traits : Personality : Active",),
            f1=str(i % 2),
            source="A",
        )
        for i in range(8)
    )
    charts = tuple(
        _chart(f"c{i}", f"p{i}", f1=str(i % 2), source="A")
        for i in range(8)
    )
    with pytest.raises(ValueError, match="training_block_fields"):
        cross_fitted_opportunity_identification(
            records,
            charts,
            model_id="bad-block",
            feature_names=("f1",),
            training_block_fields=("source",),
            candidate_match_fields=("year",),
            neighbor_count=2,
            min_label_count=1,
            min_opportunity_count=2,
            folds=2,
            max_decoys=3,
        )
