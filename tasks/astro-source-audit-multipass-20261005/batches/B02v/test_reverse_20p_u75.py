"""Original-image source-first coverage proof for current *provisional* U75 draft.

All 402 existing candidate record IDs have normalized source anchors. This
does not prove that original text has no unrecorded clauses or that the
author's historical claims predict real events.
"""
from pathlib import Path
import json,hashlib,unittest
B=Path(__file__).resolve().parent
def j(f):return json.loads((B/f).read_text())
def h(f):return hashlib.sha256((B/f).read_bytes()).hexdigest()
S=j("independent_review/REVERSE_SOURCE_COVERAGE_20P_U75_20261015.json")
R=j("RULES_DRAFT.json")
I=j("SOURCE_IMAGE_MANIFEST.json")
class BoundedU75(unittest.TestCase):
 def test_window_and_records(self):
  self.assertEqual([x["original_pdf_page"] for x in S["page_map_manifest"]],list(range(381,401)))
  self.assertEqual(S["distinct_candidate_record_ids"],list(range(2573,2975)))
  self.assertEqual(len(R["records"]),402)
 def test_source_image_hashes_and_exact_mapping(self):
  rec={x["record_number"]:x for x in R["records"]}
  images={x["pdf_page"]:x for x in I["images"]}
  for page in S["page_map_manifest"]:
   p=page["original_pdf_page"]
   self.assertEqual(h(page["map_file"]),page["map_sha256"])
   self.assertEqual(h(images[p]["path"]),images[p]["sha256"])
   for num in page["distinct_ids"]:
    self.assertIn(p,rec[num]["source_locator"]["pdf_pages"])
 def test_additional_original_branch_accounted_for(self):
  p=next(x for x in S["page_map_manifest"] if x["original_pdf_page"]==391)
  self.assertTrue(p["map_file"].endswith("P391_U75_20261015.json"))
  self.assertEqual(p["normalized_anchor_count"],20)
  self.assertEqual(len([x for x in j(p["map_file"])["source_to_record"] if x["record_number"]==2769]),2)
 def test_metadata_and_no_scientific_promotion(self):
  self.assertEqual(S["normalized_anchor_count"],420)
  self.assertEqual(S["record_page_appearances"],413)
  self.assertEqual(len(S["repeated_cross_page_record_ids"]),11)
  self.assertFalse(S["original_to_record_exhaustiveness_proved"])
  self.assertFalse(S["independent_diplomatic_text_completeness"])
  self.assertFalse(S["chapter_L_documentary_source_accepted"])
  self.assertEqual(S["current_source_draft_sha256"],h("RULES_DRAFT.json"))
  self.assertEqual(S["logged_source_issues"],75)
  self.assertEqual(S["newly_accepted"],0)
 def test_all_proposed_record_kinds_are_reference_only(self):
  for r in R["records"]:
   self.assertFalse(r["case_evidence_countable"])
   self.assertFalse(r["prospective_blinded_prediction"])
   self.assertEqual(r["runtime_status"],"REFERENCE_ONLY_NOT_PROMOTED")
 def test_source_unresolved_glyph_explicit(self):
  self.assertFalse(j("ERRATA_COLLATION.json")["candidate_in_scope"][0]["read_word_or_glyph_verified"])
if __name__=="__main__":unittest.main()
