#!/usr/bin/env python3
"""Original-only Lilly LXII archival admission; no empirical case validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda name:json.loads((B/name).read_text())
sha=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(n,obj):
 (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
out=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
     'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','CLAIM_LEDGER_ACCEPTED_LOCAL.json']
assert not any((B/x).exists() for x in out)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
P=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert I['records_count']==3484 and I['batches'][-1]['id']=='B03g'
assert I['next']['chapter']=='LXII' and I['next']['pdf_page']==426
assert I['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==43 and P['span_count']==14 and len(U['issues'])==17
keys=[r['local_id'] for r in D['rows']]
mapped=[i for s in P['source_spans'] for i in s['mapped_local_ids']]
assert keys==[f'LXII-C{i:03}' for i in range(1,44)]
assert sorted(keys)==sorted(mapped) and len(mapped)==43
for im in W['source_images']:
 assert sha(im['path'])==im['sha256']
 assert (B/im['path']).stat().st_size==im['bytes']
assert D['rows'][-1]['chapter']=='LXIII_BOUNDARY_ONLY'
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261015.md').is_file()
rules=[]
for n,r in enumerate(D['rows'],start=3485):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_admitted':True,
  'accepted_as_empirical_prediction':False,
  'empirical_case_verified':False})
assert [r['record_number'] for r in rules]==list(range(3485,3528))
assert all(r['chapter']=='LXII' for r in rules[:-1])
R={'batch':'B03h','kind':'SOURCE_DOCUMENTARY_NOT_INDEPENDENT_CASE_EVIDENCE',
 'status':'CHAPTER_LXII_LOCALLY_DOCUMENTARY_ACCEPTED_PENDING_PUBLICATION',
 'documentary_accepted_locally':True,'source_pdf_sha256':W['original_full_pdf_sha256'],
 'record_count':43,'first_record':3485,'last_record':3527,
 'chapter_lxii_source_units':42,'next_heading_only':1,
 'source_reverse_passages':14,'retained_source_issues':17,
 'author_reported_dog_return_cases':1,'independently_verified_dog_returns':0,
 'upper_room_claim_independently_verified':False,
 'complete_blind_second_diplomatic_transcription':False,
 'empirical_astrology_predictions_validated':0,'runtime_promotions':0,
 'rules':rules}
dump('RULES.json',R)
by_id={r['local_id']:r['id'] for r in rules}
MAP={'batch':'B03h','status':'ORIGINAL_SOURCE_TO_ACCEPTED_DOCUMENTARY_MAP',
 'source_spans':[{**s,'canonical_record_ids':[by_id[i] for i in s['mapped_local_ids']]}
                 for s in P['source_spans']],
 'span_count':14,'mapped_unique_source_units':43,
 'blind_second_original_reader':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',MAP)
S={'batch':'B03h','status':'ORIGINAL_SOURCE_DOCUMENTARY_ADMITTED_LOCALLY',
 'pdf_pages':[426,427,428],'first_record':3485,'last_record':3527,
 'source_spans':14,'record_count':43,
 'records':[{'record_number':r['record_number'],'page':r['original_pdf_pages'],'role':r['role']} for r in rules],
 'empirically_validated_cases':0}
dump('SOURCE_ORDER.json',S)
U['status']='RETAINED_AT_SOURCE_ADMISSION'
dump('UNRESOLVED.json',U)
dump('CLAIM_LEDGER_ACCEPTED_LOCAL.json',{
 **C,'status':'SOURCE_DOCUMENTARY_ADMITTED_LOCALLY_NOT_PUBLISHED',
 'locally_admitted_documentary_units':43,'new_globally_accepted_records':0,
 'new_empirical_predictions':0})
A={'batch':'B03h','kind':'HISTORICAL_SOURCE_DOCUMENTARY_ONLY',
 'status':'CHAPTER_LXII_LOCAL_DOCUMENTARY_ADMITTED_PENDING_ARCHIVE_AND_REMOTE',
 'documentary_accepted_locally':True,
 'previous_accepted_lilly':3484,'added_documentary_records':43,
 'first_record':'R3485','last_record':'R3527',
 'lilly_if_published':3527,'ptolemy_retained':1066,
 'combined_if_published':4593,
 'source_reverse_passages':14,'unresolved_source_issues':17,
 'original_pdf_pages':[426,427,428],
 'source_full_pdf_sha256':W['original_full_pdf_sha256'],
 'independently_authenticated_dog_recoveries':0,
 'author_reported_dog_recoveries':1,
 'upper_room_prediction_outcome':'UNRESOLVED_NOT_ESTABLISHED_BY_UNDER_TABLE_REPORT',
 'new_empirical_predictions_validated':0,'runtime_promotions':0,
 'complete_diplomatic_second_reading':False,'remote_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
 ('UNRESOLVED.json','uncertainties_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','source_audit_sha256')]:
 A[k]=sha(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03h','local_documentary_units':43,
 'lilly_if_published':3527,'combined_if_published':4593,
 'empirical_validations':0,'rules_sha256':A['rules_sha256']}))
