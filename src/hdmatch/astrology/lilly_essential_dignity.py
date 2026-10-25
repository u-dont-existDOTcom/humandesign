"""Partial first-edition Lilly (1647) essential-dignity arithmetic.

Only explicitly tabled zodiacal components. NOT a full natal strength,
full reception/accidental assessment, or human predictive model.
Table references: Christian Astrology 1647 pp.101-105, 115, and
directions p.654-655; source images are versioned in research docs.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from .sky import DirectionBirthSnapshot

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
CLASSICAL = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")
DOMICILE = {
    "sun": (4,),
    "moon": (3,),
    "mercury": (2, 5),
    "venus": (1, 6),
    "mars": (0, 7),
    "jupiter": (8, 11),
    "saturn": (9, 10),
}
EXALTATION = {
    "sun": 0,
    "moon": 1,
    "mercury": 5,
    "venus": 11,
    "mars": 9,
    "jupiter": 3,
    "saturn": 6,
}
TRIPLICITY_DAY = (
    "sun",
    "venus",
    "saturn",
    "mars",
    "sun",
    "venus",
    "saturn",
    "mars",
    "sun",
    "venus",
    "saturn",
    "mars",
)
TRIPLICITY_NIGHT = (
    "jupiter",
    "moon",
    "mercury",
    "mars",
    "jupiter",
    "moon",
    "mercury",
    "mars",
    "jupiter",
    "moon",
    "mercury",
    "mars",
)
# (exclusive upper degree, ruling planet). Table labels terms "according
# to Ptolomy"; DO NOT conflate literal 1647 rows with a separate Tetrabiblos
# recension or later reconstructed Egyptian terms.
TERMS = (
    ((6, "jupiter"), (14, "venus"), (21, "mercury"), (26, "mars"), (30, "saturn")),
    ((8, "venus"), (15, "mercury"), (22, "jupiter"), (26, "saturn"), (30, "mars")),
    ((7, "mercury"), (14, "jupiter"), (21, "venus"), (25, "saturn"), (30, "mars")),
    ((6, "mars"), (13, "jupiter"), (20, "mercury"), (27, "venus"), (30, "saturn")),
    ((6, "saturn"), (13, "mercury"), (19, "venus"), (25, "jupiter"), (30, "mars")),
    ((7, "mercury"), (13, "venus"), (18, "jupiter"), (24, "saturn"), (30, "mars")),
    ((6, "saturn"), (11, "venus"), (19, "jupiter"), (24, "mercury"), (30, "mars")),
    ((6, "mars"), (14, "jupiter"), (21, "venus"), (27, "mercury"), (30, "saturn")),
    ((8, "jupiter"), (14, "venus"), (19, "mercury"), (25, "saturn"), (30, "mars")),
    ((6, "venus"), (12, "mercury"), (19, "jupiter"), (25, "mars"), (30, "saturn")),
    ((6, "saturn"), (12, "mercury"), (20, "venus"), (25, "jupiter"), (30, "mars")),
    ((8, "venus"), (14, "jupiter"), (20, "mercury"), (26, "mars"), (30, "saturn")),
)
FACES = (
    ("mars", "sun", "venus"),
    ("mercury", "moon", "saturn"),
    ("jupiter", "mars", "sun"),
    ("venus", "mercury", "moon"),
    ("saturn", "jupiter", "mars"),
    ("sun", "venus", "mercury"),
    ("moon", "saturn", "jupiter"),
    ("mars", "sun", "venus"),
    ("mercury", "moon", "saturn"),
    ("jupiter", "mars", "sun"),
    ("venus", "mercury", "moon"),
    ("saturn", "jupiter", "mars"),
)
SOURCE_POINTS = {
    "domicile": 5,
    "exaltation": 4,
    "triplicity": 3,
    "term": 2,
    "face": 1,
    "detriment": -5,
    "fall": -4,
    "peregrine": -5,
}


@dataclass(frozen=True, slots=True)
class EssentialComponents:
    planet: str
    zodiac_sign: str
    sign_index: int
    within_sign_degrees: float
    chart_sect: str
    table_term_ruler: str
    table_face_ruler: str
    dignities_present: tuple[str, ...]
    debilities_present: tuple[str, ...]
    positive_points: int
    negative_points: int
    partial_net_points: int
    full_natal_strength: str = "UNRESOLVED_RECEPTION_ACCIDENTALS_AND_CONTEXT"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def table_integrity() -> None:
    """Mechanical checks of the manually transcribed original 12-sign table."""
    if len(SIGNS) != len(TERMS) or len(FACES) != len(SIGNS):
        raise ValueError("1647 table does not contain twelve complete sign rows")
    if set(DOMICILE) != set(CLASSICAL) or set(EXALTATION) != set(CLASSICAL):
        raise ValueError("classical domicile/exaltation registry incomplete")
    for sign in range(12):
        row = TERMS[sign]
        upper = 0
        seen = set()
        for next_upper, ruler in row:
            if next_upper <= upper or ruler not in CLASSICAL or ruler in seen:
                raise ValueError("term row is not a strict five-planet partition")
            upper = next_upper
            seen.add(ruler)
        if upper != 30 or len(row) != 5 or len(FACES[sign]) != 3:
            raise ValueError("sign does not cover all 30 degrees")
        if any(ruler not in CLASSICAL for ruler in FACES[sign]):
            raise ValueError("face ruler is not classical")
    if sum(len(signs) for signs in DOMICILE.values()) != 12:
        raise ValueError("domicile sign ownership not exactly complete")


def term_ruler(sign: int, degree: float) -> str:
    if not 0 <= sign < 12 or not math.isfinite(degree) or not 0 <= degree < 30:
        raise ValueError("term requires sign 0-11 and within-sign degree [0,30)")
    for upper, ruler in TERMS[sign]:
        if degree < upper:
            return ruler
    raise AssertionError("term table has an uncovered interval")


def essential_components(
    planet: str, tropical_longitude_deg: float, *, is_day_chart: bool
) -> EssentialComponents:
    """Visible point factors only; reception and accidental fortitudes omitted."""
    if planet not in CLASSICAL:
        raise ValueError("only seven classical natal planets have source table rows")
    if not math.isfinite(tropical_longitude_deg):
        raise ValueError("ecliptic longitude must be finite")
    lon = tropical_longitude_deg % 360.0
    sign = int(lon // 30)
    degree = lon - 30 * sign
    trip_ruler = TRIPLICITY_DAY[sign] if is_day_chart else TRIPLICITY_NIGHT[sign]
    terms = term_ruler(sign, degree)
    face = FACES[sign][int(degree // 10)]
    positive = []
    if sign in DOMICILE[planet]:
        positive.append("domicile")
    if sign == EXALTATION[planet]:
        positive.append("exaltation")
    if planet == trip_ruler:
        positive.append("triplicity")
    if planet == terms:
        positive.append("term")
    if planet == face:
        positive.append("face")
    negative = []
    if any(sign == (d + 6) % 12 for d in DOMICILE[planet]):
        negative.append("detriment")
    if sign == (EXALTATION[planet] + 6) % 12:
        negative.append("fall")
    if not positive:
        negative.append("peregrine")
    plus = sum(SOURCE_POINTS[label] for label in positive)
    minus = sum(SOURCE_POINTS[label] for label in negative)
    return EssentialComponents(
        planet=planet,
        zodiac_sign=SIGNS[sign],
        sign_index=sign,
        within_sign_degrees=round(degree, 12),
        chart_sect="day" if is_day_chart else "night",
        table_term_ruler=terms,
        table_face_ruler=face,
        dignities_present=tuple(positive),
        debilities_present=tuple(negative),
        positive_points=plus,
        negative_points=minus,
        partial_net_points=plus + minus,
    )


def natal_sun_altitude_deg(snapshot: DirectionBirthSnapshot) -> float:
    """Modern geometric horizon model for Lilly's day/night triplicities.

    Uses apparent geocentric equatorial Sun and local RAMC. The 1647 table
    specifies day/night but not this precise astronomical implementation.
    Refraction/topocentric corrections are explicitly outside scope.
    """
    points = snapshot.lookup()
    if "sun" not in points:
        raise ValueError("missing natal Sun equatorial state")
    sun = points["sun"]
    lat = math.radians(snapshot.latitude_deg)
    dec = math.radians(sun.dec_deg)
    h = math.radians((snapshot.ramc_deg - sun.ra_deg + 180.0) % 360.0 - 180.0)
    sin_alt = math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(h)
    return math.degrees(math.asin(max(-1.0, min(1.0, sin_alt))))


def source_visible_natal_components(
    snapshot: DirectionBirthSnapshot,
) -> tuple[EssentialComponents, ...]:
    """For the seven planets; never infer full radix strength from this."""
    altitude = natal_sun_altitude_deg(snapshot)
    # The exact horizon instant needs a separate sect-convention policy.
    if abs(altitude) <= 1e-8:
        raise ValueError("sun exactly at the horizon: sect unresolved")
    ecl = snapshot.ecliptic_lookup()
    missing = set(CLASSICAL) - set(ecl)
    if missing:
        raise ValueError(f"missing natal ecliptic states: {sorted(missing)}")
    return tuple(
        essential_components(body, ecl[body][0], is_day_chart=altitude > 0) for body in CLASSICAL
    )


# Lilly 1647 p.115: positional ONLY part of accidental points, no reception,
# speed, retrograde, combustion, aspects, visibility or full chart judgment.
HOUSE_POSITION_POINTS = {
    1: 5,
    10: 5,
    7: 4,
    4: 4,
    11: 4,
    2: 3,
    5: 3,
    9: 2,
    3: 1,
    12: -5,
    8: -2,
    6: -2,
}
ANGULAR_HOUSES = frozenset((1, 4, 7, 10))


def house_component(house_number: int) -> tuple[int, bool]:
    """First-edition Lilly house-position table only (pp.103,115)."""
    if not isinstance(house_number, int) or house_number not in HOUSE_POSITION_POINTS:
        raise ValueError("house must be an integer 1 through 12")
    return HOUSE_POSITION_POINTS[house_number], house_number in ANGULAR_HOUSES


def swiss_placidus_house(
    snapshot: DirectionBirthSnapshot,
    planet: str,
) -> tuple[int, float, int, bool]:
    """Modern Swiss house-position reconstruction, NOT full Lilly/Argolus.

    House location counts as one partial accidental indicator, not enough
    to determine whether Lilly's directed Jupiter is strong in radix.
    """
    import importlib

    swe = importlib.import_module("swisseph")

    if planet not in CLASSICAL:
        raise ValueError("only classical natal planetary houses are considered")
    if snapshot.true_obliquity_deg is None:
        raise ValueError("true obliquity not available")
    states = snapshot.ecliptic_lookup()
    if planet not in states:
        raise ValueError("planetary latitude/longitude is not available")
    longitude, latitude = states[planet]
    position = float(
        swe.house_pos(
            snapshot.ramc_deg,
            snapshot.latitude_deg,
            snapshot.true_obliquity_deg,
            (longitude, latitude),
            b"P",
        )
    )
    if not math.isfinite(position) or not 1.0 <= position < 13.0:
        raise ValueError("Swiss Placidus house position outside valid domain")
    house = int(math.floor(position))
    points, angular = house_component(house)
    return house, position, points, angular
