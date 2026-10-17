"""Original Lilly mines and metals historical documentary source checks.

Passing source checks do not prove mineral wealth predictions or geological claims.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


class OriginalMinesSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.types = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_sha256_all_original_page_witnesses(self):
        for x in self.w["images"].values():
            f = B / x["file"]
            data = f.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), x["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), x["sha256"])

    def test_02_mines_chapter_and_unnumbered_sixth_source_separate(self):
        self.assertEqual(list(self.w["images"]), ["609", "610", "611", "612"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["575", "576", "577", "578"],
        )
        self.assertEqual(self.w["source_body_pdf_frame"], 609)
        self.assertEqual(self.w["following_unnumbered_sixth_house_start_frame"], 610)

    def test_03_all_ids_consecutive_and_two_navigation(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(7549, 7584)),
        )
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_section_navigation"],
            ["R7582", "R7583"],
        )

    def test_04_all_nine_source_groups_reverse_covered(self):
        ids = []
        for authored, inverse in zip(self.a["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], inverse["source_span"])
            self.assertEqual(authored["original_pdf_frames"], inverse["original_pdf_frames"])
            expected = [x["id"] for x in authored["claims"]]
            self.assertEqual(expected, inverse["mapped_ids"])
            ids.extend(expected)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.map["source_groups"]), 9)

    def test_05_saturn_lord_or_occupant_alternatives(self):
        self.assertEqual(self.types["saturn_lord"], 1)
        self.assertEqual(self.types["saturn_occupant"], 1)
        self.assertIn("Lord of the fourth", self.text)

    def test_06_saturn_positive_needs_dignity_motion_and_benefics(self):
        for role in ("saturn_dignity", "saturn_direct", "saturn_swift", "saturn_benefic"):
            self.assertEqual(self.types[role], 1)

    def test_07_source_mining_substance_list_and_power_grading(self):
        self.assertEqual(self.types["mine_gain"], 1)
        self.assertEqual(self.types["mine_materials"], 1)
        self.assertEqual(self.types["mine_grading"], 1)
        self.assertEqual(self.types["saturn_magnitude"], 1)

    def test_08_fourth_ruler_reception_compound(self):
        for role in (
            "reception_first",
            "reception_second",
            "reception_mutual",
            "reception_outcome",
            "reception_minerals",
        ):
            self.assertEqual(self.types[role], 1)

    def test_09_specific_jupiter_fourth_libra_tin_and_inheritance(self):
        for role in ("jupiter_occupant", "jupiter_sign", "jupiter_tin", "jupiter_family"):
            self.assertEqual(self.types[role], 1)
        self.assertIn("Tyn especially", self.text)

    def test_10_saturn_fourth_aquarius_plus_jupiter_libra(self):
        self.assertEqual(self.types["saturn_priority"], 1)
        self.assertEqual(self.types["saturn_aquarius"], 1)
        self.assertEqual(self.types["jupiter_libra"], 1)

    def test_11_mars_fourth_leo_sun_aries_for_metal_types(self):
        for role in ("mars_fourth", "mars_leo", "sun_aries", "metal_types"):
            self.assertEqual(self.types[role], 1)
        self.assertIn("Gold Mines", self.text)

    def test_12_coal_lead_saturn_earth_sign_and_sun_mars_mercury(self):
        for role in (
            "coal_saturn",
            "coal_aspect",
            "coal_house",
            "coal_other_house",
            "coal_outcome",
        ):
            self.assertEqual(self.types[role], 1)

    def test_13_unumbered_sixth_medical_handoff_not_ingested(self):
        self.assertEqual(self.r["next_unnumbered_source_navigation"], 2)
        self.assertEqual(self.acc["next_section"], "UNNUMBERED_SIXTH_HOUSE_INFIRMITIES")
        self.assertEqual(self.acc["next_pdf_frame"], 610)

    def test_14_historical_only_no_mining_investment_forecasts(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["human_mining_outcomes_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.r["diplomatic_transcription_complete"])
        self.assertFalse(self.limits["investment_advice_authorized"])
        for x in self.r["rules"]:
            self.assertFalse(x["independent_mining_finance_prediction_validated"])
            self.assertFalse(x["actual_ore_or_mineral_deposit_validated"])
            self.assertFalse(x["runtime_rule_promoted"])

    def test_15_rules_hash_and_corpus_arithmetic(self):
        self.assertEqual(self.acc["previous_lilly"], 7548)
        self.assertEqual(self.acc["lilly_if_published"], 7583)
        self.assertEqual(self.acc["combined_if_published"], 8649)
        h = hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest()
        self.assertEqual(h, self.acc["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
