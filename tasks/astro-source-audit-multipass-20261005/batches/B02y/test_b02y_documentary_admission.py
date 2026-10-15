#!/usr/bin/env python3
"""Independent mechanical invariants for historic-documentary source intake."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
A=J('ACCEPTANCE.json')
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
S=J('SOURCE_ORDER.json')
U=J('UNRESOLVED.json')
L=J('CLAIM_LEDGER_ACCEPTED_LOCAL.json')

def admissible(rs):
 assert len(rs)==76
 assert [r['record_number'] for r in rs]==list(range(3072,3148))
 assert [r['id'] for r in rs]==[f"R{n}" for n in range(3072,3148)]
 assert [r['local_id'] for r in rs]==[f"LIII-C{n:03}" for n in range(1,77)]
 assert all(r['global_record_number']==r['record_number'] for r in rs)
 assert all(r['accepted_historical_documentary'] and not r['is_provisional'] and
            r['source_record_admitted_for_documentary_reference'] and
            not r['accepted_as_empirical_prediction'] and
            not r['empirically_verified_case'] and not r['model_runtime_promotion'] and
            not r['safe_for_real_person_prognosis'] and
            not r['source_anchor_claimed_word_for_word_complete'] for r in rs)
 assert all(r['original_printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rs)
 assert all(r['chapter']=='LIII' for r in rs[:-1])
 assert rs[-1]['record_role']=='next_heading_boundary' and rs[-1]['chapter']=='LIV_HEADING_NAVIGATION_ONLY'
 return True

class TestDocumentaryAdmission(unittest.TestCase):
 def test_consecutive_guarded_ids(self):
  self.assertTrue(admissible(R['rules']))
  self.assertEqual(R['first_record'],3072)
  self.assertEqual(R['last_record'],3147)
  self.assertEqual(R['substantive_chapter_liii_units'],75)
  self.assertEqual(R['next_chapter_navigation_only_units'],1)
 def test_original_to_final_still_bijective(self):
  maps=M['source_spans']
  self.assertEqual(len(maps),27)
  self.assertEqual(sorted(x for m in maps for x in m['canonical_record_ids']),
                   sorted(r['id'] for r in R['rules']))
  self.assertEqual(sum(len(m['canonical_record_ids']) for m in maps),76)
  self.assertEqual([r['record_number'] for r in R['rules']],
                   [r['record_number'] for r in R['rules'] if r['record_number'] in
                    set(x['record_number'] for x in R['rules'])])
 def test_draft_provenance_exact_preservation(self):
  for before,after in zip(D['rows'],R['rules'],strict=True):
   for k in ('local_id','source_anchor_editorial_abbreviation',
             'source_statement_paraphrase','source_predicates_and_qualifiers',
             'original_pdf_pages','original_printed_pages','record_role'):
    self.assertEqual(before[k],after[k],(k,before['local_id']))
 def test_original_witness_hashes(self):
  self.assertEqual(W['original_full_pdf_sha256'],A['original_full_pdf_sha256'])
  for img in W['images']:
   self.assertEqual(H(img['relative_path']),img['sha256'])
 def test_frozen_sha_receipt(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
              ('UNRESOLVED.json','unresolved_sha256'),
              ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','original_to_record_source_map_sha256'),
              ('CLAIM_LEDGER_ACCEPTED_LOCAL.json','claim_ledger_sha256'),
              ('LIII_SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_notes_sha256')]:
   self.assertEqual(H(f),A[k],f)
 def test_prior_and_future_counts(self):
  self.assertEqual(A['previous_accepted_lilly'],3071)
  self.assertEqual(A['new_documentary_records'],76)
  self.assertEqual(A['lilly_if_published'],3147)
  self.assertEqual(A['ptolemy_retained'],1066)
  self.assertEqual(A['combined_if_published'],4213)
  self.assertFalse(A['canonical_published'])
  self.assertFalse(A['independent_blind_original_transcription_done'])
 def test_source_limits_and_adverse_outcomes(self):
  self.assertEqual(len(U['points']),16)
  self.assertEqual(A['source_uncertainties_retained'],16)
  text=' '.join(r['source_statement_paraphrase'] for r in R['rules'])
  self.assertIn('other than opposition',text)
  self.assertIn('square',text)
  self.assertIn('excepted',text)
  self.assertIn('asymmetric reception',text)
  self.assertIn('elliptical',text.lower())
 def test_no_observed_outcome_or_model_promotions(self):
  self.assertEqual(R['runtime_promotions'],0)
  self.assertFalse(R['accepted_as_empirical_astro_prediction'])
  self.assertEqual(L['predictions_validated'],0)
  self.assertEqual(L['authenticated_court_outcomes'],0)
  self.assertEqual(L['real_hunting_trials'],0)
  self.assertEqual(L['new_runtime_rules'],0)
 def test_bad_mutants_are_rejected(self):
  bad=copy.deepcopy(R['rules'])
  bad[4]['record_number']=0
  with self.assertRaises(AssertionError):admissible(bad)
  bad=copy.deepcopy(R['rules'])
  bad[-1]['chapter']='LIII'
  with self.assertRaises(AssertionError):admissible(bad)
  bad=copy.deepcopy(R['rules'])
  bad[8]['empirically_verified_case']=True
  with self.assertRaises(AssertionError):admissible(bad)
if __name__=='__main__':unittest.main(verbosity=2)
