#!/usr/bin/env python3
"""Source-first 1647 parsonage worked case documentary admission, not validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
outs=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/n).exists() for n in outs)
IDX=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json');M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json');U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
assert IDX['records_count']==4508 and IDX['batches'][-1]['id']=='B03x'
assert IDX['next']['chapter']=='LXXIX' and IDX['next']['pdf_page']==471
assert IDX['source_sha256']==W['original_full_pdf_sha256']
assert D['source_units']==41 and M['span_count']==7 and len(U['issues'])==17
assert C['independent_predictions_validated']==C['independent_authenticated_outcomes']==C['runtime_promotions']==0
assert C['source_author_self_reported_failure_outcome']==1
for e in W['original_images']:
 assert H(e['path'])==e['sha256'] and (B/e['path']).stat().st_size==e['bytes']
assert (B/'SOURCE_FIRST_IMAGE_AUDIT_20261016.md').is_file()
ids=[r['source_local_id'] for r in D['rows']]
mapped=[k for s in M['source_spans'] for k in s['mapped_local_ids']]
assert len(ids)==len(mapped)==41 and sorted(ids)==sorted(mapped)
byid={r['source_local_id']:r for r in D['rows']}
assert all(s['original_pdf_pages']==byid[k]['original_pdf_pages'] for s in M['source_spans'] for k in s['mapped_local_ids'])
assert all(r['chapter']=='LXXIX' for r in D['rows'][:-2])
assert all(r['chapter']=='LXXX_NAVIGATION_ONLY' for r in D['rows'][-2:])
rs=[]
for n,r in enumerate(D['rows'],start=4509):
 rs.append({**r,'id':f'R{n}','record_number':n,'global_record_number':n,
  'historical_documentary_accepted':True,'accepted_for_primary_historical_text_reference':True,
  'independently_authenticated_parsonage_case':False,
  'empirically_validated_prediction':False,'runtime_model_promoted':False})
assert [r['record_number'] for r in rs]==list(range(4509,4550))
R={'batch':'B03y','kind':'ORIGINAL_HISTORICAL_PARSONAGE_CASE_SOURCE_ONLY',
 'status':'DOCUMENTARY_SOURCE_ACCEPTED_LOCALLY_PENDING_PUBLICATION',
 'documentary_accepted_locally':True,'record_count':41,'first_record':4509,'last_record':4549,
 'substantive_lxxix_source_annotations':39,'next_heading_navigation_only':2,
 'original_pdf_pages':[471,472,473],'source_reverse_passages':7,
 'original_unresolved_limits':17,'authorial_retrospective_failure_report':1,
 'independently_verified_parsonage_outcomes':0,'new_empirically_validated_predictions':0,
 'runtime_promotions':0,'rules':rs}
dump('RULES.json',R)
G={r['source_local_id']:r['id'] for r in rs}
dump('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',{'batch':'B03y',
 'source_spans':[{**s,'accepted_global_record_ids':[G[k] for k in s['mapped_local_ids']]}
  for s in M['source_spans']],
 'span_count':7,'mapped_source_records':41})
dump('SOURCE_ORDER.json',{'batch':'B03y','first_record':4509,'last_record':4549,
 'record_count':41,'original_pdf_pages':[471,472,473],
 'records':[{'record_number':r['record_number'],'pdf_pages':r['original_pdf_pages'],
             'role':r['role']} for r in rs],
 'independent_empirical_results':0})
U['status']='ORIGINAL_SOURCE_UNCERTAINTIES_RETAINED_AT_ADMISSION'
dump('UNRESOLVED.json',U)
A={'batch':'B03y','kind':'AUTHOR_RETROSPECTIVE_PARSONAGE_DENIAL_SOURCE_NOT_EMPIRICAL',
 'status':'LOCAL_DOCUMENTARY_ADMITTED_PENDING_RELEASE_REMOTE',
 'documentary_accepted_locally':True,'prior_lilly_accepted':4508,
 'new_documentary_records':41,'first_record':'R4509','last_record':'R4549',
 'lilly_if_published':4549,'ptolemy_retained':1066,'combined_if_published':5615,
 'original_pdf_sha256':W['original_full_pdf_sha256'],
 'original_body_pdf_pages':[471,472],'following_heading_pdf':473,
 'source_reverse_passages':7,'original_unresolved_limits':17,
 'next_chapter':'LXXX','next_original_pdf':473,
 'authorial_unverified_outcome_reports':1,'independently_verified_parsonage_outcomes':0,
 'new_empirically_validated_predictions':0,'runtime_model_promotions':0,
 'original_full_independent_diplomatic_transcription':False,
 'remote_canonical_published':False}
for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')]:
 A[k]=H(f)
dump('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B03y','local_documentary_records':41,
 'lilly_if_published':4549,'combined_if_published':5615,
 'retained_uncertainties':17,'independent_validations':0}))
