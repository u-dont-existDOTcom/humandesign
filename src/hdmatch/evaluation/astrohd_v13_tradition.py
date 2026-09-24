"""Source-grounded testimony scoring for AstroHD V1.3 development experiments.

This module implements only the testimony rules frozen in
ASTROHD-V13-SCORING-FREEZE-20260924.json. It contains no owner-case
feature selection or candidate-dependent tuning.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

SIGNS = (
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
)

CLASSICAL_RULERS = {
    "aries": "mars",
    "taurus": "venus",
    "gemini": "mercury",
    "cancer": "moon",
    "leo": "sun",
    "virgo": "mercury",
    "libra": "venus",
    "scorpio": "mars",
    "sagittarius": "jupiter",
    "capricorn": "saturn",
    "aquarius": "saturn",
    "pisces": "jupiter",
}

DOMICILES: dict[str, frozenset[str]] = {
    body: frozenset(sign for sign, ruler in CLASSICAL_RULERS.items() if ruler == body)
    for body in {"sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"}
}

EXALTATIONS = {
    "sun": "aries",
    "moon": "taurus",
    "mercury": "virgo",
    "venus": "pisces",
    "mars": "capricorn",
    "jupiter": "cancer",
    "saturn": "libra",
}

FALLS = {
    "sun": "libra",
    "moon": "scorpio",
    "mercury": "pisces",
    "venus": "virgo",
    "mars": "cancer",
    "jupiter": "capricorn",
    "saturn": "aries",
}

DAY_SECT = frozenset({"sun", "jupiter", "saturn"})
NIGHT_SECT = frozenset({"moon", "venus", "mars"})
ANGULAR_HOUSES = frozenset({1, 4, 7, 10})
LILLY_POSITIVE_HOUSES = frozenset({1, 2, 3, 4, 5, 7, 9, 10, 11})
LILLY_NEGATIVE_HOUSES = frozenset({6, 8, 12})
JYOTISH_KENDRA = frozenset({1, 4, 7, 10})
JYOTISH_TRIKONA = frozenset({1, 5, 9})
RETROGRADE_CAPABLE = frozenset({"mercury", "venus", "mars", "jupiter", "saturn"})


@dataclass(frozen=True, slots=True)
class Snapshot:
    tropical_longitudes: Mapping[str, float]
    tropical_speeds: Mapping[str, float]
    tropical_regio_houses: Mapping[str, int]
    tropical_regio_cusps: Sequence[float]
    tropical_ascendant: float
    sidereal_longitudes: Mapping[str, float]
    sidereal_speeds: Mapping[str, float]
    sidereal_ascendant: float
    is_day_chart: bool


@dataclass(frozen=True, slots=True)
class TraditionDomainEvidence:
    tradition: str
    domain_id: str
    positive: tuple[str, ...]
    negative: tuple[str, ...]

    @property
    def net(self) -> int:
        return len(self.positive) - len(self.negative)

    @property
    def sign(self) -> int:
        return (self.net > 0) - (self.net < 0)


def sign_name(longitude: float) -> str:
    return SIGNS[int((longitude % 360.0) // 30.0)]


def sign_index(longitude: float) -> int:
    return int((longitude % 360.0) // 30.0)


def whole_sign_house(longitude: float, ascendant: float) -> int:
    return ((sign_index(longitude) - sign_index(ascendant)) % 12) + 1


def opposite_sign(sign: str) -> str:
    return SIGNS[(SIGNS.index(sign) + 6) % 12]


def in_domicile(body: str, longitude: float) -> bool:
    return sign_name(longitude) in DOMICILES[body]


def in_detriment(body: str, longitude: float) -> bool:
    return any(sign_name(longitude) == opposite_sign(home) for home in DOMICILES[body])


def in_exaltation(body: str, longitude: float) -> bool:
    return sign_name(longitude) == EXALTATIONS[body]


def in_fall(body: str, longitude: float) -> bool:
    return sign_name(longitude) == FALLS[body]


def classical_lord_of_longitude(longitude: float) -> str:
    return CLASSICAL_RULERS[sign_name(longitude)]


def classical_lord_of_whole_sign_house(ascendant: float, house: int) -> str:
    sign = SIGNS[(sign_index(ascendant) + house - 1) % 12]
    return CLASSICAL_RULERS[sign]


def evaluate_domain(
    *,
    domain_id: str,
    tradition_mapping: Mapping[str, Any],
    snapshot: Snapshot,
) -> TraditionDomainEvidence:
    tradition = str(tradition_mapping["tradition"])
    planets = tuple(_mapped_ids(tradition_mapping.get("planets", ())))
    houses = tuple(int(value) for value in _mapped_ids(tradition_mapping.get("houses", ())))

    if tradition == "hellenistic_western":
        return _evaluate_hellenistic(domain_id, planets, houses, snapshot)
    if tradition == "lilly_traditional_western":
        return _evaluate_lilly(domain_id, planets, houses, snapshot)
    if tradition == "parashari_jyotish":
        return _evaluate_parashari(domain_id, planets, houses, snapshot)
    raise ValueError(f"unsupported tradition: {tradition}")


def score_candidate(
    *,
    snapshot: Snapshot,
    consensus_map: Mapping[str, Any],
    behavioral_confidence: Mapping[str, float],
) -> dict[str, float]:
    domain_rows = []
    for domain in consensus_map["domains"]:
        domain_id = str(domain["domain_id"])
        confidence = float(behavioral_confidence.get(domain_id, 0.0))
        if confidence <= 0.0:
            continue
        evidence = [
            evaluate_domain(
                domain_id=domain_id,
                tradition_mapping=tradition,
                snapshot=snapshot,
            )
            for tradition in domain["traditions"]
            if not bool(tradition.get("consensus_abstain", False))
        ]
        if not evidence:
            continue
        raw_net = sum(item.net for item in evidence)
        domain_collapse = (raw_net > 0) - (raw_net < 0)
        convergence = sum(item.sign for item in evidence)
        raw_stack = raw_net
        domain_rows.append(
            {
                "domain_id": domain_id,
                "confidence": confidence,
                "domain_collapse": domain_collapse,
                "convergence": convergence,
                "raw_stack": raw_stack,
            }
        )

    scores: dict[str, float] = {}
    for weighting in ("equal", "confidence"):
        use_confidence = weighting == "confidence"
        scores[f"domain_collapse_nonstack__{weighting}"] = sum(
            (float(row["confidence"]) if use_confidence else 1.0)
            * int(row["domain_collapse"])
            for row in domain_rows
        )
        scores[f"cross_tradition_convergence_stack__{weighting}"] = sum(
            (float(row["confidence"]) if use_confidence else 1.0)
            * int(row["convergence"])
            for row in domain_rows
        )
        scores[f"raw_independent_testimony_stack__{weighting}"] = sum(
            (float(row["confidence"]) if use_confidence else 1.0)
            * int(row["raw_stack"])
            for row in domain_rows
        )
    return scores


def score_candidate_detailed(
    *,
    snapshot: Snapshot,
    consensus_map: Mapping[str, Any],
    behavioral_confidence: Mapping[str, float],
) -> dict[str, Any]:
    domains = []
    for domain in consensus_map["domains"]:
        domain_id = str(domain["domain_id"])
        confidence = float(behavioral_confidence.get(domain_id, 0.0))
        if confidence <= 0.0:
            continue
        evidence = [
            evaluate_domain(
                domain_id=domain_id,
                tradition_mapping=tradition,
                snapshot=snapshot,
            )
            for tradition in domain["traditions"]
            if not bool(tradition.get("consensus_abstain", False))
        ]
        if not evidence:
            continue
        raw_net = sum(item.net for item in evidence)
        domains.append(
            {
                "domain_id": domain_id,
                "behavioral_confidence": confidence,
                "traditions": [
                    {
                        "tradition": item.tradition,
                        "positive": list(item.positive),
                        "negative": list(item.negative),
                        "net": item.net,
                        "sign": item.sign,
                    }
                    for item in evidence
                ],
                "domain_collapse_vote": (raw_net > 0) - (raw_net < 0),
                "cross_tradition_vote": sum(item.sign for item in evidence),
                "raw_testimony_vote": raw_net,
            }
        )
    return {
        "scores": score_candidate(
            snapshot=snapshot,
            consensus_map=consensus_map,
            behavioral_confidence=behavioral_confidence,
        ),
        "domains": domains,
    }


def _evaluate_hellenistic(
    domain_id: str,
    planets: Sequence[str],
    houses: Sequence[int],
    snapshot: Snapshot,
) -> TraditionDomainEvidence:
    positive: list[str] = []
    negative: list[str] = []
    for body in planets:
        longitude = float(snapshot.tropical_longitudes[body])
        house = whole_sign_house(longitude, snapshot.tropical_ascendant)
        if in_domicile(body, longitude):
            positive.append(f"{body}:domicile")
        if in_exaltation(body, longitude):
            positive.append(f"{body}:exaltation")
        if body in (DAY_SECT if snapshot.is_day_chart else NIGHT_SECT):
            positive.append(f"{body}:sect")
        if house in ANGULAR_HOUSES:
            positive.append(f"{body}:whole_sign_angular")
        if in_fall(body, longitude):
            negative.append(f"{body}:fall")
    for house in houses:
        lord = classical_lord_of_whole_sign_house(snapshot.tropical_ascendant, house)
        longitude = float(snapshot.tropical_longitudes[lord])
        lord_house = whole_sign_house(longitude, snapshot.tropical_ascendant)
        if in_domicile(lord, longitude):
            positive.append(f"house{house}_lord:{lord}:domicile")
        if in_exaltation(lord, longitude):
            positive.append(f"house{house}_lord:{lord}:exaltation")
        if lord_house in ANGULAR_HOUSES:
            positive.append(f"house{house}_lord:{lord}:whole_sign_angular")
        if in_fall(lord, longitude):
            negative.append(f"house{house}_lord:{lord}:fall")
    return TraditionDomainEvidence(
        "hellenistic_western", domain_id, tuple(positive), tuple(negative)
    )


def _evaluate_lilly(
    domain_id: str,
    planets: Sequence[str],
    houses: Sequence[int],
    snapshot: Snapshot,
) -> TraditionDomainEvidence:
    positive: list[str] = []
    negative: list[str] = []
    for body in planets:
        _append_lilly_planet_testimonies(body, positive, negative, snapshot, prefix=body)
    for house in houses:
        cusp = float(snapshot.tropical_regio_cusps[house - 1])
        lord = classical_lord_of_longitude(cusp)
        _append_lilly_planet_testimonies(
            lord,
            positive,
            negative,
            snapshot,
            prefix=f"house{house}_lord:{lord}",
        )
    return TraditionDomainEvidence(
        "lilly_traditional_western", domain_id, tuple(positive), tuple(negative)
    )


def _append_lilly_planet_testimonies(
    body: str,
    positive: list[str],
    negative: list[str],
    snapshot: Snapshot,
    *,
    prefix: str,
) -> None:
    longitude = float(snapshot.tropical_longitudes[body])
    house = int(snapshot.tropical_regio_houses[body])
    speed = float(snapshot.tropical_speeds[body])
    if in_domicile(body, longitude):
        positive.append(f"{prefix}:domicile")
    if in_exaltation(body, longitude):
        positive.append(f"{prefix}:exaltation")
    if speed >= 0:
        positive.append(f"{prefix}:direct")
    elif body in RETROGRADE_CAPABLE:
        negative.append(f"{prefix}:retrograde")
    if house in LILLY_POSITIVE_HOUSES:
        positive.append(f"{prefix}:positive_house:{house}")
    if in_detriment(body, longitude):
        negative.append(f"{prefix}:detriment")
    if in_fall(body, longitude):
        negative.append(f"{prefix}:fall")
    if house in LILLY_NEGATIVE_HOUSES:
        negative.append(f"{prefix}:negative_house:{house}")


def _evaluate_parashari(
    domain_id: str,
    planets: Sequence[str],
    houses: Sequence[int],
    snapshot: Snapshot,
) -> TraditionDomainEvidence:
    positive: list[str] = []
    negative: list[str] = []
    # The target-blind consensus currently admits house mappings only for this
    # tradition. Planet support is implemented conservatively for future maps.
    for body in planets:
        _append_jyotish_planet_testimonies(body, positive, negative, snapshot, prefix=body)
    for house in houses:
        lord = classical_lord_of_whole_sign_house(snapshot.sidereal_ascendant, house)
        _append_jyotish_planet_testimonies(
            lord,
            positive,
            negative,
            snapshot,
            prefix=f"house{house}_lord:{lord}",
        )
    return TraditionDomainEvidence(
        "parashari_jyotish", domain_id, tuple(positive), tuple(negative)
    )


def _append_jyotish_planet_testimonies(
    body: str,
    positive: list[str],
    negative: list[str],
    snapshot: Snapshot,
    *,
    prefix: str,
) -> None:
    longitude = float(snapshot.sidereal_longitudes[body])
    house = whole_sign_house(longitude, snapshot.sidereal_ascendant)
    speed = float(snapshot.sidereal_speeds[body])
    if in_domicile(body, longitude):
        positive.append(f"{prefix}:own_sign")
    if in_exaltation(body, longitude):
        positive.append(f"{prefix}:exaltation")
    if house in JYOTISH_KENDRA:
        positive.append(f"{prefix}:kendra:{house}")
    if house in JYOTISH_TRIKONA:
        positive.append(f"{prefix}:trikona:{house}")
    if body in RETROGRADE_CAPABLE and speed < 0:
        positive.append(f"{prefix}:retrograde_strength")
    if in_fall(body, longitude):
        negative.append(f"{prefix}:debilitation")


def _mapped_ids(values: Sequence[Any]) -> tuple[Any, ...]:
    result = []
    for value in values:
        if isinstance(value, Mapping):
            result.append(value["id"])
        else:
            result.append(value)
    return tuple(result)
