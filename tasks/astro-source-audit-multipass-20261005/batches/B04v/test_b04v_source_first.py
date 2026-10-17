import json,hashlib,copy,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text())
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=j("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=j("SOURCE_WINDOW_MANIFEST.json")
U=j("UNRESOLVED_SOURCE_LIMITS.json")
def valid(rows,spans):
 assert len(rows)==71 and len(spans)==14
 assert [r["source_local_id"] for r in rows]==[f"BOOKIII-INTRO-C{k:03}" for k in range(1,72)]
 ids=[q for x in spans for q in x["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==71
 assert set(ids)=={r["source_local_id"] for r in rows}
 by={r["source_local_id"]:r for r in rows}
 assert all(by[k]["source_span_id"]==s["span_id"] and by[k]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for k in s["mapped_local_ids"])
 assert all(r["section"]=="BOOK_III_INTRO_AND_TABLES" for r in rows[:-3])
 assert all(r["section"]=="NEXT_RECTIFICATION_CHAPTER_NAVIGATION" for r in rows[-3:])
 assert all(not r["historical_documentary_accepted"] and r["global_record_number"] is None
  and not r["independently_validated_birth_time_rectification"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] and
  not r["full_reference_tables_numeric_cells_transcribed"] for r in rows)
class Source(unittest.TestCase):
 def test_bidirectional_original_mapping(self):valid(D,M)
 def test_original_image_sha_and_all_source_pages(self):
  self.assertEqual([r["original_pdf_page"] for r in W["original_images"]],list(range(521,535)))
  for r in W["original_images"]:
   p=B/r["path"];raw=p.read_bytes()
   self.assertEqual(len(raw),r["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),r["sha256"])
  self.assertEqual(W["original_images"][0]["sha256"],"ace314d80394c1ab22b58e4525d24cf82aacbfd1b8909bdeff48afd267be1d17")
 def test_exact_book_title_numbered_pages(self):
  self.assertTrue(all(r["printed_pages"]==[None] for r in D if r["original_pdf_pages"][0] in [521,522]))
  self.assertEqual(W["next_numbered_chapter_pdf_page"],534)
  self.assertEqual(W["next_printed_chapter"],"XCVIII")
  self.assertEqual(W["prior_accepted_lilly"],5753)
  self.assertEqual(W["next_global_record"],5754)
 def test_core_time_angle_arithmetic(self):
  self.assertEqual(24*15,360)
  self.assertEqual(25*15,375)
  self.assertEqual(91*60+5+3*15*60+25*15,142*60+20)
  self.assertEqual(142*60+20+90*60,232*60+20)
 def test_original_printed_two_degree_discrepancy(self):
  e=W["source_printed_numeric_discrepancy"]
  self.assertEqual(e["printed_result"],"230 degrees 20 minutes")
  self.assertEqual(e["computed_correct_result"],"232 degrees 20 minutes")
  self.assertEqual(e["difference_arcminutes"],120)
  self.assertTrue(e["followup_page_525_uses_printed_value"])
  t=" ".join(r["historical_author_paraphrase"].lower() for r in D)
  self.assertIn("numerically false", " ".join(r["original_source_qualifications"].lower() for r in D))
  self.assertIn("230°20",t)
 def test_three_latitudes_and_all_table_pages_preserved(self):
  tables=W["source_numeric_tables"]
  self.assertEqual([t.get("latitude_degrees") for t in tables[2:]],[34,49,53])
  self.assertEqual([len(t["source_pages"]) for t in tables],[1,2,2,2,2])
  self.assertTrue(all(not t["numeric_complete"] for t in tables))
 def test_uncertainties_source_only(self):
  self.assertEqual(len(U["issues"]),24)
  self.assertFalse(W["all_numeric_cells_verified"])
  self.assertTrue(all(not r["empirically_validated_prediction"] for r in D))
 def test_blank_verso_not_invented_rules(self):
  a=[r for r in D if r["original_pdf_pages"]==[522]]
  self.assertEqual(len(a),1)
  self.assertEqual(a[0]["role"],"source_navigation")
 def test_multiple_pages_not_double_counted(self):
  self.assertEqual(len([s for s in M if len(s["original_pdf_pages"])>1]),4)
 def test_mutant_double_mapping_rejected(self):
  m=copy.deepcopy(M);m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,m)
 def test_mutant_false_predictive_validation_rejected(self):
  r=copy.deepcopy(D);r[15]["empirically_validated_prediction"]=True
  with self.assertRaises(AssertionError):valid(r,M)
 def test_mutant_next_chapter_intrusion_rejected(self):
  r=copy.deepcopy(D);r[-1]["section"]="BOOK_III_INTRO_AND_TABLES"
  with self.assertRaises(AssertionError):valid(r,M)
if __name__=="__main__":unittest.main(verbosity=2)
