"""Source-native strength scorers for AstroHD V1.3b development.

The numerical rules in this module are frozen in
ASTROHD-V13B-SOURCE-NATIVE-STRENGTH-FREEZE-20260924.json.

Lilly scores preserve the bounded subset of William Lilly's published
fortitude/debility points selected before any V1.3b owner score. Parashari
scores consume normalized Shadbala strengths from the separately frozen
PyJHora oracle; PyJHora code is not copied into this project.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from hdmatch.evaluation.astrohd_v13_traditions import (
    EXALTATIONS,
    FALLS,
    RULERS,
    TraditionSnapshot,
    sign_name,
    whole_sign_house_sign,
)

PLANETS = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")
NONLUMINARIES = frozenset({"mercury", "venus", "mars", "jupiter", "saturn"})

LILLY_TRIPLICITY = {
    "fire": {"day": "sun", "night": "jupiter"},
    "earth": {"day": "venus", "night": "moon"},
    "air": {"day": "saturn", "night": "mercury"},
    "water": {"day": "mars", "night": "mars"},
}
SIGN_ELEMENT = {
    "aries": "fire",
    "leo": "fire",
    "sagittarius": "fire",
    "taurus": "earth",
    "virgo": "earth",
    "capricorn": "earth",
    "gemini": "air",
    "libra": "air",
    "aquarius": "air",
    "cancer": "water",
    "scorpio": "water",
    "pisces": "water",
}

# Ptolemy/Lilly term boundaries. Each tuple is (exclusive upper degree, ruler).
# Values match the table used in Lilly-style essential-dignity scoring.
LILLY_TERMS: dict[str, tuple[tuple[float, str], ...]] = {
    "aries": ((6, "jupiter"), (14, "venus"), (21, "mercury"), (26, "mars"), (30, "saturn")),
    "taurus": ((8, "venus"), (15, "mercury"), (22, "jupiter"), (26, "saturn"), (30, "mars")),
    "gemini": ((7, "mercury"), (14, "jupiter"), (21, "venus"), (25, "saturn"), (30, "mars")),
    "cancer": ((6, "mars"), (13, "jupiter"), (20, "mercury"), (27, "venus"), (30, "saturn")),
    "leo": ((6, "saturn"), (13, "mercury"), (19, "venus"), (25, "jupiter"), (30, "mars")),
    "virgo": ((7, "mercury"), (13, "venus"), (18, "jupiter"), (24, "saturn"), (30, "mars")),
    "libra": ((6, "saturn"), (11, "venus"), (19, "jupiter"), (24, "mercury"), (30, "mars")),
    "scorpio": ((6, "mars"), (14, "jupiter"), (21, "venus"), (27, "mercury"), (30, "saturn")),
    "sagittarius": ((8, "jupiter"), (14, "venus"), (19, "mercury"), (25, "saturn"), (30, "mars")),
    "capricorn": ((6, "venus"), (12, "mercury"), (19, "jupiter"), (25, "mars"), (30, "saturn")),
    "aquarius": ((6, "saturn"), (12, "mercury"), (20, "venus"), (25, "jupiter"), (30, "mars")),
    "pisces": ((8, "venus"), (14, "jupiter"), (20, "mercury"), (26, "mars"), (30, "saturn")),
}

LILLY_FACES = {
    "aries": ("mars", "sun", "venus"),
    "taurus": ("mercury", "moon", "saturn"),
    "gemini": ("jupiter", "mars", "sun"),
    "cancer": ("venus", "mercury", "moon"),
    "leo": ("saturn", "jupiter", "mars"),
    "virgo": ("sun", "venus", "mercury"),
    "libra": ("moon", "saturn", "jupiter"),
    "scorpio": ("mars", "sun", "venus"),
    "sagittarius": ("mercury", "moon", "saturn"),
    "capricorn": ("jupiter", "mars", "sun"),
    "aquarius": ("venus", "mercury", "moon"),
    "pisces": ("saturn", "jupiter", "mars"),
}

LILLY_HOUSE_POINTS = {
    1: 5,
    10: 5,
    4: 4,
    7: 4,
    11: 4,
    2: 3,
    5: 3,
    9: 2,
    3: 1,
    6: -2,
    8: -2,
    12: -5,
}


def degree_in_sign(longitude: float) -> float:
    return longitude % 30.0


def lilly_triplicity_ruler(sign: str, *, day_chart: bool) -> str:
    element = SIGN_ELEMENT[sign]
    return LILLY_TRIPLICITY[element]["day" if day_chart else "night"]


def lilly_term_ruler(sign: str, degree: float) -> str:
    if not 0.0 <= degree < 30.0:
        raise ValueError(f"term degree must be in [0, 30): {degree}")
    for upper, ruler in LILLY_TERMS[sign]:
        if degree < upper:
            return ruler
    raise RuntimeError(f"uncovered term degree: {sign} {degree}")


def lilly_face_ruler(sign: str, degree: float) -> str:
    if not 0.0 <= degree < 30.0:
        raise ValueError(f"face degree must be in [0, 30): {degree}")
    return LILLY_FACES[sign][min(2, int(degree // 10.0))]


def lilly_planet_native_strength(snapshot: TraditionSnapshot, planet: str) -> dict[str, Any]:
    """Return the frozen Lilly-core point total for one planet."""
    longitude = float(snapshot.tropical_longitudes[planet])
    sign = sign_name(longitude)
    degree = degree_in_sign(longitude)
    house = int(snapshot.regio_houses[planet])

    components: dict[str, int] = {}
    essential_dignified = False

    if RULERS[sign] == planet:
        components["own_sign"] = 5
        essential_dignified = True
    if EXALTATIONS[planet] == sign:
        components["exaltation"] = 4
        essential_dignified = True
    if lilly_triplicity_ruler(sign, day_chart=snapshot.day_chart) == planet:
        components["triplicity"] = 3
        essential_dignified = True
    if lilly_term_ruler(sign, degree) == planet:
        components["term"] = 2
        essential_dignified = True
    if lilly_face_ruler(sign, degree) == planet:
        components["face"] = 1
        essential_dignified = True

    detriment_signs = {s for s, ruler in RULERS.items() if ruler == planet}
    if any(_opposite_sign(s) == sign for s in detriment_signs):
        components["detriment"] = -5
    if FALLS[planet] == sign:
        components["fall"] = -4
    if not essential_dignified:
        components["peregrine"] = -5

    components["house"] = LILLY_HOUSE_POINTS.get(house, 0)
    if planet in NONLUMINARIES:
        speed = float(snapshot.tropical_speeds[planet])
        components["motion"] = 4 if speed >= 0.0 else -5

    return {
        "planet": planet,
        "sign": sign,
        "degree_in_sign": degree,
        "house": house,
        "components": components,
        "total": float(sum(components.values())),
    }


def lilly_domain_significators(
    snapshot: TraditionSnapshot,
    mapping: Mapping[str, Any],
) -> tuple[str, ...]:
    planets = {str(row["id"]) for row in mapping.get("planets", ())}
    for row in mapping.get("houses", ()):
        house = int(row["id"])
        cusp_sign = sign_name(float(snapshot.regio_cusps[house - 1]))
        planets.add(RULERS[cusp_sign])
    return tuple(sorted(planets))


def parashari_domain_significators(
    snapshot: TraditionSnapshot,
    mapping: Mapping[str, Any],
) -> tuple[str, ...]:
    planets = {str(row["id"]) for row in mapping.get("planets", ())}
    for row in mapping.get("houses", ()):
        house = int(row["id"])
        sign = whole_sign_house_sign(snapshot.sidereal_ascendant, house)
        planets.add(RULERS[sign])
    return tuple(sorted(planets))


def validate_shadbala_strengths(strengths: Mapping[str, float]) -> dict[str, float]:
    missing = set(PLANETS) - set(strengths)
    extra = set(strengths) - set(PLANETS)
    if missing or extra:
        raise ValueError(f"Shadbala planet keys mismatch: missing={sorted(missing)} extra={sorted(extra)}")
    result: dict[str, float] = {}
    for planet in PLANETS:
        value = float(strengths[planet])
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"invalid Shadbala strength for {planet}: {value}")
        result[planet] = value
    return result


def score_lilly_native(
    snapshot: TraditionSnapshot,
    *,
    consensus_map: Mapping[str, Any],
    behavior_weights: Mapping[str, float],
    aggregation: str,
) -> dict[str, Any]:
    strengths = {planet: lilly_planet_native_strength(snapshot, planet) for planet in PLANETS}
    return _score_native_domains(
        tradition="lilly_traditional_western",
        snapshot=snapshot,
        consensus_map=consensus_map,
        behavior_weights=behavior_weights,
        aggregation=aggregation,
        strength_lookup={planet: row["total"] for planet, row in strengths.items()},
        strength_details=strengths,
    )


def score_parashari_native(
    snapshot: TraditionSnapshot,
    *,
    consensus_map: Mapping[str, Any],
    behavior_weights: Mapping[str, float],
    shadbala_strengths: Mapping[str, float],
    aggregation: str,
) -> dict[str, Any]:
    strengths = validate_shadbala_strengths(shadbala_strengths)
    return _score_native_domains(
        tradition="parashari_jyotish",
        snapshot=snapshot,
        consensus_map=consensus_map,
        behavior_weights=behavior_weights,
        aggregation=aggregation,
        strength_lookup=strengths,
        strength_details={planet: {"total": value} for planet, value in strengths.items()},
    )


def _score_native_domains(
    *,
    tradition: str,
    snapshot: TraditionSnapshot,
    consensus_map: Mapping[str, Any],
    behavior_weights: Mapping[str, float],
    aggregation: str,
    strength_lookup: Mapping[str, float],
    strength_details: Mapping[str, Any],
) -> dict[str, Any]:
    if aggregation not in {"domain_mean_nonstack", "significator_stack"}:
        raise ValueError(f"unsupported native aggregation: {aggregation}")

    domains: list[dict[str, Any]] = []
    total = 0.0
    for domain in consensus_map["domains"]:
        domain_id = str(domain["domain_id"])
        weight = float(behavior_weights.get(domain_id, 0.0))
        if weight <= 0.0:
            continue
        mapping = next(
            row for row in domain["traditions"] if row["tradition"] == tradition
        )
        if tradition == "lilly_traditional_western":
            significators = lilly_domain_significators(snapshot, mapping)
        else:
            significators = parashari_domain_significators(snapshot, mapping)
        if not significators:
            continue
        values = [float(strength_lookup[planet]) for planet in significators]
        raw = sum(values) / len(values) if aggregation == "domain_mean_nonstack" else sum(values)
        contribution = weight * raw
        total += contribution
        domains.append(
            {
                "domain_id": domain_id,
                "behavior_weight": weight,
                "significators": list(significators),
                "significator_strengths": {planet: strength_details[planet] for planet in significators},
                "raw_domain_score": raw,
                "contribution": contribution,
            }
        )
    return {"total": total, "domains": domains}


def _opposite_sign(sign: str) -> str:
    signs = tuple(RULERS)
    return signs[(signs.index(sign) + 6) % 12]
