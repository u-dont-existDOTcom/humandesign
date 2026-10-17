import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
read=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=read("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=read("RULES.json")["rules"];A=read("ACCEPTANCE.json")
class Provenance(unittest.TestCase):
 def test_ids_and_protection(self):
  self.assertEqual([r["record_number"] for r in R],list(range(5162,5194)))
  self.assertTrue(all(not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in R))
 def test_exact_source_reproduction(self):
  for d,r in zip(D,R,strict=True):
   for k in ["role","chapter","original_pdf_pages","historical_author_paraphrase","original_source_qualifications"]:
    self.assertEqual(d[k],r[k])
 def test_reverse_all_passages(self):
  m=read("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  allids=[n for s in m["source_spans"] for n in s["accepted_global_record_ids"]]
  self.assertEqual(len(set(allids)),32)
  self.assertEqual(sorted(allids),sorted(r["id"] for r in R))
 def test_original_image_hashes(self):
  for item in read("SOURCE_WINDOW_MANIFEST.json")["original_images"]:
   p=B/item["path"];self.assertEqual(p.stat().st_size,item["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),item["sha256"])
 def test_acceptance_hashes(self):
  for n,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256")]:
   self.assertEqual(H(n),A[k])
 def test_next_chapter_printed_vs_editorial(self):
  self.assertEqual(R[-1]["chapter"],"XC_NAVIGATION_ONLY")
  self.assertEqual(A["next_chapter"],"XC")
  self.assertEqual(A["next_printed_chapter"],"LXXXIX")
  self.assertEqual(A["combined_if_published"],6259)
 def test_outcome_categories_separate(self):
  t=" ".join(r["historical_author_paraphrase"].lower() for r in R)
  for x in ["mutual respect","secretly desired","mutual love","no love","twelfth"]:
   self.assertIn(x,t)
if __name__=="__main__":unittest.main(verbosity=2)
