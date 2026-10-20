#!/usr/bin/env python3
"""Source-conditioned Zi Wei => Tian Fu palace mirror, not a full natal star engine.

Source: transmitted 紫微斗數全書 Volume II, oldid 1963110, exactly frozen
original diagram 安天府图 in ChineseAstro-08. Its text says co-palace in Yin
and Shen; for example Zi Wei in Chou corresponds to Tian Fu in Mao.
One simple cyclic reflection (fixed at Yin=2 and Shen=8) is consistent with
both source statements and the diagram. It must not be represented as an
independently authenticated Ming original or a validated birth chart.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
EXCERPT=ROOT/'tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-08/SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt'
SOURCE=ROOT/'tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-08/ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json'
BRANCHES=('Zi','Chou','Yin','Mao','Chen','Si','Wu','Wei','Shen','You','Xu','Hai')

def source_witness():
    text=EXCERPT.read_text(encoding='utf-8');notes=json.loads(SOURCE.read_text(encoding='utf-8'))
    sha=hashlib.sha256(EXCERPT.read_bytes()).hexdigest()
    if sha!=notes['original_excerpt_sha256']:
        raise ValueError('Original Chinese source diagram changed; fail closed')
    if '天府惟寅申二宫紫府同宫' not in text or '如紫居丑则府' not in text or '居卯矣' not in text:
        raise ValueError('Original Tian Fu relative-placement source conditions missing')
    return {'original_oldid':notes['original_raw_oldid'],'original_Chinese_excerpt_sha256':sha,
            'source_original_diagram_witness_sha256':notes['record_rows'][0]['source_quote_utf8_sha256'],
            'independent_physical_early_edition_authenticated':False}

def tianfu_from_ziwei(ziwei_branch: str) -> str:
    """Conditional branch permutation for a GIVEN Zi Wei branch; not birth inference."""
    if ziwei_branch not in BRANCHES:
        raise ValueError('Zi Wei branch must be a known one of the 12 palaces')
    i=BRANCHES.index(ziwei_branch)
    return BRANCHES[(4-i)%12]

def source_conditional_map():
    return {'schema':'ZIWEI_TIANFU_CONDITIONAL_MIRROR_12_PALACES_V1',
            'source_witness':source_witness(),
            'derivation':'Involution i -> (4-i) mod12, reflecting 12 branches about fixed Yin and Shen axes, consistent with accepted transmitted reference diagram and Chou/Mao example.',
            'branch_order':list(BRANCHES),
            'tianfu_branch_if_given_ziwei_branch':{b:tianfu_from_ziwei(b) for b in BRANCHES},
            'ziwei_principal_star_birth_palace_known_from_calendar':False,
            'independently_verified_against_classical_early_source_or_golden_chart':False,
            'can_generate_fourteen_principal_stars':False,
            'human_outcomes_and_predictions_validated':0,
            'runtime_astrology_promotions':0}

def main():
    p=ROOT/'tasks/astro-independent-parity-20261020/ZIWEI_TIANFU_CONDITIONAL_MAP_20261020.json'
    p.write_text(json.dumps(source_conditional_map(),ensure_ascii=False,indent=2)+'\n')
    print('conditional Zi Wei/Tian Fu branch mapping recorded, full natal star engine still unavailable')
if __name__=='__main__':main()
