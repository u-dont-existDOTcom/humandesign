import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
M=json.loads((B/"SOURCE_WINDOW_PROVISIONAL.json").read_text(encoding="utf-8"))
class Scope(unittest.TestCase):
    def test_primary_scans_frozen(self):
        self.assertEqual(M["body_pages"],list(range(438,447)))
        self.assertEqual(len(M["images"]),9)
        for im in M["images"]:
            b=(B/im["path"]).read_bytes()
            self.assertEqual(im["bytes"],len(b))
            self.assertEqual(im["sha256"],hashlib.sha256(b).hexdigest())
            self.assertEqual(im["printed_page"],im["original_pdf_page"]-34)
    def test_true_sequential_boundaries(self):
        self.assertEqual(M["next_chapter"],"LXVIII")
        self.assertEqual(M["next_original_pdf_page"],446)
        self.assertIn("PDF438",M["original_opening"])
        self.assertIn("PDF446",M["original_ending"])
    def test_previous_accepted_baseline_not_changed(self):
        self.assertEqual(M["accepted_predecessor_lilly_count"],3746)
        self.assertEqual(M["retained_ptolemy_count"],1066)
        self.assertFalse(M["rule_extraction_complete"])
        self.assertFalse(M["numbered_chapter_admitted"])
        self.assertEqual(M["new_source_records"],0)
    def test_no_empirical_predictions_from_scans(self):
        self.assertEqual(M["empirical_predictions_validated"],0)
        self.assertEqual(M["runtime_promotions"],0)
if __name__=="__main__":unittest.main(verbosity=2)
