#!/usr/bin/env python3
"""Source-only local documentary admission for original 1647 Lilly Chapter LVI."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
j=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
sha=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(f,obj):
 (B/f).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
results=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
         'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','ACCEPTANCE.json']
assert not any((B/k).exists() for k in results),"Do not overwrite admission evidence"
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=j('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=j('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
S=j('SOURCE_ORDER_DRAFT.json')
W=j('SOURCE_WINDOW_MANIFEST.json')
U=j('UNRESOLVED_SOURCE_LIMITS.json')
L=j('CLAIM_LEDGER.json')
assert I['records_count']==3203 and I['batches'][-1]['id']=='B03a'
assert I['next']['chapter']=='LVI' and I['next']['pdf_page']==413
assert D['source_units']==45 and M['span_count']==19
assert len(D['rows'])==45 and len(M['source_spans'])==19
assert len(U['issues'])==17
assert I['source_sha256']==W['complete_original_pdf_sha256']
assert [x['local_id'] for x in D['rows']]==S['ordered_local_ids']
assert sorted(id for s in M['source_spans'] for id in s['local_source_ids'])==sorted(
       x['local_id'] for x in D['rows'])
assert not D['independent_full_diplomatic_transcription_claimed']
assert L['new_canonical_lilly']==L['new_empirical_siege_forecasts']==0
for v in W['images']:
 assert sha(v['path'])==v['sha256'] and (B/v['path']).stat().st_size==v['bytes']
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261015.md').exists()
rules=[]
for n,r in enumerate(D['rows'],start=3204):
    rr={**r,
       'id':f'R{n}','record_number':n,'global_record_number':n,
       'source_first_provisional':False,
       'admitted_as_historical_documentation':True,
       'accepted_as_empirically_validated_prediction':False,
       'validated_by_real_world_cases':False,'runtime_predicate_active':False,
       'real_world_military_use_authorized':False}
    rules.append(rr)
assert [r['record_number'] for r in rules]==list(range(3204,3249))
assert all(r['chapter']=='LVI' for r in rules[:-1])
assert rules[-1]['chapter']=='LVII_HEADING_NAVIGATION_ONLY'
R={
  'batch':'B03b','kind':'HISTORICAL_DOCUMENTARY_SOURCE_ONLY',
  'status':'CHAPTER_LVI_SOURCE_DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_PUBLICATION',
  'documentary_accepted_locally':True,'whole_chapter_lvi_historical_intake_complete':True,
  'source_original_pdf_sha256':W['complete_original_pdf_sha256'],
  'original_pdf_body_pages':[413,414],
  'first_record':3204,'last_record':3248,'record_count':45,
  'substantive_lvi_units':44,'next_chapter_navigation_only_units':1,
  'source_reverse_spans':19,'source_uncertainties_retained':17,
  'blind_complete_second_diplomatic_transcription':False,
  'new_empirically_validated_predictions':0,
  'new_authenticated_historical_siege_case_predictions':0,
  'runtime_promotions':0,'rules':rules
}
dump('RULES.json',R)
ids={r['local_id']:r['id'] for r in rules}
RMAP={'batch':'B03b',
      'status':'LOCALLY_ADMITTED_ORIGINAL_IMAGE_SOURCE_REVERSE_MAP',
      'source_spans':[{**s,'canonical_record_ids':[ids[k] for k in s['local_source_ids']]}
                      for s in M['source_spans']],
      'span_count':len(M['source_spans']),
      'mapped_unique_canonical_records':len(rules),
      'blind_second_diplomatic_transcription':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',RMAP)
ORDER={'batch':'B03b','status':'LOCALLY_ACCEPTED_SOURCE_ORDER',
       'original_pdf_pages':[413,414],
       'opening':'PDF413 below LV divider','closing':'PDF414 above LVII divider',
       'first_record':3204,'last_record':3248,'record_count':45,
       'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
       'source_spans':19,
       'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
                   'role':r['role']} for r in rules],
       'empirical_source_cases_counted':0}
dump('SOURCE_ORDER.json',ORDER)
U['status']='RETAINED_UNRESOLVED_AT_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03b','kind':'DOCUMENTARY_1647_SOURCE_ONLY',
   'status':'LOCALLY_ADMITTED_LVI_SOURCE_PENDING_RELEASE_AND_GITHUB',
   'documentary_accepted_locally':True,
   'whole_chapter_lvi_documentary_intake_complete':True,
   'original_full_pdf_sha256':W['complete_original_pdf_sha256'],
   'original_pdf_pages':[413,414],
   'physical_start':'original PDF413 BELOW Chapter LV divider',
   'physical_end':'original PDF414 ABOVE Chapter LVII divider',
   'previous_lilly_accepted':3203,'added_historical_units':45,
   'lilly_if_published':3248,'retained_ptolemy':1066,
   'combined_if_published':4314,
   'source_reverse_spans':19,
   'unresolved_source_issues':17,
   'page_crossing_record_count':sum(len(x['original_pdf_pages'])>1 for x in rules),
   'chapter_lvi_source_units':44,'next_heading_only':1,
   'blind_complete_second_diplomatic_reader':False,
   'new_empirical_predictions_validated':0,
   'new_authentic_siege_cases_validated':0,
   'runtime_predicate_promotions':0,
   'canonical_source_published':False}
for f,k in [('RULES.json','rules_sha256'),
            ('SOURCE_ORDER.json','source_order_sha256'),
            ('UNRESOLVED.json','unresolved_sha256'),
            ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_map_sha256'),
            ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_sha256')]:
 A[k]=sha(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({
 'batch':'B03b','local_historical_records_added':45,
 'lilly_if_published':3248,'combined_if_published':4314,
 'source_reverse_spans':19,'unresolved':17,
 'empirical_predictions':0,'runtime_promotions':0,
 'rules_sha256':A['rules_sha256']},indent=2))
