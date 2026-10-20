#!/usr/bin/env python3
"""Literal audit of five old Zi Wei day->palace ASCII grids; fail visible.

Each source cell places a tens prefix (初/十/廿, occasionally 二/三) above a
unit-character row. This creates one or more calendar day labels. The first
source is transmitted Wikisource oldid1963110, NOT authenticated original
woodblock; this module only reconstructs its written labels and conflicts.
It does not decide Gregorian->Chinese date, source bureau, birthday star, or
actual person outcomes. Duplicate/missing day slots are retained explicitly.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-07/SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json'
ORIGINAL=ROOT/'tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt'
SOURCE_SHA='1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72'
BRANCH_ROWS=((2,3,5,('Si','Wu','Wei','Shen')),(8,9,11,('Chen',None,'You')),(14,15,17,('Mao',None,'Xu')),(20,21,23,('Yin','Chou','Zi','Hai')))
ORIGINAL_BRANCHES=('巳','午','未','申','辰','','酉','卯','','戌','寅','丑','子','亥')
DIGITS='一二三四五六七八九十'
PREFIXES={'初':0,'十':10,'廿':20,'二':20,'三':30}

def split_row(line: str):
    if not line.startswith('|') or not line.endswith('|'):
        raise ValueError('Original ASCII grid cell boundary missing: '+repr(line))
    return [s.strip().replace(' ','') for s in line.split('|')[1:-1]]

def decode_digit(prefix:str,unit:str)->int:
    if prefix not in PREFIXES or unit not in DIGITS:
        raise ValueError('Unknown original numeric glyph pairing '+prefix+unit)
    # 二十 / 三十 are stand-alone Chinese numerals 20 / 30, not 30/40.
    if prefix in ('二','三'):
        if unit!='十':raise ValueError('Unexpected 二/三 + unit pairing '+prefix+unit)
        return PREFIXES[prefix]
    value=PREFIXES[prefix]+DIGITS.index(unit)+1
    if not 1<=value<=30:raise ValueError('Printed day numeral outside 1..30: '+prefix+unit)
    return value


def build_result():
    src=json.loads(SOURCE.read_text(encoding='utf-8'))
    assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()==SOURCE_SHA
    assert src['whole_raw_original_SHA256']==SOURCE_SHA
    assert src['diagram_count']==5 and len(src['diagram_reversible_witnesses'])==5
    result=[]
    for witness in src['diagram_reversible_witnesses']:
        text=witness['diagram_content'];b=text.encode('utf-8')
        assert hashlib.sha256(b).hexdigest()==witness['original_utf8_sha256']
        assert ORIGINAL.read_text(encoding='utf-8')[witness['original_codepoint_start']:witness['original_codepoint_end']]==text
        lines=text.splitlines()
        if len(lines)!=25:raise ValueError('Grid structure unexpectedly changed')
        assignments=defaultdict(list);raw_cells=[];glyph_labels=[]
        for row_prefix,row_unit,row_branch,branches in BRANCH_ROWS:
            pref=split_row(lines[row_prefix]);units=split_row(lines[row_unit]);names=split_row(lines[row_branch]);
            if len(pref)!=len(units) or len(names)!=len(pref) or len(pref)!=len(branches):
                raise ValueError('Cell splitting did not preserve columns')
            for i,branch in enumerate(branches):
                assert len(names[i])<=1
                if branch is None:
                    assert not pref[i] and not units[i] and names[i]==''
                    continue
                assert names[i] in ORIGINAL_BRANCHES and names[i] !='',(witness['bureau'],branch,names[i])
                if len(pref[i])!=len(units[i]):raise ValueError('Vertical source glyphs not parallel')
                for pre,unit in zip(pref[i],units[i]):
                    day=decode_digit(pre,unit)
                    assignments[day].append(branch)
                    glyph_labels.append({'day':day,'palace_earthly_branch':branch,'original_prefix_glyph':pre,'original_unit_glyph':unit,'original_combined_glyph':pre+unit})
                raw_cells.append({'palace':branch,'prefix_row':pref[i],'unit_row':units[i],'printed_earthly_branch':names[i]})
        duplicate={str(day):list(locs) for day,locs in sorted(assignments.items()) if len(locs)>1}
        missing=[d for d in range(1,31) if d not in assignments]
        source_map={str(day):assignments[day][0] for day in sorted(assignments) if len(assignments[day])==1}
        result.append({'original_source_bureau':witness['bureau'],'original_absolute_codepoint_span':[witness['original_codepoint_start'],witness['original_codepoint_end']],
          'original_grid_utf8_SHA256':witness['original_utf8_sha256'],
          'transmitted_original_label_count':len(glyph_labels),'unique_lunar_days_present':len(assignments),
          'day_to_palace_only_when_single_original_label':source_map,
          'duplicate_original_day_assignments':duplicate,'missing_days_1_to_30':missing,
          'raw_cell_labels_reversible':raw_cells,'literal_decoded_day_glyphs':glyph_labels,
          'can_assert_complete_day_placement_from_this_source_only':len(missing)==0 and len(duplicate)==0})
    return {'schema':'ZIWEI_FIVE_ORIGINAL_BUREAU_DAY_GRID_LITERAL_DECODER_V1',
       'source_Chinese_Wikisource_oldid':1963110,'source_original_full_text_sha256':SOURCE_SHA,
       'source_author_original_printing_authenticated':False,
       'scope':'Recover written day labels from vertically stacked original ASCII source grids, NO birthday/calendar engine and no actual star positions unless input bureau and literal table both verified.',
       'total_source_diagrams':len(result),
       'total_missing_day_labels':sum(len(x['missing_days_1_to_30']) for x in result),
       'total_duplicate_day_labels':sum(len(x['duplicate_original_day_assignments']) for x in result),
       'all_five_grid_day_maps_unique_and_complete':all(x['can_assert_complete_day_placement_from_this_source_only'] for x in result),
       'source_to_birth_calendar_engine_parity_verified':False,
       'astronomical_birthhour_month_bureau_mapping_verified':False,
       'empirical_real_person_prediction_validation':0,'runtime_astrology_model_promotions':0,
       'source_original_diagrams_decoded_with_explicit_anomalies':result}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();obj=build_result();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'diagrams':obj['total_source_diagrams'],'all_complete':obj['all_five_grid_day_maps_unique_and_complete'],'duplicates':obj['total_duplicate_day_labels'],'missing':obj['total_missing_day_labels'],'by_bureau':{x['original_source_bureau']:{'labels':x['transmitted_original_label_count'],'duplicates':x['duplicate_original_day_assignments'],'missing':x['missing_days_1_to_30']} for x in obj['source_original_diagrams_decoded_with_explicit_anomalies']}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
