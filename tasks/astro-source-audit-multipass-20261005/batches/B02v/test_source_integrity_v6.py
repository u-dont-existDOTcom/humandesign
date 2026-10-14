"""V6 documentary integrity: inherited V5 checks plus Haly/Leo correction.

Runs structural/provenance checks; NOT exhaustive semantic source review.
V5 remains historical for U53 and MUST NOT be rewritten in place.
"""
import json,hashlib
import unittest
from pathlib import Path
import test_source_integrity_v5 as prior

class CurrentV6(prior.V5OriginalSourceSafety):
    def test_unresolved_53_and_unique_ids(self):
        u=prior.U
        self.assertEqual(u["retained_count"],54)
        self.assertEqual(len(u["issues"]),54)
        self.assertEqual(len({x["id"] for x in u["issues"]}),54)
        self.assertEqual(u["issues"][-1]["id"],"U54")
    def test_quoted_haly_not_lilly(self):
        a,b=prior.P[2674],prior.P[2675]
        self.assertEqual(a["source_record_kind"],"reported_haly_leo_venus_example_start")
        self.assertEqual(b["source_record_kind"],"reported_haly_leo_venus_bed")
        self.assertIn("Haly",a["source_statement"])
        self.assertIn("Haly",b["source_statement"])
        self.assertIn("LEO",a["source_statement"])
        self.assertIn("Leo",b["source_statement"])
        self.assertIn("Venus",b["source_statement"])
        self.assertNotIn("Libra",a["source_statement"])
        self.assertEqual(a["source_locator"]["pdf_pages"],[386])
        self.assertEqual(b["source_locator"]["pdf_pages"],[387])
    def test_original_proposal_unchanged(self):
        path=prior.B/"recovery/producer_p385_387_before_20261014_haly_leo_source_correction.json"
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(actual,"5129373216be687e389690d75effe52bee8b79ec5d2738a326598edb216387dc")
    def test_no_real_world_case_promoted(self):
        for n in (2674,2675):
            x=prior.P[n]
            self.assertTrue(x["source_witness_only"])
            self.assertFalse(x["case_evidence_countable"])
            self.assertFalse(x["prospective_blinded_prediction"])
            self.assertEqual(x["runtime_status"],"REFERENCE_ONLY_NOT_PROMOTED")

if __name__=="__main__":
    unittest.main()
