#!/usr/bin/env python3
"""Document original spouse case while rejecting unverified predictive success."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
targets=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/x).exists() for x in targets)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
L=J('CLAIM_LEDGER.json')
idx=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert idx['records_count']==4007 and idx['batches'][-1]['id']=='B03o'
assert idx['next']['chapter']=='LXX' and idx['next']['pdf_page']==449
assert idx['source_sha256']==W['original_full_pdf_sha256']
assert len(D['rows'])==45 and M['span_count']==14 and len(U['issues'])==18
keys=[r['local_id'] for r in D['rows']]
mapped=[k for s in M['source_spans'] for k in s['mapped_local_ids']]
assert sorted(mapped)==sorted(keys) and len(mapped)==45
assert all(r['chapter']=='LXX' for r in D['rows'][:-1])
assert D['rows'][-1]['chapter']=='LXXI_NAVIGATION_ONLY'
assert W['printed_chart_date']=='6 February 1644'
assert L['independently_authenticated_spouse_outcomes']==0
for im in W['original_images']:
 assert H(im['path'])==im['sha256']
rules=[]
for n,r in enumerate(D['rows'],start=4008):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
   'historical_documentary_admitted':True,
   'independently_authenticated_clinical_case':False,
   'empirical_predictive_accuracy_validated':False,
   'runtime_rule_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4008,4053))
R={'batch':'B03p','kind':'ORIGINAL_HISTORICAL_WORKED_SPOUSE_CASE_ONLY',
 'status':'LOCALLY_DOCUMENTARY_ADMITTED_PENDING_PUBLICATION',
 'documentary_accepted_locally':True,'record_count':45,'first_record':4008,
 'last_record':4052,'chapter_source_units':44,'navigation_only_units':1,
 'original_pdf_pages':[449,450,451],'source_passages':14,'source_limits':18,
 'source_author_reported_outcome_cases':1,
 'source_reported_forecast_window':'late September or beginning October',
 'source_reported_forecast_alternatives':'death OR serious danger',
 'source_reported_event_day':'8 October',
 'independently_validated_historical_cases':0,
 'empirically_validated_predictive_cases':0,
 'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
ids={r['local_id']:r['id'] for r in rules}
MAP={'batch':'B03p','status':'LOCAL_DOCUMENTARY_ACCEPTED_ORIGINAL_TO_RECORD_MAP',
 'source_spans':[{**s,'canonical_record_ids':[ids[k] for k in s['mapped_local_ids']]} for s in M['source_spans']],
 'span_count':14,'mapped_records':45}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',MAP)
dump('SOURCE_ORDER.json',{'batch':'B03p','records_count':45,
 'records':[{'record_number':r['record_number'],'pdf_pages':r['original_pdf_pages']} for r in rules]})
U['status']='RETAINED_AT_LOCAL_SOURCE_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03p','status':'LOCAL_DOCUMENTARY_ACCEPTED_PENDING_GITHUB',
 'previous_lilly':4007,'new_documentary_records':45,
 'first_record':'R4008','last_record':'R4052',
 'lilly_if_published':4052,'ptolemy':1066,'combined_if_published':5118,
 'source_spans':14,'source_uncertainties':18,'next_chapter':'LXXI','next_pdf_page':451,
 'original_pdf_sha256':W['original_full_pdf_sha256'],
 'historical_author_reported_cases':1,'independently_authenticated_cases':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'remote_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
 ('UNRESOLVED.json','limits_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'accepted_locally':45,'lilly_if_published':4052,'combined':5118,
 'empirical_validations':0}))
