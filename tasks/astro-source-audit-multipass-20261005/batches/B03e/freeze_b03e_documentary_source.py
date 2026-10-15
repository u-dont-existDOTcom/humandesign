#!/usr/bin/env python3
"""Admit original 1647 chart-and-case source, NOT validated event prediction."""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,v):(B/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
out=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','ACCEPTANCE.json']
assert not any((B/n).exists() for n in out)
idx=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json');C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json');U=J('UNRESOLVED_SOURCE_LIMITS.json')
O=J('SOURCE_ORDER_DRAFT.json');L=J('CLAIM_LEDGER.json')
assert idx['records_count']==3360 and idx['batches'][-1]['id']=='B03d'
assert idx['next']['chapter']=='LIX' and idx['next']['pdf_page']==419
assert idx['source_sha256']==W['source_full_pdf_sha256']
assert D['source_units']==58 and C['span_count']==25 and len(U['issues'])==18
assert [r['source_local_id'] for r in D['rows']]==O['ordered_local_ids']
assert sorted(k for s in C['source_spans'] for k in s['mapped_source_local_ids'])==sorted(O['ordered_local_ids'])
assert L['new_globally_accepted']==L['new_empirical_predictions_validated']==0
for im in W['images']:
 assert H(im['path'])==im['sha256'] and (B/im['path']).stat().st_size==im['size_bytes']
assert D['rows'][-1]['chapter']=='LX_HEADING_ONLY'
rules=[]
for n,r in enumerate(D['rows'],start=3361):
 rr={**r,'id':f'R{n}','record_number':n,'global_record_number':n,
 'historical_documentation_admitted':True,'source_record_admitted_for_documentary_reference':True,
 'real_outcome_independently_authenticated':False,
 'empirical_astrology_prediction_validated':False,'runtime_model_promoted':False}
 rules.append(rr)
assert [r['record_number'] for r in rules]==list(range(3361,3419))
assert all(r['chapter']=='LIX' for r in rules[:-1])
R={'batch':'B03e','kind':'1647_DOCUMENTARY_WORKED_CASE_NOT_VALIDATION',
 'status':'LOCALLY_ADMITTED_CHAPTER_LIX_SOURCE_NOT_REMOTE_PUBLISHED',
 'documentary_accepted_locally':True,'whole_chapter_lix_original_source_intake_complete':True,
 'source_full_pdf_sha256':W['source_full_pdf_sha256'],
 'original_body_pdf_pages':[419,420,421,422],
 'next_header_pdf_page':423,
 'first_record':3361,'last_record':3418,'record_count':58,
 'chapter_lix_substantive_annotations':57,'next_heading_navigation_only':1,
 'source_reverse_passages':25,'source_ambiguities_retained':18,
 'complete_blind_diplomatic_second_reader':False,
 'independent_historical_outcome_confirmation':0,
 'pre_outcome_frozen_horoscope_forecasts':0,
 'empirically_validated_predictive_results':0,
 'runtime_promotions':0,'rules':rules}
dump('RULES.json',R)
by={r['source_local_id']:r['id'] for r in rules}
M={'batch':'B03e','status':'LOCALLY_ADMITTED_IMAGE_TO_RECORD_MAP',
 'source_spans':[{**s,'canonical_record_ids':[by[x] for x in s['mapped_source_local_ids']]}
     for s in C['source_spans']],
 'span_count':25,'mapped_unique_documentary_units':58,
 'full_independent_second_diplomatic_reader':False}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',M)
ORDER={'batch':'B03e','status':'LOCALLY_ACCEPTED_SOURCE_ORDER',
 'first_record':3361,'last_record':3418,'record_count':58,
 'original_body_pdf_pages':[419,420,421,422],'next_heading_pdf':423,
 'opening':'PDF419 below LVIII divider',
 'closing':'PDF422 chapter body, PDF423 LX header navigation',
 'source_reverse_passages':25,
 'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'records':[{'record_number':r['record_number'],'source_pdf_pages':r['original_pdf_pages'],
             'kind':r['role']} for r in rules],
 'independent_real_outcomes_verified':0}
dump('SOURCE_ORDER.json',ORDER)
U['status']='RETAINED_DURING_LOCAL_DOCUMENTARY_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03e','status':'LOCALLY_ACCEPTED_LIX_HISTORIC_DOCUMENTARY_PENDING_RELEASE_AND_PUBLICATION',
 'kind':'HISTORICAL_WORKED_CASE_SOURCE_ONLY',
 'documentary_accepted_locally':True,'whole_chapter_lix_documentary_accepted':True,
 'source_full_pdf_sha256':W['source_full_pdf_sha256'],
 'prior_accepted_lilly':3360,'added_documentary_units':58,
 'first_record':'R3361','last_record':'R3418',
 'lilly_if_published':3418,'ptolemy_retained':1066,'combined_if_published':4484,
 'source_reverse_passages':25,'retained_ambiguities':18,
 'substantive_lix_records':57,'lx_header_only':1,
 'original_case_date_witness':'16 June 1646 chart in original PDF419',
 'distinct_next_case_date':'11 June 1646 chart in PDF423',
 'original_chart_positions_machine_reconstructed':False,
 'blind_second_diplomatic_transcription':False,
 'independently_confirmed_marriage_outcome':0,
 'pre_outcome_frozen_predictions_count':0,
 'empirical_astrology_predictive_validations':0,
 'runtime_model_promotions':0,'canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),
 ('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','source_audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print({'batch':'B03e','historical_units_locally_admitted':58,
 'lilly_if_published':3418,'combined_if_published':4484,
 'source_passages':25,'retained_limits':18,'empirical_predictions':0,
 'rules_sha256':A['rules_sha256']})
