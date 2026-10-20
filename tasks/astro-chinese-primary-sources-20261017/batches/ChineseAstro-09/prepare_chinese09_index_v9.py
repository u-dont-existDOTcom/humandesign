#!/usr/bin/env python3
"""Guarded append-only Chinese V9: 56 original BaZi source annotations, no human results."""
import copy,hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017';OLD=T/'CHINESE_SOURCE_AUDIT_INDEX_V8.json';NEW=T/'CHINESE_SOURCE_AUDIT_INDEX_V9.json';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md';LATEST=ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_09.md';BACK=B/'recovery';RECEIPT=B/'CANONICAL_PREPARE_RECEIPT_20261020.json';BRANCH='research/astro-chinese-09-bazi-dts-13-18-20261020'
read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def downloads():
 r=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
 if r.returncode==0 and r.stdout.strip() and Path(r.stdout.strip()).is_dir() and Path(r.stdout.strip()).resolve()!=Path.home().resolve():return Path(r.stdout.strip())
 return Path.home()/'Téléchargements'
assert git('branch','--show-current')==BRANCH
for p in (NEW,LATEST,RECEIPT,BACK/'CHINESE_V8_BEFORE_09.json'):assert not p.exists(),f'Interrupted earlier source V9 admission; reconcile first: {p}'
old=read(OLD);west=read(WEST);source=read(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json');witness=read(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json');manifest=read(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json');scope=read(B/'TASK_SCOPE.json');archive=read(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json')
assert scope['root_task']=='OPEN' and scope['branch']==BRANCH
assert sha(OLD)==scope['Chinese_V8_exact_SHA256']==archive['Chinese_V8_index_sha256']
assert old['sum_source_annotations']==374 and old['systems'][0]['accepted_source_annotations']==154 and old['systems'][1]['accepted_source_annotations']==220
assert old['systems'][0]['next_id']=='BZI-R0155' and old['systems'][1]['next_id']=='ZWD-R0221'
assert old['accepted_batches'][-1]['id']=='ChineseAstro-08'
assert old['original_chinese_source_anchors_checked_against_revision']==302
assert len(source['record_rows'])==56 and [r['id'] for r in source['record_rows']]==[f'BZI-R{n:04d}' for n in range(155,211)]
assert source['next_id']=='BZI-R0211' and source['parallel_ziwei_next_id']=='ZWD-R0221'
assert source['original_wikitext_manifest_sha256']==sha(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json')
assert witness['quote_count']==56 and len(witness['quote_receipts'])==56
assert witness['original_verse_count']==7 and witness['original_transmitted_commentary_excerpt_count']==49
assert archive['ZIP_CRC_verified'] and archive['member_SHA256_and_exact_bytes_passed'] and archive['independent_original_quote_tests_replayed']==75
assert sha(downloads()/archive['filename'])==archive['archive_sha256']
assert archive['source_notes_sha256']==sha(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json')
assert archive['source_witness_sha256']==sha(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json')
assert west['records_count']==13044 and sha(WEST)==scope['Western_B07bc_exact_SHA256']==archive['parallel_Western_B07bc_index_sha256']
assert source['actual_independent_human_predictions_validated']==source['runtime_astrology_promotions']==0
assert source['claimed_nine_in_ten_historical_predictions_checked'] is False
for k,m in manifest.items():
 p=B/m['raw_local_relative'];assert p.is_file() and sha(p)==m['exact_sha256'] and p.stat().st_size==m['exact_utf8_bytes']
for file in [OLD,T/'CHINESE_SOURCE_AUDIT_INDEX_V7.json',T/'CHINESE_SOURCE_AUDIT_INDEX_V6.json',T/'batches/ChineseAstro-06/BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json',T/'batches/ChineseAstro-08/ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json',WEST]:
 name=str(file.relative_to(ROOT));assert git('rev-parse','HEAD:'+name)==git('hash-object',str(file)),name
BACK.mkdir(exist_ok=False)
for f,n in ((OLD,'CHINESE_V8_BEFORE_09.json'),(WEST,'WESTERN_B07bc_BEFORE_09.json'),(CURRENT,'CHINESE_CURRENT_BEFORE_09.md')):(BACK/n).write_bytes(f.read_bytes())
new=copy.deepcopy(old);new['schema']='ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V9';new['status']='BAZI_DITIAN_SUI_CHAPTERS_13_TO_18_EXACT_ORIGINAL_QUOTE_SOURCE_ONLY'
new['prior_index']='CHINESE_SOURCE_AUDIT_INDEX_V8.json';new['prior_index_sha256']=sha(OLD);new['as_of_utc']='2026-10-20'
new['sum_source_annotations']=430;new['original_chinese_source_anchors_checked_against_revision']=302+56
new['accepted_batches'].append({'id':'ChineseAstro-09','added_bazi_source_annotations':56,'added_ziwei_source_annotations':0,'start':'BZI-R0155','end':'BZI-R0210','path':'batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json','rules_sha256':sha(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json'),'witness_path':'batches/ChineseAstro-09/PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json','witness_sha256':sha(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json'),'original_source_manifest_path':'batches/ChineseAstro-09/PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json','original_source_manifest_sha256':sha(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json'),'source_chapters':['13','14','15','16','17','18'],'pinned_original_revisions':[manifest[k]['pinned_oldid'] for k in ['13','14','15','16','17','18']],'source_verse_count':7,'source_commentary_annotations':49,'human_validation_accuracy_claim_unverified':True,'original_source_portable_test_replays':75,'real_human_predictions_validated':0,'runtime_promotions':0})
new['systems'][0]['accepted_source_annotations']=210;new['systems'][0]['current_ids']='BZI-R0001–BZI-R0210';new['systems'][0]['next_id']='BZI-R0211';new['systems'][0]['current_batch']='ChineseAstro-09'
new['systems'][0]['source_files'].append('batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json')
new['systems'][0]['chapter_coverage']='Accepted further six transmitted Di Tian Sui original online-source chapters 13–18: balance and exceptions, softness/hardness qualifiers, following trends, cold/warm and dry/wet conditions, precise old monthly hidden-stem division, birth-hour subdivisions and contextual same-hour outcome variations. 56 exact original quotes, 7 verses + 49 commentary. Authorial 十有九驗 accuracy claim recorded explicitly UNVERIFIED; full calendrical engine and actual person evaluations absent.'
assert new['systems'][1]==old['systems'][1]
assert new['accepted_batches'][:-1]==old['accepted_batches']
assert sum(x['accepted_source_annotations'] for x in new['systems'])==430
new['separate_lilly_source_count_at_this_revision']=13044;new['separate_ptolemy_source_count_at_this_revision']=1066
new['source_parallel_western_history_binding']='ChineseAstro-09 proceeds from separately verified Western B07bc (13,044 Lilly + 1,066 Ptolemy) with exact index bytes frozen, no Western recomputation or claims.'
new['full_ziwei_original_text_collation_finished']=False;new['all_14_principal_stars_verified']=False;new['ziwei_complete_natal_calendar_engine_verified']=False;new['chinese_bazi_solar_term_engine_verified']=False;new['independently_validated_real_human_claims']=0;new['runtime_promotions']=0
new['historical_glyph_and_translator_limits']='Transmitted oldid-specific Wikisource Chinese, not authenticated ancient print, original authorship, specialist translation or independent oracle data. Old Di Tian Sui 17/18 timing claims of Lichun stem-switch day and Zi-hour fractions uncalibrated. 十有九驗 is unverified authorial claim, never measured accuracy. Historical gender and moral stereotypes unendorsed; no prospectively tested human life outcomes.'
new['next']='BaZi original Di Tian Sui section 19 onward, starting BZI-R0211; Zi Wei Volume II Life-palace interpretation starting ZWD-R0221. Independently verify traditional calendar/chart/timing calculations, freeze original textual rules and preregister blinded real-human forward/reverse tests vs matched decoys and non-astrology baselines with misses.'
NEW.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary='# Chinese source V9: pinned BaZi Di Tian Sui chapters 13–18\n\n**56 source-only annotations BZI-R0155–BZI-R0210** from six pinned exact original transmitted Chinese oldids, seven original verses and 49 commentary spans. Important methodological limitations: calendar timing rules unverified, sex/morality stereotypes unendorsed, `十有九驗` apparent high-accuracy claim **not supported by any independently tested cases**. **Chinese 210 BaZi + 220 Zi Wei = 430 historical original-text annotations** (V1–V8 unchanged). Western **13,044 Lilly + 1,066 Ptolemy = 14,110** unchanged. Next **BZI-R0211**, **ZWD-R0221**. **Verified real-human forecasts 0; runtime promotions 0**.\n\n'
CURRENT.write_text(summary+'## Previously accepted source checkpoints retained\n\n'+CURRENT.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(summary+(B/'ORIGINAL_SOURCE_REVIEW_20261020.md').read_text(encoding='utf-8'),encoding='utf-8')
receipt={'batch':'ChineseAstro-09','status':'V9_BAZI_DTS_13_18_56_PINNED_NOTES_PREPARED_REMOTE_PENDING','Chinese_before':374,'Chinese_after':430,'BaZi_before':154,'BaZi_after':210,'ZiWei_retained':220,'new_source_notes':56,'original_verses':7,'original_commentary_anchors':49,'next_BaZi':'BZI-R0211','next_ZiWei':'ZWD-R0221','old_Chinese_V8_sha256':sha(BACK/'CHINESE_V8_BEFORE_09.json'),'new_Chinese_V9_sha256':sha(NEW),'manifest_sha256':sha(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json'),'notes_sha256':sha(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json'),'witness_sha256':sha(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json'),'archive_sha256':archive['archive_sha256'],'portable_tests_replayed':75,'Western_B07bc_Lilly':13044,'Western_Ptolemy':1066,'Western_B07bc_index_sha256':sha(WEST),'claimed_nine_in_ten_source_statement_validated':False,'human_predictions_verified':0,'runtime_promotions':0}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))
