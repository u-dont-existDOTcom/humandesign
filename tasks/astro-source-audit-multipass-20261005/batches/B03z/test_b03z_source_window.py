import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
M=json.loads((B/'SOURCE_WINDOW_PROVISIONAL_20261016.json').read_text())
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
class Window(unittest.TestCase):
 def test_all_four_witness_image_hashes(self):
  self.assertEqual([f['original_pdf_page'] for f in M['original_page_images']],[473,474,475,476])
  for it in M['original_page_images']:
   p=B/it['path'];self.assertEqual(p.stat().st_size,it['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),it['sha256'])
 def test_current_authenticated_chapter_and_next(self):
  self.assertEqual(I['records_count'],4549)
  self.assertEqual(I['batches'][-1]['id'],'B03y')
  self.assertEqual(I['next']['chapter'],'LXXX')
  self.assertEqual(I['next']['pdf_page'],473)
 def test_original_eyes_on_boundary(self):
  self.assertEqual(M['source_body_pdf_pages'],[473,474,475,476])
  self.assertEqual(M['following_chapter'],'LXXXI')
  self.assertEqual(M['following_divider_pdf_page'],476)
  self.assertIn('1646/7',M['opening_figure_date_printed'])
 def test_provisional_not_admitted_and_not_empirical(self):
  self.assertEqual(M['first_unassigned_next_record_number'],4550)
  self.assertEqual(M['new_accepted_documentary_records'],0)
  self.assertEqual(M['new_empirical_validations'],0)
  self.assertEqual(M['runtime_promotions'],0)
  self.assertFalse(M['original_diplomatic_transcription_complete'])
if __name__=='__main__':unittest.main(verbosity=2)
