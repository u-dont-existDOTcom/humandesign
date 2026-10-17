import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3] if len(B.parents)>3 else None
J=lambda p:json.loads(Path(p).read_text())
W=J(B/"SOURCE_WINDOW_PROVISIONAL_20261017.json")
class SourceBoundary(unittest.TestCase):
 def test_all_14_consecutive_first_edition_images(self):
  self.assertEqual([s["original_pdf_page"] for s in W["original_images"]],list(range(541,555)))
  for s in W["original_images"]:
   p=B/s["path"];raw=p.read_bytes()
   self.assertEqual(len(raw),s["bytes"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),s["sha256"])
 def test_previous_canonical_index_stays_immutable(self):
  I=J(B/"PARENT_INDEX_BEFORE_B04y.json")
  raw=(B/"PARENT_INDEX_BEFORE_B04y.json").read_bytes()
  self.assertEqual(hashlib.sha256(raw).hexdigest(),"5c8ae2ec443d6c2f0a4d360de66a7631ee09412ee41c318e56c75d7ff4666fd1")
  if ROOT is not None:
   live=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
   if live.is_file():self.assertEqual(live.read_bytes(),raw)
  self.assertEqual(I["records_count"],5957)
  self.assertEqual(I["batches"][-1]["id"],"B04x")
  self.assertEqual(I["next"]["chapter"],"CI")
  self.assertEqual(I["next"]["pdf_page"],541)
  self.assertEqual(W["next_global_record_number"],5958)
 def test_shared_page_distinct_chapters(self):
  self.assertEqual(W["source_body_page_start"],541)
  self.assertEqual(W["source_body_page_end"],553)
  self.assertTrue(W["source_body_ends_before_next_heading"])
  self.assertEqual(W["following_heading_starts_on_shared_pdf_page"],553)
  self.assertEqual(W["following_printed_chapter"],"CI")
 def test_source_table_position_and_event_fitting(self):
  self.assertEqual(W["source_speculum_table_page"],543)
  self.assertIn("5 arcminutes per month",W["source_direction_period_rule"])
  self.assertTrue(W["original_author_prior_event_target_fitting"])
  self.assertFalse(W["blind_out_of_sample_prediction_not_established"] is False)
 def test_no_premature_documentary_or_empirical_admission(self):
  self.assertEqual(W["new_documentary_records_accepted"],0)
  self.assertEqual(W["new_empirical_validations"],0)
  self.assertEqual(W["runtime_model_promotions"],0)
  self.assertFalse(W["all_table_cell_transcription_complete"])
if __name__=="__main__":unittest.main(verbosity=2)
