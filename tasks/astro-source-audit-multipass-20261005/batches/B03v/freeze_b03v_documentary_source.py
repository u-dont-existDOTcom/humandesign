#!/usr/bin/env python3
"""Accept original historical William Lilly 1647 ecclesiastical benefice source-only clauses."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
fresh=['RULES.json','ACCEPTANCE.json','UNRESOLVED.json','SOURCE_ORDER.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in fresh)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert I['records_count']==4384 and I['batches'][-1]['id']=='B03u'
assert I['next']['chapter']=='LXXVI' and I['next']['pdf_page']==466
assert I['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==62 and M['span_count']==16 and len(U['issues'])==20
assert W['original_body_pdf_pages']==[466,467,468]
keys=[r['source_local_id'] for r in D['rows']]
mapped=[x for s in M['source_spans'] for x in s['mapped_local_ids']]
assert len(keys)==len(mapped)==62 and sorted(keys)==sorted(mapped)
by={r['source_local_id']:r for r in D['rows']}
assert all(s['original_pdf_pages']==by[k]['original_pdf_pages'] for s in M['source_spans'] for k in s['mapped_local_ids'])
assert all(r['chapter']=='LXXVI' for r in D['rows'][:-2])
assert all(r['chapter']=='LXXVII_NAVIGATION_ONLY' for r in D['rows'][-2:])
assert C['independently_authenticated_appointment_cases']==0
for im in W['original_images']:
 assert H(im['path'])==im['sha256']
 assert (B/im['path']).stat().st_size==im['bytes']
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').exists()
rules=[]
for n,r in enumerate(D['rows'],start=4385):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_accepted':True,'accepted_for_historical_source_reference':True,
  'independent_ecclesiastical_outcome_verified':False,
  'empirically_validated_forecast':False,'runtime_rule_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4385,4447))
R={'batch':'B03v','kind':'HISTORICAL_ECCLESIASTICAL_APPOINTMENT_SOURCE_ONLY',
 'status':'LOCALLY_ADMITTED_DOCUMENTARY_PENDING_ARCHIVE',
 'documentary_accepted_locally':True,'record_count':62,
 'first_record':4385,'last_record':4446,
 'substantive_lxxvi_annotations':60,'next_lxxvii_navigation_only':2,
 'original_pdf_pages':[466,467,468],
 'original_reverse_source_passages':16,
 'retained_original_source_issues':20,
 'independently_verified_clerical_appointments':0,
 'independently_verified_bribe_cases':0,
 'new_empirically_validated_astrology_predictions':0,
 'runtime_promotions':0,
 'original_full_pdf_sha256':W['original_full_pdf_sha256'],
 'rules':rules}
dump('RULES.json',R)
global_ids={r['source_local_id']:r['id'] for r in rules}
REV={'batch':'B03v','status':'ORIGINAL_SOURCE_TO_GLOBAL_HISTORICAL_DOCUMENTARY_REVERSE_MAP',
 'source_spans':[{**s,'accepted_global_record_ids':[global_ids[k] for k in s['mapped_local_ids']]}
                 for s in M['source_spans']],
 'span_count':16,'mapped_records':62,
 'independent_second_diplomatic_reader':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',REV)
dump('SOURCE_ORDER.json',{'batch':'B03v','status':'LOCALLY_ACCEPTED_ORIGINAL_SOURCE_ORDER',
 'first_record':4385,'last_record':4446,'record_count':62,
 'original_pdf_pages':[466,467,468],
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
             'role':r['role']} for r in rules],
 'empirically_validated_prediction_cases':0})
U['status']='ALL_HISTORICAL_SOURCE_LIMITS_RETAINED_AT_ACCEPTANCE'
dump('UNRESOLVED.json',U)
A={'batch':'B03v','kind':'LILLY1647_ECCLESIASTICAL_HISTORICAL_SOURCE_ONLY',
 'status':'LOCALLY_DOCUMENTARY_ACCEPTED_PENDING_ZIP_AND_PUBLICATION',
 'documentary_accepted_locally':True,
 'prior_accepted_lilly':4384,'new_documentary_records':62,
 'first_record':'R4385','last_record':'R4446',
 'lilly_if_published':4446,'ptolemy_retained':1066,'combined_if_published':5512,
 'original_full_pdf_sha256':W['original_full_pdf_sha256'],
 'original_reverse_source_passages':16,'original_unresolved_limits':20,
 'next_chapter':'LXXVII','next_original_pdf_page':468,
 'independently_authenticated_appointment_outcomes':0,
 'independently_authenticated_clergy_misconduct_cases':0,
 'new_empirically_validated_predictions':0,'runtime_model_promotions':0,
 'complete_independent_diplomatic_transcription':False,
 'remote_canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_source_audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03v','local_documentary_records':62,
 'lilly_if_published':4446,'combined_if_published':5512,
 'source_passages':16,'retained_limits':20,'empirical_validations':0}))
