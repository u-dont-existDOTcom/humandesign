#!/usr/bin/env python3
"""Reproducible development + later fixed holdout comparison, mathematics only."""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from collections.abc import Iterator
from pathlib import Path
from typing import Any, cast

from hdmatch.astrology.geometry import EquatorialPoint, GeometryMethod, direction_arc
from hdmatch.astrology.regio_pole_independent import independent_regio_pole_arc

HERE = Path(__file__).resolve().parent
PRECOMMIT = HERE / "REGIO_INDEPENDENT_PARITY_PRECOMMIT.json"


def canonical(obj: object) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def source_contract() -> dict[str, Any]:
    data = json.loads(PRECOMMIT.read_text(encoding="utf-8"))
    sample = data["sample"]
    if data["schema"] != "ARGOLI_1667_KOLEV_2004_REGIO_GEOMETRY_PARITY_PRECOMMIT_V1":
        raise ValueError("unexpected historical research contract")
    if sample["seed"] != 2004 or sample["count"] != 1200:
        raise ValueError("changed already-examined developmental panel")
    holdout = sample["new_unseen_mathematical_holdout"]
    if holdout["seed"] != 20261026 or holdout["count"] != 800:
        raise ValueError("changed precommitted mathematical holdout")
    if not sample["development_seed_already_run_in_exploratory_scratch_before_protocol_commit"]:
        raise ValueError("scratch developmental exposure must be disclosed")
    original = (
        HERE
        / "primary_1667_volume"
        / "Andrea_Argoli_Primi_Mobilis_Tabulae_1667_original_partial_volume.pdf"
    )
    if hashlib.sha256(original.read_bytes()).hexdigest() != (
        "b3f93054d64c3ca4318ffaec84e8b7161cdc79d6474bb300efd10787b743df1d"
    ):
        raise ValueError("original historical PDF witness changed")
    return cast(dict[str, Any], data)


def sample(
    seed: int, count: int
) -> Iterator[tuple[float, float, EquatorialPoint, EquatorialPoint]]:
    rng = random.Random(seed)
    for _ in range(count):
        yield (
            rng.uniform(-55, 55),
            rng.uniform(0, 360),
            EquatorialPoint(rng.uniform(0, 360), rng.uniform(-25, 25)),
            EquatorialPoint(rng.uniform(0, 360), rng.uniform(-25, 25)),
        )


def circular_error(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def compare_sample(seed: int, count: int) -> dict[str, Any]:
    quadrant_counts: Counter[str] = Counter()
    highest_error = 0.0
    high_count = 0
    for latitude, meridian, fixed, moving in sample(seed, count):
        under_pole = independent_regio_pole_arc(latitude, meridian, fixed, moving)
        vector = direction_arc(
            GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE,
            latitude,
            meridian,
            fixed,
            moving,
        )
        error = circular_error(under_pole.forward_arc_deg, vector)
        highest_error = max(highest_error, error)
        quadrant_counts[under_pole.quadrant] += 1
        high_count += int(error > 1e-8)
    if sum(quadrant_counts.values()) != count:
        raise AssertionError("synthetic case denominator changed")
    if len(quadrant_counts) != 4 or high_count:
        raise AssertionError("independent mathematical parity failed")
    return {
        "seed": seed,
        "synthetic_coordinate_cases": count,
        "quadrant_counts": dict(sorted(quadrant_counts.items())),
        "max_circular_arc_error_degrees": highest_error,
        "cases_exceeding_1e_minus_8_deg": high_count,
        "statistical_or_human_accuracy": "NOT_MEASURED",
    }


def build() -> dict[str, Any]:
    contract = source_contract()
    src = contract["lilly_example"]
    fixed = EquatorialPoint(src["sig_ra_deg"], src["sig_dec_deg"])
    prom = EquatorialPoint(src["prom_ra_deg"], src["prom_dec_deg"])
    latitude = src["latitude_north_deg"]
    ramc = src["ramc_deg"]
    constructed = independent_regio_pole_arc(latitude, ramc, fixed, prom)
    compare = {
        method.value: direction_arc(method, latitude, ramc, fixed, prom)
        for method in GeometryMethod
    }
    worked = {
        "input": {
            "latitude_deg": latitude,
            "ramc_deg": ramc,
            "significator_RA": fixed.ra_deg,
            "significator_dec": fixed.dec_deg,
            "promissor_RA": prom.ra_deg,
            "promissor_dec": prom.dec_deg,
        },
        "independent_under_pole": constructed.to_dict(),
        "published_kolev_arc_degrees": src["reference_arc_deg"],
        "absolute_error_from_published_rounded_arc_degrees": abs(
            constructed.forward_arc_deg - src["reference_arc_deg"]
        ),
        "other_method_arcs": compare,
        "regio_vector_equivalence_error_degrees": circular_error(
            constructed.forward_arc_deg,
            compare[GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE.value],
        ),
        "rounding_tolerance_degrees": src["rounding_tolerance_deg"],
    }
    if worked["absolute_error_from_published_rounded_arc_degrees"] > src["rounding_tolerance_deg"]:
        raise AssertionError("published worked source example beyond stated rounding")
    sample_spec = contract["sample"]
    holdout = sample_spec["new_unseen_mathematical_holdout"]
    developmental = compare_sample(sample_spec["seed"], sample_spec["count"])
    new_holdout = compare_sample(holdout["seed"], holdout["count"])
    return {
        "schema": "ARGOLI_1667_KOLEV_REGIO_INDEPENDENT_MATH_PARITY_V1",
        "date": "2026-10-25",
        "status": "TWO_MATHEMATICAL_PARITY_PANELS_NOT_HUMAN_ASTROLOGY_VALIDATION",
        "contract_sha256": hashlib.sha256(PRECOMMIT.read_bytes()).hexdigest(),
        "history": {
            "source_family": "Regiomontanian fictitious pole/position circles",
            "1610_exact_algorithm_authenticated": False,
            "1667_original_family_illustrated": True,
            "modern_formula_is_kolev_secondary": True,
            "source_1610_later_1667_table_variant_reconciled": False,
            "human_accuracy": "UNTESTED",
        },
        "published_worked_example": worked,
        "development_1200_seed2004": {
            **developmental,
            "note": (
                "Development seed was examined in scratch BEFORE precommit; "
                "not an untouched validation set."
            ),
        },
        "new_fixed_800_seed20261026": {
            **new_holdout,
            "note": (
                "New 800 synthetic coordinate cases first executed after "
                "protocol/code/tests published; independent geometric arithmetic only."
            ),
        },
        "human_birth_or_event_records_read": False,
        "recomputed_full_astrology_chart_or_events": False,
        "owner_root_combined_forward_blind_validation": "OPEN",
    }


def save_once() -> None:
    out = HERE / "POSITION_CIRCLE_PARITY_REPORT.json"
    if out.exists():
        raise FileExistsError("the immutable mathematical result is already present")
    result = build()
    out.write_text(canonical(result), encoding="utf-8")
    print(
        "Development 1200 max discrepancy",
        result["development_1200_seed2004"]["max_circular_arc_error_degrees"],
    )
    print(
        "Frozen-new holdout 800 max discrepancy",
        result["new_fixed_800_seed20261026"]["max_circular_arc_error_degrees"],
    )
    print(
        "Kolev source example degree error",
        result["published_worked_example"]["absolute_error_from_published_rounded_arc_degrees"],
    )


if __name__ == "__main__":
    save_once()
