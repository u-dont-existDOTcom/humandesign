#!/usr/bin/env python3
"""First-edition original source admission for Lilly LXXV, preserving transposed folio numerals."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
NEW=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/f).exists() for f in NEW),'No overwrite of accepted source layer'
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
INDEX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
idx=json.loads(INDEX.read_text(encoding='utf-8'))
assert idx['records_count']==4323 and idx['batches'][-1]['id']=='B03t'
assert idx['next']['chapter']=='LXXV' and idx['next']['pdf_page']==463
assert idx['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==61 and M['span_count']==16 and len(U['issues'])==20
assert W['original_scan_order']==[463,464,465,466]
assert W['original_imprinted_page_numerals']==[429,431,430,432]
assert C['separately_verified_traveler_cases']==C['separately_verified_competency_cases']==0
assert C['empirically_validated_astrology_predictions']==0
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').exists()
ids=[r['source_local_id'] for r in D['rows']]
mapped=[k for s in M['source_spans'] for k in s['mapped_local_ids']]
assert ids==[f'LXXV-C{i:03}' for i in range(1,62)]
assert len(mapped)==61 and sorted(mapped)==sorted(ids)
by={r['source_local_id']:r for r in D['rows']}
assert all(s['original_pdf_pages']==by[k]['original_pdf_pages'] for s in M['source_spans'] for k in s['mapped_local_ids'])
assert all(r['chapter']=='LXXV' for r in D['rows'][:-2])
assert all(r['chapter']=='LXXVI_NAVIGATION_ONLY' for r in D['rows'][-2:])
for item in W['original_images']:
 assert H(item['path'])==item['sha256']
 assert (B/item['path']).stat().st_size==item['bytes']
rules=[]
for n,r in enumerate(D['rows'],start=4324):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_accepted':True,
  'source_record_accepted_for_documentary_reference':True,
  'individual_case_independently_verified':False,
  'empirical_forecast_validated':False,'runtime_model_promoted':False})
assert [r['record_number'] for r in rules]==list(range(4324,4385))
R={'batch':'B03u','kind':'LILLY1647_HISTORICAL_SKILL_TRAVELLER_SOURCE_ONLY',
 'status':'DOCUMENTARY_SOURCE_LOCALLY_ACCEPTED_PENDING_ARCHIVE',
 'documentary_accepted_locally':True,
 'record_count':61,'first_record':4324,'last_record':4384,
 'substantive_lxxv_source_annotations':59,'lxxvi_navigation_only':2,
 'original_pdf_textual_order':[463,464,465,466],
 'original_imprinted_folios':[429,431,430,432],
 'imprinted_folio_numbers_are_swapped':True,
 'source_reverse_passages':16,'retained_original_source_uncertainties':20,
 'independently_verified_skill_cases':0,'independently_verified_absent_travellers':0,
 'independently_verified_travel_decisions':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'complete_blind_original_second_reader':False,'rules':rules}
dump('RULES.json',R)
bylocal={r['source_local_id']:r['id'] for r in rules}
rev={'batch':'B03u','status':'LOCALLY_ADMITTED_ORIGINAL_SOURCE_REVERSE_MAP',
 'original_scan_order':[463,464,465,466],
 'imprinted_folio_numbers':[429,431,430,432],
 'source_spans':[{**s,'accepted_global_record_ids':[bylocal[k] for k in s['mapped_local_ids']]}
                 for s in M['source_spans']],
 'span_count':16,'unique_accepted_documentary_records':61}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',rev)
dump('SOURCE_ORDER.json',{'batch':'B03u','status':'ORIGINAL_SCAN_ORDER_LOCAL_DOCUMENTARY_ACCEPTED',
 'original_scan_order':[463,464,465,466],'printed_folio_numerals':[429,431,430,432],
 'first_record':4324,'last_record':4384,'record_count':61,
 'source_passages':16,
 'records':[{'record_number':r['record_number'],'pdf_scan_ids':r['original_pdf_pages'],
             'imprinted_folios':r['printed_page_numerals_as_physically_imprinted'],
             'role':r['role']} for r in rules],
 'empirical_case_successes':0})
U['status']='RETAINED_AT_LOCAL_HISTORICAL_SOURCE_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03u','kind':'ORIGINAL_1647_HISTORICAL_SOURCE_NOT_EMPIRICALLY_VALIDATED',
 'status':'CHAPTER_LXXV_LOCAL_DOCUMENTARY_ADMISSION_PENDING_ARCHIVE_GITHUB',
 'documentary_accepted_locally':True,'prior_lilly_accepted':4323,
 'new_documentary_records':61,'first_record':'R4324','last_record':'R4384',
 'lilly_if_published':4384,'ptolemy_retained':1066,
 'combined_if_published':5450,
 'original_pdf_text_order':[463,464,465,466],
 'original_imprinted_folio_numbers':[429,431,430,432],
 'source_folio_pagination_numbers_transposed':True,
 'original_source_reverse_passages':16,'retained_source_issues':20,
 'source_original_pdf_sha256':W['original_full_pdf_sha256'],
 'next_numbered_chapter':'LXXVI','next_original_pdf_page':466,
 'independent_competency_outcomes':0,'independent_travel_decisions':0,
 'independent_absent_person_cases':0,
 'new_empirical_astrology_validations':0,'runtime_model_promotions':0,
 'blind_complete_diplomatic_second_reader':False,
 'canonical_remotely_published':False}
for name,key in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_original_source_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','original_visual_review_sha256')]:
 A[key]=H(name)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03u','locally_accepted_source_units':61,
 'original_visual_passages':16,'source_limits':20,
 'lilly_if_published':4384,'combined_if_published':5450,
 'independently_validated_predictions':0,'rules_sha256':A['rules_sha256']}))
