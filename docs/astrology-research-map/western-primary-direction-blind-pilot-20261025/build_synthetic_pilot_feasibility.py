#!/usr/bin/env python3
"""Existing 96-chart source exposure feasibility; NO human outcome data."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from hdmatch.astrology.western_forward_blind import (
    SOURCE_CANDIDATES,
    TENTATIVE_PILOT_PRIMARY,
    Contact,
    Interval,
    contact_uncertainty_envelopes,
    measure_intervals,
    sealed_prediction_receipt,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = ROOT / "docs/astrology-research-map/primary-direction-synthetic-panel-20261024"
REPORT = HERE / "SYNTHETIC_PILOT_FEASIBILITY.json"
ADULT = Interval(18.0, 65.0)


def canonical(data: object) -> bytes:
    return (json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def verified_parent() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = json.loads((PARENT / "VERIFICATION.json").read_text())
    loaded: dict[str, Any] = {}
    for name in ("SYNTHETIC_PANEL_EXPOSURES.json", "SYNTHETIC_PANEL_COVERAGE.json"):
        path = PARENT / name
        key = str(path.relative_to(ROOT))
        expected = manifest["archive_inputs"][key]["sha256"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("published synthetic input was modified: " + name)
        loaded[name] = json.loads(path.read_text())
    exposures = loaded["SYNTHETIC_PANEL_EXPOSURES.json"]
    coverage = loaded["SYNTHETIC_PANEL_COVERAGE.json"]
    if len(exposures) != 96 or coverage["contact_coverage"]["total_exposures"] != 216:
        raise ValueError("prior synthetic panel is not the declared 96-chart study")
    return exposures, coverage


def build() -> dict[str, Any]:
    cases, old = verified_parent()
    total_counts: Counter[str] = Counter()
    primary: Counter[str] = Counter()
    charts_with_primary = 0
    all_occupational_exposure_years = 0.0
    for records in cases.values():
        visible = [
            Contact(key=x["key"], rule_id=x["rule_id"], symbolic_age_years=float(x["age"]))
            for x in records
        ]
        envelopes = contact_uncertainty_envelopes({0: visible})
        periods = []
        for window in envelopes:
            total_counts[window.source_rule_id] += 1
            if window.source_rule_id in TENTATIVE_PILOT_PRIMARY and window.timing:
                primary[window.source_rule_id] += 1
                periods.append(window.timing)
        charts_with_primary += bool(periods)
        all_occupational_exposure_years += measure_intervals(periods, ADULT)
    if total_counts != Counter(old["contact_coverage"]["rule_exposure_count"]):
        raise ValueError("older eight-source-rule distribution changed")
    if sum(primary.values()) != 20:
        raise ValueError("published two-primary-source-contact count changed")
    code = ROOT / "src/hdmatch/astrology/western_forward_blind.py"
    dummy = sealed_prediction_receipt(
        pseudonymous_participant_id="SYNTHETIC_ONLY_NO_REAL_PERSON",
        birth_input_sha256=hashlib.sha256(b"NOT_A_REAL_BIRTH_INPUT").hexdigest(),
        chart_features_sha256=hashlib.sha256(b"NOT_A_REAL_CHART").hexdigest(),
        calculation_code_sha256=hashlib.sha256(code.read_bytes()).hexdigest(),
        rules_sha256=hashlib.sha256(canonical(TENTATIVE_PILOT_PRIMARY)).hexdigest(),
        birth_time_quality="unknown_or_rectified",
        windows=(),
        comparison_design_sha256=hashlib.sha256(b"PILOT_NOT_FROZEN").hexdigest(),
    )
    return {
        "schema": "WESTERN_DIAGNOSTIC_PILOT_SYNTHETIC_COVERAGE_V0",
        "status": "PRIOR_96_CHART_DEVELOPMENT_ONLY_NOT_PROSPECTIVE_VALIDATION",
        "existing_frozen_96_synthetic_charts": len(cases),
        "candidate_rule_count": len(SOURCE_CANDIDATES),
        "all_eight_source_candidate_contacts": dict(sorted(total_counts.items())),
        "tentative_two_occupational_contact_counts": dict(sorted(primary.items())),
        "charts_with_any_tentative_occupational_contact": charts_with_primary,
        "eligible_age_domain_years": 47.0,
        "total_unconditional_adult_age_years": len(cases) * 47.0,
        "union_tentative_occupational_exposure_years": all_occupational_exposure_years,
        "fraction_of_unconditional_age_interval_exposed": all_occupational_exposure_years
        / (len(cases) * 47.0),
        "source_window_policy": (
            "single original chart instant, ±0.5 symbolic years, no uncertainty correction"
        ),
        "actual_role_opportunity_or_documented_outcomes": "NONE",
        "source_qualified_historical_prediction_accuracy": "UNTESTED",
        "human_event_rate_or_power": "UNKNOWN",
        "only_privacy_safe_synthetic_commitment_example": dummy,
        "combined_astrology_owner_goal": "OPEN",
    }


if __name__ == "__main__":
    if REPORT.exists():
        raise FileExistsError("do not overwrite existing known-development report")
    result = build()
    REPORT.write_bytes(canonical(result))
    print("synthetic charts", result["existing_frozen_96_synthetic_charts"])
    print("two-domain contacts", sum(result["tentative_two_occupational_contact_counts"].values()))
    print("age coverage fraction", result["fraction_of_unconditional_age_interval_exposed"])
