import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda f:json.loads(Path(f).read_text())
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
C=J(B/'ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json')
P=J(B/'PRINTED_NUMBERING_CORRECTION_RECEIPT_20261016.json')
PATH=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
I=J(PATH)
def valid(c):
 assert len(c['correspondence'])==5
 assert [x['first_edition_heading'] for x in c['correspondence']]==['LXXXV','LXXXV','LXXXVI','LXXXVII','LXXXVIII']
 assert [x['original_pdf_page'] for x in c['correspondence']]==[486,489,490,491,493]
 assert [x['editorial_sequence_id'] for x in c['correspondence']]==['LXXXV','LXXXVI','LXXXVII','LXXXVIII','LXXXIX']
class Heading(unittest.TestCase):
 def test_original_1647_printed_duplicates(self):valid(C)
 def test_preserve_original_record_counts_and_prior_batches(self):
  before=J(B/'recovery/LILLY_INDEX_BEFORE_ORIGINAL_PRINTED_HEADING_CORRECTION.json')
  self.assertEqual(before['records_count'],5080)
  snap=B/'recovery/LILLY_INDEX_AFTER_CROSSWALK_BEFORE_B04g_CANONICAL.json'
  if snap.exists():
   halfway=J(snap)
   self.assertEqual(halfway['records_count'],5080)
   self.assertEqual(halfway['batches'],before['batches'])
   self.assertEqual(I['batches'][:-1],halfway['batches'])
   self.assertEqual(I['records_count'],5113)
  else:
   self.assertEqual(I['records_count'],5080)
   self.assertEqual(I['batches'],before['batches'])
  self.assertEqual(I['original_printed_chapter_heading_crosswalk']['sha256'],H(B/'ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json'))
 def test_source_crosswalk_hash_at_correct_phase(self):
  snap=B/'recovery/LILLY_INDEX_AFTER_CROSSWALK_BEFORE_B04g_CANONICAL.json'
  self.assertEqual(H(snap if snap.exists() else PATH),P['corrected_index_sha256'])
  self.assertEqual((J(snap) if snap.exists() else I)['next']['printed_chapter_numeral'],'LXXXVI')
  self.assertEqual(I['next']['printed_chapter_numeral'],'LXXXVII' if snap.exists() else 'LXXXVI')
 def test_mutant_duplicate_heading_rejected(self):
  x=copy.deepcopy(C);x['correspondence'][1]['first_edition_heading']='LXXXVI'
  with self.assertRaises(AssertionError):valid(x)
 def test_mutant_shift_next_heading_rejected(self):
  x=copy.deepcopy(C);x['correspondence'][2]['editorial_sequence_id']='LXXXVI'
  with self.assertRaises(AssertionError):valid(x)
if __name__=='__main__':unittest.main(verbosity=2)
