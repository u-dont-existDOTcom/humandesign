#!/usr/bin/env python3
"""Preserve transmitted Ziwei V2 original post-bureau diagrams exactly, no chart parity."""
import hashlib,json,re
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017'
RAW=T/'batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt';INDEX=T/'CHINESE_SOURCE_AUDIT_INDEX_V7.json';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
sha_bytes=lambda data:hashlib.sha256(data).hexdigest()
sha=lambda p:sha_bytes(p.read_bytes())
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sha(RAW)=='1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72' and len(RAW.read_bytes())==106736
index=read(INDEX);west=read(WEST);scope=read(B/'TASK_SCOPE.json')
assert index['sum_source_annotations']==355 and index['systems'][1]['next_id']=='ZWD-R0202' and index['systems'][0]['next_id']=='BZI-R0155'
assert sha(INDEX)==scope['Chinese_V7_sha256'] and west['records_count']==13044 and west['batches'][-1]['id']=='B07bc'
old=read(T/'batches/ChineseAstro-07/ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json')
assert old['next_id']=='ZWD-R0202' and old['pinned_original_volume2_full_raw_SHA256']==sha(RAW)
s=RAW.read_text(encoding='utf-8')
oldend=old['original_text_segment_absolute_end_codepoint'];assert oldend==12080,oldend
start=s.index('<nowiki>',oldend);end=s.index('</nowiki>',start)+len('</nowiki>');heading=s.index('===一 命宫===',end)
assert start==12085 and end==19951 and heading==19953
source_segment=s[start:heading];assert source_segment.startswith('<nowiki>') and source_segment.rstrip().endswith('</nowiki>')
segmentfile=B/'SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt';segmentfile.write_text(source_segment,encoding='utf-8');assert segmentfile.read_text(encoding='utf-8')==source_segment
body=s[start+len('<nowiki>'):end-len('</nowiki>')]
parts=re.split(r'\n\s*\n',body)
assert len(parts)==4,[(i,len(p)) for i,p in enumerate(parts)]
labels=['安天府图','殇使祸福紧慢图岁限为灾之局','禄权科忌图','|   |庙       |旺']
for part,label in zip(parts,labels):assert part.count(label)==1,label
names=['TIANFU_REFERENCE_STAR_PALACE_DIAGRAM','TIANSHANG_TIANSHI_YEAR_LIMIT_RISK_DIAGRAM','LU_QUAN_KE_JI_TRANSFORMATIONS_DIAGRAM','TWELVE_BRANCH_SEVEN_GRADE_STAR_CONDITIONS_TABLE']
notes=['Tian Fu chart map relative to Zi Wei is a historical diagram; palace placement algorithm not independently checked.','Archaic year-limit danger/death diagram; the fatalistic prediction is not a verified outcome, and must not be used to forecast mortality.','Four-transformation chart with traditional judgments; not a verified chart or predictive timing engine.','Twelve earthly-branch star-conditions table with seven historical dignity categories; cells use abbreviated characters requiring original-symbol collation.']
rows=[]; witnesses=[]
def add(typ,quote,gloss,extra=None):
 i=len(rows);pos=s.find(quote,start)
 assert pos>=start and pos<heading and s.count(quote,start,heading)==1,(i,typ,len(quote),s.count(quote,start,heading))
 data=quote.encode('utf-8');assert s[pos:pos+len(quote)]==quote
 r={'id':f'ZWD-R{202+i:04d}','source':'ZWDS-CLASSIC-01','source_type':typ,'source_original_full_oldid':1963110,'source_original_full_SHA256':sha(RAW),'source_original_exact_quote':quote,'source_quote_utf8_sha256':sha_bytes(data),'source_quote_utf8_bytes':len(data),'source_original_absolute_character_offset':pos,'source_original_absolute_utf8_byte_offset':len(s[:pos].encode('utf-8')),'source_original_excerpt_relative_character_offset':pos-start,'historical_research_gloss_NOT_quotation':gloss,'original_source_physical_early_edition_authenticated':False,'original_Chinese_source_exact_text_excerpt_not_expert_translation':True,'historic_table_symbol_cell_or_calendar_engine_validated':False,'independent_human_forecast_or_outcome_validated':False,'runtime_model_promoted':False}
 if extra:r.update(extra)
 rows.append(r)
 witnesses.append({'id':r['id'],'source_exact_byte_offset':r['source_original_absolute_utf8_byte_offset'],'source_codepoint_offset':pos,'utf8_bytes':len(data),'quote_sha256':r['source_quote_utf8_sha256']})
