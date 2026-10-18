"""CLVI and directions original 1647 source windows; NOT predictive/annotation acceptance."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3] if len(B.parents) > 3 else B.parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalDeathDirectionsWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clvi = read("ORIGINAL_CLVI_WINDOW_AND_LIMITS_20261018.json")
        cls.photos = read("ORIGINAL_SOURCE_WINDOW_WITNESS.json")
        cls.directions = read("ORIGINAL_DIRECTIONS_WINDOW_20261018.json")
        cls.index = (
            json.loads(
                (
                    ROOT / "tasks/astro-source-audit-multipass-20261005/"
                    "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
                ).read_text()
            )
            if (
                ROOT / "tasks/astro-source-audit-multipass-20261005/"
                "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
            ).exists()
            else None
        )

    def test_01_first_edition_photos_678_through_685(self):
        self.assertEqual(
            list(self.photos["source_images"]),
            [str(n) for n in range(678, 686)],
        )
        for item in self.photos["source_images"].values():
            raw = (B / item["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertGreater(len(raw), 150000)
            self.assertEqual(len(raw), item["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])

    def test_02_direction_photos_685_through_690(self):
        self.assertEqual(list(self.directions["source_images"]), [str(n) for n in range(685, 691)])
        for item in self.directions["source_images"].values():
            raw = (B / item["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), item["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])

    def test_03_overlap_page_685_same_exact_SHA(self):
        a = self.photos["source_images"]["685"]
        b = self.directions["source_images"]["685"]
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertEqual(a["bytes"], b["bytes"])

    def test_04_accurate_body_CLVI_seven_frames(self):
        self.assertEqual(self.clvi["body_pdf_frames"], list(range(678, 685)))
        self.assertEqual(self.photos["body_frames"], list(range(678, 685)))
        self.assertEqual(self.photos["printed_chapter"], "CLVI")

    def test_05_next_source_unnumbered_685(self):
        self.assertEqual(self.clvi["following_unnumbered"]["starts_pdf"], 685)
        self.assertEqual(self.directions["starts_pdf"], 685)
        self.assertEqual(self.directions["printed_page_start"], 651)

    def test_06_directions_next_printed_CLVII_688(self):
        self.assertEqual(self.directions["next_printed"], "CLVII")
        self.assertEqual(self.directions["next_printed_heading_pdf"], 688)

    def test_07_directions_following_CLVIII_pdf690(self):
        self.assertEqual(self.directions["following_numbered"], "CLVIII")
        self.assertEqual(self.directions["following_numbered_heading_pdf"], 690)

    def test_08_author_source_limits_not_person_risk(self):
        self.assertTrue(self.clvi["source_limits"]["no_person_level_mortality_forecasts"])
        self.assertTrue(self.clvi["source_limits"]["author_advises_against_certain_death_timing"])
        self.assertEqual(self.clvi["source_limits"]["independently_validated_humans"], 0)
        self.assertEqual(self.photos["person_level_mortality_accuracy_validated"], 0)

    def test_09_no_new_canonical_rules_or_model_promotions(self):
        self.assertEqual(self.photos["admitted_new_historical_rules"], 0)
        self.assertEqual(self.directions["documentary_records_admitted"], 0)
        self.assertEqual(self.photos["runtime_promotions"], 0)
        self.assertEqual(self.directions["runtime_promotions"], 0)

    def test_10_canonical_accepted_frontier_remains_CLVI_next(self):
        if self.index is not None:
            self.assertEqual(self.index["records_count"], 10246)
            self.assertEqual(self.index["batches"][-1]["id"], "B07j")
            self.assertEqual(self.index["next"]["printed_chapter_numeral"], "CLVI")
            self.assertEqual(self.index["next"]["pdf_page"], 678)


if __name__ == "__main__":
    unittest.main()
