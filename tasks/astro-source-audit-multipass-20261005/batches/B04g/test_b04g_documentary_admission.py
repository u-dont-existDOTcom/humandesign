import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
def check(rows):
 assert len(rows)==33
 assert [r['record_number'] for r in rows]==list(range(5081,5114))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(5081,5114)]
 assert all(r['historical_documentary_accepted'] and not r['independently_authenticated_preferment_outcome'] and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXXVII' and r['original_printed_chapter_numeral']=='LXXXVI' for r in rows[:-2])
 assert all(r['chapter']=='LXXXVIII_NAVIGATION_ONLY' and r['original_printed_chapter_numeral']=='LXXXVII' for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_ids_and_original_numeral_preserved(self):check(R)
 def test_content_identity(self):
  for d,r in zip(D,R,strict=True):
   for key in ('source_local_id','source_span_id','role','chapter','original_printed_chapter_numeral','original_pdf_pages','historical_author_paraphrase','original_source_qualifications'):
    self.assertEqual(d[key],r[key])
 def test_reverse_map_bijection(self):
  items=[x for s in M['source_spans'] for x in s['accepted_global_record_ids']]
  self.assertEqual(len(items),len(set(items)))
  self.assertEqual(sorted(items),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],6)
 def test_source_hash_receipts(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),('UNRESOLVED.json','unresolved_sha256'),('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')]:
   self.assertEqual(H(f),A[k])
 def test_canary_counts(self):
  self.assertEqual(A['prior_lilly_accepted'],5080)
  self.assertEqual(A['lilly_if_published'],5113)
  self.assertEqual(A['combined_if_published'],6179)
  self.assertEqual(A['next_editorial_chapter'],'LXXXVIII')
  self.assertEqual(A['next_original_printed_chapter'],'LXXXVII')
  self.assertEqual(A['independently_verified_office_outcomes'],0)
  self.assertFalse(A['remote_canonical_published'])
 def test_fake_hit_mutant_rejected(self):
  rows=copy.deepcopy(R);rows[7]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(rows)
if __name__=='__main__':unittest.main(verbosity=2)
