# ruff: noqa: E501
"""Pre-freeze PRIMARY DIRECTIONS source/method feasibility inventory.

Research-only. This script does not score people, produce event predictions,
select favorable timing keys, or alter existing computation. It reuses the
source-assessment functions already checked against historical text.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from hdmatch.astrology.lilly_1647_photo import MINUTE_LABEL_ABSENT, MINUTE_PARTIALLY_LEGIBLE
from hdmatch.astrology.source_witness_scope import (
    placidus_1657_latin_role_assessment,
    solar_key_source_assessment,
)

HERE = Path(__file__).resolve().parent


def arm(
    id: str,
    title: str,
    args: list[str] | None,
    evidence: str,
    limitation: str,
    *,
    support: str = "not_fully_attributed",
    duplicate_group: str | None = None,
) -> dict[str, object]:
    return {
        "id": id,
        "title": title,
        "cli_flags": args,
        "source_evidence": evidence,
        "source_support": support,
        "limitations": limitation,
        "geometric_duplicate_group": duplicate_group,
        "interpretation_frozen": False,
        "real_human_prediction_validated": False,
        "human_study_admitted_by_this_inventory": False,
    }


def build() -> dict[str, object]:
    brahe = solar_key_source_assessment("brahe_true_midnight_birth_day")
    placidus = solar_key_source_assessment("placidus_cumulative_true_solar_ra")
    contrary = placidus_1657_latin_role_assessment(
        "zodiacal_promissor_ray", "traditional_role_reversed_converse"
    )
    assert brahe.status.value == "partial_source_support"
    assert placidus.status.value == "compatible_selected_rule"
    assert contrary.status.value == "incompatible_witness"

    entries = [
        arm(
            "PD01",
            "Bodily contacts, one degree/year",
            ["--profile", "body_conjunctions", "--key", "ptolemy_one_degree_per_year"],
            "Gansten source audit: conventional one-degree symbolic year",
            "Full source-defined event interpretations have not been frozen.",
        ),
        arm(
            "PD02",
            "Bodily contacts, Placidus variable solar RA",
            [
                "--profile",
                "body_conjunctions",
                "--solar-time-key",
                "placidus_cumulative_true_solar_ra",
            ],
            "Placidus 1657 original Latin thesis 65 supports successive solar RA daily advances",
            "Timing principle sourced; entire historic geometry/TT/UT conventions and event meanings not fully certified.",
            support=placidus.status.value,
        ),
        arm(
            "PD03",
            "Bodily contacts, Brahe natal birth-day RA",
            ["--profile", "body_conjunctions", "--solar-time-key", "brahe_true_midnight_birth_day"],
            "Brahe 1573 contemporary Latin via critical scholarly transcription, varying real solar motion",
            "Specific local true-midnight samples are later Gansten-informed reconstruction, not proved in inspected 1573 passage.",
            support=brahe.status.value,
        ),
        arm(
            "PD04",
            "Direct zero-latitude zodiacal promissor rays",
            ["--profile", "zodiacal_promissor_rays", "--method", "proportional_semi_arc"],
            "Gansten purchased-book technical audit Ch.5 and Ch.8",
            "Does not implement all Bianchini/Morin latitude or source-defined event meanings.",
        ),
        arm(
            "PD05",
            "Mundane normalized proportional semi-arc aspects",
            ["--profile", "mundane_proportional_semi_arc"],
            "Independent semi-arc phase mathematical reconstruction",
            "Not a historically certified complete Placidus or Regiomontanian mundane-ray algorithm.",
            support="analytic_reconstruction",
        ),
        arm(
            "PD06",
            "Generic bodily traditional converse",
            [
                "--profile",
                "role_variants",
                "--contact-construction",
                "bodily_conjunction",
                "--rotation-regime",
                "traditional_role_reversed_converse",
            ],
            "Gansten converse audit; Placidus 1657 allows non-angle converse body roles",
            "Do not move Ascendant/Midheaven; author-specific geometry and interpretation remain open.",
        ),
        arm(
            "PD07",
            "Generic role-reversed zodiacal promissor rays",
            [
                "--profile",
                "role_variants",
                "--contact-construction",
                "zodiacal_promissor_ray",
                "--rotation-regime",
                "traditional_role_reversed_converse",
            ],
            "Math candidate, but Placidus 1657 expressly excludes zodiacal rays in converse",
            "NOT historically attributable to Placidus. Same arcs as PD08 under swapped names for bodily/unprojected seven-planet comparison.",
            support="incompatible_as_placidus_1657",
            duplicate_group="fixed_ray_swapped_roles",
        ),
        arm(
            "PD08",
            "Direct significator-owned zero-latitude zodiacal aspects",
            [
                "--profile",
                "role_variants",
                "--contact-construction",
                "zodiacal_significator_aspect",
                "--rotation-regime",
                "direct_primary_motion",
            ],
            "Experimental construction preserving disputed source definitions",
            "Same 288 bodily/unprojected arcs as PD07 after swapping promissor/significator labels; not independent predictive evidence.",
            support="experimental",
            duplicate_group="fixed_ray_swapped_roles",
        ),
        arm(
            "PD09",
            "Modern reverse-rotation complementary arc",
            [
                "--profile",
                "role_variants",
                "--contact-construction",
                "bodily_conjunction",
                "--rotation-regime",
                "modern_reverse_rotation_diagnostic",
            ],
            "Contemporary mathematical diagnostic, not Placidus original converse",
            "Not interchangeable with moving the significator in traditional converse.",
            support="modern_diagnostic",
        ),
        arm(
            "PD10",
            "Naibod fixed 59′08″ annual-rate diagnostic",
            ["--profile", "body_conjunctions", "--key", "naibod_59m08s_fixed_diagnostic"],
            "Modern explicit fixed angular-rate model",
            "Not the original Lilly printed lookup nor exact 360/365.25 rational rate.",
            support="continuous_diagnostic",
        ),
        arm(
            "PD11",
            "Original Lilly 1647 literal table diagnostic",
            None,
            "Two independently photographed original Lilly 1647 copies",
            "Not continuous; minute 27 absent, six faint minutes; fractional seconds not printed.",
            support="incomplete_original_table",
        ),
        arm(
            "PD12",
            "Modern Lilly 2003 retyped literal diagnostic",
            None,
            "Separate WorldAstrology 2003 Lilly retypesetting",
            "Differs from original on 22 degree-year rows plus minute-one day; final 19°52′ prose differs.",
            support="modern_witness_only",
        ),
    ]
    ids = [row["id"] for row in entries]
    assert len(ids) == len(set(ids)) == 12
    duplicates = [
        row["id"]
        for row in entries
        if row["geometric_duplicate_group"] == "fixed_ray_swapped_roles"
    ]
    assert duplicates == ["PD07", "PD08"]
    return {
        "schema": "ASTRO_PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY_V1",
        "date": "2026-10-24",
        "status": "UNFROZEN_RESEARCH_NOT_PREDICTION_VALIDATION",
        "owner_goal": (
            "accurate separate astrology calculations, freeze interpretations "
            "before prospectively scored blinded human responses, compare jointly "
            "to matched alternatives without hindsight fitting"
        ),
        "original_Lilly_1647_faint_minutes": sorted(MINUTE_PARTIALLY_LEGIBLE),
        "original_Lilly_1647_absent_minute_label": sorted(MINUTE_LABEL_ABSENT),
        "source_Witness_Placidus_converse_zodiacal": contrary.to_dict(),
        "double_count_warning": {
            "ids": duplicates,
            "earlier_frozen_math_scope": (
                "288/288 bodily, unprojected, seven-classical-planet contacts "
                "share identical arcs after planet role label exchange"
            ),
            "number_of_independent_physical_rotations": "count once for identical arc",
            "source_interpretations_not_assumed_identical": True,
        },
        "missing_before_prospective_scored_claims": [
            "Historically attributed event/behavior mapping and exact prediction window",
            "A method-choice freeze independent of known human outcomes",
            "Separate consent and prospective blinding/model-control evidence",
        ],
        "never_infer": [
            "historical source support or synthetic parity proves human predictive power",
            "a generic role-reversed zodiacal ray is authentic Placidus 1657",
            "literal 1647 Naibod table can time arbitrary fractional arcs without added rules",
            "two labels for the same geometric rotation are two independent confirmations",
        ],
        "not_new_mandatory_source_gate": True,
        "human_prediction_mapping_frozen": False,
        "all_source_engineering_only": True,
        "arms": entries,
    }


def main() -> None:
    data = build()
    out = HERE / "PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    csv_file = HERE / "PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.csv"
    names = [
        "id",
        "title",
        "source_support",
        "source_evidence",
        "geometric_duplicate_group",
        "interpretation_frozen",
        "real_human_prediction_validated",
        "cli_flags",
        "limitations",
    ]
    with csv_file.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        for item in data["arms"]:
            row = dict(item)
            row["cli_flags"] = " ".join(row["cli_flags"] or [])
            writer.writerow({field: row[field] for field in names})
    print("12 unfrozen source-labeled method families; CSV and JSON written")


if __name__ == "__main__":
    main()
