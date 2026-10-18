"""Original Lilly CXL Causes of Travels and Haly: historic source integrity."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class HistoricTravelCauseAndHaly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["source_anchor_not_diplomatic"] for x in cls.r["rules"])

    def one(self, *names):
        for name in names:
            self.assertEqual(self.roles[name], 1, name)

    def test_01_original_images_byte_and_sha256(self):
        self.assertEqual(list(self.w["images"]), ["643", "644", "645", "646"])
        for src in self.w["images"].values():
            raw = (B / src["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), src["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), src["sha256"])

    def test_02_first_edition_printed_page_mapping(self):
        self.assertEqual(self.w["body_pdf_frames"], [643, 644])
        self.assertEqual(self.w["following_printed_CXLI_heading_pdf"], 644)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()], ["609", "610", "611", "612"]
        )

    def test_03_original_source_one_numbered_chapter(self):
        self.assertEqual(self.a["printed_chapter"], "CXL")
        self.assertEqual(self.a["next_printed"], "CXLI")
        self.assertEqual(self.accept["numbered_chapters_added"], 1)

    def test_04_exact_record_sequence_53_source_items(self):
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(8807, 8860)))
        self.assertEqual(len(set(x["id"] for x in self.r["rules"])), 53)

    def test_05_six_reversible_group_mapping(self):
        ids = []
        for src, dest in zip(self.a["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(src["source_span"], dest["source_span"])
            self.assertEqual(src["original_pdf_frames"], dest["original_pdf_frames"])
            groupids = [x["id"] for x in src["claims"]]
            self.assertEqual(groupids, dest["mapped_record_ids"])
            ids.extend(groupids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.map["source_group_count"], 6)

    def test_06_sun_or_planets_alternatives_not_all_needed(self):
        self.one("heading", "planet_significators", "house_positions", "nature_planet")

    def test_07_saturn_all_three_different_triggers(self):
        self.one("saturn_conjunction", "saturn_dignity", "saturn_self")

    def test_08_saturn_mines_estate_commodities_distinct(self):
        self.one("saturn_mines", "saturn_inheritance", "saturn_commodities")

    def test_09_saturn_people_and_relative_social_class(self):
        self.one("saturn_people", "source_personal_context")

    def test_10_jupiter_law_religion_honour_ecclesiastical(self):
        self.one(
            "jupiter_significator",
            "jupiter_religion",
            "jupiter_honour",
            "jupiter_law",
            "jupiter_ecclesiastical",
            "jupiter_people",
        )

    def test_11_cross_reference_other_planets_not_assimilated(self):
        self.one("other_planets", "look_houses")
        self.assertIn("specified second House", self.anchors)

    def test_12_first_curiosity_second_trade_and_wealth(self):
        self.one(
            "first_house", "curiosity", "second_house", "commerce", "enrichment", "house_logic"
        )

    def test_13_haly_attribution_not_original_cross_collation(self):
        self.one("haly_heading", "ninth_lord")
        self.assertFalse(self.limits["haly_original_text_crosscollated"])
        for r in self.r["rules"]:
            self.assertFalse(r["historical_haly_original_independently_verified"])

    def test_14_haly_first_travel_often_and_second_profit(self):
        self.one("haly_first", "haly_first_many", "haly_second", "haly_second_profit")

    def test_15_haly_third_intimacy_and_moving_not_equivalent(self):
        self.one("haly_third", "haly_third_partner", "haly_third_shift")

    def test_16_haly_fourth_parent_illness_and_travel_death_separate(self):
        self.one("haly_fourth", "haly_parent_infirmity", "haly_native_death", "parent_vs_native")

    def test_17_haly_fifth_children_other_country_only(self):
        self.one("haly_fifth", "haly_children_foreign")

    def test_18_haly_sixth_slave_servant_economics_and_cattle_illness(self):
        self.one("haly_sixth", "haly_servants_gain", "haly_cattle_sick")

    def test_19_haly_seventh_wife_and_ill_supported_obedience(self):
        self.one("haly_seventh", "haly_wife_good", "haly_wife_obedient")

    def test_20_haly_eighth_estate_motive_and_crossing_seas(self):
        self.one("haly_eighth", "haly_desire_estate", "haly_ocean")

    def test_21_original_haly_sequence_stops_at_eighth(self):
        self.one("end_haly_at_eighth")
        self.assertIn("excerpt stops at eighth", " ".join(self.limits["issues"]).lower())

    def test_22_following_cxli_is_separate_success_and_danger(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R8858", "R8859"],
        )
        self.assertEqual(self.r["substantive"], 51)
        self.assertEqual(self.accept["next_printed_chapter"], "CXLI")
        self.assertEqual(self.accept["next_original_pdf"], 644)

    def test_23_no_medical_parent_sex_faith_profit_forecasts(self):
        self.assertFalse(
            self.limits["real_person_motive_faith_health_or_intimate_inference_authorized"]
        )
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_person_travel_causes_validated",
                "independent_trade_or_law_motive_validated",
                "independent_people_or_estate_event_validated",
                "independent_animal_or_parent_illness_validated",
                "independent_travel_death_validated",
                "private_religious_moral_health_inference_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))

    def test_24_rules_digest_and_expected_lilly_total(self):
        self.assertEqual(self.accept["prior_lilly"], 8806)
        self.assertEqual(self.accept["lilly_if_published"], 8859)
        self.assertEqual(self.accept["combined_if_published"], 9925)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
