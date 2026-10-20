#!/usr/bin/env python3
"""Deterministically create fake test fixtures; ZERO human birth or answer data."""

import json
from pathlib import Path

B = Path(__file__).resolve().parent
CHARTS = [
    ("SYNTH-CHART-01", "武曲"),
    ("SYNTH-CHART-02", "廉贞"),
    ("SYNTH-CHART-03", "天梁"),
    ("SYNTH-CHART-04", "破军"),
]
QUESTIONS = ["Q_DECISIVE", "Q_ARGUMENT", "Q_HELPING", "Q_COMPETE"]
STARS = [star for _, star in CHARTS]


def save(file, obj):
    file.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate():
    charts = {
        "schema": "ASTROLOGY_EXPLICIT_MOCK_CHART_FEATURES_V1",
        "status": "SYNTHETIC_FEATURE_TOKENS_NOT_CALCULATED_BIRTH_CHARTS",
        "there_are_no_birth_dates_times_places_or_real_individuals": True,
        "original_source_model_is_not_a_verified_natal_calculator": True,
        "eligibility": "One fake star per fake Life-palace chart, only for scoring-plumbing tests",
        "declared_nuisance_stratum": "toy_all_equal_not_a_real_demographic_match",
        "charts": [
            {"chart_id": id, "life_palace_main_star_mock": star, "synthetic": True}
            for id, star in CHARTS
        ],
    }
    save(B / "SYNTHETIC_CHART_TOKENS_V1.json", charts)
    for scen in (
        "aligned_positive_control",
        "constant_null_control",
        "deliberately_opposite_control",
    ):
        cases = []
        for i, (chartid, _) in enumerate(CHARTS):
            if scen == "aligned_positive_control":
                vals = [4 if x == i else 0 for x in range(4)]
            elif scen == "constant_null_control":
                vals = [2, 2, 2, 2]
            else:
                vals = [4 if x == (i + 1) % 4 else 0 for x in range(4)]
            cases.append(
                {
                    "case_id": f"SYNTH-P{i + 1:02d}",
                    "true_chart_id": chartid,
                    "mock_responses": dict(zip(QUESTIONS, vals, strict=True)),
                    "synthetic_case": True,
                }
            )
        d = {
            "schema": "ASTROLOGY_EXPLICIT_SYNTHETIC_RESPONSE_BATCH_V1",
            "status": "MOCK_OUTCOMES_CONSTRUCTED_AFTER_DESIGN_FOR_POSITIVE_AND_NULL_TESTS",
            "scenario": scen,
            "real_human_data": False,
            "actual_birth_chart_data": False,
            "cases": cases,
        }
        save(B / f"SYNTHETIC_RESPONSES_{scen.upper()}_V1.json", d)
    print("SYNTHETIC FIXTURES: 4 fake chart tokens, 3 fake response scenarios, 0 DOB")


if __name__ == "__main__":
    generate()
