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
 assert len(rows)==62
 assert [r['record_number'] for r in rows]==list(range(4385,4447))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(4385,4447)]
 assert all(r['historical_documentary_accepted'] and
  r['global_record_number']==r['record_number'] and
  not r['independent_ecclesiastical_outcome_verified'] and
  not r['empirically_validated_forecast'] and
  not r['runtime_rule_promoted'] for r in rows)
 assert all(r['chapter']=='LXXVI' for r in rows[:-2])
 assert all(r['chapter']=='LXXVII_NAVIGATION_ONLY' for r in rows[-2:])
 return True
class Documentary(unittest.TestCase):
 def test_accepted_contiguous_identity(self):self.assertTrue(valid(R))
 def test_provisional_exact_source_content_preserved(self):
  for a,b in zip(D,R,strict=True):
   for key in ('source_local_id','role','original_pdf_pages','short_original_anchor_not_diplomatic',
               'historical_author_paraphrase','original_conditions_and_uncertainty','chapter'):
    self.assertEqual(a[key],b[key])
   self.assertIsNone(a['global_record_number'])
 def test_original_reverse_mapping_one_to_one(self):
  mapped=[v for s in M['source_spans'] for v in s['accepted_global_record_ids']]
  self.assertEqual(len(mapped),62)
  self.assertEqual(sorted(mapped),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],16)
 def test_admission_hashes_frozen(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_source_audit_sha256')]:
   self.assertEqual(H(f),A[k],f)
 def test_acceptance_and_negative_outcome(self):
  self.assertEqual(A['prior_accepted_lilly'],4384)
  self.assertEqual(A['new_documentary_records'],62)
  self.assertEqual(A['lilly_if_published'],4446)
  self.assertEqual(A['combined_if_published'],5512)
  self.assertEqual(A['next_chapter'],'LXXVII')
  self.assertEqual(A['next_original_pdf_page'],468)
  self.assertEqual(len(U['issues']),20)
  self.assertEqual(A['independently_authenticated_appointment_outcomes'],0)
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertFalse(A['remote_canonical_published'])
 def test_invalid_number_rejected(self):
  rs=copy.deepcopy(R);rs[6]['record_number']=0
  with self.assertRaises(AssertionError):valid(rs)
 def test_false_success_rejected(self):
  rs=copy.deepcopy(R);rs[17]['empirically_validated_forecast']=True
  with self.assertRaises(AssertionError):valid(rs)
 def test_next_chapter_inclusion_rejected(self):
  rs=copy.deepcopy(R);rs[-1]['chapter']='LXXVI'
  with self.assertRaises(AssertionError):valid(rs)
if __name__=='__main__':unittest.main(verbosity=2)
