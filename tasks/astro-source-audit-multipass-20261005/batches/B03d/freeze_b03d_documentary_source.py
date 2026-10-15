#!/usr/bin/env python3
"""Admit original 1647 Chapter LVIII as historical source only."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(f,obj):(B/f).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
out=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','ACCEPTANCE.json']
assert not any((B/f).exists() for f in out)
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
O=J('SOURCE_ORDER_DRAFT.json')
L=J('CLAIM_LEDGER.json')
assert I['records_count']==3322 and I['batches'][-1]['id']=='B03c'
assert I['next']['chapter']=='LVIII' and I['next']['pdf_page']==417
assert I['source_sha256']==W['source_full_pdf_sha256']
assert D['units']==38 and C['span_count']==18 and len(U['issues'])==14
assert [r['source_local_id'] for r in D['rows']]==O['ordered_ids']
assert sorted(k for s in C['source_spans'] for k in s['mapped_source_local_ids'])==sorted(O['ordered_ids'])
assert not D['independent_diplomatic_full_transcription_claimed']
assert L['new_globally_accepted']==0 and L['new_predictive_validations']==0
for v in W['images']:
 assert H(v['relative_path'])==v['sha256']
 assert (B/v['relative_path']).stat().st_size==v['bytes']
rules=[]
for n,r in enumerate(D['rows'],start=3323):
 rr={**r,'id':f'R{n}','record_number':n,'global_record_number':n,
 'source_first_provisional':False,'historical_documentation_accepted':True,
 'source_record_admitted_for_documentary_reference':True,
 'observed_real_adversary_cases':0,
 'empirical_predictive_validation':False,
 'active_personality_or_honesty_classifier':False,
 'runtime_model_promoted':False}
 rules.append(rr)
assert [r['record_number'] for r in rules]==list(range(3323,3361))
assert all(r['chapter']=='LVIII' for r in rules[:-1])
assert rules[-1]['chapter']=='LIX_HEADING_ONLY'
R={'batch':'B03d','kind':'HISTORICAL_DOCUMENTARY_SOURCE_ONLY',
   'status':'LOCALLY_ACCEPTED_CHAPTER_LVIII_PENDING_PUBLICATION',
   'documentary_accepted_locally':True,'whole_chapter_lviii_complete_at_source_level':True,
   'original_full_pdf_sha256':W['source_full_pdf_sha256'],
   'original_pdf_pages':[417,418,419],
   'first_record':3323,'last_record':3360,'record_count':38,
   'substantive_lviii_units':37,'next_heading_navigation_only':1,
   'source_reverse_passages':18,'retained_uncertainties':14,
   'independent_blind_diplomatic_second_transcription':False,
   'authenticated_person_level_adversary_observations':0,
   'new_predictive_accuracy_validation':0,
   'runtime_model_promotions':0,'rules':rules}
dump('RULES.json',R)
by={r['source_local_id']:r['id'] for r in rules}
MAP={'batch':'B03d','status':'LOCALLY_ACCEPTED_IMAGE_TO_RECORD_REVERSE_MAP',
     'source_spans':[{**s,'canonical_record_ids':[by[k] for k in s['mapped_source_local_ids']]}
                    for s in C['source_spans']],
     'span_count':18,'mapped_unique_historical_source_records':38,
     'blind_independent_diplomatic_reader_done':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',MAP)
ORDER={'batch':'B03d','status':'LOCALLY_ACCEPTED_SOURCE_ORDER',
 'first_record':3323,'last_record':3360,'record_count':38,
 'source_original_pdf_pages':[417,418,419],'source_reverse_passages':18,
 'opening':'PDF417 below LVII divider','closing':'PDF419 above LIX divider',
 'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'number':r['record_number'],'original_pages':r['original_pdf_pages'],
             'role':r['role']} for r in rules],
 'independently_validated_real_cases':0}
dump('SOURCE_ORDER.json',ORDER)
U['status']='RETAINED_UNRESOLVED_AT_LOCAL_ACCEPTANCE'
dump('UNRESOLVED.json',U)
A={'batch':'B03d','kind':'HISTORICAL_1647_SOURCE_ONLY',
 'status':'LOCALLY_SOURCE_ACCEPTED_PENDING_RELEASE_AND_REMOTE_PUBLICATION',
 'documentary_accepted_locally':True,
 'whole_chapter_lviii_documentary_source_accepted':True,
 'original_full_pdf_sha256':W['source_full_pdf_sha256'],
 'original_pdf_pages':[417,418,419],
 'previous_accepted_lilly':3322,'new_historical_documentary_units':38,
 'first_record':'R3323','last_record':'R3360',
 'lilly_if_published':3360,'ptolemy_retained':1066,
 'combined_if_published':4426,'source_reverse_passages':18,
 'retained_text_uncertainties':14,'substantive_chapter_units':37,
 'one_next_chapter_boundary':1,
 'cross_page_units':sum(len(r['original_pdf_pages'])>1 for r in rules),
 'complete_blind_second_diplomatic_transcription':False,
 'new_validated_predictions':0,'real_enemy_cases_authenticated':0,
 'runtime_promotions':0,'canonical_publication_verified':False}
for f,key in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','visual_review_sha256')]:
 A[key]=H(f)
dump('ACCEPTANCE.json',A)
print({'batch':'B03d','local_source_units':38,'first':3323,'last':3360,
 'combined_if_published':4426,'reverse_spans':18,'uncertainties':14,'empirical':0})
