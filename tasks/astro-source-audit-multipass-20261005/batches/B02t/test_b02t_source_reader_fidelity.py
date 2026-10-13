"""Source image first-read findings A/B converted to targeted documentary regressions.
PASS does not certify astrology, theft, animal health, capture, or prognosis.
"""
from pathlib import Path
import json,unittest,hashlib
B=Path(__file__).resolve().parent
def rd(n):return json.loads((B/n).read_text())
D=rd("PHASE1_RULES_DRAFT.json")
R={x["record_number"]:x for x in D["rules"]}
def t(n):return " ".join([R[n]["source_statement"]]+R[n]["preconditions"]+R[n]["exceptions_and_evidence_limits"]).lower()
A=rd("SOURCE_ORDER.json")["ids"]
class ReaderFindings(unittest.TestCase):
 def test_full_first_phase_draft_never_counts_as_lilly_full_chapter(self):
  self.assertEqual(len(R),168)
  self.assertFalse(D["all_chapter_L_complete"])
  self.assertTrue(all(not x["case_evidence_countable"] for x in R.values()))
 def test_from_moon_eighth_vs_radical_eighth(self):
  for n in (2163,2164):self.assertIn("from the moon",t(n))
  self.assertIn("radical eighth",t(2165))
  self.assertIn("die very shortly",t(2164))
 def test_beast_two_lords_checked_before_still(self):
  self.assertIn("both",t(2161))
  self.assertIn("second-house lord",t(2161))
  self.assertIn("before",t(2162))
 def test_loss_last_separation_alternate_houses(self):
  for n,name in ((2151,"jupiter"),(2152,"mars"),(2153,"sun"),(2154,"venus")):
   self.assertIn("or",t(n))
   self.assertIn(name,t(n))
  self.assertIn("fast",t(2151))
 def test_moon_ruler_not_moon_small_beast(self):
  self.assertIn("moon's house lord",t(2267))
  for sign in ("aries","capricorn"):self.assertIn(sign,t(2267))
  self.assertIn("moon",t(2145))
 def test_one_sign_not_only_thirty_degrees(self):
  self.assertIn("one sign",t(2146))
  self.assertIn("house",t(2146))
 def test_moon_returners_three_qualifications(self):
  self.assertIn("contrary",t(2268))
  self.assertIn("would fain",t(2269))
  self.assertIn("will restore",t(2270))
  self.assertIn("trouble or pain",t(2175))
  self.assertIn("moon in the ascendant",t(2175))
 def test_original_house_boundary_no_thief_body(self):
  self.assertIn("of a thief and theft",t(2266))
  self.assertEqual(R[2266]["source_locator"]["pdf_pages"],[364])
  self.assertTrue(rd("SECTION_COVERAGE.json")["phase2_starts_below_of_a_thief_and_theft_heading"])
 def test_fifth_not_sixth_fortunate_cattle(self):
  self.assertIn("fifth",t(2205))
  self.assertIn("second",t(2205))
  self.assertIn("eleventh",t(2205))
  self.assertNotIn("second, sixth or eleventh",t(2205))
 def test_four_sign_glyphs_source_read(self):
  for name in ("gemini","virgo","sagittarius","pisces"):self.assertIn(name,t(2197))
 def test_capricorn_last_face_vs_last_moiety(self):
  self.assertIn("last face",t(2179))
  self.assertIn("harbour",t(2179))
  self.assertIn("last moiety",t(2192))
 def test_8th_animal_cross_page_complete(self):
  s=t(2183)
  for k in ("moon or","moon","eighth house from moon","radical eighth"):self.assertIn(k,s)
  self.assertIn("die shortly",s)
 def test_stolen_source_has_two_sections_and_negative_case(self):
  self.assertIn("not stolen",t(2272))
  self.assertIn("losing",t(2169))
  self.assertIn("thief",t(2166))
  self.assertTrue(all("stol" in t(n) for n in (2158,2272)))
 def test_moon_application_to_house_cusp_not_second_lord(self):
  self.assertIn("degree",t(2172))
  self.assertNotIn("second ruler",R[2172]["source_statement"].lower())
 def test_sixth_and_twelfth_official_custody_not_any_pound(self):
  for n in (2203,2204,2189):
   self.assertTrue(any(word in t(n) for word in ("pound","cattle","beasts","animals")))
  self.assertIn("for the most part",t(2204))
 def test_saturn_long_in_pound_and_mars_aspect_to_moon(self):
  self.assertIn("saturn",t(2226))
  self.assertIn("moon in twelfth",t(2226))
  self.assertIn("mars aspecting saturn",t(2227))
  for k in ("first","fourth","eighth","twelfth"):self.assertIn(k,t(2287))
 def test_sixth_ruler_soft_hard_alternate_lunar_targets(self):
  self.assertIn("moon",t(2289))
  self.assertIn("sextile",t(2289))
  self.assertIn("moon",t(2290))
  self.assertIn("village",t(2290))
 def test_direction_cadent_airy_not_west(self):
  self.assertIn("left",t(2218))
  self.assertIn("further",t(2291))
  self.assertIn("cadent",t(2291))
  self.assertNotIn("west",R[2291]["source_statement"].lower())
 def test_watery_angular_vs_cadent_meadow(self):
  self.assertIn("angular",t(2292))
  self.assertIn("succedent",t(2293))
  self.assertIn("cadent",t(2294))
  self.assertIn("meadows",t(2294))
 def test_earth_close_not_closer(self):
  self.assertIn("closes",t(2217))
  self.assertIn("querent",t(2217))
 def test_angul_fiery_overrides_woods(self):
  self.assertIn("but",t(2216))
  self.assertIn("angular",t(2216))
 def test_moveable_goods_not_movable_sign(self):
  self.assertIn("goods",t(2212))
  self.assertIn("fixed",t(2213))
 def test_same_quadrant_town_hundred_not_100_metric(self):
  for key in ("same quadrant","town","hundred"):self.assertIn(key,t(2286))
 def test_first_seventh_significators_fugitive_direction(self):
  self.assertIn("sun",t(2233))
  self.assertIn("querent",t(2233))
  self.assertIn("moon",t(2236))
  self.assertIn("fugitive",t(2236))
 def test_news_vs_remorse_moon_directions(self):
  self.assertIn("separating from first lord",t(2301))
  self.assertIn("seventh",t(2301))
  self.assertIn("separating from seventh lord",t(2248))
  self.assertIn("entreat",t(2248))
 def test_cross_page_infortune_not_fortune(self):
  self.assertEqual(R[2251]["source_locator"]["pdf_pages"],[363,364])
  self.assertIn("beholding an infortune",t(2251))
  self.assertIn("money",t(2251))
 def test_source_three_day_return_or_news_and_print_erratum(self):
  self.assertIn("own house",t(2253))
  self.assertIn("distance",t(2253))
  e=rd("ERRATA_COLLATION.json")
  self.assertEqual((e["entries"][1]["printed_page"],e["entries"][1]["replacement"]),(330,"or"))
  self.assertIn("erratum",t(2253))
 def test_capture_good_search_vs_detained_not_imprisoned(self):
  for x in ("good search","both","detained but not imprisoned"):self.assertIn(x,t(2242))
 def test_fugitive_good_moon_and_infortune_not_capture(self):
  self.assertIn("applying",t(2236))
  self.assertIn("return",t(2237))
  self.assertNotIn("capture",R[2237]["source_statement"].lower())
 def test_divergent_17_5_1_distance(self):
  for n,k in ((2256,"seventeen"),(2257,"five"),(2258,"one")):self.assertIn(k,t(n))
  self.assertIn("discretion",t(2256))
 def test_structural_headings_new_vs_existing(self):
  for n in (2279,2280,2281,2282,2283,2284,2285,2295,2296,2297,2298,2299):
   self.assertIn("heading",t(n))
 def test_12_original_pages_source_order_unique(self):
  self.assertEqual(len(A),len(set(A)),168)
  self.assertEqual(set(A),set(R))
  self.assertLess(A.index(2260),A.index(2266))
  self.assertLess(A.index(2162),A.index(2161))
 def test_unresolved_original_source_claims_not_validated(self):
  U=rd("UNRESOLVED.json")
  self.assertEqual(U["retained_count"],56)
  self.assertFalse(rd("COUNTS.json")["all_chapter_l_complete"])
 def test_original_reviews_frozen_and_distinct(self):
  for name,expected in (
   ("OPUS_A_INITIAL.md","e30df2b3ce3e6f1b2088919fbb04cce899f392f532fae14944f43e44d719a6fc"),
   ("OPUS_B_INITIAL.md","20de3a61ac25b299d7de909710c05b10201884497e54e260c5b80487635fa455")
  ):
   self.assertEqual(hashlib.sha256((B/"independent_review"/name).read_bytes()).hexdigest(),expected)
if __name__=="__main__":unittest.main()
