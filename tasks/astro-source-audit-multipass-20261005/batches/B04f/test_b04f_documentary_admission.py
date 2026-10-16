import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows'];R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json');A=J('ACCEPTANCE.json')
def check(rows):
 assert len(rows)==54
 assert [r['record_number'] for r in rows]==list(range(5027,5081))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(5027,5081)]
 assert all(r['historical_documentary_accepted'] and not r['independently_authenticated_royal_military_outcome']
 and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXXVI' for r in rows[:-2])
 assert all(r['chapter']=='LXXXVII_NAVIGATION_ONLY' for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_contiguous_ids_and_no_empirical_promotion(self):check(R)
 def test_preservation_of_draft_claims(self):
  for before,after in zip(D,R,strict=True):
   for key in ('source_local_id','source_span_id','role','chapter','original_pdf_pages',
               'historical_author_paraphrase','original_source_qualifications'):
    self.assertEqual(before[key],after[key])
 def test_reverse_coverage(self):
  ids=[x for g in M['source_spans'] for x in g['accepted_global_record_ids']]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],10)
 def test_source_hashes(self):
  for f,k in (('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
              ('UNRESOLVED.json','unresolved_sha256'),
              ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
              ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')):
   self.assertEqual(H(f),A[k])
 def test_counts_and_source_dates(self):
  self.assertEqual(A['prior_lilly_accepted'],5026)
  self.assertEqual(A['new_documentary_records'],54)
  self.assertEqual(A['lilly_if_published'],5080)
  self.assertEqual(A['combined_if_published'],6146)
  self.assertTrue(A['figure_absolute_date_unresolved'])
  self.assertTrue(A['Queen_army_destroyed_claim_unverified_partial_miss'])
  self.assertEqual(A['new_empirically_validated_predictions'],0)
 def test_false_validation_mutant(self):
  changed=copy.deepcopy(R);changed[15]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(changed)
if __name__=='__main__':unittest.main(verbosity=2)
