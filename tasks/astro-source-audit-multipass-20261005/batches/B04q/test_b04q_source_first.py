import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=j("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=j("SOURCE_WINDOW_MANIFEST.json")
def valid(rows,spans):
 assert len(rows)==34 and len(spans)==7
 assert [r["source_local_id"] for r in rows]==[f"XCVII-C{k:03}" for k in range(1,35)]
 ids=[x for s in spans for x in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==34
 assert set(ids)=={r["source_local_id"] for r in rows}
 assert all(r["chapter"]=="XCVII" for r in rows[:-4])
 assert all(r["chapter"]=="POST_XCVI_NAVIGATION_ONLY" for r in rows[-4:])
 assert all(not r["empirically_validated_prediction"] and not r["independently_verified_prior_garrison_capture"] for r in rows)
class Source(unittest.TestCase):
 def test_mapping(self):valid(D,M)
 def test_witness(self):
  for x in W["original_images"]:
   raw=(B/x["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
   self.assertEqual(len(raw),x["bytes"])
 def test_source_history(self):
  self.assertEqual(W["previous_accepted_lilly"],5552)
  self.assertEqual(W["original_numbered_body_pages"],[505,506])
  self.assertEqual(W["following_unnumbered_page"],507)
 def test_outcomes_distinct(self):
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for q in ("past and future","within three days","day before the question","money","garrison"):self.assertIn(q,t)
 def test_next_unumbered(self):
  self.assertEqual(len([r for r in D if r["role"]=="next_navigation"]),4)
  self.assertTrue(W["unnumbered_source_study_remains_open"])
 def test_duplicate_mutant(self):
  m=copy.deepcopy(M);m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,m)
 def test_false_validation_mutant(self):
  r=copy.deepcopy(D);r[12]["independently_verified_prior_garrison_capture"]=True
  with self.assertRaises(AssertionError):valid(r,M)
if __name__=="__main__":unittest.main(verbosity=2)
