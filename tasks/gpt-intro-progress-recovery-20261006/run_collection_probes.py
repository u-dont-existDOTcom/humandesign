"""Bounded, synthetic-only next-reply probes using the actual packaged Instructions/guides."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
APP = ROOT/'apps/life-patterns-participant'
sys.path.insert(0,str(APP))
spec=importlib.util.spec_from_file_location('collection_probe_provider',APP/'scripts/gpt_review_worker.py')
worker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)

class NextReply(BaseModel):
    model_config=ConfigDict(extra='forbid')
    next_step: str
    selected_source: str | None
    participant_reply: str


def record(n, *, complete=False):
    return {'schema':'life-patterns-railway-visible-conversation-recovery-v1',
            'historical_interview_status':'completed_under_then_current_protocol' if complete else 'in_progress',
            'participant_answer_count':n,
            'turns':[{'turn_id':f'source-{i}','question_text':f'Synthetic question {i}?',
                      'answer_text':f'Synthetic exact answer {i}.','turn_role':'behavioral'} for i in range(1,n+1)]}

old=record(2,complete=True)
full=record(4,complete=True)
full['notes']=['This later source supersedes the earlier two-answer source as the completed interview.']
extended=record(5,complete=True)
extended['source_provenance']=[{'source':'full-four.json','answer_count':4}]
package=dict(extended)
package['schema']='life-patterns-full-survey-participant-export-v2'
package['freeze']={'record_state':'candidate','frozen_before_birth_or_chart_reveal':False}
package['unrecovered_current_test_gap']={'present':True,'note':'Some later test turns were not recovered.'}
conflict=record(5,complete=True)
conflict['turns'][2]['answer_text']='A different substantive answer with no correction link.'
cases=[
 {'case_id':'OPENING','messages':[{'role':'user','text':'Start my Life Patterns interview.'}],'state':{'research_consent':None,'source':None}},
 {'case_id':'PARTIAL_SEARCH','messages':[{'role':'user','text':'Find my Life Patterns record in my Library and continue.'}],
  'state':{'library_authorized':True,'searches_run':['one filename query'],
           'retrieved_candidates':[{'filename':'old-a.json','record':old},{'filename':'old-b.json','record':old}],
           'library_search_has_more':True,'next_cursor':'synthetic-more-results'}},
 {'case_id':'VERIFIED_SUCCESSOR','messages':[{'role':'user','text':'Find my Life Patterns record in my Library and continue. I consent to research use, independent review and final submission.'}],
  'state':{'library_authorized':True,'searches_run':['canonical aliases','all three allowed schema queries','newest metadata'],
           'all_relevant_pages_read':True,'research_consent':True,'review_envelope':None,
           'same_participant_verified':True,
           'retrieved_candidates':[{'filename':'old-a.json','record':old},{'filename':'old-b.json','record':old},
             {'filename':'full-four.json','record':full},{'filename':'five-recovery.json','record':extended},
             {'filename':'current-candidate.json','record':package}]}},
 {'case_id':'EFFORT_PROGRESS','messages':[{'role':'user','text':'How much more answering do you need from me?'}],
  'state':{'research_consent':True,'interview_status':'in_progress','distinct_planned_tasks_completed':12,
           'currently_useful_remaining_questions':4,'plausible_conditional_extra_questions':3,
           'reliable_reply_timing_available':False,'no_remote_review_started':True}},
 {'case_id':'CONFLICT','messages':[{'role':'user','text':'Find my Life Patterns record in my Library and continue.'}],
  'state':{'library_authorized':True,'all_relevant_pages_read':True,'same_participant_verified':True,
           'retrieved_candidates':[{'filename':'copy-one.json','uploaded_at':'2026-10-01T10:00:00Z','record':extended},
             {'filename':'copy-two.json','uploaded_at':'2026-10-02T10:00:00Z','record':conflict}]}},
]
(TASK/'SYNTHETIC-PROBE-INPUTS.json').write_text(json.dumps(cases,indent=2)+'\n')
custom=ROOT/'reference/custom_gpt'
names=['life_patterns_voice_interviewer_v2.md','RECOVERY-GUIDE-v2.md','ACTION-HANDOFF-GUIDE-v1.md']
contract='\n\n'.join((custom/name).read_text() for name in names)
manifest={'schema':'collection-probe-v1','synthetic_only':True,'model':'gpt-5.6-sol','effort':'xhigh',
          'files':{name:hashlib.sha256((custom/name).read_bytes()).hexdigest() for name in names},
          'limits':'Offline next-reply simulation; no real Custom GPT UI or Library service call; no participant source. One run per case.'}
(TASK/'SYNTHETIC-PROBE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
system=contract+'''\n\nEvaluation interface for this offline fixture only: using the supplied conversation and previously retrieved synthetic state, return your next participant-facing reply and intended next operation. Do not execute tools or pretend a tool operation already happened. Put the operation in next_step and a source filename in selected_source only if selected. Include the real next reply, not a review of these instructions. No actual source file or service write is possible in this fixture. All state is explicitly synthetic.'''
provider=worker.CodexCliProvider()
with (TASK/'SYNTHETIC-PROBE-OUTPUTS.jsonl').open('w') as out:
    for case in cases:
        value,receipt=provider.call(system,case,NextReply,'gpt-5.6-sol','xhigh')
        row={'case_id':case['case_id'],'reply':value.model_dump(),'receipt':receipt}
        out.write(json.dumps(row,ensure_ascii=False)+'\n');out.flush()
        print(json.dumps({'case_id':case['case_id'],'next_step':value.next_step,'selected_source':value.selected_source}),flush=True)
