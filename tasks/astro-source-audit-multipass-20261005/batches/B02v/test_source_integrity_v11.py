"""V11 source-only fixture for U61–U64, source-PDF393–395 corrections."""
import hashlib,json,unittest
import test_source_integrity_v10 as prev
B=prev.B
P=prev.P
class CurrentV11(prev.CurrentV10):
    def test_unresolved_53_and_unique_ids(self):
        j=json.loads((B/"UNRESOLVED_DRAFT.json").read_text())
        self.assertEqual(j["retained_count"],64)
        self.assertEqual(len(j["issues"]),64)
        self.assertEqual(len({x["id"] for x in j["issues"]}),64)
        self.assertEqual([x["id"] for x in j["issues"][-4:]],["U61","U62","U63","U64"])
    def test_p361_peregrines_no_minimum_count(self):
        r=P[2855]
        self.assertEqual(r["source_record_kind"],"many_thieves_peregrine_planets_angular_unspecified_count")
        self.assertEqual(r["source_locator"]["pdf_pages"],[395])
        self.assertIn("no minimum COUNT",r["source_statement"])
        self.assertIn("plural generic",r["preconditions"][0])
        self.assertIn("Many Thieves",r["preconditions"][0])
        self.assertNotIn("angular placement of multiple planets",r["preconditions"][0])
        self.assertFalse(r["prospective_blinded_prediction"])
    def test_before_U64_file_and_original_395(self):
        orig=B/"recovery/producer_p393_395_pre_U64_20261015.json"
        self.assertEqual(hashlib.sha256(orig.read_bytes()).hexdigest(),"ff8492a92b503654d57261b35d75e048fe4441709cbd6f57c0a9f10314e3079a")
        m=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
        w=next(x for x in m["images"] if x["pdf_page"]==395)
        self.assertEqual(hashlib.sha256((B/w["path"]).read_bytes()).hexdigest(),w["sha256"])
if __name__=="__main__":unittest.main()
