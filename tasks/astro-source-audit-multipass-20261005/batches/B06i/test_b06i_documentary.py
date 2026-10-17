"""Lilly 1647 CXXXI documentary consistency, NOT a marriage timing validation."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class MarriageEaseAndDirectionsSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.method = read("MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_source_photos_sha256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["623", "624", "625", "626", "627"])
        for src in self.w["images"].values():
            path = B / src["file"]
            raw = path.read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), src["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), src["sha256"])

    def test_02_physical_chapter_boundaries(self):
        self.assertEqual(self.w["body_original_frames"], [623, 624])
        self.assertEqual(self.w["next_printed_CXXXII_heading_frame"], 624)
        self.assertTrue(self.w["marriage_time_heading_within_CXXXI"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["589", "590", "591", "592", "593"],
        )

    def test_03_append_only_83_records(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(7944, 8027)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 83)

    def test_04_reversible_source_mapping_eleven_groups(self):
        refs = []
        for source, inverse in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], inverse["source_span"])
            self.assertEqual(source["original_pdf_frames"], inverse["original_pdf_frames"])
            groupids = [c["id"] for c in source["claims"]]
            self.assertEqual(inverse["mapped_record_ids"], groupids)
            refs.extend(groupids)
        self.assertEqual(refs, [r["id"] for r in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 11)

    def test_05_majority_fortunate_versus_all_weak(self):
        for role in (
            "indicator_majority",
            "indicator_fortified",
            "easy_outcome",
            "weak_indicators",
            "infortunes_signify",
            "difficulty_outcome",
            "all_weak",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_06_failed_wooing_not_equal_to_no_marriage(self):
        self.assertEqual(self.roles["many_failed_wooing"], 1)
        self.assertEqual(self.roles["sudden_wedding"], 1)
        self.assertEqual(self.roles["procurement_hard"], 1)

    def test_07_venus_mars_alleged_love_inconveniences(self):
        self.assertEqual(self.roles["venus_mars_negative"], 1)
        self.assertEqual(self.roles["inconvenience_outcome"], 1)

    def test_08_weak_strong_malefic_exception(self):
        self.assertEqual(self.roles["benefic_source"], 1)
        self.assertEqual(self.roles["malefic_source"], 1)
        self.assertEqual(self.roles["malefic_power_exception"], 1)

    def test_09_author_anecdote_four_independent_alternatives(self):
        for role in (
            "author_anecdote",
            "saturn_mars_opposition",
            "saturn_seventh_cusp",
            "venus_leo_scorpio",
            "venus_mars_absent",
            "mars_seventh_signs",
            "mars_venus_optional",
            "author_difficulty",
        ):
            self.assertEqual(self.roles[role], 1)
        anecdote = next(x for x in self.r["rules"] if x["role"] == "author_anecdote")
        self.assertEqual(anecdote["source_qualification"], "unverified-author-claim")

    def test_10_no_person_moral_sexual_label(self):
        self.assertEqual(self.roles["moral_women"], 1)
        self.assertFalse(self.limits["intimate_behavior_predictions_authorized"])

    def test_11_time_heading_same_cxxxi(self):
        self.assertEqual(self.roles["time_heading"], 1)
        self.assertIn("The time of Marriage", self.text)

    def test_12_oriental_moon_and_six_house_list(self):
        for role in (
            "majority_time",
            "moon_oriental",
            "east_quarters",
            "east_house_list",
            "marry_youth",
            "late_young_spouse",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("tenth eleventh twelfth fourth fifth sixth", self.text)

    def test_13_occidental_age_versus_spouse_widow_or_aged(self):
        for role in (
            "occidental_sun",
            "occidental_quarters",
            "west_house_list",
            "late_marriage",
            "youth_widow",
            "youth_aged_spouse",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("ninth eighth seventh first second third", self.text)

    def test_14_motion_direct_swift_vs_retro_slow_stationary(self):
        for role in (
            "direct_motion",
            "swift_motion",
            "direct_result",
            "retrograde_motion",
            "slow_motion",
            "stationary_motion",
            "delay_result",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_15_discrepant_testimonies_select_moon_precedence(self):
        self.assertEqual(self.roles["discordant_sources"], 1)
        self.assertEqual(self.roles["moon_priority"], 1)
        self.assertIn("especially Moon", self.text)

    def test_16_seventh_and_moon_venus_directions_to_ascendant(self):
        for role in (
            "specific_directions",
            "direction_seventh_degree",
            "direction_seventh_lord",
            "direction_moon",
            "direction_venus",
            "direction_target_asc_degree",
            "direction_target_asc_lord",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_17_mid_heaven_to_venus_four_aspects_and_moon_option(self):
        for role in (
            "author_dissent",
            "midheaven_directed",
            "venus_body",
            "venus_sextile",
            "venus_square",
            "venus_trine",
            "venus_radix_strong",
            "moon_same_aspects",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_18_sun_both_directions_four_aspects(self):
        for role in (
            "sun_direct",
            "sun_converse",
            "sun_to_body",
            "sun_to_sextile",
            "sun_to_square",
            "sun_to_trine",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_19_moon_sun_mars_hard_aspect_terms_fortune(self):
        for role in (
            "moon_to_sun",
            "moon_to_mars",
            "malefic_square_opposition",
            "terms_of_fortune",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("Terms of a Fortune", self.text)

    def test_20_sun_moon_mc_to_seventh_house_lord_benefic(self):
        for role in (
            "mc_direction_positive",
            "sun_direction_positive",
            "moon_direction_positive",
            "seventh_lord_target",
            "benefic_occupant_target",
            "marriage_timing_result",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_21_structured_directions_method_fourteen_steps(self):
        self.assertEqual(len(self.method["steps"]), 14)
        self.assertEqual(
            [s["order"] for s in self.method["steps"]],
            list(range(1, 15)),
        )
        self.assertEqual(
            self.method["procedure_status"],
            "HISTORICAL_SOURCE_STRUCTURED_NOT_EXECUTABLE_OR_VALIDATED",
        )

    def test_22_missing_arcs_epoch_age_boundaries_and_comparator(self):
        missing = " ".join(self.method["missing_for_executable_rule"]).lower()
        for key in ("arc-to-years", "youth", "calendar", "direction", "priority"):
            self.assertIn(key, missing)
        self.assertFalse(self.method["empirical_status"]["dates_predicted"])
        self.assertFalse(self.method["empirical_status"]["age_years_computed"])

    def test_23_no_human_timing_validation_or_runtime(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_human_marriage_timing_validations"], 0)
        self.assertFalse(self.r["direction_algorithm_complete"])
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertEqual(self.method["empirical_status"]["runtime_promotions"], 0)
        for r in self.r["rules"]:
            self.assertFalse(r["independent_human_marriage_difficulty_validated"])
            self.assertFalse(r["independent_marriage_calendar_date_validated"])
            self.assertFalse(r["actual_partner_age_or_personal_behavior_validated"])
            self.assertFalse(r["source_direction_computation_executable"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_24_cxxxii_multiple_wives_is_separate_chapter(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R8025", "R8026"],
        )
        self.assertEqual(self.accept["next_printed_chapter"], "CXXXII")
        self.assertEqual(self.accept["next_original_pdf"], 624)
        self.assertEqual(self.r["substantive"], 81)

    def test_25_rules_and_procedure_hash_and_corpus_total(self):
        self.assertEqual(self.accept["prior_lilly"], 7943)
        self.assertEqual(self.accept["lilly_if_published"], 8026)
        self.assertEqual(self.accept["combined_if_published"], 9092)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(
                (B / "MARRIAGE_PRIMARY_DIRECTIONS_HISTORICAL_METHOD_V1.json").read_bytes()
            ).hexdigest(),
            self.accept["marriage_method_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
