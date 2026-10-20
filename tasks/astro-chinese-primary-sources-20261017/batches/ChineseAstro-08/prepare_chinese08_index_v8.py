#!/usr/bin/env python3
"""Guarded Chinese V8: append 19 exact historical diagrams, never chart validation."""
import copy,hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017'
OLD=T/'CHINESE_SOURCE_AUDIT_INDEX_V7.json';NEW=T/'CHINESE_SOURCE_AUDIT_INDEX_V8.json';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md';LATEST=ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_08.md'
BACK=B/'recovery';RECEIPT=B/'CANONICAL_PREPARE_RECEIPT_20261020.json';BRANCH='research/astro-chinese-08-ziwei-postbureau-tables-20261020'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def downloads():
 p=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
 if p.returncode==0 and p.stdout.strip() and Path(p.stdout.strip()).is_dir() and Path(p.stdout.strip()).resolve()!=Path.home().resolve():return Path(p.stdout.strip())
 return Path.home()/'Téléchargements'
for f in (NEW,LATEST,RECEIPT,BACK/'CHINESE_V7_BEFORE_08.json'):
 assert not f.exists(),f'Interrupted admission needs reconciliation: {f}'
assert git('branch','--show-current')==BRANCH
old=read(OLD);west=read(WEST);source=read(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json');witness=read(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json');scope=read(B/'TASK_SCOPE.json');archive=read(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json')
assert scope['root_task']=='OPEN' and scope['branch']==BRANCH
assert sha(OLD)==scope['Chinese_V7_sha256']==archive['Chinese_V7_index_sha256']
assert old['sum_source_annotations']==355 and old['systems'][0]['accepted_source_annotations']==154 and old['systems'][1]['accepted_source_annotations']==201
assert old['systems'][1]['next_id']=='ZWD-R0202' and old['systems'][0]['next_id']=='BZI-R0155' and old['accepted_batches'][-1]['id']=='ChineseAstro-07'
assert old['original_chinese_source_anchors_checked_against_revision']==283
assert len(source['record_rows'])==19 and [x['id'] for x in source['record_rows']]==[f'ZWD-R{n:04d}' for n in range(202,221)]
assert source['next_id']=='ZWD-R0221'
assert witness['original_source_full_SHA256']==source['original_raw_full_SHA256'] and source['original_raw_full_SHA256']==sha(T/'batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt')
assert len(witness['exact_source_quotes'])==19 and source['diagram_count']==4
assert sha(B/'SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt')==source['original_excerpt_sha256']
assert archive['ZIP_CRC_passed'] and archive['members_SHA256_and_exact_bytes_verified'] and archive['independent_extraction_test_replay']==38
assert sha(downloads()/archive['filename'])==archive['archive_sha256']
assert archive['source_notes_sha256']==sha(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json')
assert archive['source_witness_sha256']==sha(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json')
assert west['records_count']==13044 and west['batches'][-1]['id']=='B07bc' and sha(WEST)==archive['Western_B07bc_index_sha256']
assert source['independent_real_human_predictions_validated']==source['runtime_promotions']==0
assert all(not x['independent_human_forecast_or_outcome_validated'] and not x['runtime_model_promoted'] for x in source['record_rows'])
# Old root history, all prior source rows and untouched parallel Western remain frozen.
for f in (OLD,T/'CHINESE_SOURCE_AUDIT_INDEX_V6.json',T/'CHINESE_SOURCE_AUDIT_INDEX_V5.json',T/'batches/ChineseAstro-07/ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json',T/'batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt',T/'batches/ChineseAstro-06/BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json',WEST):
 relative=str(f.relative_to(ROOT));assert git('rev-parse','HEAD:'+relative)==git('hash-object',str(f)),relative
BACK.mkdir(exist_ok=False)
for f,n in ((OLD,'CHINESE_V7_BEFORE_08.json'),(WEST,'WESTERN_B07bc_BEFORE_08.json'),(CURRENT,'CHINESE_CURRENT_BEFORE_08.md')):(BACK/n).write_bytes(f.read_bytes())
updated=copy.deepcopy(old)
updated['schema']='ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V8'
updated['status']='ZIWEI_POST_FIVE_BUREAU_FOUR_ORIGINAL_DIAGRAMS_12_BRANCH_STRENGTH_TABLE_DOCUMENTED'
updated['prior_index']='CHINESE_SOURCE_AUDIT_INDEX_V7.json';updated['prior_index_sha256']=sha(OLD)
updated['as_of_utc']='2026-10-20'
updated['sum_source_annotations']=374
updated['original_chinese_source_anchors_checked_against_revision']=283+19
updated['accepted_batches'].append({'id':'ChineseAstro-08','added_bazi_source_annotations':0,'added_ziwei_source_annotations':19,'start':'ZWD-R0202','end':'ZWD-R0220','path':'batches/ChineseAstro-08/ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json','rules_sha256':sha(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json'),'witness_path':'batches/ChineseAstro-08/SOURCE_1963110_POSTBUREAU_WITNESS_V1.json','witness_sha256':sha(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json'),'source_original_full_oldid':1963110,'source_original_full_raw_sha256':source['original_raw_full_SHA256'],'source_excerpt_sha256':source['original_excerpt_sha256'],'unparsed_diagrams':4,'unparsed_seven_grade_12_branch_source_table':True,'portable_independent_extraction_test_replays':38,'traditional_calendar_or_star_chart_engine_validated':False,'independent_real_person_predictions_validated':0,'runtime_promotions':0})
updated['systems'][1]['accepted_source_annotations']=220
updated['systems'][1]['current_ids']='ZWD-R0001–ZWD-R0220'
updated['systems'][1]['next_id']='ZWD-R0221'
updated['systems'][1]['current_batch']='ChineseAstro-08'
updated['systems'][1]['source_files'].append('batches/ChineseAstro-08/ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json')
updated['systems'][1]['chapter_coverage']='Transmitted Zi Wei Volume II through original 5 elemental bureau day/palace diagrams (prior V7), then four additional original Zi Wei/Tian Fu, year-limit risk, four-transformations and 12-branch × seven-grade stellar-condition diagrams. V8 adds 19 source-only exact original Chinese notes; original abbr glyphs/diagram cells remain unparsed as computational engine. Next separate ===一 命宫=== prose; all birth calendar/day/star outcomes unverified.'
assert updated['systems'][0]==old['systems'][0]
assert sum(s['accepted_source_annotations'] for s in updated['systems'])==374
assert updated['accepted_batches'][:-1]==old['accepted_batches']
updated['separate_lilly_source_count_at_this_revision']=13044
updated['separate_ptolemy_source_count_at_this_revision']=1066
updated['source_parallel_western_history_binding']='This ChineseAstro-08 index was independently advanced after the published Western Lilly B07bc source addition on the same exact owner branch baseline: 13,044 Lilly + 1,066 Ptolemy (14,110 Western); it does NOT revise Western history.'
updated['full_ziwei_original_text_collation_finished']=False
updated['all_14_principal_stars_verified']=False
updated['ziwei_complete_natal_calendar_engine_verified']=False
updated['chinese_bazi_solar_term_engine_verified']=False
updated['historical_glyph_and_translator_limits']='Transmitted Simplified Chinese Wikitext oldid1963110, NOT authenticated Ming original. Four original post-bureau diagrams preserve exact characters but are not astronomical ephemeris, calendar or 14-star chart parity. Year-limit diagram fatalism, source social/gender health status and old astrology prose are unverified claims, never high-stakes predictions. The prior five bureau day diagrams remain unparsed. Original 火玲 ambiguous.'
updated['independently_validated_real_human_claims']=0;updated['runtime_promotions']=0
updated['next']='Zi Wei ZWD-R0221: after diagrams, begin the distinct ===一 命宫=== Life-palace original source prose. BaZi BZI-R0155 Di Tian Sui next untouched original section. All traditional calendar/placement/math engine parity and preregistered blinded forward/reverse human test against decoys/nonastrology controls remain unverified; keep misses.'
NEW.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary='# Zi Wei original Volume II further diagrams, Chinese source V8\n\n**19 exact source-only notes ZWD-R0202–ZWD-R0220** freeze original post-bureau Tian Fu, life/year-limit risk, four-transformations and 12-branch seven-grade star-conditions diagrams with exact Chinese text and individual byte offsets in oldid1963110. No calendar/chart decoder parity, mortality forecast or personal prediction established. **Chinese historical 154 BaZi + 220 Zi Wei = 374**. Independently already accepted Western **13,044 Lilly + 1,066 Ptolemy = 14,110** retained. V1–V7 immutable. Next **ZWD-R0221 Life palace** and **BZI-R0155**. **Actual human validations 0; runtime astrology promotions 0.**\n\n'
CURRENT.write_text(summary+'## Previous accepted historical checkpoint retained\n\n'+CURRENT.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(summary+(B/'ORIGINAL_SOURCE_REVIEW_20261020.md').read_text(encoding='utf-8'),encoding='utf-8')
receipt={'batch':'ChineseAstro-08','status':'V8_CHINESE_INDEX_GUARDED_SOURCE_APPEND_REMOTE_PENDING','Chinese_before':355,'Chinese_after':374,'BaZi_retained':154,'ZiWei_before':201,'ZiWei_after':220,'new_original_source_annotations':19,'next_ZiWei':'ZWD-R0221','next_BaZi':'BZI-R0155','original_full_oldid':1963110,'original_raw_source_sha256':source['original_raw_full_SHA256'],'V7_index_exact_sha256':sha(BACK/'CHINESE_V7_BEFORE_08.json'),'V8_index_exact_sha256':sha(NEW),'source_notes_sha256':sha(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json'),'source_witness_sha256':sha(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json'),'portable_archive_sha256':archive['archive_sha256'],'portable_test_replays':38,'Western_Lilly_pinned':13044,'Western_Ptolemy_pinned':1066,'parallel_Western_index_sha256':sha(WEST),'independent_human_predictions_validated':0,'runtime_promotions':0}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
