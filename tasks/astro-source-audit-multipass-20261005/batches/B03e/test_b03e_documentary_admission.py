"""Historical case documentary rule release checks, not empirical prediction tests."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda x:json.loads((B/x).read_text(encoding='utf-8'))
H=lambda x:hashlib.sha256((B/x).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
def validate(rows):
 assert len(rows)==58
 assert [r['record_number'] for r in rows]==list(range(3361,3419))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(3361,3419)]
 assert [r['source_local_id'] for r in rows]==[f'LIX-C{i:03}' for i in range(1,59)]
 assert all(r['historical_documentation_admitted']
   and not r['real_outcome_independently_authenticated']
   and not r['empirical_astrology_prediction_validated']
   and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LIX' for r in rows[:-1])
 assert rows[-1]['chapter']=='LX_HEADING_ONLY'
 return True
class AcceptedCaseSource(unittest.TestCase):
 def test_record_sequence_and_roles(self):
  self.assertTrue(validate(R['rules']))
  self.assertEqual(R['chapter_lix_substantive_annotations'],57)
  self.assertEqual(R['next_heading_navigation_only'],1)
 def test_draft_lossless_meaning(self):
  for old,new in zip(D['rows'],R['rules'],strict=True):
   for k in ('source_local_id','role','original_pdf_pages','source_short_anchor_not_diplomatic',
     'historical_author_report_paraphrase','conditions_source_limits_or_chronology'):
    self.assertEqual(old[k],new[k])
   self.assertIsNone(old['global_record_number'])
 def test_bidirectional_provenance(self):
  found=[]
  byid={r['id']:r for r in R['rules']}
  for s in M['source_spans']:
   for id in s['canonical_record_ids']:
    self.assertEqual(byid[id]['original_pdf_pages'],s['original_pdf_pages'])
    found.append(id)
  self.assertEqual(sorted(found),sorted(byid))
  self.assertEqual(len(found),58)
  self.assertEqual(M['span_count'],25)
 def test_original_scans_and_receipt(self):
  for im in W['images']:
   self.assertEqual(H(im['path']),im['sha256'])
  for f,key in [
   ('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256')]:
   self.assertEqual(H(f),A[key])
 def test_no_independent_success(self):
  self.assertEqual(A['independently_confirmed_marriage_outcome'],0)
  self.assertEqual(A['pre_outcome_frozen_predictions_count'],0)
  self.assertFalse(A['original_chart_positions_machine_reconstructed'])
  self.assertEqual(R['empirically_validated_predictive_results'],0)
 def test_guarded_cumulative_totals(self):
  self.assertEqual(A['prior_accepted_lilly'],3360)
  self.assertEqual(A['added_documentary_units'],58)
  self.assertEqual(A['lilly_if_published'],3418)
  self.assertEqual(A['combined_if_published'],4484)
  self.assertEqual(len(U['issues']),18)
  self.assertFalse(A['canonical_published'])
 def test_mutants_rejected(self):
  bad=copy.deepcopy(R['rules']);bad[2]['record_number']=0
  with self.assertRaises(AssertionError):validate(bad)
  bad=copy.deepcopy(R['rules']);bad[9]['real_outcome_independently_authenticated']=True
  with self.assertRaises(AssertionError):validate(bad)
  bad=copy.deepcopy(R['rules']);bad[-1]['chapter']='LIX'
  with self.assertRaises(AssertionError):validate(bad)
if __name__=='__main__':unittest.main(verbosity=2)
