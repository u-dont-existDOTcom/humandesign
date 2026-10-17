import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
m=json.loads((B/"SOURCE_WINDOW_PROVISIONAL_20261017.json").read_text())
class Window(unittest.TestCase):
 def test_original_witness_hashes(self):
  self.assertEqual([r["original_pdf_page"] for r in m["original_images"]],[504,505])
  for r in m["original_images"]:
   p=B/r["path"]
   self.assertEqual(p.stat().st_size,r["bytes"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r["sha256"])
 def test_verified_parent_count_not_modified(self):
  root=B.parents[3]
  p=root/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
  I=json.loads(p.read_text())
  self.assertEqual(I["records_count"],5510)
  self.assertEqual(I["batches"][-1]["id"],"B04o")
  self.assertEqual(I["next"]["chapter"],"XCVI")
  self.assertEqual(m["next_global_record_number"],5511)
  self.assertEqual(m["new_accepted_documentary_records"],0)
 def test_original_page_divider_separation(self):
  self.assertEqual(m["original_body_pdf_pages"],[504,505])
  self.assertEqual(m["following_heading_pdf"],505)
  self.assertEqual(m["following_heading_printed"],"XCVI")
  self.assertEqual(m["following_heading_editorial"],"XCVII")
  self.assertTrue(m["next_chapter_has_distinct_horary_figure"])
 def test_direction_vs_letter_vs_recapture(self):
  self.assertEqual(m["source_forecast_direction"],"Eastwards")
  self.assertTrue(m["author_reported_direction_confirmation"])
  self.assertTrue(m["author_reported_news_friday"])
  self.assertTrue(m["author_reported_recapture_sunday"])
  self.assertEqual(m["independent_actual_arrest_records_authenticated"],0)
 def test_historical_not_empirical(self):
  self.assertEqual(m["new_empirical_validations"],0)
  self.assertEqual(m["runtime_promotions"],0)
  self.assertFalse(m["original_diplomatic_second_transcription_complete"])
if __name__=="__main__":unittest.main(verbosity=2)
