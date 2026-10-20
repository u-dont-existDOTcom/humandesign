#!/usr/bin/env python3
"""Strict chart-feature support / hour-branch sensitivity, synthetic only.

A methodological abstraction of four historical original Chinese source
anchors, not a traditional Zi Wei co-star interpretation or a horoscope.

Reuse the independently pinned earlier accepted original 312 comparison
oracle and its audited SHA+source labels. Never claim any human prediction.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UP = ROOT / "tasks/astro-chart-eligibility-20261020"
sys.path.insert(0, str(UP))
import audit_synthetic_natal_feature_coverage as oracle  # noqa: E402

OUTPUT = HERE / "FOUR_ANCHOR_SOURCE_FEATURE_HOUR_SENSITIVITY_V1.json"
PREVIOUS = UP / "SYNTHETIC_CHART_FOUR_ANCHOR_ELIGIBILITY_AUDIT_V1.json"
PREVIOUS_SHA = "f571b1c17db513f868bc2e645fb2a51ee21f91e5a287537f4e733a6d998f2c99"
UP_CODE = UP / "audit_synthetic_natal_feature_coverage.py"
UP_CODE_SHA = "1e114ccb205569feea91b250461cdc4f7c36f0b6b644252cf0d1a6a451c68080"
BRANCHES = ("Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai")
SELECTED = ("LianZhen", "PoJun", "TianLiang", "WuQu")
STATUS = (
    "ABSTAIN_NO_SELECTED_STAR",
    "ABSTAIN_TWO_SELECTED_STARS",
    "ABSTAIN_OTHER_PRINCIPAL_STAR_PRESENT",
    "ABSTAIN_SELECTED_SOLE_BUT_VENDOR_SCHOOL_DISAGREES",
    "CONDITIONAL_SOURCE_CALCULATION_AGREES_NOT_HUMAN_PREDICTION",
)
CURRENT_SHA = "dbfa03e27827b86404d052ecdbffbec791e9ea74"


def sha(b: bytes) -> str:
    return sha256(b).hexdigest()


def fail(s: str) -> None:
    raise ValueError("Conservative source feature/hour-sensitivity audit: " + s)


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def check_predecessor():
    if sha(PREVIOUS.read_bytes()) != PREVIOUS_SHA or sha(UP_CODE.read_bytes()) != UP_CODE_SHA:
        fail("accepted prior synthetic source eligibility report or checker changed")
    r = read(PREVIOUS)
    if (
        r["strict_sole_model_eligible_cases"] != 12
        or r["strict_sole_model_abstentions"] != 108
        or r["unique_source_chart_coverage_counts"]["unique_source_chart_states"] != 120
    ):
        fail("prior source eligibility audit expected 12/120 structural model drift")
    if r["empirical_human_chart_predictions_validated"] != 0:
        fail("parent source audit cannot claim human astrology evidence")
    return r


def life_stars(s: dict) -> tuple[str, ...]:
    original = s["star_palaces"]
    return tuple(sorted(name for name, loc in original.items() if loc == s["life_palace"]))


def classify(stars: tuple[str, ...], all_vendor_match: bool) -> str:
    selected = tuple(s for s in stars if s in SELECTED)
    if not selected:
        return STATUS[0]
    if len(selected) > 1:
        return STATUS[1]
    if len(stars) > 1:
        return STATUS[2]
    if not all_vendor_match:
        return STATUS[3]
    return STATUS[4]


def grouped_source_cases(data: dict) -> dict:
    if data.get("preregistered_blinded_real_person_tests") != 0:
        fail("original accepted oracle comparison contains fake real-human claim")
    grouped = defaultdict(list)
    for row in data["all_312_case_records"]:
        oracle.verify_parity_record(row)
        s = row["source_case"]
        grouped[(s["gregorian_reference_date"], s["hour_branch"])].append(row)
    if len(grouped) != 120:
        fail("historical source benchmark should have precisely 120 deduped states")
    canonical = {}
    for key, rows in grouped.items():
        if any(
            oracle.chart_signature(x["source_case"])
            != oracle.chart_signature(rows[0]["source_case"])
            for x in rows
        ):
            fail("source vendor/sex duplicates changed the source geometry")
        allmatch = all(x["match"] for x in rows)
        state = rows[0]["source_case"]
        stars = life_stars(state)
        label = classify(stars, allmatch)
        canonical[key] = {
            "synthetic_reference_date": key[0],
            "Earthly_hour_branch": key[1],
            "major_stars_in_Life_palace": list(stars),
            "selected_candidate_stars_in_Life_palace": [x for x in stars if x in SELECTED],
            "source_original_leap_month": state["is_leap_month"],
            "source_qualified_mechanics": any(
                x["source_case"]["source_status"] == "qualified_source_variant" for x in rows
            ),
            "original_calendar_school": "transmitted Quan Shu lunar New Year and always-next leap",
            "number_of_independent_vendor_comparisons": len(rows),
            "all_vendor_variants_match_source": allmatch,
            "any_vendor_variant_matches_source": any(x["match"] for x in rows),
            "toy_model_rule_status": label,
            "is_actual_calculated_human_birth_chart": False,
            "is_original_behavioral_validity_evidence": False,
        }
    if len({x["synthetic_reference_date"] for x in canonical.values()}) != 10:
        fail("expected exactly ten purposively sampled calendar dates")
    return canonical


def adjacent_day_status(cases: dict, key: tuple[str, str], delta: int) -> dict:
    """Same synthetic reference date, adjacent Earthly two-hour branch.

    At Zi/Hai wraps the actual calendar day would change; mark those rows
    as NOT a physically adjacent birth-time test. Never silently call a
    wrapped same-day synthetic chart an actual adjacent birth instant.
    """
    date, branch = key
    index = BRANCHES.index(branch)
    crossing = index + delta not in range(12)
    nbranch = BRANCHES[(index + delta) % 12]
    neighbor = cases[(date, nbranch)]
    result = {
        "neighbor_hour_branch": nbranch,
        "cyclic_same_reference_date_only": True,
        "actual_chronological_adjacent_hour_check_invalid_at_midnight_wrap": crossing,
        "neighbor_toy_status": neighbor["toy_model_rule_status"],
        "neighbor_selected_stars": neighbor["selected_candidate_stars_in_Life_palace"],
        "neighbor_full_major_stars": neighbor["major_stars_in_Life_palace"],
        "same_strict_supported_star_and_school": False,
    }
    own = cases[key]
    result["same_strict_supported_star_and_school"] = (
        not crossing
        and own["toy_model_rule_status"] == STATUS[4]
        and neighbor["toy_model_rule_status"] == STATUS[4]
        and own["selected_candidate_stars_in_Life_palace"]
        == neighbor["selected_candidate_stars_in_Life_palace"]
    )
    return result


def audit(data: dict) -> dict:
    check_predecessor()
    if (
        data["synthetic_cases"] != 312
        or len(data["all_312_case_records"]) != 312
        or data["chosen_original_leap_rule"]
        != "transmitted Quan Shu leap month always counts as following month"
    ):
        fail("source school, case IDs or count unsupported")
    cases = grouped_source_cases(data)
    tally = Counter(x["toy_model_rule_status"] for x in cases.values())
    expected = {STATUS[0]: 86, STATUS[1]: 3, STATUS[2]: 19, STATUS[3]: 2, STATUS[4]: 10}
    if dict(tally) != expected:
        fail(f"original source coverage no longer agrees with historical audit {dict(tally)}")
    strict = []
    robust = Counter()
    for key in sorted(cases):
        x = cases[key]
        if x["toy_model_rule_status"] not in (STATUS[3], STATUS[4]):
            continue
        before = adjacent_day_status(cases, key, -1)
        after = adjacent_day_status(cases, key, 1)
        matching_nonwrap = (
            not before["actual_chronological_adjacent_hour_check_invalid_at_midnight_wrap"]
            and not after["actual_chronological_adjacent_hour_check_invalid_at_midnight_wrap"]
        )
        stable_pure = (
            x["selected_candidate_stars_in_Life_palace"]
            == before["neighbor_selected_stars"]
            == after["neighbor_selected_stars"]
            and x["major_stars_in_Life_palace"]
            == before["neighbor_full_major_stars"]
            == after["neighbor_full_major_stars"]
        )
        case = {
            "synthetic_reference_date": key[0],
            "synthetic_selected_hour_branch": key[1],
            "original_selected_star": x["selected_candidate_stars_in_Life_palace"][0],
            "source_vendor_all_comparisons_match": x["all_vendor_variants_match_source"],
            "strict_source_without_vendor_agreement": x["toy_model_rule_status"] == STATUS[3],
            "previous_two_hour_Earthly_Branch_at_same_reference_day": before,
            "next_two_hour_Earthly_Branch_at_same_reference_day": after,
            "both_neighbors_nonwrapping": matching_nonwrap,
            "same_full_one_selected_star_with_both_neighbors": stable_pure,
            "both_neighbor_source_calculation_conditional_eligible": before[
                "same_strict_supported_star_and_school"
            ]
            and after["same_strict_supported_star_and_school"],
        }
        strict.append(case)
        robust["strict_source_only_candidates"] += 1
        robust["nonwrapping_2_neighbor_checks"] += matching_nonwrap
        robust["cyclic_full_star_stable_with_both_neighbors"] += stable_pure
        robust["both_neighbor_source_oracle_eligible"] += case[
            "both_neighbor_source_calculation_conditional_eligible"
        ]
        robust["at_least_one_calendar_wrap_neighbor"] += not matching_nonwrap
        if x["toy_model_rule_status"] == STATUS[4]:
            robust["both_source_vendor_matched_at_chosen_branch"] += 1
    if len(strict) != 12 or dict(robust) != {
        "strict_source_only_candidates": 12,
        "nonwrapping_2_neighbor_checks": 10,
        "cyclic_full_star_stable_with_both_neighbors": 0,
        "both_neighbor_source_oracle_eligible": 0,
        "at_least_one_calendar_wrap_neighbor": 2,
        "both_source_vendor_matched_at_chosen_branch": 10,
    }:
        fail(f"source hour-neighbor sensitivity counts changed: {dict(robust)}")
    return {
        "schema": "HUMANDESIGN_ASTROLOGY_FOUR_ANCHOR_HOUR_BRANCH_STRICT_SUPPORT_AUDIT_V1",
        "status": (
            "SYNTHETIC_METHOD_ABSTENTION_AND_HOUR_BRANCH_SENSITIVITY_NOT_ASTROLOGY_PREDICTION"
        ),
        "prior_audited_research_branch_commit": CURRENT_SHA,
        "prior_original_source_eligibility_AUDIT_SHA256": PREVIOUS_SHA,
        "prior_audit_python_SHA256": UP_CODE_SHA,
        "source_original_vendor_oracle_commit": oracle.PARITY_COMMIT,
        "source_original_vendor_oracle_312_fixture_SHA256": oracle.PARITY_SHA,
        "source_four_question_provisional_mapping_sha256": oracle.SOURCE_MAPPING_SHA,
        "original_source_school_precommitted_for_mechanics_only": (
            "transmitted Quan Shu leap month always counts as following month"
        ),
        "source_mutually_qualifying_star_rules_expert_collated": False,
        "unique_synthetic_source_states": 120,
        "actual_people_charted": 0,
        "real_human_forward_or_reverse_predictions_validated": 0,
        "human_questionnaire_responses_collected": 0,
        "independent_natal_civil_to_lunar_time_pipeline_integrated": False,
        "source_original_chinese_astrology_historic_truth": False,
        "conditional_model_status_definition": list(STATUS),
        "synthetic_source_state_counts_by_exclusive_status": dict(tally),
        "conditional_source_mechanics_only_candidate_count": 10,
        "conditional_source_mechanics_only_candidate_star_count": {
            star: sum(
                x["toy_model_rule_status"] == STATUS[4]
                and x["selected_candidate_stars_in_Life_palace"] == [star]
                for x in cases.values()
            )
            for star in SELECTED
        },
        "source_only_non_vendor_corrob_leap_cases": 2,
        "strict_methodological_abstentions_from_120_synthetic_states": 110,
        "all_120_synthetic_states": {"|".join(key): value for key, value in sorted(cases.items())},
        "neighbor_Earthly_hour_branch_stress_test_summary": dict(robust),
        "all_12_strict_source_only_cases_neighboring_branch_checks": strict,
        "near_Zi_Hai_midnight_calendar_day_wrap_invalid_as_real_clock_adjacent": True,
        "birth_time_uncertainty_must_be_propagated_without_hour_selection": True,
        "neighboring_branch_difference_not_equal_real_clock_uncertainty_probability": True,
        "sampled_dates_not_population_prevalence": True,
        "original_text_source_trait_conditional_modifiers_not_resolved": True,
        "no_selected_star_does_not_predict_trait_absence": True,
        "no_personal_medical_gender_moral_predictions_authorized": True,
        "real_natal_chart_scoring_approved": False,
        "production_astro_rule_promotions": 0,
    }


def run() -> dict:
    data = oracle.load_pinned_parity_data()
    report = audit(data)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    report = run()
    print(
        json.dumps(
            {
                "exclusive_status_counts": report[
                    "synthetic_source_state_counts_by_exclusive_status"
                ],
                "neighboring_hour_checks": report[
                    "neighbor_Earthly_hour_branch_stress_test_summary"
                ],
                "actual_human_predictions": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
