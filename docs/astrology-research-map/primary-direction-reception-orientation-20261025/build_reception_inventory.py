#!/usr/bin/env python3
"""Synthetic source reception analysis only."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from hdmatch.astrology.lilly_angle_progression import (
    AngularAxis,
    source_forward_angular_arc,
)
from hdmatch.astrology.lilly_reception import (
    DignityPlacement,
    ReceptionEvidence,
    all_chart_receptions,
)

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PARENT = ROOT / "docs/astrology-research-map/primary-direction-essential-dignity-20261025"


def canonical(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def verified_source_rows() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    contract = json.loads((HERE / "RECEPTION_ORIENTATION_PRECOMMIT.json").read_text())
    if contract["schema"] != "LILLY_1647_RECEPTION_AND_ANGLE_ARC_PRECOMMIT_V1":
        raise ValueError("source feature contract changed")
    old_manifest = json.loads((PARENT / "VERIFICATION.json").read_text())
    files = ("PARTIAL_DIGNITIES_PLANET_ROWS.csv", "PARTIAL_DIGNITIES_CONTACT_CROSSWALK.json")
    for name in files:
        path = PARENT / name
        key = str(path.relative_to(ROOT))
        if hashlib.sha256(path.read_bytes()).hexdigest() != old_manifest["files"][key]["sha256"]:
            raise ValueError("parent 96-chart data changed: " + name)
    with (PARENT / files[0]).open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    links = json.loads((PARENT / files[1]).read_text())
    if len(rows) != 672 or len(links) != 216:
        raise ValueError("prior frozen sample must have 672 planet rows and 216 contacts")
    if any(r["full_natal_strength"] for r in rows):
        raise ValueError("parent chart strength was not unresolved")
    if any(r["full_source_judgment"] != "UNRESOLVED_NEVER_SCORED" for r in links):
        raise ValueError("parent direction outcome status was modified")
    return rows, links


def source_angle_examples() -> dict[str, Any]:
    def item(axis: AngularAxis, fixed: float, prom: float) -> dict[str, Any]:
        return source_forward_angular_arc(axis, fixed, prom).to_dict()

    return {
        "schema": "ORIGINAL_1647_ANGULAR_COORDINATE_ARITHMETIC_V1",
        "scope": "p515 MC right ascension and p517 ASC oblique ascension",
        "examples": {
            "p515_mercury_terms": item(
                AngularAxis.MC_RIGHT_ASCENSION,
                222 + 10 / 60,
                229 + 35 / 60,
            ),
            "p515_venus_terms": item(
                AngularAxis.MC_RIGHT_ASCENSION,
                222 + 10 / 60,
                222 + 31 / 60,
            ),
            "p517_first_oblique": item(
                AngularAxis.ASC_OBLIQUE_ASCENSION,
                312 + 10 / 60,
                313 + 34 / 60,
            ),
            "p517_last_oblique": item(
                AngularAxis.ASC_OBLIQUE_ASCENSION,
                312 + 10 / 60,
                332 + 2 / 60,
            ),
        },
        "p515_internal_print_discrepancy": {
            "intermediate_arc": "7 degrees 45 minutes",
            "operand_subtraction_and_final_worked_result": "7 degrees 25 minutes",
            "status": "BOTH_PRIMARY_PRINTED_READINGS_PRESERVED",
        },
        "historical_scope_warning": (
            "not a complete source authentication of converse directions, "
            "Argolus geometry, planetary latitude or universal time key"
        ),
    }


def build() -> dict[str, Any]:
    rows, contacts = verified_source_rows()
    placements: dict[str, list[DignityPlacement]] = defaultdict(list)
    for item in rows:
        placements[item["chart_id"]].append(
            DignityPlacement(
                planet=item["planet"],
                zodiac_sign=item["sign"],
                chart_sect=item["chart_sect"],
                term_ruler=item["term_ruler"],
                face_ruler=item["face_ruler"],
            )
        )
    if len(placements) != 96:
        raise ValueError("one or more frozen synthetic charts are absent")
    reception_by_chart: dict[str, tuple[ReceptionEvidence, ...]] = {}
    all_receptions = {}
    same_modes: Counter[str] = Counter()
    mixed_only = 0
    n_none = 0
    for chart_id, bodies in sorted(placements.items()):
        pairs = all_chart_receptions(tuple(bodies))
        if not pairs:
            n_none += 1
        for relation in pairs:
            same_modes.update(relation.same_mode_receptions)
            mixed_only += int(relation.mixed_only)
        reception_by_chart[chart_id] = pairs
        all_receptions[chart_id] = [r.to_dict() for r in pairs]
    count_pairs = sum(len(x) for x in all_receptions.values())
    if count_pairs > 96 * 21:
        raise ValueError("duplicate unordered pair counted as evidence")

    jupiter_mc_contacts = [row for row in contacts if row["source_rule_id"] == "L1647-MC-JUP-SOFT"]
    if len(jupiter_mc_contacts) != 47:
        raise ValueError("unfrozen expansion of earlier Jupiter/MC exposures")
    linked: list[dict[str, Any]] = []
    for item in jupiter_mc_contacts:
        chart = item["chart_id"]
        jupiter_pairs = [
            rec for rec in reception_by_chart[chart] if "jupiter" in (rec.planet_a, rec.planet_b)
        ]
        own_modes = sorted({m for rec in jupiter_pairs for m in rec.same_mode_receptions})
        linked.append(
            {
                "chart_id": chart,
                "frozen_direction_key": item["original_contact_key"],
                "symbolic_age_years": item["symbolic_age_years"],
                "jupiter_reception_partners": [
                    (x.planet_b if x.planet_a == "jupiter" else x.planet_a) for x in jupiter_pairs
                ],
                "source_reciprocal_same_modes": own_modes,
                "has_source_domicile_reception": "domicile" in own_modes,
                "has_source_exaltation_reception": "exaltation" in own_modes,
                "mixed_only_partner_count": sum(x.mixed_only for x in jupiter_pairs),
                "already_reported_essential_partial_points": item[
                    "promissor_visible_partial_points"
                ],
                "complete_jupiter_strength": None,
                "full_lilly_direction_prediction": None,
            }
        )
    mode_counts = {
        kind: sum(kind in row["source_reciprocal_same_modes"] for row in linked)
        for kind in ("domicile", "exaltation", "triplicity", "term", "face")
    }

    summary = {
        "schema": "LILLY_1647_RECEPTION_SYNT_HISTORICAL_FEATURE_COUNTS_V1",
        "status": "SOURCE_FEATURE_ONLY_NO_HUMAN_EVENTS_NO_FULL_STRENGTH",
        "n_synthetic_charts": 96,
        "n_prior_planet_rows": 672,
        "n_prior_source_rule_contacts": 216,
        "n_unordered_reception_pairs": count_pairs,
        "n_charts_without_any_reciprocal_reception": n_none,
        "same_dignity_mode_pair_counts": dict(sorted(same_modes.items())),
        "mixed_only_pairs_not_history_scored": mixed_only,
        "mc_jupiter_favorable_prior_contacts": 47,
        "mc_jupiter_mutual_mode_contact_counts": mode_counts,
        "mc_jupiter_contacts_full_strength_certified": 0,
        "mc_jupiter_interpretation_frozen": False,
        "full_lilly_radix_strength_verdicts": 0,
        "one_sided_hosts_counted_as_mutual": False,
        "house_receiving_refers_to": "zodiacal_sign_domicile_NOT_mundane_houses",
        "numeric_source_points_stacked_on_own_dignity": False,
        "owner_combined_untouched_human_study": "OPEN",
        "empirical_predictive_accuracy": "UNTESTED",
    }
    return {
        "receptions": all_receptions,
        "jupiter_mc_contacts": linked,
        "summary": summary,
        "source_angular_examples": source_angle_examples(),
    }


OUTPUTS = {
    "receptions": "RECEPTION_RELATIONS.json",
    "jupiter_mc_contacts": "RECEPTION_MC_JUPITER_CROSSWALK.json",
    "summary": "RECEPTION_SYNTHETIC_SUMMARY.json",
    "source_angular_examples": "SOURCE_ANGULAR_ARITHMETIC.json",
}


def run_once() -> None:
    if any((HERE / filename).exists() for filename in OUTPUTS.values()):
        raise FileExistsError("refuse to overwrite fixed synthetic outputs")
    result = build()
    for key, filename in OUTPUTS.items():
        (HERE / filename).write_text(canonical(result[key]), encoding="utf-8")
    print(
        "96 frozen charts; unordered reception pairs:",
        result["summary"]["n_unordered_reception_pairs"],
    )
    print(
        "47 Jupiter/MC source contacts; full-strength verdicts:",
        result["summary"]["full_lilly_radix_strength_verdicts"],
    )


if __name__ == "__main__":
    run_once()