for nm,part,gloss in zip(names,parts,notes):add('original_source_diagram_unparsed',part,gloss,{'source_diagram_role':nm,'no_cross_branch_chart_engine_parity':True})
add('source_historical_condition', '天府惟寅申二宫紫府同宫','The transmitted Tian Fu chart says Zi Wei and Tian Fu co-occupy Yin and Shen palaces; no independently verified source-calendar natal chart or algorithm.','' if False else None)
add('source_historical_seven_grade_taxonomy','|   |庙       |旺       |得地     |利益     |平和     |不得地   |落陷     |','Traditional table columns list seven condition grades, not empirical star influence or seven empirically measured outcomes.')
# Each branch's row spans three ORIGINAL lines with corresponding named branch in the middle.
lines=parts[3].splitlines(keepends=True)
branches=list('子丑寅卯辰巳午未申酉戌亥')
found=[]
for j,line in enumerate(lines):
 m=re.match(r'^\|(?P<branch>[子丑寅卯辰巳午未申酉戌亥])\s*\|',line)
 if m:
  q=''.join(lines[j-1:j+2]);branch=m.group('branch');found.append(branch)
  add('source_historical_branch_star_grade_row',q,f'Original {branch} earthly-branch diagram grade row preserved with adjacent multi-line star abbreviations; not yet decoded or externally cross-verified.',{'earthly_branch':branch,'grade_columns':['庙','旺','得地','利益','平和','不得地','落陷'],'independent_astrological_strength_computation_verified':False})
assert found==branches,found
# This is a section boundary, not re-extraction of the next Life palace interpretation.
assert s[heading:heading+len('===一 命宫===')]=='===一 命宫===';pos=heading;quote='===一 命宫===';data=quote.encode();rows.append({'id':f'ZWD-R{202+len(rows):04d}','source':'ZWDS-CLASSIC-01','source_type':'NEXT_SECTION_BOUNDARY','source_original_full_oldid':1963110,'source_original_full_SHA256':sha(RAW),'source_original_exact_quote':quote,'source_quote_utf8_sha256':sha_bytes(data),'source_quote_utf8_bytes':len(data),'source_original_absolute_character_offset':pos,'source_original_absolute_utf8_byte_offset':len(s[:pos].encode('utf-8')),'source_original_excerpt_relative_character_offset':pos-start,'historical_research_gloss_NOT_quotation':'Original text next begins the separate twelve-palace Life palace meanings; substantive Life-palace claims are unextracted, begin next record.','original_source_physical_early_edition_authenticated':False,'original_Chinese_source_exact_text_excerpt_not_expert_translation':True,'historic_table_symbol_cell_or_calendar_engine_validated':False,'independent_human_forecast_or_outcome_validated':False,'runtime_model_promoted':False})
witnesses.append({'id':rows[-1]['id'],'source_exact_byte_offset':rows[-1]['source_original_absolute_utf8_byte_offset'],'source_codepoint_offset':pos,'utf8_bytes':len(data),'quote_sha256':rows[-1]['source_quote_utf8_sha256']})
assert len(rows)==19 and rows[0]['id']=='ZWD-R0202' and rows[-1]['id']=='ZWD-R0220'
source={'schema':'ORIGINAL_ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_ONLY_V1','batch':'ChineseAstro-08','original_raw_oldid':1963110,'original_source_raw_file_relative':str(RAW.relative_to(ROOT)),'original_raw_full_SHA256':sha(RAW),'original_raw_utf8_bytes':RAW.stat().st_size,'original_excerpt_relative_file':str(segmentfile.relative_to(ROOT)),'original_excerpt_absolute_start_character':start,'original_excerpt_absolute_end_character_exclusive':heading,'original_excerpt_sha256':sha(segmentfile),'diagram_count':4,'star_condition_earthly_branches':branches,'source_historical_annotation_count':len(rows),'first_id':rows[0]['id'],'last_id':rows[-1]['id'],'next_id':'ZWD-R0221','next_section':'===一 命宫===','early_original_woodblock_edition_authenticated':False,'original_source_star_name_abbreviations_fully_collated':False,'traditional_ziwei_complete_calendar_and_chart_engine_verified':False,'historic_year_limit_mortality_forecast_validated':False,'independent_real_human_predictions_validated':0,'runtime_promotions':0,'record_rows':rows}
save(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json',source)
w={'batch':'ChineseAstro-08','original_source_full_SHA256':sha(RAW),'original_exact_excerpt_SHA256':sha(segmentfile),'original_exact_excerpt_UTF8_bytes':segmentfile.stat().st_size,'original_excerpt_original_character_range':[start,heading],'original_four_unparsed_diagram_UTF8_SHA256':[sha_bytes(part.encode('utf-8')) for part in parts],'exact_source_quotes':witnesses,'source_read_as_transmitted_Wikitext_not_old_woodblock':True,'original_table_computational_reconstruction_verified':False,'real_human_predictive_results_verified':0}
save(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json',w)
assert len(rows)==len(w['exact_source_quotes'])==19
print(json.dumps({'status':'NOT_ADMITTED','records':len(rows),'from':rows[0]['id'],'to':rows[-1]['id'],'next':'ZWD-R0221','raw_segment_codepoint_range':[start,heading],'four_diagrams':len(parts),'12_branch_rows':len(found),'source_sha256':sha(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json'),'quote_offsets_verified':len(witnesses)},indent=2))
