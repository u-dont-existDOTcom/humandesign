"""Acceptance invariants for original 1647 CIX/CX historical-only intellect chapter.

These tests prove integrity and faithful preservation of *authored* mapping,
not accuracy of astrology in humans or exact diplomatic palaeography.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def H(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class SourceAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_CLAIMS_AUTHORING.json")
        cls.r = j("RULES.json")
        cls.m = j("SOURCE_TO_RECORD_REVERSE_MAP.json")
        cls.w = j("SOURCE_IMAGE_WITNESSES.json")
        cls.q = j("ACCEPTANCE.json")
        cls.u = j("UNRESOLVED_SOURCE_LIMITS.json")

    def test_first_last_count(self):
        self.assertEqual(self.r["record_count"], 53)
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(6592, 6645)))

    def test_source_group_ids_and_count(self):
        self.assertEqual(
            [s["id"] for s in self.a["source_passages"]], [f"B05h-S{i:03d}" for i in range(1, 13)]
        )
        self.assertEqual(len(self.m["source_passages"]), 12)

    def test_bidirectional_full_coverage(self):
        reverse = []
        for s, m in zip(self.a["source_passages"], self.m["source_passages"], strict=True):
            self.assertEqual(s["id"], m["source_span"])
            refs = [c["proposed_record"] for c in s["claims"]]
            self.assertEqual(refs, m["mapped_record_ids"])
            reverse.extend(refs)
        self.assertEqual(reverse, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(set(reverse)), len(reverse))

    def test_original_pages_order_sha(self):
        self.assertEqual(list(self.w["pages"].keys()), ["577", "578", "579", "580", "581"])
        for _, info in self.w["pages"].items():
            p = B / info["file"]
            self.assertEqual(H(p), info["sha256"])
            self.assertEqual(p.stat().st_size, info["bytes"])
            self.assertTrue(p.read_bytes()[:2] == bytes.fromhex("ffd8"))

    def test_original_printed_pagination_anomaly(self):
        self.assertEqual(
            [v["observed_printed_page"] for v in self.w["pages"].values()],
            ["543", "544", "545", "538", "539"],
        )
        self.assertIn("do not reorder", self.w["pdf_to_printed_note"].lower())

    def test_claim_hash_stable(self):
        self.assertEqual(H(B / "RULES.json"), self.q["accepted_rules_sha256"])

    def test_source_and_navigation_separated(self):
        roles = [r["role"] for r in self.r["rules"]]
        self.assertEqual(roles.count("next_chapter_navigation"), 3)
        self.assertEqual(len(roles) - roles.count("next_chapter_navigation"), 50)
        self.assertTrue(
            all(
                r["record_number"] >= 6642
                for r in self.r["rules"]
                if r["role"] == "next_chapter_navigation"
            )
        )

    def test_no_empirical_evidence_claim(self):
        for k in (
            "empirical_validations",
            "runtime_promotions",
            "clinical_or_intelligence_predictive_validation",
        ):
            self.assertEqual(self.r[k], 0)
        for r in self.r["rules"]:
            for key in (
                "validated_human_intelligence",
                "validated_cognitive_disability_classification",
                "validated_personality_prediction",
                "runtime_model_promoted",
            ):
                self.assertIs(r[key], False)

    def test_source_only_uncertainty_disclosed(self):
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertTrue(self.u["not_authorized_for_personality_or_medical_claims"])
        self.assertGreaterEqual(len(self.u["issues"]), 8)

    def test_mercury_moon_aspect_separation(self):
        anchors = " ".join(r["anchor_not_diplomatic"].lower() for r in self.r["rules"])
        for x in ["conjunction", "sextile", "trine", "square", "opposition", "no aspect"]:
            self.assertIn(x, anchors)
        self.assertTrue(any("preferred" in r["meaning_historical_only"] for r in self.r["rules"]))
        self.assertTrue(
            any("wit enough" in r["anchor_not_diplomatic"].lower() for r in self.r["rules"])
        )

    def test_qualified_swift_vs_slow(self):
        all_text = " ".join(r["meaning_historical_only"].lower() for r in self.r["rules"])
        for s in ["swift", "retrograde", "combust", "under-beams", "dispositor", "reception"]:
            self.assertIn(s, all_text)

    def test_disability_and_moral_stereotypes_not_promoted(self):
        text = " ".join(r["meaning_historical_only"].lower() for r in self.r["rules"])
        self.assertIn("stutter", text)
        self.assertIn("derogatory", text)
        self.assertIn("moral", text)
        self.assertEqual(self.q["medical_or_disability_validations"], 0)

    def test_limit_vague_numerics(self):
        self.assertEqual(self.a["pages"]["body"], [577, 578, 579, 580])
        self.assertEqual(self.q["next_original_pdf_page"], 580)
        self.assertIn("538", self.q["next_printed_page_as_seen"])

    def test_prior_checkpoint_not_modified(self):
        # Replaying in an archive has no parent repository; local root check if present.
        idx = B.parents[1] / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        if idx.exists():
            z = json.loads(idx.read_text())
            self.assertIn(z["records_count"], (6591, 6644))
            self.assertEqual(z["empirical_validations"], 0)

    def test_original_before_retype(self):
        self.assertIn("original 1647", self.a["method"])
        self.assertIn("modern retype", self.a["method"])
        self.assertFalse(self.r["full_diplomatic_transcription"])

    def test_accepted_counts(self):
        self.assertEqual(
            (self.q["prior_lilly"], self.q["lilly_if_published"], self.q["combined_if_published"]),
            (6591, 6644, 7710),
        )
        self.assertEqual(self.q["source_groups"], 12)

    def test_no_fitted_humans(self):
        self.assertTrue(any("no human birth times" in x.lower() for x in self.u["issues"]))
        self.assertEqual(self.q["independent_intelligence_validations"], 0)

    def test_cannot_relabel_source_claim_as_medical(self):
        for row in self.r["rules"]:
            self.assertEqual(
                row["source_limitation"],
                (
                    "Historical source assertion from 1647, not independent clinical, cognitive "
                    "or social prediction."
                ),
            )


if __name__ == "__main__":
    unittest.main()
