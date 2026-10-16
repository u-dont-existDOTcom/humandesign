import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda x:json.loads((B/x).read_text())
H=lambda x:hashlib.sha256((B/x).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows'];R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json');A=J('ACCEPTANCE.json')
def verify(rs):
 assert len(rs)==48
 assert [r['record_number'] for r in rs]==list(range(5114,5162))
 assert [r['id'] for r in rs]==[f'R{i}' for i in range(5114,5162)]
 assert all(r['historical_documentary_accepted'] and not r['independently_authenticated_hope_fulfilment']
  and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rs)
 assert all(r['original_printed_chapter_numeral']=='LXXXVII' for r in rs[:-2])
 assert all(r['chapter']=='LXXXIX_NAVIGATION_ONLY' for r in rs[-2:])
class Admission(unittest.TestCase):
 def test_accepted_ids_no_empirical_credit(self):verify(R)
 def test_source_first_content_preserved(self):
  for a,r in zip(D,R,strict=True):
   for k in ('source_local_id','role','chapter','source_span_id','original_pdf_pages','historical_author_paraphrase','original_source_qualifications','original_printed_chapter_numeral'):
    self.assertEqual(a[k],r[k])
 def test_bidirectional_reverse_map(self):
  ids=[v for g in M['source_spans'] for v in g['accepted_global_record_ids']]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R))
 def test_source_hashes(self):
  for f,k in (('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),('UNRESOLVED.json','unresolved_sha256'),('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')):
   self.assertEqual(H(f),A[k])
 def test_count_and_next_label(self):
  self.assertEqual(A['prior_lilly_accepted'],5113)
  self.assertEqual(A['lilly_if_published'],5161)
  self.assertEqual(A['combined_if_published'],6227)
  self.assertEqual(A['next_original_printed_chapter'],'LXXXVIII')
  self.assertEqual(A['next_editorial_chapter'],'LXXXIX')
  self.assertEqual(A['independently_verified_hope_outcomes'],0)
 def test_false_empirical_mutant(self):
  r=copy.deepcopy(R);r[25]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):verify(r)
if __name__=='__main__':unittest.main(verbosity=2)
