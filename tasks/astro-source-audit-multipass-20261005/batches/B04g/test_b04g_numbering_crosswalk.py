import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda f:json.loads(Path(f).read_text())
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
C=J(B/'ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json')
P=J(B/'PRINTED_NUMBERING_CORRECTION_RECEIPT_20261016.json')
I=J(ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json')
def valid(c):
 assert len(c['correspondence'])==5
 assert [x['first_edition_heading'] for x in c['correspondence']]==['LXXXV','LXXXV','LXXXVI','LXXXVII','LXXXVIII']
 assert [x['original_pdf_page'] for x in c['correspondence']]==[486,489,490,491,493]
 assert [x['editorial_sequence_id'] for x in c['correspondence']]==['LXXXV','LXXXVI','LXXXVII','LXXXVIII','LXXXIX']
class Heading(unittest.TestCase):
 def test_original_1647_printed_duplicates(self):valid(C)
 def test_preserve_record_count_batches(self):
  old=J(B/'recovery/LILLY_INDEX_BEFORE_ORIGINAL_PRINTED_HEADING_CORRECTION.json')
  self.assertEqual(old['records_count'],I['records_count'])
  self.assertEqual(old['batches'],I['batches'])
  self.assertEqual(I['original_printed_chapter_heading_crosswalk']['sha256'],H(B/'ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json'))
 def test_next_heading_and_sha_receipts(self):
  self.assertEqual(I['next']['chapter'],'LXXXVII')
  self.assertEqual(I['next']['printed_chapter_numeral'],'LXXXVI')
  self.assertEqual(H(ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'),P['corrected_index_sha256'])
 def test_mutant_second_repeated_chapter_incorrect(self):
  x=copy.deepcopy(C);x['correspondence'][1]['first_edition_heading']='LXXXVI'
  with self.assertRaises(AssertionError):valid(x)
 def test_mutant_shift_next_heading(self):
  x=copy.deepcopy(C);x['correspondence'][2]['editorial_sequence_id']='LXXXVI'
  with self.assertRaises(AssertionError):valid(x)
if __name__=='__main__':unittest.main(verbosity=2)
