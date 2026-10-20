#!/usr/bin/env python3
"""Guarded append-only B07bc historical source admission after portable archive tests."""
import hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-source-audit-multipass-20261005'
INDEX=T/'LILLY_SOURCE_EXTRACTION_INDEX_V1.json'; CHINA=ROOT/'tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md';LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bc_SICKNESSE_SERVANTS.md'
BACK=B/'recovery'; RECEIPT=B/'CANONICAL_PREPARE_RECEIPT_20261020.json';BRANCH='research/astro-b07bc-clxxx-sicknesse-servants-20261020'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def download_dir():
 p=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
 if p.returncode==0 and p.stdout.strip() and Path(p.stdout.strip()).is_dir() and Path(p.stdout.strip()).resolve()!=Path.home().resolve():return Path(p.stdout.strip())
 return Path.home()/'Téléchargements'
assert git('branch','--show-current')==BRANCH
assert not BACK.exists() and not LATEST.exists() and not RECEIPT.exists(), 'An interrupted admission exists; reconcile before doing anything else'
index=read(INDEX);china=read(CHINA);source=read(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json');rules=read(B/'RULES.json');accept=read(B/'ACCEPTANCE.json');scope=read(B/'TASK_SCOPE.json');archive=read(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json')
assert scope['branch']==BRANCH and scope['root_outcome']=='OPEN'
assert index['records_count']==accept['Lilly_before']==13017 and index['batches'][-1]['id']=='B07bb'
assert sum(x['records_count'] for x in index['batches'])==13017
assert index['read_numbered_chapters']==list(range(1,180)) and index['read_headed_units_count']==95
assert index['partial_numbered_chapters']==[]
assert index['next']['pdf_page']==787 and index['next']['printed_page']==753 and index['next']['chapter']=='CLXXX'
assert index['empirical_validations']==index['runtime_promotions']==0
assert len(source['records'])==len(rules['rules'])==rules['record_count']==27
assert [x['record_number'] for x in rules['rules']]==list(range(13018,13045))
assert source['next_R']==accept['next_R']=='R13045' and accept['next_chapter']=='CLXXXI'
assert china['sum_source_annotations']==355 and sha(CHINA)==scope['chinese_v7_sha256']
assert china['independently_validated_real_human_claims']==china['runtime_promotions']==0
assert accept['Ptolemy_retained']==1066 and accept['Lilly_after_if_accepted']==13044 and accept['Western_after_if_accepted']==14110
assert sha(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json')==accept['source_notes_sha256']
assert sha(B/'RULES.json')==accept['rules_sha256']
assert archive['original_index_sha256']==sha(INDEX) and archive['Chinese_V7_index_sha256']==sha(CHINA)
assert archive['member_SHA256_and_bytes_verified'] and archive['ZIP_CRC_verified'] and archive['independently_extracted_test_replays']==44
assert archive['archive_sha256']==sha(download_dir()/archive['filename'])
assert all(not x['runtime_model_promoted'] and not x['independent_actual_person_prediction_result_validated'] for x in source['records'])
# Fail closed on modifications to pre-existing canonical records or the Chinese ledger.
for f in (INDEX,CHINA,T/'batches/B07bb/RULES.json',T/'batches/B07bb/ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json'):
 relative=str(f.relative_to(ROOT));assert git('rev-parse','HEAD:'+relative)==git('hash-object',str(f)),relative
BACK.mkdir(exist_ok=False)
for f,name in ((INDEX,'LILLY_INDEX_BEFORE_B07bc.json'),(CURRENT,'CURRENT_BEFORE_B07bc.md'),(CHINA,'CHINESE_V7_BEFORE_B07bc.json')):(BACK/name).write_bytes(f.read_bytes())
index['batches'].append({'id':'B07bc','path':'batches/B07bc/RULES.json','records_count':27,'sha256':accept['rules_sha256'],'scope':'Original Lilly 1647 CLXXX sixth-house Sicknesse, Servants printed753–754/PDF787–788, compared with independently typeset 1659 printed753–754/DjVu782–783. 27 source-only historical R13018–R13044: Mercury sixth/servants lord, Saturn ascendant ruler, Moon/Oculus Taurus and Mars conditions, archaic blood corruption and fever causality, illness variation and purported mitigation, old page119/247 crossrefs, social/servant predictions and discriminatory red-haired stereotype. Original aspect glyphs, real diagnoses/records, chart parity, independent outcomes unverified. CLXXXI Marriage distinct below divider printed754/PDF788. Zero human predictions validated; zero runtime rules promoted.'})
index['records_count']=13044
index['status']='BOOK_III_CLXXX_SICKNESSE_SERVANTS_PHYSICAL_SOURCE_COVERED_NEXT_CLXXXI_MARRIAGE'
index['read_numbered_chapters'].append(180);index['read_headed_units_count']=96
index.setdefault('completed_original_source_units_with_uncertainty',[]).append({'printed_chapter':'CLXXX','editorial_ordinal':180,'chapter_heading':'Sicknesse, Servants','physical_source_start_pdf':787,'accepted_through_pdf':788,'printed_folios':[753,754],'source_batch':'B07bc','historical_start':'R13018','historical_end':'R13044','complete':True,'physical_source_span_covered':True,'source_expert_diplomatic_collation_complete':False,'original_astrological_glyphs_fully_collated':False,'independent_historical_chart_engine_parity':False,'historical_merchant_medical_outcomes_independently_verified':False,'historical_servant_behavior_independently_verified':False,'independent_human_predictions_validated':0,'runtime_model_promoted':False})
index['next']={'pdf_page':788,'printed_page':754,'chapter':'CLXXXI','printed_chapter_numeral':'CLXXXI','editorial_source_sequence_ordinal':181,'heading':'Of Marriage','include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,'position':'1647 printed754/PDF788 below clear divider from sixth-house CLXXX; seventh-house CHAP CLXXXI Of Marriage starts on same folio. Next historical note R13045. Previous medical/servants forecasts are source-only and not outcomes.','research_scope':'Original seventh-house marriage source clauses about known native. No real-person confirmation or unblinded human predictive validation.'}
index['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bc_SICKNESSE_SERVANTS.md'
index['chapter_CLXXX_historical_medical_social_claims_unverified']='Original 1647/1659 first/second printing preserved as historical sixth-house and servants predictions for known merchant. No independent real patient records, medical etiological truth, servants trust outcomes, source-critical astrological glyphs, or old-epoch chart engine validated. Avoid historical discriminatory servant selection advice.'
assert index['records_count']==sum(x['records_count'] for x in index['batches'])
assert index['read_numbered_chapters']==list(range(1,181)) and index['empirical_validations']==index['runtime_promotions']==0
INDEX.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=('# Lilly 1647/1659 original CLXXX Sicknesse, Servants — source covered (B07bc)\n\n'
'**27 source-only documentary notes R13018–R13044** from original printed753–754/PDF787–788 and independent 1659 typesetting. Historical sixth-house health rhetoric includes blood-corruption theory, fever, illness changes, mitigating directions and remedies; servants section makes unsupported trustworthiness and red-haired stereotypes. Neither constitutes medical truth, personnel advice or independent predictions. **13,044 Lilly + 1,066 Ptolemy = 14,110 Western historical annotations**. Chinese V7 **154 BaZi + 201 Zi Wei = 355**, unchanged. Physical original CLXXX chapter boundary covered but critical glyphs, independently calculated natal/timing engine and human prediction outcomes remain unverified. Next **R13045**, original PDF788/printed754 **CLXXXI Of Marriage** below divider. Zero validated human forecasts, no runtime model promotion.\n\n')
CURRENT.write_text(summary+'## Previous accepted historical checkpoint retained\n\n'+CURRENT.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(summary+(B/'ORIGINAL_SOURCE_REVIEW_20261020.md').read_text(encoding='utf-8'),encoding='utf-8')
receipt={'batch':'B07bc','status':'GUARDED_CLXXX_27_NOTES_PREPARED_REMOTE_PUBLISH_PENDING','Lilly_before':13017,'Lilly_after':13044,'Ptolemy_retained':1066,'Western_after':14110,'Chinese_V7_retained':355,'new_historical_annotations':27,'four_original_ed_page_images_verified':True,'next_R':'R13045','next_original_pdf':788,'next_printed_chapter':'CLXXXI','old_index_sha256':sha(BACK/'LILLY_INDEX_BEFORE_B07bc.json'),'new_index_sha256':sha(INDEX),'source_notes_sha256':accept['source_notes_sha256'],'rules_sha256':accept['rules_sha256'],'archive_sha256':archive['archive_sha256'],'portable_tests_replayed':44,'Chinese_V7_sha256':sha(CHINA),'clinical_and_person_outcomes_verified':0,'independent_human_predictions_validated':0,'runtime_promotions':0}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))
