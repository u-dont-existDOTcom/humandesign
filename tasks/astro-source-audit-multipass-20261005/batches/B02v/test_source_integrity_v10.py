"""V10 historical-source-only checks for printed p360 ambiguity U61-U63.

Inherit V9's earlier image and source-integrity assertions without changing
historical fixture. Passing is not 402-unit fidelity certification.
"""
import hashlib, json, unittest
import test_source_integrity_v9 as earlier

B=earlier.B
P=earlier.P
class CurrentV10(earlier.CurrentV9):
    def test_unresolved_53_and_unique_ids(self):
        j=json.loads((B/"UNRESOLVED_DRAFT.json").read_text())
        self.assertEqual(j["retained_count"],63)
        self.assertEqual(len(j["issues"]),63)
        self.assertEqual(len({x["id"] for x in j["issues"]}),63)
        self.assertEqual([x["id"] for x in j["issues"][-3:]],["U61","U62","U63"])
    def test_p360_source_condition_restored(self):
        r=P[2828]
        self.assertEqual(r["source_record_kind"],"suspect_stronger_lord1_moon_separation_evil_conditional")
        self.assertIn("select",r["preconditions"][0])
        self.assertIn("separation",r["source_statement"])
        self.assertIn("second-house lord",r["source_statement"])
        self.assertIn("hath played the Thiefe",r["exceptions_and_evidence_limits"][0])
        self.assertFalse(r["case_evidence_countable"])
    def test_p360_truth_referent_not_overinterpreted(self):
        a=P[2829]
        b=P[2830]
        self.assertEqual(a["source_record_kind"],"first_angular_cadent_truth_said_ambiguous_referent")
        self.assertEqual(b["source_record_kind"],"moon_angular_joins_same_ambiguous_truth_consequent")
        self.assertIn("truth is said of him",a["source_statement"])
        self.assertIn("signifie the same",b["source_statement"])
        self.assertNotIn("truthfulness testimony",b["source_statement"])
        self.assertNotIn("said to tell truth",a["source_statement"])
        self.assertEqual(a["source_locator"]["pdf_pages"],[394])
        self.assertEqual(b["source_locator"]["pdf_pages"],[394])
    def test_original_prior_producer_and_scan_immutable(self):
        p=B/"recovery/producer_p393_395_before_20261015_U61_U63_p360.json"
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),"2908da4463611476649e88d022e903fed4e06f495def259d443f3961c47c299a")
        m=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
        z=next(x for x in m["images"] if x["pdf_page"]==394)
        self.assertEqual(hashlib.sha256((B/z["path"]).read_bytes()).hexdigest(),z["sha256"])
    def test_provisional_no_canonical_index_advance(self):
        j=json.loads((B/"COUNTS.json").read_text())
        self.assertEqual(j["accepted_new_documentary_records"],0)
        self.assertEqual(j["accepted_lilly_before"],2572)
        self.assertFalse(json.loads((B/"RULES_DRAFT.json").read_text())["accepted"])
        self.assertEqual(len(json.loads((B/"RULES_DRAFT.json").read_text())["records"]),402)
if __name__=="__main__":unittest.main()
