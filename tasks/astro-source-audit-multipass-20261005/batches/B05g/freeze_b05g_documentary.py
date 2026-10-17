from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;R=B.parents[3]
index=R/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
I=json.loads(index.read_text());S=json.loads((B/'SOURCE_FIRST_PROVISIONAL_20261017.json').read_text())
assert I['records_count']==6560 and I['batches'][-1]['id']=='B05f' and I['next']['pdf_page']==573
assert len(S['provisional_annotations'])==31 and len(S['source_passages'])==8
assert len([r for r in S['provisional_annotations'] if r['role']=='next_navigation'])==2
assert len({r['id'] for r in S['provisional_annotations']})==31
records=[]
for n,r in enumerate(S['provisional_annotations'],6561):
 records.append({**r,'record_number':n,'id':f'R{n}',
  'source_local_id':r['id'],'accepted':True,'historical_documentary_accepted':True,
  'validated_personality_prediction':False,'runtime_model_promoted':False})
# Refuse to count these as measured people or psychometric labels.
rules={'batch':'B05g','status':'HISTORICAL_DOCUMENTARY_LOCALLY_ADMITTED','record_count':31,
 'first_record':6561,'last_record':6591,'original_printed_chapter':'CVIII','editorial_chapter':'CIX',
 'source_passage_groups':8,'substantive_historical_annotations':29,'next_chapter_navigation':2,
 'original_pdf_pages':[573,574,575,576,577,578],
 'original_source_paraphrase_qualification':'Second full diplomatic transcription and trait-cell completeness not claimed',
 'original_trait_tables_not_empirically_validated':True,
 'independent_human_personality_validation':0,'empirical_validations':0,'runtime_promotions':0,
 'rules':records}
(B/'RULES.json').write_text(json.dumps(rules,indent=2)+'\n')
sha=hashlib.sha256((B/'RULES.json').read_bytes()).hexdigest()
A={'batch':'B05g','local_historical_annotations':31,'prior_lilly':6560,'lilly_if_published':6591,
'ptolemy_retained':1066,'combined_if_published':7657,'accepted_rules_sha256':sha,
 'source_pages':[573,574,575,576,577,578],'next_heading_page':577,
 'following_printed_chapter':'CIX','following_editorial_chapter':'CX',
 'no_independent_personality_evidence':True,'empirical_validations':0,'runtime_promotions':0}
(B/'ACCEPTANCE.json').write_text(json.dumps(A,indent=2)+'\n')
print('locally admitted',len(records),'expected new Lilly',6591,'combined',7657)
