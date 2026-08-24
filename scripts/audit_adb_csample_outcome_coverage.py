#!/usr/bin/env python3
"""Audit Astro-Databank C-sample phenotype coverage without astronomy.

This is intentionally an outcome-only eligibility step.  It reports source
quality, timed-record eligibility, and counts for predeclared activity/energy
categories, but never calculates 5-15 or any other birth-derived predictor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from hdmatch.human.astrodatabank_export import iter_astrodatabank_export

TARGET_CATEGORIES = {
    1: "Traits : Body : Constitution hardy",
    2: "Traits : Body : Constitution sensitive",
    3: "Traits : Body : Aerobic exercise",
    85: "Traits : Personality : Active",
    96: "Traits : Personality : Fiery",
    97: "Traits : Personality : Juggles lots at once",
    103: "Traits : Personality : Passive/ Bland",
    1929: "Traits : Personality : Hard worker",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, dest="input_path")
    parser.add_argument("--output", required=True, type=Path, dest="output_path")
    args = parser.parse_args()

    total = 0
    by_rating: Counter[str] = Counter()
    public_aa_a_timed = 0
    alternative_birth_data = 0
    eligible = 0
    category_counts: Counter[int] = Counter()
    personality_coded = 0
    short_biography_present = 0

    for record in iter_astrodatabank_export(args.input_path):
        total += 1
        by_rating[record.rodden_rating] += 1
        if record.has_alternative_birth_data:
            alternative_birth_data += 1
        if (
            record.rodden_rating in {"AA", "A"}
            and record.data_type == "Public Figure"
            and record.birth_utc is not None
        ):
            public_aa_a_timed += 1
        if not record.is_primary_timed_public_record:
            continue
        eligible += 1
        if record.short_biography:
            short_biography_present += 1
        if any(item.text.startswith("Traits : Personality :") for item in record.categories):
            personality_coded += 1
        ids = {item.cat_id for item in record.categories}
        for cat_id in TARGET_CATEGORIES:
            if cat_id in ids:
                category_counts[cat_id] += 1

    payload = {
        "schema": "adb-csample-outcome-coverage-v1",
        "phase": "VALIDATION_ELIGIBILITY_OUTCOME_ONLY",
        "astronomical_predictor_calculated": False,
        "input_sha256": _sha256_file(args.input_path),
        "records_total": total,
        "records_by_rodden_rating": dict(sorted(by_rating.items())),
        "public_aa_a_timed_before_alt_exclusion": public_aa_a_timed,
        "records_with_alternative_birth_data": alternative_birth_data,
        "primary_birth_eligible_records": eligible,
        "eligible_with_short_biography": short_biography_present,
        "eligible_with_any_personality_category": personality_coded,
        "target_category_counts": {
            str(cat_id): {
                "label": label,
                "count": category_counts[cat_id],
            }
            for cat_id, label in TARGET_CATEGORIES.items()
        },
        "interpretation_rule": (
            "Use these marginal outcome counts only to decide whether a prespecified phenotype "
            "has enough coverage for a useful external test. Do not calculate or inspect 5-15 "
            "until the external outcome definition and analysis are frozen."
        ),
    }
    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    args.output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"OUTCOME_COVERAGE_OK:{eligible}")
    print(f"OUTPUT:{args.output_path}")
    return 0


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
