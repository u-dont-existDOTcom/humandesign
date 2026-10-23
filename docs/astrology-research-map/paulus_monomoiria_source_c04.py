"""Source-only reconstruction of the *printed corrected* Paulus monomoiria canon.

Paulus Alexandrinus Introductory Matters ch. 32 in Dorian Greenbaum's
'Late Classical Astrology', printed page 67 / PDF leaf 83. The reproduced
table is labelled D for diurnal. Its printed entries are a seven-star
cyclic arrangement, repeated across 30 degrees in four trigons.

This reconstructs an edition's observed *daytime* table, NOT the original
autograph, a night rule, a 10-degree decan, a chart calculator, or an
empirically valid prediction. Greenbaum's notes (pp. 66, 68-70) identify
conflicting table/scholion readings; a conflicting scholion explicitly
associates Venus with the 8th degree of Cancer, while the reproduced canon
assigns Mars. Both witnesses remain distinct and must not be fitted
against a biography.
"""
from __future__ import annotations

from dataclasses import dataclass

PLANET_CYCLE: tuple[str, ...] = (
    "Sun", "Jupiter", "Venus", "Moon", "Saturn", "Mercury", "Mars"
)

TRIPLICITIES: dict[str, tuple[int, ...]] = {
    "fire": (0, 4, 8),   # Aries Leo Sagittarius
    "earth": (1, 5, 9), # Taurus Virgo Capricorn
    "air": (2, 6, 10),  # Gemini Libra Aquarius
    "water": (3, 7, 11),# Cancer Scorpio Pisces
}

# Directly inspected headings, first degree of each column, printed p. 67.
PRINTED_DIURNAL_FIRST: dict[str, str] = {
    "fire": "Sun",
    "earth": "Venus",
    "air": "Saturn",
    "water": "Mars",
}
ZODIAC: tuple[str, ...] = (
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
)


@dataclass(frozen=True)
class SourceChoice:
    name: str
    edition: str
    source_page: str
    status: str


CANON = SourceChoice(
    "GREENBAUM_PRINTED_CORRECTED_DAY_TABLE",
    "Paulus Alexandrinus/Greenbaum, Late Classical Astrology",
    "Introductory Matters ch32 p67, PDF leaf 83",
    "EDITORIAL_RECONSTRUCTION_SOURCE_ONLY",
)
EXAMPLE_VARIANT = SourceChoice(
    "OLYMPIODORAN_SCHOLION_87_CANCER_8_VENUS",
    "Greenbaum's included scholion and editorial comparison",
    "printed p69, PDF leaf 85",
    "DISPUTED_EXAMPLE_NOT_A_GENERAL_NIGHT_TABLE",
)


def triplicity_for_sign(sign: str) -> str:
    if sign not in ZODIAC:
        raise ValueError("sign must match a canonical zodiac sign")
    idx = ZODIAC.index(sign)
    return next(k for k, members in TRIPLICITIES.items() if idx in members)


def edited_day_degree_ruler(sign: str, degree: int, *, sect: str) -> str:
    """One-based printed degree, reproducible editorial diurnal table only."""
    if sect != "day":
        raise ValueError("night and unknown sect intentionally unresolved")
    if type(degree) is not int or not 1 <= degree <= 30:
        raise ValueError("degree must be an integer from 1 to 30")
    start = PRINTED_DIURNAL_FIRST[triplicity_for_sign(sign)]
    idx = PLANET_CYCLE.index(start)
    return PLANET_CYCLE[(idx + degree - 1) % len(PLANET_CYCLE)]


def source_specific_example(sign: str, degree: int, variant: str) -> str:
    """Never substitute this one scholion for a 120-cell source table."""
    if variant == CANON.name:
        return edited_day_degree_ruler(sign, degree, sect="day")
    if variant == EXAMPLE_VARIANT.name and (sign, degree) == ("Cancer", 8):
        return "Venus"
    raise ValueError("alternative scholion attests ONLY the Cancer degree-8 example")


def invariant_check() -> dict[str, int]:
    """Counters for mechanical testing, not predictive scientific scoring."""
    covered = {
        (name,deg): edited_day_degree_ruler(sign,deg,sect="day")
        for name, members in TRIPLICITIES.items()
        for sign in (ZODIAC[members[0]],)
        for deg in range(1,31)
    }
    return {
        "cells_in_edition_diurnal_canon": len(covered),
        "distinct_planets": len(set(covered.values())),
        "scholion_example_cancer_degree_8_disagrees": int(
            source_specific_example("Cancer",8,CANON.name) !=
            source_specific_example("Cancer",8,EXAMPLE_VARIANT.name)
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(invariant_check(), indent=2))
