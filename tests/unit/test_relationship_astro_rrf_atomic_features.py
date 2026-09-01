from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from hdmatch.relationship.astro_rrf import result_payload, score_astro_rrf_v01
from hdmatch.relationship.astro_rrf_features import (
    atomic_feature_payload,
    freeze_atomic_features_v1,
)
from hdmatch.relationship.western import WesternNatalSnapshot, relationship_features

SCHEMA_PATH = Path("reference/relationship/astro_rrf_atomic_feature_schema_v1.json")
MODEL_PATH = Path("reference/development_models/astro_rrf_directional_v0_1.json")
CASE_ROLE_PATH = Path("reference/development_cases/astro_rrf_case_role_manifest_v1.json")


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


def _natal(
    longitudes: dict[str, float],
    *,
    houses: bool = True,
) -> WesternNatalSnapshot:
    return WesternNatalSnapshot(
        birth_utc=datetime(1990, 1, 1, tzinfo=UTC),
        longitudes=longitudes,
        latitude=0.0 if houses else None,
        longitude=0.0 if houses else None,
        ascendant=0.0 if houses else None,
        midheaven=270.0 if houses else None,
        house_cusps=(
            tuple(float(value) for value in range(0, 360, 30)) if houses else None
        ),
    )


def _schema() -> tuple[dict[str, Any], str]:
    raw = SCHEMA_PATH.read_bytes()
    parsed = json.loads(raw)
    assert isinstance(parsed, dict)
    return parsed, hashlib.sha256(raw).hexdigest()


def _freeze(
    a: WesternNatalSnapshot,
    b: WesternNatalSnapshot,
) -> dict[str, Any]:
    schema, digest = _schema()
    frozen = freeze_atomic_features_v1(
        relationship_features(a, b),
        schema,
        schema_sha256=digest,
    )
    return atomic_feature_payload(frozen)


def test_atomic_feature_freeze_has_deterministic_fixed_keys() -> None:
    a = _natal(_longitudes())
    b = _natal(_longitudes(sun=44.0, venus=130.0, uranus=180.0))

    first = _freeze(a, b)
    second = _freeze(a, b)

    assert first == second
    assert tuple(first["directions"]) == ("a", "b")
    for actor_id in ("a", "b"):
        direction = first["directions"][actor_id]
        assert len(direction["synastry_aspects"]) == 11 * 11
        assert len(direction["house_overlays"]) == 11 * 7
        assert tuple(direction["angle_contacts"]) == (
            "partner_uranus__actor_ascendant",
        )
        assert tuple(direction["novelty_flags"]) == (
            "natal_uranus_house_5",
            "natal_uranus_major_aspect_venus",
            "natal_uranus_major_aspect_mars",
            "synastry_actor_mars__partner_uranus",
            "partner_uranus__actor_house_5",
        )
    assert len(first["composite_aspects"]) == 55
    assert "actor_venus__partner_sun" in first["directions"]["a"]["synastry_aspects"]
    assert "sun__mercury" in first["composite_aspects"]


def test_actor_swap_preserves_direction_and_house_owner() -> None:
    a = _natal(_longitudes(sun=0.0, venus=250.0, uranus=5.0))
    b = _natal(_longitudes(sun=180.0, venus=130.0, uranus=200.0))

    ab = _freeze(a, b)
    ba = _freeze(b, a)

    assert ab["directions"]["a"] == ba["directions"]["b"]
    assert ab["directions"]["b"] == ba["directions"]["a"]
    assert ab["composite_aspects"] == ba["composite_aspects"]
    assert ab["directions"]["a"]["house_overlays"][
        "partner_venus__actor_house_5"
    ] is True
    assert ab["directions"]["b"]["house_overlays"][
        "partner_venus__actor_house_5"
    ] is False


def test_available_absence_is_zero_or_false_but_unavailable_geometry_is_null() -> None:
    available = _freeze(
        _natal(_longitudes()),
        _natal(_longitudes(sun=44.0, venus=130.0, uranus=44.0)),
    )
    no_aspect = available["directions"]["a"]["synastry_aspects"][
        "actor_sun__partner_sun"
    ]
    assert no_aspect == {
        "present": False,
        "aspect": None,
        "orb_degrees": None,
        "orb_kernel": 0.0,
    }
    assert available["directions"]["a"]["house_overlays"][
        "partner_venus__actor_house_7"
    ] is False

    unavailable = _freeze(
        _natal(_longitudes(), houses=False),
        _natal(_longitudes(uranus=44.0), houses=False),
    )
    assert unavailable["directions"]["a"]["house_overlays"][
        "partner_venus__actor_house_5"
    ] is None
    assert unavailable["directions"]["a"]["angle_contacts"][
        "partner_uranus__actor_ascendant"
    ] == {
        "present": None,
        "aspect": None,
        "orb_degrees": None,
        "orb_kernel": None,
    }


def test_schema_hash_is_bound_and_atomic_freeze_does_not_change_v01_scores() -> None:
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
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    before = result_payload(score_astro_rrf_v01(features, model))
    schema, digest = _schema()

    frozen = freeze_atomic_features_v1(features, schema, schema_sha256=digest)
    payload = atomic_feature_payload(frozen)
    after = result_payload(score_astro_rrf_v01(features, model))

    assert payload["schema_sha256"] == digest
    assert before == after
    with pytest.raises(ValueError, match="schema_sha256"):
        freeze_atomic_features_v1(features, schema, schema_sha256="not-a-digest")


def test_atomic_payload_excludes_private_and_behavioral_fields() -> None:
    rendered = json.dumps(
        _freeze(_natal(_longitudes()), _natal(_longitudes(sun=90.0))),
        sort_keys=True,
    ).casefold()
    for forbidden in (
        '"birth',
        '"email',
        '"contact',
        '"name',
        '"narrative',
        '"answer',
        '"latitude',
        '"longitude',
    ):
        assert forbidden not in rendered


def test_existing_six_cases_are_diagnostic_only_not_calibration_or_validation() -> None:
    manifest = json.loads(CASE_ROLE_PATH.read_text(encoding="utf-8"))
    assert [item["case_id"] for item in manifest["cases"]] == [
        "pair_1",
        "pair_2",
        "pair_3",
        "pair_4",
        "pair_5",
        "pair_6",
    ]
    assert {item["role"] for item in manifest["cases"]} == {
        "development_diagnostic_only"
    }
    assert "ordinal_calibration" in manifest["prohibited_roles_for_listed_cases"]
    assert "untouched_validation" in manifest["prohibited_roles_for_listed_cases"]
