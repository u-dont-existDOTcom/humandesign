"""Original image and editorial traceability checks."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
L=J('CLAIM_LEDGER.json')
def check(rows,spans):
 assert len(rows)==74 and len(spans)==26
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LVII-C{i:03}' for i in range(1,75)]
 mapped=[i for s in spans for i in s['mapped_local_source_ids']]
 assert sorted(ids)==sorted(mapped) and len(ids)==len(mapped)
 byid={r['source_local_id']:r for r in rows}
 assert all(byid[i]['original_pdf_pages']==s['original_pdf_pages']
    for s in spans for i in s['mapped_local_source_ids'])
 assert all(r['global_record_number'] is None
   and not r['historical_documentary_admitted']
   and not r['validated_predictive_accuracy']
   and not r['runtime_model_promoted']
   and not r['word_for_word_transcription_complete'] for r in rows)
 assert all(r['chapter']=='LVII' for r in rows[:-1])
 assert rows[-1]['chapter']=='LVIII_HEADING_ONLY'
 assert rows[-1]['role']=='next_heading_boundary'
 return True
class SourceTests(unittest.TestCase):
 def test_bijection(self):
  self.assertTrue(check(D['rows'],C['source_spans']))
 def test_source_images_sha256(self):
  self.assertEqual(W['original_pdf_pages'],[414,415,416,417])
  for i in W['original_witness_images']:
   p=B/i['path']
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),i['sha256'])
   self.assertEqual(p.stat().st_size,i['bytes'])
 def test_page_seams(self):
  self.assertEqual(sorted(set(tuple(s['original_pdf_pages']) for s in C['source_spans'] if len(s['original_pdf_pages'])>1)),
   [(414,415),(415,416),(416,417)])
 def test_subsection(self):
  self.assertEqual(sum(r['role']=='subheading' for r in D['rows']),1)
  self.assertEqual(D['rows'][-1]['original_pdf_pages'],[417])
 def test_retained_limits(self):
  self.assertEqual(len(U['issues']),19)
  self.assertEqual(L['new_accepted_documentary_records'],0)
  self.assertEqual(L['new_accurate_astro_forecasts'],0)
 def test_semantic_contrasts(self):
  v=' '.join(r['original_author_claim_paraphrase']+' '+r['source_qualifiers_and_limits'] for r in D['rows']).lower()
  for s in ['fidelity','lack of expertise','exception','reception','contrary','weigh','source']:
   if s!='weigh':self.assertIn(s,v)
 def test_mutant_mapping(self):
  x=copy.deepcopy(C['source_spans'])
  x[0]['mapped_local_source_ids'].append(x[1]['mapped_local_source_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],x)
 def test_mutant_mislabel(self):
  x=copy.deepcopy(D['rows']);x[-1]['chapter']='LVII'
  with self.assertRaises(AssertionError):check(x,C['source_spans'])
 def test_mutant_prediction(self):
  x=copy.deepcopy(D['rows']);x[0]['validated_predictive_accuracy']=True
  with self.assertRaises(AssertionError):check(x,C['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
