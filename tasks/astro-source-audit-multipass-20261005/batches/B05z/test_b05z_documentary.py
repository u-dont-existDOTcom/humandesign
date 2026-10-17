"""Original Lilly estate inheritance historical source only; no financial validity tests."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class InheritedEstateSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.u = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(r["role"] for r in cls.r["rules"])
        cls.anchors = " ".join(r["anchor_not_diplomatic"] for r in cls.r["rules"])

    def test_01_original_first_edition_images_hash_bytes(self):
        for x in self.w["images"].values():
            f = B / x["file"]
            data = f.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), x["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), x["sha256"])

    def test_02_source_order_and_following_heading(self):
        self.assertEqual(list(self.w["images"]), ["606", "607", "608", "609"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["572", "573", "574", "575"],
        )
        self.assertEqual(self.w["body_original_frames"], [606, 607])
        self.assertEqual(self.w["next_printed_CXXV_heading_frame"], 607)

    def test_03_record_numbers_consecutive(self):
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(7441, 7474)))
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 33)

    def test_04_bidirectional_source_mapping(self):
        ids = []
        for g, reverse in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(g["source_span"], reverse["source_span"])
            self.assertEqual(g["pdf_frames"], reverse["original_pdf_frames"])
            sub = [c["id"] for c in g["claims"]]
            self.assertEqual(reverse["mapped_record_ids"], sub)
            ids.extend(sub)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 8)

    def test_05_day_and_night_inheritance_benefics(self):
        self.assertEqual(self.roles["day_condition"], 1)
        self.assertEqual(self.roles["night_condition"], 2)
        self.assertEqual(self.roles["benefic_aspect"], 1)
        self.assertIn("day", self.anchors.lower())
        self.assertIn("nocturnal", self.anchors.lower())

    def test_06_positive_inheritance_has_place_and_dominion_alternatives(self):
        self.assertEqual(self.roles["benefic_places"], 1)
        self.assertEqual(self.roles["benefic_dominion"], 1)
        self.assertEqual(self.roles["positive_result"], 3)

    def test_07_mars_bad_sect_and_no_benefic_rescue(self):
        for kind in (
            "bad_mars",
            "sect_negative_day",
            "sect_negative_night",
            "no_relief",
            "bad_result",
        ):
            self.assertEqual(self.roles[kind], 1)

    def test_08_night_moon_weak_and_both_second_and_fourth(self):
        self.assertEqual(self.roles["night_condition"], 2)
        self.assertEqual(self.roles["moon_afflicted"], 1)
        self.assertEqual(self.roles["second_ruler"], 1)
        self.assertEqual(self.roles["fourth_ruler"], 1)
        self.assertEqual(self.roles["second_house"], 1)

    def test_09_saturn_twelfth_both_peregrine(self):
        self.assertEqual(self.roles["saturn_twelfth"], 1)
        self.assertEqual(self.roles["peregrine_pair"], 1)
        self.assertEqual(self.roles["ruin_result"], 3)

    def test_10_fourth_malefics_and_first_ruler_unfortunate(self):
        self.assertEqual(self.roles["malefics_fourth"], 1)
        self.assertEqual(self.roles["asc_ruler_weak"], 1)

    def test_11_sun_mars_peregrine_second_house(self):
        self.assertEqual(self.roles["sun_mars"], 1)
        self.assertEqual(self.roles["peregrine_condition"], 1)
        self.assertEqual(self.roles["second_harm"], 1)

    def test_12_next_parents_concord_navigation_only(self):
        nav = [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"]
        self.assertEqual(nav, ["R7472", "R7473"])
        self.assertEqual(self.r["substantive_historical"], 31)

    def test_13_not_wealth_management_or_legal_advice(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["economic_predictions_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.r["diplomatic_transcription_complete"])
        for x in self.r["rules"]:
            self.assertFalse(x["independent_human_inheritance_validated"])
            self.assertFalse(x["family_finances_or_management_predicted"])
            self.assertFalse(x["legal_or_financial_advice_authorized"])
            self.assertFalse(x["runtime_model_promoted"])

    def test_14_documentary_rules_sha_and_total(self):
        self.assertEqual(self.acc["previous_lilly"], 7440)
        self.assertEqual(self.acc["lilly_if_published"], 7473)
        self.assertEqual(self.acc["combined_if_published"], 8539)
        self.assertGreaterEqual(len(self.u["issues"]), 12)
        digest = hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest()
        self.assertEqual(digest, self.acc["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
