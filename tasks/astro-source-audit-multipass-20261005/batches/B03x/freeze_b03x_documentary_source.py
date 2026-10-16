#!/usr/bin/env python3
"""Guarded local documentary admission of original Lilly 1647 LXXVIII."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert not any((B/f).exists() for f in ('RULES.json','ACCEPTANCE.json','SOURCE_ORDER.json','UNRESOLVED.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json'))
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json');M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json');U=J('UNRESOLVED_SOURCE_LIMITS.json');C=J('CLAIM_LEDGER.json')
assert I['records_count']==4484 and I['batches'][-1]['id']=='B03w' and I['next']['chapter']=='LXXVIII'
assert I['source_sha256']==W['original_full_pdf_sha256'] and I['next']['pdf_page']==470
assert D['source_units']==24 and M['span_count']==6 and len(U['issues'])==14
assert C['independently_validated_predictions']==C['independently_authenticated_case_outcomes']==C['runtime_promotions']==0
for a in W['original_images']:
 assert H(a['path'])==a['sha256'] and (B/a['path']).stat().st_size==a['bytes']
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').is_file()
local={r['source_local_id'] for r in D['rows']}
mapped=[k for s in M['source_spans'] for k in s['mapped_local_ids']]
assert len(local)==len(mapped)==24 and local==set(mapped)
assert all(r['chapter']=='LXXVIII' for r in D['rows'][:-2])
assert all(r['chapter']=='LXXIX_NAVIGATION_ONLY' for r in D['rows'][-2:])
rs=[{**r,'id':f'R{i}','record_number':i,'global_record_number':i,
 'historical_documentary_accepted':True,'accepted_for_primary_historical_text_reference':True,
 'independently_authenticated_dream_case':False,'empirically_validated_prediction':False,
 'runtime_model_promoted':False} for i,r in enumerate(D['rows'],start=4485)]
assert [r['record_number'] for r in rs]==list(range(4485,4509))
dump('RULES.json',{'batch':'B03x','kind':'HISTORICAL_RETROSPECTIVE_DREAM_CASE_NOT_EMPIRICAL',
 'status':'LOCALLY_ACCEPTED_PENDING_GITHUB','documentary_accepted_locally':True,
 'record_count':24,'first_record':4485,'last_record':4508,'substantive_lxxviii_source_annotations':22,
 'next_heading_navigation_only':2,'source_reverse_passages':6,'unresolved_source_issues':14,
 'authorial_unverified_success_reports':1,'independently_verified_dream_outcomes':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'original_pdf_pages':[470,471],'rules':rs})
by={r['source_local_id']:r['id'] for r in rs}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',{'batch':'B03x',
 'source_spans':[{**s,'accepted_global_record_ids':[by[k] for k in s['mapped_local_ids']]} for s in M['source_spans']],
 'span_count':6,'mapped_source_records':24})
dump('SOURCE_ORDER.json',{'batch':'B03x','first_record':4485,'last_record':4508,'record_count':24,
 'original_pdf_pages':[470,471],
 'records':[{'record_number':r['record_number'],'role':r['role'],
             'pdf_pages':r['original_pdf_pages']} for r in rs],
 'independent_empirical_results':0})
U['status']='UNRESOLVED_SOURCE_LIMITS_RETAINED_AT_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03x','kind':'RETROSPECTIVE_AUTHORIAL_DREAM_CASE_HISTORICAL_ONLY',
 'status':'LOCAL_DOCUMENTARY_ADMITTED_PENDING_RELEASE_AND_GITHUB','documentary_accepted_locally':True,
 'prior_lilly_accepted':4484,'new_documentary_records':24,
 'first_record':'R4485','last_record':'R4508','lilly_if_published':4508,
 'ptolemy_retained':1066,'combined_if_published':5574,
 'original_pdf_sha256':W['original_full_pdf_sha256'],'original_pdf_pages':[470,471],
 'source_reverse_passages':6,'retained_source_limitations':14,'next_chapter':'LXXIX',
 'next_original_pdf':471,'authorial_unverified_success_reports':1,
 'independently_verified_dream_outcomes':0,'new_empirically_validated_predictions':0,
 'runtime_model_promotions':0,'independent_second_diplomatic_transcription':False,
 'remote_canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03x','locally_admitted_source_annotations':24,
 'lilly_if_published':4508,'combined_if_published':5574,
 'authorial_self_reported_success':1,'independent_validations':0}))
