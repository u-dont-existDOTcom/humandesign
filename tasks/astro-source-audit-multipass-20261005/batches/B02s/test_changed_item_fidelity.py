"""Regression evidence from two original-page changed-item reviews.
These checks guard SOURCE TRANSCRIPTION, not astrology or ethical assertions.
"""
import json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
D=json.loads((B/"RULES.json").read_text())
R={r["record_number"]:r for r in D["rules"]}
def t(n):return " ".join([R[n]["source_statement"]]+R[n]["preconditions"]+R[n]["exceptions_and_evidence_limits"]).lower()
class LastSourceCorrections(unittest.TestCase):
 def test_moon_afliction_not_deleted_by_neighbor_repair(self):
  x=t(2010)
  for s in ("moon","fall","square","opposition","saturn","mars","retrograde","ascendant"):
   self.assertIn(s,x)
 def test_genders_attributed_to_right_questioner(self):
  x=t(1992)
  for s in ("man","woman","moon","sun","venus","saturn","jupiter"):
   self.assertIn(s,x)
  self.assertIn("painstaking",x)
 def test_venus_and_moon_strong_motion(self):
  x=t(1931)
  self.assertIn("moon likewise strong",x)
  self.assertIn("increasing",x)
  self.assertIn("dignit",x)
 def test_receiver_heavy_not_only_afflicted(self):
  self.assertIn("heavy or ponderous",t(2021))
  self.assertIn("square or opposition",t(2021))
 def test_mastery_two_branches(self):
  x=t(2007)
  for s in ("seventh lord","angular","strive","neither"):
   self.assertIn(s,x)
 def test_source_negates_other_mans_coercive_success(self):
  self.assertIn("cannot bring her under his yoak",t(2064))
  self.assertIn("no",t(2064))
 def test_node_head_means_deluded_not_self_blame(self):
  x=t(2120)
  for s in ("head","deluded","deceived","tail","still guilty","mars"):
   self.assertIn(s,x)
 def test_fixed_angles_tempted_now(self):
  x=t(2119)
  for s in ("angles","fixed","movable","common","still tempted"):
   self.assertIn(s,x)
 def test_mars_is_7th_lord(self):
  for n in (2067,2126):
   self.assertIn("mars is",t(n))
   self.assertIn("seventh",t(n))
 def test_seventh_in_seventh_own_domicile_intensifier(self):
  self.assertIn("especially",t(1952))
  self.assertIn("in the seventh",t(1952))
 def test_moon_in_seventh_completion_alternative(self):
  self.assertIn("moon in seventh",t(1945))
 def test_no_other_lover_head_node_branch(self):
  self.assertIn("dragon",t(2075))
  self.assertIn("void of course",t(2075))
 def test_rumor_denial_and_no_credit(self):
  self.assertIn("false",t(2047))
  self.assertIn("gave no credit",t(2047))
 def test_before_she_knew_husband(self):
  self.assertIn("predating",t(2066))
  self.assertIn("husband",t(2066))
 def test_one_degree_house_scope(self):
  self.assertIn("one degree",t(2065))
  self.assertIn("house",t(2065))
 def test_either_both_in_nonconsensual_source(self):
  self.assertIn("or she was unwillingly drawn",t(2122))
  self.assertIn("violence",t(2122))
 def test_print_says_relate_to_eleventh_not_question_about_it(self):
  self.assertIn("relation to the eleventh house",t(2136))
  self.assertIn("question",t(2136))
 def test_mistress_sweetheart_own_source_record(self):
  self.assertEqual(D["record_count"],217)
  self.assertEqual(R[2137]["source_locator"]["pdf_pages"],[352])
  self.assertIn("mistress or sweetheart",t(2137))
  self.assertTrue(R[2137]["source_review_inserted"])
 def test_new_record_follows_p318_heading(self):
  order=json.loads((B/"RULES_SOURCE_ORDER.json").read_text())["ids"]
  self.assertEqual(len(order),217)
  self.assertEqual(order[order.index(2095)+1],2137)
 def test_must_not_call_source_records_empirical_predictions(self):
  self.assertTrue(all(not r["independently_verified_outcome"] and not r["case_evidence_countable"] and not r["prospective_frozen_forecast"] for r in R.values()))
if __name__=="__main__":unittest.main()
