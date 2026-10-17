"""Original Lilly CXXX servants/livestock documentary checks; NOT ethics inference."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class OriginalServantsCattle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_images_original_sha_and_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(620, 628)])
        for row in self.w["images"].values():
            path = B / row["path"]
            data = path.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_02_chapter_and_following_unnumbered_seventh_house(self):
        self.assertEqual(self.w["body_original_pdf_frame"], 620)
        self.assertEqual(self.w["unnumbered_seventh_house_start_pdf_frame"], 621)
        self.assertEqual(self.w["end_of_original_pdf_620_handover_word"], "The")
        self.assertIn("seventh House", self.w["following_pdf_621_heading"])
        self.assertEqual(self.a["printed_chapter"], "CXXX")
        self.assertEqual(self.a["following_pdf_frame"], 621)

    def test_03_record_ids_contiguous(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(7836, 7878)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 42)

    def test_04_every_original_passage_reversibly_mapped(self):
        ids = []
        for source, mapped in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], mapped["source_span"])
            self.assertEqual(source["original_pdf_frames"], mapped["original_pdf_frames"])
            refs = [c["id"] for c in source["clauses"]]
            self.assertEqual(mapped["mapped_record_ids"], refs)
            ids.extend(refs)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 8)

    def test_05_three_classes_of_servant_significators(self):
        self.assertEqual(self.roles["significator"], 4)
        for term in ("sixt house", "Lord thereof", "Mercury", "Planets in sixt"):
            self.assertIn(term, self.anchors)

    def test_06_majority_benefic_or_strong_and_opposite(self):
        for role in (
            "favourable_testimony",
            "favourable_alternative",
            "many_servants",
            "servants_profitable",
            "contrary_condition",
            "contrary_result",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_07_small_cattle_economic_result_is_separate(self):
        self.assertEqual(self.roles["cattle_extension"], 1)
        self.assertEqual(self.roles["cattle_profit"], 1)

    def test_08_dignified_malefic_with_good_aspect_exemption(self):
        for role in (
            "malefic_indication",
            "malefic_servant_role",
            "malefic_aspect",
            "malefic_positive",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_09_sixth_ruler_angle_versus_tenth_promotion(self):
        self.assertEqual(self.roles["sixth_ruler_angle"], 1)
        self.assertEqual(self.roles["sixth_ruler_good"], 1)
        self.assertEqual(self.roles["sixth_ruler_tenth"], 1)
        self.assertEqual(self.roles["servants_promotion"], 1)

    def test_10_mercury_many_faithful_servants_preconditions(self):
        for role in (
            "mercury_well",
            "mercury_house",
            "mercury_application",
            "mercury_sign",
            "mercury_many",
            "mercury_faithful",
        ):
            self.assertEqual(self.roles[role], 1)
        ambiguous = next(x for x in self.r["rules"] if x["role"] == "mercury_application")
        self.assertEqual(ambiguous["qualification"], "glyph-unresolved")

    def test_11_mercury_combust_retrograde_fixed_and_opposite_fortune(self):
        for role in (
            "mercury_retrograde",
            "mercury_combust",
            "mercury_infortunes",
            "mercury_negative",
            "fortune_house",
            "fortune_profitable",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_12_saturn_node_mars_air_fire_and_sixth_qualifiers(self):
        for role in (
            "saturn_peregrine",
            "node_or_mars",
            "elemental_signs",
            "sixth_house",
            "negative_thieves",
            "negative_profit",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_13_seventh_marriage_is_navigation_only_not_numbered(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_section_navigation"],
            ["R7876", "R7877"],
        )
        self.assertEqual(self.r["substantive_source_annotations"], 40)
        self.assertEqual(self.acc["next_source"], "UNNUMBERED_SEVENTH_HOUSE_MARRIAGE")
        self.assertEqual(self.acc["numbered_chapters_added"], 1)

    def test_14_no_real_workers_ethics_or_criminality_inferences(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["real_workers_or_cattle_outcomes_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.limits["criminality_classification_authorized"])
        for x in self.r["rules"]:
            self.assertFalse(x["independent_human_worker_ethics_accuracy_validated"])
            self.assertFalse(x["worker_criminality_or_dishonesty_allegation_authorized"])
            self.assertFalse(x["actual_livestock_economic_outcome_validated"])
            self.assertFalse(x["employment_or_financial_advice_authorized"])
            self.assertFalse(x["runtime_model_promoted"])

    def test_15_source_counts_sha_not_diplomatic(self):
        self.assertEqual(self.acc["prior_lilly"], 7835)
        self.assertEqual(self.acc["lilly_if_published"], 7877)
        self.assertEqual(self.acc["combined_if_published"], 8943)
        self.assertFalse(self.r["diplomatic_transcription_complete"])
        self.assertGreaterEqual(len(self.limits["issues"]), 12)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
