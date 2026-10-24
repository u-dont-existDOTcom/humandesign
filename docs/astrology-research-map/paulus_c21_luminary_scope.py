"""C21 Greek chapter-5 / chapter-32 research-only domain separation.

The chapter-32 allotment uses the light of sect, not an arbitrary natal
point. This adapter checks the *named* luminary against sect and delegates
only to the pre-existing frozen C05 narrative reconstruction.
It is NOT a chart engine, autograph, or production scoring rule.
"""
from __future__ import annotations

from pathlib import Path
import json

from paulus_bysign_papyrus_c04 import sign_monomoiria
from paulus_trigon_narrative_c05 import narrative_degree_ruler

SOURCE = Path(__file__).with_name("PAULUS_C21_GREEK_SECT_LIGHT_CLAUSES_V1.json")
SECT_TO_LIGHT = {"day": "Sun", "night": "Moon"}


def greek_source_witness() -> dict:
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def chapter5_by_sign_ruler(sign: str, completed_degrees: int, arcminutes: int) -> str:
    """Greek ch5 source rule; first ordinal degree spans [0°,1°)."""
    return sign_monomoiria(sign, completed_degrees, arcminutes)


def chapter32_sect_light_ruler(
    *, sect: str, luminary: str, light_sign: str, ordinal_degree: int,
) -> str:
    """Greek ch32 narrative for the sect light only (not any arbitrary point).

    The ordinal degree is intentionally explicit: the Greek ch32 page
    does not independently specify whether its degrees with minutes
    share chapter-5 rounding. Do not extrapolate ch5 to ch32 silently.
    """
    if sect not in SECT_TO_LIGHT:
        raise ValueError("sect must be explicitly day or night")
    if luminary != SECT_TO_LIGHT[sect]:
        raise ValueError("ch32 requires the light OF SECT: Sun day; Moon night")
    return narrative_degree_ruler(light_sign, ordinal_degree, sect=sect)


def source_scope_audit() -> dict:
    record = greek_source_witness()
    return {
        "source_layer": "DIGITAL_GREEK_TEXT_BODY_NOT_PRINTED_APPARATUS",
        "clauses_attested": len(record["clauses"]),
        "ch5_libra_2deg35": chapter5_by_sign_ruler("Libra", 2, 35),
        "ch32_day_fire_degree1": chapter32_sect_light_ruler(
            sect="day", luminary="Sun", light_sign="Aries", ordinal_degree=1
        ),
        "ch32_night_fire_degree1": chapter32_sect_light_ruler(
            sect="night", luminary="Moon", light_sign="Aries", ordinal_degree=1
        ),
        "ch32_day_water_degree8": chapter32_sect_light_ruler(
            sect="day", luminary="Sun", light_sign="Cancer", ordinal_degree=8
        ),
        "digital_online_diagram_has_transcribed_120_planet_cells": False,
        "source_methods_may_apply_to_arbitrary_point": False,
        "preexisting_Greenbaum_narrative_conflicting_cells": record[
            "missing_digital_table_rows"
        ]["C04_to_C05_printed_disagreements"],
        "Oxford_4277_matches_retained": record[
            "source_model_bindings"
        ]["C05_P_Oxy_4277_historical_matches"],
        "human_predictive_validations": 0,
        "production_rules_promoted": False,
    }


if __name__ == "__main__":
    print(json.dumps(source_scope_audit(), indent=2))
