"""V7 structural and selected-image-consistency tests for B02v U55 snapshot.

Inherit the earlier fixed source predicates without changing historical
test files; supersede only the uncertainty-count fixture, and add page366
Moon-Mars OPPOSITION + exact before-change bytes checks. Neither a passing
suite nor a source paraphrase proves actual crime or astrology validity.
"""
import json, hashlib, unittest
import test_source_integrity_v6 as prior
P=prior.prior.P
B=prior.prior.B

class CurrentV7(prior.CurrentV6):
    def test_unresolved_53_and_unique_ids(self):
        u=json.loads((B/"UNRESOLVED_DRAFT.json").read_text())
        self.assertEqual((u["retained_count"],len(u["issues"])),(55,55))
        self.assertEqual(len({r["id"] for r in u["issues"]}),55)
        self.assertEqual(u["issues"][-1]["id"],"U55")
    def test_final_p366_capture_opposition_not_conjunction(self):
        r=P[2973]
        self.assertEqual(r["source_record_kind"],"other_capture_moon_eighth_opposition_mars_second")
        self.assertEqual(r["source_locator"]["pdf_pages"],[400])
        self.assertIn("OPPOSITION",r["source_statement"])
        self.assertIn("Moon in the eighth",r["source_statement"])
        self.assertIn("Mars in the second",r["source_statement"])
        self.assertIn("it does not prescribe conjunction",r["source_statement"])
        self.assertFalse(r["case_evidence_countable"])
        self.assertFalse(r["prospective_blinded_prediction"])
    def test_original_p400_evidence_and_previous_producer_preserved(self):
        image=next(x for x in prior.prior.M["images"] if x["pdf_page"]==400)
        self.assertEqual(hashlib.sha256((B/image["path"]).read_bytes()).hexdigest(),image["sha256"])
        backup=B/"recovery/producer_p398_400_before_20261014_p366_opposition_fix.json"
        self.assertEqual(hashlib.sha256(backup.read_bytes()).hexdigest(),"764dc513c0614ef0b79132d02a9c462b2183005beb0cd32593c5e0a8004d71ca")
    def test_canonical_unchanged(self):
        self.assertFalse(prior.prior.R["accepted"])
        self.assertEqual(prior.prior.C["accepted_new_documentary_records"],0)
        self.assertEqual(prior.prior.C["accepted_lilly_before"],2572)
        self.assertEqual(len(prior.prior.R["records"]),402)
if __name__=="__main__":
    unittest.main()
