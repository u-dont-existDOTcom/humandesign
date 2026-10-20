#!/usr/bin/env python3
"""Source-locked audit of four hypothetical Zi Wei Life-palace natal features.

ALL cases come from a previously accepted 312-row SYNTHETIC chart parity
dataset, NEVER actual human chart/birth/behavior measurements.

The saved four-question prototype contains exactly-one-mock-star tokens,
but traditional Life palaces can contain 0, 1, or 2 major stars. This
program audits the risk of its unsupported applicability assumptions.
No scoring/human predictions and no source index edits.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
MAP = (
    ROOT / "tasks/astro-source-four-anchor-synthetic-20261020/SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json"
)
OUTPUT = B / "SYNTHETIC_CHART_FOUR_ANCHOR_ELIGIBILITY_AUDIT_V1.json"
PARITY_COMMIT = "6f4a75febc1624e44b54d724422804a05f31fd12"
PARITY_PATH = (
    "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-12/"
    "IZTRO_2_6_0_FULL_312_CHART_COMPARISON_V1.json"
)
PARITY_SHA = "01efe5181d7c9d07a6c9f780df9d03b557b356baa4ca3770464f38e8552feaa5"
SOURCE_MAPPING_SHA = "acd1fef1b9764bfac4525785ee1fd42e7dac2727880e829ee038aa9562db8a62"
EXPECTED_STARS = (("WuQu", "武曲"), ("LianZhen", "廉贞"), ("TianLiang", "天梁"), ("PoJun", "破军"))
STAR_NAMES = {
    "ZiWei",
    "TianJi",
    "TaiYang",
    "WuQu",
    "TianTong",
    "LianZhen",
    "TianFu",
    "TaiYin",
    "TanLang",
    "JuMen",
    "TianXiang",
    "TianLiang",
    "QiSha",
    "PoJun",
}
EXPECTED_DATES = 10
EXPECTED_HOURS = 12
EXPECTED_ROWS = 312


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(reason: str) -> None:
    raise ValueError("Synthetic source chart audit rejected: " + reason)


def load_pinned_parity_data(override_path: Path | None = None) -> dict:
    if override_path is None:
        proc = subprocess.run(
            ["git", "show", f"{PARITY_COMMIT}:{PARITY_PATH}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
        raw = proc.stdout
    else:
        raw = override_path.read_bytes()
    if len(raw) != 899155 or digest(raw) != PARITY_SHA:
        fail("pinned independent chart oracle case fixture byte count/SHA not verified")
    return json.loads(raw.decode("utf-8"))


def verify_candidates() -> tuple[str, ...]:
    if digest(MAP.read_bytes()) != SOURCE_MAPPING_SHA:
        fail("unchanged source-anchored four-behavior candidate mapping SHA drift")
    source = read(MAP)
    if (
        source.get("score_probabilities_calibrated") is not False
        or source.get("human_predictive_validation_count") != 0
        or source.get("study_has_been_preregistered") is not False
        or source.get("scored_real_human_recruitment_authorized") is not False
    ):
        fail("toy source candidates must remain exploratory and not human-authorized")
    rows = source["candidates"]
    if len(rows) != 4 or set((x["star_roman"], x["star_native"]) for x in rows) != set(
        EXPECTED_STARS
    ):
        fail("unexpected four-star source candidates or altered original mapping")
    if any(x["original_birth_chart_calculator_for_this_condition_verified"] for x in rows):
        fail("unverified natal calculation was promoted in this source map")
    return tuple(sorted(x["star_roman"] for x in rows))


def chart_signature(source: dict) -> tuple:
    keys = {
        "gregorian_reference_date",
        "lunar_year",
        "lunar_month",
        "lunar_day",
        "is_leap_month",
        "hour_branch",
        "source_status",
        "life_palace",
        "body_palace",
        "bureau_number",
        "source_purple_star_provenance",
        "source_bureau_provenance",
        "star_palaces",
        "gender",
        "fix_leap",
    }
    if set(source) != keys:
        fail("synthetic independent engine source chart fields changed")
    positions = source["star_palaces"]
    if set(positions) != STAR_NAMES or any(
        not isinstance(position, str) or not position for position in positions.values()
    ):
        fail("not exactly fourteen canonical principal-star placements")
    if source["source_status"] not in ("original_transcription_only", "qualified_source_variant"):
        fail("historical source mechanic status unexpectedly promoted")
    return (
        source["gregorian_reference_date"],
        source["lunar_year"],
        source["lunar_month"],
        source["lunar_day"],
        source["is_leap_month"],
        source["hour_branch"],
        source["life_palace"],
        source["body_palace"],
        source["bureau_number"],
        tuple(sorted(positions.items())),
    )


def verify_parity_record(row: dict) -> None:
    if set(row) != {
        "id",
        "source_case",
        "iztro",
        "match",
        "differing_fields",
        "differing_14_stars",
        "comparison_classification",
    }:
        fail("original independent parity case record shape changed")
    s = row["source_case"]
    i = row["iztro"]
    chart_signature(s)
    if (
        set(i) != {"life_palace", "body_palace", "bureau_number", "star_palaces"}
        or set(i["star_palaces"]) != STAR_NAMES
    ):
        fail("vendor comparison output no longer complete")
    actual = (
        i["life_palace"] == s["life_palace"]
        and i["body_palace"] == s["body_palace"]
        and i["bureau_number"] == s["bureau_number"]
        and i["star_palaces"] == s["star_palaces"]
    )
    if row["match"] is not actual:
        fail("vendor comparison match flag contradicts literal fourteen-star outputs")
    if row["match"] and (row["differing_fields"] or row["differing_14_stars"]):
        fail("matched chart has an unexpected asserted source-vendor mismatch")
    if s["gender"] not in ("male", "female") or type(s["fix_leap"]) is not bool:
        fail("reference controls are not explicit synthetic sex/leap variants")


def evaluate(data: dict) -> dict:
    anchors = verify_candidates()
    if (
        data.get("synthetic_cases") != EXPECTED_ROWS
        or data.get("original_official_HKO_dates") != 10
        or data.get("preregistered_blinded_real_person_tests") != 0
        or data.get("runtime_astrological_forecast_promotions") != 0
        or data.get("independent_ancient_imprint_authenticated") is not False
        or data.get("birthplace_local_to_calendar_date_verified") is not False
        or len(data.get("all_312_case_records", [])) != EXPECTED_ROWS
        or len(data.get("all_disagreements", [])) != 120
    ):
        fail("source fixture totals or human/ancient-imprint source claims drift")
    if data.get("iztro_version") != "2.6.0":
        fail("independent vendor version changed without explicit source audit")
    if data.get("chosen_original_leap_rule") != (
        "transmitted Quan Shu leap month always counts as following month"
    ):
        fail("original source leap month policy silently rewritten")
    rows = data["all_312_case_records"]
    seen_ids = set()
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    raw = Counter()
    for row in rows:
        verify_parity_record(row)
        if row["id"] in seen_ids:
            fail("source oracle fixture ID duplicated")
        seen_ids.add(row["id"])
        source = row["source_case"]
        key = (source["gregorian_reference_date"], source["hour_branch"])
        grouped[key].append(row)
        raw["cases"] += 1
        raw["matched"] += bool(row["match"])
        raw["mismatched"] += not row["match"]
        raw["leap_comparisons"] += bool(source["is_leap_month"])
        raw["nonleap_comparisons"] += not source["is_leap_month"]
    dates = sorted({key[0] for key in grouped})
    hours = sorted({key[1] for key in grouped})
    if (len(dates), len(hours), len(grouped)) != (
        EXPECTED_DATES,
        EXPECTED_HOURS,
        EXPECTED_DATES * EXPECTED_HOURS,
    ):
        fail("ten selected reference dates and twelve hour branches not present")
    if raw != {
        "cases": 312,
        "matched": 192,
        "mismatched": 120,
        "nonleap_comparisons": 168,
        "leap_comparisons": 144,
    }:
        fail("original published 312 synthetic comparison counts changed")
    totals = Counter()
    by_star = Counter()
    by_date = {}
    strict_cases = []
    grouped_comparison = {"all_vendor_match": 0, "any_vendor_match": 0, "none_vendor_match": 0}
    for date in dates:
        by_date[date] = {
            "synthetic_hour_branch_states": 0,
            "strict_mock_eligibility_states": 0,
            "any_selected_star_states": 0,
            "nonleap_states": 0,
            "leap_states": 0,
        }
    for key in sorted(grouped):
        group = grouped[key]
        sigs = {chart_signature(row["source_case"]) for row in group}
        if len(sigs) != 1:
            fail("gender/leap duplicate comparison rows have different SOURCE chart content")
        example = group[0]["source_case"]
        n_expected = 4 if example["is_leap_month"] else 2
        if len(group) != n_expected:
            fail("oracle case group failed sex and leap option duplicate accounting")
        if {x["source_case"]["gender"] for x in group} != {"male", "female"}:
            fail("synthetic vendor study doesn't have both gender chart variants")
        if {x["source_case"]["fix_leap"] for x in group} != (
            {False, True} if example["is_leap_month"] else {True}
        ):
            fail("unexpected synthetic vendor leap policy controls")
        life = example["life_palace"]
        all_in_life = tuple(
            sorted(star for star, house in example["star_palaces"].items() if house == life)
        )
        selected = tuple(sorted(set(all_in_life) & set(anchors)))
        sole = len(all_in_life) == len(selected) == 1
        selected_with_conjunction = bool(selected) and len(all_in_life) > 1
        any_vendor_match = any(x["match"] for x in group)
        all_vendor_match = all(x["match"] for x in group)
        totals["unique_source_chart_states"] += 1
        totals["any_selected_star_states"] += bool(selected)
        totals["no_selected_star_states"] += not selected
        totals["exactly_one_selected_star_states"] += len(selected) == 1
        totals["two_selected_stars_states"] += len(selected) == 2
        totals["selected_stars_with_any_conjunction"] += selected_with_conjunction
        totals["sole_selected_without_any_other_principal_star"] += sole
        totals["life_palace_star_count_" + str(len(all_in_life))] += 1
        totals[
            "nonleap_unique_states" if not example["is_leap_month"] else "leap_unique_states"
        ] += 1
        if sole:
            by_star[selected[0]] += 1
            totals["sole_selected_any_vendor_match"] += any_vendor_match
            totals["sole_selected_all_vendor_match"] += all_vendor_match
            strict_cases.append(
                {
                    "synthetic_reference_date": key[0],
                    "hour_branch": key[1],
                    "sole_selected_principal_star": selected[0],
                    "source_original_leap_month": bool(example["is_leap_month"]),
                    "all_vendor_variant_outputs_match_source": all_vendor_match,
                    "any_vendor_variant_output_matches_source": any_vendor_match,
                }
            )
        grouped_comparison["any_vendor_match"] += any_vendor_match
        grouped_comparison["all_vendor_match"] += all_vendor_match
        grouped_comparison["none_vendor_match"] += not any_vendor_match
        d = by_date[key[0]]
        d["synthetic_hour_branch_states"] += 1
        d["strict_mock_eligibility_states"] += sole
        d["any_selected_star_states"] += bool(selected)
        d["nonleap_states" if not example["is_leap_month"] else "leap_states"] += 1
    if dict(grouped_comparison) != {
        "all_vendor_match": 84,
        "any_vendor_match": 96,
        "none_vendor_match": 24,
    }:
        fail("all/any vendor parity across unique SOURCE configurations changed")
    expected = {
        "unique_source_chart_states": 120,
        "any_selected_star_states": 34,
        "no_selected_star_states": 86,
        "exactly_one_selected_star_states": 31,
        "two_selected_stars_states": 3,
        "selected_stars_with_any_conjunction": 22,
        "sole_selected_without_any_other_principal_star": 12,
        "life_palace_star_count_0": 23,
        "life_palace_star_count_1": 59,
        "life_palace_star_count_2": 38,
        "nonleap_unique_states": 84,
        "leap_unique_states": 36,
        "sole_selected_any_vendor_match": 10,
        "sole_selected_all_vendor_match": 10,
    }
    if dict(totals) != expected or dict(by_star) != {"PoJun": 6, "TianLiang": 4, "LianZhen": 2}:
        fail(f"Original synthetic Life-palace star eligibility source changed: {totals} {by_star}")
    return {
        "schema": "HUMANDESIGN_ZIWEI_FOUR_ANCHOR_SYNTHETIC_CHART_ELIGIBILITY_AUDIT_V1",
        "status": "MECHANICAL_SOURCE_CHART_ELIGIBILITY_ONLY_NO_HUMAN_PREDICTIONS",
        "pin_independent_engine_commit": PARITY_COMMIT,
        "pin_independent_engine_source_path": PARITY_PATH,
        "pin_independent_engine_fixture_sha256": PARITY_SHA,
        "pin_unvalidated_four_question_source_map_sha256": SOURCE_MAPPING_SHA,
        "source_oracle_vendor": "Iztro 2.6.0 independently computed comparison",
        "source_leap_month_school_rule": data["chosen_original_leap_rule"],
        "no_birthplace_historical_iana_or_apparent_solar_time_verification": True,
        "source_star_profile_texts_not_independent_natal_chart_truth": True,
        "all_312_records_are_synthetic_comparison_not_real_subjects": True,
        "number_of_selected_reference_dates": len(dates),
        "number_of_synthetic_hour_branches_per_date": len(hours),
        "raw_comparison_counts_not_independent_source_chart_cases": dict(raw),
        "dedupe_key": (
            "synthetic_reference_date plus two-hour Earthly Branch; "
            "verify identical source chart despite gender/fixLeap comparator variants"
        ),
        "unique_source_chart_coverage_counts": dict(totals),
        "strict_sole_star_counts": {key: by_star.get(key, 0) for key in anchors},
        "grouped_independent_vendor_raw_parity": {
            **grouped_comparison,
            "interpretation": (
                "84 non-leap states match every duplicate comparison; 12 leap "
                "states have some matching comparator; never choose a vendor "
                "leap policy after seeing a person's answers."
            ),
        },
        "ten_selected_reference_dates_each_twelve_synthetic_branch_outcomes": by_date,
        "all_12_sole_selected_synthetic_cases": strict_cases,
        "strict_sole_model_abstentions": 108,
        "strict_sole_model_eligible_cases": 12,
        "strict_sole_model_eligibility_fraction_toy_dataset": 12 / 120,
        "model_candidate_decision": (
            "Current four-straight-single-star toy tokens require explicit "
            "abstention or a separately preselected multi-star combination "
            "rule; cannot be a representative valid single-star birth "
            "population model."
        ),
        "other_major_stars_and_all_source_modifiers_not_resolved": True,
        "source_original_leap_policy_not_overwritten": True,
        "source_gender_sex_chart_variant_not_human_gender_measurement": True,
        "selected_dates_not_statistical_representative_population": True,
        "empirical_human_chart_predictions_validated": 0,
        "real_person_birth_records_included": 0,
        "participant_questionnaire_data_included": 0,
        "astrological_production_rules_promoted": 0,
    }


def build(override_path: Path | None = None) -> dict:
    data = load_pinned_parity_data(override_path)
    result = evaluate(data)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = build()
    print(
        json.dumps(
            {
                "synthetic_states": result["unique_source_chart_coverage_counts"][
                    "unique_source_chart_states"
                ],
                "strict_single_star_eligible": result["strict_sole_model_eligible_cases"],
                "abstentions": result["strict_sole_model_abstentions"],
                "sole_star_counts": result["strict_sole_star_counts"],
                "raw_vendor_parity": result[
                    "raw_comparison_counts_not_independent_source_chart_cases"
                ],
                "human_validations": 0,
            },
            indent=2,
        )
    )
