#!/usr/bin/env python3
"""Freeze locally reviewed B02y as documentary source only; not publication."""
import hashlib
import json
from pathlib import Path

B=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
j=lambda f:json.loads((B/f).read_text(encoding='utf-8'))
dump=lambda f,o:(B/f).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
FILES=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','CLAIM_LEDGER_ACCEPTED_LOCAL.json','ACCEPTANCE.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/f).exists() for f in FILES),'Freeze is one-time; guard against overwrite'
D=j('SOURCE_FIRST_CLAUSES_DRAFT.json');C=j('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
O=j('SOURCE_ORDER_DRAFT.json');W=j('SOURCE_WINDOW_MANIFEST.json')
U=j('UNRESOLVED_SOURCE_LIMITS.json');L=j('CLAIM_LEDGER.json')
assert D['record_count']==76 and C['span_count']==27 and len(U['points'])==16
assert W['previously_accepted_lilly_count']==3071 and W['original_pdf_pages']==list(range(405,411))
assert [s['span_id'] for s in C['source_spans']]==[f'LIII-S{i:03}' for i in range(1,28)]
assert len(set(x['local_id'] for x in D['rows']))==76
for f in W['images']:
 assert sha(f['relative_path'])==f['sha256'] and len((B/f['relative_path']).read_bytes())==f['bytes']
assert (B/'LIII_SOURCE_FIRST_IMAGE_AUDIT_20261015.md').is_file()
rules=[]
for n,r in enumerate(D['rows'],start=3072):
 rr={**r,'id':f'R{n}','record_number':n,'global_record_number':n,
     'is_provisional':False,'accepted_historical_documentary':True,
     'source_record_admitted_for_documentary_reference':True,
     'accepted_as_empirical_prediction':False,
     'empirically_verified_case':False,
     'model_runtime_promotion':False,'safe_for_real_person_prognosis':False}
 rules.append(rr)
assert rules[-1]['record_role']=='next_heading_boundary'
R={'batch':'B02y','kind':'HISTORICAL_SOURCE_DOCUMENTARY_ONLY',
   'status':'CHAPTER_LIII_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_PUBLICATION',
   'documentary_accepted_locally':True,'whole_chapter_liii_source_intake_complete':True,
   'source_pdf_sha256':W['original_full_pdf_sha256'],
   'source_pages':list(range(405,411)),'first_record':3072,'last_record':3147,
   'record_count':76,'substantive_chapter_liii_units':75,'next_chapter_navigation_only_units':1,
   'source_reverse_passages':27,'source_uncertainties_retained':16,'rules':rules,
   'blind_independent_diplomatic_second_transcription':False,
   'accepted_as_empirical_astro_prediction':False,
   'independently_authenticated_historical_cases':0,'runtime_promotions':0}
dump('RULES.json',R)
rid_by_local={r['local_id']:r['id'] for r in rules}
mapped=[]
for s in C['source_spans']:
 mapped.append({**s,'canonical_record_ids':[rid_by_local[i] for i in s['draft_local_ids']],
                'documentary_image_source_admitted_locally':True})
M={'batch':'B02y','status':'LOCAL_DOCUMENTARY_ORIGINAL_IMAGE_REVERSE_MAP',
   'source_spans':mapped,'span_count':len(mapped),
   'mapped_unique_documentary_units':len(rules),
   'independent_blind_original_transcription_done':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M)
S={'batch':'B02y','status':'LOCALLY_ACCEPTED_ORIGINAL_SOURCE_ORDER',
   'original_source_pages':list(range(405,411)),'opening':'PDF405 below LII divider',
   'closing':'PDF410 above LIV divider','first_record':3072,'last_record':3147,
   'record_count':76,'source_spans':27,
   'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
   'records':[{'record_number':r['record_number'],
               'pdf_pages':r['original_pdf_pages'],'kind':r['record_role']} for r in rules],
   'empirical_evidence_counted':0}
dump('SOURCE_ORDER.json',S)
U['status']='RETAINED_AT_LOCAL_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
CL={**L,'status':'LOCALLY_ACCEPTED_DOCUMENTARY_NOT_YET_GLOBALLY_PUBLISHED',
    'new_documentary_units_locally_admitted':76,
    'new_globally_accepted_records':0,
    'globally_counted_only_after_published_git_ref_and_readback':True}
dump('CLAIM_LEDGER_ACCEPTED_LOCAL.json',CL)
A={'batch':'B02y','kind':'HISTORICAL_SOURCE_DOCUMENTARY_ONLY',
   'status':'CHAPTER_LIII_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_RELEASE_AND_GIT_PUBLICATION',
   'documentary_accepted_locally':True,'whole_chapter_liii_complete_at_documentary_source_level':True,
   'original_full_pdf_sha256':W['original_full_pdf_sha256'],
   'original_pdf_pages':list(range(405,411)),
   'opening':'PDF405 BELOW LII divider','closing':'PDF410 ABOVE LIV divider',
   'previous_accepted_lilly':3071,'new_documentary_records':76,
   'first_record':'R3072','last_record':'R3147',
   'lilly_if_published':3147,'ptolemy_retained':1066,
   'combined_if_published':4213,'original_source_reverse_spans':27,
   'source_uncertainties_retained':16,
   'cross_page_unit_count':len([r for r in rules if len(r['original_pdf_pages'])>1]),
   'author_original_images_visually_reviewed':True,
   'fully_diplomatic_second_reader_done':False,
   'independent_blind_original_transcription_done':False,
   'empirical_predictions_validated':0,'real_judge_bribery_trials_authenticated':0,
   'runtime_promotions':0,'canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
             ('UNRESOLVED.json','unresolved_sha256'),
             ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','original_to_record_source_map_sha256'),
             ('CLAIM_LEDGER_ACCEPTED_LOCAL.json','claim_ledger_sha256'),
             ('LIII_SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_notes_sha256')]:
 A[k]=sha(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'status':A['status'],'new_documentary_units_locally':76,
                  'lilly_if_published':3147,
                  'ptolemy_retained':1066,'combined_if_published':4213,
                  'new_empirical_predictions':0,'runtime_promotions':0,
                  'rules_sha256':A['rules_sha256']}))
