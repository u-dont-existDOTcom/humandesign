"""Frozen AstroRRF V0.1 scoring plus later frozen-family feature flags."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Literal, cast

from .western import (
    WesternNatalSnapshot,
    WesternRelationshipFeatures,
    classify_major_aspect,
)

ActorId = Literal["a", "b"]


@dataclass(frozen=True, slots=True)
class ScoreContribution:
    feature: str
    value: float
    detail: str


@dataclass(frozen=True, slots=True)
class DirectionalScore:
    actor: ActorId
    axis: str
    score: float
    contributions: tuple[ScoreContribution, ...]


@dataclass(frozen=True, slots=True)
class AstroRRFV01Result:
    model_version: str
    max_orb_degrees: float
    directional_scores: tuple[DirectionalScore, ...]
    frozen_family_flags: dict[str, Any]


def score_astro_rrf_v01(
    features: WesternRelationshipFeatures,
    model: dict[str, Any],
) -> AstroRRFV01Result:
    """Apply only the exact V0.1 feature families/weights frozen in the model JSON."""

    max_orb = float(model["max_orb_degrees"])
    scores: list[DirectionalScore] = []
    for actor in ("a", "b"):
        actor_id = cast(ActorId, actor)
        actor_natal, partner_natal, overlays = _direction(features, actor_id)
        scores.extend(
            (
                _score_eros(actor_id, actor_natal, partner_natal, overlays, max_orb=max_orb),
                _score_communication(
                    actor_id, actor_natal, partner_natal, max_orb=max_orb
                ),
                _score_emotional_ease(
                    actor_id, actor_natal, partner_natal, max_orb=max_orb
                ),
                _score_engulfment(
                    actor_id, actor_natal, partner_natal, overlays, max_orb=max_orb
                ),
            )
        )
    return AstroRRFV01Result(
        model_version=str(model["version"]),
        max_orb_degrees=max_orb,
        directional_scores=tuple(scores),
        frozen_family_flags=_later_family_flags(features, max_orb=max_orb),
    )


def result_payload(result: AstroRRFV01Result) -> dict[str, Any]:
    return {
        "model_version": result.model_version,
        "max_orb_degrees": result.max_orb_degrees,
        "directional_scores": [
            {
                "actor": row.actor,
                "axis": row.axis,
                "score": round(row.score, 6),
                "contributions": [
                    {
                        "feature": item.feature,
                        "value": round(item.value, 6),
                        "detail": item.detail,
                    }
                    for item in row.contributions
                ],
            }
            for row in result.directional_scores
        ],
        "frozen_family_flags": result.frozen_family_flags,
        "interpretation_boundary": (
            "Raw frozen-model scores/features only. No post-hoc absolute high/low threshold "
            "is invented here; later calibration must be versioned separately."
        ),
    }


def _score_eros(
    actor_id: ActorId,
    actor: WesternNatalSnapshot,
    partner: WesternNatalSnapshot,
    overlays: dict[str, int],
    *,
    max_orb: float,
) -> DirectionalScore:
    contributions: list[ScoreContribution] = []
    for actor_body in ("venus", "mars"):
        for partner_body in ("sun", "moon"):
            _add_aspect(
                contributions,
                actor,
                partner,
                actor_body,
                partner_body,
                weights={
                    "conjunction": 1.0,
                    "square": 1.0,
                    "opposition": 1.0,
                    "sextile": 0.45,
                    "trine": 0.45,
                },
                feature="actor_venus_or_mars_to_partner_sun_or_moon",
                max_orb=max_orb,
            )
    for body in ("venus", "mars"):
        house = overlays.get(body)
        weight = {5: 1.1, 7: 1.0, 8: 0.9}.get(house)
        if weight is not None:
            contributions.append(
                ScoreContribution(
                    "partner_venus_or_mars_house_overlay",
                    weight,
                    f"partner {body} in actor house {house}",
                )
            )
    for body in ("sun", "moon"):
        house = overlays.get(body)
        if house in {5, 7, 8}:
            contributions.append(
                ScoreContribution(
                    "partner_sun_or_moon_house_overlay",
                    0.4,
                    f"partner {body} in actor house {house}",
                )
            )
    for actor_body in ("venus", "mars"):
        _add_aspect(
            contributions,
            actor,
            partner,
            actor_body,
            "pluto",
            weights={
                "conjunction": 0.75,
                "square": 0.75,
                "opposition": 0.75,
                "sextile": 0.35,
                "trine": 0.35,
            },
            feature="actor_venus_or_mars_to_partner_pluto",
            max_orb=max_orb,
        )
    return _final_score(actor_id, "actor_eros_passion", contributions)


def _score_communication(
    actor_id: ActorId,
    actor: WesternNatalSnapshot,
    partner: WesternNatalSnapshot,
    *,
    max_orb: float,
) -> DirectionalScore:
    contributions: list[ScoreContribution] = []
    for partner_body in ("mercury", "sun"):
        _add_aspect(
            contributions,
            actor,
            partner,
            "mercury",
            partner_body,
            weights={
                "conjunction": 0.6,
                "sextile": 0.6,
                "trine": 0.6,
                "square": 0.15,
                "opposition": 0.15,
            },
            feature="actor_mercury_to_partner_mercury_or_sun",
            max_orb=max_orb,
        )
    _add_aspect(
        contributions,
        actor,
        partner,
        "mercury",
        "uranus",
        weights={
            "conjunction": 1.0,
            "square": 1.0,
            "opposition": 1.0,
            "sextile": 0.6,
            "trine": 0.6,
        },
        feature="actor_mercury_to_partner_uranus",
        max_orb=max_orb,
    )
    _add_aspect(
        contributions,
        actor,
        partner,
        "mercury",
        "pluto",
        weights={
            "conjunction": 0.9,
            "square": 0.9,
            "opposition": 0.9,
            "sextile": 0.7,
            "trine": 0.7,
        },
        feature="actor_mercury_to_partner_pluto",
        max_orb=max_orb,
    )
    return _final_score(actor_id, "actor_communication_intellectual_fit", contributions)


def _score_emotional_ease(
    actor_id: ActorId,
    actor: WesternNatalSnapshot,
    partner: WesternNatalSnapshot,
    *,
    max_orb: float,
) -> DirectionalScore:
    contributions: list[ScoreContribution] = []
    _add_aspect(
        contributions,
        actor,
        partner,
        "moon",
        "moon",
        weights={
            "conjunction": 1.5,
            "sextile": 1.5,
            "trine": 1.5,
            "square": -1.5,
            "opposition": -1.5,
        },
        feature="actor_moon_to_partner_moon",
        max_orb=max_orb,
    )
    _add_aspect(
        contributions,
        actor,
        partner,
        "moon",
        "pluto",
        weights={"conjunction": -3.5, "square": -3.5, "opposition": -3.5},
        feature="actor_moon_to_partner_pluto",
        max_orb=max_orb,
    )
    for body in ("venus", "jupiter"):
        _add_aspect(
            contributions,
            actor,
            partner,
            "moon",
            body,
            weights={"square": -0.5, "opposition": -0.5},
            feature="actor_moon_to_partner_venus_or_jupiter",
            max_orb=max_orb,
        )
    for body in ("saturn", "neptune"):
        _add_aspect(
            contributions,
            actor,
            partner,
            "moon",
            body,
            weights={"sextile": 0.25, "trine": 0.25},
            feature="actor_moon_to_partner_saturn_or_neptune",
            max_orb=max_orb,
        )
    _add_aspect(
        contributions,
        actor,
        partner,
        "moon",
        "neptune",
        weights={"square": -0.8, "opposition": -0.8},
        feature="actor_moon_to_partner_neptune",
        max_orb=max_orb,
    )
    return _final_score(actor_id, "actor_emotional_ease", contributions)


def _score_engulfment(
    actor_id: ActorId,
    actor: WesternNatalSnapshot,
    partner: WesternNatalSnapshot,
    overlays: dict[str, int],
    *,
    max_orb: float,
) -> DirectionalScore:
    contributions: list[ScoreContribution] = []
    for actor_body, partner_body, hard, soft, feature in (
        ("moon", "pluto", 4.0, 0.5, "actor_moon_to_partner_pluto"),
        ("venus", "pluto", 2.0, 0.5, "actor_venus_to_partner_pluto"),
        ("saturn", "pluto", 1.5, 0.5, "actor_saturn_to_partner_pluto"),
    ):
        _add_aspect(
            contributions,
            actor,
            partner,
            actor_body,
            partner_body,
            weights={
                "conjunction": hard,
                "square": hard,
                "opposition": hard,
                "sextile": soft,
                "trine": soft,
            },
            feature=feature,
            max_orb=max_orb,
        )
    for body in ("venus", "mars"):
        if overlays.get(body) in {7, 8}:
            contributions.append(
                ScoreContribution(
                    "partner_venus_or_mars_house_overlay",
                    0.5,
                    f"partner {body} in actor house {overlays[body]}",
                )
            )
    if overlays.get("moon") == 12:
        contributions.append(
            ScoreContribution(
                "partner_moon_house_overlay",
                0.75,
                "partner moon in actor house 12",
            )
        )
    if actor.ascendant is not None:
        best_orb: float | None = None
        for axis in (actor.ascendant, (actor.ascendant + 180.0) % 360.0):
            match = classify_major_aspect(
                partner.longitudes["uranus"], axis, max_orb=max_orb
            )
            if match is not None and (best_orb is None or match[1] < best_orb):
                best_orb = match[1]
        if best_orb is not None:
            value = -1.5 * _orb_kernel(best_orb, max_orb)
            contributions.append(
                ScoreContribution(
                    "partner_uranus_to_actor_ascendant_axis",
                    value,
                    f"major aspect to Asc/Desc axis, orb {best_orb:.3f}°",
                )
            )
    return _final_score(actor_id, "actor_engulfment_pressure", contributions)


def _add_aspect(
    contributions: list[ScoreContribution],
    actor: WesternNatalSnapshot,
    partner: WesternNatalSnapshot,
    actor_body: str,
    partner_body: str,
    *,
    weights: dict[str, float],
    feature: str,
    max_orb: float,
) -> None:
    match = classify_major_aspect(
        actor.longitudes[actor_body], partner.longitudes[partner_body], max_orb=max_orb
    )
    if match is None:
        return
    aspect, orb = match
    weight = weights.get(aspect)
    if weight is None:
        return
    value = weight * _orb_kernel(orb, max_orb)
    contributions.append(
        ScoreContribution(
            feature,
            value,
            f"actor {actor_body} {aspect} partner {partner_body}, orb {orb:.3f}°",
        )
    )


def _orb_kernel(orb: float, max_orb: float) -> float:
    return math.exp(-0.5 * (orb / max_orb) ** 2)


def _final_score(
    actor_id: ActorId,
    axis: str,
    contributions: list[ScoreContribution],
) -> DirectionalScore:
    return DirectionalScore(
        actor=actor_id,
        axis=axis,
        score=sum(item.value for item in contributions),
        contributions=tuple(contributions),
    )


def _direction(
    features: WesternRelationshipFeatures,
    actor_id: ActorId,
) -> tuple[WesternNatalSnapshot, WesternNatalSnapshot, dict[str, int]]:
    if actor_id == "a":
        return features.natal_a, features.natal_b, features.b_planets_in_a_houses
    return features.natal_b, features.natal_a, features.a_planets_in_b_houses


def _later_family_flags(
    features: WesternRelationshipFeatures,
    *,
    max_orb: float,
) -> dict[str, Any]:
    return {
        "houses_available": {
            "a": features.natal_a.house_cusps is not None,
            "b": features.natal_b.house_cusps is not None,
        },
        "shared_intellectual_candidates": {
            "composite_mercury_sun": _aspect_flag(
                features.composite_longitudes, "mercury", "sun", max_orb=max_orb
            ),
            "composite_mercury_neptune": _aspect_flag(
                features.composite_longitudes, "mercury", "neptune", max_orb=max_orb
            ),
            "composite_jupiter_neptune": _aspect_flag(
                features.composite_longitudes, "jupiter", "neptune", max_orb=max_orb
            ),
        },
        "novelty_habituation_candidates": {
            "a": _novelty_flags(features.natal_a, features.natal_b, features.b_planets_in_a_houses, max_orb=max_orb),
            "b": _novelty_flags(features.natal_b, features.natal_a, features.a_planets_in_b_houses, max_orb=max_orb),
        },
    }


def _novelty_flags(
    actor: WesternNatalSnapshot,
    partner: WesternNatalSnapshot,
    overlays: dict[str, int],
    *,
    max_orb: float,
) -> dict[str, Any]:
    natal_uranus_aspects = {
        body: _direct_aspect(actor, "uranus", actor, body, max_orb=max_orb)
        for body in ("venus", "mars")
    }
    return {
        "natal_uranus_house_5": (
            _house_of_natal_body(actor, "uranus") == 5 if actor.house_cusps else None
        ),
        "natal_uranus_major_aspect_venus_or_mars": natal_uranus_aspects,
        "synastry_actor_mars_partner_uranus": _direct_aspect(
            actor, "mars", partner, "uranus", max_orb=max_orb
        ),
        "partner_uranus_in_actor_house_5": (
            overlays.get("uranus") == 5 if overlays else None
        ),
    }


def _house_of_natal_body(natal: WesternNatalSnapshot, body: str) -> int | None:
    if natal.house_cusps is None:
        return None
    from .western import house_for_longitude

    return house_for_longitude(natal.longitudes[body], natal.house_cusps)


def _direct_aspect(
    left: WesternNatalSnapshot,
    left_body: str,
    right: WesternNatalSnapshot,
    right_body: str,
    *,
    max_orb: float,
) -> dict[str, Any] | None:
    match = classify_major_aspect(
        left.longitudes[left_body], right.longitudes[right_body], max_orb=max_orb
    )
    if match is None:
        return None
    aspect, orb = match
    return {"aspect": aspect, "orb_degrees": round(orb, 6)}


def _aspect_flag(
    longitudes: dict[str, float],
    body_a: str,
    body_b: str,
    *,
    max_orb: float,
) -> dict[str, Any] | None:
    match = classify_major_aspect(longitudes[body_a], longitudes[body_b], max_orb=max_orb)
    if match is None:
        return None
    aspect, orb = match
    return {"aspect": aspect, "orb_degrees": round(orb, 6)}
