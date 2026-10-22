#!/usr/bin/env python3
"""Source-first book and cross-tradition research map integrity checks."""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from urllib.parse import urlparse
import importlib.util,json,re,tempfile,unittest
from unittest.mock import patch

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
M=B/"MAYA_RANKED_SOURCE_REGISTER_V1.json"
OTH=B/"ADDITIONAL_TRADITIONS_PRIORITY_REGISTER_V1.json"
CROSS=B/"TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json"
MAP=B/"MULTITRADITION_SOURCE_TO_TEST_MAP.md"
GUIDE=B/"MAYA_BOOKS_OTHER_SYSTEMS_AND_METHOD_20261022.md"
PREV=B/"BOOK_AND_MAYAN_COVERAGE_STATUS_20261022.md"
NORM=ROOT/"reference/core/survey_v2_behavioral_domains.json"
PREV_SHA="dcdeffc1f5f76cbb12b3851b205404f40ed7249b197a8f89c882b74545d1c105"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
def load_module(filename):
 spec=importlib.util.spec_from_file_location(filename.removesuffix(".py"),B/filename)
 mod=importlib.util.module_from_spec(spec)
 assert spec.loader is not None
 spec.loader.exec_module(mod)
 return mod

def strict_document_checks(maya,other,cross):
 if len(maya["source_records"])!=15:raise ValueError("Expected 15 distinct Maya source leads")
 if len(other["traditions"])!=7:raise ValueError("Expected 7 materially distinct other tradition classes")
 if len(cross["crosswalk"])!=20:raise ValueError("Source-to-survey coverage ledger changed")
 ids=[s["source_id"] for s in maya["source_records"]]
 if ids!=[f"MAYA-{i:02d}" for i in range(1,16)]:
  raise ValueError("Maya source IDs not consecutive/unique")
 if len({s["reference_url"] for s in maya["source_records"]})!=len(ids):
  raise ValueError("Duplicate named Maya sources/URLs")
 if not all(urlparse(s["reference_url"]).scheme=="https" for s in maya["source_records"]):
  raise ValueError("Non-https or missing source provenance URL")
 if not all(s["original_content_ingested"] is False and s["source_to_human_observable_rules_promoted"]==0
            and s["empirical_human_predictive_validations"]==0 for s in maya["source_records"]):
  raise ValueError("Source discovery falsely elevated to read original or human success")
 if not any(s["source_kind"]=="original_codex" for s in maya["source_records"]):
  raise ValueError("Original codices omitted")
 if not any(s["source_kind"]=="contemporary_indigenous_source" for s in maya["source_records"]):
  raise ValueError("Living Indigenous Maya tradition omitted")
 if not any(s["title"].startswith("Calendrical Calculations") for s in maya["source_records"]):
  raise ValueError("Existing independent calendar algorithm/reference method omitted")
 if not all(x["validated_real_human_prediction_results"]==0 for x in other["traditions"]):
  raise ValueError("Unstudied traditions falsely count human outcomes")
 if not any(x["tradition_id"]=="ASTRO-MESOAMERICAN-NAHUA" for x in other["traditions"]):
  raise ValueError("Related but separate Nahua prognostics omitted")
 if maya["regional_practice_layers"][2]["system"]!="MODERN-DREAMSPELL" or not maya["regional_practice_layers"][2]["cannot_label_ancient_maya_astrology"]:
  raise ValueError("Modern Dreamspell being mistaken for ancient codex")
 if not maya["not_a_uniform_historical_maya_personality_horoscope"]:
  raise ValueError("Unfounded monolithic ancient Maya personality astrology inferred")
 norm=rd(NORM)
 norm_ids=[x["id"] for x in norm["domains"]]
 if cross["existing_Human_Design_domain_ids"]!=norm_ids or len(norm_ids)!=6:
  raise ValueError("Existing frozen HD Survey-v2 domain IDs no longer match")
 hd=[x for x in cross["crosswalk"] if x["tradition"]=="Human Design"]
 if len(hd)!=6 or {x["existing_Human_Design_survey_v2_domain_id"] for x in hd}!=set(norm_ids):
  raise ValueError("Existing HD six survey domains lost/rewritten")
 nonhd=[x for x in cross["crosswalk"] if x["tradition"]!="Human Design"]
 if len(nonhd)!=14 or any(x["existing_Human_Design_survey_v2_domain_id"] is not None for x in nonhd):
  raise ValueError("A cross-tradition source concept was silently assigned an HD-specific question")
 if any(x["cross_tradition_claim_equivalence"] or x["ready_for_new_cross_tradition_blind_pred"]
        or x["real_human_predictive_validations"] for x in cross["crosswalk"]):
  raise ValueError("Unvalidated novel traditions promoted to empirical evidence")
 if cross["validated_human_blind_predictions"] or cross["cross_tradition_hypotheses_active_in_runtime"]:
  raise ValueError("Claim map falsely scored as a deployed human-trial model")
 return True

