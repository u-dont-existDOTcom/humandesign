#!/usr/bin/env python3
"""Local source-documentary admission: Lilly Chapter LX original 1647 pages 389-390.
DO NOT turn author-reported marriage into empirical validation.
"""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(f,x):(B/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
DERIVED=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','CLAIM_LEDGER_ACCEPTED_LOCAL.json','ACCEPTANCE.json']
assert not any((B/f).exists() for f in DERIVED)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json');M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json');U=J('UNRESOLVED_SOURCE_LIMITS.json');CL=J('CLAIM_LEDGER.json')
idx=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert idx['records_count']==3418 and idx['batches'][-1]['id']=='B03e'
assert idx['next']['chapter']=='LX' and idx['next']['pdf_page']==423
assert idx['source_sha256']==W['source_full_pdf_sha256']
assert D['source_units']==31 and M['span_count']==13 and len(U['issues'])==13
assert not W['case_independently_authenticated'] and not W['frozen_prospective_prediction']
assert [r['source_local_id'] for r in D['rows']]==[f'LX-C{i:03}' for i in range(1,32)]
ids=[r['source_local_id'] for r in D['rows']]
mapped=[rid for span in M['source_spans'] for rid in span['mapped_source_local_ids']]
assert len(mapped)==len(ids) and sorted(mapped)==sorted(ids)
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261015.md').is_file()
for img in W['original_images']:
 assert H(img['path'])==img['sha256']
 assert (B/img['path']).stat().st_size==img['size_bytes']
rules=[]
for n,r in enumerate(D['rows'],start=3419):
 x={**r,'id':f'R{n}','record_number':n,'global_record_number':n,
   'historical_documentation_admitted':True,
   'source_record_admitted_for_documentary_reference':True,
   'accepted_as_empirical_prediction':False,
   'real_outcome_independently_authenticated':False,
   'is_independently_blinded_case':False,
   'empirical_astrology_prediction_validated':False,
   'runtime_model_promoted':False}
 rules.append(x)
assert [r['record_number'] for r in rules]==list(range(3419,3450))
assert sum(r['chapter']=='LX' for r in rules)==30
assert rules[-1]['chapter']=='LXI_NAVIGATION_ONLY'
RULE={'batch':'B03f','status':'CHAPTER_LX_HISTORICAL_DOCUMENTARY_ADMITTED_LOCALLY',
 'source_pdf_sha256':W['source_full_pdf_sha256'],
 'documentary_accepted_locally':True,
 'whole_chapter_lx_documentary_accepted':True,
 'first_record':3419,'last_record':3449,'record_count':31,
 'substantive_lx_records':30,'lxi_heading_only':1,
 'source_reverse_spans':13,'uncertainties_retained':13,
 'original_case_independently_authenticated':False,
 'independently_confirmed_marriage_outcomes':0,
 'source_internal_reported_marriage_outcomes':1,
 'independent_blinded_second_diplomatic_transcription':False,
 'new_empirical_predictions_validated':0,'runtime_promotions':0,
 'rules':rules}
dump('RULES.json',RULE)
xid={r['source_local_id']:r['id'] for r in rules}
MAP={'batch':'B03f','status':'LOCAL_DOCUMENTARY_SOURCE_REVERSE_MAP',
 'source_spans':[{**s,'canonical_record_ids':[xid[k] for k in s['mapped_source_local_ids']]}
                 for s in M['source_spans']],
 'span_count':13,'mapped_unique_documentary_records':31,
 'independent_second_transcription':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',MAP)
ORDER={'batch':'B03f','status':'LOCAL_ORIGINAL_SOURCE_ORDER_ADMITTED',
 'original_pdf_pages':[423,424],'first_record':3419,'last_record':3449,
 'record_count':31,'source_spans':13,
 'records':[{'record_number':r['record_number'],'pdf_pages':r['original_pdf_pages'],
             'role':r['role']} for r in rules],
 'reverse_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json'}
dump('SOURCE_ORDER.json',ORDER)
U['status']='UNRESOLVED_RETAINED_AT_LOCAL_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
cl={**CL,'status':'LOCAL_DOCUMENTARY_SOURCE_ONLY_PENDING_GITHUB',
    'locally_documentary_accepted_units':31,'globally_accepted_new_units':0,
    'author_narrated_positive_cases_counted_as_empirical':0}
dump('CLAIM_LEDGER_ACCEPTED_LOCAL.json',cl)
A={'batch':'B03f','kind':'HISTORICAL_WORKED_CASE_SOURCE_ONLY',
 'status':'CHAPTER_LX_LOCAL_DOCUMENTARY_ADMISSION_PENDING_ARCHIVE_AND_GITHUB',
 'documentary_accepted_locally':True,'whole_chapter_lx_documentary_accepted':True,
 'original_source_pdf_sha256':W['source_full_pdf_sha256'],
 'original_pdf_pages':[423,424],'previous_lilly_accepted':3418,
 'added_documentary_units':31,'first_record':'R3419','last_record':'R3449',
 'lilly_if_published':3449,'retained_ptolemy':1066,'combined_if_published':4515,
 'source_reverse_spans':13,'unresolved_source_issues':13,
 'chapter_lx_source_units':30,'next_heading_only':1,
 'second_reader_complete_diplomatic_transcription':False,
 'independent_real_life_case_outcomes_validated':0,
 'source_internal_positive_cases':1,
 'empirical_astrology_predictions_validated':0,'runtime_promotions':0,
 'canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','source_reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_sha256'),
 ('CLAIM_LEDGER_ACCEPTED_LOCAL.json','claim_ledger_sha256')]:A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03f','local_records':31,'source_spans':13,
 'if_published':3449,'combined_if_published':4515,
 'case_outcomes_empirically_validated':0,'rules_sha256':A['rules_sha256']}))
