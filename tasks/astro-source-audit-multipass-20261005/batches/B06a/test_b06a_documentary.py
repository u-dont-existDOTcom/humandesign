"""Lilly 1647 parent-parent agreement source integrity only; not relationship forecasts."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class HistoricParentConcordSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.a = read("ACCEPTANCE.json")
        cls.types = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_original_primary_image_sha256(self):
        for info in self.w["images"].values():
            file = B / info["file"]
            raw = file.read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), info["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), info["sha256"])

    def test_02_original_folio_and_next_chapter(self):
        self.assertEqual(list(self.w["images"]), ["607", "608", "609"])
        self.assertEqual(
            [f["original_printed_folio"] for f in self.w["images"].values()],
            ["573", "574", "575"],
        )
        self.assertEqual(self.w["body_original_frame"], 607)
        self.assertEqual(self.w["following_chapter_CXXVI_frame"], 608)

    def test_03_record_ids_unique_and_consecutive(self):
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(7474, 7503)))
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 29)

    def test_04_source_groups_reversible(self):
        ordered = []
        for orig, mapped in zip(
            self.author["source_groups"],
            self.map["source_groups"],
            strict=True,
        ):
            self.assertEqual(orig["source_span"], mapped["source_span"])
            self.assertEqual(orig["original_pdf_frames"], mapped["original_pdf_frames"])
            refs = [r["id"] for r in orig["claims"]]
            self.assertEqual(refs, mapped["mapped_record_ids"])
            ordered.extend(refs)
        self.assertEqual(ordered, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.map["source_group_count"], 9)

    def test_05_day_chart_uses_sun_and_venus(self):
        self.assertEqual(self.types["diurnal_significators"], 1)
        self.assertEqual(self.types["diurnal_method"], 1)
        self.assertEqual(self.types["diurnal_alternative"], 1)
        self.assertIn("Sun and Venus", self.anchors)

    def test_06_day_positive_venus_applying_combustion_not_general(self):
        self.assertEqual(self.types["venus_condition"], 2)
        self.assertIn("going to Combustion", self.anchors)

    def test_07_negative_venus_requires_multiple_source_states(self):
        self.assertEqual(self.types["venus_negative"], 3)
        for text in ("Retrograde", "Peregrine unfortunate", "separate from Sun"):
            self.assertIn(text, self.anchors)

    def test_08_night_sun_substitute_preserves_saturn_moon(self):
        self.assertEqual(self.types["night_significators"], 1)
        self.assertEqual(self.types["night_method"], 1)
        self.assertEqual(self.types["night_favorable"], 1)
        self.assertIn("Saturn and Moon", self.anchors)

    def test_09_night_discord_square_or_opposition(self):
        self.assertEqual(self.types["night_adverse"], 2)
        self.assertIn("Square", self.anchors)
        self.assertIn("Opposition", self.anchors)

    def test_10_first_fourth_tenth_house_opposition_and_blame(self):
        self.assertEqual(self.types["house_opposition"], 1)
        self.assertEqual(self.types["house_opposition_result"], 1)
        self.assertEqual(self.types["tenth_malefic"], 1)
        self.assertEqual(self.types["fourth_malefic"], 1)
        self.assertEqual(self.types["mother_blamed"], 1)
        self.assertEqual(self.types["father_blamed"], 1)

    def test_11_next_regiomontanus_chapter_boundary(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7501", "R7502"],
        )
        self.assertEqual(self.r["substantive_historical_clauses"], 27)

    def test_12_no_validated_marital_ethics_or_runtime(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_parental_relationship_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertGreaterEqual(len(self.limits["issues"]), 9)
        for row in self.r["rules"]:
            self.assertFalse(row["actual_parental_marriage_harmony_validated"])
            self.assertFalse(row["verified_personal_ethics_or_behavior"])
            self.assertFalse(row["clinical_or_family_actions_authorized"])
            self.assertFalse(row["promoted_to_runtime"])

    def test_13_sha_source_and_corpus_size(self):
        self.assertEqual(self.a["previous_lilly"], 7473)
        self.assertEqual(self.a["lilly_if_published"], 7502)
        self.assertEqual(self.a["combined_historical_if_published"], 8568)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(), self.a["rules_sha256"]
        )


if __name__ == "__main__":
    unittest.main()
