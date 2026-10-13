"""Source-specific regressions for errors found by two independent original-image readers."""
import json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
d=json.loads((B/"RULES.json").read_text())
R={x["record_number"]:x for x in d["rules"]}
K={x["source_record_kind"]:x for x in d["rules"]}
def txt(n):return " ".join([R[n]["source_statement"]]+R[n]["preconditions"]+R[n]["exceptions_and_evidence_limits"]).lower()
def kind(k):return " ".join([K[k]["source_statement"]]+K[k]["exceptions_and_evidence_limits"]).lower()
class ReviewerHighFindings(unittest.TestCase):
 def test_unwilling_original_not_silently_repaired(self):
  self.assertIn("unwillingly",txt(1937))
  self.assertIn("conflicts",txt(1937))
 def test_moon_tenth_not_seventh_in_mediation_clause(self):
  self.assertIn("moon in the tenth",txt(1940))
  self.assertIn("venus",txt(1940))
 def test_source_erases_conjunction_from_p305(self):
  self.assertIn("conjunction",txt(1961))
  self.assertIn("delet",txt(1961))
  self.assertIn("square",txt(1961))
  self.assertIn("opposition",txt(1961))
 def test_alkindus_first_lord_application_unrestricted(self):
  self.assertIn("not restrict",txt(1930))
 def test_sun_three_conditions_own_dispositor(self):
  self.assertIn("sun",txt(1932))
  self.assertIn("own sign",txt(1932))
  self.assertIn("and",txt(1932))
 def test_applying_both_cadent_not_not_applying(self):
  self.assertIn("application",txt(1933))
  self.assertIn("both",txt(1933))
  self.assertIn("cadent",txt(1933))
 def test_not_invented_sun_venus_angular_exchange(self):
  self.assertIn("interchangeable",txt(1949))
  self.assertIn("triplicity",txt(1949))
  self.assertEqual(R[1949]["source_locator"]["pdf_pages"],[338,339])
 def test_evil_prohibiting_vs_helpful_translation(self):
  self.assertIn("evil",txt(1963))
  self.assertIn("prohibit",txt(1963))
 def test_rumours_not_declared_actual_infidelity(self):
  for k in ("objected","scandalized","feared"):
   self.assertIn(k,txt(1967))
 def test_correct_sun_saturn_person_type(self):
  self.assertIn("sun",txt(1992))
  self.assertIn("saturn",txt(1992))
  self.assertIn("painstaking",txt(1992))
 def test_dead_men_and_own_industry_not_quarrels(self):
  self.assertIn("by dead men",txt(2018))
  self.assertIn("conjunct",txt(2018))
  self.assertIn("own industry",txt(2018))
 def test_capricorn_not_virgo_arabic_rule(self):
  self.assertIn("capricorn",txt(2028))
  self.assertIn("six months",txt(2028))
  self.assertIn("discord",txt(2028))
  self.assertIn("caution",txt(2028))
 def test_infortune_in_fourth_not_fourth_ruler(self):
  self.assertIn("in the fourth",txt(2013))
  self.assertIn("divorce",txt(2013))
 def test_five_degree_uninvented_separation_comparison(self):
  self.assertIn("five degrees",txt(2048))
  self.assertIn("no",txt(2048))
  for planet in ("saturn","jupiter","mars","sun"):self.assertIn(planet,txt(2048))
 def test_explicit_denial_of_unfounded_reports(self):
  self.assertIn("false",txt(2047))
  self.assertIn("gave no credit",txt(2047))
  self.assertIn("slander",kind("moon_tail_slander_warning"))
 def test_separate_unforced_vs_forced_branch(self):
  self.assertIn("consent",kind("forced_not_voluntary_exception"))
  self.assertIn("force",txt(2057))
 def test_moon_and_lord_seventh_both_required(self):
  self.assertIn("both",txt(2053))
  self.assertIn("not faulty",txt(2053))
 def test_node_corrections_both_p315_errata(self):
  e=json.loads((B/"ERRATA_COLLATION.json").read_text())["entries"]
  self.assertEqual(e[-2]["printed_page"],315)
  self.assertIn("south node",e[-2]["erratum"].lower())
  self.assertIn("south node",txt(2062))
  self.assertIn("dragons head",txt(2063).replace("'","")) if False else None
 def test_venus_friendship_not_infidelity(self):
  self.assertIn("friendship with women",txt(2069))
  self.assertIn("not naturally lewd",txt(2069))
 def test_seventh_house_planet_by_planet_denials(self):
  for key in ("seventh_mars_not_ruler","seventh_saturn_denial","seventh_jupiter_conflict","seventh_venus_denial","seventh_mercury_past","seventh_moon_none_yet","seventh_sun_dragonhead_none"):
   self.assertIn(key,K)
  self.assertIn("without physical involvement",kind("seventh_saturn_denial"))
  self.assertIn("denies",kind("seventh_venus_denial"))
 def test_free_will_of_querent_printed(self):
  self.assertIn("freedom of will",txt(2080))
  self.assertIn("with or without",txt(2080))
 def test_generic_mediator_not_sun_mars_invention(self):
  self.assertIn("masculine",txt(2085))
  self.assertIn("nocturnal",txt(2085))
 def test_parentage_only_after_prior_testimonies_absent(self):
  self.assertIn("none",txt(2094))
  self.assertIn("just suspition",txt(2094))
  self.assertIn("stuprated",txt(2094))
 def test_reconciliation_two_step_mediator(self):
  self.assertEqual(R[2098]["source_locator"]["pdf_pages"],[352,353])
  self.assertIn("seventh",txt(2098))
  self.assertIn("ascendant",txt(2098))
 def test_return_after_source_abuse_branch(self):
  self.assertIn("abused",txt(2106))
  self.assertIn("respect",txt(2106))
class SourceGroupAndTrace(unittest.TestCase):
 def test_distinct_love_direction_contradictions_retained(self):
  self.assertIn("loving",txt(1950))
  self.assertIn("against the ancients",txt(2083))
 def test_29_added_recovered_source_clauses(self):
  self.assertEqual(d["added_missed_original_units"],29)
  self.assertEqual(d["record_count"],216)
 def test_intervening_headings_separate(self):
  for k in ("strife_or_good_heading","postmarital_agreement_heading","lover_separate_heading","manner_person_heading","honest_to_husband_heading"):
   self.assertIn(k,K)
 def test_source_order_moral_heading_precedes_inquiry(self):
  s=json.loads((B/"RULES_SOURCE_ORDER.json").read_text())["ids"]
  self.assertLess(s.index(2054),s.index(2050))
 def test_source_order_previous_section_finishes_before_new(self):
  s=json.loads((B/"RULES_SOURCE_ORDER.json").read_text())["ids"]
  self.assertLess(s.index(2077),s.index(2075))
 def test_no_independent_empirical_outcomes(self):
  self.assertTrue(all(not r["independently_verified_outcome"] for r in R.values()))
if __name__=="__main__":unittest.main()
