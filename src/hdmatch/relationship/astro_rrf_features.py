"""Outcome-blind atomic geometry freeze for later AstroRRF calibration.

The legacy V0.1 scores intentionally remain in :mod:`astro_rrf`.  This module
serializes the already-computed Western geometry without assigning new outcome
meanings, weights, thresholds, probabilities, or hit/miss labels.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations, product
from typing import Any, Literal, cast

from .western import (
    WesternNatalSnapshot,
    WesternRelationshipFeatures,
    classify_major_aspect,
)

ActorId = Literal["a", "b"]
SCHEMA_VERSION: Literal["astro-rrf-atomic-feature-schema-v1"] = (
    "astro-rrf-atomic-feature-schema-v1"
)


@dataclass(frozen=True, slots=True)
class AtomicAspectFeature:
    """One major-aspect atom.

    ``present=False`` and ``orb_kernel=0`` mean the geometry was available but
    no declared major aspect fell inside the frozen orb.  ``present=None`` means
    the required geometry (currently an angle) was unavailable.
    """

    present: bool | None
    aspect: str | None
    orb_degrees: float | None
    orb_kernel: float | None


@dataclass(frozen=True, slots=True)
class AstroRRFAtomicFeatureFreezeV1:
    schema_version: Literal["astro-rrf-atomic-feature-schema-v1"]
    schema_sha256: str
    max_orb_degrees: float
    directions: dict[ActorId, dict[str, Any]]
    composite_aspects: dict[str, AtomicAspectFeature]
    interpretation_boundary: str = (
        "Outcome-blind atomic geometry only. These values have no ordinal outcome mapping, "
        "calibrated probability, or hit/miss meaning."
    )


def freeze_atomic_features_v1(
    features: WesternRelationshipFeatures,
    schema: dict[str, Any],
    *,
    schema_sha256: str,
) -> AstroRRFAtomicFeatureFreezeV1:
    """Freeze the exact fixed-key geometry declared by the public schema."""

    if schema.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported AstroRRF atomic schema: {schema.get('schema_version')!r}")
    if len(schema_sha256) != 64 or any(char not in "0123456789abcdef" for char in schema_sha256):
        raise ValueError("schema_sha256 must be a lowercase SHA-256 digest")

    max_orb = float(schema["max_orb_degrees"])
    if not math.isfinite(max_orb) or max_orb <= 0.0:
        raise ValueError("max_orb_degrees must be finite and positive")
    bodies = _string_tuple(schema, "bodies")
    house_bodies = _string_tuple(schema, "house_overlay_bodies")
    house_targets = _house_targets(schema)
    composite_bodies = _string_tuple(schema, "composite_bodies")
    angle_contacts = _angle_contacts(schema)

    directions: dict[ActorId, dict[str, Any]] = {}
    actor_ids: tuple[ActorId, ActorId] = ("a", "b")
    for actor_id in actor_ids:
        actor, partner, overlays = _direction(features, actor_id)
        synastry = {
            f"actor_{actor_body}__partner_{partner_body}": _aspect_feature(
                actor.longitudes[actor_body],
                partner.longitudes[partner_body],
                max_orb=max_orb,
            )
            for actor_body, partner_body in product(bodies, repeat=2)
        }
        houses_available = actor.house_cusps is not None
        house_overlays = {
            f"partner_{body}__actor_house_{house}": (
                overlays[body] == house if houses_available else None
            )
            for body in house_bodies
            for house in house_targets
        }
        angle_features = {
            f"partner_{body}__actor_{angle}": _angle_aspect_feature(
                partner,
                body,
                actor,
                angle,
                max_orb=max_orb,
            )
            for body, angle in angle_contacts
        }
        novelty = {
            "natal_uranus_house_5": (
                _natal_body_house(actor, "uranus") == 5 if houses_available else None
            ),
            "natal_uranus_major_aspect_venus": _aspect_feature(
                actor.longitudes["uranus"], actor.longitudes["venus"], max_orb=max_orb
            ),
            "natal_uranus_major_aspect_mars": _aspect_feature(
                actor.longitudes["uranus"], actor.longitudes["mars"], max_orb=max_orb
            ),
            "synastry_actor_mars__partner_uranus": synastry[
                "actor_mars__partner_uranus"
            ],
            "partner_uranus__actor_house_5": house_overlays[
                "partner_uranus__actor_house_5"
            ],
        }
        directions[actor_id] = {
            "synastry_aspects": synastry,
            "house_overlays": house_overlays,
            "angle_contacts": angle_features,
            "novelty_flags": novelty,
        }

    composite_aspects = {
        f"{body_a}__{body_b}": _aspect_feature(
            features.composite_longitudes[body_a],
            features.composite_longitudes[body_b],
            max_orb=max_orb,
        )
        for body_a, body_b in combinations(composite_bodies, 2)
    }
    return AstroRRFAtomicFeatureFreezeV1(
        schema_version=SCHEMA_VERSION,
        schema_sha256=schema_sha256,
        max_orb_degrees=max_orb,
        directions=directions,
        composite_aspects=composite_aspects,
    )


def atomic_feature_payload(result: AstroRRFAtomicFeatureFreezeV1) -> dict[str, Any]:
    """Return a stable JSON-compatible payload without raw birth/chart longitudes."""

    return {
        "schema_version": result.schema_version,
        "schema_sha256": result.schema_sha256,
        "max_orb_degrees": result.max_orb_degrees,
        "directions": {
            actor_id: {
                "synastry_aspects": {
                    key: _aspect_payload(value)
                    for key, value in direction["synastry_aspects"].items()
                },
                "house_overlays": dict(direction["house_overlays"]),
                "angle_contacts": {
                    key: _aspect_payload(value)
                    for key, value in direction["angle_contacts"].items()
                },
                "novelty_flags": {
                    key: (
                        _aspect_payload(value)
                        if isinstance(value, AtomicAspectFeature)
                        else value
                    )
                    for key, value in direction["novelty_flags"].items()
                },
            }
            for actor_id, direction in result.directions.items()
        },
        "composite_aspects": {
            key: _aspect_payload(value) for key, value in result.composite_aspects.items()
        },
        "interpretation_boundary": result.interpretation_boundary,
    }


def _aspect_payload(value: AtomicAspectFeature) -> dict[str, Any]:
    return {
        "present": value.present,
        "aspect": value.aspect,
        "orb_degrees": value.orb_degrees,
        "orb_kernel": value.orb_kernel,
    }


def _aspect_feature(
    longitude_a: float,
    longitude_b: float,
    *,
    max_orb: float,
) -> AtomicAspectFeature:
    match = classify_major_aspect(longitude_a, longitude_b, max_orb=max_orb)
    if match is None:
        return AtomicAspectFeature(False, None, None, 0.0)
    aspect, orb = match
    return AtomicAspectFeature(
        True,
        aspect,
        round(orb, 6),
        round(math.exp(-0.5 * (orb / max_orb) ** 2), 6),
    )


def _angle_aspect_feature(
    partner: WesternNatalSnapshot,
    partner_body: str,
    actor: WesternNatalSnapshot,
    angle: str,
    *,
    max_orb: float,
) -> AtomicAspectFeature:
    longitude = actor.ascendant if angle == "ascendant" else actor.midheaven
    if longitude is None:
        return AtomicAspectFeature(None, None, None, None)
    return _aspect_feature(partner.longitudes[partner_body], longitude, max_orb=max_orb)


def _natal_body_house(natal: WesternNatalSnapshot, body: str) -> int | None:
    if natal.house_cusps is None:
        return None
    from .western import house_for_longitude

    return house_for_longitude(natal.longitudes[body], natal.house_cusps)


def _direction(
    features: WesternRelationshipFeatures,
    actor_id: ActorId,
) -> tuple[WesternNatalSnapshot, WesternNatalSnapshot, dict[str, int]]:
    if actor_id == "a":
        return features.natal_a, features.natal_b, features.b_planets_in_a_houses
    return features.natal_b, features.natal_a, features.a_planets_in_b_houses


def _string_tuple(schema: dict[str, Any], key: str) -> tuple[str, ...]:
    raw = schema.get(key)
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) for item in raw):
        raise ValueError(f"atomic schema {key} must be a nonempty string list")
    values = tuple(cast(list[str], raw))
    if len(values) != len(set(values)):
        raise ValueError(f"atomic schema {key} contains duplicates")
    return values


def _house_targets(schema: dict[str, Any]) -> tuple[int, ...]:
    raw = schema.get("house_overlay_target_houses")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, int) for item in raw):
        raise ValueError("atomic schema house_overlay_target_houses must be an integer list")
    values = tuple(cast(list[int], raw))
    if len(values) != len(set(values)) or any(value < 1 or value > 12 for value in values):
        raise ValueError("atomic schema house targets must be unique values from 1 through 12")
    return values


def _angle_contacts(schema: dict[str, Any]) -> tuple[tuple[str, str], ...]:
    raw = schema.get("angle_contacts")
    if not isinstance(raw, list):
        raise ValueError("atomic schema angle_contacts must be a list")
    values: list[tuple[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("atomic schema angle contacts must be objects")
        body = item.get("partner_body")
        angle = item.get("actor_angle")
        if not isinstance(body, str) or angle not in {"ascendant", "midheaven"}:
            raise ValueError("atomic schema angle contact is invalid")
        values.append((body, cast(str, angle)))
    if len(values) != len(set(values)):
        raise ValueError("atomic schema angle_contacts contains duplicates")
    return tuple(values)
