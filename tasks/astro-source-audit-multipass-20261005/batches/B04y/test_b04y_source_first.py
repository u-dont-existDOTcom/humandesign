import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
def check(rows,spans):
 assert len(rows)==188 and len(spans)==13
 assert [r["source_local_id"] for r in rows]==[f"ACCIDENT-C{i:03}" for i in range(1,189)]
 ids=[k for s in spans for k in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==188
 assert set(ids)=={r["source_local_id"] for r in rows}
 mapping={r["source_local_id"]:r for r in rows}
 assert all(mapping[x]["source_span_id"]==s["span_id"]
   and mapping[x]["original_pdf_pages"]==s["original_pdf_pages"]
   for s in spans for x in s["mapped_local_ids"])
 assert all(r["chapter"]=="CI" for r in rows[:-3])
 assert all(r["chapter"]=="CII_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None
  and not r["historical_documentary_accepted"]
  and not r["independently_authenticated_merchant_life_event"]
  and not r["independently_validated_birth_time_rectification"]
  and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_original_page_bijection_and_chapter_scope(self):check(D,M)
 def test_original_all_14_source_image_hashes(self):
  self.assertEqual([i["original_pdf_page"] for i in W["original_images"]],list(range(541,555)))
  for image in W["original_images"]:
   data=(B/image["path"]).read_bytes()
   self.assertEqual(len(data),image["bytes"])
   self.assertEqual(hashlib.sha256(data).hexdigest(),image["sha256"])
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_previous_source_and_following_regiomontanus_heading(self):
  self.assertEqual(W["previous_accepted_lilly"],5957)
  self.assertEqual(W["next_global_record"],5958)
  self.assertEqual(W["following_heading_pdf_page"],553)
  self.assertEqual(W["following_printed_chapter"],"CI")
  self.assertEqual(W["following_editorial_chapter"],"CII")
  self.assertTrue(all(r["role"]=="next_navigation" for r in D[-3:]))
 def test_negative_method_and_accident_timing_precision(self):
  text=" ".join((r["historical_author_paraphrase"]+" "+r["original_source_qualifications"]).lower() for r in D)
  for phrase in ("no reliability","month and year","year-only","backward or forward","5 arcminutes"):
   self.assertIn(phrase,text,phrase)
 def test_minor_aspects_full_angular_inventory(self):
  text=" ".join(r["historical_author_paraphrase"] for r in D)
  for v in (30,36,45,72,108,135,144):
   self.assertIn(f"{v}°",text)
  self.assertEqual(len([r for r in D if r["role"]=="aspect_definition"]),7)
 def test_moon_angular_coordinate_misprint_preserved(self):
  self.assertEqual(61*60+44+144*60,205*60+44)
  self.assertEqual(W["source_Moon61deg44_plus144_correct"],"205deg44")
  self.assertEqual(W["source_page546_apparent_misprint"],"105deg44")
  self.assertEqual(W["source_page547_follows_correct_value"],"205deg44")
  self.assertTrue(any(r["role"]=="original_numeric_inconsistency" for r in D))
 def test_merchants_four_initial_outcomes_and_one_year_mismatch(self):
  self.assertEqual(W["retrospective_event_merchant_initial_target_ages"],[
   {"event":"master appointment","years":16,"months":7},
   {"event":"sea voyage","years":20,"months":4},
   {"event":"burning fever","years":20,"months":10},
   {"event":"later fever melancholy scurvy","years":24,"months":11}])
  self.assertEqual(W["source_mars_opposition_fit_age"],{"years":19,"months":10,"days":10})
  self.assertTrue(W["source_fever_age_mismatch_unresolved"])
  self.assertEqual(len([r for r in D if r["role"]=="historical_target"]),4)
 def test_career_ascendant_arc_arithmetic(self):
  self.assertEqual(238*60+45-(222*60+10),16*60+35)
  self.assertEqual(round(63*54/60),57)
  self.assertEqual(331*60+26+round(40*54/60),332*60+2)
  self.assertEqual(332*60+2-(312*60+10),19*60+52)
  self.assertEqual(len([r for r in D if r["role"]=="arithmetic_example"]),8)
 def test_author_admits_off_by_one_term_risk(self):
  s=" ".join((r["historical_author_paraphrase"]+" "+r["original_source_qualifications"]).lower() for r in D)
  self.assertIn("one degree",s)
  self.assertIn("twelfth degree rather than eleventh",s)
 def test_footnote_scientific_caveats(self):
  self.assertEqual(len(U["issues"]),25)
  self.assertFalse(W["in_sample_accident_fitting_only"] is False)
  self.assertFalse(W["independent_merchant_birth_certificate"])
  self.assertFalse(W["all_speculum_numeric_cells_transcribed"])
 def test_mutant_duplicate_span_rejected(self):
  m=copy.deepcopy(M);m[0]["mapped_local_ids"].append(m[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,m)
 def test_mutant_false_birth_time_accuracy_rejected(self):
  rows=copy.deepcopy(D);rows[160]["independently_validated_birth_time_rectification"]=True
  with self.assertRaises(AssertionError):check(rows,M)
 def test_mutant_next_chapter_leak_rejected(self):
  rows=copy.deepcopy(D);rows[-1]["chapter"]="CI"
  with self.assertRaises(AssertionError):check(rows,M)
if __name__=="__main__":unittest.main(verbosity=2)
