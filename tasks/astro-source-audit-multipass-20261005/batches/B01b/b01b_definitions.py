"""Bounded reference definitions for Robbins/Ptolemy I.9-I.16.

This module does not calculate natal charts, invent orbs, interpret people,
resolve a fixed-star catalogue, or score predictions. Pair tables below are
Robbins's explicit notes, not a substitution by modern reflection formulae.
"""
from __future__ import annotations

import math

SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
ASPECT_BY_DISTANCE = {2: "SEXTILE", 3: "QUARTILE", 4: "TRINE", 6: "OPPOSITION"}
HARMONY = {
    "SEXTILE": "HARMONIOUS", "TRINE": "HARMONIOUS",
    "QUARTILE": "DISHARMONIOUS", "OPPOSITION": "DISHARMONIOUS",
}
COMMANDING_PAIRS = (
    ("Taurus", "Pisces"), ("Gemini", "Aquarius"),
    ("Cancer", "Capricorn"), ("Leo", "Sagittarius"), ("Virgo", "Scorpio"),
)
EQUAL_POWER_PAIRS = (
    ("Gemini", "Leo"), ("Taurus", "Virgo"), ("Aries", "Libra"),
    ("Pisces", "Scorpio"), ("Aquarius", "Sagittarius"),
)
SEASON_QUALITIES = {"spring": "MOIST", "summer": "HOT", "autumn": "DRY", "winter": "COLD"}
REGION_QUALITIES = {"east": "DRY", "south": "HOT", "west": "MOIST", "north": "COLD"}
QUADRANT_POLARITY = {
    "ASC_TO_MC": "MASCULINE_MATUTINAL",
    "MC_TO_DSC": "FEMININE_EVENING",
    "DSC_TO_IC": "MASCULINE_MATUTINAL",
    "IC_TO_ASC": "FEMININE_EVENING",
}
Sign = str | int | None


def sign_index(value: Sign) -> int | None:
    """None is explicitly unknown; bool/floats/wrapped integers are not signs."""
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("Boolean is not a sign index")
    if isinstance(value, int) and 0 <= value < 12:
        return value
    if isinstance(value, str) and value in SIGNS:
        return SIGNS.index(value)
    raise ValueError("Use an exact sign name or an integer in [0, 11]")


def sign_definition(value: Sign) -> dict[str, str] | None:
    index = sign_index(value)
    if index is None:
        return None
    if index in (0, 6):
        category = "EQUINOCTIAL"
    elif index in (3, 9):
        category = "SOLSTITIAL"
    elif index in (1, 4, 7, 10):
        category = "SOLID"
    else:
        category = "BICORPOREAL"
    return {
        "sign": SIGNS[index], "source_class": category,
        "fixed_polarity": "MASCULINE_DIURNAL" if index % 2 == 0 else "FEMININE_NOCTURNAL",
    }


def ascendant_alternating_polarity(value: Sign, ascendant: Sign) -> str | None:
    index, origin = sign_index(value), sign_index(ascendant)
    if index is None or origin is None:
        return None
    # Historical reported alternative; does not combine with the Aries-origin convention.
    return "MASCULINE" if (index - origin) % 2 == 0 else "FEMININE"


def quadrant_polarity(quadrant: str | None) -> str | None:
    """Caller must establish actual quadrant; no zodiac-house shortcut here."""
    if quadrant is None:
        return None
    if quadrant not in QUADRANT_POLARITY:
        raise ValueError("An explicit source quadrant is required")
    return QUADRANT_POLARITY[quadrant]


def sign_relationship(a: Sign, b: Sign) -> dict:
    ia, ib = sign_index(a), sign_index(b)
    if ia is None or ib is None:
        return {
            "status": "UNKNOWN", "distance": None, "listed_aspect": None,
            "commanding_direction": None, "equal_power": None,
            "disjunct": None, "harmony": None, "same_sign": None,
        }
    aa, bb = SIGNS[ia], SIGNS[ib]
    distance = min((ia - ib) % 12, (ib - ia) % 12)
    aspect = ASPECT_BY_DISTANCE.get(distance)
    direction = None
    if (aa, bb) in COMMANDING_PAIRS:
        direction = "A_COMMANDS_B"
    elif (bb, aa) in COMMANDING_PAIRS:
        direction = "B_COMMANDS_A"
    equal_power = (aa, bb) in EQUAL_POWER_PAIRS or (bb, aa) in EQUAL_POWER_PAIRS
    disjunct = distance in (1, 5) and aspect is None and direction is None and not equal_power
    return {
        "status": "KNOWN_SOURCE_SIGN_RELATION", "distance": distance,
        "listed_aspect": aspect, "commanding_direction": direction,
        "equal_power": equal_power, "disjunct": disjunct,
        "harmony": HARMONY.get(aspect), "same_sign": distance == 0,
    }


def seasonal_hour_minutes(daylight_minutes: float | None, *, night: bool = False) -> float | None:
    """Unit conversion only; caller supplies daylight, no solar-event calculation.

    Endpoints 0 and 1440 lack the ordinary alternating day/night prerequisite.
    Reject them instead of manufacturing a polar convention.
    """
    if daylight_minutes is None:
        return None
    if isinstance(daylight_minutes, bool) or not isinstance(daylight_minutes, (int, float)):
        raise ValueError("Daylight must be a finite duration")
    if not math.isfinite(daylight_minutes) or not 0 < daylight_minutes < 1440:
        raise ValueError("An ordinary day/night span is required")
    if not isinstance(night, bool):
        raise ValueError("night must be boolean")
    span = 1440 - daylight_minutes if night else daylight_minutes
    return span / 12
