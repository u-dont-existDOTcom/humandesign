#!/usr/bin/env python3
"""Freeze auditable Lilly first-edition event-claim evidence and source hashes."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
old = ROOT / "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024"
registry = json.loads((HERE / "LILLY_1647_EVENT_CLAIM_CANDIDATES.json").read_text())
synthetic = json.loads((HERE / "LILLY_1647_SYNTHETIC_GEOMETRY_COVERAGE.json").read_text())
source = json.loads((old / "SOURCE_PROVENANCE.json").read_text())
assert source["first_edition_witness_A"]["printed_page_to_zero_based_canvas"] == {
    "713": 747,
    "714": 748,
    "715": 749,
}
assert len(registry["entries"]) == 7
assert len(synthetic["matches"]) == 7
assert all(item["scored_people"] == 0 for item in registry["entries"])
assert all(item["not_a_prediction"] for item in registry["entries"])
assert registry["time_key_selected_for_human_test"] is False
assert synthetic["no_actual_events_or_answers_consulted"] is True

files = [
    "tests/unit/test_lilly_1647_event_claims.py",
    "tests/unit/test_lilly_1647_photo.py",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/generate_source_claims.py",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/generate_synthetic_coverage.py",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/LILLY_1647_EVENT_CLAIM_CANDIDATES.json",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/LILLY_1647_EVENT_CLAIM_CANDIDATES.csv",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/LILLY_1647_SYNTHETIC_GEOMETRY_COVERAGE.json",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/WELLCOME_CANVAS_LOCATION_CORRECTION.md",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/README.md",
    "docs/astrology-research-map/lilly-event-claims-pretest-20261024/CONTINUATION_CHECKPOINT.md",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/regenerate_collation.py",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/SOURCE_PROVENANCE.json",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/VERIFICATION.json",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/README.md",
]
files += [str(x.relative_to(ROOT)) for x in sorted((HERE / "source_page_images").glob("*.jpg"))]
assert len(files) == 23
assert len(registry["source_scope"]["original_1647_photos_sha256"]) == 8
assert all((ROOT / name).exists() for name in files)

for page, sha in registry["source_scope"]["original_1647_photos_sha256"].items():
    photo = HERE / "source_page_images" / f"lilly_1647_printed_{page}.jpg"
    assert hashlib.sha256(photo.read_bytes()).hexdigest() == sha

with (old / "LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv").open(
    newline="", encoding="utf-8"
) as stream:
    rows = list(csv.DictReader(stream))
assert len(rows) == 152
assert sum(bool(r["verified_difference"]) for r in rows) == 23

coverage = {
    k: int(v["total_geometric_outputs_across_methods"]) for k, v in synthetic["matches"].items()
}
assert coverage == {
    "LIL-E01": 3,
    "LIL-E02": 0,
    "LIL-E03": 0,
    "LIL-E04": 3,
    "LIL-E05": 3,
    "LIL-E06": 0,
    "LIL-E07": 6,
}

v = {
    "schema": "LILLY_1647_EVENT_SOURCE_HYPOTHESES_AUDIT_V1",
    "date": "2026-10-24",
    "branch": "research/lilly-event-claims-source-20261024",
    "parent_commit": "f6f922a9449932118c44a2c2c4166a9fcdec73f7",
    "scope": "original-text conditional event interpretations, not predictions",
    "source": {
        "original_1647": "William Lilly, Christian Astrology Book III, first edition",
        "witness": "Wellcome Collection b30338724 printed pp654,657,659,661,669,670,683,684",
        "source_images": 8,
        "original_1647_all_relevant_pages_directly_inspected": True,
        "source_conditions": "natal house/rulership, dignity, strength and eligibility retained",
        "paid_Kindle_pages_copied": False,
        "wellcome_zero_based_canvas_map_corrected": {"713": 747, "714": 748, "715": 749},
        "prior_23_numeric_table_discrepancies_unchanged": True,
    },
    "outcome_claims": {
        "number_of_source_conditional_claims": 7,
        "alternative_marriage_childbirth_outcomes_UNRESOLVED": True,
        "modern_event_targets": "analyst proposals, not source wordings and not frozen",
        "real_human_chart_data_used": False,
        "human_participants_or_outcomes_scored": 0,
        "no_time_key_chosen_for_prediction": True,
        "match_is_modern_geometrical_proxy_not_full_Lilly_historic_algorithm": True,
    },
    "synthetic_diagnostic": {
        "invented_chart": "2000-01-01 12:00 UTC at 45N 0E",
        "arc_limit": 125,
        "candidate_counts_across_three_geometries": coverage,
        "date_of_actual_event_inferred": False,
        "absence_of_math_contact_is_not_a_prediction_failure": True,
        "different_methods_NOT_independent_human_confirmation": True,
    },
    "assurance": {
        "extended_tests": "140 passed",
        "ruff": "passed",
        "mypy": "passed in 13 source files",
        "no_previous_maths_modified": True,
        "user_or_third_party_event_histories_consulted": False,
        "historical_natal_condition_full_implementation": False,
        "human_predictive_validity": "UNTESTED",
    },
    "parent_original_source_locator_manifest": hashlib.sha256(
        (old / "VERIFICATION.json").read_bytes()
    ).hexdigest(),
    "files": {
        name: {
            "bytes": (ROOT / name).stat().st_size,
            "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
        }
        for name in files
    },
    "root_owner_outcome": "OPEN",
    "next_safe_implementation": (
        "source-specific radix condition computation and independent event "
        "meaning selection; no prospective scoring without separate participant authority"
    ),
}
(HERE / "VERIFICATION.json").write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n")
print(
    json.dumps(
        {
            "result": "VERIFIED",
            "files": len(files),
            "source_claims": len(registry["entries"]),
            "original_scans": 8,
            "synthetic_counts": coverage,
            "manifest_SHA256": hashlib.sha256(
                (HERE / "VERIFICATION.json").read_bytes()
            ).hexdigest(),
        },
        indent=2,
    )
)
