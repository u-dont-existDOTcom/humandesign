"""Source-only regression: Haly is the attributed author and Leo the sign."""
from pathlib import Path
import unittest,json,hashlib
B=Path(__file__).resolve().parent
def load(name): return json.loads((B/name).read_text())
R=load("RULES_DRAFT.json")
U=load("UNRESOLVED_DRAFT.json")
C=load("COUNTS.json")
I=load("SOURCE_IMAGE_MANIFEST.json")
S={x["record_number"]:x for x in R["records"]}
class SourceAttribution(unittest.TestCase):
    def test_start(self):
        r=S[2674]
        self.assertEqual(r["source_record_kind"],"reported_haly_leo_venus_example_start")
        self.assertIn("Haly",r["source_statement"])
        self.assertIn("LEO",r["source_statement"])
        self.assertNotIn("Libra",r["source_statement"])
        self.assertEqual(r["source_locator"]["pdf_pages"],[386])
    def test_end(self):
        r=S[2675]
        self.assertEqual(r["source_record_kind"],"reported_haly_leo_venus_bed")
        self.assertIn("Haly",r["source_statement"])
        self.assertIn("Leo",r["source_statement"])
        self.assertIn("Venus",r["source_statement"])
        self.assertEqual(r["source_locator"]["pdf_pages"],[387])
    def test_original_pages(self):
        for pg in [386,387]:
            x=next(z for z in I["images"] if z["pdf_page"]==pg)
            self.assertEqual(hashlib.sha256((B/x["path"]).read_bytes()).hexdigest(),x["sha256"])
    def test_original_pre_edit_preserved(self):
        p=B/"recovery/producer_p385_387_before_20261014_haly_leo_source_correction.json"
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),"5129373216be687e389690d75effe52bee8b79ec5d2738a326598edb216387dc")
    def test_unaccepted(self):
        self.assertEqual(U["retained_count"],54)
        self.assertEqual(len(U["issues"]),54)
        self.assertEqual(len({x["id"] for x in U["issues"]}),54)
        self.assertEqual(U["issues"][-1]["id"],"U54")
        self.assertFalse(R["accepted"])
        self.assertEqual(C["accepted_new_documentary_records"],0)
        self.assertEqual(len(R["records"]),402)
    def test_role_scientific_separation(self):
        for n in [2674,2675]:
            self.assertFalse(S[n]["case_evidence_countable"])
            self.assertFalse(S[n]["prospective_blinded_prediction"])
if __name__=="__main__": unittest.main()
