"""V8 source-only regression for printed357/363 clause changes U56-U58.

Retain earlier V5/V6/V7 checks and original fixture files. Passing proves
internal state and selected source readings, not exhaustive text fidelity.
"""
import json,hashlib,unittest
import test_source_integrity_v7 as prior
B=prior.B
P=prior.P
class CurrentV8(prior.CurrentV7):
    def test_unresolved_53_and_unique_ids(self):
        u=json.loads((B/"UNRESOLVED_DRAFT.json").read_text())
        self.assertEqual((u["retained_count"],len(u["issues"])),(58,58))
        self.assertEqual(len({x["id"] for x in u["issues"]}),58)
        self.assertEqual([x["id"] for x in u["issues"][-3:]],["U56","U57","U58"])
    def test_p357_recovery_consequent_plus_timing(self):
        x=P[2762]
        self.assertEqual(x["source_record_kind"],"bodily_application_recovery_with_timing")
        self.assertIn("will THEN be recovered",x["source_statement"])
        self.assertIn("retrograde/direct",x["source_statement"])
        self.assertEqual(x["source_locator"]["pdf_pages"],[391])
        self.assertFalse(x["case_evidence_countable"])
    def test_p363_plural_not_singular(self):
        x=P[2895]
        self.assertEqual(x["source_record_kind"],"knave_significators_plural_change_sign")
        self.assertIn("the Significators",x["source_statement"])
        self.assertIn("which/how many",x["source_statement"])
        self.assertEqual(x["source_locator"]["pdf_pages"],[397])
    def test_p363_beholding_actor_unassigned(self):
        x=P[2901]
        self.assertEqual(x["source_record_kind"],"remains_first_cadent_behold_asc_actor_unspecified")
        self.assertIn("without unambiguously identifying",x["source_statement"])
        self.assertEqual(x["source_locator"]["pdf_pages"],[397])
        self.assertFalse(x["prospective_blinded_prediction"])
    def test_before_change_bytes_and_original_images(self):
        frozen={
         "producer_p391_392_pre_U56_20261014.json":"bfde726a22a1519eeab743168252bd8ba905d63cf0fc95812ddbea992935e5b8",
         "producer_p396_397_pre_U57_U58_20261014.json":"4d6c0c0fdf6e305a79532914741cb3a359f7e2d8023fa8a1e43f92acd0a35a28"}
        for name,digest in frozen.items():
            self.assertEqual(hashlib.sha256((B/"recovery"/name).read_bytes()).hexdigest(),digest)
        m=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
        for pg in [391,397]:
            e=next(x for x in m["images"] if x["pdf_page"]==pg)
            self.assertEqual(hashlib.sha256((B/e["path"]).read_bytes()).hexdigest(),e["sha256"])
if __name__=="__main__":unittest.main()
