from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from pathlib import Path

import pytest

from hdmatch.evaluation.nodal_environment_v2 import (
    NodalEnvironmentV2Item,
    item_matches,
    load_nodal_environment_v2_items,
    select_nodal_split_item,
)
from hdmatch.schemas import CandidateState, LocalDateOverlap, StructuralChartFeatures


ROOT = Path(__file__).resolve().parents[2]


def _items() -> tuple[NodalEnvironmentV2Item, ...]:
    return load_nodal_environment_v2_items(
        gate_catalog_path=ROOT / "reference/core/mapping_v2_gate_catalog.json",
        nodal_roles_path=ROOT / "reference/core/mapping_v2_nodal_environment_roles.json",
    )


def test_nodal_secondary_bank_has_256_opaque_items() -> None:
    items = _items()

    assert len(items) == 256
    assert len({item.question_id for item in items}) == 256
    assert {item.domain for item in items} == {"environment", "perspective"}
    assert all(item.question_id.startswith("Q2N-") for item in items)
    assert all("node" not in item.prompt.casefold() for item in items)
    assert all("gate" not in item.prompt.casefold() for item in items)
    assert all("human design" not in item.prompt.casefold() for item in items)
    assert all("other / context-dependent" in item.response_format.casefold() for item in items)


def test_north_node_items_offer_not_yet_observable() -> None:
    items = _items()
    north = next(item for item in items if item.node == "north_node")
    south = next(item for item in items if item.node == "south_node")

    assert "not yet observable for my life stage" in north.response_format.casefold()
    assert north.reliability == pytest.approx(0.60)
    assert south.reliability == pytest.approx(0.75)


def test_nodal_matching_and_selector_are_structural_only() -> None:
    items = _items()
    gate_2 = next(
        item
        for item in items
        if item.side == "design" and item.node == "south_node" and item.gate == 2
    )
    gate_9 = next(
        item
        for item in items
        if item.side == "design" and item.node == "south_node" and item.gate == 9
    )
    states = (
        _state("a", {"design:south_node": 2}),
        _state("b", {"design:south_node": 2}),
        _state("c", {"design:south_node": 9}),
        _state("d", {"design:south_node": 9}),
    )
    features = states[0].chart_features
    assert isinstance(features, StructuralChartFeatures)
    assert item_matches(features, gate_2)
    assert not item_matches(features, gate_9)

    selected = select_nodal_split_item(
        states=states,
        weights=(1.0, 1.0, 1.0, 1.0),
        items=(gate_2, gate_9),
        answered_question_ids=frozenset(),
    )
    assert selected is not None
    assert selected[0].question_id == min(gate_2.question_id, gate_9.question_id)
    assert selected[1] == pytest.approx(0.75)


def _state(state_id: str, activations: dict[str, int]) -> CandidateState:
    start = datetime(2000, 1, 1, tzinfo=UTC) + timedelta(
        hours=sum(state_id.encode("utf-8")) % 24
    )
    end = start + timedelta(hours=1)
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=sha256(state_id.encode("utf-8")).hexdigest(),
        chart_features=StructuralChartFeatures(
            type="Generator",
            strategy="Wait to Respond",
            authority="Sacral",
            profile="1/3",
            definition="single",
            defined_centers=("Sacral",),
            channels=(),
            activation_gates=activations,
        ),
        local_date_overlaps=(
            LocalDateOverlap(date=date(2000, 1, 1), seconds=3600.0),
        ),
    )
