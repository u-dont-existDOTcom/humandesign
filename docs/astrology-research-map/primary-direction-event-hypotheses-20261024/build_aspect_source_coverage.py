#!/usr/bin/env python3
"""Historical aspect-source coverage on one synthetic chart, not human scoring."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SYNTHETIC = HERE / "synthetic_examples/synthetic_2000_zodiacal_rays.json"
OUTPUT = HERE / "ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json"

# Original first-edition pages were directly read; modern operational implications
# are deliberately distinct from the author's multi-effect descriptions.
RULES = [
    {
        "id": "L1647-MC-SAT-HARD",
        "promissor": "saturn",
        "significator": "mc",
        "aspects": ["square", "opposition"],
        "source_pages": [669],
        "exact_source_excerpt": (
            "deprives him of his former Honour, Office, Magistracy, Employment or Reputation"
        ),
        "candidate_event": "formal loss of occupational office or status",
        "condition_unresolved": "must independently establish prior relevant office",
        "status": "DIRECT_SOURCE_MEANING_MODERN_EVENT_PREDICATE_UNFROZEN",
    },
    {
        "id": "L1647-MC-JUP-SOFT",
        "promissor": "jupiter",
        "significator": "mc",
        "aspects": ["sextile", "trine"],
        "source_pages": [670],
        "exact_source_excerpt": "it elevates him even from the Dunghil",
        "candidate_event": "formal office/promotion, similar to MC-Jupiter body",
        "condition_unresolved": (
            "SOURCE EXPRESSLY REQUIRES JUPITER STRONG IN RADIX; natal-strength algorithm not frozen"
        ),
        "status": "CONDITIONAL_NOT_ELIGIBLE_FOR_HUMAN_SCORING",
    },
    {
        "id": "L1647-ASC-JUP-SOFT",
        "promissor": "jupiter",
        "significator": "asc",
        "aspects": ["sextile", "trine"],
        "source_pages": [658],
        "exact_source_excerpt": "it produces an augmentation of Fortune",
        "candidate_event": "external material patronage or substantial benefit",
        "condition_unresolved": (
            "historical alternatives broad; external-benefit threshold still unfrozen"
        ),
        "status": "SOURCE_ANCHORED_BUT_MODERN_THRESHOLD_UNRESOLVED",
    },
    {
        "id": "L1647-ASC-MARS-HARD",
        "promissor": "mars",
        "significator": "asc",
        "aspects": ["square", "opposition"],
        "source_pages": [660],
        "exact_source_excerpt": "it stirs up many Enemies, many Accusations",
        "candidate_event": "formal adverse accusation/complaint, not all private disagreement",
        "condition_unresolved": (
            "historical claim has many alternative effects; "
            "formal filing is derived and not assured"
        ),
        "status": "EXPLORATORY_MODERN_CONSTRUCT_NOT_READY",
    },
]


def build() -> dict[str, object]:
    source = SYNTHETIC.read_bytes()
    chart = json.loads(source)
    assert chart["scope"]["profile"] == "zodiacal_promissor_rays"
    assert chart["method_provenance"]["time_key"] == "ptolemy_one_degree_per_year"
    assert chart["scope"]["significator_projection"] == "retain_bodily"
    out: list[dict[str, object]] = []
    for rule in RULES:
        matches = [
            record
            for record in chart["directions"]
            if record["promissor"] == rule["promissor"]
            and record["significator"] == rule["significator"]
            and record["ray_aspect"] in rule["aspects"]
            and record["direction"] == "direct"
            and 18 <= record["symbolic_age_years"] < 65
        ]
        groups: dict[tuple[str, str, float], dict[str, object]] = {}
        for record in matches:
            key = (
                record["ray_aspect"],
                record["ray_offset_branch"],
                round(record["symbolic_age_years"], 8),
            )
            group = groups.setdefault(
                key,
                {
                    "aspect": record["ray_aspect"],
                    "branch": record["ray_offset_branch"],
                    "symbolic_age_years": record["symbolic_age_years"],
                    "methods": [],
                },
            )
            group["methods"].append(record["method"])
        deduplicated = sorted(
            groups.values(), key=lambda g: (g["symbolic_age_years"], g["aspect"], g["branch"])
        )
        for g in deduplicated:
            g["methods"] = sorted(set(g["methods"]))
            g["independent_evidence_count"] = 1
        out.append(
            {
                **rule,
                "matched_raw_method_records": len(matches),
                "unique_synthetic_contact_exposures": len(deduplicated),
                "synthetic_contact_groups": deduplicated,
            }
        )
    return {
        "schema": "ASTRO_LILLY_FIRST_EDITION_ASPECT_COVERAGE_V0",
        "status": "SYNTHETIC_COVERAGE_ONLY_NO_FROZEN_PREDICTIONS_NO_HUMAN_VALIDATION",
        "source": "Lilly original 1647 first edition pp.658,669,670,660",
        "source_reading": (
            "visually verified facsimiles; source statements and inferred events kept distinct"
        ),
        "geometry_scope": (
            "zodiacal promissor rays beta=0, retain bodily angles, software direct sense"
        ),
        "note": (
            "One selected synthetic chart, not a representative incidence or "
            "empirical performance estimate; three identical geometric outputs count once."
        ),
        "human_outcome_information_used": False,
        "input_sha256": hashlib.sha256(source).hexdigest(),
        "raw_records_in_full_aspect_timeline": len(chart["directions"]),
        "families": out,
        "total_raw_selected_method_records": sum(x["matched_raw_method_records"] for x in out),
        "total_unique_exposure_groups": sum(x["unique_synthetic_contact_exposures"] for x in out),
        "study_ready": False,
    }


if __name__ == "__main__":
    result = build()
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Synthetic aspect rule groups:", result["total_unique_exposure_groups"])
