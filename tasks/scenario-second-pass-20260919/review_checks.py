"""Structural review checks and typed-state fixtures, not NLP validation."""
from pathlib import Path
import json
import re
import importlib.util
import tempfile
import unittest
ROOT=Path(__file__).resolve().parent

def next_probe(state: dict) -> str:
    if state.get('paused'): return 'PAUSED'
    if state.get('design_example'): return 'DESIGN_FEEDBACK'
    if state.get('confused'): return 'REPAIR_QUESTION'
    if state.get('declined'): return 'CHANGE_TOPIC'
    if state.get('reason_given'): return 'NO_REASON_REASK'
    if state.get('action')=='accept': return 'What would make you say yes?'
    if state.get('action')=='decline': return 'What would make you say no?'
    if state.get('action')=='defer': return 'What would make you choose later?'
    return 'NO_MOTIVE_INFERENCE'
ANTECEDENTS={'R01':'recurrence','R04':'body_signal','M10':'body_signal','M06':'cue','R11':'withdrawal','R12':'reported_change','R13':'changed_trust','M02':'pressure_reaction','M08':'named_ability'}
def admit(qid: str,state: dict) -> bool:
    if state.get('paused') or state.get('topic_declined') or state.get('confused'): return False
    if qid in state.get('answered',[]): return False
    key=ANTECEDENTS.get(qid)
    if key and state.get(key)!='reported': return False
    return True
class DesignChecks(unittest.TestCase):
    def test_full_bank_and_facet_inventory(self):
        old=json.loads((ROOT/'source-interviewer-bank.json').read_text())
        bank=json.loads((ROOT/'interviewer-bank-v4.json').read_text())
        audit=json.loads((ROOT/'question-audit.json').read_text())
        self.assertEqual({q['id'] for q in old['questions']},{a['id'] for a in audit})
        self.assertEqual(len(audit),55)
        self.assertEqual(len({q['id'] for q in bank['questions']}),len(bank['questions']))
        facets=json.loads((ROOT/'coverage-plan-v4.json').read_text())['facets']
        self.assertEqual(len(facets),73)
        ids={q['id'] for q in bank['questions']}
        for f in facets:
            self.assertTrue(f['candidate_routes'])
            self.assertTrue(set(f['candidate_routes'])<=ids)
            self.assertEqual(f['status'],'planned_not_empirically_verified')
    def test_one_visible_question(self):
        bank=json.loads((ROOT/'interviewer-bank-v4.json').read_text())
        for q in bank['questions']:
            # Quoted dialogue can itself contain a question, without adding a respondent task.
            outside_dialogue=re.sub(r'“[^”]*”', '', q['question'])
            self.assertEqual(outside_dialogue.count('?'),1,q['id'])
        # Punctuation is not semantic proof of one response task.
    def test_motive_routes(self):
        cases=[({'action':'accept'},'What would make you say yes?'),({'action':'decline'},'What would make you say no?'),({'action':'defer'},'What would make you choose later?'),({'action':'accept','reason_given':True},'NO_REASON_REASK'),({'action':'accept','paused':True},'PAUSED'),({'action':'accept','design_example':True},'DESIGN_FEEDBACK'),({'action':'accept','confused':True},'REPAIR_QUESTION'),({'action':'accept','declined':True},'CHANGE_TOPIC'),({},'NO_MOTIVE_INFERENCE')]
        for state,expected in cases:self.assertEqual(next_probe(state),expected)
    def test_all_reaction_guards(self):
        for qid,key in ANTECEDENTS.items():
            for value in ('absent','unknown','inapplicable','declined',None):self.assertFalse(admit(qid,{key:value}),(qid,value))
            self.assertTrue(admit(qid,{key:'reported'}),qid)
            self.assertFalse(admit(qid,{key:'reported','answered':[qid]}),qid)
            self.assertFalse(admit(qid,{key:'reported','paused':True}),qid)
    def test_variants_not_biography(self):
        for qid in ('R02','R07','R08','M04','R10'):
            self.assertTrue(admit(qid,{}));self.assertFalse(admit(qid,{'topic_declined':True}))
        # Hypothetical admission does not write evidence or an actual event.
spec=importlib.util.spec_from_file_location('capture',ROOT/'private_capture.py')
capture=importlib.util.module_from_spec(spec);spec.loader.exec_module(capture)
class CaptureChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='hd-capture-test-',dir=str(Path.home()));self.root=Path(self.tmp.name)/'private'
        self.q={'event_id':'e0001','kind':'presented_question','text':'What would you reply?','captured_at':'2026-09-19T00:00:00Z','source_surface':'synthetic_test','scenario_id':'A0','scenario_version':'test'}
    def tearDown(self):self.tmp.cleanup()
    def test_roundtrip_and_idempotence(self):
        first=capture.append_event(self.root,self.q);second=capture.append_event(self.root,self.q)
        self.assertTrue(first['created']);self.assertFalse(second['created']);self.assertEqual(capture.export(self.root)['events'],[self.q])
    def test_no_overwrite(self):
        capture.append_event(self.root,self.q)
        with self.assertRaises(ValueError):capture.append_event(self.root,{**self.q,'text':'different'})
        self.assertEqual(capture.export(self.root)['events'],[self.q])
    def test_missing_question_and_design_example(self):
        a={'event_id':'e0002','kind':'participant_answer','text':'yes','captured_at':'2026-09-19T00:00:01Z','source_surface':'synthetic_test','question_event_id':'e0001','source_kind':'usual_scenario_self_report','is_design_example':False}
        with self.assertRaises(ValueError):capture.append_event(self.root,a)
        capture.append_event(self.root,self.q)
        with self.assertRaises(ValueError):capture.append_event(self.root,{**a,'is_design_example':True})
        self.assertTrue(capture.append_event(self.root,a)['saved']);self.assertEqual(capture.export(self.root)['participant_answers'],1)
    def test_correction_preserves_original(self):
        capture.append_event(self.root,self.q)
        event={'event_id':'e0002','kind':'correction','text':'corrected wording','captured_at':'2026-09-19T00:00:02Z','source_surface':'synthetic_test','revises_event_id':'e0001'}
        capture.append_event(self.root,event);self.assertEqual(capture.export(self.root)['events'][0],self.q)
    def test_symlink_and_git_refused(self):
        outside=Path(self.tmp.name)/'outside';outside.mkdir(mode=0o700);self.root.symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError):capture.append_event(self.root,self.q)
        self.root.unlink();self.root.mkdir(mode=0o700);(self.root/'.git').mkdir()
        with self.assertRaises(ValueError):capture.append_event(self.root,self.q)
    def test_permissions_and_source_mode(self):
        capture.append_event(self.root,self.q)
        self.assertEqual((self.root/'events/e0001.json').stat().st_mode & 0o777,0o600);self.assertEqual(self.root.stat().st_mode & 0o777,0o700)
        a={**self.q,'event_id':'e0002','kind':'participant_answer','question_event_id':'e0001','is_design_example':False}
        with self.assertRaises(ValueError):capture.append_event(self.root,a)
if __name__=='__main__':unittest.main(verbosity=2)
