"""Non-production diagnostics for incompatible readings of BPHS 18.33/34/38/40.

Only symbolic synthetic positions are accepted; no person, ephemeris, outcome,
source weight, marriage forecast, or empirical performance is computed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MODE = Literal["RAHU_IN_FIFTH_OR_NINTH", "RAHU_WITH_BOTH_HOUSE_LORDS"]
CLASSICAL_LORDS = ("Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter")


def house(sign: int, lagna_sign: int) -> int:
    """Inclusive whole-sign house; 0=Aries, 11=Pisces."""
    if not all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x < 12
               for x in (sign, lagna_sign)):
        raise ValueError("Synthetic signs must be integers 0..11")
    return ((sign - lagna_sign) % 12) + 1


def sign_of_house(lagna_sign: int, relative_house: int) -> int:
    if not isinstance(relative_house, int) or not 1 <= relative_house <= 12:
        raise ValueError("Whole-sign house must be 1..12")
    return (lagna_sign + relative_house - 1) % 12


def bphs_18_33_candidate_antecedents(*, lagna_sign: int, positions: dict[str, int],
                                      synthetic: bool = False) -> dict[str, object]:
    """Show rival *editorial* interpretations, NOT an asserted canonical rule."""
    if not synthetic:
        raise ValueError("Source-only diagnostics require synthetic=True")
    for planet in ("Venus", "Rahu"):
        if planet not in positions:
            raise ValueError("Missing synthetic " + planet)
    for planet, sign in positions.items():
        house(sign, lagna_sign)
    lord5 = CLASSICAL_LORDS[sign_of_house(lagna_sign, 5)]
    lord9 = CLASSICAL_LORDS[sign_of_house(lagna_sign, 9)]
    for lord in (lord5, lord9):
        if lord not in positions:
            raise ValueError("Missing synthetic house lord " + lord)
    venus5 = house(positions["Venus"], lagna_sign) == 5
    rahu_house = house(positions["Rahu"], lagna_sign)
    return {
        "Rahu_in_one_of_houses": venus5 and rahu_house in (5, 9),
        "Rahu_conjunct_both_house_lords": venus5 and positions[lord5] == positions[lord9] == positions["Rahu"],
        "house_lords": {"fifth": lord5, "ninth": lord9},
        "source_interpretation_canonical": None,
        "source_only": True,
        "score_allowed": False,
    }


@dataclass(frozen=True)
class Witness:
    verse: str
    reading: str
    interpretation: str
    witness_id: str
    transmission_family: str


def witness_disagreement(witnesses: tuple[Witness, ...]) -> dict[str, object]:
    if not witnesses:
        raise ValueError("Witnesses required")
    if len({w.verse for w in witnesses}) != 1:
        raise ValueError("Compare same verse only")
    if len({w.witness_id for w in witnesses}) != len(witnesses):
        raise ValueError("Duplicate witness id")
    return {
        "verse": witnesses[0].verse,
        "distinct_literal_readings": len({w.reading for w in witnesses}),
        "distinct_interpretations": len({w.interpretation for w in witnesses}),
        "distinct_declared_transmission_families": len({w.transmission_family for w in witnesses}),
        "independent_manuscripts_verified": 0,
        "score_allowed": False,
        "canonical_selection": None,
    }


def event_age_vs_duration(value: int, interpretation: Literal["EVENT_AGE", "DURATION_YEARS"]) -> dict[str, object]:
    if interpretation not in ("EVENT_AGE", "DURATION_YEARS") or not 1 <= value <= 120:
        raise ValueError("Explicit duration-vs-age semantic tag and valid value required")
    return {"value": value, "semantics": interpretation, "score_allowed": False}
