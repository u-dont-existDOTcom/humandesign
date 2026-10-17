import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==31 and len(spans)==5
 assert [r["source_local_id"] for r in rows]==[f"XCII-C{i:03}" for i in range(1,32)]
 local=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(local)==len(set(local))==31
 assert set(local)=={r["source_local_id"] for r in rows}
 byid={r["source_local_id"]:r for r in rows}
 assert all(r["source_span_id"]==s["span_id"] and r["original_pdf_pages"]==s["original_pdf_pages"]
            for s in spans for k in s["mapped_local_ids"] for r in [byid[k]])
 assert all(r["printed_pages"]==[p-34 for p in r["original_pdf_pages"]] for r in rows)
 assert all(r["chapter"]=="XCII" for r in rows[:-2])
 assert all(r["chapter"]=="XCIII_NAVIGATION_ONLY" for r in rows[-2:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"] and
   not r["independently_authenticated_captive_outcome"] and
   not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_source_mapping(self):check(D,M)
 def test_source_page_original_hashes(self):
  self.assertEqual([p["original_pdf_page"] for p in W["original_images"]],[497,498])
  for p in W["original_images"]:
   b=(B/p["path"]).read_bytes()
   self.assertEqual(len(b),p["bytes"])
   self.assertEqual(hashlib.sha256(b).hexdigest(),p["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"01ed9cf447bd250d7fc4499be68bbcc56974fdd4dd2f2cbbcd475ef6a38f0647")
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_baseline_and_printed_boundary(self):
  self.assertEqual(W["previous_accepted_lilly"],5307)
  self.assertEqual(W["editorial_chapter"],"XCII")
  self.assertEqual(W["original_printed_chapter"],"XCI")
  self.assertEqual(W["next_printed_chapter"],"XCII")
  self.assertEqual(W["next_editorial_chapter"],"XCIII")
  self.assertEqual(W["following_heading_pdf"],498)
 def test_physical_cross_page_not_doubled(self):
  self.assertEqual([s["original_pdf_pages"] for s in M if len(s["original_pdf_pages"])>1],[[497,498]])
  self.assertEqual(D[21]["role"],"source_continuation")
 def test_exact_duration_constraints_distinct(self):
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for phrase in ("within one month","forty-day","longer confinement","prolonged confinement","comparatively early release"):
   self.assertIn(phrase,t)
 def test_moon_qualified_and_harm_separate(self):
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  for phrase in ("moon-hour branch","shackling","beating","sun's beams"):
   self.assertIn(phrase,t)
 def test_no_independently_verified_people(self):
  self.assertEqual(len(U["issues"]),19)
  self.assertTrue(any("No identified prisoner" in x["issue"] for x in U["issues"]))
  self.assertTrue(all(not r["empirically_validated_prediction"] for r in D))
 def test_duplicate_span_mutant_fails(self):
  s=copy.deepcopy(M);s[0]["mapped_local_ids"].append(s[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,s)
 def test_false_historical_validation_mutant_fails(self):
  rs=copy.deepcopy(D);rs[11]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):check(rs,M)
 def test_import_next_chapter_mutant_fails(self):
  rs=copy.deepcopy(D);rs[-1]["chapter"]="XCII"
  with self.assertRaises(AssertionError):check(rs,M)
if __name__=="__main__":unittest.main(verbosity=2)
