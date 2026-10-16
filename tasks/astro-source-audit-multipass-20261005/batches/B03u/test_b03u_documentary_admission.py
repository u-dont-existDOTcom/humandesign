import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED.json')
def check(rs):
 assert len(rs)==61
 assert [r['record_number'] for r in rs]==list(range(4324,4385))
 assert [r['id'] for r in rs]==[f'R{n}' for n in range(4324,4385)]
 assert all(r['global_record_number']==r['record_number']
   and r['historical_documentary_accepted']
   and not r['individual_case_independently_verified']
   and not r['empirical_forecast_validated']
   and not r['runtime_model_promoted'] for r in rs)
 assert all(r['chapter']=='LXXV' for r in rs[:-2])
 assert all(r['chapter']=='LXXVI_NAVIGATION_ONLY' for r in rs[-2:])
 assert all(r['printed_page_numerals_as_physically_imprinted']==
   [{463:429,464:431,465:430,466:432}[n] for n in r['original_pdf_pages']] for r in rs)
class Admission(unittest.TestCase):
 def test_ids_and_historical_only(self):check(R)
 def test_original_authorial_claims_survive(self):
  for draft,final in zip(D,R,strict=True):
   for key in ('source_local_id','role','chapter','original_pdf_pages',
               'printed_page_numerals_as_physically_imprinted',
               'historical_author_paraphrase','source_conditions_uncertainty'):
    self.assertEqual(draft[key],final[key])
   self.assertIsNone(draft['global_record_number'])
   self.assertFalse(draft['historical_documentary_accepted'])
 def test_reverse_source_unique(self):
  refs=[r for s in M['source_spans'] for r in s['accepted_global_record_ids']]
  self.assertEqual(len(refs),61)
  self.assertEqual(sorted(refs),sorted(x['id'] for x in R))
  self.assertEqual(M['span_count'],16)
 def test_hash_receipts_from_accepted_bytes(self):
  for f,k in [('RULES.json','rules_sha256'),
   ('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_original_source_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','original_visual_review_sha256')]:
   self.assertEqual(H(f),A[k])
 def test_original_scan_ids_not_printed_numeric_order(self):
  self.assertEqual(A['original_pdf_text_order'],[463,464,465,466])
  self.assertEqual(A['original_imprinted_folio_numbers'],[429,431,430,432])
  self.assertTrue(A['source_folio_pagination_numbers_transposed'])
  for im in W['original_images']:
   self.assertEqual(H(im['path']),im['sha256'])
 def test_prior_count_proposed_total_and_boundary(self):
  self.assertEqual(A['prior_lilly_accepted'],4323)
  self.assertEqual(A['new_documentary_records'],61)
  self.assertEqual(A['lilly_if_published'],4384)
  self.assertEqual(A['combined_if_published'],5450)
  self.assertEqual(A['next_numbered_chapter'],'LXXVI')
  self.assertEqual(A['next_original_pdf_page'],466)
  self.assertFalse(A['canonical_remotely_published'])
 def test_unverified_cases_remain_zero(self):
  self.assertEqual(A['independent_competency_outcomes'],0)
  self.assertEqual(A['independent_travel_decisions'],0)
  self.assertEqual(A['independent_absent_person_cases'],0)
  self.assertEqual(A['new_empirical_astrology_validations'],0)
  self.assertEqual(A['runtime_model_promotions'],0)
  self.assertEqual(len(U['issues']),20)
 def test_mutations_fail(self):
  rs=copy.deepcopy(R);rs[0]['record_number']=4323
  with self.assertRaises(AssertionError):check(rs)
  rs=copy.deepcopy(R);rs[28]['empirical_forecast_validated']=True
  with self.assertRaises(AssertionError):check(rs)
  rs=copy.deepcopy(R);rs[-1]['chapter']='LXXV'
  with self.assertRaises(AssertionError):check(rs)
  rs=copy.deepcopy(R);rs[22]['printed_page_numerals_as_physically_imprinted']=[430]
  with self.assertRaises(AssertionError):check(rs)
if __name__=='__main__':unittest.main(verbosity=2)
