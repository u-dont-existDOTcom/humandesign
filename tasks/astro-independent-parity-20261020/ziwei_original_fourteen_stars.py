#!/usr/bin/env python3
"""Strict original-source fourteen principal-star PALACE pattern GIVEN ZiWei.

Original placement rhyme (紫微斗數全書 卷二 oldid1963110) defines six ZiWei
group stars going backward and eight TianFu group stars going forward.
The separately source-anchored TianFu mirror determines TianFu from ZiWei.

This is a reproducible chart-MECHANICS fragment, not independently verified
historical calendar, physical Ming source, actual natal birth chart, life
prediction, or validated timing system. Late secondary reading remains opt-in.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from ziwei_tianfu_relative import tianfu_from_ziwei
from ziwei_original_bureau_candidate import candidate_given_bureau_day
from ziwei_secondary_nayin_reading import source_bureau_with_explicit_edition_policy

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt'
SOURCE_SHA='1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72'
BRANCHES=('Zi','Chou','Yin','Mao','Chen','Si','Wu','Wei','Shen','You','Xu','Hai')
# Chinese originals for the source abbreviations 阳 武 同 etc; exact source order.
ZGROUP=(('ZiWei','紫微',0),('TianJi','天机',-1),('TaiYang','太阳',-3),
        ('WuQu','武曲',-4),('TianTong','天同',-5),('LianZhen','廉贞',-8))
FGROUP=(('TianFu','天府',0),('TaiYin','太阴',1),('TanLang','贪狼',2),
        ('JuMen','巨门',3),('TianXiang','天相',4),('TianLiang','天梁',5),
        ('QiSha','七杀',6),('PoJun','破军',10))
VERSE='紫微天机逆行旁，隔一阳武天同当，又隔二位廉贞地，空三复见紫微郎，\n天府太阴与贪狼，巨门天相及天梁，七杀空三破军位，八星顺数细推详。'
AUTHORIAL_EXAMPLE='如甲生人安命在寅却起甲己之年丙为首，是丙寅丁卯炉中火，却去火局寻某日生期起紫微帝王，\n如是正月初一生者是火局，酉宫起初一日，就从酉宫起紫微，数无差迟，若错了则失之毫厘，差之千里矣。'

def source_provenance():
    b=SOURCE.read_bytes()
    if hashlib.sha256(b).hexdigest()!=SOURCE_SHA:raise ValueError('Original source raw SHA unexpectedly changed')
    s=b.decode('utf-8')
    if s.count(VERSE)!=1 or s.count(AUTHORIAL_EXAMPLE)!=1:
        raise ValueError('Original 14-star placement verse / worked example not exact')
    return {
      'original_Vol2_revision_oldid':1963110,
      'original_raw_SHA256':SOURCE_SHA,
      'original_14_star_verse_exact':VERSE,
      'original_14_star_verse_sha256':hashlib.sha256(VERSE.encode()).hexdigest(),
      'verse_start_original_codepoint_offset':s.index(VERSE),
      'verse_start_original_utf8_byte_offset':len(s[:s.index(VERSE)].encode()),
      'original_worked_example_exact':AUTHORIAL_EXAMPLE,
      'original_worked_example_sha256':hashlib.sha256(AUTHORIAL_EXAMPLE.encode()).hexdigest(),
      'modern_secondary_explainer_for_crossreading_only':'https://xingge.tw/en/quanshu/anming-zhuxing',
      'source_ancient_Ming_physical_edition_verified':False,
      'expert_textual_critical_collation_complete':False,
    }

def move(branch:str,n:int)->str:
    if branch not in BRANCHES or type(n)!=int:raise ValueError('Known 12-branch palace and integer relative offset required')
    return BRANCHES[(BRANCHES.index(branch)+n)%12]

def fourteen_star_palaces_given_ziwei(ziwei_branch:str):
    if ziwei_branch not in BRANCHES:raise ValueError('A known original ZiWei birth-star palace required')
    tianfu=tianfu_from_ziwei(ziwei_branch)
    z={roman:move(ziwei_branch,offset) for roman,chinese,offset in ZGROUP}
    f={roman:move(tianfu,offset) for roman,chinese,offset in FGROUP}
    assert len(z)==6 and len(f)==8 and len(z|f)==14
    return {'ziwei_base_branch':ziwei_branch,'tianfu_base_branch':tianfu,
       'counterclockwise_six_ziwei_group':z,'clockwise_eight_tianfu_group':f,
       'all_fourteen_primary_stars_conditional_on_source_palaces':z|f,
       'group_star_counts':{'ZiWeiGroup':6,'TianFuGroup':8},
       'source_trine_TanLang_QiSha_PoJun_spacing_equals_four_houses':True,
       'physical_early_Ming_original_authenticated':False,
       'independent_original_birth_calendar_computed_and_verified':False,
       'personal_predictions_validated':0}

def fourteen_source_candidate_given_year_life_day(yearstem:str,life_branch:str,lunar_day:int,
            *,source_edition_policy:str='strict_oldid1963110'):
    bureau=source_bureau_with_explicit_edition_policy(yearstem,life_branch,edition_policy=source_edition_policy)
    b=bureau['effective_bureau_candidate_under_requested_source_policy']
    if b is None:
        return {'input_birth_yearstem':yearstem,'input_life_palace':life_branch,'input_lunar_day':lunar_day,
          'source_edition_policy':source_edition_policy,'source_bureau':bureau,
          'source_ZiWei_lunar_day_original':None,'conditional_fourteen_stars':None,
          'result_status':'UNRESOLVED_SOURCE_NAYIN_GLYPH_CONFLICT', 'full_historical_birth_chart_parity_verified':False,
          'human_predictions_validated':0}
    grid=candidate_given_bureau_day(b,lunar_day)
    star=grid.literal_ziwei_branch_if_single_source_label
    result=None if star is None else fourteen_star_palaces_given_ziwei(star)
    return {'input_birth_yearstem':yearstem,'input_life_palace':life_branch,'input_lunar_day':lunar_day,
      'source_edition_policy':source_edition_policy,'source_bureau':bureau,
      'source_ZiWei_lunar_day_original':grid.__dict__ if hasattr(grid,'__dict__') else {
         k:getattr(grid,k) for k in grid.__dataclass_fields__},
      'conditional_fourteen_stars':result,
      'result_status':'UNRESOLVED_ORIGINAL_BUREAU_DAY_TABLE_DUPLICATE_OR_MISSING' if result is None else 'FOURTEEN_SOURCE_CONDITIONAL_STAR_PALACES_CALCULATED_NOT_NATAL_VALIDATED',
      'full_historical_birth_chart_parity_verified':False,'human_predictions_validated':0}

def twelve_anchor_configurations():
    all_maps=[fourteen_star_palaces_given_ziwei(b) for b in BRANCHES]
    for r in all_maps:
        val=r['all_fourteen_primary_stars_conditional_on_source_palaces']
        pos=[BRANCHES.index(val[x]) for x in ('TanLang','QiSha','PoJun')]
        assert (pos[0]-pos[1])%12==8
        assert (pos[1]-pos[0])%12==4 and (pos[2]-pos[1])%12==4
        assert val['ZiWei']==r['ziwei_base_branch'] and val['TianFu']==r['tianfu_base_branch']
    example=fourteen_source_candidate_given_year_life_day('Jia','Yin',1)
    assert example['conditional_fourteen_stars']['ziwei_base_branch']=='You'
    return {'schema':'ZIWEI_FOURTEEN_MAJOR_STARS_SOURCE_CONDITIONAL_RHYME_V1',
      'original_source_witness':source_provenance(),
      'basis':'Given ZiWei original day/bureau palace, derive TianFu mirror and 6 counterclockwise/8 clockwise major stars by exact classical mnemonic gaps.',
      'source_branches':'Zi,Chou,Yin,Mao,Chen,Si,Wu,Wei,Shen,You,Xu,Hai',
      'original_star_source_six_group':[{'name':x,'original_Chinese':y,'relative_branch_offset':o} for x,y,o in ZGROUP],
      'original_star_source_eight_group':[{'name':x,'original_Chinese':y,'relative_branch_offset':o} for x,y,o in FGROUP],
      'source_14_stars_derived_for_all_12_possible_ZiWei_base_branches':True,
      'all_12_anchor_configurations':all_maps,
      'unretuned_authorial_JiaYin_Fire_day1_exemplary_14_star_result':example,
      'not_an_independently_verified_classical_birth_chart':True,
      'source_malformed_grid_and_nayin_labels_remaining':True,
      'birth_year_timezone_lunar_leap_month_and_true_solar_time_parity_verified':False,
      'full_actual_birth_natal_chart_calculation_independently_verified':False,
      'past_or_future_real_human_predictions_validated':0,'runtime_promotions':0}

def main():
    p=Path(__file__).resolve().parent/'ZIWEI_14_STARS_12_ANCHORS_SOURCE_CONDITIONAL_20261020.json'
    obj=twelve_anchor_configurations()
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    ex=obj['unretuned_authorial_JiaYin_Fire_day1_exemplary_14_star_result']['conditional_fourteen_stars']
    print(json.dumps({'anchors':12,'stars_per_anchor':14,'original_example':{'ZiWei':ex['ziwei_base_branch'],'TianFu':ex['tianfu_base_branch']},
      'complete_natal_chart_verified':False,'human_predictions_validated':0},indent=2))
if __name__=='__main__':main()
