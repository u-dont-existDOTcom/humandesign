"""First-edition stature chapter historical-documentary checks, not validity tests."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent


def j(file):
    return json.loads((B / file).read_text())


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class FirstEditionStature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = j("SOURCE_FIRST_AUTHORING.json")
        cls.a = j("ACCEPTANCE.json")
        cls.r = j("RULES.json")
        cls.images = j("ORIGINAL_IMAGE_MANIFEST.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.unresolved = j("UNRESOLVED.json")

    def test_original_pages_and_physical_folio(self):
        self.assertEqual(
            [(n, f["printed_folio_as_seen"]) for n, f in self.images["images"].items()],
            [("580", "538"), ("581", "539"), ("582", "548")],
        )
        self.assertIn("continuous", self.images["pagination_note"])

    def test_image_sha256_bytes_and_jpeg_magic(self):
        for page in self.images["images"].values():
            path = B / page["file"]
            self.assertEqual(sha(path), page["sha256"])
            self.assertEqual(path.stat().st_size, page["bytes"])
            self.assertEqual(path.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_consecutive_ids(self):
        self.assertEqual([r["record_number"] for r in self.r["rules"]], list(range(6645, 6672)))
        self.assertEqual(self.r["record_count"], 27)

    def test_bidirectional_mapping_unique_complete(self):
        found = []
        for orig, cross in zip(self.input["groups"], self.map["groups"], strict=True):
            self.assertEqual(orig["id"], cross["source_span"])
            self.assertEqual(orig["original_pdf_pages"], cross["pdf_pages"])
            expected = [c["record"] for c in orig["claims"]]
            self.assertEqual(expected, cross["mapped_record_ids"])
            found.extend(expected)
        self.assertEqual(found, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(found), len(set(found)))

    def test_all_five_planets_both_orientations(self):
        pairs = [
            (r["original_anchor_not_diplomatic"].split()[0], r["role"])
            for r in self.r["rules"]
            if r["role"] in ("oriental", "occidental")
        ]
        self.assertEqual(len(pairs), 10)
        self.assertEqual(
            pairs,
            [
                (planet, direction)
                for planet in ("Saturn", "Jupiter", "Mars", "Venus", "Mercury")
                for direction in ("oriental", "occidental")
            ],
        )

    def test_stature_priority_and_tiebreaker(self):
        text = " ".join(r["historical_only_meaning"] for r in self.r["rules"])
        self.assertIn("Ascendant ruler", text)
        self.assertIn("strongest", text)

    def test_mercury_and_luminary_qualifications(self):
        override = [r for r in self.r["rules"] if r["role"] in ("override", "override_condition")]
        self.assertEqual(len(override), 4)
        self.assertTrue(any("dispositor" in r["historical_only_meaning"] for r in override))
        self.assertTrue(
            any("Sun and Moon" in r["historical_only_meaning"] for r in self.r["rules"])
        )

    def test_distinct_proportions_sources(self):
        parts = [r for r in self.r["rules"] if r["role"] == "proportions_component"]
        self.assertEqual(len(parts), 5)
        joined = " ".join(r["historical_only_meaning"] for r in parts)
        for token in ["rising sign", "planets", "solar", "season", "Fixed stars"]:
            self.assertIn(token.lower(), joined.lower())

    def test_new_chapter_navigation_strictly_separate(self):
        rows = self.r["rules"]
        self.assertEqual(sum(r["role"] == "next_chapter_navigation" for r in rows), 3)
        self.assertEqual([r["record_number"] for r in rows[-3:]], [6669, 6670, 6671])
        self.assertEqual(self.a["following_chapter_pdf_frame"], 581)
        self.assertEqual(self.a["next_printed_chapter"], "CXI")

    def test_source_limitations_and_provenance(self):
        self.assertFalse(self.r["original_full_diplomatic_transcription"])
        self.assertGreaterEqual(len(self.unresolved["notes"]), 8)
        self.assertTrue(any("sex, age, cohort" in s for s in self.unresolved["notes"]))

    def test_zero_scientific_validation_and_promotion(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertEqual(self.a["new_height_validations"], 0)
        for row in self.r["rules"]:
            self.assertFalse(row["independently_tested_height_prediction"])
            self.assertFalse(row["validated_medical_or_ancestry_prediction"])
            self.assertFalse(row["promoted_into_runtime"])

    def test_documentary_integrity_and_total(self):
        self.assertEqual(sha(B / "RULES.json"), self.a["rules_sha256"])
        self.assertEqual(self.a["previous_lilly"], 6644)
        self.assertEqual(self.a["new_historical_source_annotations"], 27)
        self.assertEqual(self.a["lilly_if_published"], 6671)
        self.assertEqual(self.a["historical_combined_if_published"], 7737)


if __name__ == "__main__":
    unittest.main()
