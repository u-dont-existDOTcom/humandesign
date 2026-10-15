"""V9 source-only checks for original PDF396/printed362 U59-U60.

Prior V8 fixture remains immutable for the 58-issue previous snapshot.
The original primary source controls interpretation. These tests do not
establish real demographic inference or complete independent document audit.
"""
import hashlib,json,unittest
import test_source_integrity_v8 as prev
B=prev.B
P=prev.P
class CurrentV9(prev.CurrentV8):
    def test_unresolved_53_and_unique_ids(self):
        j=json.loads((B/"UNRESOLVED_DRAFT.json").read_text())
        self.assertEqual(j["retained_count"],60)
        self.assertEqual(len(j["issues"]),60)
        self.assertEqual(len({x["id"] for x in j["issues"]}),60)
        self.assertEqual([x["id"] for x in j["issues"][-2:]],["U59","U60"])
    def test_p362_age_or_thief_significator(self):
        r=P[2871]
        self.assertEqual(r["source_locator"]["pdf_pages"],[396])
        self.assertEqual(r["source_record_kind"],"age_moon_applying_planet_or_thief_significator")
        self.assertIn("OR the age of the thief",r["source_statement"])
        self.assertIn("neither is necessarily the other",r["preconditions"][0])
        self.assertFalse(r["case_evidence_countable"])
    def test_p362_stature_or_not_and(self):
        r=P[2876]
        self.assertEqual(r["source_record_kind"],"stature_small_occidental_or_water_signs")
        self.assertEqual(r["source_locator"]["pdf_pages"],[396])
        self.assertIn("OR if",r["source_statement"])
        self.assertIn("not AND",r["preconditions"][0])
        self.assertFalse(r["prospective_blinded_prediction"])
    def test_original_producer_backup_and_image(self):
        q=B/"recovery/producer_p396_397_pre_U59_U60_20261015.json"
        self.assertEqual(hashlib.sha256(q.read_bytes()).hexdigest(),
         "1f4e8755a3babe464c1c5fdadfd66dc8cc2b1ed3d01213c0ffc22a228e49eaf8")
        m=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
        e=next(x for x in m["images"] if x["pdf_page"]==396)
        self.assertEqual(hashlib.sha256((B/e["path"]).read_bytes()).hexdigest(),e["sha256"])
    def test_inventory_still_unaccepted(self):
        j=json.loads((B/"COUNTS.json").read_text())
        self.assertEqual(j["accepted_new_documentary_records"],0)
        self.assertEqual(j["accepted_lilly_before"],2572)
        self.assertEqual(len(json.loads((B/"RULES_DRAFT.json").read_text())["records"]),402)
if __name__=="__main__":unittest.main()
