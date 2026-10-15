import json,hashlib,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
class Admission(unittest.TestCase):
 def test_consecutive_global_ids(self):
  self.assertEqual([r['record_number'] for r in R],list(range(3528,3572)))
  self.assertEqual([r['id'] for r in R],[f'R{i}' for i in range(3528,3572)])
 def test_preserved_draft_text(self):
  for before,after in zip(D,R,strict=True):
   for k in ('local_id','source_conditions_and_uncertainty','historical_author_paraphrase',
    'original_pdf_pages','role'):
    self.assertEqual(before[k],after[k])
   self.assertIsNone(before['global_record_number'])
 def test_original_source_to_final_map(self):
  mapped=[x for s in M['source_spans'] for x in s['accepted_global_record_ids']]
  self.assertEqual(sorted(mapped),sorted(r['id'] for r in R))
  self.assertEqual(len(mapped),44)
  self.assertEqual(M['span_count'],15)
 def test_accepted_document_hashes(self):
  for f,key in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256')]:
   self.assertEqual(H(f),A[key])
 def test_historical_case_not_accurate_prediction(self):
  self.assertEqual(A['author_reported_money_recovery_cases'],1)
  self.assertEqual(A['independent_authentication_of_theft_outcome'],0)
  self.assertEqual(A['independent_authentication_of_thief_identity'],0)
  self.assertEqual(A['new_empirical_predictions_validated'],0)
  self.assertFalse(A['second_diplomatic_original_reader'])
 def test_source_numbering_exception(self):
  self.assertEqual(R[-1]['chapter'],'NEXT_PRINTED_LIV_FISH_STOLEN_NAVIGATION_ONLY')
  self.assertEqual(A['next_heading_printed'],'CHAP. LIV. Fish Stolen')
  self.assertEqual(A['next_heading_sequential'],'LXIV')
 def test_predecessor_and_new_count(self):
  self.assertEqual(A['previous_accepted_lilly'],3527)
  self.assertEqual(A['new_documentary_records'],44)
  self.assertEqual(A['lilly_if_published'],3571)
  self.assertEqual(A['combined_if_published'],4637)
  self.assertFalse(A['remote_published'])
 def test_no_false_case_mutation(self):
  altered=copy.deepcopy(R)
  altered[10]['empirically_validated_thief_or_case']=True
  self.assertTrue(any(r['empirically_validated_thief_or_case'] for r in altered))
  self.assertFalse(any(r['empirically_validated_thief_or_case'] for r in R))
if __name__=='__main__':unittest.main(verbosity=2)
