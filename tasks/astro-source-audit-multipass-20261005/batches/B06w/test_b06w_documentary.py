"""Original first-edition Lilly CXLIII dream source integrity, not predictive validity."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalDreamSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.rules = read("RULES.json")
        cls.witness = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.rules["rules"])
        cls.anchors = " ".join(x["source_anchor_not_diplomatic"] for x in cls.rules["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_source_photos_sha256_bytes(self):
        self.assertEqual(list(self.witness["images"]), [str(n) for n in range(647, 652)])
        for photo in self.witness["images"].values():
            data = (B / photo["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), photo["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), photo["sha256"])

    def test_02_folio_and_two_distinct_following_headings(self):
        self.assertEqual(self.witness["body_original_pdf_frames"], [647, 648])
        self.assertEqual(self.witness["following_unnumbered_tenth_house_pdf"], 649)
        self.assertEqual(self.witness["following_printed_CXLIIII_heading_pdf"], 649)
        self.assertEqual(
            [x["printed_folio"] for x in self.witness["images"].values()],
            ["613", "614", "615", "616", "617"],
        )

    def test_03_unique_append_only_sixty_six_records(self):
        self.assertEqual([x["record_number"] for x in self.rules["rules"]], list(range(9040, 9106)))
        self.assertEqual(len({x["id"] for x in self.rules["rules"]}), 66)

    def test_04_seven_reversible_source_passage_groups(self):
        ids = []
        for a, b in zip(self.author["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(a["source_span"], b["source_span"])
            self.assertEqual(a["original_pdf_frames"], b["original_pdf_frames"])
            groupids = [x["id"] for x in a["claims"]]
            self.assertEqual(groupids, b["mapped_record_ids"])
            ids.extend(groupids)
        self.assertEqual(ids, [x["id"] for x in self.rules["rules"]])
        self.assertEqual(self.map["source_group_count"], 7)

    def test_05_jupiter_or_venus_ninth_potent_and_unafflicted(self):
        self.one("jupiter_ninth", "venus_ninth", "potent", "not_afflicted", "true_dream_claim")

    def test_06_malefic_ninth_distinct_scurvy_and_false_dreams(self):
        self.one("ninth_malefics", "scurvy_dreams", "wholly_deceitful")

    def test_07_benefic_debilitated_ambiguous_true_false(self):
        self.one(
            "benefic_weak", "benefic_afflicted", "ambiguous", "some_true", "some_false", "no_credit"
        )

    def test_08_ninth_unoccupied_fallback_to_sign_and_lord(self):
        self.one("empty_ninth", "ninth_sign", "lord_ninth", "lord_condition")

    def test_09_quality_heading_content_not_prophecy(self):
        self.one("subheading_quality", "planet_as_significator", "truth_vs_content")
        self.assertIn("Of the quality of Dreames", self.anchors)

    def test_10_saturn_agriculture_digging_caves_treasure(self):
        self.one("saturn_husbandry", "saturn_rude", "saturn_dig", "saturn_treasure", "saturn_caves")

    def test_11_saturn_burial_spirits_fear_are_themes_only(self):
        self.one("saturn_dark", "saturn_burial", "saturn_devil", "saturn_fear")

    def test_12_jupiter_gentry_preferment_church_and_elites(self):
        self.one(
            "jupiter_pleasant",
            "jupiter_gentry",
            "jupiter_preferment",
            "jupiter_church",
            "jupiter_elites",
        )

    def test_13_mars_fights_enmity_horses_war_fire_dogs(self):
        self.one(
            "mars_contention",
            "mars_enmities",
            "mars_horses",
            "mars_wars",
            "mars_fire",
            "mars_dogs_hunting",
        )

    def test_14_solar_money_magistracy_dignity_different_from_future(self):
        self.one("sun_gold", "sun_high_estate", "sun_magistracy", "sun_preferment")

    def test_15_venus_merriment_clothing_picture_scent_and_gender_context(self):
        self.one(
            "venus_delightful",
            "venus_pleasure",
            "venus_clothes",
            "venus_people",
            "venus_pictures",
            "venus_smells",
        )

    def test_16_mercury_journey_books_accounts_money_youth(self):
        self.one(
            "mercury_journey",
            "mercury_learning",
            "mercury_accounts",
            "mercury_money",
            "mercury_youth",
        )

    def test_17_lunar_water_navigation_sea_flying(self):
        self.one(
            "moon_waters", "moon_navigation", "moon_business", "moon_dangers_sea", "moon_flying"
        )

    def test_18_saturn_with_moon_horrible_exception(self):
        self.one("saturn_with_moon", "horrible_dreams")
        self.assertIn("if Saturn be with her", self.anchors)

    def test_19_next_unumbered_tenth_house_does_not_increment_twice(self):
        self.assertEqual(
            [x["id"] for x in self.rules["rules"] if x["role"] == "next_section_navigation"],
            ["R9104", "R9105"],
        )
        self.assertEqual(self.rules["substantive"], 64)
        self.assertEqual(self.accept["next_source"], "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES")
        self.assertEqual(self.accept["following_printed_chapter"], "CXLIIII")
        self.assertEqual(self.accept["numbered_chapters_added"], 1)

    def test_20_no_live_dream_predictive_or_clinical_success(self):
        self.assertEqual(self.rules["empirical_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertFalse(self.limits["actual_sleep_or_spiritual_diagnosis_authorized"])
        for x in self.rules["rules"]:
            for flag in (
                "independent_dream_content_prediction_validated",
                "independent_dream_prophecy_accuracy_validated",
                "independent_sleep_psychological_diagnosis_validated",
                "human_spiritual_or_nightmare_classification_authorized",
                "dream_to_real_event_causation_verified",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[flag], x["id"])

    def test_21_lilly_source_and_hash_count(self):
        self.assertEqual(self.accept["prior_lilly"], 9039)
        self.assertEqual(self.accept["lilly_if_published"], 9105)
        self.assertEqual(self.accept["combined_if_published"], 10171)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(), self.accept["rules_sha256"]
        )


if __name__ == "__main__":
    unittest.main()
