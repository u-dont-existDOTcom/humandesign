"""Paulus Alexandrinus trigon monomoiria: Greek narrative reconstruction.

SOURCE / NOT AN ASTROLOGY PREDICTOR.
Paulus 'Introductory Matters' II (Greek), chapter 2 enumerates
day/night primary rulers of the four trigons; ch32 instructs rotating
through trigon pairs, skipping a second occurrence of any planet until
all seven have appeared. It specifically reverses the ruler order at
night (fire starts Jupiter followed by Sun).

The *Greek narrative* reconstruction below is NOT the same as the
Greenbaum edition's CORRECTED PRINTED DIURNAL TABLE. They agree in
fire/earth, but differ on portions of air/water (an editorial textual
variant, not human validation). Neither one has been established to be
Paulus's autograph or the only accepted ancient variant.

This exact module has no DOB, calendars, ephemerides or participant data.
"""
from __future__ import annotations

from paulus_monomoiria_source_c04 import (
    PRINTED_DIURNAL_FIRST,
    ZODIAC,
    edited_day_degree_ruler,
    triplicity_for_sign,
)

TRIGON_ORDER = ("fire", "earth", "air", "water")
# The *two original sect rulers* for each triplicity are attested in
# Eulogikon Greek Paulus chapter 2, not inferred from a recent blog.
TRIGON_DAY_NIGHT = {
    "fire": ("Sun", "Jupiter"),
    "earth": ("Venus", "Moon"),
    "air": ("Saturn", "Mercury"),
    "water": ("Venus", "Mars"),
}
SECTS = ("day", "night")


def _require_trigon_sect(trigon: str, sect: str) -> None:
    if trigon not in TRIGON_ORDER:
        raise ValueError("unknown Greek source triplicity")
    if sect not in SECTS:
        raise ValueError("sect must explicitly be day or night")


def narrative_one_cycle(trigon: str, sect: str) -> tuple[str, ...]:
    """Seven unique star allocations, from narrative rules rather than table.

    Start with the current trigon then continue cyclically fire->earth->
    air->water; each encountered trigon contributes its sect-ordered pair.
    A planet with a prior allocation is skipped until a complete
    seven-star cycle is obtained. The resulting full ordering is a
    deterministic *interpretation*; do not mislabel it a manuscript table.
    """
    _require_trigon_sect(trigon, sect)
    index = TRIGON_ORDER.index(trigon)
    assigned: list[str] = []
    for offset in range(4):
        tri = TRIGON_ORDER[(index + offset) % 4]
        day_lord, night_lord = TRIGON_DAY_NIGHT[tri]
        sequence = (day_lord, night_lord) if sect == "day" else (night_lord, day_lord)
        for planet in sequence:
            if planet not in assigned:
                assigned.append(planet)
    if len(assigned) != 7 or len(set(assigned)) != 7:
        raise AssertionError("Greek-source interpretation must allocate seven stars")
    return tuple(assigned)


def narrative_degree_ruler(sign: str, degree: int, *, sect: str) -> str:
    if sign not in ZODIAC:
        raise ValueError("unknown zodiac sign")
    if type(degree) is not int or not 1 <= degree <= 30:
        raise ValueError("ordinal degree must be an exact integer 1..30")
    order = narrative_one_cycle(triplicity_for_sign(sign), sect)
    return order[(degree - 1) % 7]


def printed_diurnal_difference_summary() -> dict[str, object]:
    """Comparison with Greenbaum's printed table, no biography involved."""
    mismatches = {}
    disagreements = {}
    for trigon in TRIGON_ORDER:
        sign = next(s for s in ZODIAC if triplicity_for_sign(s) == trigon)
        contrary = [
            degree for degree in range(1, 31)
            if narrative_degree_ruler(sign, degree, sect="day")
            != edited_day_degree_ruler(sign, degree, sect="day")
        ]
        mismatches[trigon] = len(contrary)
        disagreements[trigon] = contrary
    return {
        "witness_pair": ("PAULUS_GREEK_NARRATIVE_RECONSTRUCTION",
                         "GREENBAUM_EDITED_PRINTED_DAY_CANON"),
        "degrees_per_trigon": 30,
        "difference_count": mismatches,
        "differing_degree_indices": disagreements,
        "total_differing_cells": sum(mismatches.values()),
        "total_cells": 120,
        "scientific_status": "SOURCE_DISAGREEMENT_ONLY",
    }


if __name__ == "__main__":
    import json
    print(json.dumps({
        "day_orders": {k: narrative_one_cycle(k, "day") for k in TRIGON_ORDER},
        "night_orders": {k: narrative_one_cycle(k, "night") for k in TRIGON_ORDER},
        "day_against_printed": printed_diurnal_difference_summary(),
    }, indent=2))