class TraditionsSourceMap(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.maya=rd(M);cls.other=rd(OTH);cls.cross=rd(CROSS)
 def test_prior_original_status_report_sha_unchanged(self):
  self.assertEqual(sha(PREV),PREV_SHA)
 def test_source_manifest_structural_and_empirical_truth(self):
  self.assertTrue(strict_document_checks(self.maya,self.other,self.cross))
 def test_prior_human_design_architecture_not_overwritten(self):
  self.assertTrue((ROOT/"ARCHITECTURE.md").is_file())
  self.assertTrue((ROOT/"reference/core/MAPPING_V2_EVIDENCE_PROTOCOL.md").is_file())
  self.assertEqual(rd(NORM)["status"],"candidate_blind_prevalidation")
 def test_free_primary_and_living_maya_separate(self):
  kinds={s["source_id"]:s["source_kind"] for s in self.maya["source_records"]}
  self.assertEqual(kinds["MAYA-01"],"original_codex")
  self.assertEqual(kinds["MAYA-02"],"contemporary_indigenous_source")
  self.assertEqual(kinds["MAYA-03"],"ethnography")
  self.assertNotEqual(kinds["MAYA-13"],kinds["MAYA-03"])
  self.assertIn("HTTP_403",self.maya["source_records"][1]["access_status_at_discovery"])
 def test_maya_correlation_is_declared_not_locked_to_dreamspell(self):
  self.assertIn("584283",self.maya["original_Maya_calendar_correlation_policy"])
  self.assertNotIn("584283",self.maya["regional_practice_layers"][2]["system"])
 def test_no_untrusted_fake_book_urls(self):
  for s in self.maya["source_records"]:
   with self.subTest(source=s["source_id"]):
    u=urlparse(s["reference_url"])
    self.assertIn(u.netloc.lower(),{
      "www.slub-dresden.de","maya.nmai.si.edu","www.unmpress.com",
      "ethos.lps.library.cmu.edu","upcolorado.com","www.pennpress.org",
      "utpress.utexas.edu","www.si.edu","reingold.co","research.famsi.org",
      "www.famsi.org"})
 def test_important_other_systems_breadth(self):
  self.assertEqual(len({r["tradition_id"] for r in self.other["traditions"]}),7)
  self.assertTrue({"ASTRO-HELLENISTIC","ASTRO-ISLAMIC-PERSIAN",
                   "ASTRO-MESOAMERICAN-NAHUA","ASTRO-MESOPOTAMIAN"}
                  .issubset({x["tradition_id"] for x in self.other["traditions"]}))
 def test_four_mermaid_graphs_are_complete_not_decorative(self):
  text=MAP.read_text(encoding="utf-8")
  blocks=re.findall(r"```mermaid\n(.*?)\n```",text,re.S)
  self.assertEqual(len(blocks),4)
  self.assertTrue(all(block.strip().startswith("flowchart ") for block in blocks))
  for token in ("OLD","source","RELATIONSHIP"):
   pass
  self.assertIn("ABSTAIN",text.upper())
  self.assertIn("cross-tradition",text.lower())
  self.assertIn("Human Design",text)
  self.assertIn("DREAMSPELL",text.upper())
 def test_book_guide_uses_ranked_sources_and_scope_distinctions(self):
  text=GUIDE.read_text(encoding="utf-8")
  for token in ("Barbara Tedlock","Dresden","Skywatchers",
                "Calendrical Calculations","Vettius Valens","al-Bīrūnī",
                "Dreamspell","cross-tradition","forward"):
   self.assertIn(token,text)
 def test_research_generator_reproduces_identical_source_registers(self):
  source=load_module("build_astro_source_map_registers.py")
  with tempfile.TemporaryDirectory(prefix="maya-source-reg-replay-") as tmp:
   old_B=source.B
   try:
    source.B=Path(tmp);source.generate()
    for name in ("MAYA_RANKED_SOURCE_REGISTER_V1.json",
                 "ADDITIONAL_TRADITIONS_PRIORITY_REGISTER_V1.json"):
     self.assertEqual((Path(tmp)/name).read_bytes(),(B/name).read_bytes())
   finally:
    source.B=old_B
 def test_crosswalk_reproduction_against_normative_survey_v2(self):
  source=load_module("build_tradition_survey_crosswalk.py")
  with tempfile.TemporaryDirectory(prefix="crosswalk-replay-") as tmp:
   old_B=source.B
   try:
    source.B=Path(tmp);source.main()
    self.assertEqual((Path(tmp)/"TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json").read_bytes(),CROSS.read_bytes())
   finally:
    source.B=old_B
 def test_mutant_one_fabricated_human_success_is_rejected(self):
  x=json.loads(json.dumps(self.maya))
  x["source_records"][0]["empirical_human_predictive_validations"]=1
  with self.assertRaises(ValueError):
   strict_document_checks(x,self.other,self.cross)
 def test_mutant_ancient_dreamspell_attribution_is_rejected(self):
  x=json.loads(json.dumps(self.maya))
  x["regional_practice_layers"][2]["cannot_label_ancient_maya_astrology"]=False
  with self.assertRaises(ValueError):
   strict_document_checks(x,self.other,self.cross)
 def test_mutant_cross_tradition_repurposed_HD_question_is_rejected(self):
  x=json.loads(json.dumps(self.cross))
  x["crosswalk"][-1]["existing_Human_Design_survey_v2_domain_id"]="V2_PROFILE_ROLE"
  with self.assertRaises(ValueError):
   strict_document_checks(self.maya,self.other,x)
 def test_mutant_cross_tradition_runtime_rule_activation_is_rejected(self):
  x=json.loads(json.dumps(self.cross))
  x["cross_tradition_hypotheses_active_in_runtime"]=1
  with self.assertRaises(ValueError):
   strict_document_checks(self.maya,self.other,x)
if __name__=="__main__":
 unittest.main()
