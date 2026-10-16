#!/usr/bin/env python3
"""Admit original Lilly 1647 Book II LXXIII documentary source, no predictive case promotion."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
out=['RULES.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','UNRESOLVED.json',
 'SOURCE_ORDER.json','ACCEPTANCE.json']
assert not any((B/x).exists() for x in out),'Refuse overwrite frozen admission'
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
INDEX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
j=json.loads(INDEX.read_text(encoding='utf-8'))
assert j['records_count']==4136 and j['batches'][-1]['id']=='B03r'
assert j['next']['chapter']=='LXXIII' and j['next']['pdf_page']==455
assert j['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==34 and M['span_count']==10 and len(U['issues'])==17
ids=[r['source_local_id'] for r in D['rows']]
mapped=[x for sp in M['source_spans'] for x in sp['mapped_source_local_ids']]
assert len(ids)==len(mapped)==34 and sorted(ids)==sorted(mapped)
assert all(r['chapter']=='LXXIII' for r in D['rows'][:-2])
assert all(r['chapter']=='LXXIV_NAVIGATION_ONLY' for r in D['rows'][-2:])
assert C['separately_verified_paid_portion_cases']==0
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').is_file()
for im in W['original_images']:
 assert H(im['path'])==im['sha256'] and (B/im['path']).stat().st_size==im['bytes']
rules=[]
for num,row in enumerate(D['rows'],start=4137):
 rules.append({**row,'id':f'R{num}','record_number':num,
  'global_record_number':num,'historical_documentary_admitted':True,
  'documentary_reference_accepted':True,
  'independent_payment_outcome_verified':False,
  'empirically_validated_prediction':False,'runtime_rule_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4137,4171))
R={'batch':'B03s','kind':'HISTORICAL_PROMISED_PORTION_CASE_SOURCE_ONLY',
 'status':'LOCAL_DOCUMENTARY_ACCEPTED_PENDING_RELEASE_GITHUB',
 'documentary_accepted_locally':True,'record_count':34,
 'first_record':4137,'last_record':4170,'substantive_chapter_units':32,
 'next_chapter_navigation_units':2,'original_pdf_pages':[455,456],
 'visual_source_spans':10,'unresolved_source_issues':17,
 'author_reported_general_success_claims':1,
 'independently_verified_paid_portion_outcomes':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
by_local={r['source_local_id']:r['id'] for r in rules}
REV={'batch':'B03s','status':'LOCALLY_ACCEPTED_ORIGINAL_TO_GLOBAL_REVERSE_MAP',
 'source_spans':[{**sp,'canonical_record_ids':[by_local[k] for k in sp['mapped_source_local_ids']]}
                  for sp in M['source_spans']],
 'span_count':10,'unique_accepted_source_records':34}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',REV)
dump('SOURCE_ORDER.json',{'batch':'B03s','status':'LOCALLY_ADMITTED_ORIGINAL_PAGE_ORDER',
 'first_record':4137,'last_record':4170,'record_count':34,'original_pdf_pages':[455,456],
 'records':[{'record_number':r['record_number'],'pdf_pages':r['original_pdf_pages'],
  'role':r['role']} for r in rules],'independently_verified_cases':0})
U['status']='RETAINED_AT_DOCUMENTARY_ADMISSION';dump('UNRESOLVED.json',U)
A={'batch':'B03s','status':'HISTORICAL_SOURCE_LOCALLY_ACCEPTED_NOT_REMOTELY_PUBLISHED',
 'documentary_accepted_locally':True,'prior_accepted_lilly':4136,
 'new_documentary_records':34,'first_record':'R4137','last_record':'R4170',
 'lilly_if_published':4170,'ptolemy_retained':1066,'combined_if_published':5236,
 'original_image_source_spans':10,'unresolved_source_issues':17,
 'original_pdf_sha256':W['original_full_pdf_sha256'],
 'original_chart_date':'13 July 1634','original_chart_time':'6:15 PM',
 'next_chapter':'LXXIV','next_original_pdf_page':456,
 'independently_verified_dowry_receipts':0,'new_empirical_predictions':0,
 'runtime_model_promotions':0,'full_independent_diplomatic_transcription':False,
 'remotely_published':False}
for f,key in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_review_sha256')]:A[key]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'new_local_source_records':34,'new_lilly_if_published':4170,
 'combined_if_published':5236,'independent_payment_events':0,
 'reverse_source_spans':10,'source_issues':17}))
