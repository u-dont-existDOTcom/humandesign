#!/usr/bin/env python3
"""Regenerate traceable source-label examples without inspecting any human events."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.solar_time_keys import (
    SolarRAEngine,
    SolarTimeKey,
    apply_solar_key,
)
from hdmatch.astrology.source_witness_scope import placidus_1814_role_assessment
from hdmatch.astrology.timeline import generate_timeline

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)
at = datetime(2000, 1, 1, 12, tzinfo=UTC)
sky = snapshot_from_swiss_files(at, latitude_deg=45, longitude_east_deg=0, ephemeris_directory=EPHE)
engine = SolarRAEngine(sky, EPHE)
geometry = generate_timeline(sky, max_age_years=125).to_dict()
frozen = ROOT / "docs/astrology-research-map/gansten-solar-time-keys-20261024/examples"
records = {}
for profile, name in (
    (SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY, "synthetic_2000_brahe_birth_day.json"),
    (SolarTimeKey.PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA, "synthetic_2000_placidus_true_ra.json"),
):
    prior = json.loads((frozen / name).read_text())
    current = apply_solar_key(geometry, engine, profile, requested_max_age=100)
    assert current["directions"] == prior["directions"]
    assert current["coverage"] == prior["coverage"]
    records[profile.value] = {
        "source_scope": current["solar_time_key"]["primary_source_scope"],
        "contact_count": len(current["directions"]),
        "original_numeric_contact_SHA256": hashlib.sha256(
            json.dumps(current["directions"], sort_keys=True).encode()
        ).hexdigest(),
        "frozen_prior_file_SHA256": hashlib.sha256((frozen / name).read_bytes()).hexdigest(),
        "source_metadata_changed_not_numbers": True,
    }
evidence = json.loads((HERE / "SOURCE_WITNESS_AUDIT.json").read_text())
p_record = placidus_1814_role_assessment(
    "zodiacal_promissor_ray", "traditional_role_reversed_converse"
)
out = {
    "schema": "SOLAR_KEY_PRIMARY_TEXT_SOURCE_SCOPE_REGRESSION_V1",
    "date": "2026-10-24",
    "synthetic_natal": "2000-01-01T12:00Z, 45N 0E; not a person's birth data",
    "historical_witnesses": [w["id"] for w in evidence["source_evidence_classes"]],
    "before_after_by_key": records,
    "explicit_placidus_converse_zodiacal_prohibition": p_record.to_dict(),
    "research_state": (
        "source provenance corrected; historical method completeness and empirical validity OPEN"
    ),
}
(HERE / "SOURCE_SCOPED_SYNTHETIC_CHECK.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + "\n"
)
print(
    json.dumps(
        {
            "status": "PASS",
            "profiles": {k: v["contact_count"] for k, v in records.items()},
            "historical_source_rule": p_record.status.value,
        },
        indent=2,
    )
)
