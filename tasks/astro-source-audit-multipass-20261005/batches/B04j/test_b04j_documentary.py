import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
R=J("RULES.json")["rules"];A=J("ACCEPTANCE.json")
H=lambda p:hashlib.sha256((B/p).read_bytes()).hexdigest()
class OriginalSource(unittest.TestCase):
 def test_provenance_and_continuity(self):
  self.assertEqual([r["record_number"] for r in R],list(range(5194,5223)))
  self.assertEqual(len(D),29)
  self.assertTrue(all(r["chapter"]=="XC" for r in R[:-2]))
  self.assertTrue(all(r["chapter"]=="XCI_NAVIGATION_ONLY" for r in R[-2:]))
 def test_original_claims_unchanged(self):
  for d,r in zip(D,R,strict=True):
   for key in ("role","original_pdf_pages","short_original_anchor_not_diplomatic","historical_author_paraphrase","original_source_qualifications"):
    self.assertEqual(d[key],r[key])
 def test_original_witness_hashes(self):
  for x in J("SOURCE_WINDOW_MANIFEST.json")["original_images"]:
   p=B/x["path"];self.assertEqual(p.stat().st_size,x["bytes"]);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x["sha256"])
 def test_reverse_map_once(self):
  mapping=J("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json")
  ids=[q for s in mapping["source_spans"] for q in s["accepted_global_record_ids"]]
  self.assertEqual(len(ids),len(set(ids)));self.assertEqual(set(ids),{r["id"] for r in R})
 def test_enemy_identity_and_health_not_evidence(self):
  text=" ".join(r["historical_author_paraphrase"].lower() for r in R)
  for term in ("unnamed enemy","identified enemy","illness","near death","querent"):
   self.assertIn(term,text)
  self.assertTrue(all(not r["independently_verified_enemy_identity"] and not r["empirically_validated_prediction"] for r in R))
 def test_accepted_archive_fields(self):
  self.assertEqual(H("RULES.json"),A["rules_sha256"])
  self.assertEqual(H("SOURCE_ORDER.json"),A["order_sha256"])
  self.assertEqual(H("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"),A["reverse_sha256"])
  self.assertEqual(A["combined_if_published"],6288)
  self.assertEqual(A["empirical_validations"],0)
if __name__=="__main__":unittest.main(verbosity=2)
