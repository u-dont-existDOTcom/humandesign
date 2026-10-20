#!/usr/bin/env python3
"""Six exact original Wikitext chapters of Di Tian Sui, source-only qualitative notes."""
import hashlib,json,re
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017'
M=B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json';OLD=T/'CHINESE_SOURCE_AUDIT_INDEX_V8.json';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sha_bytes=lambda b:hashlib.sha256(b).hexdigest()
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=read(M);old=read(OLD);scope=read(B/'TASK_SCOPE.json');west=read(WEST)
assert sha(OLD)==scope['Chinese_V8_exact_SHA256'] and sha(WEST)==scope['Western_B07bc_exact_SHA256']
assert old['sum_source_annotations']==374 and old['systems'][0]['next_id']=='BZI-R0155' and old['systems'][1]['next_id']=='ZWD-R0221'
assert west['records_count']==13044
assert set(manifest)==set(scope['original_sources_chapters'])=={'13','14','15','16','17','18'}
# Each tuple is a self-contained excerpt from original transmitted commentary,
# followed by a non-expert working source gloss; does not count as a validated prediction.
commentary={
'13':[
('中而且和，子平之要法','The commentary treats moderation and balance as a central Zi Ping interpretive ideal.'),
('有病方為貴，無傷不是奇','Older rhetorical maxim about chart blemishes/fortune, not illness or diagnosis.'),
('格中如去病，財祿兩相隨','Metaphor of removing an affliction to obtain wealth/status, not verified wealth data.'),
('若身弱而財官旺也，取富貴不必於中也','Qualified exception: weak day-master with strong wealth/official factors need not show centered equilibrium to imply status.'),
('用神強，亦取富貴不必於和也','Qualified exception: strong useful factor is said to be compatible with fortune without equalized harmony.'),
('偏氣古怪，亦取富貴不必於中且和也','Author offers another exception for unusual skewed-qi formations; this does not establish outcomes.'),
],
'14':[
('剛者濟之以柔，而不得其情，反助其剛矣','Balancing hardness with softness can backfire if the relationship is inappropriate, according to source.'),
('庚辛生於七月，遇丁火而激其威','Specific stem/month condition in the authorial illustrative chart reading.'),
('遇乙木而助其暴，遇己土而成其志，遇癸水而益其銳','Source assigns context-dependent behavior to Yi Wood/Ji Earth/Gui Water alongside Metal in an example.'),
('壬水有正性，能引通庚之情故也','Ren Water is described as a compensating force for Geng Metal in this particular hypothetical combination.'),
('柔者濟之以剛，而不得其情，反其柔矣','Second conditional: balancing softness with hardness can counterproductively intensify softness.'),
('譬之婦人而遇恩威，則成淫賤','Historical sexist moral/social analogy in commentary; absolutely no evidence about actual women.'),
('乙木生於八月，遇甲丙壬而喜則舒情','Specific Yi Wood in eighth-month example predicts different response under Jia/Bing/Ren conditions.'),
('遇戊寅庚而畏則失身','Old source moralizing example; ambiguous sequence Wu/Yin/Geng preserved exact, no person claim accepted.'),
('丁火有正性，能定乙木之情故也','Specific Ding Fire/ Yi Wood contextual balancing condition claimed, not validated.'),
],
'15':[
('剛柔之道，可順而不可逆也','Hard/soft dynamic is described as better followed than reversed.'),
('源遠流長，可順而不可逆也','Long established flow is treated as a non-reversal condition.'),
('其勢已成，可順而不可逆也','Established momentum is identified as a condition where reversal is disfavored.'),
('權在一人，可順而不可逆也','A single dominant authority is used as a metaphor for following the dominant force.'),
('二人同心，可順而不可逆也','Two aligned forces are given as another historical non-reversal example.'),
],
'16':[
('陰支為寒，陽支為暖，金水為寒，木火為暖','Source assigns qualitative cold/warm symbolism to yin/yang branches and elemental pairs.'),
('得氣之寒，遇暖而發，得氣之暖，遇寒而成','Conditional balance principle: cold in strength benefits from warmth and vice versa.'),
('寒之甚，暖之至，內有一二成象，必無好處','Extreme cold/warmth historically deemed unfavorable, not a verified physical/person outcome.'),
('若五行陽遇子月，則一陽後萬物懷胎','Yang in Zi month and return of yang given as traditional calendrical-cosmological analogy.'),
('陰逄午月，則一陰後，萬物收藏','Yin in Wu month as analogous cosmological phase, preserving original 逄 glyph.'),
('過於濕者，滯而無成，過於燥者，烈而有禍','Excess moisture or dryness said to create figurative difficulty/ill fortune, no observed data.'),
('水有金生，遇寒土而愈濕','Metal-generated Water under cold Earth is considered more damp in source cosmology.'),
('火有木生，遇暖土而愈燥','Wood-generated Fire with warm Earth is considered drier in source cosmology.'),
('木火傷官要濕也','Source notes Wood-Fire hurting-officer formation supposedly requires moisture.'),
('金水傷官要燥也','Source notes Metal-Water hurting-officer formation supposedly requires dryness.'),
('間有火土而宜燥者，用土而後用火','An exception: certain Fire-Earth combinations call for dryness and Earth before Fire.'),
('金燥而宜濕者，用金而後用水','An exception: certain dry Metal formations call for moisture and Metal before Water.'),
],
'17':[
('令星，乃命之至要','Month-command factor is described as crucial to historical chart selection.'),
('如寅中戊土丙火甲木','Yin branch given with hidden Wu Earth, Bing Fire and Jia Wood.'),
('辨其孰為用事，則可以取格，可以取用','The identity of the active hidden factor affects pattern/useful-force classification.'),
('如寅月生人，立春後七日前，皆值戊土用事','Specific old transmitted time-segment convention: first seven days after Lichun Wu Earth governs Yin month; not checked against independent classical text or ephemeris.'),
('八日後十四日前，丙火用事','Second transmitted phase: eighth–fourteenth days of Yin month assigned Bing Fire.'),
('十五日後，甲木用事','Third transmitted phase: fifteenth onward assigned Jia Wood; no independent old-calendar day-boundary parity.'),
],
'18':[
('子時生人前三刻三分，壬水用事','Traditional subdivided Zi hour rule assigns earlier time to Ren Water; unit fractions not calibrated.'),
('後四刻七分，癸水用事','Later fraction of Zi hour assigned Gui Water; printed fractional units remain unverified.'),
('丙火用事何如？','Asks whether Bing Fire active in the Yin hour changes source pattern interpretation.'),
('甲木用事何如？','Asks whether Jia Wood active changes assessment of a source example.'),
('凡同年月日時，而百人各一應者','Source acknowledges purported differing outcomes among people with exactly same year/month/day/hour, an essential real-world falsification challenge.'),
('固當究其時之先後，又當論其山川之異，世德之殊','The author adds finer time, geography and family/social context as explanatory conditions; dangerous post-hoc flexibility without preregistration.'),
('十有九驗','Text appears to claim nine in ten cases verified, but no underlying sample, preregistered study, measured outcome or independent replication is supplied; cannot be scored as success.'),
('不過此則有官，彼則多子，此則多財，彼則妻美','Examples of differing career/children/wealth/spousal outcomes despite same birth details; no human sample provided.'),
('夫山川之異，不惟東酉南北','Historical geographic context argument, preserving original odd 東酉 glyph without silent correction.'),
('世德之殊，不惟富貴貧賤','Historical family/social circumstances distinguished as context, not verified natal indicator.'),
('善惡邪正，不盡齊也','Authorial moral variation label not something a chart actually predicts reliably from this source.'),
]
}
verse_gloss={
'13':['Moderation/balance of the five phases is described as overarching source goal, not measured success.'],
'14':['Hardness/softness should be guided rather than forcibly controlled, per historical aphorism.'],
'15':['Given momentum/flow conditions, follow rather than reverse, according to historical aphorism.'],
'16':['Heating/cooling analogy and upper/lower bounds; an old cosmological metaphor, not temperature medicine.','Moist/dry earth analogy should avoid single-sided extremes; not observed outcome evidence.'],
'17':['Month-command houses hidden human-source activation, claimed crucial to pattern selection.'],
'18':['Minute/subhour hidden-stem analogies and birth-time source contextual variation, not a proven clock algorithm.'],
}
rows=[];receipts=[]
for chap in ['13','14','15','16','17','18']:
 meta=manifest[chap];p=B/meta['raw_local_relative'];content=p.read_bytes();text=content.decode('utf-8')
 assert p.stat().st_size==meta['exact_utf8_bytes'] and sha(p)==meta['exact_sha256'] and meta['source_chapter']=='滴天髓/'+chap
 verses=list(re.finditer(r'\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}',text,re.S))
 assert len(verses)==len(verse_gloss[chap]),(chap,len(verses))
 current=[('original_verse',m.group(1),verse_gloss[chap][i]) for i,m in enumerate(verses)]+[('transmitted_commentary',a,b) for a,b in commentary[chap]]
 for role,quote,gloss in current:
  assert text.count(quote)==1,(chap,role,quote,text.count(quote))
  cp=text.index(quote);bytelen=len(text[:cp].encode('utf-8'));enc=quote.encode('utf-8')
  assert content[bytelen:bytelen+len(enc)]==enc
  name=f'BZI-R{155+len(rows):04d}'
  is_moral=('婦人' in quote or '淫賤' in quote or '善惡' in quote or '失身' in quote)
  is_actual_unverified=('十有九驗' in quote)
  row={'id':name,'batch':'ChineseAstro-09','source':'BAZI-DTS-WIKISOURCE-TRANSMITTED','source_chapter':'滴天髓/'+chap,'source_chapter_section_number':int(chap),'source_oldid':meta['pinned_oldid'],'source_raw_relative_file':str(p.relative_to(ROOT)),'original_raw_file_sha256':meta['exact_sha256'],'source_layer':role,'original_chinese_exact_quote':quote,'original_chinese_quote_sha256':sha_bytes(enc),'original_chinese_quote_utf8_bytes':len(enc),'original_chinese_character_offset':cp,'original_chinese_byte_offset':bytelen,'researcher_nonexpert_gloss_NOT_original_translation':gloss,'historical_moral_or_gender_stereotype_not_endorsed':is_moral,'source_nine_in_ten_accuracy_claim_without_data':is_actual_unverified,'original_early_print_authorship_expert_authenticated':False,'old_calendar_or_hidden_stem_time_engine_verified':False,'real_human_claim_or_prediction_independently_validated':False,'model_runtime_promoted':False}
  rows.append(row);receipts.append({'id':name,'chapter':chap,'source_raw_sha256':meta['exact_sha256'],'source_quote_sha256':sha_bytes(enc),'quote_character_offset':cp,'quote_byte_offset':bytelen,'quote_byte_length':len(enc)})
