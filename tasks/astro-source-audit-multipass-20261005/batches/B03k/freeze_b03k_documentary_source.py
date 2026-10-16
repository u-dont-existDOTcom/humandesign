#!/usr/bin/env python3
"""Original 1647 Chapter LXV source acceptance without predictive-case promotion."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
new=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'ACCEPTANCE.json','CLAIM_LEDGER_ACCEPTED_LOCAL.json']
assert not any((B/n).exists() for n in new)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
P=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
CL=J('CLAIM_LEDGER.json')
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert I['records_count']==3630 and I['batches'][-1]['id']=='B03j'
assert I['next']['chapter']=='LXV' and I['next']['pdf_page']==433
assert I['source_sha256']==W['full_original_pdf_sha256']
assert D['source_units']==40 and P['span_count']==10 and len(U['issues'])==18
assert W['chart_original_date']=='29 March 1644'
assert W['chart_original_time']=='10:12 AM'
ids=[r['local_id'] for r in D['rows']]
mapped=[x for sp in P['source_spans'] for x in sp['mapped_local_ids']]
assert ids==[f'LXV-C{i:03}' for i in range(1,41)]
assert len(mapped)==40 and sorted(mapped)==sorted(ids)
assert D['rows'][-1]['chapter']=='LXVI_NAVIGATION_ONLY'
assert all(r['chapter']=='LXV' for r in D['rows'][:-1])
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261015.md').is_file()
for im in W['original_page_images']:
 assert H(im['path'])==im['sha256'] and (B/im['path']).stat().st_size==im['bytes']
rules=[]
for n,r in enumerate(D['rows'],start=3631):
 rules.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historically_admitted':True,
  'source_record_admitted_for_documentary_reference':True,
  'source_case_independently_authenticated':False,
  'empirical_astrological_prediction_validated':False,
  'runtime_rule_promoted':False})
assert [r['record_number'] for r in rules]==list(range(3631,3671))
R={'batch':'B03k','kind':'HISTORICAL_BATTLE_CASE_SOURCE_ONLY',
 'status':'CHAPTER_LXV_LOCALLY_DOCUMENTARY_ADMITTED_PENDING_REMOTE_PUBLICATION',
 'documentary_accepted_locally':True,'whole_chapter_lxv_documentary_accepted':True,
 'source_full_pdf_sha256':W['full_original_pdf_sha256'],
 'first_record':3631,'last_record':3670,'record_count':40,
 'substantive_lxv_source_units':39,'next_chapter_heading_only':1,
 'source_original_pdf_body_pages':[433,434],
 'reverse_source_passages':10,'source_uncertainties_retained':18,
 'chart_original_date':'29 March 1644','chart_original_time':'10:12 AM',
 'author_reported_favorable_battle_letter_cases':1,
 'independent_letter_arrival_time_verified':False,
 'independent_battle_prediction_outcome_verified':False,
 'new_empirical_predictions_validated':0,'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
ids_final={r['local_id']:r['id'] for r in rules}
M={'batch':'B03k','status':'LOCALLY_ADMITTED_ORIGINAL_IMAGE_REVERSE_MAP',
 'source_spans':[{**sp,'canonical_record_ids':[ids_final[x] for x in sp['mapped_local_ids']]}
   for sp in P['source_spans']],
 'span_count':10,'mapped_unique_documentary_units':40,
 'blind_original_second_reader':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M)
S={'batch':'B03k','status':'LOCALLY_DOCUMENTARY_ADMITTED_ORIGINAL_ORDER',
 'original_source_body_pdf_pages':[433,434],
 'next_heading_pdf_page':435,
 'first_record':3631,'last_record':3670,'record_count':40,
 'original_source_passages':10,
 'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
   'role':r['role']} for r in rules],'empirical_outcomes_counted':0}
dump('SOURCE_ORDER.json',S)
U['status']='ALL_RETAINED_AT_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
local_ledger={**CL,'status':'SOURCE_DOCUMENTARY_ADMITTED_LOCAL_ONLY',
 'local_documentary_units_admitted':40,'new_accepted_historical_records':0,
 'independently_validated_11_to_12_hour_forecast':False}
dump('CLAIM_LEDGER_ACCEPTED_LOCAL.json',local_ledger)
A={'batch':'B03k','kind':'HISTORICAL_ASTROLOGY_BATTLE_CASE_NOT_EMPIRICALLY_VALIDATED',
 'status':'CHAPTER_LXV_LOCAL_DOCUMENTARY_ADMISSION_PENDING_RELEASE_AND_GITHUB',
 'documentary_accepted_locally':True,'whole_chapter_lxv_complete':True,
 'previous_lilly_accepted':3630,'new_documentary_records':40,
 'first_record':'R3631','last_record':'R3670',
 'lilly_if_published':3670,'ptolemy_retained':1066,
 'combined_if_published':4736,
 'source_reverse_passages':10,'source_uncertainties_retained':18,
 'original_pdf_body_pages':[433,434],
 'next_heading_page':435,'next_chapter':'LXVI',
 'original_chart_date':'29 March 1644','original_chart_time':'10:12 AM',
 'original_pdf_sha256':W['full_original_pdf_sha256'],
 'historical_favorable_battle_reported_cases':1,
 'independent_letter_arrival_time_evidence':0,
 'independently_authenticated_battle_outcomes':0,
 'eleven_to_twelve_hour_claim_empirically_verified':False,
 'complete_victory_not_unqualified':True,
 'new_empirical_predictions_validated':0,'runtime_promotions':0,
 'blind_full_original_diplomatic_second_transcription':False,
 'remote_published':False}
for f,k in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','original_image_audit_sha256'),
 ('CLAIM_LEDGER_ACCEPTED_LOCAL.json','local_ledger_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03k','local_documentary_units':40,'lilly_if_published':3670,
 'combined_if_published':4736,'empirical_validations':0,'rules_sha256':A['rules_sha256']}))
