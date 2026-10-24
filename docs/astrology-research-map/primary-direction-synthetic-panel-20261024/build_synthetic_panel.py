#!/usr/bin/env python3
"""Deterministic synthetic-only natal contact coverage; no human evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import statistics
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path

from hdmatch.astrology.aspect_points import RayAspect
from hdmatch.astrology.aspect_timeline import AspectProfile, generate_aspect_timeline
from hdmatch.astrology.geometry import GeometryMethod
from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.timeline import TimeKey, generate_timeline

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREVIOUS = ROOT / "docs/astrology-research-map/primary-direction-event-hypotheses-20261024"
PLAN_SHA256 = "948a1289b5f891c7f7870632ad116fb16ea6409d1bed575483c07c9901fbc0d0"
EXPECTED_EPHEMERIS = {
    "sepl_18.se1": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
    "semo_18.se1": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
}
METHOD = (GeometryMethod.PROPORTIONAL_SEMI_ARC,)
KEY = TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR


def canonical(data: object) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def load_plan() -> dict:
    raw = (HERE / "PANEL_PLAN.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != PLAN_SHA256:
        raise ValueError("panel plan changed after source-side precommit")
    spec = json.loads(raw)
    if spec["n_cases"] != 96:
        raise ValueError("wrong synthetic panel count")
    return spec


def build_inputs(spec: dict) -> dict:
    rng = random.Random(spec["seed"])
    cases = []
    for month in spec["months"]:
        for lat in spec["latitudes"]:
            dt = datetime(
                rng.randint(*spec["years"]),
                month,
                rng.randint(*spec["days"]),
                rng.randint(*spec["utc_hours"]),
                rng.randint(*spec["utc_minutes"]),
                tzinfo=UTC,
            )
            lon = round(rng.uniform(*spec["longitude_east_range"]), 6)
            cases.append(
                {
                    "id": f"SYN-PD-{len(cases) + 1:03d}",
                    "birth_utc": dt.isoformat(),
                    "latitude_deg": lat,
                    "longitude_east_deg": lon,
                    "month_stratum": month,
                }
            )
    if len(cases) != spec["n_cases"]:
        raise ValueError("panel size differs from preregistration")
    sensitivity = spec["birth_time_sensitivity"]
    subset = sorted(
        random.Random(sensitivity["seed"]).sample(
            [case["id"] for case in cases], sensitivity["random_sample_n"]
        )
    )
    return {
        "schema": "SYNTHETIC_ONLY_BIRTH_INPUTS_V1",
        "plan_sha256": PLAN_SHA256,
        "selection_frozen_before_astronomy": True,
        "synthetic_cases": cases,
        "sensitivity_case_ids": subset,
    }


def verified_inputs(spec: dict) -> dict:
    declared = build_inputs(spec)
    actual = json.loads((HERE / "SYNTHETIC_PANEL_INPUTS.json").read_text())
    if actual != declared:
        raise ValueError("synthetic birth cases changed after selection")
    return actual


def check_ephemeris(root: Path) -> None:
    for name, expected in EXPECTED_EPHEMERIS.items():
        file = root / name
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != expected:
            raise ValueError(f"verified Swiss ephemeris file unavailable/mismatch: {name}")


def source_rules() -> tuple[list[dict], list[dict]]:
    bodily = json.loads((PREVIOUS / "LILLY_1647_EVENT_CANDIDATES.json").read_text())
    aspects = json.loads((PREVIOUS / "ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json").read_text())
    body_rules = bodily["source_to_construct_rules"]
    aspect_rules = aspects["families"]
    assert len(body_rules) == 4 and len(aspect_rules) == 4
    assert not aspects["study_ready"]
    return body_rules, aspect_rules


def natal(case: dict, ephe: Path):
    instant = datetime.fromisoformat(case["birth_utc"])
    result = snapshot_from_swiss_files(
        instant,
        latitude_deg=case["latitude_deg"],
        longitude_east_deg=case["longitude_east_deg"],
        ephemeris_directory=ephe,
    )
    if result.ephemeris_mode != "SWIEPH verified for all seven classical bodies":
        raise RuntimeError("Swiss ephemeris fallback is prohibited")
    return result


def exposure_records(sky, body_rules: list[dict], aspect_rules: list[dict]) -> list[dict]:
    body = generate_timeline(sky, methods=METHOD, time_key=KEY, max_age_years=65)
    rays = generate_aspect_timeline(
        sky,
        profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
        methods=METHOD,
        aspects=tuple(RayAspect),
        time_key=KEY,
        max_age_years=65,
    )
    mapping = {(r["promissor"], r["target_role"]): r["id"] for r in body_rules}
    aspect_mapping = {(r["promissor"], r["significator"]): r for r in aspect_rules}
    found = []
    for rec in body.directions:
        rid = mapping.get((rec.promissor, rec.significator))
        if rid and rec.contact == "body_to_angle" and rec.direction == "direct":  # noqa: SIM102
            if 18 <= rec.symbolic_age_years < 65:
                found.append(
                    {
                        "key": rid + "/body",
                        "rule_id": rid,
                        "kind": "body",
                        "age": round(rec.symbolic_age_years, 9),
                    }
                )
    for rec in rays.directions:
        rule = aspect_mapping.get((rec.promissor, rec.significator))
        if rule and rec.ray_aspect in rule["aspects"] and rec.direction == "direct":  # noqa: SIM102
            if 18 <= rec.symbolic_age_years < 65:
                rid = rule["id"]
                found.append(
                    {
                        "key": f"{rid}/{rec.ray_aspect}/{rec.ray_offset_branch}",
                        "rule_id": rid,
                        "kind": "aspect",
                        "age": round(rec.symbolic_age_years, 9),
                    }
                )
    if len({item["key"] for item in found}) != len(found):
        raise ValueError("duplicate source-rule/aspect-branch key")
    return sorted(found, key=lambda x: (x["rule_id"], x["key"]))


def union_span(exposures: list[dict], half_window: float) -> float:
    segments = sorted(
        (max(18.0, r["age"] - half_window), min(65.0, r["age"] + half_window)) for r in exposures
    )
    merged = []
    for low, high in segments:
        if not merged or low > merged[-1][1]:
            merged.append([low, high])
        else:
            merged[-1][1] = max(merged[-1][1], high)
    return round(sum(high - low for low, high in merged), 8)


def summarize(
    cases: list[dict], exposure_by_id: dict, source_ids: list[str], half: float
) -> tuple[dict, list[dict]]:
    counts = Counter()
    rows = []
    for case in cases:
        contacts = exposure_by_id[case["id"]]
        counts.update(x["rule_id"] for x in contacts)
        body = sum(x["kind"] == "body" for x in contacts)
        aspects = len(contacts) - body
        row = {
            "id": case["id"],
            "month_stratum": case["month_stratum"],
            "latitude_deg": case["latitude_deg"],
            "body_exposures": body,
            "aspect_exposures": aspects,
            "all_exposures": len(contacts),
            "union_years": union_span(contacts, half),
        }
        rows.append(row)
    total = [row["all_exposures"] for row in rows]
    body_total = [row["body_exposures"] for row in rows]
    aspect_total = [row["aspect_exposures"] for row in rows]
    summary = {
        "n_charts": len(rows),
        "candidate_rule_count": len(source_ids),
        "total_exposures": sum(total),
        "mean_exposures_per_synthetic_chart": round(statistics.mean(total), 6),
        "median_exposures": statistics.median(total),
        "min_exposures": min(total),
        "max_exposures": max(total),
        "zero_body_chart_count": sum(x == 0 for x in body_total),
        "zero_aspect_chart_count": sum(x == 0 for x in aspect_total),
        "zero_any_chart_count": sum(x == 0 for x in total),
        "body_exposure_total": sum(body_total),
        "aspect_exposure_total": sum(aspect_total),
        "mean_union_window_years_per_chart": round(
            statistics.mean(row["union_years"] for row in rows), 6
        ),
        "rule_exposure_count": {k: counts[k] for k in sorted(source_ids)},
    }
    return summary, rows


def check_angle_geometry_parity(sky, body_rules: list[dict], aspect_rules: list[dict]) -> dict:
    all_methods = tuple(GeometryMethod)
    timeline = generate_timeline(sky, methods=all_methods, time_key=KEY, max_age_years=65)
    rays = generate_aspect_timeline(
        sky,
        profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
        methods=all_methods,
        time_key=KEY,
        max_age_years=65,
    )
    bpairs = {(r["promissor"], r["target_role"]) for r in body_rules}
    apairs = {(r["promissor"], r["significator"]): set(r["aspects"]) for r in aspect_rules}
    groups: dict[tuple, list[tuple[str, float]]] = {}
    for r in timeline.directions:
        if (r.promissor, r.significator) in bpairs and r.direction == "direct":  # noqa: SIM102
            if 18 <= r.symbolic_age_years < 65:
                key = ("body", r.promissor, r.significator)
                groups.setdefault(key, []).append((r.method, r.symbolic_age_years))
    for r in rays.directions:
        if (
            r.ray_aspect in apairs.get((r.promissor, r.significator), set())
            and r.direction == "direct"
            and 18 <= r.symbolic_age_years < 65
        ):
            key = (r.ray_aspect, r.ray_offset_branch, r.promissor, r.significator)
            groups.setdefault(key, []).append((r.method, r.symbolic_age_years))
    failures = []
    max_spread = 0.0
    for key, variants in sorted(groups.items()):
        methods = {m for m, _ in variants}
        ages = [age for _, age in variants]
        spread = max(ages) - min(ages)
        max_spread = max(max_spread, spread)
        if len(variants) != 3 or len(methods) != 3 or spread > 1e-8:
            failures.append({"key": key, "method_ages": variants})
    return {
        "groups_checked": len(groups),
        "largest_age_spread_years": max_spread,
        "failures": failures,
    }


def birth_time_stress(
    inputs: dict,
    base: dict,
    ephe: Path,
    body_rules: list[dict],
    aspect_rules: list[dict],
    spec: dict,
) -> dict:
    case_by_id = {x["id"]: x for x in inputs["synthetic_cases"]}
    offsets = spec["birth_time_sensitivity"]["offsets_minutes"]
    results = []
    for offset in offsets:
        n_reference = n_common = n_half_year = n_one_year = n_new = 0
        absolute_deltas = []
        details = []
        for cid in inputs["sensitivity_case_ids"]:
            reference = {x["key"]: x["age"] for x in base[cid]}
            altered = dict(case_by_id[cid])
            altered["birth_utc"] = (
                datetime.fromisoformat(altered["birth_utc"]) + timedelta(minutes=offset)
            ).isoformat()
            variant = exposure_records(natal(altered, ephe), body_rules, aspect_rules)
            alternative = {x["key"]: x["age"] for x in variant}
            intersection = set(reference) & set(alternative)
            shifts = [abs(reference[k] - alternative[k]) for k in intersection]
            n_reference += len(reference)
            n_common += len(intersection)
            n_new += len(set(alternative) - set(reference))
            n_half_year += sum(delta <= 0.5 for delta in shifts)
            n_one_year += sum(delta <= 1.0 for delta in shifts)
            absolute_deltas.extend(shifts)
            details.append(
                {
                    "id": cid,
                    "baseline_contacts": len(reference),
                    "perturbed_contacts": len(alternative),
                    "shared_rule_branch": len(intersection),
                    "within_half_year": sum(d <= 0.5 for d in shifts),
                    "within_one_year": sum(d <= 1.0 for d in shifts),
                }
            )
        results.append(
            {
                "offset_minutes": offset,
                "case_count": len(details),
                "baseline_contact_denominator": n_reference,
                "matched_rule_branches": n_common,
                "new_rule_branches": n_new,
                "missing_rule_branches": n_reference - n_common,
                "within_half_year": n_half_year,
                "within_one_year": n_one_year,
                "half_year_retention_fraction": (
                    round(n_half_year / n_reference, 6) if n_reference else None
                ),
                "median_abs_shift_years_if_common": (
                    round(statistics.median(absolute_deltas), 6) if absolute_deltas else None
                ),
                "individual_cases": details,
            }
        )
    return {
        "schema": "SYNTHETIC_BIRTH_TIME_SENSITIVITY_V1",
        "status": "COMPUTATIONAL_STABILITY_NOT_HUMAN_PREDICTIVE_VALIDITY",
        "selected_synthetic_case_ids": inputs["sensitivity_case_ids"],
        "offset_summaries": results,
        "outcome_records_used": False,
    }


def run_panel(spec: dict, frozen: dict, ephe: Path) -> dict:
    check_ephemeris(ephe)
    body_rules, aspect_rules = source_rules()
    sources = [r["id"] for r in body_rules + aspect_rules]
    exposures: dict[str, list[dict]] = {}
    parity_checked = 0
    parity_groups = 0
    parity_failures = []
    max_parity_spread = 0.0
    for i, case in enumerate(frozen["synthetic_cases"]):
        sky = natal(case, ephe)
        exposures[case["id"]] = exposure_records(sky, body_rules, aspect_rules)
        if i < spec["parity_check_n"]:
            test = check_angle_geometry_parity(sky, body_rules, aspect_rules)
            parity_checked += 1
            parity_groups += test["groups_checked"]
            max_parity_spread = max(max_parity_spread, test["largest_age_spread_years"])
            parity_failures.extend(test["failures"])
        if (i + 1) % 24 == 0:
            print("synthetic charts processed:", i + 1, flush=True)
    summary, rows = summarize(
        frozen["synthetic_cases"],
        exposures,
        sources,
        spec["age_window_half_width_years"],
    )
    stability = birth_time_stress(frozen, exposures, ephe, body_rules, aspect_rules, spec)
    analysis = {
        "schema": "ASTRO_PRIMARY_DIRECTION_SYNTHETIC_96_CHART_COVERAGE_V1",
        "status": "ENGINEERING_COVERAGE_ONLY_NOT_VALIDATED_PREDICTIONS",
        "sampling": "12 birth months x 8 latitude strata; years/clock/longitude seeded",
        "representative_population_sample": False,
        "parent_astrology_validation_goal": "OPEN",
        "frozen_plan_sha256": PLAN_SHA256,
        "no_human_natal_or_event_records": True,
        "time_key": KEY.value,
        "direction": "software-direct shortest signed arc (not historical Lilly)",
        "geometry": METHOD[0].value,
        "contact_coverage": summary,
        "angle_geometry_parity": {
            "charts_checked": parity_checked,
            "groups_checked": parity_groups,
            "max_spread_years": max_parity_spread,
            "mismatches": parity_failures,
        },
        "observational_outcome_scoring": "NOT_PERFORMED",
    }
    return {
        "analysis": analysis,
        "chart_rows": rows,
        "exposures": exposures,
        "stability": stability,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--freeze-inputs", action="store_true")
    choice.add_argument("--run", action="store_true")
    parser.add_argument("--ephemeris-dir", type=Path)
    args = parser.parse_args()
    spec = load_plan()
    input_file = HERE / "SYNTHETIC_PANEL_INPUTS.json"
    if args.freeze_inputs:
        if input_file.exists():
            raise FileExistsError("inputs already frozen: refuse overwrite")
        input_file.write_text(canonical(build_inputs(spec)), encoding="utf-8")
        print("froze", spec["n_cases"], "synthetic input tuples")
        return
    if args.ephemeris_dir is None:
        raise ValueError("--ephemeris-dir is required for actual astronomy")
    frozen = verified_inputs(spec)
    outputs = [
        HERE / "SYNTHETIC_PANEL_COVERAGE.json",
        HERE / "SYNTHETIC_PANEL_EXPOSURES.json",
        HERE / "SYNTHETIC_PANEL_CHART_ROWS.csv",
        HERE / "BIRTH_TIME_PERTURBATION.json",
    ]
    if any(path.exists() for path in outputs):
        raise FileExistsError("do not overwrite prior synthetic analysis")
    results = run_panel(spec, frozen, args.ephemeris_dir)
    texts = (
        canonical(results["analysis"]),
        canonical(results["exposures"]),
        None,
        canonical(results["stability"]),
    )
    for path, text in zip(outputs, texts, strict=True):
        if text is not None:
            path.write_text(text, encoding="utf-8")
    with outputs[2].open("w", newline="", encoding="utf-8") as dest:
        writer = csv.DictWriter(dest, fieldnames=list(results["chart_rows"][0]))
        writer.writeheader()
        writer.writerows(results["chart_rows"])
    print("coverage totals:", results["analysis"]["contact_coverage"]["total_exposures"])
    print("birth-time sensitivity offsets:", len(results["stability"]["offset_summaries"]))
    print(
        "geometry parity mismatches:",
        len(results["analysis"]["angle_geometry_parity"]["mismatches"]),
    )


if __name__ == "__main__":
    main()
