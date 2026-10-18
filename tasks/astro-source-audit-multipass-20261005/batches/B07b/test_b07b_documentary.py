"""Lilly 1647 CXLVIII profession-source documentary tests, not career accuracy."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class ProfessionSignificatorSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.lim = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_source_photos_sha256_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(i) for i in range(658, 663)])
        for item in self.w["images"].values():
            data = (B / item["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), item["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])

    def test_02_original_printed_source_boundary(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [658, 659, 660])
        self.assertEqual(self.w["following_printed_CXLIX_heading_pdf"], 660)
        self.assertEqual(
            [v["printed_folio"] for v in self.w["images"].values()],
            ["624", "625", "626", "627", "628"],
        )

    def test_03_exact_82_unique_append_only_source_annotations(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(9445, 9527)),
        )
        self.assertEqual(len(set(r["id"] for r in self.r["rules"])), 82)

    def test_04_all_source_group_maps_bidirectional(self):
        ids = []
        for source, mapped in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], mapped["source_span"])
            self.assertEqual(source["original_pdf_frames"], mapped["original_pdf_frames"])
            row_ids = [r["id"] for r in source["clauses"]]
            self.assertEqual(row_ids, mapped["mapped_record_ids"])
            ids.extend(row_ids)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 6)

    def test_05_magistery_livelihood_study_main_time_reputation(self):
        self.one(
            "magistery_study",
            "magistery_art",
            "lifetime_action",
            "earn_living",
            "maintain_estimation",
            "principal_time",
        )

    def test_06_public_private_learned_mechanical_amusement_counts(self):
        self.one(
            "public_role",
            "public_justice",
            "military",
            "hunting",
            "philosophy",
            "theology",
            "mathematics",
            "private_role",
            "mechanical",
            "pleasure",
        )

    def test_07_own_industry_and_apprenticeship_distinct(self):
        self.one("learned_other", "own_industry")

    def test_08_three_question_targets_never_pooled(self):
        self.one(
            "question1",
            "question_no_profession",
            "question2",
            "question3_fortune",
            "question3_fame",
        )

    def test_09_three_vocation_planets_separate_source_qualities(self):
        self.one("significator_heading", "mercury", "mercury_mind", "mars_body", "venus_delight")

    def test_10_first_seventh_tenth_house_eligibility(self):
        self.one("eligible_tenth", "eligible_first", "eligible_seventh")

    def test_11_essential_dignity_not_combust_not_under_beams(self):
        self.one("planet_own_dignity", "not_combust", "not_under_sun", "eligible_profession")

    def test_12_mid_heaven_ruler_of_three_dignity_prerequisite(self):
        self.one("no_candidate_house", "candidate_lord_mc", "mc_essential_dignity")

    def test_13_mid_heaven_ruler_peregrine_or_fall_excluded(self):
        self.one("peregrine_exclusion", "fall_exclusion")

    def test_14_partile_moon_aspect_alternative_selection(self):
        self.one("no_mc_ruler", "moon_partile", "two_or_three")

    def test_15_moon_multiple_candidate_precedence(self):
        self.one("prefer_strongest", "prefer_best_aspect", "most_partile", "sinister_before_dexter")

    def test_16_moon_half_orb_following_paragraph_ambiguity_preserved(self):
        self.one("none_partile_moon", "moon_mediety_orb", "powerful_aspect")
        self.assertFalse(self.lim["original_profession_selection_algorithm_complete"])

    def test_17_malefic_conjunction_square_opposition_excludes(self):
        self.one("reject_malefic", "corp_conjunction", "malefic_square", "malefic_opposition")

    def test_18_solar_first_mover_last_fallback_distinct(self):
        self.one("sun_antecedence", "sun_antecedence_numerics", "profession_dominion")

    def test_19_lower_source_tiers_cannot_predict_profession_from_no_data(self):
        self.one(
            "third_fourth_fifth_only", "ignoble_profession", "manage_negligently", "no_profession"
        )

    def test_20_author_retrospective_tenth_sign_study_not_validation(self):
        self.one("author_practice", "tenth_sign", "tenth_ruler_sign_house")

    def test_21_original_ptolemy_alternative_not_same_as_Lilly(self):
        self.one("ptolemy_attribution", "ptolemy_two_ways", "ptolemy_sun", "ptolemy_mc")
        self.assertFalse(self.lim["ptolemy_profession_rules_crosscollated"])

    def test_22_ptolemy_morning_rising_vs_tenth_house(self):
        self.one("morning_riser", "lord_mc", "planet_mc", "moon_aspect_mc")

    def test_23_ptolemy_two_path_coincidence_or_one_path_fallback(self):
        self.one(
            "same_planet_both",
            "same_planet_in_tenth",
            "master_arts",
            "one_path_suffices",
            "not_independent",
        )

    def test_24_following_cxlix_profession_aphorisms_not_imported(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R9525", "R9526"],
        )
        self.assertEqual(self.r["substantive"], 80)
        self.assertEqual(self.accept["next_printed_chapter"], "CXLIX")

    def test_25_no_real_human_jobs_fame_or_moral_claims_validated(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.lim["actual_person_professional_moral_labels_authorized"])
        for row in self.r["rules"]:
            for k in (
                "independent_real_profession_occurrence_validated",
                "independent_real_occupation_category_validated",
                "independent_real_professional_fame_or_income_validated",
                "source_ptolemy_original_cross_collated",
                "person_level_employment_or_moral_forecast_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[k], (row["id"], k))

    def test_26_source_sha_and_cumulative_historical_count(self):
        self.assertEqual(self.accept["prior_lilly"], 9444)
        self.assertEqual(self.accept["lilly_if_published"], 9526)
        self.assertEqual(self.accept["combined_if_published"], 10592)
        self.assertEqual(self.accept["new_numbered_chapters"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
