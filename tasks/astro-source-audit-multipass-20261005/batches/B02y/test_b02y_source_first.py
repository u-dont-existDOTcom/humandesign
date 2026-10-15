#!/usr/bin/env python3
import copy
import hashlib
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
j=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
D=j('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=j('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=j('SOURCE_WINDOW_MANIFEST.json')
U=j('UNRESOLVED_SOURCE_LIMITS.json')
L=j('CLAIM_LEDGER.json')
O=j('SOURCE_ORDER_DRAFT.json')

def validate(rows,spans,images):
    assert len(rows)==76
    assert len(spans)==27
    ids=[r['local_id'] for r in rows]
    assert ids==[f'LIII-C{i:03}' for i in range(1,77)]
    assert len(set(ids))==len(ids)
    mapped=[rid for s in spans for rid in s['draft_local_ids']]
    assert sorted(mapped)==sorted(ids) and len(mapped)==len(ids)
    assert all(tuple(s['original_pdf_pages'])==tuple(rows[ids.index(rid)]['original_pdf_pages'])
               for s in spans for rid in s['draft_local_ids'])
    assert all(r['global_record_number'] is None and
           r['source_anchor_claimed_word_for_word_complete'] is False and
           r['is_provisional'] and not r['accepted_historical_documentary'] and
           not r['empirically_verified_case'] and not r['model_runtime_promotion'] and
           not r['safe_for_real_person_prognosis'] for r in rows)
    assert all(set(r['original_pdf_pages']).issubset(set(range(405,411))) for r in rows)
    assert all(r['original_printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
    assert rows[0]['record_role']=='heading' and rows[0]['original_pdf_pages']==[405]
    assert rows[-1]['record_role']=='next_heading_boundary' and rows[-1]['original_pdf_pages']==[410]
    assert rows[-1]['chapter']=='LIV_HEADING_NAVIGATION_ONLY'
    assert all(r['chapter']=='LIII' for r in rows[:-1])
    assert len(images)==6 and [i['pdf_page'] for i in images]==list(range(405,411))
    assert all(i['printed_page']==i['pdf_page']-34 and i['bytes']>200000 for i in images)
    assert all(len(r['source_statement_paraphrase'])>25 and
               len(r['source_predicates_and_qualifiers'])>22 for r in rows)
    assert sum(r['record_role']=='marginal_author_note' for r in rows)==1
    assert sum(r['record_role']=='subheading' for r in rows)==1
    assert len([r for r in rows if len(r['original_pdf_pages'])>1])>=10

class TestB02y(unittest.TestCase):
    def test_canonical_frozen_baseline(self):
        self.assertEqual(W['previously_accepted_lilly_count'],3071)
        self.assertEqual(W['chapter'],'LIII')
        self.assertEqual(L['new_globally_accepted_records'],0)
        self.assertEqual(L['predictions_validated'],0)
        self.assertEqual(L['new_runtime_rules'],0)
    def test_source_first_bijection_and_position(self):
        validate(D['rows'],C['source_spans'],W['images'])
        self.assertEqual(O['ordered_local_ids'],[r['local_id'] for r in D['rows']])
        self.assertEqual(O['navigation_only_last_id'],'LIII-C076')
        self.assertEqual([s['span_id'] for s in C['source_spans']],
                         [f'LIII-S{i:03}' for i in range(1,28)])
    def test_original_images_integrity(self):
        for i in W['images']:
            b=(B/i['relative_path']).read_bytes()
            self.assertEqual(len(b),i['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(),i['sha256'])
        self.assertEqual(W['original_full_pdf_sha256'],
                         '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
    def test_editorial_boundary_and_subjects(self):
        self.assertIn('BELOW',W['opening'])
        self.assertIn('ABOVE',W['closing'])
        roles=[r['record_role'] for r in D['rows']]
        self.assertIn('assignment',roles)
        self.assertIn('exception',roles)
        self.assertIn('historical_allegation',roles)
        txt=' '.join(r['source_statement_paraphrase'] for r in D['rows']).lower()
        for needle in ('hunting','lawsuit','judge','reconciliation','adversary',
                       'third parties','moon','fourth','reception','saturn','malefic',
                       'court','bribery','capricorn'):
            self.assertIn(needle,txt,needle)
    def test_high_risk_claim_boundary(self):
        for r in D['rows']:
            self.assertFalse(r['accepted_historical_documentary'])
            self.assertFalse(r['empirically_verified_case'])
            self.assertFalse(r['safe_for_real_person_prognosis'])
        self.assertFalse(C['independent_diplomatic_transcription_claimed'])
        self.assertEqual(len(U['points']),16)
        self.assertTrue(L['not_factual_real_person_honesty_or_corruption_diagnostics'])
    def test_known_semantic_reading_and_nonexpansion(self):
        txt=' '.join(r['source_statement_paraphrase'] for r in D['rows'])
        self.assertIn('other than opposition',txt)
        self.assertIn('Saturn',txt)
        self.assertIn('third-party',txt)
        self.assertIn('one-way reception',txt)
        self.assertIn('mutual reception',txt)
        self.assertIn('unresolved',' '.join(r['source_predicates_and_qualifiers'] for r in D['rows']).lower())
        self.assertIn('e contrario',txt.lower())
        self.assertIn('not a validated',' '.join(r['source_predicates_and_qualifiers'] for r in D['rows']).lower())
    def test_mutant_accepted_rejected(self):
        r=copy.deepcopy(D['rows']);r[1]['accepted_historical_documentary']=True
        with self.assertRaises(AssertionError):validate(r,C['source_spans'],W['images'])
    def test_mutant_wrong_boundary_rejected(self):
        r=copy.deepcopy(D['rows']);r[-1]['original_pdf_pages']=[411]
        with self.assertRaises(AssertionError):validate(r,C['source_spans'],W['images'])
    def test_mutant_fake_transcription_rejected(self):
        r=copy.deepcopy(D['rows']);r[10]['source_anchor_claimed_word_for_word_complete']=True
        with self.assertRaises(AssertionError):validate(r,C['source_spans'],W['images'])
    def test_mutant_double_count_rejected(self):
        s=copy.deepcopy(C['source_spans']);s[0]['draft_local_ids'].append(s[1]['draft_local_ids'][0])
        with self.assertRaises(AssertionError):validate(D['rows'],s,W['images'])

if __name__=='__main__':unittest.main(verbosity=2)
