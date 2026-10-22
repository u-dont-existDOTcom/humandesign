#!/usr/bin/env python3
"""Maya owner-local intake controls, copyright-safe and source-status explicit."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,unittest
from build_maya_source_inventory import SOURCES,SOURCE_WINDOWS,sha,epub_scan

B=Path(__file__).resolve().parent
DATA=B/"MAYA_LOCAL_SOURCE_INVENTORY_V1.json"
EXPECTED_INTAKE_SHA="2a4af2c69ba6c19935984c8a725bf3b23af5efa81ab803a1aaaaa8c80a13c089"
BOOKS=Path.home()/"Documents/astrology"

class OwnerBookIntake(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads(DATA.read_text(encoding="utf-8"))
  cls.records=cls.data["input_sources"]
  cls.index={row["id"]:row for row in cls.records}
 def test_source_inventory_bitwise_SHA(self):
  self.assertEqual(sha(DATA),EXPECTED_INTAKE_SHA)
 def test_declared_document_class_count(self):
  self.assertEqual((self.data["total_input_files"],self.data["research_sources_usable_for_next_reading"],self.data["fiction_omitted_from_original_sources"]),(5,4,1))
  self.assertEqual(len(self.records),5)
  self.assertEqual(len({x["id"] for x in self.records}),5)
 def test_each_owner_source_exact_binary_fingerprint(self):
  for code,token,title,authors,edition,role,limitation,want_sha,page_num in SOURCES:
   with self.subTest(code=code):
    p=BOOKS/self.index[code]["owner_document_basename"]
    self.assertTrue(p.is_file(),p.name)
    self.assertEqual(sha(p),want_sha)
    self.assertEqual(p.stat().st_size,self.index[code]["source_bytes"])
 def test_book_metadata_types_correct(self):
  for code in ("MAYA-AVENI-VAIL-MADRID","MAYA-AVENI-SKYWATCHERS","MAYA-REINGOLD-DERSHOWITZ-CALENDRICAL"):
   x=self.index[code]
   self.assertEqual(x["input_file_type"],".pdf")
   self.assertGreater(x["PDF_pages"],400)
  self.assertEqual(self.index["MAYA-TEDLOCK-HIGHLAND-DAYKEEPERS"]["input_file_type"],".epub")
 def test_Tedlock_actual_content_survives_bad_metadata(self):
  x=self.index["MAYA-TEDLOCK-HIGHLAND-DAYKEEPERS"]["epub_structure"]
  self.assertTrue(x["test_metadata_anomaly"])
  self.assertGreaterEqual(x["epub_xml_page_files"],250)
  self.assertTrue(x["actual_chapter_content_checked"])
 def test_doomsday_match_is_a_novel_not_Dresden_manuscript(self):
  x=self.index["EXCLUDE-WHEELER-FICTION"]
  self.assertEqual(x["intake_role"],"FICTION_NOT_THE_DRESDEN_CODEX")
  self.assertFalse(x["include_in_scholarly_original_source_counts"])
  self.assertIn("Jeff Wheeler",x["authors_or_editors"])
 def test_no_historical_or_human_predictive_rules_have_been_admitted(self):
  self.assertEqual(self.data["books_fully_read_or_complete"],0)
  self.assertEqual(self.data["published_original_Maya_predicate_rules"],0)
  self.assertEqual((self.data["real_human_blinded_predictive_validations"],self.data["runtime_astrology_rule_promotions"]),(0,0))
  self.assertTrue(all(not x["has_been_read_in_full"] for x in self.records))
 def test_regional_sources_distinct(self):
  roles={x["intake_role"] for x in self.records}
  self.assertEqual(len(roles),5)
  self.assertIn("living_Maya_daykeeper_260_day_ethnography",roles)
  self.assertIn("source_critical_Codex_Madrid_interpretation",roles)
  self.assertIn("formal_calendar_conversion_algorithms",roles)
 def test_page_windows_original_PDF_boundaries(self):
  for x in self.records:
   pages=x.get("PDF_pages")
   if pages is None:continue
   for w in x["source_provenance_next_reading_windows"]:
    self.assertTrue(1<=w["pdf_index_start"]<=pages,x["id"])
 def test_six_original_nonoverlapping_source_classes_and_policy(self):
  self.assertNotEqual(self.data["source_regions_not_interchangeable"][0],self.data["source_regions_not_interchangeable"][1])
  self.assertIn("584283",self.data["correlation_policy"])
  self.assertIn("584285",self.data["correlation_policy"])
  self.assertFalse(self.data["Maya_date_conversion_algorithm_verified_against_independent_oracle"])
  self.assertFalse(self.data["Maya_regional_daykeeper_meaning_collated"])
 def test_prohibit_copyrighted_original_bytes_in_inventory(self):
  serialized=DATA.read_text(encoding="utf-8")
  self.assertLess(DATA.stat().st_size,21000)
  self.assertFalse(self.data["copyright_originals_in_Git_or_archive"])
  self.assertNotIn("<onlyinclude>",serialized)
 def test_readonly_generator_rejects_existing_output(self):
  import tempfile,subprocess,sys
  result=subprocess.run([sys.executable,str(B/"build_maya_source_inventory.py"),"--out",str(DATA)],capture_output=True,text=True)
  self.assertNotEqual(result.returncode,0)
  self.assertIn("Source inventory exists",result.stderr)

if __name__=="__main__":
 unittest.main()
