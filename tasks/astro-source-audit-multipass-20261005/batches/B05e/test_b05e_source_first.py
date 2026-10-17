import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"];W=J("SOURCE_WINDOW_MANIFEST.json")
def valid(rows,groups):
 assert len(rows)==59 and len(groups)==9
 assert [r["source_local_id"] for r in rows]==[f"TEMPER-C{i:03}" for i in range(1,60)]
 ids=[z for s in groups for z in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==59
 assert set(ids)=={r["source_local_id"] for r in rows}
 lookup={r["source_local_id"]:r for r in rows}
 assert all(lookup[z]["source_span_id"]==s["span_id"] and set(lookup[z]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"])) for s in groups for z in s["mapped_local_ids"])
 assert all(r["chapter"]=="CVII" for r in rows[:-3])
 assert all(r["chapter"]=="CVIII_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"] and not r["independently_validated_temperament_or_health"] and not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_exact_source_group_bijection(self):valid(D,M)
 def test_all_original_scanned_page_hashes(self):
  self.assertEqual([w["original_pdf_page"] for w in W["original_images"]],[566,567,568,569])
  for w in W["original_images"]:
   p=B/w["path"];raw=p.read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),w["sha256"])
   self.assertEqual(len(raw),w["bytes"])
 def test_precise_chapter_seams_and_baseline(self):
  self.assertEqual(W["previous_accepted_lilly"],6415)
  self.assertEqual(W["next_global_record"],6416)
  self.assertEqual(W["following_heading_pdf"],568)
  self.assertEqual([r["original_pdf_pages"] for r in D[-3:]],[[568],[568],[569]])
  self.assertEqual(W["next_printed_chapter"],"CVII")
 def test_four_humour_source_classes(self):
  d=[r for r in D if r["role"]=="humour_class"]
  self.assertEqual(len(d),4)
  self.assertEqual(W["four_humours_source_labels"],["sanguine","phlegmatic","choleric","melancholic"])
 def test_full_planet_phase_and_lunar_quality_set(self):
  self.assertEqual(len([r for r in D if r["role"]=="planet_quality"]),10)
  self.assertEqual(len([r for r in D if r["role"]=="lunar_phase"]),4)
  self.assertEqual(len([r for r in D if r["role"]=="solar_season"]),4)
  self.assertEqual(len([r for r in D if r["role"]=="sign_triplicity"]),4)
 def test_all_significator_categories_and_malefic_override(self):
  self.assertEqual(len([r for r in D if r["role"]=="testimony_input"]),8)
  self.assertTrue(any(r["role"]=="conditional_exception" for r in D))
  self.assertTrue(any("other testimonies agree" in r["historical_author_paraphrase"] for r in D))
 def test_conditional_weighting_and_opposed_cancellation(self):
  self.assertTrue(W["testimony_counts_cancel_opposed_equal"])
  self.assertTrue(W["lord_geniture_and_ascendant_planet_threefold"])
  self.assertTrue(W["moon_in_ascendant_twofold"])
  self.assertEqual(len([r for r in D if r["role"]=="tie_rule"]),3)
  self.assertEqual(len([r for r in D if r["role"]=="weight_rule"]),2)
 def test_uncertainty_and_no_biomedical_promotion(self):
  self.assertEqual(len(J("UNRESOLVED_SOURCE_LIMITS.json")["issues"]),23)
  self.assertFalse(W["actual_human_humoral_biomedical_validation"])
  self.assertTrue(all(not r["empirically_validated_prediction"] for r in D))
 def test_duplicate_source_mutant(self):
  groups=copy.deepcopy(M);groups[0]["mapped_local_ids"].append(groups[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):valid(D,groups)
 def test_false_human_validation_mutant(self):
  rows=copy.deepcopy(D);rows[20]["independently_validated_temperament_or_health"]=True
  with self.assertRaises(AssertionError):valid(rows,M)
 def test_next_manners_chapter_merge_mutant(self):
  rows=copy.deepcopy(D);rows[-1]["chapter"]="CVII"
  with self.assertRaises(AssertionError):valid(rows,M)
if __name__=="__main__":unittest.main(verbosity=2)
