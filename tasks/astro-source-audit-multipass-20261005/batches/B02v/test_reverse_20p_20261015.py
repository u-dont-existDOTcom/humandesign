"""Bounded original-print reverse-map coverage checks for the U74 source snapshot.

These tests intentionally do NOT certify unrecorded source clauses, a
diplomatic transcription, independent second-read or predictive efficacy.
"""
import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
def read(name):return json.loads((B/name).read_text(encoding="utf-8"))
def sha(data):return hashlib.sha256(data).hexdigest()
J=read("independent_review/REVERSE_SOURCE_COVERAGE_20P_20261015.json")
R=read("RULES_DRAFT.json")
U=read("UNRESOLVED_DRAFT.json")
class BoundedReverseMapAudit(unittest.TestCase):
 def test_20_original_pages(self):
  self.assertEqual(J["source_reverse_pages_mapped"],20)
  self.assertEqual(J["pdf_pages"],list(range(381,401)))
  self.assertEqual([x["original_pdf_page"] for x in J["page_map_manifest"]],list(range(381,401)))
 def test_all_candidate_IDs_are_mapped_but_not_accepted(self):
  self.assertEqual(J["distinct_candidate_record_ids_mapped"],402)
  self.assertEqual(J["distinct_candidate_record_ids"],list(range(2573,2975)))
  self.assertEqual(len(R["records"]),402)
  self.assertFalse(R["accepted"])
  self.assertEqual(J["newly_accepted"],0)
  self.assertEqual(J["current_accepted_Lilly"],2572)
 def test_source_map_manifest_hashes_and_ids(self):
  s={i["record_number"]:i for i in R["records"]}
  for p in J["page_map_manifest"]:
   raw=(B/p["map_file"]).read_bytes()
   self.assertEqual(sha(raw),p["map_sha256"])
   j=json.loads(raw)
   self.assertEqual(j["printed_page"],p["original_pdf_page"]-34)
   for n in p["distinct_ids"]:
    self.assertIn(n,s)
    self.assertIn(p["original_pdf_page"],s[n]["source_locator"]["pdf_pages"])
 def test_original_image_hash_provenance(self):
  m={x["pdf_page"]:x for x in read("SOURCE_IMAGE_MANIFEST.json")["images"]}
  for p in J["page_map_manifest"]:
   x=m[p["original_pdf_page"]]
   self.assertEqual(sha((B/x["path"]).read_bytes()),x["sha256"])
   self.assertEqual(x["sha256"],p["source_image_sha256"])
 def test_anchors_not_equated_with_independent_completeness(self):
  self.assertEqual(J["normalized_anchor_count"],419)
  self.assertEqual(J["record_page_appearances"],413)
  self.assertEqual(len(J["repeated_cross_page_record_ids"]),11)
  self.assertFalse(J["original_to_record_exhaustiveness_proved"])
  self.assertFalse(J["independent_diplomatic_text_completeness"])
  self.assertFalse(J["chapter_L_documentary_source_accepted"])
 def test_zero_empirical_case_promotion(self):
  self.assertEqual(U["retained_count"],74)
  self.assertEqual(J["logged_source_issues"],74)
  for r in R["records"]:
   self.assertFalse(r["case_evidence_countable"])
   self.assertFalse(r["prospective_blinded_prediction"])
   self.assertEqual(r["runtime_status"],"REFERENCE_ONLY_NOT_PROMOTED")
if __name__=="__main__":unittest.main()
