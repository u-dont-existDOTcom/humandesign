"""Local admission verifies source-preserving transformations."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
def admissible(rows):
 assert len(rows)==74
 assert [r['record_number'] for r in rows]==list(range(3249,3323))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(3249,3323)]
 assert [r['source_local_id'] for r in rows]==[f'LVII-C{i:03}' for i in range(1,75)]
 assert all(r['historical_documentary_admitted'] and not r['validated_predictive_accuracy']
  and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LVII' for r in rows[:-1])
 assert rows[-1]['chapter']=='LVIII_HEADING_ONLY'
 return True
class Admission(unittest.TestCase):
 def test_local_sequence(self):
  self.assertTrue(admissible(R['rules']))
 def test_source_text_preservation(self):
  for old,new in zip(D['rows'],R['rules'],strict=True):
   for k in ['source_local_id','role','original_pdf_pages',
     'source_anchor_short_not_diplomatic',
     'original_author_claim_paraphrase','source_qualifiers_and_limits']:
    self.assertEqual(old[k],new[k])
 def test_reverse_map(self):
  ids=[id for s in M['source_spans'] for id in s['canonical_record_ids']]
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R['rules']))
  self.assertEqual(len(ids),74)
 def test_original_bytes(self):
  for im in W['original_witness_images']:
   self.assertEqual(H(im['path']),im['sha256'])
  for n,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
    ('UNRESOLVED.json','unresolved_sha256'),
    ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256')]:
   self.assertEqual(H(n),A[k])
 def test_baseline_and_uncertainty(self):
  self.assertEqual((A['previous_accepted_lilly'],A['added_documentary_units'],
    A['lilly_if_published'],A['combined_if_published']),(3248,74,3322,4388))
  self.assertEqual(len(U['issues']),19)
  self.assertFalse(A['canonical_published'])
 def test_negative_evidence(self):
  self.assertEqual(R['empirically_validated_predictions'],0)
  self.assertEqual(R['runtime_model_promotions'],0)
 def test_mutated_identifier(self):
  r=copy.deepcopy(R['rules']);r[2]['record_number']=4
  with self.assertRaises(AssertionError):admissible(r)
 def test_mutated_attestation(self):
  r=copy.deepcopy(R['rules']);r[3]['validated_predictive_accuracy']=True
  with self.assertRaises(AssertionError):admissible(r)
if __name__=='__main__':unittest.main(verbosity=2)
