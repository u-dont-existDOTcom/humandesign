"""Source-only checks after selective original-image review; do NOT certify full-text fidelity."""
import json, hashlib, unittest
from pathlib import Path
B=Path(__file__).resolve().parents[1]
def load(name): return json.loads((B/name).read_text())
R=load("RULES_DRAFT.json")
C=load("COUNTS.json")
M=load("SOURCE_IMAGE_MANIFEST.json")
I=load("RETAINED_LILLY_INDEX_BEFORE.json")
U=load("UNRESOLVED_DRAFT.json")
E=load("ERRATA_COLLATION.json")
P={r["record_number"]:r for r in R["records"]}
class ReviewCoherence(unittest.TestCase):
    def test_count_and_consecutive_ids(self):
        self.assertEqual(len(R["records"]),402)
        self.assertEqual([r["record_number"] for r in R["records"]],list(range(2573,2975)))
        self.assertEqual([r["id"] for r in R["records"]],["LI.1647.II.L.R"+str(i) for i in range(2573,2975)])
    def test_baseline_retained(self):
        self.assertEqual(I["records_count"],2572)
        self.assertEqual(I["batches"][-1]["id"],"B02u")
        self.assertEqual(C["accepted_lilly_before"],2572)
        self.assertEqual(C["retained_ptolemy"],1066)
        self.assertEqual(C["accepted_new_documentary_records"],0)
        self.assertEqual(C["proposed_new_documentary_records"],402)
        self.assertEqual(C["lilly_if_accepted"],2974)
    def test_open_review_gate(self):
        self.assertFalse(R["accepted"])
        self.assertFalse(C["independent_fidelity_review_complete"])
        self.assertTrue(C["full_chapter_l_completion_not_yet_admitted"])
        self.assertFalse(C["runtime_promotion"])
    def test_source_image_hashes(self):
        self.assertEqual(len(M["images"]),21)
        for e in M["images"]:
            f=B/e["path"]
            self.assertEqual(f.stat().st_size,e["bytes"])
            self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),e["sha256"])
    def test_all_20_original_pages_touched_by_citation(self):
        pages={p for r in R["records"] for p in r["source_locator"]["pdf_pages"]}
        self.assertEqual(pages,set(range(381,401)))
    def test_exact_start_end_and_nonpredictive_status(self):
        self.assertTrue(all(not r["prospective_blinded_prediction"] for r in R["records"]))
        self.assertTrue(all(r["source_witness_only"] for r in R["records"]))
        self.assertTrue(all(not r["case_evidence_countable"] for r in R["records"]))
        self.assertEqual(R["source_pdf_pages"],list(range(381,401)))
    def test_page381_glyph_corrected(self):
        self.assertEqual(P[2576]["source_record_kind"],"sun_as_thief_house_marker")
        self.assertEqual(P[2577]["source_record_kind"],"sun_oriental_house_east")
        self.assertIn("Sun",P[2576]["source_statement"])
        self.assertIn("Moon",P[2576]["source_statement"])
        self.assertNotIn("fortune-like",P[2576]["source_statement"].lower())
    def test_page394_two_source_corrections(self):
        self.assertEqual(P[2819]["source_record_kind"],"sun_conjunction_square_opposition_thief_known")
        self.assertIn("conjunction, square or opposition",P[2819]["source_statement"])
        self.assertEqual(P[2832]["source_record_kind"],"owner_self_second_sixth_seventh")
        self.assertIn("second, sixth or seventh",P[2832]["source_statement"])
    def test_backups_are_original_unedited_bytes(self):
        expected={
          "recovery/producer_p381_384_before_20261014_sun_review.json":"0157b9b0c1855f49cf24f462b9aac1f9e613548bb41211911e3911df350dfd5a",
          "recovery/producer_p393_395_before_20261014_p360_review.json":"176c99f0c9c36309ae6b311a4d2510c3819bd58484bf7f0e64ad895aed4b6561",
        }
        for p,h in expected.items():self.assertEqual(hashlib.sha256((B/p).read_bytes()).hexdigest(),h)
    def test_errata_is_located_not_silently_changed(self):
        x=E["candidate_in_scope"][0]
        self.assertEqual((x["printed_page"],x["original_pdf_page"]), (360,394))
        self.assertTrue(x["body_line_located"])
        self.assertFalse(x["read_word_or_glyph_verified"])
    def test_retained_uncertainty_count(self):
        self.assertEqual(U["retained_count"],len(U["issues"]))
        self.assertEqual(len({x["id"] for x in U["issues"]}),U["retained_count"])
if __name__=="__main__":unittest.main()
