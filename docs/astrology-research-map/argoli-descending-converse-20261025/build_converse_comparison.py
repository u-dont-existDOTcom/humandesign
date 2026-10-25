#!/usr/bin/env python3
"""Non-empirical, source-bound Argoli 1610 converse-arc research.

Constructs 500 EXPLORATORY + 400 separately precommitted new synthetic
coordinate comparisons; do not call either panel human validation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import statistics
from pathlib import Path
from typing import Any

from hdmatch.astrology.argoli_1610_direction_conventions import (
    source_motivated_converse_comparison,
    wrapped_source_arc,
)
from hdmatch.astrology.geometry import EquatorialPoint

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT = HERE / "SOURCE_METHOD_ALIGNMENT.json"
REPORT = HERE / "CONVERSE_SOURCE_AND_GEOMETRY_REPORT.json"
CASES = HERE / "CONVERSE_SYNTHETIC_COORDINATE_CASES.csv"


def canonical(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def source_check() -> dict[str, Any]:
    s = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if s["schema"] != "ARGOLI_1610_1667_DESCENDING_CONVERSE_SOURCE_V1":
        raise ValueError("unexpected Argoli source contract")
    for witness in s["original_source_files"]:
        path = HERE / witness["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != witness["sha256"]:
            raise ValueError("original page witness mismatch: " + str(path))
    iiif = ROOT / s["first_editions"]["1610"]["institutional_manifest"]
    if (
        hashlib.sha256(iiif.read_bytes()).hexdigest()
        != s["first_editions"]["1610"]["manifest_sha256"]
    ):
        raise ValueError("institutional 1610 IIIF manifest mismatch")
    original = s["first_editions"]["1667"]["original_pdf"]
    if (
        hashlib.sha256((ROOT / original).read_bytes()).hexdigest()
        != s["first_editions"]["1667"]["original_pdf_sha256"]
    ):
        raise ValueError("old original Michigan 1667 PDF changed")
    witnesses = s["matched_worked_examples"]
    computed = {}
    for item in witnesses:
        if item["id"] == "SUN_TO_JUPITER_SEXTILE_ALTERNATE_ASCENSION":
            lower = item["correct_subtrahend_in_1610_and_1667_prose"]
        else:
            lower = item["printed_subtrahend"]
        first = item.get("extended_minued", item["printed_minued"])
        actual = wrapped_source_arc(tuple(first), tuple(lower))
        if list(actual) != item["arithmetic_result"]:
            raise ValueError("source arithmetic mismatch: " + item["id"])
        computed[item["id"]] = list(actual)
    if len(witnesses) != 4 or len(s["original_source_files"]) != 11:
        raise ValueError("changed source table denominator")
    typo = next(
        item for item in witnesses if item["id"] == "SUN_TO_JUPITER_SEXTILE_ALTERNATE_ASCENSION"
    )
    literal = wrapped_source_arc(
        tuple(typo["printed_minued"]),
        tuple(typo["misprinted_1667_table_subtrahend"]),
    )
    if list(literal) != typo["arithmetic_if_later_printed_operand_taken_literally"]:
        raise ValueError("reported 1667 106-degrees error changed")
    return {
        "schema": "ARGOLI_1610_1667_SOURCE_NUMERIC_RECONCILIATION_V1",
        "four_matched_worked_direction_arcs": computed,
        "printed_1667_table_subtrahend": [106, 3],
        "correct_subtrahend_both_prose_and_1610": [160, 3],
        "wrong_operand_computed_arc": list(literal),
        "arithmetically_correct_and_printed_1667_arc": [46, 58],
        "wrong_operand_difference_degrees": typo["later_printed_operand_error_degrees"],
        "human_outcomes_evaluated": False,
        "source_1644_status": "UNREAD_429_OR_403",
        "full_historical_converse_validity": "UNRESOLVED",
    }


def _panel(seed: int, count: int, panel_label: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rng = random.Random(seed)
    samples: list[dict[str, Any]] = []
    for i in range(count):
        latitude = rng.uniform(-55, 55)
        ramc = rng.uniform(0, 360)
        significator = EquatorialPoint(rng.uniform(0, 360), rng.uniform(-25, 25))
        promissor = EquatorialPoint(rng.uniform(0, 360), rng.uniform(-25, 25))
        record = source_motivated_converse_comparison(
            latitude,
            ramc,
            significator,
            promissor,
        )
        samples.append(
            {
                "panel": panel_label,
                "i": i + 1,
                "latitude_deg": latitude,
                "ramc_deg": ramc,
                "significator_ra_deg": significator.ra_deg,
                "significator_dec_deg": significator.dec_deg,
                "promissor_ra_deg": promissor.ra_deg,
                "promissor_dec_deg": promissor.dec_deg,
                "direct_deg": record.direct_using_significator_circle_deg,
                "role_swapped_converse_deg": record.converse_using_promissor_circle_deg,
                "naive_reverse_deg": record.naive_360_minus_direct_deg,
                "absolute_difference_deg": record.absolute_difference_converse_vs_naive_deg,
            }
        )
    deltas = [float(row["absolute_difference_deg"]) for row in samples]
    return (
        {
            "panel": panel_label,
            "seed": seed,
            "n": count,
            "method": "regiomontanian_position_circle",
            "n_disagree_over_one_degree": sum(v > 1.0 for v in deltas),
            "n_disagree_over_five_degrees": sum(v > 5.0 for v in deltas),
            "median_absolute_difference_deg": statistics.median(deltas),
            "maximum_absolute_difference_deg": max(deltas),
            "minimum_absolute_difference_deg": min(deltas),
            "claims": "SOURCE_MOTIVATED_MATHEMATICAL_DIAGNOSTIC_NOT_ASTROLOGY_VALIDATION",
        },
        samples,
    )


def build() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    h = source_check()
    contract = json.loads(CONTRACT.read_text())
    dev = contract["exploratory_converse_math_500"]
    if (dev["seed"], dev["n"], dev["status"]) != (
        20261025,
        500,
        "DEVELOPMENT_ALREADY_RUN_BEFORE_CONTRACT",
    ):
        raise ValueError("development-source exposure status was changed")
    held = contract["new_unrun_bounded_math_holdout"]
    if held["prior_outcome"] is not None or held["seed"] != 20261029 or held["n"] != 400:
        raise ValueError("new mathematical holdout not originally frozen")
    development, dev_cases = _panel(dev["seed"], dev["n"], "EXPLORATORY_DEVELOPMENT")
    if (
        development["n_disagree_over_one_degree"] != dev["nonzero_over_one_degree"]
        or development["n_disagree_over_five_degrees"] != dev["nonzero_over_five_degrees"]
    ):
        raise ValueError("exploratory 500-case baseline is not reproducible")
    holdout, held_cases = _panel(held["seed"], held["n"], "AFTER_PRECOMMIT_MATH_HOLDOUT")
    if len(dev_cases) + len(held_cases) != 900:
        raise ValueError("synthetic sample denominator changed")
    return (
        {
            "schema": "ARGOLI_1610_DESCENDING_CONVERSE_GEOMETRY_V1",
            "source_numeric_concordance": h,
            "source_original_first_edition_1610": "BSB, printed p43–47",
            "source_1667_comparison": "Michigan original printed p31–33",
            "human_data_seen": False,
            "predictive_accuracy": "UNTESTED",
            "source_exact_complete_1610_Argoli": "NOT_AUTHENTICATED",
            "later_1667_converse_chapter_presence": "UNKNOWN_OUTSIDE_ALIGNED_SEQUENCE",
            "development": development,
            "mathematical_holdout": holdout,
            "caution": (
                "Role swapping implements a modern Regiomontanian geometry "
                "interpretation of 1610 p47; not a complete author-certified method"
            ),
        },
        dev_cases + held_cases,
    )


def emit_once() -> None:
    if REPORT.exists() or CASES.exists():
        raise FileExistsError("Refusing to overwrite historical math result")
    info, rows = build()
    REPORT.write_text(canonical(info), encoding="utf-8")
    with CASES.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("DEVELOPMENT", info["development"]["n"], "HOLDOUT", info["mathematical_holdout"]["n"])
    print("HOLDOUT_DIFF", info["mathematical_holdout"]["median_absolute_difference_deg"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()
    if args.source_only:
        print("HISTORICAL_SOURCE_ONLY", canonical(source_check())[:400])
    else:
        emit_once()
