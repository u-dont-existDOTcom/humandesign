#!/usr/bin/env python3
"""Admit original historical Chapter LXXI source; no real outcome validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
assert not any((B/n).exists() for n in ['RULES.json','ACCEPTANCE.json','SOURCE_ORDER.json'])
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert I['records_count']==4052 and I['batches'][-1]['id']=='B03p'
assert I['next']['chapter']=='LXXI' and I['next']['pdf_page']==451
assert I['source_sha256']==W['original_pdf_sha256']
assert len(D['rows'])==41 and len(M['source_spans'])==10 and len(U['issues'])==18
keys=[r['source_local_id'] for r in D['rows']]
mapped=[k for s in M['source_spans'] for k in s['mapped_local_ids']]
assert len(mapped)==41 and sorted(mapped)==sorted(keys)
assert all(r['chapter']=='LXXI' for r in D['rows'][:-1])
assert D['rows'][-1]['chapter']=='LXXII_NAVIGATION_ONLY'
for im in W['original_images']:
 assert H(im['path'])==im['sha256']
assert C['early_false_rumor_author_reports']==C['later_reliable_news_author_reports']==C['later_person_return_author_reports']==1
assert C['independent_outcomes_verified']==0
rules=[]
for n,r in enumerate(D['rows'],start=4053):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
   'documentary_accepted':True,'independently_authenticated_return_case':False,
   'empirical_prediction_validated':False,'runtime_rule_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4053,4094))
R={'batch':'B03q','kind':'HISTORICAL_SOURCE_REPORTED_MISSING_HUSBAND_ONLY',
 'status':'DOCUMENTARY_LOCALLY_ACCEPTED','documentary_accepted_locally':True,
 'record_count':41,'first_record':4053,'last_record':4093,
 'chapter_source_units':40,'next_heading_only':1,'source_spans':10,
 'unresolved_limits':18,'reported_false_early_rumors':1,
 'reported_later_news':1,'reported_delayed_returns':1,
 'independently_verified_outcomes':0,'empirical_predictions_validated':0,
 'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
idmap={r['source_local_id']:r['id'] for r in rules}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',{'batch':'B03q',
 'source_spans':[{**s,'canonical_record_ids':[idmap[k] for k in s['mapped_local_ids']]} for s in M['source_spans']],
 'span_count':10,'mapped_unique_documentary_units':41})
dump('SOURCE_ORDER.json',{'batch':'B03q','first_record':4053,'last_record':4093,
 'original_pdf_pages':[451,452,453],'records':[{'id':r['id'],'pages':r['original_pdf_pages']} for r in rules]})
U['status']='RETAINED_AFTER_LOCAL_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03q','kind':'SOURCE_DOCUMENTARY_NO_EMPIRICAL_RETURN_VALIDATION',
 'status':'LOCAL_SOURCE_ACCEPTED_PENDING_ARCHIVE_PUBLICATION',
 'documentary_accepted_locally':True,'prior_lilly':4052,
 'new_documentary_records':41,'first_record':'R4053','last_record':'R4093',
 'lilly_if_published':4093,'ptolemy_retained':1066,
 'combined_if_published':5159,'source_spans':10,'source_issues':18,
 'next_chapter':'LXXII','next_original_pdf':453,
 'source_full_pdf_sha256':W['original_pdf_sha256'],
 'author_reported_first_false_rumor':1,
 'author_reported_may_news':1,'author_reported_july_return':1,
 'independent_verified_outcomes':0,'empirically_validated_predictions':0,
 'runtime_promotions':0,'remote_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
 ('UNRESOLVED.json','uncertainties_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03q','accepted_locally':41,'lilly_if_published':4093,'combined_if_published':5159}))
