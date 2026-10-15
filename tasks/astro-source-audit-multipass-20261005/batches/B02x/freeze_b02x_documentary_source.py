"""Documentary-only local admission from frozen original-image-first B02x data."""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256((B/p).read_bytes()).hexdigest()
files=('RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','CLAIM_LEDGER.json','ACCEPTANCE.json')
assert not any((B/f).exists() for f in files)
D=json.loads((B/'SOURCE_FIRST_CLAUSES_DRAFT.json').read_text())
P=json.loads((B/'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json').read_text())
W=json.loads((B/'SOURCE_WINDOW_MANIFEST.json').read_text())
U=json.loads((B/'UNRESOLVED_DRAFT.json').read_text())
assert D['provisional_editorial_units']==55
assert [r['record_number'] for r in D['rows']]==list(range(3017,3072))
assert P['mapped_unique_provisional_units']==55 and P['span_count']==42
assert not P['accepted'] and not D['empirical_validations']
assert len(U['issues'])==13
for v in W['original_source_scans']:
 assert sha(v['relative_path'])==v['sha256']
assert sum(x['role']=='boundary' for x in D['rows'])==1
assert D['rows'][-1]['claim_kind']=='next_chapter_hunting_boundary'
assert sum(x['role']=='margin' for x in D['rows'])==1
assert sum(x['role']=='converse' for x in D['rows'])==3
assert all(x['accepted'] is False and x['historical_source_only'] and not x['empirical_accuracy_verified'] for x in D['rows'])
A={'batch':'B02x','kind':'HISTORICAL_SOURCE_DOCUMENTARY_ONLY',
'status':'CHAPTER_LII_SOURCE_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_RELEASE_AND_GIT_PUBLICATION',
'documentary_accepted_locally':True,'whole_chapter_lii_complete_at_documentary_source_level':True,
'original_pdf_sha256':W['source_full_pdf_sha256'],
'original_pdf_pages':[403,404,405],'last_page_position':'ABOVE divider before Chapter LIII',
'original_printed_pages':[369,370,371],
'last_chapter_heading_on_boundary':'CHAP LIII Of Hunting; body excluded',
'previous_accepted_lilly':3016,'new_documentary_records':55,'chapter_lii_source_units':54,'next_chapter_boundary_only_units':1,
'first_record':'R3017','last_record':'R3071',
'lilly_if_integrated':3071,'ptolemy_retained':1066,'combined_documentary_if_integrated':4137,
'original_source_reverse_spans':42,'source_uncertainties_retained':13,
'literal_e_contra_abbreviations':3,'cross_page_records':2,
'fully_diplomatic_second_reader_done':False,'independent_blind_original_transcription_done':False,
'new_empirical_astro_validations':0,'verified_criminal_legal_health_outcomes':0,
'runtime_promotions':0,'canonical_published':False}
R={'batch':'B02x','status':'HISTORICAL_DOCUMENTARY_ACCEPTED_LOCALLY',
'documentary_accepted_locally':True,
'whole_chapter_lii_complete_at_documentary_source_level':True,
'source_pdf_sha256':W['source_full_pdf_sha256'],
'source_pages':[403,404,405],'next_chapter_boundary_pdf':405,
'first_record':3017,'last_record':3071,'record_count':55,
'substantive_chapter_lii_units':54,'next_chapter_navigation_only_units':1,
'rules':[{**r,'source_record_admitted_for_documentary_reference':True,
'accepted_as_empirical_prediction':False,'accepted':False} for r in D['rows']],
'accepted_as_empirical_astro_prediction':False,'independently_authenticated_historical_cases':0,
'measured_predictive_accuracy':False,'runtime_promotions':0,
'source_note':'Editorial normalized original source claims only; 13 retained source issues; original-to-record map 42 visual source passages; three unresolved e-contra short inverses. Not a full diplomatic independently blinded transcription.'}
(B/'RULES.json').write_text(json.dumps(R,indent=2,ensure_ascii=False)+'\n')
S={'batch':'B02x','status':'LOCALLY_ACCEPTED_ORIGINAL_SOURCE_ORDER','original_source_pages':[403,404,405],
'physical_boundary_only_pdf':405,'first_record':3017,'last_record':3071,
'reverse_source_map':'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','record_count':55,'source_spans':42,
'records':[{'record_number':r['record_number'],'pdf_pages':r['original_pdf_pages'],'kind':r['claim_kind'],'source_record_role':r['role']} for r in R['rules']],
'empirical_evidence_counted':0}
(B/'SOURCE_ORDER.json').write_text(json.dumps(S,indent=2,ensure_ascii=False)+'\n')
U['status']='RETAINED_AT_LOCAL_DOCUMENTARY_ADMISSION'
(B/'UNRESOLVED.json').write_text(json.dumps(U,indent=2,ensure_ascii=False)+'\n')
claim={'batch':'B02x','scope':'HISTORICAL_WILLIAM_LILLY_1647_ORIGINAL_SOURCE_ONLY','new_documentary_units':55,
'original_pdf_body_pages':[403,404,405],'empirical_predictions_validated':0,
'real_world_legal_outcomes_tested':0,'relationship_match_validations':0,
'forward_blind_rankings_tested':0,'personal_birth_chart_changes':0,'runtime_promotions':0,
'authorial_claims':'Suit success, partnership, neighbor fellowship and relocation are original historical author statements, not modern causal or forecasting evidence.'}
(B/'CLAIM_LEDGER.json').write_text(json.dumps(claim,indent=2,ensure_ascii=False)+'\n')
a_hashes={k:sha(k+'.json') for k in ('RULES','SOURCE_ORDER','UNRESOLVED','CLAIM_LEDGER')}
A.update({'rules_sha256':a_hashes['RULES'],'source_order_sha256':a_hashes['SOURCE_ORDER'],
'unresolved_sha256':a_hashes['UNRESOLVED'],'claim_ledger_sha256':a_hashes['CLAIM_LEDGER'],
'original_to_record_source_map_sha256':sha('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json'),
'notes_sha256':sha('LII_SOURCE_FIRST_INVENTORY_NOTES_20261015.md'),
'archive_extracted_tests_count':0,'source_only_tests_before_admission':20})
(B/'ACCEPTANCE.json').write_text(json.dumps(A,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'admission':A['status'],'new_source_units':55,'total_lilly_if_published':3071,
'combined_with_Ptolemy_if_published':4137,'rules_sha256':A['rules_sha256']},indent=2))
