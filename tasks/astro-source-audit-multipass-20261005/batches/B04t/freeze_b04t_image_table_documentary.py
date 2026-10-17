from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
j=lambda name:json.loads((B/name).read_text())
def put(name,obj):(B/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
h=lambda file:hashlib.sha256((B/file).read_bytes()).hexdigest()
files=['RULES.json','ACCEPTANCE.json','SOURCE_ORDER.json','UNRESOLVED.json','CLAIM_LEDGER.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/x).exists() for x in files)
idx=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=j('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows'];M=j('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')['source_spans']
W=j('SOURCE_WINDOW_MANIFEST.json');S=j('TABLE_PAGE_SOURCE_SCHEMA_20261017.json');U=j('UNRESOLVED_NUMERIC_AND_SOURCE_LIMITS.json')
assert idx['records_count']==5629 and idx['batches'][-1]['id']=='B04s'
assert idx['next']['chapter']=='PLANETARY_HOUR_TABLE' and idx['next']['pdf_page']==508
assert idx['source_sha256']==W['original_full_pdf_sha256']
assert len(D)==10 and len(M)==9 and len(W['original_images'])==9 and len(U['issues'])==18
assert not S['numeric_hours_all_cells_digitized']
for x in W['original_images']:
 assert h(x['path'])==x['sha256'] and (B/x['path']).stat().st_size==x['bytes']
local=[d['source_local_id'] for d in D];maps=[x for m in M for x in m['mapped_local_ids']]
assert len(maps)==len(set(maps))==10 and sorted(local)==sorted(maps)
records=[{**d,'id':f'R{n}','record_number':n,'global_record_number':n,
 'historical_documentary_accepted':True,'source_numeric_cells_fully_transcribed':False,
 'empirically_validated_prediction':False,'runtime_model_promoted':False}
 for n,d in enumerate(D,5630)]
assert [x['record_number'] for x in records]==list(range(5630,5640))
R={'batch':'B04t','kind':'ORIGINAL_1647_PLANETARY_HOUR_TABLE_PAGE_WITNESSES_NOT_MACHINE_DIGITIZED',
 'status':'LOCALLY_ACCEPTED_IMAGE_DOCUMENTARY_ONLY','record_count':10,
 'first_record':5630,'last_record':5639,'original_table_leaf_records':8,
 'next_chapter_navigation_records':2,'original_pdf_pages':list(range(508,517)),
 'source_spans':9,'source_uncertainties':18,'original_image_table_pages_all_preserved':True,
 'source_numeric_cell_data_fully_transcribed':False,
 'independently_verified_all_numeric_cells':False,'estimated_numeric_boundary_cells':1488,
 'empirically_validated_predictions':0,'runtime_promotions':0,'rules':records}
put('RULES.json',R)
idmap={r['source_local_id']:r['id'] for r in records}
put('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',{
 'batch':'B04t','span_count':9,'mapped_source_records':10,
 'source_spans':[{**m,'accepted_global_record_ids':[idmap[x] for x in m['mapped_local_ids']]} for m in M]})
put('SOURCE_ORDER.json',{'batch':'B04t','record_count':10,'first_record':5630,'last_record':5639,
 'original_pdf_pages':list(range(508,517)),
 'record_ids':[r['id'] for r in records]})
put('UNRESOLVED.json',U)
put('CLAIM_LEDGER.json',{'batch':'B04t','source_documentary_units':10,
 'table_pages':8,'navigation_records':2,'source_page_spans':9,
 'all_table_image_sha256_preserved':True,
 'estimated_numeric_hours_cells':1488,'verified_numeric_cells_digitized':False,
 'independent_predictive_validations':0,'runtime_promotions':0})
A={'batch':'B04t','status':'LOCAL_IMAGE_DOCUMENTARY_ACCEPTED_NUMERIC_DIGITIZATION_OPEN',
 'previous_lilly':5629,'new_documentary_records':10,'lilly_if_published':5639,
 'retained_ptolemy':1066,'combined_if_published':6705,
 'next_chapter':'XCVIII','next_printed_chapter':'XCVII',
 'next_original_pdf':516,'original_images_complete':True,
 'numeric_cell_transcription_complete':False,
 'next_numeric_transcription_still_open':True,
 'independent_empirical_validations':0,'runtime_promotions':0,'original_pdf_sha256':W['original_full_pdf_sha256']}
for file,key in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_sha256'),
 ('TABLE_PAGE_SOURCE_SCHEMA_20261017.json','table_schema_sha256'),
 ('TABLE_SOURCE_FIRST_AUDIT_20261017.md','table_audit_sha256')]:A[key]=h(file)
put('ACCEPTANCE.json',A)
print(json.dumps(A,indent=2))
