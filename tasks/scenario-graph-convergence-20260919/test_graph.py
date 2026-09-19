"""Focused, explicit-state graph tests; no natural-language scoring."""
from pathlib import Path
import copy,json,unittest
from graph_model import State, Binding, admit, validate_graph, explicit_comparison
ROOT=Path(__file__).resolve().parent
GRAPH=json.loads((ROOT/'ROUTING-GRAPH.json').read_text())
BANK=json.loads((ROOT/'interviewer-bank-v6.json').read_text())
C={c['id']:c for c in GRAPH['routing_contracts']}

def witness(qid):
    c=C[qid];s=State()
    s.annotations={flag:True for flag in c['required_annotations']}
    if c['context_mode']!='self_contained':
        source=c['context_candidates'][0] if c['context_candidates'] else 'volunteered-answer'
        s.binding=Binding('example-event',source,s.context_key,topic=C.get(source,c)['default_topic'])
    return s

class GraphTests(unittest.TestCase):
    def test_consistency(self):self.assertEqual(validate_graph(GRAPH,BANK),[])
    def test_every_question_has_possible_witness(self):
        for qid in C:
            with self.subTest(qid=qid):self.assertEqual(admit(C[qid],witness(qid)),'ADMIT')
    def test_pause_is_global(self):
        for qid in C:
            s=witness(qid);s.paused=True
            with self.subTest(qid=qid):self.assertEqual(admit(C[qid],s),'STOPPED')
    def test_complete_or_unhelpful_questions_skipped(self):
        for qid in C:
            s=witness(qid);s.already_answered=True
            with self.subTest(qid=qid):self.assertEqual(admit(C[qid],s),'ALREADY_ANSWERED')
            s.already_answered=False;s.useful_missing_distinction=False
            with self.subTest(qid=qid):self.assertEqual(admit(C[qid],s),'NO_USEFUL_GAP')
    def test_each_annotation_must_be_established(self):
        for qid,c in C.items():
            for flag in c['required_annotations']:
                for value in [False,None,'yes']:
                    s=witness(qid);s.annotations[flag]=value
                    with self.subTest(qid=qid,flag=flag,value=value):
                        self.assertEqual(admit(c,s),'PREREQUISITE_OR_GAP_UNESTABLISHED')
    def test_absence_blocks_body_not_generic_clarity(self):
        for qid in ['R04','M10','SIGNAL-DEPENDABILITY','SIGNAL-NOT-FOLLOWED']:
            s=witness(qid);s.annotations['bodily_reaction_reported']=False
            self.assertNotEqual(admit(C[qid],s),'ADMIT')
        self.assertEqual(admit(C['CHOICE-TIME'],witness('CHOICE-TIME')),'ADMIT')
    def test_bodily_subparts_not_conflated(self):
        s=witness('R04');s.annotations['across_choice_occurrence_missing']=False
        self.assertEqual(admit(C['R04'],s),'ADMIT')
        s.annotations['usefulness_missing']=False
        self.assertNotEqual(admit(C['R04'],s),'ADMIT')
    def test_same_context_and_current_source_required(self):
        for qid,c in C.items():
            if c['context_mode']=='self_contained':continue
            s=witness(qid);s.binding=None
            self.assertEqual(admit(c,s),'NEEDS_CONTEXT')
            s=witness(qid);s.binding=Binding('old','G09','other-scene')
            self.assertEqual(admit(c,s),'WRONG_CONTEXT')
            s.binding=Binding('old','G09',s.context_key,active=False)
            self.assertEqual(admit(c,s),'SUPERSEDED_SOURCE')
            s.binding=Binding('premise','G09',s.context_key,is_participant_source=False)
            self.assertEqual(admit(c,s),'STIMULUS_IS_NOT_ANSWER')
    def test_alternative_contexts_not_all_required(self):
        for source in ['B0','R06']:
            s=witness('MOOD-AFTER');s.binding=Binding('event',source,s.context_key,topic=C[source]['default_topic'])
            self.assertEqual(admit(C['MOOD-AFTER'],s),'ADMIT')
    def test_volunteered_equivalent_context_is_allowed(self):
        s=witness('WHY');s.binding=Binding('corrected-action','F0',s.context_key,topic='persuasion')
        self.assertEqual(admit(C['WHY'],s),'ADMIT')
        s.binding=Binding('wrong','F0',s.context_key,semantic_match=False)
        self.assertEqual(admit(C['WHY'],s),'UNVERIFIED_CONTEXT')
    def test_standalone_advisory_links_do_not_force_questions(self):
        for qid in ['A0','ROUTINE-CHANGE','OWNERSHIP','STATUS']:
            self.assertEqual(admit(C[qid],State()),'ADMIT')
    def test_declined_scope_crosses_family_boundary(self):
        for qid in ['G12','G13','R05','B0','PHYSICAL-CLOSENESS','ROMANCE-FADE']:
            s=witness(qid);s.closed_topics={'romance'}
            self.assertEqual(admit(C[qid],s),'TOPIC_CLOSED')
        s=witness('G14');s.closed_topics={'romance'}
        self.assertEqual(admit(C['G14'],s),'ADMIT')
    def test_role_substitution_requires_explicit_election(self):
        s=witness('B0');s.closed_topics={'romance'};s.selected_topic='friend_emotion'
        self.assertEqual(admit(C['B0'],s),'UNAUTHORIZED_ROLE_SUBSTITUTION')
        s.role_change_elected=True
        self.assertEqual(admit(C['B0'],s),'ADMIT')
    def test_generic_followups_inherit_private_scope(self):
        for qid in ['MOOD-AFTER','WHY']:
            s=witness(qid);s.closed_topics={'romance'}
            s.binding=Binding('partner-answer','B0',s.context_key,topic='romance')
            self.assertEqual(admit(C[qid],s),'TOPIC_CLOSED')
            s.binding=Binding('friend-answer','B0',s.context_key,topic='friend_emotion')
            self.assertEqual(admit(C[qid],s),'ADMIT')
    def test_closed_catalog_family_does_not_block_unrelated_source(self):
        s=witness('WHY');s.closed_topics={'friend_company'}
        s.binding=Binding('promise-answer','M03',s.context_key,topic='promise')
        self.assertEqual(admit(C['WHY'],s),'ADMIT')
    def test_unclassified_source_scope_not_silently_open(self):
        s=witness('MOOD-AFTER')
        s.binding=Binding('unknown-scope','B0',s.context_key)
        self.assertEqual(admit(C['MOOD-AFTER'],s),'NEEDS_SOURCE_SCOPE')
    def test_unknown_no_endless_repeat(self):
        s=witness('R04');s.repeated_unresolved_probe=True
        self.assertEqual(admit(C['R04'],s),'MOVE_ON_UNRESOLVED')
    def test_imagination_not_silently_assumed(self):
        s=State(applicable=False)
        self.assertEqual(admit(C['G12'],s),'INAPPLICABLE')
        s.imagined_explicitly_elected=True
        self.assertEqual(admit(C['G12'],s),'ADMIT')
    def test_comparison_needs_two_compatible_records(self):
        a={'answer_event':'a','active':True,'comparison_group':'meal_entry','response_task':'action','role':'self','time_frame':'current','conditions_explicit':True,'condition_key':'not-asked','declared_changed_fields':['invitation']}
        b={**a,'answer_event':'b','condition_key':'asked'}
        self.assertTrue(explicit_comparison(a,b))
        for key,val in [('answer_event',None),('active',False),('comparison_group','other'),('response_task','preferred_role'),('role','partner'),('time_frame','childhood'),('conditions_explicit',False)]:
            with self.subTest(key=key):self.assertFalse(explicit_comparison(a,{**b,key:val}))
    def test_one_message_can_supply_both_contrast_branches(self):
        a={'answer_event':'same-message','active':True,'comparison_group':'meal',
           'condition_key':'unasked','response_task':'action','role':'self',
           'time_frame':'current','conditions_explicit':True,'declared_changed_fields':['invitation']}
        b={**a,'condition_key':'asked'}
        self.assertTrue(explicit_comparison(a,b))
        self.assertFalse(explicit_comparison(a,a))
    def test_explicit_earlier_life_contrast_is_allowed(self):
        a={'answer_event':'same-message','active':True,'comparison_group':'friend-book',
           'condition_key':'current','response_task':'reply','role':'self',
           'time_frame':'current','conditions_explicit':True,'declared_changed_fields':['time_frame']}
        b={**a,'condition_key':'earlier','time_frame':'earlier'}
        self.assertTrue(explicit_comparison(a,b))
        self.assertFalse(explicit_comparison(a,{**b,'declared_changed_fields':['invitation']}))
    def test_four_graph_mutants_rejected(self):
        g=copy.deepcopy(GRAPH);g['edges'][0]['to']='q:nonexistent'
        self.assertIn('dangling_edge',validate_graph(g,BANK))
        g=copy.deepcopy(GRAPH);g['routing_contracts'][0]['targets_are_evidence']=True
        self.assertTrue(any('stimulus_credit' in e for e in validate_graph(g,BANK)))
        g=copy.deepcopy(GRAPH);next(c for c in g['routing_contracts'] if c['id']=='M02')['context_candidates']=[]
        self.assertIn('pressure_antecedent_missing',validate_graph(g,BANK))
        g=copy.deepcopy(GRAPH);g['edges'].append({'from':'q:M02','to':'q:M01','kind':'context_candidate'})
        self.assertIn('circular_prerequisite',validate_graph(g,BANK))

if __name__=='__main__':unittest.main(verbosity=2)
