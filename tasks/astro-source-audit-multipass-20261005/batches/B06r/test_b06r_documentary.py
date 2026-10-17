"""Original first-edition 1647 ninth-house introduction documentary consistency."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(n):
    return json.loads((B / n).read_text(encoding="utf-8"))


class NinthHouseIntroOriginal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.l = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])
        cls.text = " ".join(row["original_anchor_not_diplomatic"] for row in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_photographic_original_sha256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["640", "641", "642"])
        for v in self.w["images"].values():
            data = (B / v["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), v["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), v["sha256"])

    def test_02_original_folio_and_same_page_source_boundary(self):
        self.assertEqual(self.w["body_pdf_frames"], [640])
        self.assertTrue(self.w["unnumbered"])
        self.assertEqual(self.w["next_printed_CXXXIX_heading_pdf"], 640)
        self.assertEqual(
            [v["printed_folio"] for v in self.w["images"].values()],
            ["606", "607", "608"],
        )

    def test_03_source_no_numbered_chapter_increment(self):
        self.assertIsNone(self.a["printed_chapter"])
        self.assertEqual(self.acc["numbered_chapters_added"], 0)
        self.assertEqual(self.a["following_printed_chapter"], "CXXXIX")

    def test_04_exact_contiguous_25_historical_records(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(8681, 8706)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 25)

    def test_05_all_five_source_passages_reversibly_mapped(self):
        ids = []
        for source, inverse in zip(self.a["source_groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], inverse["source_span"])
            self.assertEqual(source["original_pdf_frames"], inverse["original_pdf_frames"])
            refs = [c["id"] for c in source["claims"]]
            self.assertEqual(refs, inverse["mapped_record_ids"])
            ids.extend(refs)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 5)

    def test_06_ninth_and_ruler_primary_vs_planets_in_ninth(self):
        self.one("ninth_house", "ninth_lord", "ninth_occupants")

    def test_07_moon_and_mercury_vs_attributed_ptolemy_mars(self):
        self.one("moon", "mercury", "ptolemy_mars")
        self.assertIn("Ptolomey addes Mars", self.text)
        self.assertFalse(self.l["original_ptolemy_mars_attribution_verified"])

    def test_08_one_many_foreign_travel_not_always_lifelong(self):
        self.one("yes_no", "count_once", "count_many", "frequently", "lifelong_abroad", "seldom")

    def test_09_destination_categorization_is_conditional_on_travel(self):
        self.one(
            "presuppose_travel",
            "which_world_region",
            "natal_reference",
            "many_regions",
            "dominant_region",
        )

    def test_10_travel_cause_and_success_are_different_questions(self):
        self.one("cause", "success")
        self.assertIn("causes principall", self.text)

    def test_11_travel_safety_and_life_hazard_not_real_predictions(self):
        self.one("danger", "life_danger")
        self.assertFalse(self.l["real_person_safety_or_faith_predictions_authorized"])

    def test_12_religion_only_heading_not_substantive_conclusion(self):
        self.one("heading", "journey_title")
        self.assertFalse(self.l["religious_personality_judgment_in_this_section"])

    def test_13_next_numbered_cxxxix_only_navigation_not_its_body(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R8704", "R8705"],
        )
        self.assertEqual(self.r["substantive"], 23)
        self.assertEqual(self.acc["next_original_pdf_frame"], 640)

    def test_14_zero_actual_human_destination_faith_risk_validity(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for r in self.r["rules"]:
            for key in (
                "independent_travel_occurrence_or_frequency_validated",
                "independent_travel_destination_or_cause_validated",
                "independent_travel_success_or_danger_validated",
                "real_person_faith_religion_or_safety_claim_authorized",
                "ptolemy_travel_attribution_independently_verified",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[key], r["id"])

    def test_15_accepted_corpus_count_and_sha(self):
        self.assertEqual(self.acc["previous_lilly"], 8680)
        self.assertEqual(self.acc["lilly_if_published"], 8705)
        self.assertEqual(self.acc["combined_if_published"], 9771)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