assert len(rows)==56,len(rows)
assert rows[0]['id']=='BZI-R0155' and rows[-1]['id']=='BZI-R0210' and [r['id'] for r in rows]==[f'BZI-R{n:04d}' for n in range(155,211)]
src={'schema':'BAZI_DITIAN_SUI_13_18_SOURCE_56_EXACT_CHINESE_WITNESSES_V1','batch':'ChineseAstro-09','source_edition':'transmitted Chinese Wikisource original 2017 pinned revisions, NOT verified ancient edition','source_chapters':['13','14','15','16','17','18'],'original_wikitext_manifest_path':str(M.relative_to(ROOT)),'original_wikitext_manifest_sha256':sha(M),'source_verses':sum(len(x) for x in verse_gloss.values()),'source_commentary_anchor_count':sum(len(x) for x in commentary.values()),'new_source_historical_annot_count':len(rows),'first_id':rows[0]['id'],'last_id':rows[-1]['id'],'next_id':'BZI-R0211','parallel_ziwei_next_id':'ZWD-R0221','early_edition_text_authorship_authenticated':False,'classical_chinese_expert_commentary_attribution_verified':False,'subhour_and_solar_term_old_calendar_engine_independently_validated':False,'claimed_nine_in_ten_historical_predictions_checked':False,'actual_independent_human_predictions_validated':0,'runtime_astrology_promotions':0,'record_rows':rows}
save(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json',src)
witness={'schema':'BAZI_DTS_13_18_ORIGINAL_SIX_REVISION_QUOTE_SHA_BYTE_WITNESS','source_manifest_sha256':sha(M),'source_revisions':{k:v['pinned_oldid'] for k,v in manifest.items()},'source_raw_bytes_SHA256':{k:{'bytes':v['exact_utf8_bytes'],'sha256':v['exact_sha256']} for k,v in manifest.items()},'independent_old_author_authentication':False,'quote_count':len(receipts),'original_verse_count':src['source_verses'],'original_transmitted_commentary_excerpt_count':src['source_commentary_anchor_count'],'quote_receipts':receipts}
save(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json',witness)
print(json.dumps({'status':'DRAFT_NOT_ADMITTED','verses':src['source_verses'],'commentary':src['source_commentary_anchor_count'],'total':len(rows),'first':rows[0]['id'],'last':rows[-1]['id'],'next':src['next_id'],'source_SHA256':sha(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json'),'emphasis_source_18_unverified_accuracy_quote':[r['id'] for r in rows if r['source_nine_in_ten_accuracy_claim_without_data']]},indent=2))
