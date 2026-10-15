"""Check accepted B03b records are lossless documentary derivatives, no proven claims."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda x:json.loads((B/x).read_text(encoding='utf-8'))
H=lambda x:hashlib.sha256((B/x).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
R=J('RULES.json')
C=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED.json')
def allowed(rows):
 assert len(rows)==45
 assert [r['record_number'] for r in rows]==list(range(3204,3249))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(3204,3249)]
 assert [r['local_id'] for r in rows]==[f'LVI-C{i:03}' for i in range(1,46)]
 assert all(r['global_record_number']==r['record_number'] and
            r['admitted_as_historical_documentation'] and
            not r['accepted_as_empirically_validated_prediction'] and
            not r['validated_by_real_world_cases'] and
            not r['runtime_predicate_active'] and
            not r['real_world_military_use_authorized'] and
            not r['complete_diplomatic_transcription'] for r in rows)
 assert all(r['chapter']=='LVI' for r in rows[:-1])
 assert rows[-1]['role']=='next_heading_boundary' and rows[-1]['chapter']=='LVII_HEADING_NAVIGATION_ONLY'
 return True
class Documentary(unittest.TestCase):
 def test_frozen_source_units(self):
  self.assertTrue(allowed(R['rules']))
  self.assertEqual(R['first_record'],3204)
  self.assertEqual(R['last_record'],3248)
  self.assertEqual(R['substantive_lvi_units'],44)
  self.assertEqual(R['next_chapter_navigation_only_units'],1)
 def test_exact_draft_to_documentary_safeguards(self):
  for prior,now in zip(D['rows'],R['rules'],strict=True):
   for key in ['local_id','role','original_pdf_pages','original_printed_pages',
     'original_source_abbreviated_anchor_not_full_quote',
     'historical_author_assertion_paraphrase','predicates_and_caveats']:
    self.assertEqual(prior[key],now[key],(prior['local_id'],key))
   self.assertIsNone(prior['global_record_number'])
   self.assertFalse(prior['admitted_as_historical_documentation'])
 def test_source_image_to_id_bijection(self):
  byid={r['id']:r for r in R['rules']}
  seen=[]
  for s in C['source_spans']:
   self.assertEqual([r['original_pdf_pages'] for r in (byid[x] for x in s['canonical_record_ids'])],
                    [s['original_pdf_pages']]*len(s['canonical_record_ids']))
   seen+=s['canonical_record_ids']
  self.assertEqual(len(seen),45)
  self.assertEqual(sorted(seen),sorted(byid))
  self.assertEqual(C['span_count'],19)
 def test_sha256_witnesses_and_acceptance(self):
  for image in W['images']:
   self.assertEqual(H(image['path']),image['sha256'])
   self.assertEqual((B/image['path']).stat().st_size,image['bytes'])
  for file,key in [
    ('RULES.json','rules_sha256'),
    ('SOURCE_ORDER.json','source_order_sha256'),
    ('UNRESOLVED.json','unresolved_sha256'),
    ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_map_sha256'),
    ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_sha256')]:
   self.assertEqual(H(file),A[key],file)
 def test_scope_and_counts(self):
  self.assertEqual(A['previous_lilly_accepted'],3203)
  self.assertEqual(A['lilly_if_published'],3248)
  self.assertEqual(A['retained_ptolemy'],1066)
  self.assertEqual(A['combined_if_published'],4314)
  self.assertEqual(len(U['issues']),17)
  self.assertEqual(A['unresolved_source_issues'],17)
  self.assertFalse(A['canonical_source_published'])
 def test_negative_prediction_guards(self):
  self.assertFalse(R['blind_complete_second_diplomatic_transcription'])
  self.assertEqual(R['new_empirically_validated_predictions'],0)
  self.assertEqual(A['new_authentic_siege_cases_validated'],0)
  self.assertEqual(A['runtime_predicate_promotions'],0)
  self.assertTrue(all(r['validated_by_real_world_cases'] is False for r in R['rules']))
 def test_original_grammar_preserved(self):
  text=' '.join(x['historical_author_assertion_paraphrase'] for x in R['rules']).lower()
  for phrase in ['one-way','seventh','fourth','moon','governor',
                 'absence of reception','holdout','retrogradation']:
   if phrase not in text:
    # Some qualifiers live in predicate caveats, not the summary.
    combined=text+' '+' '.join(x['predicates_and_caveats'] for x in R['rules']).lower()
    self.assertIn(phrase,combined)
 def test_bad_mutants_rejected(self):
  wrong=copy.deepcopy(R['rules']);wrong[10]['validated_by_real_world_cases']=True
  with self.assertRaises(AssertionError):allowed(wrong)
  wrong=copy.deepcopy(R['rules']);wrong[-1]['chapter']='LVI'
  with self.assertRaises(AssertionError):allowed(wrong)
  wrong=copy.deepcopy(R['rules']);wrong[1]['record_number']=3000
  with self.assertRaises(AssertionError):allowed(wrong)
if __name__=='__main__':unittest.main(verbosity=2)
