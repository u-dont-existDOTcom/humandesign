#!/usr/bin/env python3
"""Admit Chapter LXI original documentary source with explicit unverified case outcome."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
read=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
sha=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(n,obj):
 (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
new=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
     'CLAIM_LEDGER_ACCEPTED_LOCAL.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in new),'No destructive overwrite of admitted materials'
D=read('SOURCE_FIRST_CLAUSES_DRAFT.json')
P=read('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=read('SOURCE_WINDOW_MANIFEST.json')
U=read('UNRESOLVED_SOURCE_LIMITS.json')
C=read('CLAIM_LEDGER.json')
idx=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert idx['records_count']==3449 and idx['batches'][-1]['id']=='B03f'
assert idx['next']['chapter']=='LXI' and idx['next']['pdf_page']==424
assert idx['source_sha256']==W['source_full_pdf_sha256']
assert len(D['rows'])==35 and D['source_units']==35 and P['span_count']==15
assert len(U['issues'])==16
assert [r['source_local_id'] for r in D['rows']]==[f'LXI-C{i:03}' for i in range(1,36)]
original_keys=[k for s in P['source_spans'] for k in s['mapped_source_local_ids']]
assert len(original_keys)==35 and sorted(original_keys)==sorted(r['source_local_id'] for r in D['rows'])
for img in W['original_images']:
 assert sha(img['path'])==img['sha256']
 assert (B/img['path']).stat().st_size==img['bytes']
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261015.md').is_file()
assert C['source_internal_servant_return_reports']==1 and C['empirical_predictions_validated']==0
rules=[]
for i,r in enumerate(D['rows'],start=3450):
 rr={**r,'id':f'R{i}','record_number':i,'global_record_number':i,
   'historical_documentation_admitted':True,
   'source_record_admitted_for_documentary_reference':True,
   'accepted_as_empirical_prediction':False,
   'real_outcome_independently_authenticated':False,
   'is_independently_blinded_case':False,
   'empirical_astrology_prediction_validated':False,
   'runtime_model_promoted':False}
 rules.append(rr)
assert [r['record_number'] for r in rules]==list(range(3450,3485))
assert sum(r['chapter']=='LXI' for r in rules)==34
assert rules[-1]['chapter']=='LXII_NAVIGATION_ONLY'
R={'batch':'B03g','kind':'HISTORICAL_SOURCE_AND_AUTHOR_NARRATED_CASE_ONLY',
 'status':'CHAPTER_LXI_DOCUMENTARY_ADMITTED_LOCALLY_PENDING_ARCHIVE_AND_GIT',
 'documentary_accepted_locally':True,'whole_chapter_lxi_documentary_accepted':True,
 'source_pdf_sha256':W['source_full_pdf_sha256'],
 'source_original_pdf_pages':[424,425,426],
 'first_record':3450,'last_record':3484,'record_count':35,
 'chapter_lxi_source_units':34,'next_chapter_navigation_only':1,
 'source_reverse_spans':15,'source_uncertainties_retained':16,
 'author_reported_servant_return_outcomes':1,
 'independently_authenticated_servant_outcomes':0,
 'reliably_verified_predicted_distance':False,
 'claim_one_or_two_days_not_scoreable_without_question_date':True,
 'complete_independent_diplomatic_second_reader':False,
 'empirically_validated_predictive_cases':0,'runtime_promotions':0,
 'rules':rules}
dump('RULES.json',R)
id_by_local={r['source_local_id']:r['id'] for r in rules}
M={'batch':'B03g','status':'LOCALLY_ACCEPTED_DOCUMENTARY_SOURCE_REVERSE_MAP',
 'source_spans':[{**s,'canonical_record_ids':[id_by_local[k] for k in s['mapped_source_local_ids']]}
  for s in P['source_spans']],
 'span_count':15,'mapped_unique_original_documentary_units':35,
 'independent_diplomatic_second_reader':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M)
S={'batch':'B03g','status':'LOCALLY_ADMITTED_PHYSICAL_1647_SOURCE_ORDER',
 'original_pdf_pages':[424,425,426],'first_record':3450,'last_record':3484,
 'record_count':35,'source_spans':15,
 'last_chapter_heading_only_pdf':426,
 'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
     'role':r['role']} for r in rules],
 'empirical_case_evidence_counted':0}
dump('SOURCE_ORDER.json',S)
U['status']='RETAINED_AT_LOCAL_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
cl={**C,'status':'LOCALLY_ADMITTED_HISTORICAL_DOCUMENTARY_SOURCE_ONLY',
 'locally_admitted_documentary_units':35,
 'globally_accepted_new_source_units':0,
 'source_internal_servant_return_reports_recognized':1,
 'source_internal_servant_return_reports_counted_as_empirical':0}
dump('CLAIM_LEDGER_ACCEPTED_LOCAL.json',cl)
A={'batch':'B03g','status':'CHAPTER_LXI_LOCAL_DOCUMENTARY_ACCEPTED_PENDING_RELEASE_AND_PUBLICATION',
 'kind':'HISTORICAL_WORKED_CASE_NOT_VERIFIED_PREDICTION',
 'documentary_accepted_locally':True,
 'whole_chapter_lxi_documentary_accepted':True,
 'source_pdf_sha256':W['source_full_pdf_sha256'],
 'previous_accepted_lilly':3449,'new_documentary_records':35,
 'first_record':'R3450','last_record':'R3484',
 'lilly_if_published':3484,'ptolemy_retained':1066,'combined_if_published':4550,
 'source_reverse_spans':15,'retained_source_uncertainties':16,
 'cross_page_records':sum(len(r['original_pdf_pages'])>1 for r in rules),
 'original_case_independently_authenticated':False,
 'case_asked_date_exact_known':False,
 'source_only_friday_return_report':True,
 'source_only_kingston_location_qualified_as_if_true':True,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'independent_full_diplomatic_transcription_done':False,
 'canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_sha256'),
 ('CLAIM_LEDGER_ACCEPTED_LOCAL.json','claim_ledger_sha256')]:
 A[k]=sha(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03g','local_admission':35,
 'lilly_if_published':3484,'combined_if_published':4550,
 'author_case_outcome_empirically_validated':False,
 'source_rules_sha256':A['rules_sha256']}))
