import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
def valid(rows):
 assert len(rows)==34
 assert [r['record_number'] for r in rows]==list(range(4137,4171))
 assert [r['id'] for r in rows]==[f'R{n}' for n in range(4137,4171)]
 assert all(r['global_record_number']==r['record_number'] and
  r['historical_documentary_admitted'] and not r['independent_payment_outcome_verified']
  and not r['empirically_validated_prediction'] and not r['runtime_rule_promoted'] for r in rows)
 assert all(r['chapter']=='LXXIII' for r in rows[:-2])
 assert all(r['chapter']=='LXXIV_NAVIGATION_ONLY' for r in rows[-2:])
class Acceptance(unittest.TestCase):
 def test_contiguous_ids(self):valid(R)
 def test_exact_draft_content(self):
  for a,b in zip(D,R,strict=True):
   for k in ('source_local_id','role','chapter','original_pdf_pages',
    'historical_author_paraphrase','original_scope_uncertainty'):
    self.assertEqual(a[k],b[k])
   self.assertIsNone(a['global_record_number'])
 def test_reverse_map_unique(self):
  refs=[k for s in M['source_spans'] for k in s['canonical_record_ids']]
  self.assertEqual(len(refs),34)
  self.assertEqual(sorted(refs),sorted(x['id'] for x in R))
  self.assertEqual(M['span_count'],10)
 def test_exact_hashes(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_review_sha256')]:
   self.assertEqual(H(f),A[k])
 def test_evidentiary_separation(self):
  self.assertEqual(A['prior_accepted_lilly'],4136)
  self.assertEqual(A['new_documentary_records'],34)
  self.assertEqual(A['lilly_if_published'],4170)
  self.assertEqual(A['combined_if_published'],5236)
  self.assertEqual(A['independently_verified_dowry_receipts'],0)
  self.assertEqual(A['new_empirical_predictions'],0)
  self.assertFalse(A['remotely_published'])
  self.assertEqual(len(U['issues']),17)
 def test_corrupted_id_rejected(self):
  bad=copy.deepcopy(R);bad[0]['record_number']=200
  with self.assertRaises(AssertionError):valid(bad)
 def test_false_prognosis_rejected(self):
  bad=copy.deepcopy(R);bad[4]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):valid(bad)
 def test_next_section_leak_rejected(self):
  bad=copy.deepcopy(R);bad[-2]['chapter']='LXXIII'
  with self.assertRaises(AssertionError):valid(bad)
if __name__=='__main__':unittest.main(verbosity=2)
