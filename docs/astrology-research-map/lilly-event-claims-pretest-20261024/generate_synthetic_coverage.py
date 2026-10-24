"""Pure synthetic-geometry COVERAGE only; no historical prediction scoring.

Uses one invented natal instant unrelated to any participant. The original
angles/geometry are unchanged and no event outcomes are opened. Counts of
method outputs are not independent confirmations of predictive accuracy.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.astrology.role_directions import (
    ContactConstruction,
    RotationRegime,
    generate_role_timeline,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "generate_source_claims.py"
EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)


def main() -> None:
    spec = importlib.util.spec_from_file_location("original1647claimsource", SOURCE)
    assert spec and spec.loader
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    registry = gen.compile_register()

    natal = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    records: list[dict[str, object]] = []
    engine_profiles = []
    for construction in (
        ContactConstruction.BODY_CONJUNCTION,
        ContactConstruction.ZODIACAL_PROMISSOR_RAY,
    ):
        result = generate_role_timeline(
            natal,
            construction=construction,
            regime=RotationRegime.DIRECT_PRIMARY_MOTION,
            max_age_years=125,
        )
        records.extend(x.to_dict() for x in result.directions)
        engine_profiles.append(
            {
                "construction": construction.value,
                "geometries": [x.value for x in result.methods],
                "evaluated": result.evaluated,
                "contacts_accepted_below_125_arc_degrees": len(result.directions),
            }
        )

    matched = {}
    for claim in registry["entries"]:
        candidates = [r for r in records if gen.matches_role_contact(claim, r)]
        matched[claim["claim_id"]] = {
            "candidate_outputs_per_geometry": {
                method: sum(r["method"] == method for r in candidates)
                for method in sorted({r["method"] for r in candidates})
            },
            "total_geometric_outputs_across_methods": len(candidates),
            "has_geometric_contact_in_test_window": bool(candidates),
            "different_geometry_labels_NOT_independent_validation": True,
            "event_occurred_or_ever_asked": None,
        }
    assert len(matched) == 7
    assert sum(v["has_geometric_contact_in_test_window"] for v in matched.values()) == 4
    assert [
        cid for cid, value in matched.items() if not value["has_geometric_contact_in_test_window"]
    ] == ["LIL-E02", "LIL-E03", "LIL-E06"]

    packet = {
        "schema": "LILLY_1647_UNFROZEN_EVENT_CLAIM_SYNTHETIC_COVERAGE_V1",
        "date": "2026-10-24",
        "status": "SYNTHETIC_ENGINE_COVERAGE_NOT_EVENT_PREDICTIONS_OR_HUMAN_EVIDENCE",
        "synthetic_natal": {
            "utc": "2000-01-01T12:00:00+00:00",
            "latitude": 45,
            "longitude_east": 0,
            "made_up_not_personal": True,
        },
        "astronomy_provenance": {
            "verified_Swiss": True,
            "ephemeris_file_SHA256": dict(natal.ephemeris_file_sha256),
        },
        "rule_registry_SHA256": hashlib.sha256(
            (HERE / "LILLY_1647_EVENT_CLAIM_CANDIDATES.json").read_bytes()
        ).hexdigest(),
        "engine_profiles": engine_profiles,
        "arc_limit_degrees": 125,
        "age_time_key_for_human_predictions": "NOT_SELECTED",
        "model_interpretations_frozen": False,
        "no_actual_events_or_answers_consulted": True,
        "no_raw_age_dates_in_this_report": True,
        "counts_are_not_predictive_accuracy": True,
        "zero_pattern_counts_do_not_mean_the_claim_was_falsified": True,
        "matches": matched,
    }
    output = HERE / "LILLY_1647_SYNTHETIC_GEOMETRY_COVERAGE.json"
    output.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
    print(
        "Synthetic-only geometric matches:",
        {k: v["total_geometric_outputs_across_methods"] for k, v in matched.items()},
    )


if __name__ == "__main__":
    main()
