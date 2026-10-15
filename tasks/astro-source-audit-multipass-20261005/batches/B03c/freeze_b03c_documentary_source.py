#!/usr/bin/env python3
"""Locally admit original-image LVII historical source, without forecasting efficacy."""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(name,obj):(B/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
NEW=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
     'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in NEW)
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
O=J('SOURCE_ORDER_DRAFT.json')
L=J('CLAIM_LEDGER.json')
assert I['records_count']==3248 and I['batches'][-1]['id']=='B03b'
assert I['next']['chapter']=='LVII' and I['next']['pdf_page']==414
assert I['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==74 and C['span_count']==26
assert len(U['issues'])==19
assert D['rows'][-1]['chapter']=='LVIII_HEADING_ONLY'
assert D['rows'][-1]['source_local_id']=='LVII-C074'
assert [r['source_local_id'] for r in D['rows']]==O['ordered_local_ids']
mapped=[k for s in C['source_spans'] for k in s['mapped_local_source_ids']]
assert sorted(mapped)==sorted(r['source_local_id'] for r in D['rows']) and len(mapped)==74
for x in W['original_witness_images']:
 assert H(x['path'])==x['sha256'] and (B/x['path']).stat().st_size==x['bytes']
assert L['new_accepted_documentary_records']==0 and L['new_accurate_astro_forecasts']==0
rules=[]
for i,r in enumerate(D['rows'],start=3249):
  rr={**r,'id':f'R{i}','record_number':i,'global_record_number':i,
      'historical_documentary_admitted':True,
      'source_record_admitted_for_documentary_reference':True,
      'accepted_as_empirically_validated_prediction':False,
      'validated_real_historical_cases':0,
      'validated_predictive_accuracy':False,
      'runtime_model_promoted':False,
      'real_world_military_advice':False}
  rules.append(rr)
assert [r['record_number'] for r in rules]==list(range(3249,3323))
assert all(r['chapter']=='LVII' for r in rules[:-1])
assert rules[-1]['chapter']=='LVIII_HEADING_ONLY'
RULES={'batch':'B03c','kind':'HISTORICAL_1647_DOCUMENTARY_ONLY',
 'status':'LVII_SOURCE_LOCALLY_ADMITTED_PENDING_REMOTE_PUBLICATION',
 'documentary_accepted_locally':True,
 'whole_chapter_lvii_source_intake_complete':True,
 'original_source_pdf_sha256':W['original_full_pdf_sha256'],
 'original_pdf_pages':[414,415,416,417],
 'first_record':3249,'last_record':3322,'record_count':74,
 'substantive_lvii_historical_annotations':73,
 'next_heading_only_markers':1,
 'source_reverse_spans':26,
 'source_uncertainties_retained':19,
 'independent_blind_diplomatic_transcription_done':False,
 'empirically_validated_predictions':0,
 'real_conflict_cases_authenticated':0,
 'runtime_model_promotions':0,'rules':rules}
dump('RULES.json',RULES)
by={r['source_local_id']:r['id'] for r in rules}
MAP={'batch':'B03c','status':'LOCALLY_ACCEPTED_ORIGINAL_IMAGE_REVERSE_MAP',
 'source_spans':[{**s,'canonical_record_ids':[by[k] for k in s['mapped_local_source_ids']]}
                for s in C['source_spans']],
 'span_count':26,'mapped_documentary_source_units':74,
 'blind_diplomatic_second_reader':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',MAP)
ORDER={'batch':'B03c','status':'LOCALLY_ACCEPTED_ORIGINAL_SOURCE_ORDER',
 'source_original_pdf_pages':[414,415,416,417],
 'first_record':3249,'last_record':3322,'record_count':74,
 'opening':'PDF414 below LVI divider',
 'closing':'PDF417 above LVIII divider',
 'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'source_spans':26,
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
             'role':r['role']} for r in rules],
 'empirical_evidence_counted':0}
dump('SOURCE_ORDER.json',ORDER)
U['status']='RETAINED_AT_LOCAL_DOCUMENTARY_ACCEPTANCE'
dump('UNRESOLVED.json',U)
A={'batch':'B03c','kind':'ORIGINAL_LILLY_DOCUMENTARY_SOURCE_ONLY',
   'status':'LVII_LOCALLY_SOURCE_ACCEPTED_PENDING_RELEASE_AND_PUBLICATION',
   'documentary_accepted_locally':True,
   'whole_chapter_lvii_source_intake_complete':True,
   'original_full_pdf_sha256':W['original_full_pdf_sha256'],
   'original_pdf_pages':[414,415,416,417],
   'previous_accepted_lilly':3248,
   'added_documentary_units':74,
   'first_record':'R3249','last_record':'R3322',
   'lilly_if_published':3322,'ptolemy_retained':1066,
   'combined_if_published':4388,'source_reverse_spans':26,
   'retained_source_issues':19,
   'cross_page_records':sum(len(r['original_pdf_pages'])>1 for r in rules),
   'substantive_lvii_annotations':73,'lviii_navigation_only':1,
   'full_independent_diplomatic_reader_done':False,
   'empirical_astro_predictions_validated':0,
   'real_historical_case_outcomes_authenticated':0,
   'runtime_promotions':0,'canonical_published':False}
for file,key in [
 ('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','visual_audit_sha256')]:
 A[key]=H(file)
dump('ACCEPTANCE.json',A)
print({'batch':'B03c','locally_admitted':74,'lilly_if_published':3322,
       'combined_if_published':4388,'source_passages':26,
       'unresolved_source_limits':19,'new_predictive_validations':0,
       'rules_sha256':A['rules_sha256']})
