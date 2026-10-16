#!/usr/bin/env python3
"""Freeze original 1647 Lilly LXIX historical-source documentary units."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
new=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in new)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
idx=json.loads(IDX.read_text())
assert idx['records_count']==3976 and idx['batches'][-1]['id']=='B03n'
assert idx['next']['chapter']=='LXIX' and idx['next']['pdf_page']==448
assert idx['source_sha256']==W['source_original_pdf_sha256']
assert D['source_units']==31 and M['span_count']==12 and len(U['issues'])==14
ids=[r['local_id'] for r in D['rows']]
mapped=[k for sp in M['source_spans'] for k in sp['mapped_local_ids']]
assert ids==[f'LXIX-C{i:03}' for i in range(1,32)]
assert len(mapped)==31 and sorted(mapped)==sorted(ids)
assert all(r['chapter']=='LXIX' for r in D['rows'][:-1])
assert D['rows'][-1]['chapter']=='LXX_NAVIGATION_ONLY'
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').is_file()
for f in W['original_images']:
 assert H(f['path'])==f['sha256'] and (B/f['path']).stat().st_size==f['bytes']
rules=[]
for n,r in enumerate(D['rows'],start=3977):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_admitted':True,'source_only_reference_accepted':True,
  'independent_danger_outcome_verified':False,'empirically_validated_prediction':False,
  'runtime_model_promoted':False})
assert [r['record_number'] for r in rules]==list(range(3977,4008))
R={'batch':'B03o','kind':'HISTORICAL_FEAR_AND_DANGER_ASSERTIONS_ONLY',
 'status':'CHAPTER_LXIX_SOURCE_DOCUMENTARY_ADMITTED_LOCALLY',
 'documentary_accepted_locally':True,'record_count':31,
 'first_record':3977,'last_record':4007,'chapter_lxix_units':30,
 'next_chapter_navigation_only':1,'source_passages':12,'source_uncertainties':14,
 'independently_verified_danger_cases':0,'new_empirical_predictions':0,
 'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
by={r['local_id']:r['id'] for r in rules}
M2={'batch':'B03o','status':'LOCAL_ACCEPTED_REVERSE_PRIMARY_IMAGE_MAP',
 'source_spans':[{**sp,'canonical_record_ids':[by[k] for k in sp['mapped_local_ids']]}
  for sp in M['source_spans']],'span_count':12,'mapped_records':31}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M2)
dump('SOURCE_ORDER.json',{'batch':'B03o','original_pages':[448,449],
 'first_record':3977,'last_record':4007,'record_count':31,
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
  'role':r['role']} for r in rules]})
U['status']='RETAINED_AT_LOCAL_DOCUMENTARY_ACCEPTANCE'
dump('UNRESOLVED.json',U)
A={'batch':'B03o','kind':'DOCUMENTARY_NOT_REAL_DANGER_PREDICTION',
 'status':'LOCAL_ADMISSION_PENDING_RELEASE_AND_REMOTE',
 'documentary_accepted_locally':True,'previous_lilly_accepted':3976,
 'new_documentary_records':31,'first_record':'R3977','last_record':'R4007',
 'lilly_if_published':4007,'ptolemy_retained':1066,'combined_if_published':5073,
 'source_passages':12,'unresolved_source_issues':14,'next_chapter':'LXX',
 'next_source_pdf':449,'source_full_pdf_sha256':W['source_original_pdf_sha256'],
 'independent_danger_outcomes':0,'empirically_validated_predictions':0,
 'runtime_promotions':0,'remote_published':False}
for n,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','audit_sha256')]:A[k]=H(n)
dump('ACCEPTANCE.json',A)
print(json.dumps({'records':31,'new_if_published':4007,'combined':5073,'source_passages':12}))
