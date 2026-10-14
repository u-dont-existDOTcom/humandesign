"""B02v staging regressions; they do NOT constitute acceptance of historical rules."""
import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
def rd(n):return json.loads((B/n).read_text())
I=rd("RETAINED_LILLY_INDEX_BEFORE.json")
M=rd("SOURCE_IMAGE_MANIFEST.json")
R=rd("SOURCE_REPLAY_RECEIPT.json")
S=rd("SOURCE_IDENTITY.json")
C=rd("COUNTS.json")
F=rd("SECTION_COVERAGE.json")
E=rd("ERRATA_COLLATION.json")
def h(x):return hashlib.sha256(x).hexdigest()
class SourceWitnessProvenance(unittest.TestCase):
    def test_previous_index_unmodified(self):
        self.assertEqual(I["records_count"],2572)
        self.assertEqual(I["batches"][-1]["id"],"B02u")
        self.assertEqual(I["next"]["chapter"],"L")
        self.assertEqual(I["next"]["pdf_page"],381)
    def test_exact_volume_digest_declared(self):
        self.assertEqual(S["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
        self.assertEqual(S["original_pdf_bytes"],141842963)
        self.assertEqual(M["original_pdf_sha256"],S["original_full_pdf_sha256"])
        self.assertEqual(R["original_pdf_sha256"],S["original_full_pdf_sha256"])
    def test_twenty_pages_and_errata_all_present(self):
        self.assertEqual(len(M["images"]),21)
        self.assertEqual([x["pdf_page"] for x in M["images"] if x["pdf_page"]!=888],list(range(381,401)))
        self.assertTrue(all((B/x["path"]).is_file() for x in M["images"]))
    def test_source_image_hashes_and_byte_sizes(self):
        for x in M["images"]:
            p=B/x["path"];self.assertEqual(p.stat().st_size,x["bytes"]);self.assertEqual(h(p.read_bytes()),x["sha256"])
    def test_render_independent_pixels_verified(self):
        self.assertTrue(R["all_source_image_renders_replayed_rgb_identical"])
        self.assertEqual(len(R["images"]),21)
        self.assertTrue(all(x["rgb_pixel_identical"] for x in R["images"]))
    def test_prior_acceptance_start_boundary(self):
        self.assertIn("house of the Thiefe",S["admitted_start"])
        self.assertIn("PDF381",F["first_page_boundary"])
    def test_next_chapter_stop_boundary(self):
        self.assertIn("Chapter LI",S["admitted_end"])
        self.assertIn("PDF400",F["last_page_boundary"])
    def test_source_body_not_declared_prediction(self):
        self.assertFalse(S["empirical_predictive_validation"])
        self.assertEqual(S["new_records_accepted"],0)
        self.assertFalse(C["runtime_promotion"])
        self.assertTrue(C["full_chapter_l_completion_not_yet_admitted"])
    def test_pending_record_identity(self):
        self.assertEqual(C["accepted_new_documentary_records"],0)
        self.assertEqual((C["accepted_lilly_before"],C["retained_ptolemy"],C["accepted_lilly_before"]+C["retained_ptolemy"]),(2572,1066,3638))
    def test_stage_five_windows_all_pages_covered(self):
        self.assertEqual(F["five_reader_windows"],{"A":[381,385],"B":[385,389],"C":[389,393],"D":[393,397],"E":[397,400]})
        self.assertEqual(F["overlap_pages"],[385,389,393,397])
    def test_errata_is_printed_page_not_pdf_page(self):
        self.assertEqual(E["candidate_in_scope"][0]["printed_page"],360)
        self.assertEqual(E["candidate_in_scope"][0]["original_pdf_page"],394)
        self.assertTrue(E["candidate_in_scope"][0]["body_line_located"])
        self.assertFalse(E["candidate_in_scope"][0]["read_word_or_glyph_verified"])
    def test_other_errata_pages_excluded(self):
        self.assertEqual([x["original_pdf_page"] for x in E["other_provider_alto_errata_entries_after_this_range"]],[419,426,431])
    def test_no_extra_image_for_numbered_chapter_51(self):
        self.assertEqual(M["images"][-2]["pdf_page"],400)
        self.assertEqual(M["images"][-1]["pdf_page"],888)
class IndependentWindowEvidence(unittest.TestCase):pass
for w,first,last in [("A",381,385),("B",385,389),("C",389,393),("D",393,397),("E",397,400)]:
    def check(self,w=w,first=first,last=last):
        manifest=rd(f"SOURCE_READER_INPUT_{w}.json")
        self.assertEqual(manifest["source_window"],[first,last])
        self.assertEqual(manifest["review_kind"],"FIRST_INDEPENDENT_SOURCE_IMAGE_FIRST_DRAFT")
        pgs={x["path"] for x in manifest["files"] if x["path"].endswith(".png")}
        self.assertEqual(pgs,{f"source_images/pdf-{p}.png" for p in range(first,last+1)}|{"source_images/errata-888.png"})
        self.assertEqual(len(pgs),last-first+2)
    check.__name__=f"test_window_{w.lower()}_images_and_scope"
    setattr(IndependentWindowEvidence,check.__name__,check)
if __name__=="__main__":unittest.main()
