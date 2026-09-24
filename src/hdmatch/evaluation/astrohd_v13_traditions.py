"""Tradition-grounded AstroHD V1.3 development scorer.

This module implements only the testimony rules frozen before owner scoring in
ASTROHD-V13-SCORING-FREEZE-20260924.json. It deliberately contains no
owner-tuned salience/directness or structural-rarity weights.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import swisseph as swe

from hdmatch.relationship.western import house_for_longitude

PLANETS = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")
BODY_IDS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
}
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
RULERS = {
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
DETRIMENTS = {
    "sun": {"aquarius"},
    "moon": {"capricorn"},
    "mercury": {"sagittarius", "pisces"},
    "venus": {"aries", "scorpio"},
    "mars": {"taurus", "libra"},
    "jupiter": {"gemini", "virgo"},
    "saturn": {"cancer", "leo"},
}
DIURNAL = {"sun", "jupiter", "saturn"}
NOCTURNAL = {"moon", "venus", "mars"}
ANGULAR_HOUSES = {1, 4, 7, 10}
CADENT_HOUSES = {3, 6, 9, 12}
KENDRA = {1, 4, 7, 10}
TRIKONA = {1, 5, 9}
UPACHAYA = {3, 6, 10, 11}
DUSTHANA = {6, 8, 12}
RETRO_STRENGTH_PLANETS = {"mercury", "venus", "mars", "jupiter", "saturn"}
NONLUMINARIES = {"mercury", "venus", "mars", "jupiter", "saturn"}
PLANETARY_JOYS = {
    "mercury": 1,
    "moon": 3,
    "venus": 5,
    "mars": 6,
    "sun": 9,
    "jupiter": 11,
    "saturn": 12,
}


@dataclass(frozen=True, slots=True)
class TraditionSnapshot:
    when: datetime
    tropical_longitudes: dict[str, float]
    tropical_speeds: dict[str, float]
    tropical_ascendant: float
    regio_cusps: tuple[float, ...]
    regio_houses: dict[str, int]
    tropical_whole_houses: dict[str, int]
    day_chart: bool
    sidereal_longitudes: dict[str, float]
    sidereal_speeds: dict[str, float]
    sidereal_ascendant: float
    sidereal_whole_houses: dict[str, int]


def datetime_to_jd(value: datetime) -> float:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    utc = value.astimezone(UTC)
    hour = utc.hour + utc.minute / 60.0 + utc.second / 3600.0 + utc.microsecond / 3.6e9
    return float(swe.julday(utc.year, utc.month, utc.day, hour, swe.GREG_CAL))


def sign_name(longitude: float) -> str:
    return SIGNS[int((longitude % 360.0) // 30.0)]


def whole_sign_house(longitude: float, ascendant: float) -> int:
    planet_sign = int((longitude % 360.0) // 30.0)
    asc_sign = int((ascendant % 360.0) // 30.0)
    return ((planet_sign - asc_sign) % 12) + 1


def whole_sign_house_sign(ascendant: float, house: int) -> str:
    if not 1 <= house <= 12:
        raise ValueError(f"invalid house: {house}")
    asc_sign = int((ascendant % 360.0) // 30.0)
    return SIGNS[(asc_sign + house - 1) % 12]


def build_snapshot(
    when: datetime,
    *,
    latitude: float,
    longitude: float,
    ephemeris_root: Path,
) -> TraditionSnapshot:
    jd = datetime_to_jd(when)
    swe.set_ephe_path(str(ephemeris_root))
    tropical: dict[str, float] = {}
    tropical_speeds: dict[str, float] = {}
    flags = int(swe.FLG_SWIEPH) | int(swe.FLG_SPEED)
    for body, body_id in BODY_IDS.items():
        values, returned = swe.calc_ut(jd, body_id, flags)
        _assert_swiss_file_flags(returned, body=body, when=when)
        tropical[body] = float(values[0]) % 360.0
        tropical_speeds[body] = float(values[3])

    raw_cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b"R", 0)
    regio_cusps = tuple(float(x) % 360.0 for x in raw_cusps[:12])
    tropical_asc = float(ascmc[0]) % 360.0
    regio_houses = {
        body: house_for_longitude(value, regio_cusps) for body, value in tropical.items()
    }
    whole_tropical = {
        body: whole_sign_house(value, tropical_asc) for body, value in tropical.items()
    }
    day_chart = regio_houses["sun"] in {7, 8, 9, 10, 11, 12}

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    sidereal: dict[str, float] = {}
    sidereal_speeds: dict[str, float] = {}
    sid_flags = flags | int(swe.FLG_SIDEREAL)
    for body, body_id in BODY_IDS.items():
        values, returned = swe.calc_ut(jd, body_id, sid_flags)
        _assert_swiss_file_flags(returned, body=body, when=when)
        sidereal[body] = float(values[0]) % 360.0
        sidereal_speeds[body] = float(values[3])
    _cusps_sid, ascmc_sid = swe.houses_ex(jd, latitude, longitude, b"P", int(swe.FLG_SIDEREAL))
    sidereal_asc = float(ascmc_sid[0]) % 360.0
    whole_sidereal = {
        body: whole_sign_house(value, sidereal_asc) for body, value in sidereal.items()
    }

    return TraditionSnapshot(
        when=when,
        tropical_longitudes=tropical,
        tropical_speeds=tropical_speeds,
        tropical_ascendant=tropical_asc,
        regio_cusps=regio_cusps,
        regio_houses=regio_houses,
        tropical_whole_houses=whole_tropical,
        day_chart=day_chart,
        sidereal_longitudes=sidereal,
        sidereal_speeds=sidereal_speeds,
        sidereal_ascendant=sidereal_asc,
        sidereal_whole_houses=whole_sidereal,
    )


def _assert_swiss_file_flags(returned: int, *, body: str, when: datetime) -> None:
    if returned & int(swe.FLG_MOSEPH) or not returned & int(swe.FLG_SWIEPH):
        raise RuntimeError(
            f"Swiss Ephemeris fallback for {body} at {when.isoformat()}: returned_flags={returned}"
        )


def _add_once(store: dict[str, int], key: str, value: int) -> None:
    old = store.get(key)
    if old is not None and old != value:
        raise RuntimeError(f"contradictory testimony for {key}: {old} vs {value}")
    store[key] = value


def _hellenistic_planet_testimonies(snapshot: TraditionSnapshot, planet: str) -> dict[str, int]:
    out: dict[str, int] = {}
    sign = sign_name(snapshot.tropical_longitudes[planet])
    house = snapshot.tropical_whole_houses[planet]
    if RULERS[sign] == planet:
        _add_once(out, f"{planet}:domicile", 1)
    if EXALTATIONS[planet] == sign:
        _add_once(out, f"{planet}:exaltation", 1)
    if house == PLANETARY_JOYS[planet]:
        _add_once(out, f"{planet}:joy_house", 1)
    if planet in DIURNAL and snapshot.day_chart:
        _add_once(out, f"{planet}:sect", 1)
    if planet in NOCTURNAL and not snapshot.day_chart:
        _add_once(out, f"{planet}:sect", 1)
    return out


def _lilly_planet_testimonies(snapshot: TraditionSnapshot, planet: str) -> dict[str, int]:
    out: dict[str, int] = {}
    sign = sign_name(snapshot.tropical_longitudes[planet])
    house = snapshot.regio_houses[planet]
    speed = snapshot.tropical_speeds[planet]
    if RULERS[sign] == planet:
        _add_once(out, f"{planet}:own_sign", 1)
    if EXALTATIONS[planet] == sign:
        _add_once(out, f"{planet}:exaltation", 1)
    if sign in DETRIMENTS[planet]:
        _add_once(out, f"{planet}:detriment", -1)
    if FALLS[planet] == sign:
        _add_once(out, f"{planet}:fall", -1)
    if planet in NONLUMINARIES:
        if speed >= 0.0:
            _add_once(out, f"{planet}:direct", 1)
        else:
            _add_once(out, f"{planet}:retrograde", -1)
    if house in ANGULAR_HOUSES:
        _add_once(out, f"{planet}:angular_house", 1)
    elif house in CADENT_HOUSES:
        _add_once(out, f"{planet}:cadent_house", -1)
    return out


def _parashari_planet_testimonies(snapshot: TraditionSnapshot, planet: str) -> dict[str, int]:
    out: dict[str, int] = {}
    sign = sign_name(snapshot.sidereal_longitudes[planet])
    house = snapshot.sidereal_whole_houses[planet]
    speed = snapshot.sidereal_speeds[planet]
    if RULERS[sign] == planet:
        _add_once(out, f"{planet}:own_sign", 1)
    if EXALTATIONS[planet] == sign:
        _add_once(out, f"{planet}:exaltation", 1)
    if FALLS[planet] == sign:
        _add_once(out, f"{planet}:debilitation", -1)
    if house in KENDRA:
        _add_once(out, f"{planet}:kendra", 1)
    if house in TRIKONA:
        _add_once(out, f"{planet}:trikona", 1)
    if house in UPACHAYA:
        _add_once(out, f"{planet}:upachaya", 1)
    if house in DUSTHANA:
        _add_once(out, f"{planet}:dusthana", -1)
    if planet in RETRO_STRENGTH_PLANETS and speed < 0.0:
        _add_once(out, f"{planet}:retrograde_strength", 1)
    return out


def _mapped_house_lord(snapshot: TraditionSnapshot, tradition: str, house: int) -> str:
    if tradition == "hellenistic_western":
        sign = whole_sign_house_sign(snapshot.tropical_ascendant, house)
    elif tradition == "lilly_traditional_western":
        sign = sign_name(snapshot.regio_cusps[house - 1])
    elif tradition == "parashari_jyotish":
        sign = whole_sign_house_sign(snapshot.sidereal_ascendant, house)
    else:
        raise ValueError(f"unknown tradition: {tradition}")
    return RULERS[sign]


def tradition_domain_testimonies(
    snapshot: TraditionSnapshot,
    *,
    tradition: str,
    planets: list[str],
    houses: list[int],
) -> dict[str, int]:
    out: dict[str, int] = {}
    if tradition == "hellenistic_western":
        fn = _hellenistic_planet_testimonies
    elif tradition == "lilly_traditional_western":
        fn = _lilly_planet_testimonies
    elif tradition == "parashari_jyotish":
        fn = _parashari_planet_testimonies
    else:
        raise ValueError(f"unknown tradition: {tradition}")

    for planet in planets:
        for key, value in fn(snapshot, planet).items():
            _add_once(out, key, value)
    for house in houses:
        lord = _mapped_house_lord(snapshot, tradition, int(house))
        for key, value in fn(snapshot, lord).items():
            _add_once(out, key, value)
    return out


def score_snapshot(
    snapshot: TraditionSnapshot,
    *,
    consensus_map: dict[str, Any],
    behavior_weights: dict[str, float],
) -> dict[str, Any]:
    domain_rows: list[dict[str, Any]] = []
    totals = {
        "domain_collapse_nonstack": 0.0,
        "cross_tradition_convergence_stack": 0.0,
        "raw_independent_testimony_stack": 0.0,
    }
    for domain in consensus_map["domains"]:
        domain_id = str(domain["domain_id"])
        weight = float(behavior_weights.get(domain_id, 0.0))
        traditions = []
        raw_total = 0
        tradition_sign_sum = 0
        for mapping in domain["traditions"]:
            tradition = str(mapping["tradition"])
            planets = [str(x["id"]) for x in mapping.get("planets", [])]
            houses = [int(x["id"]) for x in mapping.get("houses", [])]
            if not planets and not houses:
                traditions.append(
                    {
                        "tradition": tradition,
                        "raw_net": 0,
                        "sign": 0,
                        "testimonies": {},
                        "mapped": False,
                    }
                )
                continue
            testimonies = tradition_domain_testimonies(
                snapshot,
                tradition=tradition,
                planets=planets,
                houses=houses,
            )
            raw = sum(testimonies.values())
            has_positive = any(value > 0 for value in testimonies.values())
            has_negative = any(value < 0 for value in testimonies.values())
            sign = (
                1
                if has_positive and not has_negative
                else -1
                if has_negative and not has_positive
                else 0
            )
            raw_total += raw
            tradition_sign_sum += sign
            traditions.append(
                {
                    "tradition": tradition,
                    "raw_net": raw,
                    "sign": sign,
                    "testimonies": testimonies,
                    "mapped": True,
                }
            )
        all_testimonies = [
            value
            for row in traditions
            for value in row["testimonies"].values()
        ]
        has_positive = any(value > 0 for value in all_testimonies)
        has_negative = any(value < 0 for value in all_testimonies)
        collapse = (
            1
            if has_positive and not has_negative
            else -1
            if has_negative and not has_positive
            else 0
        )
        votes = {
            "domain_collapse_nonstack": collapse,
            "cross_tradition_convergence_stack": tradition_sign_sum,
            "raw_independent_testimony_stack": raw_total,
        }
        for arm, vote in votes.items():
            totals[arm] += weight * vote
        domain_rows.append(
            {
                "domain_id": domain_id,
                "behavior_weight": weight,
                "votes": votes,
                "traditions": traditions,
            }
        )
    return {"totals": totals, "domains": domain_rows}


def behavior_weight_variants(
    behavior: dict[str, Any],
    crosswalk: dict[str, Any],
) -> dict[str, dict[str, float]]:
    cluster_to_domain = {
        str(row["historical_cluster"]): str(row["neutral_domain"])
        for row in crosswalk["historical_merged_cluster_crosswalk"]
    }
    equal: dict[str, float] = {}
    confidence: dict[str, float] = {}
    for row in behavior["translations"]:
        cluster = str(row["historical_cluster"])
        domain = cluster_to_domain[cluster]
        value = float(row.get("behavioral_confidence", 0.0))
        if row.get("relation") != "supported" or value <= 0.0:
            continue
        equal[domain] = 1.0
        confidence[domain] = value
    return {
        "equal_domain": equal,
        "frozen_measurement_confidence": confidence,
    }
