"""Source-only coverage, exceptions and hash tests for Lilly 1647 body bulk."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class MatureBodySourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.q = j("ACCEPTANCE.json")
        cls.u = j("UNRESOLVED_SOURCE_LIMITS.json")

    def test_01_original_image_hash_and_magic(self):
        for img in self.w["images"].values():
            path = B / img["path"]
            self.assertEqual(h(path), img["sha256"])
            self.assertEqual(path.stat().st_size, img["bytes"])
            self.assertEqual(path.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_02_printed_folio_anomalies_not_reordered(self):
        self.assertEqual(
            [p["original_printed_folio"] for p in self.w["images"].values()],
            ["549", "542", "543", "552"],
        )
        self.assertEqual(self.w["body_pdf_frames"], [583, 584])

    def test_03_record_ids_consecutive(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(6734, 6765)),
        )

    def test_04_mapping_bidirectional(self):
        all_ids = []
        for original, reverse in zip(self.a["source_groups"], self.m["source_groups"], strict=True):
            self.assertEqual(original["source_span"], reverse["source_span"])
            self.assertEqual(original["original_pdf_frames"], reverse["pdf_pages"])
            refs = [c["id"] for c in original["claims"]]
            self.assertEqual(refs, reverse["record_ids"])
            all_ids.extend(refs)
        self.assertEqual(all_ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual(len(self.m["source_groups"]), 13)

    def test_05_adult_onset_qualified_not_a_treatment_claim(self):
        anchors = " ".join(r["anchor_not_diplomatic"] for r in self.r["rules"])
        self.assertIn("full age", anchors)
        self.assertIn("about thirty", anchors)

    def test_06_12_signs_exactly_once_in_groups(self):
        rows = [r for r in self.r["rules"] if r["role"] in ("zodiac_half", "zodiac_group")]
        text = " ".join(r["anchor_not_diplomatic"] for r in rows)
        for sign in [
            "Aries",
            "Taurus",
            "Leo",
            "Gemini",
            "Scorpio",
            "Cancer",
            "Capricorn",
            "Sagittarius",
            "Aquarius",
            "Pisces",
            "Libra",
            "Virgo",
        ]:
            self.assertIn(sign, text)
        self.assertEqual(len(rows), 9)

    def test_07_early_late_divisions_not_mixed(self):
        roles = Counter(r["role"] for r in self.r["rules"])
        self.assertEqual(roles["zodiac_half"], 8)
        self.assertEqual(roles["zodiac_half_exception"], 1)
        self.assertEqual(roles["zodiac_group"], 1)

    def test_08_explicit_late_aquarius_exception(self):
        self.assertTrue(
            any(
                r["role"] == "zodiac_half_exception" and "Aquarius" in r["anchor_not_diplomatic"]
                for r in self.r["rules"]
            )
        )

    def test_09_significator_and_aspect_contingencies(self):
        roles = Counter(r["role"] for r in self.r["rules"])
        self.assertEqual(roles["primary_significator"], 2)
        self.assertEqual(roles["selection"], 2)
        self.assertEqual(roles["selection_condition"], 1)

    def test_10_almuten_unoccupied_moiety_not_omitted(self):
        fallback = [r for r in self.r["rules"] if r["role"] == "fallback"]
        self.assertEqual(len(fallback), 2)
        self.assertTrue(any("Almuten" in r["anchor_not_diplomatic"] for r in fallback))
        self.assertIn("Almuten", " ".join(self.u["issues"]))

    def test_11_conjunction_requires_mars_absence(self):
        rows = [r for r in self.r["rules"] if r["role"] == "solar_condition"]
        self.assertEqual(len(rows), 3)
        self.assertIn("Mars being absent", " ".join(r["anchor_not_diplomatic"] for r in rows))
        self.assertTrue(any("agreement" in r["meaning_historical_only"] for r in rows))

    def test_12_equivalent_dominion_tiebreaker(self):
        rows = [r for r in self.r["rules"] if r["role"] == "tiebreak"]
        self.assertEqual(len(rows), 3)
        text = " ".join(r["anchor_not_diplomatic"] for r in rows)
        self.assertIn("equall dominion", text)
        self.assertIn("partilly", text)
        self.assertIn("Exaltation", text)

    def test_13_declined_stigmatizing_premodern_category(self):
        rows = [r for r in self.r["rules"] if r["role"] == "limitation"]
        self.assertEqual(len(rows), 2)
        self.assertTrue(any("forbeare" in r["anchor_not_diplomatic"] for r in rows))
        self.assertTrue(self.u["no_clinical_or_personal_disability_inference"])

    def test_14_navigation_not_in_substantive(self):
        rows = [r for r in self.r["rules"] if r["role"] == "next_chapter_navigation"]
        self.assertEqual([r["id"] for r in rows], ["R6763", "R6764"])
        self.assertEqual(self.q["original_following_pdf_frame"], 585)
        self.assertEqual(self.r["substantive_historical_annotations"], 29)

    def test_15_no_empirical_appearance_or_medical_validations(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["real_human_body_size_validation"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            self.assertFalse(row["independent_human_size_validation"])
            self.assertFalse(row["medical_or_metabolic_validation"])
            self.assertFalse(row["ancestry_or_stigma_classification_validated"])
            self.assertFalse(row["runtime_rule_promoted"])

    def test_16_corpus_index_and_accepted_hash(self):
        self.assertEqual(self.q["previous_lilly"], 6733)
        self.assertEqual(self.q["lilly_if_published"], 6764)
        self.assertEqual(self.q["total_historical_if_published"], 7830)
        self.assertEqual(h(B / "RULES.json"), self.q["rules_sha256"])

    def test_17_all_source_scope_restrictions(self):
        self.assertFalse(self.u["diplomatic_transcription_complete"])
        self.assertGreaterEqual(len(self.u["issues"]), 10)
        notes = " ".join(self.u["issues"])
        self.assertIn("degree cutoffs", notes)
        self.assertIn("blind", notes)
        self.assertIn("sex, cohort", notes)


if __name__ == "__main__":
    unittest.main()
