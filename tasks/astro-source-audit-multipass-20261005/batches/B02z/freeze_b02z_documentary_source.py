#!/usr/bin/env python3
"""Admit documented source-only B02z from frozen earlier provisional draft.
Prior provisional records and their baseline remain historically unchanged.
"""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=lambda p:json.loads((B/p).read_text(encoding='utf-8'))
dump=lambda f,o:(B/f).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
new=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
     'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','ACCEPTANCE.json']
assert not any((B/k).exists() for k in new),'Do not overwrite an admitted source'
D=j('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=j('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=j('SOURCE_WINDOW_MANIFEST.json')
U=j('UNRESOLVED_SOURCE_LIMITS.json')
L=j('CLAIM_LEDGER.json')
IDX=json.loads((B.parents[3]/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert IDX['records_count']==3147 and IDX['batches'][-1]['id']=='B02y'
assert IDX['next']['chapter']=='LIV' and IDX['next']['pdf_page']==410
assert W['original_full_pdf_sha256']==IDX['source_sha256']
assert D['record_count']==24 and C['span_count']==16 and len(U['issues'])==14
assert [x['local_id'] for x in D['rows']]==[f'LIV-C{i:03}' for i in range(1,25)]
assert len(D['rows'])==24 and D['rows'][-1]['record_role']=='boundary'
mapped=[k for s in C['source_spans'] for k in s['draft_local_ids']]
assert sorted(mapped)==sorted(r['local_id'] for r in D['rows']) and len(mapped)==24
for x in W['images']:
 assert sha(B/x['path'])==x['sha256'] and (B/x['path']).stat().st_size==x['size_bytes']
assert L['globally_accepted_new_documentary_units']==0
rules=[]
for n, r in enumerate(D['rows'],start=3148):
 rr={**r,'id':f'R{n}','record_number':n,'global_record_number':n,
 'is_provisional':False,'accepted_historical_documentary':True,
 'source_record_admitted_for_documentary_reference':True,
 'accepted_as_empirical_prediction':False,
 'empirically_verified_case':False,'model_runtime_promotion':False,
 'safe_for_real_person_prognosis':False}
 rules.append(rr)
assert [x['record_number'] for x in rules]==list(range(3148,3172))
assert sum(x['chapter']=='LIV' for x in rules)==23
assert rules[-1]['chapter']=='LV_HEADING_NAVIGATION_ONLY'
R={'batch':'B02z','kind':'HISTORICAL_SOURCE_DOCUMENTARY_ONLY',
'status':'CHAPTER_LIV_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_PUBLICATION',
'documentary_accepted_locally':True,'whole_chapter_liv_source_intake_complete':True,
'source_pdf_sha256':W['original_full_pdf_sha256'],
'first_record':3148,'last_record':3171,'record_count':24,
'substantive_chapter_liv_units':23,'next_chapter_navigation_only_units':1,
'source_reverse_passages':16,'source_uncertainties_retained':14,
'blind_independent_diplomatic_second_transcription':False,
'accepted_as_empirical_astro_prediction':False,
'authenticated_market_cases':0,'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
by_id={r['local_id']:r['id'] for r in rules}
M={'batch':'B02z','status':'LOCALLY_ADMITTED_ORIGINAL_SOURCE_REVERSE_MAP',
'source_spans':[{**s,'canonical_record_ids':[by_id[k] for k in s['draft_local_ids']],
'documentary_image_source_admitted_locally':True} for s in C['source_spans']],
'span_count':16,'mapped_unique_documentary_units':24,
'independent_blind_original_transcription_done':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M)
S={'batch':'B02z','status':'LOCALLY_ADMITTED_SOURCE_ORDER',
'original_source_pages':[410,411],'opening':'PDF410 BELOW LIII divider',
'closing':'PDF411 ABOVE LV divider','first_record':3148,'last_record':3171,
'record_count':24,'source_spans':16,
'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
'records':[{'record_number':r['record_number'],'pdf_pages':r['original_pdf_pages'],
'kind':r['record_role']} for r in rules],'empirical_evidence_counted':0}
dump('SOURCE_ORDER.json',S)
U['status']='RETAINED_AT_LOCAL_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B02z','status':'CHAPTER_LIV_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_RELEASE_AND_GIT_PUBLICATION',
'kind':'HISTORICAL_SOURCE_DOCUMENTARY_ONLY','documentary_accepted_locally':True,
'whole_chapter_liv_complete_at_documentary_source_level':True,
'original_full_pdf_sha256':W['original_full_pdf_sha256'],
'previous_accepted_lilly':3147,'new_documentary_records':24,
'first_record':'R3148','last_record':'R3171',
'lilly_if_published':3171,'ptolemy_retained':1066,'combined_if_published':4237,
'original_source_reverse_spans':16,'source_uncertainties_retained':14,
'cross_page_unit_count':sum(len(r['original_pdf_pages'])>1 for r in rules),
'fully_diplomatic_second_reader_done':False,
'new_empirical_astro_validations':0,'real_market_transactions_authenticated':0,
'runtime_promotions':0,'canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),
('SOURCE_ORDER.json','source_order_sha256'),
('UNRESOLVED.json','unresolved_sha256'),
('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','original_to_record_source_map_sha256'),
('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','source_audit_sha256')]:
 A[k]=sha(B/f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B02z','status':A['status'],
    'locally_added':24,'lilly_if_published':3171,
    'combined_if_published':4237,'empirical':0,'sha256':A['rules_sha256']}))
