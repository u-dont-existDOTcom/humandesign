import hashlib,json,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
class Admission(unittest.TestCase):
 def test_contiguous_ids(self):
  self.assertEqual([r['record_number'] for r in R],list(range(3485,3528)))
  self.assertEqual([r['id'] for r in R],[f'R{i}' for i in range(3485,3528)])
 def test_original_provisional_content_preserved(self):
  for a,b in zip(D,R,strict=True):
   for k in ('local_id','role','source_paraphrase','original_pdf_pages','qualifiers_and_unresolved'):
    self.assertEqual(a[k],b[k])
   self.assertIsNone(a['global_record_number'])
 def test_original_to_final_map(self):
  mapped=[k for x in M['source_spans'] for k in x['canonical_record_ids']]
  self.assertEqual(len(mapped),43)
  self.assertEqual(sorted(mapped),sorted(r['id'] for r in R))
 def test_rules_hash_and_source(self):
  self.assertEqual(H('RULES.json'),A['rules_sha256'])
  self.assertEqual(H('UNRESOLVED.json'),A['uncertainties_sha256'])
  self.assertEqual(H('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json'),A['reverse_map_sha256'])
  self.assertEqual(len(U['issues']),17)
 def test_unverified_outcome_retained(self):
  self.assertEqual(A['author_reported_dog_recoveries'],1)
  self.assertEqual(A['independently_authenticated_dog_recoveries'],0)
  self.assertEqual(A['new_empirical_predictions_validated'],0)
  self.assertFalse(A['complete_diplomatic_second_reading'])
  self.assertEqual(A['upper_room_prediction_outcome'],'UNRESOLVED_NOT_ESTABLISHED_BY_UNDER_TABLE_REPORT')
 def test_baseline(self):
  self.assertEqual(A['previous_accepted_lilly'],3484)
  self.assertEqual(A['added_documentary_records'],43)
  self.assertEqual(A['lilly_if_published'],3527)
  self.assertEqual(A['combined_if_published'],4593)
  self.assertFalse(A['remote_published'])
 def test_last_navigation_only(self):
  self.assertTrue(all(r['chapter']=='LXII' for r in R[:-1]))
  self.assertEqual(R[-1]['chapter'],'LXIII_BOUNDARY_ONLY')
  self.assertEqual(R[-1]['original_pdf_pages'],[428])
 def test_mutant_false_acceptance_flag(self):
  invalid=copy.deepcopy(R)
  invalid[5]['empirical_case_verified']=True
  self.assertTrue(any(r['empirical_case_verified'] for r in invalid))
  self.assertFalse(any(r['empirical_case_verified'] for r in R))
if __name__=='__main__':unittest.main(verbosity=2)
