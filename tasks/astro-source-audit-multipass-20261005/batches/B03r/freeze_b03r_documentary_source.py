#!/usr/bin/env python3
"""Original Lilly LXXII historical source admission; independently known event ≠ verified forecast."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
new=['RULES.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
     'SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json']
assert not any((B/f).exists() for f in new)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
idx=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert idx['records_count']==4093 and idx['batches'][-1]['id']=='B03q'
assert idx['next']['chapter']=='LXXII' and idx['next']['pdf_page']==453
assert idx['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==43 and M['span_count']==11 and len(U['issues'])==18
ids=[r['source_local_id'] for r in D['rows']]
mapped=[k for s in M['source_spans'] for k in s['mapped_source_local_ids']]
assert len(mapped)==43 and sorted(mapped)==sorted(ids)
assert all(r['chapter']=='LXXII' for r in D['rows'][:-1])
assert D['rows'][-1]['chapter']=='LXXIII_NAVIGATION_ONLY'
assert sum(r['historical_execution_event_verified_independently'] for r in D['rows'])==2
assert not any(r['prospective_astrology_prediction_validated'] for r in D['rows'])
assert C['independently_authenticated_prior_forecasts']==0
assert C['independently_confirmed_historical_events']==1
for v in W['original_images']:
 assert H(v['path'])==v['sha256'] and (B/v['path']).stat().st_size==v['bytes']
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').exists()
rules=[]
for n,r in enumerate(D['rows'],start=4094):
 rules.append({**r,'id':f'R{n}','record_number':n,
   'global_record_number':n,'historical_documentary_accepted':True,
   'accepted_as_historical_source_reference':True,
   'prospective_astrology_prediction_validated':False,'runtime_rule_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4094,4137))
R={'batch':'B03r','kind':'LILLY1647_CANTERBURY_HISTORICAL_CASE_ONLY',
 'status':'LOCAL_DOCUMENTARY_SOURCE_ADMISSION_PENDING_RELEASE',
 'documentary_accepted_locally':True,'record_count':43,
 'first_record':4094,'last_record':4136,
 'chapter_source_units':42,'next_heading_only':1,
 'source_original_pdf_pages':[453,454,455],
 'source_visual_passages':11,'source_limitations':18,
 'independent_historical_execution_event_confirmed':1,
 'independent_prospective_astro_forecasts_verified':0,
 'source_author_reported_forecast':'not hanged; other noble mode; six or seven weeks or thereabouts',
 'source_author_reported_event':'beheaded about 10 January following',
 'actual_external_event_date':'10 January 1645',
 'elapsed_days_from_chart_to_actual_event':38,
 'strict_six_week_lower_bound_days':42,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'full_blind_second_source_transcription_done':False,'rules':rules}
dump('RULES.json',R)
mapping={r['source_local_id']:r['id'] for r in rules}
reverse={'batch':'B03r','status':'LOCAL_DOCUMENTARY_ADMITTED_PRIMARY_IMAGE_REVERSE_MAP',
 'source_spans':[{**sp,'accepted_record_ids':[mapping[k] for k in sp['mapped_source_local_ids']]}
  for sp in M['source_spans']],
 'span_count':11,'mapped_accepted_records':43}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',reverse)
dump('SOURCE_ORDER.json',{'batch':'B03r','status':'LOCAL_HISTORICAL_SOURCE_ORDER',
 'first_record':4094,'last_record':4136,'record_count':43,
 'original_pdf_pages':[453,454,455],
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
  'role':r['role']} for r in rules]})
U['status']='RETAINED_AT_DOCUMENTARY_SOURCE_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03r','status':'LOCAL_HISTORICAL_SOURCE_ADMITTED',
 'previous_lilly':4093,'new_documentary_records':43,
 'lilly_if_published':4136,'ptolemy':1066,'combined_if_published':5202,
 'source_passages':11,'source_uncertainties':18,
 'next_chapter':'LXXIII','next_pdf':455,
 'independent_event_confirmed':True,'independent_forecast_confirmed':False,
 'empirically_validated_predictions':0,'runtime_promotions':0,
 'remote_published':False}
for f,key in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','order_sha256'),
 ('UNRESOLVED.json','limits_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','audit_sha256')]:
 A[key]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03r','locally_admitted':43,'combined_if_published':5202,
 'independent_event':True,'verified_prediction':False}))
