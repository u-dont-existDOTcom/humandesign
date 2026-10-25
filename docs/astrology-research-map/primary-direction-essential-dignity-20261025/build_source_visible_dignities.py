#!/usr/bin/env python3
"""Source-visible 1647 Lilly partial natal dignities on prior frozen synthetic charts.

No new birth inputs, no human event outcomes, no full 'strong Jupiter' verdict.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from hdmatch.astrology.lilly_essential_dignity import (
    CLASSICAL,
    source_visible_natal_components,
    swiss_placidus_house,
    table_integrity,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = ROOT / "docs/astrology-research-map/primary-direction-synthetic-panel-20261024"
EXPECTED_PARENT_PLAN = "948a1289b5f891c7f7870632ad116fb16ea6409d1bed575483c07c9901fbc0d0"
EXPECTED_EPHE = {
    "sepl_18.se1": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
    "semo_18.se1": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
}


def canonical(data: object) -> str:
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def verify_inputs(ephe: Path) -> tuple[dict, dict]:
    contract = json.loads((HERE / "DIGNITY_PRE_FREEZE_CONTRACT.json").read_text())
    if contract["schema"] != "LILLY_1647_PARTIAL_STRENGTH_PRECOMMIT_V1":
        raise ValueError("changed historical feature contract")
    panel = json.loads((PARENT / "SYNTHETIC_PANEL_INPUTS.json").read_text())
    old = json.loads((PARENT / "SYNTHETIC_PANEL_COVERAGE.json").read_text())
    exposures = json.loads((PARENT / "SYNTHETIC_PANEL_EXPOSURES.json").read_text())
    if len(panel["synthetic_cases"]) != 96 or len(exposures) != 96:
        raise ValueError("prior frozen synthetic panel is not intact")
    if (
        old["frozen_plan_sha256"] != EXPECTED_PARENT_PLAN
        or old["contact_coverage"]["total_exposures"] != 216
    ):
        raise ValueError("upstream historical panel differs from declared checkpoint")
    if set(panel["synthetic_cases"][0]) != {
        "id",
        "birth_utc",
        "latitude_deg",
        "longitude_east_deg",
        "month_stratum",
    }:
        raise ValueError("unexpected synthetic natal input format")
    for name, sha in EXPECTED_EPHE.items():
        f = ephe / name
        if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != sha:
            raise ValueError("Swiss file mismatch: " + name)
    return panel, exposures


SOURCE_RULE_PROMISSOR = {
    "L1647-MC-JUP-BODY": "jupiter",
    "L1647-MC-JUP-SOFT": "jupiter",
    "L1647-ASC-JUP-BODY": "jupiter",
    "L1647-ASC-JUP-SOFT": "jupiter",
    "L1647-ASC-MARS-BODY": "mars",
    "L1647-ASC-MARS-HARD": "mars",
    "L1647-MC-SAT-BODY": "saturn",
    "L1647-MC-SAT-HARD": "saturn",
}


def compute(ephe: Path) -> dict:
    table_integrity()
    panel, contacts = verify_inputs(ephe)
    planet_rows = []
    by_chart = {}
    sect_counts: Counter[str] = Counter()
    score_hists: dict[str, Counter[str]] = {body: Counter() for body in CLASSICAL}
    angular_counts: Counter[str] = Counter()
    for i, case in enumerate(panel["synthetic_cases"]):
        birth = snapshot_from_swiss_files(
            datetime.fromisoformat(case["birth_utc"]),
            latitude_deg=case["latitude_deg"],
            longitude_east_deg=case["longitude_east_deg"],
            ephemeris_directory=ephe,
        )
        if birth.ephemeris_mode != "SWIEPH verified for all seven classical bodies":
            raise ValueError("SWIEPH was not actually returned")
        components = source_visible_natal_components(birth)
        sect = components[0].chart_sect
        sect_counts[sect] += 1
        for component in components:
            house, house_fractional, house_points, angular = swiss_placidus_house(
                birth, component.planet
            )
            row = {
                "chart_id": case["id"],
                "planet": component.planet,
                "chart_sect": sect,
                "sign": component.zodiac_sign,
                "term_ruler": component.table_term_ruler,
                "face_ruler": component.table_face_ruler,
                "dignities": list(component.dignities_present),
                "debilities": list(component.debilities_present),
                "positive_points": component.positive_points,
                "negative_points": component.negative_points,
                "partial_net_points": component.partial_net_points,
                "placidus_house": house,
                "fractional_house": round(house_fractional, 9),
                "isolated_house_points": house_points,
                "house_angular": angular,
                "full_natal_strength": None,
            }
            score_hists[component.planet][str(component.partial_net_points)] += 1
            angular_counts[component.planet] += int(angular)
            planet_rows.append(row)
            by_chart[(case["id"], component.planet)] = row
        if (i + 1) % 24 == 0:
            print("source-visible natal components:", i + 1, "charts", flush=True)
    if len(planet_rows) != 96 * 7:
        raise ValueError("the seven classical natal component rows are incomplete")

    linked = []
    by_family: Counter[str] = Counter()
    for case in panel["synthetic_cases"]:
        for contact in contacts[case["id"]]:
            rid = contact["rule_id"]
            if rid not in SOURCE_RULE_PROMISSOR:
                raise ValueError("unregistered source-rule ID: " + rid)
            promissor = SOURCE_RULE_PROMISSOR[rid]
            detail = by_chart[(case["id"], promissor)]
            by_family[rid] += 1
            linked.append(
                {
                    "chart_id": case["id"],
                    "source_rule_id": rid,
                    "original_contact_key": contact["key"],
                    "symbolic_age_years": contact["age"],
                    "promissor": promissor,
                    "promissor_dignities": detail["dignities"],
                    "promissor_debilities": detail["debilities"],
                    "promissor_visible_partial_points": detail["partial_net_points"],
                    "promissor_house": detail["placidus_house"],
                    "promissor_house_angular": detail["house_angular"],
                    "significator": "mc" if "-MC-" in rid else "asc",
                    "significator_radix_strength": None,
                    "full_source_judgment": "UNRESOLVED_NEVER_SCORED",
                }
            )
    if len(linked) != 216 or by_family["L1647-MC-JUP-SOFT"] != 47:
        raise ValueError("source-exposure joining changed the prior 96-chart study")
    jupiter_mc = [x for x in linked if x["source_rule_id"] == "L1647-MC-JUP-SOFT"]
    jupiter_domicile_or_exaltation = sum(
        "domicile" in x["promissor_dignities"] or "exaltation" in x["promissor_dignities"]
        for x in jupiter_mc
    )
    summary = {
        "schema": "ASTRO_LILLY_1647_SOURCE_VISIBLE_DIGNITY_AUDIT_V1",
        "status": "PARTIAL_TABLE_COMPONENTS_NOT_COMPLETE_RADIX_STRENGTH",
        "source": "original first-edition Lilly 1647 pp.101-105,115,654-655,670",
        "n_synthetic_charts": len(panel["synthetic_cases"]),
        "n_planet_rows": len(planet_rows),
        "n_source_rule_contact_rows": len(linked),
        "n_lilly_classical_planets": len(CLASSICAL),
        "per_planet_partial_points_histogram": {
            body: dict(sorted(hist.items(), key=lambda x: int(x[0])))
            for body, hist in score_hists.items()
        },
        "n_planet_angular_house_by_planet": dict(sorted(angular_counts.items())),
        "chart_sect_counts": dict(sorted(sect_counts.items())),
        "source_rule_contact_counts": dict(sorted(by_family.items())),
        "jupiter_mc_favorable_aspect": {
            "exposure_count": len(jupiter_mc),
            "domicile_or_exaltation_indicator_count": jupiter_domicile_or_exaltation,
            "promissor_angular_house_count": sum(
                bool(x["promissor_house_angular"]) for x in jupiter_mc
            ),
            "full_strong_jupiter_verdict_count": 0,
        },
        "historical_condition_interpretation": "UNRESOLVED_NO_CUTOFF",
        "full_radix_strength_verdicts": 0,
        "human_outcomes": "NONE",
        "predictive_accuracy": "UNTESTED",
        "parent_combined_astrology_project": "OPEN",
    }
    return {"summary": summary, "planet_rows": planet_rows, "contact_rows": linked}


def write_results(result: dict) -> None:
    files = [
        HERE / "PARTIAL_DIGNITIES_SUMMARY.json",
        HERE / "PARTIAL_DIGNITIES_PLANET_ROWS.csv",
        HERE / "PARTIAL_DIGNITIES_CONTACT_CROSSWALK.json",
    ]
    if any(path.exists() for path in files):
        raise FileExistsError("refuse to overwrite an existing synthetic result")
    files[0].write_text(canonical(result["summary"]), encoding="utf-8")
    files[2].write_text(canonical(result["contact_rows"]), encoding="utf-8")
    header = [
        "chart_id",
        "planet",
        "chart_sect",
        "sign",
        "term_ruler",
        "face_ruler",
        "dignities",
        "debilities",
        "positive_points",
        "negative_points",
        "partial_net_points",
        "placidus_house",
        "fractional_house",
        "isolated_house_points",
        "house_angular",
        "full_natal_strength",
    ]
    with files[1].open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=header)
        writer.writeheader()
        for original in result["planet_rows"]:
            record = dict(original)
            for name in ("dignities", "debilities"):
                record[name] = "|".join(record[name])
            writer.writerow(record)
    print("saved 96-chart essential-dignity/house-only diagnostics")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ephemeris-dir", type=Path, required=True)
    args = parser.parse_args()
    write_results(compute(args.ephemeris_dir))


if __name__ == "__main__":
    main()
