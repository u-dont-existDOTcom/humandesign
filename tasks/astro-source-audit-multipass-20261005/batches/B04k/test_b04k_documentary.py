import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];R=J("RULES.json")["rules"];A=J("ACCEPTANCE.json")
class HistoricalSource(unittest.TestCase):
 def test_contiguous_ids_and_no_empirical_claims(self):
  self.assertEqual([r["record_number"] for r in R],list(range(5223,5308)))
  self.assertTrue(all(not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in R))
 def test_original_clauses_preserved(self):
  for d,r in zip(D,R,strict=True):
   for k in ("chapter","role","original_pdf_pages","historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[k],r[k])
 def test_passage_map_once(self):
  x=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  mapped=[q for s in x["source_spans"] for q in s["accepted_global_record_ids"]]
  self.assertEqual(len(mapped),len(set(mapped)))
  self.assertEqual(set(mapped),{r["id"] for r in R})
 def test_source_image_sha256(self):
  for w in J("SOURCE_WINDOW_MANIFEST.json")["original_images"]:
   p=B/w["path"];self.assertEqual(p.stat().st_size,w["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),w["sha256"])
 def test_limits_and_harm_unverified(self):
  self.assertEqual(len(J("UNRESOLVED_SOURCE_LIMITS.json")["issues"]),22)
  self.assertEqual(A["independent_prisoner_outcomes"],0)
  self.assertEqual(A["independent_deaths"],0)
  self.assertEqual(A["combined_if_published"],6373)
 def test_outcomes_distinct(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in R)
  for token in ["short detention","longer confinement","re-imprisonment","escape","death","misery","release"]:
   self.assertIn(token,text)
 def test_hashes(self):
  for f,key in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
  ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
  ("UNRESOLVED_SOURCE_LIMITS.json","issues_sha256")]:self.assertEqual(H(f),A[key])
 def test_following_heading_separate(self):
  self.assertTrue(all(r["chapter"]=="XCI" for r in R[:-2]))
  self.assertTrue(all(r["chapter"]=="XCII_NAVIGATION_ONLY" for r in R[-2:]))
  self.assertEqual(A["next_original_pdf_page"],497)
if __name__=="__main__":unittest.main(verbosity=2)
