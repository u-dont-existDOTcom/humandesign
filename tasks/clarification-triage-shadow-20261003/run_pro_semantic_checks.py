"""Full-bank synthetic checks. Expected answers never enter an inference packet."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
TASK=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'apps/life-patterns-participant'))
from participant.domain import import_record, load_instrument, new_state
from participant.shadow_triage import privacy_safe_case_summary, run_shadow_fast_spec_path


def main():
    cases=json.loads((TASK/'PRO-SEMANTIC-CASES-20261005.json').read_text())
    assert cases['synthetic_only'] is True
    spec=importlib.util.spec_from_file_location('pro_worker',ROOT/'apps/life-patterns-participant/scripts/gpt_review_worker.py')
    worker=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=worker
    spec.loader.exec_module(worker)
    result_path=TASK/'PRO-SEMANTIC-RESULTS-20261005.jsonl'
    trace_path=TASK/'PRO-SEMANTIC-SYNTHETIC-TRACE-20261005.jsonl'
    if result_path.exists() or trace_path.exists():
        raise SystemExit('Results already exist; refusing an unrecorded retry.')
    module=ROOT/'apps/life-patterns-participant/participant/shadow_triage.py'
    manifest={'schema':'life-patterns-pro-review-run-v1','synthetic_only':True,
              'module_sha256':hashlib.sha256(module.read_bytes()).hexdigest(),
              'case_packet_sha256':hashlib.sha256((TASK/'PRO-SEMANTIC-CASES-20261005.json').read_bytes()).hexdigest(),
              'model':'gpt-5.6-sol','effort':'xhigh','full_bank':True,'expected_targets_in_inference':False}
    (TASK/'PRO-SEMANTIC-MANIFEST-20261005.json').write_text(json.dumps(manifest,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='lp-pro-authority-') as temp:
        instrument=load_instrument(worker.authority_copy(Path(temp)))
        base_provider=worker.CodexCliProvider()
        for case in cases['cases']:
            state=new_state('pro-synthetic','gpt-5.6-sol','xhigh')
            record={'schema':'life-patterns-full-survey-participant-export-v2',
                    'collection_mode':'chatgpt_text','turns':case['turns']}
            import_record(state,record,'prior_json',instrument,'chatgpt_text')
            state.update(consent=True,phase='ready')
            assert not state.get('addressed_routes')
            trace=[]
            class SyntheticTraceProvider:
                def call(self,system,payload,schema,model,effort):
                    value,call=base_provider.call(system,payload,schema,model,effort)
                    safe_value=value.model_dump() if hasattr(value,'model_dump') else value
                    trace.append({'schema':schema.__name__,'result':safe_value})
                    # Store synthetic structured results only, never provider prompts or credentials.
                    with trace_path.open('a') as f:
                        f.write(json.dumps({'synthetic_only':True,'case_id':case['case_id'],**trace[-1]},ensure_ascii=False)+'\n')
                    return value,call
            try:
                result=run_shadow_fast_spec_path(state,instrument,SyntheticTraceProvider(),model='gpt-5.6-sol',effort='xhigh')
                row=privacy_safe_case_summary(case['case_id'],state,result)
                row['synthetic_only']=True
                row['questions']={rid:q.text for rid,q in result['final_questions'].items()}
            except Exception as exc:
                row={'case_id':case['case_id'],'synthetic_only':True,'error_type':type(exc).__name__,
                     'error':str(exc)}
            with result_path.open('a') as f:
                f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
            print(json.dumps({'case_id':case['case_id'],'outcome':row.get('shadow_outcome'),
                              'ready_routes':row.get('ready_question_route_ids'),'error_type':row.get('error_type')}),flush=True)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
