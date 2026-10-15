#!/usr/bin/env python3
"""Accept Lilly historical text Chapter LV from preserved source-first B03a ZIP."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
dump=lambda f,o:(B/f).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
F=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in F)
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
old=J('CLAIM_LEDGER.json')
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
assert I['records_count']==3171 and I['batches'][-1]['id']=='B02z'
assert I['next']['chapter']=='LV' and I['next']['pdf_page']==411
assert I['source_sha256']==W['complete_original_pdf_sha256']
assert D['source_units']==32 and len(D['rows'])==32
assert C['span_count']==17 and len(C['visual_source_spans'])==17
assert len(U['issues'])==16
assert old['new_canonical_accepted_lilly_units']==0
assert [r['source_local_id'] for r in D['rows']]==[f'LV-C{i:03}' for i in range(1,33)]
mapped=[k for s in C['visual_source_spans'] for k in s['mapped_source_ids']]
assert sorted(mapped)==sorted(r['source_local_id'] for r in D['rows']) and len(mapped)==32
for v in W['original_images']:
 assert H(v['relative_path'])==v['sha256']
 assert (B/v['relative_path']).stat().st_size==v['bytes']
assert D['rows'][-1]['role']=='boundary' and D['rows'][-1]['chapter']=='LVI_BOUNDARY_ONLY'
assert all(r['chapter']=='LV' for r in D['rows'][:-1])
rules=[]
for i,r in enumerate(D['rows'],start=3172):
 rr={**r,'id':f'R{i}','record_number':i,'global_record_number':i,
     'historical_documentary_admitted':True,
     'source_record_admitted_for_documentary_reference':True,
     'accepted_as_empirical_astro_prediction':False,
     'validated_predictive_results':0,
     'runtime_promoted':False}
 rules.append(rr)
R={'batch':'B03a','status':'CHAPTER_LV_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_PUBLICATION',
   'documentary_accepted_locally':True,'whole_chapter_lv_source_intake_complete':True,
   'source_pdf_sha256':W['complete_original_pdf_sha256'],
   'source_original_pdf_pages':[411,412,413],
   'first_record':3172,'last_record':3203,
   'record_count':32,'chapter_lv_substantive_units':31,
   'next_chapter_navigation_only_units':1,
   'source_reverse_passages':17,'source_uncertainties_retained':16,
   'independent_complete_diplomatic_transcription':False,
   'empirically_verified_cases':0,'runtime_promotions':0,
   'accepted_as_empirical_astro_prediction':False,'rules':rules}
dump('RULES.json',R)
ids={r['source_local_id']:r['id'] for r in rules}
M={'batch':'B03a','status':'LOCALLY_ACCEPTED_SOURCE_TO_DOCUMENTARY_REVERSE_MAP',
 'source_spans':[{**s,'canonical_record_ids':[ids[k] for k in s['mapped_source_ids']]}
                  for s in C['visual_source_spans']],
 'span_count':17,'mapped_unique_source_units':32,
 'blind_independent_complete_transcription':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M)
S={'batch':'B03a','status':'LOCALLY_ADMITTED_ORIGINAL_SOURCE_ORDER',
 'source_original_pdf_pages':[411,412,413],
 'opening':'PDF411 below LIV divider','closing':'PDF413 above LVI divider',
 'first_record':3172,'last_record':3203,'record_count':32,'source_spans':17,
 'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'record_number':r['record_number'],'original_pdf_pages':r['original_pdf_pages'],
             'role':r['role']} for r in rules],'empirical_evidence_counted':0}
dump('SOURCE_ORDER.json',S)
U['status']='RETAINED_AT_LOCAL_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03a','status':'CHAPTER_LV_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_RELEASE_AND_PUBLICATION',
 'kind':'HISTORICAL_DOCUMENTARY_SOURCE_ONLY','documentary_accepted_locally':True,
 'whole_chapter_lv_complete_at_documentary_source_level':True,
 'original_full_pdf_sha256':W['complete_original_pdf_sha256'],
 'previous_accepted_lilly':3171,'new_documentary_records':32,
 'first_record':'R3172','last_record':'R3203',
 'lilly_if_published':3203,'ptolemy_retained':1066,'combined_if_published':4269,
 'original_source_reverse_spans':17,'source_uncertainties_retained':16,
 'cross_page_unit_count':sum(len(r['original_pdf_pages'])>1 for r in rules),
 'fully_diplomatic_second_reader_done':False,
 'new_empirical_astrological_predictions_validated':0,
 'new_authenticated_partnership_cases':0,
 'runtime_promotions':0,'canonical_published':False}
for p,k in [('RULES.json','rules_sha256'),
            ('SOURCE_ORDER.json','source_order_sha256'),
            ('UNRESOLVED.json','unresolved_sha256'),
            ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','source_reverse_map_sha256'),
            ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','source_review_sha256')]:
 A[k]=H(p)
dump('ACCEPTANCE.json',A)
print({'batch':'B03a','locally_admitted':32,'first':3172,'last':3203,
'accepted_total_if_published':3203,'combined_if_published':4269,
'sha':A['rules_sha256']})
