"""First-edition Lilly sibling-number source mapping, not birth prediction tests."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class OriginalSiblingNumber(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = load("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = load("RULES.json")
        cls.map = load("SOURCE_TO_RECORD_MAP.json")
        cls.w = load("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = load("UNRESOLVED_SOURCE_LIMITS.json")
        cls.a = load("ACCEPTANCE.json")
        cls.types = Counter(x["role"] for x in cls.r["rules"])

    def text(self):
        return " ".join(r["original_anchor_not_diplomatic"] for r in self.r["rules"])

    def test_01_image_hash_and_bytes(self):
        for info in self.w["images"].values():
            p = B / info["file"]
            self.assertEqual(p.stat().st_size, info["bytes"])
            self.assertEqual(sha(p), info["sha256"])
            self.assertEqual(p.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_02_original_page_sequence(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(598, 603)])
        self.assertEqual(
            [v["printed_page"] for v in self.w["images"].values()],
            ["564", "565", "566", "567", "568"],
        )
        self.assertEqual(self.w["body_pdf_frames"], [598, 599, 600])

    def test_03_chapter_boundaries(self):
        self.assertEqual(self.w["next_chapter_CXIX_heading_pdf"], 600)
        self.assertEqual(self.w["next_next_chapter_CXX_heading_pdf"], 601)

    def test_04_identifiers_in_order(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(7139, 7187)),
        )
        self.assertEqual(self.r["record_count"], 48)

    def test_05_all_ten_source_groups_mapped(self):
        ids = []
        for g, reverse in zip(self.author["groups"], self.map["groups"], strict=True):
            self.assertEqual(g["source_span"], reverse["source_span"])
            self.assertEqual(g["original_pdf_pages"], reverse["original_pdf_pages"])
            expected = [x["id"] for x in g["claims"]]
            self.assertEqual(reverse["record_ids"], expected)
            ids.extend(expected)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(set(ids)), 48)

    def test_06_original_three_sources_not_one(self):
        self.assertEqual(self.types["house_window"], 2)
        self.assertEqual(self.types["house_lord"], 1)
        self.assertEqual(self.types["interceptions"], 1)
        self.assertIn("five degrees preceding", self.text())

    def test_07_mars_brothers_moon_sisters_separate(self):
        self.assertEqual(self.types["brother_significator"], 1)
        self.assertEqual(self.types["sister_significator"], 1)

    def test_08_many_requires_planet_and_sign(self):
        self.assertEqual(self.types["many_condition"], 3)
        self.assertEqual(self.types["many_result"], 1)
        self.assertIn("greater part", self.text())
        self.assertIn("prolificall Signes", self.text())

    def test_09_barren_and_mixed_cases_not_erased(self):
        self.assertEqual(self.types["few_condition"], 1)
        self.assertEqual(self.types["few_result"], 1)
        self.assertEqual(self.types["mixed_condition"], 1)
        self.assertEqual(self.types["mixed_result"], 1)

    def test_10_number_and_potency_separate(self):
        self.assertEqual(self.types["ranking_rule"], 2)
        self.assertIn("number of Significators", self.text())
        self.assertIn("their potency", self.text())

    def test_11_venus_jupiter_saturn_mars_and_optional_node(self):
        self.assertEqual(self.types["fruitful_planets"], 1)
        self.assertEqual(self.types["barren_planets"], 1)
        self.assertEqual(self.types["node_optional"], 1)
        self.assertEqual(self.types["barren_node"], 1)
        self.assertIn("some do adde", self.text())

    def test_12_luminaries_and_mercury_conditional(self):
        for role in (
            "luminaries_middle",
            "sun_modifier",
            "moon_modifier",
            "mercury_neutral",
            "mercury_fruitful",
            "mercury_barren",
        ):
            self.assertEqual(self.types[role], 1)

    def test_13_full_aspect_priority_including_partile(self):
        self.assertEqual(self.types["aspect_priority"], 5)
        text = self.text()
        for marker in (
            "Conjunction preferred before Trine",
            "Trine before Sextile",
            "Sextile before Square",
            "Square before Opposition",
            "Partill aspect before a Platick",
        ):
            self.assertIn(marker, text)

    def test_14_all_twelve_zodiac_signs_once(self):
        rows = [x for x in self.r["rules"] if x["role"] == "sign_source"]
        self.assertEqual(len(rows), 12)
        for name in (
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ):
            self.assertEqual(
                sum(name in row["original_anchor_not_diplomatic"] for row in rows),
                1,
                name,
            )

    def test_15_scorpio_exception_prevents_mars_shortcut(self):
        text = next(
            x["meaning_historical_only"]
            for x in self.r["rules"]
            if x["role"] == "sign_source" and "Scorpio" in x["original_anchor_not_diplomatic"]
        )
        self.assertIn("exception", text.lower())

    def test_16_optional_glyph_and_biological_uncertainties(self):
        self.assertTrue(any("glyph" in x for x in self.limits["issues"]))
        self.assertTrue(any("family planning" in x for x in self.limits["issues"]))
        self.assertGreaterEqual(len(self.limits["issues"]), 13)

    def test_17_next_chapter_navigation_only(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R7185", "R7186"],
        )
        self.assertEqual(self.r["substantive_historical_records"], 46)

    def test_18_no_real_demographic_or_health_predictions(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_family_count_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for r in self.r["rules"]:
            self.assertFalse(r["independent_sibling_number_validation"])
            self.assertFalse(r["human_sex_or_fertility_prediction_validated"])
            self.assertFalse(r["clinical_or_family_planning_advice_authorized"])
            self.assertFalse(r["runtime_rule_promoted"])

    def test_19_documentary_not_diplomatic(self):
        self.assertFalse(self.r["diplomatic_transcription_complete"])
        self.assertEqual(self.map["sign_specific_records"], 12)
        self.assertEqual(self.map["next_navigation"], 2)

    def test_20_canonical_calculation_and_rules_checksum(self):
        self.assertEqual(self.a["previous_lilly"], 7138)
        self.assertEqual(self.a["lilly_if_published"], 7186)
        self.assertEqual(self.a["combined_if_published"], 8252)
        self.assertEqual(sha(B / "RULES.json"), self.a["source_rules_sha256"])


if __name__ == "__main__":
    unittest.main()
