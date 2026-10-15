#!/usr/bin/env python3
"""Original Lilly 1647 Chapter LXIII historical documentary admission."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text())
sha=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
outputs=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','ACCEPTANCE.json']
assert not any((B/n).exists() for n in outputs)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
P=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_FIRST_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
idx=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert idx['records_count']==3527 and idx['batches'][-1]['id']=='B03h'
assert idx['next']['chapter']=='LXIII' and idx['next']['pdf_page']==428
assert idx['source_sha256']==W['original_pdf_sha256']
assert D['source_units']==44 and P['span_count']==15 and len(U['issues'])==16
keys=[r['local_id'] for r in D['rows']]
mapped=[k for s in P['source_spans'] for k in s['mapped_local_ids']]
assert sorted(keys)==sorted(mapped) and len(mapped)==44
assert W['next_heading_exact_original_roman']=='LIV' and W['next_heading_logical_chapter']=='LXIV'
for im in W['original_page_images']:
 assert sha(im['path'])==im['sha256']
 assert (B/im['path']).stat().st_size==im['bytes']
assert D['rows'][-1]['chapter']=='NEXT_PRINTED_LIV_FISH_STOLEN_NAVIGATION_ONLY'
rules=[]
for n,r in enumerate(D['rows'],start=3528):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_admitted':True,'empirically_validated_thief_or_case':False,
  'accepted_as_empirical_prediction':False})
assert [r['record_number'] for r in rules]==list(range(3528,3572))
assert all(r['chapter']=='LXIII' for r in rules[:-1])
R={'batch':'B03i','kind':'ORIGINAL_THEFT_SOURCE_HISTORICAL_ONLY',
 'status':'CHAPTER_LXIII_LOCALLY_SOURCE_ADMITTED_PENDING_REMOTE',
 'documentary_accepted_locally':True,'record_count':44,
 'first_record':3528,'last_record':3571,'source_reverse_spans':15,
 'unresolved_source_issues':16,'chapter_lxiii_units':43,'next_heading_only':1,
 'next_original_printed_heading':'CHAP. LIV. Fish Stolen',
 'next_sequential_chapter':'LXIV',
 'author_reported_money_recovery_cases':1,
 'independent_thief_convictions_verified':0,
 'independent_documented_money_recovery_cases':0,
 'empirical_astrology_predictions_validated':0,'runtime_promotions':0,
 'full_independent_diplomatic_second_reading':False,'rules':rules}
dump('RULES.json',R)
ids={r['local_id']:r['id'] for r in rules}
M={'batch':'B03i','status':'LOCAL_DOCUMENTARY_ORIGINAL_IMAGE_REVERSE_SOURCE_MAP',
 'source_spans':[{**s,'accepted_global_record_ids':[ids[k] for k in s['mapped_local_ids']]}
   for s in P['source_spans']],
 'span_count':15,'mapped_unique_accepted_records':44,
 'printed_heading_anomaly_preserved':True}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M)
S={'batch':'B03i','status':'LOCALLY_ADMITTED_ORIGINAL_SOURCE_ORDER',
 'original_pdf_body_pages':[428,429,430],
 'following_heading_pdf':431,'following_heading_literal_roman':'LIV',
 'record_count':44,'first_record':3528,'last_record':3571,
 'source_reverse_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'record_number':r['record_number'],
  'original_pdf_pages':r['original_pdf_pages'],'role':r['role']} for r in rules]}
dump('SOURCE_ORDER.json',S)
U['status']='RETAINED_AT_DOCUMENTARY_SOURCE_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03i','kind':'SOURCE_HISTORICAL_CASE_NOT_EMPIRICAL_VALIDATION',
 'status':'CHAPTER_LXIII_LOCALLY_ACCEPTED_HISTORICAL_DOCUMENTATION_PENDING_GITHUB',
 'documentary_accepted_locally':True,'previous_accepted_lilly':3527,
 'new_documentary_records':44,'first_record':'R3528','last_record':'R3571',
 'lilly_if_published':3571,'ptolemy_retained':1066,'combined_if_published':4637,
 'source_reverse_spans':15,'unresolved_source_issues':16,
 'original_pdf_body_pages':[428,429,430],'next_heading_pdf':431,
 'next_heading_printed':'CHAP. LIV. Fish Stolen',
 'next_heading_sequential':'LXIV',
 'source_full_pdf_sha256':W['original_pdf_sha256'],
 'author_reported_money_recovery_cases':1,
 'independent_authentication_of_theft_outcome':0,
 'independent_authentication_of_thief_identity':0,
 'new_empirical_predictions_validated':0,'runtime_promotions':0,
 'second_diplomatic_original_reader':False,'remote_published':False}
for f,k in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('LXIII_SOURCE_FIRST_BOUNDARY_AUDIT_20261015.md','source_audit_sha256')]:
 A[k]=sha(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03i','local_documentary_source_units':44,
 'accepted_if_published_lilly':3571,'combined_if_published':4637,
 'new_empirical_validation':0,'rules_sha256':A['rules_sha256']}))
