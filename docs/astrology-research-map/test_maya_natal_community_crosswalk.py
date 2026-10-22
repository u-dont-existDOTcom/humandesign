#!/usr/bin/env python3
"""Maya natal source/domain separation tests, not human predictive tests."""
import json
from pathlib import Path
import unittest
from maya_calendar_reference import KICHE_DAY_NAMES_BY_YUCATEC,YUCATEC_DAYS

CROSSWALK=json.loads(Path(__file__).with_name(
  "MAYA_MOMOSTENANGO_ZUNIL_NATAL_DOMAIN_CROSSWALK_V1.json").read_text(encoding="utf-8"))

class MayaCommunityNatalSourceTests(unittest.TestCase):
    def test_twenty_unique_semantic_source_pairs(self):
        records=CROSSWALK["records"]
        self.assertEqual(len(records),20)
        self.assertEqual(CROSSWALK["count"],20)
        self.assertEqual(len({r["kiche_reference_name"] for r in records}),20)
        mapping=dict(zip(YUCATEC_DAYS,KICHE_DAY_NAMES_BY_YUCATEC))
        for r in records:
            self.assertEqual(mapping[r["yucatec_crosswalk"]],r["kiche_reference_name"])
            self.assertTrue(r["momostenango_natal_domain_labels"])
            self.assertTrue(r["zunil_natal_domain_labels"])
            self.assertFalse(r["source_predicate_frozen"])

    def test_noj_natal_creativity_single_community_not_cross_replication(self):
        x={r["kiche_reference_name"]:r for r in CROSSWALK["records"]}
        self.assertEqual(x["NO’J"]["momostenango_page"],122)
        self.assertEqual(x["NO’J"]["zunil_pdf_page"],2)
        self.assertIn("creative",x["NO’J"]["momostenango_natal_domain_labels"])
        self.assertNotIn("creative",x["NO’J"]["zunil_natal_domain_labels"])
        self.assertIn("creativity",x["IMOX"]["zunil_natal_domain_labels"])

    def test_toj_medical_ascription_never_translated_to_claim_of_fact(self):
        x={r["kiche_reference_name"]:r for r in CROSSWALK["records"]}
        self.assertIn("debt",x["TOJ"]["momostenango_natal_domain_labels"])
        self.assertIn("mediation",x["TOJ"]["zunil_natal_domain_labels"])
        self.assertIsNotNone(x["TOJ"]["stigma_or_safety_quarantine"])
        self.assertIsNotNone(x["TZ’I’"]["stigma_or_safety_quarantine"])

    def test_status_remains_source_only_without_any_human_promotion(self):
        self.assertEqual(CROSSWALK["statuses"]["human_blind_predictive_results"],0)
        self.assertEqual(CROSSWALK["statuses"]["scored_natal_rules"],0)
        self.assertEqual(CROSSWALK["source_a"]["community"],"Momostenango, K'iche'")
        self.assertIn("Zunil",CROSSWALK["source_b"]["community"])
        for r in CROSSWALK["records"]:
            self.assertEqual(r["human_prediction_status"],"UNTESTED")

    def test_no_copyrighted_books_in_crosswalk_and_hashes_present(self):
        for s in [CROSSWALK["source_a"],CROSSWALK["source_b"]]:
            self.assertFalse(s["source_file_copied_into_repo"])
            self.assertRegex(s["file_sha256"],r"^[a-f0-9]{64}$")

if __name__=="__main__":
    unittest.main()
