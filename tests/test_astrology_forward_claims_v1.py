"""Mechanical tests for atomic forward claim evaluation; synthetic fixtures only."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'score_astrology_forward_claims_v1.py'
spec = importlib.util.spec_from_file_location('astro_forward_score', SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

HEX = 'a'*64


def fixture(*, phase='DEVELOPMENT', with_decoys=True):
    decoys = ([{'id':'near','panel':'matched','panel_source_ref':'frozen matched seed'},
               {'id':'distant','panel':'broad','panel_source_ref':'frozen broad seed'}]
              if with_decoys else [])
    return {
       'schema': 'astrology-forward-claims-v1',
       'study_id':'synthetic-test-only', 'arm_id':'western_lilly',
       'ruleset_version':'w-0.1', 'phase':phase,
       'created_at_utc':'2026-10-20T16:00:00Z',
       'chart_feature_sha256':HEX, 'questionnaire_sha256':'b'*64,
       'probability_status':'DECLARED_UNCALIBRATED',
       'decoy_panels':decoys,
       'claims':[{
          'claim_id':'A1','question_id':'Q1','status':'DIRECTIONAL',
          'domain':'decisions', 'context':'importance to respondent high',
          'response_window':'last twelve months',
          'operational_definition':'Which response happened most often on consequential decisions?',
          'dependency_cluster':'decision_timing',
          'source_rule_refs':['lilly:rule-001'],
          'baseline_source_ref':'frozen development frequencies dummy',
          'outcomes':['wait','act'],
          'preferred_option':'wait', 'counterexample_outcomes':['act'],
          'predicted':{'wait':0.75,'act':0.25},
          'baseline':{'wait':0.60,'act':0.40},
          'decoys':({
              'near':{'wait':0.50,'act':0.50},
              'distant':{'wait':0.40,'act':0.60}}
              if with_decoys else {})
       },{
          'claim_id':'A2','question_id':'Q2','status':'NULL',
          'domain':'spirituality','context':'longer term','response_window':'last twelve months',
          'operational_definition':'How strongly practice shapes decisions',
          'dependency_cluster':'spirituality','source_rule_refs':['source rule tested'],
          'reason':'no unambiguous directional support'
       }]
    }


def responses(p, value='wait'):
    raw=json.dumps(p,sort_keys=True).encode()
    return raw,{
       'schema':'astrology-forward-responses-v1',
       'prediction_sha256':hashlib.sha256(raw).hexdigest(),
       'captured_at_utc':'2026-10-20T17:00:00Z',
       'answers':{'Q1':value,'Q2':'act'}
    }


class ContractTests(unittest.TestCase):
    def test_valid_fixture(self):
        r=mod.validate_predictions(fixture())
        self.assertEqual((r['directional'],r['null_or_unresolved']),(1,1))

    def test_equal_opposite_alternatives_do_not_count(self):
        p=fixture();c=p['claims'][0]
        c['predicted']={'wait':.5,'act':.5}
        with self.assertRaisesRegex(mod.ContractError,'no unique preferred option'):
            mod.validate_predictions(p)

    def test_no_provenance_for_baseline(self):
        p=fixture();del p['claims'][0]['baseline_source_ref']
        with self.assertRaisesRegex(mod.ContractError,'baseline_source_ref'):
            mod.validate_predictions(p)

    def test_no_gain_over_baseline(self):
        p=fixture();p['claims'][0]['predicted']={'wait':.55,'act':.45}
        with self.assertRaisesRegex(mod.ContractError,'no incremental'):
            mod.validate_predictions(p)

    def test_improper_distribution_rejected(self):
        p=fixture();p['claims'][0]['predicted']={'wait':.8,'act':.4}
        with self.assertRaisesRegex(mod.ContractError,'sum to 1'):
            mod.validate_predictions(p)

    def test_missing_opposite_outcome_rejected(self):
        p=fixture();p['claims'][0]['counterexample_outcomes']=[]
        with self.assertRaisesRegex(mod.ContractError,'enumerate all opposite'):
            mod.validate_predictions(p)

    def test_duplicate_question_alternative_cannot_double_score(self):
        p=fixture();extra=copy.deepcopy(p['claims'][0]);extra['claim_id']='A3'
        p['claims'].append(extra)
        with self.assertRaisesRegex(mod.ContractError,'duplicate claim_id or question_id'):
            mod.validate_predictions(p)

    def test_null_fallback_forbidden(self):
        p=fixture();p['claims'][1]['predicted']={'spiritual':.8,'nonspiritual':.2}
        with self.assertRaisesRegex(mod.ContractError,'must not claim predictive credit'):
            mod.validate_predictions(p)

    def test_two_panel_requirement_only_in_evidential_phase(self):
        p=fixture(phase='VALIDATION',with_decoys=False)
        with self.assertRaisesRegex(mod.ContractError,'matched and broad'):
            mod.validate_predictions(p)
        self.assertEqual(mod.validate_predictions(fixture(with_decoys=False))['decoy_count'],0)

    def test_brier_positive_on_preferred_observation(self):
        p=fixture();data,r=responses(p)
        res=mod.score_predictions(data,r)
        self.assertEqual(res['summary']['scored'],1)
        self.assertEqual(res['summary']['null_or_unresolved'],1)
        self.assertGreater(res['records'][0]['brier_skill'],0)
        self.assertFalse(res['summary']['independent_freeze_proven_by_this_tool'])
        self.assertEqual(len(res['summary']['decoy_comparison']),2)

    def test_opposite_observation_produces_negative_score(self):
        p=fixture();data,r=responses(p,'act')
        res=mod.score_predictions(data,r)
        self.assertFalse(res['records'][0]['directional_hit'])
        self.assertLess(res['records'][0]['brier_skill'],0)
        self.assertLess(res['records'][0]['log_skill'],0)

    def test_unknown_not_a_hit_and_coverage_reported(self):
        p=fixture();data,r=responses(p,'__UNKNOWN__')
        res=mod.score_predictions(data,r)
        self.assertEqual(res['summary']['scored'],0)
        self.assertEqual(res['summary']['missing_or_unknown'],1)
        self.assertEqual(res['summary']['scorable_coverage'],0)

    def test_missing_value_not_added_as_negative(self):
        p=fixture();data,r=responses(p)
        del r['answers']['Q1']
        res=mod.score_predictions(data,r)
        self.assertEqual(res['summary']['missing_or_unknown'],1)
        self.assertEqual(res['summary']['directional_hits'],0)

    def test_response_binding_requires_identical_bytes(self):
        p=fixture();data,r=responses(p)
        r['prediction_sha256']='0'*64
        with self.assertRaisesRegex(mod.ContractError,'not bound'):
            mod.score_predictions(data,r)

    def test_missing_chronology_not_a_prospective_freeze(self):
        p=fixture();data,r=responses(p)
        r['captured_at_utc']='2026-10-19T17:00:00Z'
        with self.assertRaisesRegex(mod.ContractError,'after the declared'):
            mod.score_predictions(data,r)

    def test_unanticipated_response_rejected(self):
        p=fixture();data,r=responses(p)
        r['answers']['Q1']='sometimes'
        with self.assertRaisesRegex(mod.ContractError,'not a predeclared'):
            mod.score_predictions(data,r)

    def test_avoid_double_counting_repeated_questions_in_same_cluster(self):
        p=fixture();q=copy.deepcopy(p['claims'][0]);q['claim_id']='A3';q['question_id']='Q3'
        p['claims'].append(q)
        data,r=responses(p)
        r['answers']['Q3']='act'
        res=mod.score_predictions(data,r)
        self.assertEqual(res['summary']['cluster_count'],1)
        half=(res['records'][0]['log_skill']+res['records'][-1]['log_skill'])/2
        self.assertAlmostEqual(res['summary']['mean_log_skill_by_dependency_cluster'],half)

    def test_identical_true_and_decoy_chart_has_no_discrimination_margin(self):
        p=fixture();p['claims'][0]['decoys']['near']={'wait':.75,'act':.25}
        data,r=responses(p)
        res=mod.score_predictions(data,r)
        margins={a['id']:a['mean_true_over_decoy_log_score'] for a in res['summary']['decoy_comparison']}
        self.assertAlmostEqual(margins['near'],0)
        self.assertGreater(margins['distant'],0)

if __name__=='__main__':
    unittest.main()