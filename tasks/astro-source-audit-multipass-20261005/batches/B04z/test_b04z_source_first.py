import copy,hashlib,json,unittest,math
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
N=J("SOURCE_NUMERIC_ARITHMETIC_AUDIT_20261017.json")
def check(rows,spans):
 assert len(rows)==70 and len(spans)==6
 assert [r["source_local_id"] for r in rows]==[f"REGIOMONTANUS-C{k:03}" for k in range(1,71)]
 ids=[id for s in spans for id in s["mapped_local_ids"]]
 assert len(ids)==len(set(ids))==70
 assert set(ids)=={r["source_local_id"] for r in rows}
 byid={r["source_local_id"]:r for r in rows}
 assert all(byid[x]["source_span_id"]==s["span_id"] and byid[x]["original_pdf_pages"]==s["original_pdf_pages"] for s in spans for x in s["mapped_local_ids"])
 assert all(r["chapter"]=="CII" for r in rows[:-3])
 assert all(r["chapter"]=="CIII_NAVIGATION_ONLY" for r in rows[-3:])
 assert all(r["global_record_number"] is None and not r["historical_documentary_accepted"] and
  not r["full_source_numeric_tables_independently_parity_checked"] and
  not r["independently_verified_natal_birth_instant"] and
  not r["empirically_validated_prediction"] and not r["runtime_model_promoted"] for r in rows)
class Source(unittest.TestCase):
 def test_original_source_bijection(self):check(D,M)
 def test_original_six_page_image_hashes(self):
  self.assertEqual([x["original_pdf_page"] for x in W["original_images"]],list(range(553,559)))
  for x in W["original_images"]:
   p=B/x["path"];raw=p.read_bytes()
   self.assertEqual(len(raw),x["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
  self.assertEqual(W["original_full_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_correct_prior_and_new_chapter(self):
  self.assertEqual(W["previous_accepted_lilly"],6145)
  self.assertEqual(W["first_global_record"],6146)
  self.assertEqual(W["following_heading_pdf"],558)
  self.assertEqual(W["next_printed_chapter"],"CII")
  self.assertEqual(W["next_editorial_chapter"],"CIII")
 def test_original_natal_clock_not_independently_verified(self):
  self.assertEqual(W["original_birth_time"],"19 September 1616 14:24:25 historical local time")
  self.assertTrue(W["source_uses_30_seconds_in_one_time_conversion"])
  self.assertFalse(W["independent_known_birth_instant"])
  self.assertEqual(len(U["issues"]),24)
 def test_solar_ra_time_angle_exact_arithmetic(self):
  self.assertAlmostEqual(N["solar_ra_bracket"]["ra_increment_arcminutes"],55*37/60)
  sun_arcsec=(185*60+30)*60+55*37
  time_arcsec=(2*3600+24*60+25)*15
  sum_arcsec=sun_arcsec+time_arcsec
  self.assertEqual(sum_arcsec,((222*60+10)*60+10))
  self.assertEqual(N["midheaven"]["difference_arcseconds"],10)
  self.assertEqual(N["time_angle"]["computed_exact"],"36°06′15″")
  self.assertEqual(N["time_angle"]["source_used"],"36°07′")
 def test_pole_values_and_six_cusps(self):
  self.assertEqual([x["source_oa"] for x in N["other_cusps"]],
   ["252°10′","282°10′","312°10′","342°10′","12°10′"])
  self.assertEqual([x["pole_latitude_deg"] for x in N["other_cusps"]],[34,49,53,49,34])
  self.assertEqual(N["midheaven"]["printed_ecliptic_cusp"],"Scorpio 14°39′")
  self.assertEqual((342+30)%360,12)
 def test_two_local_interpolation_discrepancies(self):
  twelfth=N["other_cusps"][1];first=N["other_cusps"][2]
  self.assertAlmostEqual(twelfth["computed_zodiac_arcminutes"],61*60/76)
  self.assertEqual(twelfth["source_result_zodiac_arcminutes"],49)
  self.assertAlmostEqual(first["computed_zodiac_arcminutes"],39*60/59)
  self.assertEqual(first["source_result_zodiac_arcminutes"],37)
  self.assertTrue(39*60/59-37>2.5)
 def test_locality_reference_time_rounding(self):
  self.assertEqual(N["ephemeris_motion_time"]["computed_sum"],"3:31:25")
  self.assertEqual(N["ephemeris_motion_time"]["source_rounded_used"],"3:31")
 def test_illustrative_source_not_empirical(self):
  self.assertFalse(N["all_ephemeris_chart_parity_complete"])
  self.assertFalse(N["independently_authenticated_merchant_birth_time"])
  self.assertFalse(N["empirical_predictive_validation"])
 def test_wrong_second_chapter_merged_rejected(self):
  r=copy.deepcopy(D);r[-1]["chapter"]="CII"
  with self.assertRaises(AssertionError):check(r,M)
 def test_duplicate_source_record_rejected(self):
  s=copy.deepcopy(M);s[0]["mapped_local_ids"].append(s[1]["mapped_local_ids"][0])
  with self.assertRaises(AssertionError):check(D,s)
 def test_false_birth_certificate_rejected(self):
  r=copy.deepcopy(D);r[28]["independently_verified_natal_birth_instant"]=True
  with self.assertRaises(AssertionError):check(r,M)
if __name__=="__main__":unittest.main(verbosity=2)
