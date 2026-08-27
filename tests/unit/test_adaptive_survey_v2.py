from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from pathlib import Path

import pytest

from hdmatch.evaluation.adaptive_survey_v2 import (
    PRIMARY_NATAL_BODIES,
    AdaptiveSurveyV2Item,
    item_matches,
    load_adaptive_v2_items,
    select_structural_split_item,
)
from hdmatch.schemas import CandidateState, LocalDateOverlap, StructuralChartFeatures


ROOT = Path(__file__).resolve().parents[2]


def _items() -> tuple[AdaptiveSurveyV2Item, ...]:
    return load_adaptive_v2_items(
        gate_catalog_path=ROOT / "reference/core/mapping_v2_gate_catalog.json",
        channel_catalog_path=ROOT / "reference/core/mapping_v2_channel_catalog.json",
        planet_roles_path=ROOT / "reference/core/mapping_v2_planet_roles.json",
    )


def test_v2_catalog_generates_1444_opaque_candidate_blind_items() -> None:
    items = _items()

    assert PRIMARY_NATAL_BODIES == (
        "sun",
        "earth",
        "moon",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
        "pluto",
    )
    assert len(items) == 1444
    assert len({item.question_id for item in items}) == 1444
    assert sum(item.kind == "planet_gate" for item in items) == 1408
    assert sum(item.kind == "channel" for item in items) == 36
    assert all(item.question_id.startswith("Q2-") for item in items)
    assert all("moon" not in item.question_id.casefold() for item in items)
    assert all("gate" not in item.prompt.casefold() for item in items)
    assert all("human design" not in item.prompt.casefold() for item in items)
    assert all("other / context-dependent" in item.response_format.casefold() for item in items)
    assert not any(item.body in {"north_node", "south_node"} for item in items)


def test_outer_planet_roles_generate_candidate_blind_items() -> None:
    items = _items()
    expected_bodies = {"jupiter", "saturn", "uranus", "neptune", "pluto"}
    observed_bodies = {
        item.body
        for item in items
        if item.kind == "planet_gate" and item.body in expected_bodies
    }

    assert observed_bodies == expected_bodies
    jupiter = next(
        item
        for item in items
        if item.kind == "planet_gate"
        and item.side == "personality"
        and item.body == "jupiter"
        and item.gate == 53
    )
    assert "expansion" in jupiter.prompt.casefold()
    assert "jupiter" not in jupiter.prompt.casefold()
    assert "53" not in jupiter.prompt


def test_design_planet_items_require_outside_observation_followup() -> None:
    items = _items()
    design = next(
        item
        for item in items
        if item.kind == "planet_gate"
        and item.side == "design"
        and item.body == "moon"
        and item.gate == 53
    )
    personality = next(
        item
        for item in items
        if item.kind == "planet_gate"
        and item.side == "personality"
        and item.body == "moon"
        and item.gate == 53
    )

    assert design.reliability == pytest.approx(0.70)
    assert personality.reliability == pytest.approx(0.80)
    assert len(design.followups) == len(personality.followups) + 1
    assert "close others" in design.followups[-1].casefold()


def test_item_matching_is_exact_for_body_side_gate_and_channel_order_independent() -> None:
    items = _items()
    state = _state(
        "one",
        activations={"personality:moon": 53, "design:moon": 12},
        channels=("48-16",),
    )
    features = state.chart_features
    assert isinstance(features, StructuralChartFeatures)

    moon_53 = next(
        item
        for item in items
        if item.kind == "planet_gate"
        and item.side == "personality"
        and item.body == "moon"
        and item.gate == 53
    )
    moon_12 = next(
        item
        for item in items
        if item.kind == "planet_gate"
        and item.side == "personality"
        and item.body == "moon"
        and item.gate == 12
    )
    channel = next(
        item for item in items if item.kind == "channel" and item.channel == "16-48"
    )

    assert item_matches(features, moon_53)
    assert not item_matches(features, moon_12)
    assert item_matches(features, channel)


def test_selector_prefers_balanced_reliable_split_without_using_answers() -> None:
    items = _items()
    moon_53 = next(
        item
        for item in items
        if item.kind == "planet_gate"
        and item.side == "personality"
        and item.body == "moon"
        and item.gate == 53
    )
    moon_12 = next(
        item
        for item in items
        if item.kind == "planet_gate"
        and item.side == "personality"
        and item.body == "moon"
        and item.gate == 12
    )
    states = (
        _state("a", activations={"personality:moon": 53}),
        _state("b", activations={"personality:moon": 53}),
        _state("c", activations={"personality:moon": 12}),
        _state("d", activations={"personality:moon": 12}),
    )

    selected = select_structural_split_item(
        states=states,
        weights=(1.0, 1.0, 1.0, 1.0),
        items=(moon_53, moon_12),
        answered_question_ids=frozenset(),
    )
    assert selected is not None
    assert selected[0].question_id == min(moon_53.question_id, moon_12.question_id)
    assert selected[1] == pytest.approx(0.8)


def _state(
    state_id: str,
    *,
    activations: dict[str, int],
    channels: tuple[str, ...] = (),
) -> CandidateState:
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
            channels=channels,
            activation_gates=activations,
        ),
        local_date_overlaps=(
            LocalDateOverlap(date=date(2000, 1, 1), seconds=3600.0),
        ),
    )
