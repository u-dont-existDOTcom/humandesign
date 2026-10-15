#!/usr/bin/env python3
"""Freeze original 1647 fish-loss source as historical documentary only."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(f,x):(B/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
new=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','ACCEPTANCE.json',
 'CLAIM_LEDGER_ACCEPTED_LOCAL.json']
assert not any((B/x).exists() for x in new),'One-time source admission: do not overwrite.'
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert I['records_count']==3571 and I['batches'][-1]['id']=='B03i'
assert I['next']['chapter']=='LXIV' and I['next']['printed_chapter_numeral']=='LIV'
assert I['next']['pdf_page']==431 and I['source_sha256']==W['source_full_pdf_sha256']
assert D['source_units']==59 and M['span_count']==18 and len(U['issues'])==20
assert W['printed_heading_literal']=='LIV' and W['sequential_chapter_identity']=='LXIV'
assert C['source_author_reported_full_recovery_case_count']==0
assert C['source_author_reported_partially_recovered_fish_case_count']==1
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261015.md').is_file()
ids=[r['local_id'] for r in D['rows']]
mapped=[k for s in M['source_spans'] for k in s['mapped_local_ids']]
assert ids==[f'LXIV-C{i:03}' for i in range(1,60)]
assert len(mapped)==59 and sorted(mapped)==sorted(ids)
assert D['rows'][-1]['chapter_logical']=='LXV_NAVIGATION_ONLY'
assert all(r['chapter_logical']=='LXIV' for r in D['rows'][:-1])
for item in W['original_images']:
 assert H(item['path'])==item['sha256']
 assert (B/item['path']).stat().st_size==item['bytes']
rules=[]
for num,r in enumerate(D['rows'],start=3572):
 rules.append({**r,'id':f'R{num}','record_number':num,
  'global_record_number':num,
  'accepted_historical_documentary':True,
  'source_record_admitted_for_documentary_reference':True,
  'real_world_case_independently_authenticated':False,
  'empirical_predictive_outcome_validated':False,
  'accepted_as_empirical_prediction':False,
  'runtime_rule_promoted':False})
assert [r['record_number'] for r in rules]==list(range(3572,3631))
R={'batch':'B03j','kind':'HISTORICAL_SOURCE_PARTIAL_FISH_RECOVERY_UNVERIFIED',
 'status':'CHAPTER_LXIV_SOURCE_DOCUMENTARY_ADMITTED_LOCALLY',
 'documentary_accepted_locally':True,
 'whole_fish_stolen_chapter_admitted':True,
 'original_printed_chapter_number':'LIV','logical_sequential_chapter':'LXIV',
 'source_pdf_sha256':W['source_full_pdf_sha256'],
 'original_pdf_body_pages':[431,432,433],
 'record_count':59,'first_record':3572,'last_record':3630,
 'substantive_fish_stolen_source_units':58,'next_chapter_navigation_only':1,
 'source_visual_passages':18,'retained_source_uncertainties':20,
 'author_reported_partial_fish_recovery_cases':1,
 'author_reported_full_fish_recovery_cases':0,
 'independently_verified_fish_recoveries':0,
 'remaining_fish_relinquished':True,
 'independent_blind_full_diplomatic_transcription_done':False,
 'new_validated_predictions':0,'runtime_promotions':0,
 'rules':rules}
dump('RULES.json',R)
by_local={r['local_id']:r['id'] for r in rules}
source_map={'batch':'B03j','status':'LOCALLY_ADMITTED_SOURCE_TO_RECORD_REVERSE_MAP',
 'source_spans':[{**sp,'canonical_record_ids':[by_local[k] for k in sp['mapped_local_ids']]}
  for sp in M['source_spans']],
 'span_count':18,'mapped_accepted_source_units':59,
 'original_printed_heading':'LIV','logical_position':'LXIV',
 'independent_blind_diplomatic_transcription_done':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',source_map)
order={'batch':'B03j','status':'ORIGINAL_CHAPTER_PHYSICAL_ORDER_SOURCE_ONLY',
 'original_pdf_pages':[431,432,433],
 'original_printed_pages':[397,398,399],
 'original_chapter_heading':'CHAP LIV Fish Stolen',
 'logical_chapter':'LXIV','next_printed_chapter':'LXV',
 'first_record':3572,'last_record':3630,'record_count':59,'source_spans':18,
 'source_to_accepted_reverse_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'record_number':r['record_number'],'pages':r['original_pdf_pages'],'role':r['role']} for r in rules],
 'empirical_outcomes_counted':0}
dump('SOURCE_ORDER.json',order)
U['status']='RETAINED_AT_LOCAL_HISTORICAL_SOURCE_ADMISSION'
dump('UNRESOLVED.json',U)
cl={**C,'status':'LOCALLY_DOCUMENTARY_SOURCE_ADMITTED_NOT_PUBLISHED',
 'locally_admitted_historical_source_units':59,
 'globally_accepted_new_source_units':0,
 'reported_partial_fish_return_counted_as_external_validation':0}
dump('CLAIM_LEDGER_ACCEPTED_LOCAL.json',cl)
A={'batch':'B03j','kind':'LILLY1647_HISTORICAL_FISH_THEFT_CASE_NOT_EMPIRICAL',
 'status':'CHAPTER_LXIV_LOCALLY_DOCUMENTARY_ACCEPTED_PENDING_ARCHIVE_AND_GITHUB',
 'documentary_accepted_locally':True,'whole_chapter_lxiv_source_intake_complete':True,
 'previous_accepted_lilly':3571,'new_documentary_records':59,
 'first_record':'R3572','last_record':'R3630',
 'lilly_if_published':3630,'ptolemy_retained':1066,
 'combined_if_published':4696,
 'source_reverse_spans':18,'retained_source_uncertainties':20,
 'original_pdf_body_pages':[431,432,433],
 'original_printed_heading':'LIV','logical_number':'LXIV',
 'next_printed_chapter':'LXV','next_source_pdf_page':433,
 'source_full_pdf_sha256':W['source_full_pdf_sha256'],
 'author_reported_partially_recovered_fish_cases':1,
 'author_reported_complete_recovery_cases':0,
 'independently_verified_case_outcomes':0,
 'independently_verified_thief_identity':0,
 'remaining_fish_unrecovered_or_relinquished':True,
 'new_empirically_validated_predictions':0,'runtime_model_changes':0,
 'complete_blind_original_diplomatic_second_transcription':False,
 'canonical_published':False}
for f,k in [
 ('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_map_sha256'),
 ('CLAIM_LEDGER_ACCEPTED_LOCAL.json','claim_ledger_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','original_visual_review_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03j','locally_admitted':59,'source_spans':18,
 'if_published_lilly':3630,'combined_if_published':4696,
 'empirically_verified_cases':0,'rules_sha256':A['rules_sha256']}))
