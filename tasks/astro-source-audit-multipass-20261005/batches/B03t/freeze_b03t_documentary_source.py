#!/usr/bin/env python3
"""Original William Lilly ninth-house Chapter LXXIV documentary admission; not predictive validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
new=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in new),'Preserve existing acceptance bytes'
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
P=J('SOURCE_ORDER_DRAFT.json')
INDEX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
idx=json.loads(INDEX.read_text(encoding='utf-8'))
assert idx['records_count']==4170 and idx['batches'][-1]['id']=='B03s'
assert idx['next']['chapter']=='LXXIV' and idx['next']['pdf_page']==456
assert idx['source_sha256']==W['source_original_full_pdf_sha256']
assert D['source_units']==153 and M['span_count']==28 and len(U['issues'])==32
assert W['original_body_pdf_pages']==list(range(456,464))
ids=[r['local_id'] for r in D['rows']]
mapped=[k for s in M['source_spans'] for k in s['mapped_local_ids']]
assert ids==[f'LXXIV-C{i:03}' for i in range(1,154)]
assert len(mapped)==153 and sorted(mapped)==sorted(ids)
byid={r['local_id']:r for r in D['rows']}
assert all(s['original_pdf_pages']==byid[k]['original_pdf_pages']
 for s in M['source_spans'] for k in s['mapped_local_ids'])
assert all(r['chapter']=='LXXIV' for r in D['rows'][:-2])
assert all(r['chapter']=='LXXV_NAVIGATION_ONLY' for r in D['rows'][-2:])
assert C['independently_authenticated_journey_cases']==0
assert C['new_empirically_validated_predictions']==0
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').is_file()
for im in W['original_images']:
 assert H(im['path'])==im['sha256']
 assert (B/im['path']).stat().st_size==im['bytes']
rules=[]
for n,r in enumerate(D['rows'],start=4171):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_accepted':True,'accepted_as_original_source_annotation':True,
  'independently_authenticated_case_outcome':False,
  'empirically_validated_prediction':False,'runtime_model_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4171,4324))
R={'batch':'B03t','kind':'HISTORICAL_NINTH_HOUSE_VOYAGE_SOURCE_ONLY',
 'status':'SOURCE_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_PUBLICATION',
 'documentary_accepted_locally':True,'record_count':153,
 'first_record':4171,'last_record':4323,
 'chapter_substantive_annotations':151,'next_heading_navigation_only':2,
 'original_pdf_pages':list(range(456,464)),
 'source_visual_passages':28,'retained_source_limits':32,
 'independently_verified_journey_cases':0,'independently_verified_weather_cases':0,
 'independently_verified_missing_person_cases':0,
 'new_empirically_validated_astrological_predictions':0,
 'runtime_promotions':0,'complete_second_blind_diplomatic_transcription':False,
 'rules':rules}
dump('RULES.json',R)
by={r['local_id']:r['id'] for r in rules}
rev={'batch':'B03t','status':'LOCALLY_ADMITTED_SOURCE_TO_ACCEPTED_RECORD_REVERSE_MAP',
 'source_spans':[{**s,'accepted_record_ids':[by[k] for k in s['mapped_local_ids']]}
                for s in M['source_spans']],
 'span_count':28,'unique_accepted_source_units':153,
 'blind_original_second_reader':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',rev)
dump('SOURCE_ORDER.json',{'batch':'B03t','status':'LOCAL_ACCEPTED_ORIGINAL_SOURCE_ORDER',
 'original_pdf_pages':list(range(456,464)),
 'first_record':4171,'last_record':4323,'record_count':153,
 'source_passages':28,'original_reverse_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
             'role':r['role']} for r in rules],
 'empirical_case_successes':0})
U['status']='ALL_SOURCE_LIMITS_RETAINED_AT_LOCAL_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03t','kind':'ORIGINAL_HISTORICAL_NINTH_HOUSE_SOURCE_ONLY',
 'status':'LOCAL_DOCUMENTARY_ADMISSION_PENDING_ZIP_AND_PUBLICATION',
 'documentary_accepted_locally':True,
 'prior_accepted_lilly':4170,'new_documentary_records':153,
 'first_record':'R4171','last_record':'R4323',
 'lilly_if_published':4323,'retained_ptolemy':1066,'combined_if_published':5389,
 'original_image_reverse_passages':28,'retained_source_uncertainties':32,
 'original_pdf_pages':list(range(456,464)),
 'original_full_pdf_sha256':W['source_original_full_pdf_sha256'],
 'next_numbered_chapter':'LXXV','next_original_pdf_page':463,
 'no_independently_verified_journey_outcomes':True,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'complete_second_diplomatic_reader':False,'remotely_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03t','locally_accepted':153,'source_spans':28,
 'source_limits':32,'lilly_if_published':4323,'combined_if_published':5389,
 'new_validated_predictions':0,'rules_sha256':A['rules_sha256']}))
