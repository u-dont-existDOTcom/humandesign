from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.relationship.astro_rrf import score_astro_rrf_v01
from hdmatch.relationship.western import (
    WesternNatalSnapshot,
    circular_midpoint,
    classify_major_aspect,
    house_for_longitude,
    relationship_features,
)


def _natal(longitudes: dict[str, float]) -> WesternNatalSnapshot:
    return WesternNatalSnapshot(
        birth_utc=datetime(1990, 1, 1, tzinfo=UTC),
        longitudes=longitudes,
        latitude=0.0,
        longitude=0.0,
        ascendant=0.0,
        midheaven=270.0,
        house_cusps=tuple(float(value) for value in range(0, 360, 30)),
    )


def _longitudes(**overrides: float) -> dict[str, float]:
    values = {
        "sun": 0.0,
        "moon": 10.0,
        "mercury": 20.0,
        "venus": 30.0,
        "mars": 40.0,
        "jupiter": 50.0,
        "saturn": 60.0,
        "uranus": 70.0,
        "neptune": 80.0,
        "pluto": 90.0,
        "north_node": 100.0,
    }
    values.update(overrides)
    return values


def test_major_aspect_and_circular_midpoint_geometry() -> None:
    assert classify_major_aspect(0.0, 90.0) == ("square", 0.0)
    assert classify_major_aspect(359.0, 1.0) == ("conjunction", 2.0)
    assert classify_major_aspect(0.0, 44.0) is None
    assert circular_midpoint(350.0, 10.0) == 0.0
    assert circular_midpoint(0.0, 180.0) == 90.0
    assert circular_midpoint(180.0, 0.0) == 90.0
    near_forward = circular_midpoint(0.0, 179.9999999)
    near_reverse = circular_midpoint(179.9999999, 0.0)
    assert math.isclose(near_forward, near_reverse, rel_tol=0.0, abs_tol=1e-12)
    assert not math.isclose(near_forward, 90.0, rel_tol=0.0, abs_tol=1e-12)


def test_house_assignment_wraps_across_zero() -> None:
    cusps = (350.0, 20.0, 50.0, 80.0, 110.0, 140.0, 170.0, 200.0, 230.0, 260.0, 290.0, 320.0)
    assert house_for_longitude(355.0, cusps) == 1
    assert house_for_longitude(5.0, cusps) == 1
    assert house_for_longitude(25.0, cusps) == 2


def test_frozen_v01_scorer_preserves_direction_and_house_owner() -> None:
    a = _natal(_longitudes(venus=0.0, mars=15.0, mercury=30.0, moon=45.0))
    b = _natal(
        _longitudes(
            sun=90.0,
            moon=135.0,
            venus=130.0,
            mars=220.0,
            mercury=30.0,
            uranus=120.0,
            pluto=180.0,
        )
    )
    features = relationship_features(a, b)
    model = json.loads(
        Path("reference/development_models/astro_rrf_directional_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    result = score_astro_rrf_v01(features, model)
    scores = {(row.actor, row.axis): row for row in result.directional_scores}
    a_eros = scores[("a", "actor_eros_passion")]
    assert a_eros.score > 1.0
    assert any(
        item.feature == "actor_venus_or_mars_to_partner_sun_or_moon"
        and "venus square partner sun" in item.detail
        for item in a_eros.contributions
    )
    assert any(
        item.feature == "partner_venus_or_mars_house_overlay"
        and "venus in actor house 5" in item.detail
        for item in a_eros.contributions
    )
    assert ("b", "actor_eros_passion") in scores
    assert result.frozen_family_flags["houses_available"] == {"a": True, "b": True}
