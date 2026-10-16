from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
assert not any((B/n).exists() for n in ('RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json'))
I=json.loads((ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json').read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows'];M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')['source_spans']
W=J('SOURCE_WINDOW_MANIFEST.json');U=J('UNRESOLVED_SOURCE_LIMITS.json')
assert I['records_count']==5113 and I['batches'][-1]['id']=='B04g'
assert I['next']['chapter']=='LXXXVIII' and I['next']['printed_chapter_numeral']=='LXXXVII'
assert I['source_sha256']==W['original_full_pdf_sha256']
assert len(D)==48 and len(M)==7 and len(U['issues'])==21
assert all(H(x['path'])==x['sha256'] for x in W['original_images'])
names=[v for g in M for v in g['mapped_local_ids']]
assert len(names)==len(set(names))==48
rs=[{**r,'id':f'R{n}','record_number':n,'global_record_number':n,
 'historical_documentary_accepted':True,'accepted_for_primary_historical_text_reference':True,
 'independently_authenticated_hope_fulfilment':False,
 'empirically_validated_prediction':False,'runtime_model_promoted':False}
 for n,r in enumerate(D,start=5114)]
assert [r['record_number'] for r in rs]==list(range(5114,5162))
R={'batch':'B04h','kind':'1647_ELEVENTH_HOUSE_HOPES_HISTORICAL_SOURCE_ONLY',
 'status':'LOCAL_DOCUMENTARY_ADMISSION_PENDING_PUBLICATION',
 'documentary_accepted_locally':True,'record_count':48,
 'first_record':5114,'last_record':5161,'substantive_eleventh_house_units':46,
 'following_chapter_navigation_only':2,'source_passages':7,
 'source_unresolved_limits':21,'original_pdf_pages':[491,492,493],
 'original_printed_chapter':'LXXXVII','editorial_alias':'LXXXVIII',
 'different_complete_partial_probable_or_harm_outcomes':True,
 'independently_verified_hope_outcomes':0,'empirically_validated_predictions':0,
 'runtime_promotions':0,'rules':rs}
put('RULES.json',R)
lookup={r['source_local_id']:r['id'] for r in rs}
put('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',{'batch':'B04h','span_count':7,
 'source_spans':[{**g,'accepted_global_record_ids':[lookup[k] for k in g['mapped_local_ids']]} for g in M],
 'mapped_source_records':48})
put('SOURCE_ORDER.json',{'batch':'B04h','record_count':48,'first_record':5114,'last_record':5161,
 'records':[{'record_number':r['record_number'],'role':r['role'],
 'printed_chapter':r['original_printed_chapter_numeral'],'pdf_pages':r['original_pdf_pages']} for r in rs],
 'new_empirical_validations':0})
U['status']='SOURCE_LIMITS_RETAINED_AT_ADMISSION';put('UNRESOLVED.json',U)
A={'batch':'B04h','status':'DOCUMENTARY_ACCEPTED_LOCAL_PENDING_ARCHIVE_REMOTE',
 'prior_lilly_accepted':5113,'new_documentary_records':48,
 'first_record':'R5114','last_record':'R5161','lilly_if_published':5161,
 'retained_ptolemy':1066,'combined_if_published':6227,
 'original_pdf_sha256':W['original_full_pdf_sha256'],
 'source_passages':7,'source_unresolved_limits':21,
 'original_printed_chapter':'LXXXVII','editorial_alias':'LXXXVIII',
 'next_original_printed_chapter':'LXXXVIII','next_editorial_chapter':'LXXXIX',
 'next_original_pdf':493,'independently_verified_hope_outcomes':0,
 'new_empirically_validated_predictions':0,'runtime_model_promotions':0,
 'remote_canonical_published':False}
for f,k in (('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
 ('UNRESOLVED.json','unresolved_sha256'),
 ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
 ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')):A[k]=H(f)
put('ACCEPTANCE.json',A)
print(json.dumps({'batch':'B04h','new_records':48,'projected_combined':6227}))
