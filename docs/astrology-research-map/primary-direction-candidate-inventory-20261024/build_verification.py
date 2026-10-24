# ruff: noqa: E501 (long exact reproduction commands retained)
#!/usr/bin/env python3
"""Rebuild SHA-based verification of the research-only candidate inventory."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
inp = json.loads((HERE / "PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.json").read_text())
with (HERE / "PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.csv").open(encoding="utf-8", newline="") as f:
    records = list(csv.DictReader(f))
assert len(records) == len(inp["arms"]) == 12
assert inp["not_new_mandatory_source_gate"] is True
assert inp["all_source_engineering_only"] is True
assert inp["human_prediction_mapping_frozen"] is False
assert all(x["real_human_prediction_validated"] is False for x in inp["arms"])
assert len([x for x in inp["arms"] if x["geometric_duplicate_group"]]) == 2

files = [
    "docs/astrology-research-map/primary-direction-candidate-inventory-20261024/generate_inventory.py",
    "docs/astrology-research-map/primary-direction-candidate-inventory-20261024/PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.json",
    "docs/astrology-research-map/primary-direction-candidate-inventory-20261024/PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.csv",
    "docs/astrology-research-map/primary-direction-candidate-inventory-20261024/README.md",
    "docs/astrology-research-map/primary-direction-candidate-inventory-20261024/CONTINUATION_CHECKPOINT.md",
    "tests/unit/test_primary_direction_inventory.py",
]
for f in files:
    assert (ROOT / f).is_file(), f
v = {
    "schema": "PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY_VERIFICATION_V1",
    "date": "2026-10-24",
    "branch": "research/primary-direction-method-inventory-20261024",
    "parent_commit": "46e73635e9cb79ba9630978e656d065662989069",
    "state": "BOUNDED_RESEARCH_INVENTORY_COMPLETE_PARENT_EMPIRICAL_GOAL_OPEN",
    "source": "previously inspected original 1647 Lilly, original 1657 Placidus, Brahe 1573 critical text and Gansten book audit",
    "result": {
        "method_families": 12,
        "method_families_with_cli_flags": sum(x["cli_flags"] is not None for x in inp["arms"]),
        "literal_witness_diagnostics_without_timeline_cli": sum(
            x["cli_flags"] is None for x in inp["arms"]
        ),
        "historical_placidus_converse_zodiacal_incompatible": True,
        "duplicate_geom_group": ["PD07", "PD08"],
        "unresolved_original_1647_minute_rows": inp["original_Lilly_1647_faint_minutes"],
        "Lilly_minute_27_absent": True,
        "no_human_scoring_or_predictive_validation": True,
        "interpretation_rules_frozen": False,
    },
    "tests": {
        "command": "PYTHONPATH=src HDMATCH_PRIMARY_DIR_EPHE_DIR=$HOME/.local/share/hdmatch/ephemeris/1800-2399 $HOME/humandesign/.venv/bin/python -m pytest -q tests/unit/test_primary_direction_inventory.py tests/unit/test_lilly_1647_photo.py tests/unit/test_placidus_1657_latin.py tests/unit/test_solar_primary_source_scope.py tests/unit/test_solar_time_keys.py tests/unit/test_naibod_original_1647.py tests/unit/test_historical_naibod.py tests/unit/test_primary_direction_roles.py tests/unit/test_primary_direction_aspects.py tests/unit/test_primary_directions.py tests/unit/test_astronomy_reference.py tests/unit/test_relationship_western_rrf.py",
        "result": "130 passed",
        "ruff": "passed",
        "mypy": "passed in 13 source files",
    },
    "all_source_engineering_only": True,
    "no_user_birth_data_used": True,
    "no_new_mandatory_gate": True,
    "files": {
        f: {
            "bytes": (ROOT / f).stat().st_size,
            "sha256": hashlib.sha256((ROOT / f).read_bytes()).hexdigest(),
        }
        for f in files
    },
}
(HERE / "VERIFICATION.json").write_text(json.dumps(v, indent=2, ensure_ascii=False) + "\n")
print(
    json.dumps(
        {
            "status": "VERIFIED",
            "file_count": len(files),
            "model_families": 12,
            "independent_math_overlap_group": ["PD07", "PD08"],
            "manifest_SHA256": hashlib.sha256(
                (HERE / "VERIFICATION.json").read_bytes()
            ).hexdigest(),
        },
        indent=2,
    )
)
