import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda x:json.loads((B/x).read_text())
R=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')['source_spans']
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
class SourceTests(unittest.TestCase):
 def test_exact_bijection(self):
  ids=[r['local_id'] for r in R]
  self.assertEqual(ids,[f'LXII-C{i:03}' for i in range(1,44)])
  mapped=[k for s in M for k in s['mapped_local_ids']]
  self.assertEqual(sorted(ids),sorted(mapped))
  self.assertEqual(len(mapped),43)
  self.assertEqual(len(M),14)
 def test_original_scans(self):
  self.assertEqual(W['physical_body_pages'],[426,427,428])
  for x in W['source_images']:
   body=(B/x['path']).read_bytes()
   self.assertEqual(len(body),x['bytes'])
   self.assertEqual(hashlib.sha256(body).hexdigest(),x['sha256'])
 def test_source_uncertainty(self):
  self.assertEqual(len(U['issues']),17)
  self.assertEqual(C['independently_authenticated_cases'],0)
  self.assertEqual(C['new_empirical_predictions'],0)
 def test_boundary(self):
  self.assertEqual(R[0]['original_pdf_pages'],[426])
  self.assertEqual(R[-1]['chapter'],'LXIII_BOUNDARY_ONLY')
  self.assertTrue(all(r['chapter']=='LXII' for r in R[:-1]))
 def test_provisional(self):
  self.assertTrue(all(not r['historical_documentary_admitted'] and
    not r['empirical_case_verified'] for r in R))
 def test_source_date_and_mixed_location(self):
  text=' '.join(r['source_paraphrase']+' '+r['qualifiers_and_unresolved'] for r in R).lower()
  self.assertIn('29 august 1646',text)
  self.assertIn('under a table',text)
  self.assertIn('upper-room',text)
  self.assertIn('does not establish',text)
 def test_original_to_source_positions(self):
  by={r['local_id']:r for r in R}
  for span in M:
   for k in span['mapped_local_ids']:
    self.assertEqual(by[k]['original_pdf_pages'],span['original_pdf_pages'])
 def test_house_printed_page_offsets(self):
  for r in R:
   self.assertEqual(r['printed_pages'],[p-34 for p in r['original_pdf_pages']])
 def test_mutation_boundary(self):
  import copy
  bad=copy.deepcopy(R)
  bad[-1]['chapter']='LXII'
  self.assertNotEqual(bad[-1]['chapter'],'LXIII_BOUNDARY_ONLY')
if __name__=='__main__':unittest.main(verbosity=2)
