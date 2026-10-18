"""Lilly 1647 printed CXLVI original source integrity, not occupational prediction."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class HistoricalPrefermentCauses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])

    def once(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_jpegs_sha_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["655", "656", "657", "658"])
        for v in self.w["images"].values():
            data = (B / v["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), v["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), v["sha256"])

    def test_02_first_ed_folios_and_seams(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [655, 656])
        self.assertEqual(self.w["following_printed_CXLVII_heading_pdf"], 656)
        self.assertEqual(
            [v["printed_folio"] for v in self.w["images"].values()],
            ["621", "622", "623", "624"],
        )

    def test_03_number_gap_preserved(self):
        self.assertTrue(self.a["previous_printed_CXLV_missing_unchanged"])
        self.assertFalse(self.r["previous_printed_CXLV_present"])
        self.assertEqual(self.r["printed_chapter"], "CXLVI")
        self.assertEqual(self.r["following_printed"], "CXLVII")

    def test_04_fifty_five_unique_contiguous_records(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(9313, 9368)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 55)

    def test_05_four_passages_source_to_record_reversibility(self):
        ids = []
        for source, mapped in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], mapped["source_span"])
            self.assertEqual(source["original_pdf_frames"], mapped["original_pdf_frames"])
            these = [x["id"] for x in source["claims"]]
            self.assertEqual(mapped["mapped_record_ids"], these)
            ids.extend(these)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 4)

    def test_06_preferment_causes_vs_status_separate(self):
        self.once("heading", "preferment_quality")
        self.assertEqual(self.r["substantive"], 53)

    def test_07_planets_partile_and_priority_stronger_luminary(self):
        self.once(
            "partile_aspect_planets", "stronger_luminary", "nature_planets", "plurality_testimonies"
        )

    def test_08_saturn_requires_strength_and_contact(self):
        self.once("saturn_strong", "saturn_inherit", "saturn_possessions", "saturn_favour")

    def test_09_saturn_people_relative_social_class(self):
        self.once("saturn_elders", "saturn_frugal")

    def test_10_jupiter_venus_virtue_honesty_justice_distinct(self):
        self.once("jupiter_venus", "virtue", "honesty", "gravity", "justice", "benefic_people")

    def test_11_mars_has_military_not_universal_government_cause(self):
        self.once("mars", "mars_armies", "mars_victories", "mars_valour", "mars_recommendations")

    def test_12_mercury_learning_commerce_professions(self):
        self.once(
            "mercury", "wit", "judgment", "oratory", "learning", "merchants", "scholars", "lawyers"
        )

    def test_13_house_overlay_first_industry_second_riches(self):
        self.once(
            "consider_house",
            "first_house",
            "own_industry",
            "second_house",
            "riches",
            "other_houses",
            "combine_house_planet",
        )

    def test_14_if_no_luminary_contact_tenth_occupants_fallback(self):
        self.once("no_aspect", "planets_tenth", "choose_strongest_tenth", "tenanted_tenth_cause")

    def test_15_if_tenth_empty_tenth_lord_and_its_house_fallback(self):
        self.once("empty_tenth", "lord_tenth", "lord_tenth_house")

    def test_16_other_astrologers_use_separate_dispositor_approach(self):
        self.once(
            "other_authors", "dispositor_luminary", "light_above_earth", "light_partile_tenth"
        )

    def test_17_rival_method_has_no_independent_replicated_results(self):
        self.once("rival_not_verified")
        self.assertFalse(self.limits["source_planet_essential_dignity_weights_complete"])

    def test_18_following_continuation_honours_is_new_chapter(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R9366", "R9367"],
        )
        self.assertEqual(self.acc["following_printed_chapter"], "CXLVII")
        self.assertEqual(self.acc["following_heading_pdf"], 656)

    def test_19_zero_real_person_class_or_causal_accuracy(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(
            self.limits["real_person_recommendation_or_moral_classification_authorized"]
        )
        for x in self.r["rules"]:
            for k in (
                "independent_human_profession_or_promotion_cause_validated",
                "independent_human_property_or_military_advancement_validated",
                "independent_human_wit_morality_or_industry_validated",
                "real_person_employment_or_social_class_inference_authorized",
                "source_causal_attribution_experimentally_verified",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[k], (x["id"], k))

    def test_20_corpus_sha_and_numbering(self):
        self.assertEqual(self.acc["prior_lilly"], 9312)
        self.assertEqual(self.acc["lilly_if_published"], 9367)
        self.assertEqual(self.acc["combined_if_published"], 10433)
        self.assertEqual(self.acc["new_numbered_chapters"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
