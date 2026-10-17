"""Original 1647 curability chapter: documentary tests, NOT medical accuracy."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


class OriginalCurabilityHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])
        cls.text = " ".join(row["anchor_not_diplomatic"] for row in cls.r["rules"])

    def test_01_original_page_images_sha256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["619", "620", "621"])
        for info in self.w["images"].values():
            p = B / info["file"]
            content = p.read_bytes()
            self.assertEqual(content[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(content), info["bytes"])
            self.assertEqual(hashlib.sha256(content).hexdigest(), info["sha256"])

    def test_02_printed_folios_and_servants_boundary(self):
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["585", "586", "587"],
        )
        self.assertEqual(self.w["body_original_pdf_frames"], [619, 620])
        self.assertEqual(self.w["following_CXXX_heading_pdf"], 620)

    def test_03_contiguous_27_source_ids(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(7809, 7836)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 27)

    def test_04_six_source_groups_bidirectionally_complete(self):
        all_ids = []
        for authored, mapped in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], mapped["source_span"])
            self.assertEqual(authored["original_pdf_frames"], mapped["original_pdf_frames"])
            these = [x["id"] for x in authored["claims"]]
            self.assertEqual(these, mapped["mapped_record_ids"])
            all_ids.extend(these)
        self.assertEqual(all_ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 6)

    def test_05_positive_planets_aspect_plus_moveable_required(self):
        self.assertEqual(self.roles["favorable_condition"], 1)
        self.assertEqual(self.roles["favorable_aspect"], 2)
        self.assertEqual(self.roles["movable_signs"], 1)
        self.assertEqual(self.roles["easy_result"], 1)

    def test_06_fixed_sign_without_benefic_is_opposite(self):
        self.assertEqual(self.roles["fixed_signs"], 1)
        self.assertEqual(self.roles["no_fortune"], 1)
        self.assertEqual(self.roles["fixed_outcome"], 2)

    def test_07_partile_contact_and_remote_time_modifier(self):
        for role in ("proximity", "partile", "near_result", "remote_condition", "remote_result"):
            self.assertEqual(self.roles[role], 1)

    def test_08_exact_three_source_planet_aid_categories(self):
        for role in ("three_cure_sources", "jupiter_aid", "mercury_aid", "venus_aid"):
            self.assertEqual(self.roles[role], 1)
        for item in ("Money and good Counsell", "Medicine", "Magick"):
            self.assertIn(item, self.text)

    def test_09_helpers_must_be_strong_and_favorably_aspected(self):
        for role in ("cure_support", "cure_aspect", "cure_promise"):
            self.assertEqual(self.roles[role], 1)

    def test_10_domocile_and_exaltation_contrary_not_removed(self):
        self.assertEqual(self.roles["contrary_condition"], 1)
        self.assertEqual(self.roles["contrary_alternative"], 1)
        self.assertEqual(self.roles["contrary_result"], 1)
        self.assertIn("little hope of remedy", self.text)

    def test_11_following_cxxx_not_a_curability_rule(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R7834", "R7835"],
        )
        self.assertEqual(self.r["substantive_historical_clauses"], 25)
        self.assertEqual(self.accept["next_printed_chapter"], "CXXX")

    def test_12_zero_actual_patients_predictions_and_magic_advice(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["human_prognosis_outcomes_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.limits["medical_or_treatment_advice_authorized"])
        for x in self.r["rules"]:
            self.assertFalse(x["independent_disease_recovery_forecast_validated"])
            self.assertFalse(x["real_patient_diagnosis_or_prognosis_validated"])
            self.assertFalse(x["medicine_or_magic_treatment_authorized"])
            self.assertFalse(x["runtime_rule_promoted"])

    def test_13_not_diplomatic_and_uncertainties_retained(self):
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertGreaterEqual(len(self.limits["issues"]), 10)

    def test_14_canonical_numbers_and_hash(self):
        self.assertEqual(self.accept["previous_lilly"], 7808)
        self.assertEqual(self.accept["lilly_if_published"], 7835)
        self.assertEqual(self.accept["combined_if_published"], 8901)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
