#!/usr/bin/env python3
"""Document original 1647 dream source, without validating any dream prediction."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
new=['RULES.json','ACCEPTANCE.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in new)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
index=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert index['records_count']==4446 and index['batches'][-1]['id']=='B03v'
assert index['next']['chapter']=='LXXVII' and index['next']['pdf_page']==468
assert index['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==38 and M['span_count']==8 and len(U['issues'])==15
ids=[r['source_local_id'] for r in D['rows']]
mapped=[x for s in M['source_spans'] for x in s['mapped_local_ids']]
assert len(ids)==len(mapped)==38 and sorted(ids)==sorted(mapped)
byid={r['source_local_id']:r for r in D['rows']}
assert all(s['original_pdf_pages']==byid[k]['original_pdf_pages'] for s in M['source_spans'] for k in s['mapped_local_ids'])
assert all(r['chapter']=='LXXVII' for r in D['rows'][:-2])
assert all(r['chapter']=='LXXVIII_NAVIGATION_ONLY' for r in D['rows'][-2:])
assert C['independently_authenticated_dream_events']==0
assert C['independently_validated_predictive_outcomes']==0
for im in W['original_images']:
 assert H(im['path'])==im['sha256']
 assert (B/im['path']).stat().st_size==im['bytes']
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').exists()
rules=[]
for n,r in enumerate(D['rows'],start=4447):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_accepted':True,
  'accepted_for_primary_historical_text_reference':True,
  'independently_authenticated_dream_case':False,
  'empirically_validated_prediction':False,'runtime_model_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4447,4485))
R={'batch':'B03w','kind':'ORIGINAL_1647_HISTORICAL_DREAM_INTERPRETATION_ONLY',
 'status':'HISTORICAL_SOURCE_ACCEPTED_LOCALLY_PENDING_RELEASE',
 'documentary_accepted_locally':True,'record_count':38,
 'first_record':4447,'last_record':4484,
 'substantive_lxxvii_source_annotations':36,'next_heading_navigation_only':2,
 'original_pdf_pages':[468,469,470],'source_reverse_passages':8,
 'unresolved_source_issues':15,'independently_verified_dream_outcomes':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
ids_global={r['source_local_id']:r['id'] for r in rules}
reverse={'batch':'B03w','status':'ORIGINAL_DOCUMENTARY_REVERSE_MAPPING_ACCEPTED_LOCAL',
 'source_spans':[{**s,'accepted_global_record_ids':[ids_global[k] for k in s['mapped_local_ids']]}
  for s in M['source_spans']],'span_count':8,'mapped_source_records':38}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',reverse)
dump('SOURCE_ORDER.json',{'batch':'B03w','status':'LOCAL_HISTORICAL_SOURCE_ORDER',
 'first_record':4447,'last_record':4484,'record_count':38,
 'original_pdf_pages':[468,469,470],
 'records':[{'record_number':r['record_number'],'pdf_pages':r['original_pdf_pages'],'role':r['role']} for r in rules],
 'new_empirical_results':0})
U['status']='SOURCE_LIMITS_RETAINED_AT_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03w','kind':'SOURCE_HISTORICAL_DREAMS_NOT_EMPIRICAL',
 'status':'LOCAL_DOCUMENTARY_SOURCE_ADMITTED_PENDING_ARCHIVE_AND_GITHUB',
 'documentary_accepted_locally':True,'prior_lilly_accepted':4446,
 'new_documentary_records':38,'first_record':'R4447','last_record':'R4484',
 'lilly_if_published':4484,'ptolemy_retained':1066,'combined_if_published':5550,
 'source_original_pdf_sha256':W['original_full_pdf_sha256'],
 'source_reverse_passages':8,'original_unresolved_limits':15,
 'original_body_pdf_pages':[468,469],'next_chapter':'LXXVIII','next_original_pdf':470,
 'separate_worked_case_date':'26 January 1648','separate_worked_case_time':'9:27 AM',
 'independently_verified_dream_outcomes':0,
 'new_empirically_validated_predictions':0,'runtime_model_promotions':0,
 'original_full_independent_second_diplomatic_transcription':False,
 'remote_canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03w','documentary_locally_admitted':38,
 'lilly_if_published':4484,'combined_if_published':5550,
 'source_spans':8,'unresolved_limits':15,'empirical_validations':0}))
