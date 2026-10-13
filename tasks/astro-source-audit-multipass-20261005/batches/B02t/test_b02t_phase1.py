"""Documentary and source-specific first-phase structural/regression checks."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
def rd(n):return json.loads((B/n).read_text())
D=rd("PHASE1_RULES_DRAFT.json");R=D["rules"];BY={v["record_number"]:v for v in R}
IM=rd("SOURCE_IMAGE_MANIFEST.json");REPLAY=rd("SOURCE_REPLAY_RECEIPT.json")
S=rd("SOURCE_IDENTITY.json");PRE=rd("RETAINED_LILLY_INDEX_BEFORE.json")
E=rd("ERRATA_COLLATION.json");SEC=rd("SECTION_COVERAGE.json")
CNT=rd("COUNTS.json");U=rd("UNRESOLVED.json")
def text(n):return " ".join([BY[n]["source_statement"]]+BY[n]["preconditions"]+BY[n]["exceptions_and_evidence_limits"]).lower()
def sha(x):return hashlib.sha256(x).hexdigest()
class Identity(unittest.TestCase):
 def test_exact_number_and_ids(self):
  self.assertEqual(len(R),162)
  self.assertEqual([x["record_number"] for x in R],list(range(2138,2300)))
  self.assertEqual(D["record_count"],162)
 def test_parent_index_unchanged(self):
  self.assertEqual(PRE["records_count"],2137)
  self.assertEqual(PRE["batches"][-1]["id"],"B02s")
  self.assertEqual(PRE["next"]["chapter"],"L")
  self.assertEqual(sum(x["records_count"] for x in PRE["batches"]),2137)
 def test_counts(self):
  self.assertEqual((CNT["lilly_before"],CNT["draft_source_units"],CNT["candidate_lilly_after"],
                    CNT["ptolemy_retained"],CNT["candidate_combined_after"]),(2137,162,2299,1066,3365))
  self.assertFalse(CNT["all_chapter_l_complete"])
 def test_full_volume_sha(self):
  self.assertEqual(S["original_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
  self.assertEqual(S["original_pdf_pages"],894)
 def test_full_chapter_boundaries_not_phase_boundaries(self):
  self.assertIn("PDF353",S["chapter_start"])
  self.assertIn("PDF400",S["chapter_end"])
  self.assertIn("LI",S["next_numbered_chapter"])
  self.assertFalse(D["all_chapter_L_complete"])
  self.assertFalse(SEC["full_lilly_chapter_l_complete"])
 def test_first_phase_exact_scope(self):
  self.assertEqual((SEC["start_pdf_page"],SEC["last_pdf_page"]),(353,364))
  self.assertTrue(SEC["next_phase_repeats_pdf364_from_heading"])
  self.assertEqual(len(SEC["pages"]),12)
  self.assertEqual([x["pdf_page"] for x in SEC["pages"]],list(range(353,365)))
 def test_source_page_images_hash(self):
  self.assertEqual(len(IM["images"]),19)
  for e in IM["images"]:
   p=B/e["path"]
   self.assertTrue(p.is_file(),p)
   self.assertEqual(p.stat().st_size,e["bytes"])
   self.assertEqual(sha(p.read_bytes()),e["sha256"])
 def test_original_replay(self):
  self.assertTrue(REPLAY["all_rgb_pixel_identical"])
  self.assertEqual(REPLAY["images_pixel_replayed"],19)
  self.assertTrue(all(v["pixels_identical"] for v in REPLAY["pages"]))
 def test_physical_page_link_source(self):
  for r in R:
   a=r["source_locator"]
   self.assertEqual(a["printed_pages"],[x-34 for x in a["pdf_pages"]])
   self.assertTrue(all(353<=x<=364 for x in a["pdf_pages"]))
   self.assertTrue(all((B/f).is_file() for f in a["page_images"]))
   self.assertFalse(a["source_statement_is_verbatim"])
 def test_all_records_historical_not_empirical(self):
  for r in R:
   self.assertEqual(r["runtime_status"],"REFERENCE_ONLY_NOT_PROMOTED")
   for k in ("case_evidence_countable","independently_authenticated_outcome","prospective_blind_prediction","clinical_or_criminal_inference_verified"):
    self.assertFalse(r[k])
  self.assertEqual(CNT["verified_outcomes"],0)
 def test_preconditions_and_limits_distinct(self):
  self.assertTrue(all(x["preconditions"] and x["exceptions_and_evidence_limits"] for x in R))
  self.assertTrue(all(x["source_statement_type"]=="SOURCE_IMAGE_DERIVED_PARAPHRASE_NOT_VERBATIM" for x in R))
 def test_kind_uniqueness(self):
  self.assertEqual(len(set(r["source_record_kind"] for r in R)),len(R))
 def test_errata_exact_pages_and_no_body_overwrite(self):
  self.assertEqual(E["count"],2)
  self.assertEqual([(x["printed_page"],x["replacement"]) for x in E["entries"]],[(324,"the"),(330,"or")])
  self.assertEqual([x["body_target_proved"] for x in E["entries"]],[False,True])
  self.assertTrue(E["source_body_unmodified"])
 def test_original_errata_not_treated_as_book_source_body(self):
  self.assertTrue((B/"evidence/errata-888.png").is_file())
  self.assertEqual(IM["images"][-1]["pdf_page"],888)
 def test_no_theft_section_body_admitted(self):
  self.assertIn("of a thief and theft",text(2266))
  self.assertIn("next",text(2266))
  self.assertFalse(CNT["all_chapter_l_complete"])
 def test_report_ledger_matches(self):
  raw=(B/"AUDIT_REPORT.md").read_bytes()
  l=rd("CLAIM_LEDGER.json")
  self.assertEqual(l["report_sha256"],sha(raw))
  self.assertEqual(l["unit_count"],len(l["units"]))
  self.assertEqual("\n\n".join(x["text"] for x in l["units"]),raw.decode())
  for part in l["units"]:self.assertEqual(sha(part["text"].encode()),part["sha256"])
 def test_unresolved_have_unique_ids(self):
  self.assertEqual(U["retained_count"],len(U["issues"]))
  self.assertEqual(len(set(x["id"] for x in U["issues"])),U["retained_count"])
 def test_independent_source_reviews_are_separately_gated(self):
  self.assertTrue((B/"independent_review/INPUT_A.json").is_file())
  self.assertTrue((B/"independent_review/INPUT_B.json").is_file())
  self.assertIn("REVIEW",D["status"])
class SourceReadings(unittest.TestCase):
 def test_moon_general_lost_object(self):self.assertIn("moon",text(2139))
 def test_last_separation_not_application_for_cause(self):
  self.assertIn("separat",text(2149));self.assertIn("saturn",text(2150));self.assertIn("mercury",text(2155))
 def test_beast_self_vs_taken_reverses_separation(self):
  self.assertIn("separat",text(2159))
  self.assertIn("separat",text(2160))
  self.assertNotEqual(BY[2159]["source_statement"],BY[2160]["source_statement"])
 def test_death_claim_from_eighth_aspect_only(self):
  self.assertIn("eighth",text(2163));self.assertIn("eighth",text(2164))
 def test_stolen_allegation_requires_contact(self):
  self.assertIn("thief",text(2166));self.assertIn("square",text(2167));self.assertIn("opposition",text(2167))
 def test_direction_from_moon_house(self):
  for w in ("tenth","seventh","fourth","first"):
   self.assertIn(w,text(2177))
 def test_lost_beast_not_inanimate_interchangeable(self):
  self.assertIn("beast",text(2157))
  self.assertIn("inanimate/dead things",text(2197))
 def test_animal_sizes(self):
  self.assertIn("sixth",text(2188));self.assertIn("twelfth",text(2188))
 def test_pound_means_custody(self):
  self.assertIn("pound",text(2189))
  self.assertIn("pound",text(2204))
 def test_alternative_another_judgment(self):
  self.assertIn("another judgment",text(2196))
 def test_distance_own_house_vs_far(self):
  self.assertIn("distance",text(2208))
  self.assertIn("thirty",text(2209))
 def test_water_north_vs_fire_east(self):
  self.assertIn("watery",text(2219))
  self.assertIn("fiery",text(2216))
 def test_fugitive_capture_uses_seventh(self):
  self.assertIn("fugitive",text(2233))
  self.assertIn("seventh",text(2234))
 def test_fugitive_capture_not_willing_return(self):
  self.assertIn("capture",text(2240))
  self.assertIn("return",text(2246))
 def test_seventh_hour_vs_moon_distance(self):
  self.assertIn("seventh",text(2254))
  self.assertIn("moon",text(2255))
 def test_17_5_1_distances(self):
  for n,v in ((2256,"seventeen"),(2257,"five"),(2258,"one")):
   self.assertIn(v,text(n))
 def test_woman_heading_before_theft_heading(self):
  self.assertIn("woman",text(2260))
  self.assertIn("thief",text(2266))
 def test_woman_oriental_vs_occidental(self):
  self.assertIn("occidental",text(2261))
  self.assertIn("oriental",text(2262))
 def test_hard_aspect_requires_no_reception(self):
  self.assertIn("without reception",text(2264))
class PerRecordSourceSupport(unittest.TestCase):pass
for num in range(2138,2300):
 def f(self,num=num):
  r=BY[num]
  self.assertEqual(r["record_number"],num)
  self.assertEqual(r["batch"],"B02t")
  self.assertGreaterEqual(len(r["source_statement"]),35)
  self.assertTrue(r["source_locator"]["page_images"])
  self.assertEqual(len(r["source_locator"]["pdf_pages"]),len(r["source_locator"]["page_images"]))
  self.assertFalse(r["independently_authenticated_outcome"])
 f.__name__=f"test_source_unit_R{num}"
 setattr(PerRecordSourceSupport,f.__name__,f)
if __name__=="__main__":unittest.main()
